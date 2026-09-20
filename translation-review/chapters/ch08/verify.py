"""Verify Chapter 8 only, without modifying shared tools or baseline data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
SOURCE = (
    "zh-cn/Chapter-8_Style_Guides_and_Rules/"
    "Chapter-8_Style_Guides_and_Rules.md"
)
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

PUNCTUATION = {",": "，", ";": "；", ":": "：", "?": "？", "!": "！", "(": "（", ")": "）"}
QUOTES = {"「": "“", "」": "”", "『": "‘", "』": "’"}
LINK = re.compile(r"!?\[[^\]]*\]\([^)]*\)")
TAG = re.compile(r"<[^>]+>")
PROTECTED_INLINE = re.compile(
    r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>\"`]+"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def chinese(char):
    return bool(audit.HAN.search(char)) or char in "“”‘’·—…《》〈〉【】、。，！？；：（）"


def heading_prefix(line):
    han = audit.HAN.search(line)
    if han and re.match(r"^\s*(?:#+\s|\*\*)", line):
        return line[:han.start()]
    return ""


def normalize_punctuation(line):
    chars = list(line)
    protected = set(range(len(heading_prefix(line))))
    for match in PROTECTED_INLINE.finditer(line):
        protected.update(range(match.start(), match.end()))
    opening_quote = True
    for i, char in enumerate(chars):
        if i in protected:
            continue
        if char == '"':
            chars[i] = "“" if opening_quote else "”"
            opening_quote = not opening_quote
        elif char in QUOTES:
            chars[i] = QUOTES[char]
        elif char in PUNCTUATION:
            left = chars[i - 1] if i else ""
            right = chars[i + 1] if i + 1 < len(chars) else ""
            if chinese(left) or chinese(right):
                chars[i] = PUNCTUATION[char]
    return "".join(chars)


def block_shape(text):
    return [
        (token.type, token.tag, token.nesting, token.level, token.map)
        for token in audit.MD.parse(text)
    ]


def inline_shape(text):
    return [
        (token.map, [
            (child.type, child.tag, child.nesting, child.markup, child.attrs)
            for child in token.children or [] if child.type != "text"
        ])
        for token in audit.MD.parse(text) if token.type == "inline"
    ]


def verify():
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    manifest = json.loads((REVIEW / "edits.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Unexpected baseline commit")
    require(manifest["source"] == SOURCE, "Unexpected manifest source")
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"]
    )
    current = (ROOT / SOURCE).read_bytes()
    require(
        audit.digest(original) == baseline["files"][SOURCE]["sha256"]
        == manifest["baseline_sha256"],
        "Baseline hash mismatch",
    )
    old_text, new_text = original.decode("utf-8"), current.decode("utf-8")
    old, new = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
    require(len(old) == len(new), "Line count changed")
    chinese_lines = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changed = {i for i, pair in enumerate(zip(old, new), 1) if pair[0] != pair[1]}
    replacements = {int(k): v for k, v in manifest["replacements"].items()}
    require(
        len(replacements) == len(manifest["replacements"]),
        "Duplicate numeric replacement key",
    )
    retained = set(manifest["reviewed_unchanged_lines"])
    held = {int(k) for k in manifest["held_lines"]}
    require(changed == set(replacements), "Manifest does not match changed lines")
    require(not (changed & retained or changed & held or retained & held), "Coverage overlap")
    require(changed | retained | held == chinese_lines, "Incomplete Chinese line coverage")
    require(len(retained) == len(manifest["reviewed_unchanged_lines"]), "Duplicate retained line")
    require(all(manifest["held_lines"].values()), "Held lines require reasons")

    for number, (before, after) in enumerate(zip(old, new), 1):
        require(
            re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0],
            f"Indentation or blank line changed: {number}",
        )
        require(
            re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
            f"Trailing whitespace or line ending changed: {number}",
        )
        require(
            LINK.findall(before) == LINK.findall(after),
            f"Literal Markdown link changed: {number}",
        )
        require(
            TAG.findall(before) == TAG.findall(after),
            f"HTML or angle-bracket text changed: {number}",
        )
        prefix = heading_prefix(before)
        require(after.startswith(prefix), f"Heading prefix changed: {number}")
        if number not in changed:
            require(before == after, f"Unreviewed edit: {number}")
            continue
        replacement = replacements[number]
        require("\n" not in replacement and "\r" not in replacement, "Multiline replacement")
        require(bool(audit.HAN.search(replacement)), f"Chinese removed: {number}")
        require(after.rstrip("\r\n") == replacement, f"Replacement mismatch: {number}")

    # This complete English clause was already duplicated inside a Chinese footnote.
    embedded_english = "where multiple languages define general comment rules."
    require(
        old[335].count(embedded_english) == new[335].count(embedded_english) == 1,
        "Embedded English clause changed",
    )
    punctuation_residuals = [
        number for number in sorted(chinese_lines - held)
        if normalize_punctuation(new[number - 1]) != new[number - 1]
    ]
    require(not punctuation_residuals, f"Punctuation residuals: {punctuation_residuals}")

    before_doc = audit.parse_document(SOURCE, old_text)
    after_doc = audit.parse_document(SOURCE, new_text)
    before, after = audit.protected(before_doc), audit.protected(after_doc)
    require(before == baseline["files"][SOURCE], "Parser differs from original baseline")
    for key in before:
        if key != "sha256":
            require(before[key] == after[key], f"Protected field changed: {key}")
    require(block_shape(old_text) == block_shape(new_text), "Markdown block structure changed")
    require(inline_shape(old_text) == inline_shape(new_text), "Inline markup structure changed")
    require(before_doc["codes"] == after_doc["codes"], "Code content or position changed")
    require(before_doc["links"] == after_doc["links"], "Link content or position changed")
    require(before_doc["footnotes"] == after_doc["footnotes"], "Footnote position changed")
    code_chinese = [
        item["line"] for item in before_doc["codes"]
        if item["kind"] in {"fence", "code_block"} and audit.HAN.search(item["content"])
    ]
    return {
        "validation_status": "pass",
        "review_status": "complete_except_held" if held else "complete",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(current),
        "physical_lines": len(old),
        "original_chinese_lines": len(chinese_lines),
        "covered_chinese_lines": len(changed | retained | held),
        "completed_chinese_lines": len(changed | retained),
        "edited_chinese_lines": len(changed),
        "reviewed_unchanged_lines": sorted(retained),
        "held_lines": manifest["held_lines"],
        "english_source_lines": len(before["english_line_hashes"]),
        "english_segments": len(before["english_segment_hashes"]),
        "protected_code_items": len(before["code_hashes"]),
        "fenced_code_blocks": sum(c["kind"] == "fence" for c in before_doc["codes"]),
        "chinese_code_blocks": code_chinese,
        "links": len(before["links"]),
        "structural_items": len(before["structures"]),
        "html_items": len(before["html_hashes"]),
        "footnote_markers": len(before["footnotes"]),
        "punctuation_residuals_completed_lines": len(punctuation_residuals),
        "protection_exceptions": [],
        "chapter_only": True,
        "checks": [
            "fixed Git snapshot, baseline JSON and manifest hashes agree",
            "complete, disjoint changed/unchanged/held coverage with exact replacements",
            "non-Chinese source lines preserved byte-for-byte",
            "English heading prefixes and embedded English source clause preserved",
            "all shared translation_audit protections pass without exceptions",
            "Markdown block types, levels, nesting and source maps preserved",
            "inline markup, literal Markdown links and angle-bracket content preserved",
            "code, links and footnotes preserved including their positions",
            "blank lines, indentation, trailing whitespace and line endings preserved",
            "punctuation normalization idempotent on every completed Chinese line",
        ],
        "limitations": [
            "held lines are covered but not counted as completed",
            "known source defects are preserved and documented in notes.md",
            "external URLs and historical claims were not refreshed",
            "semantic review was manual; structural checks do not prove translation quality",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    result = json.dumps(verify(), ensure_ascii=False, indent=2) + "\n"
    if args.write_report:
        (REVIEW / "verification-detailed.json").write_text(result, encoding="utf-8")
    print(result, end="")
