"""Validate only Chapter 10 against the fixed original snapshot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
SOURCE = "zh-cn/Chapter-10_Documentation/Chapter-10_Documentatio.md"
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

# These lines were individually reviewed, not inferred from an empty diff.
RETAINED = [
    6, 30, 45, 136, 174, 188, 224, 240, 241, 242, 243, 250, 268,
    290, 310, 347, 365, 389, 462, 494, 521, 568, 582, 618, 632, 646,
]
HOLDS = {
    "397": (
        "The documentation sample has translated SQL keywords and 'Type' into "
        "Chinese. Preserve the whole sample line pending permission to repair "
        "sample literals; do not count this line as completed."
    ),
    "610": (
        "Chinese text is inside the fenced freshness-metadata documentation "
        "sample. Preserve the entire code block, its HTML-like delimiters, "
        "inline backticks, owner field and date; not editorially completed."
    ),
}
PUNCTUATION = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))
QUOTES = {
    "\u300c": "\u201c", "\u300d": "\u201d",
    "\u300e": "\u2018", "\u300f": "\u2019",
}
INLINE = re.compile(r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>]+")
ENGLISH_QUOTE = re.compile(r"\u201c([^\u3400-\u9fff\u201c\u201d]+)\u201d")
SAMPLE_LITERALS = {
    294: ["Foo", "x", "y", "z", "Bar", "Baz"],
    334: ["Returns:", "Throws:"],
    395: ["foobar", "baz"],
    397: ["my_foobar_db"],
    450: ["foobar", "baz", "shell"],
    563: ["Frobber"],
    616: ["Last Review by\u2026"],
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_chinese(char):
    return bool(audit.HAN.search(char)) or char in (
        "\u201c\u201d\u2018\u2019\u00b7\u2014\u2026\u300a\u300b"
        "\u3008\u3009\u3010\u3011\u3001\u3002\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09"
    )


def normalize_punctuation(line):
    chars = list(line)
    protected = set()
    first_han = audit.HAN.search(line)
    if first_han and re.match(r"^\s*(?:#|\*{1,2})", line):
        protected.update(range(first_han.start()))
    for match in INLINE.finditer(line):
        protected.update(range(match.start(), match.end()))
    # English labels in the documentation examples retain their own punctuation.
    for match in ENGLISH_QUOTE.finditer(line):
        if re.search(r"[A-Za-z]", match[1]):
            protected.update(range(match.start(1), match.end(1)))
    opening = True
    for i, char in enumerate(chars):
        if i in protected:
            continue
        if char == '"':
            chars[i] = "\u201c" if opening else "\u201d"
            opening = not opening
        elif char in QUOTES:
            chars[i] = QUOTES[char]
        elif char in PUNCTUATION:
            left = chars[i - 1] if i else ""
            right = chars[i + 1] if i + 1 < len(chars) else ""
            if is_chinese(left) or is_chinese(right):
                chars[i] = PUNCTUATION[char]
    return "".join(chars)


def markdown_shape(source):
    blocks, inline = [], []
    for token in audit.MD.parse(source):
        blocks.append((
            token.type, token.tag, token.nesting, token.level, token.map,
            token.markup, token.info, token.attrs,
        ))
        if token.children:
            inline.append([
                (child.type, child.tag, child.nesting, child.markup, child.attrs)
                for child in token.children
            ])
    return blocks, inline


def validate(original, current, manifest, baseline):
    require(manifest["source"] == SOURCE, "Manifest source mismatch")
    require(
        audit.digest(original) == manifest["baseline_sha256"]
        == baseline["files"][SOURCE]["sha256"],
        "Baseline SHA-256 mismatch",
    )
    old_text, new_text = original.decode("utf-8"), current.decode("utf-8")
    old, new = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
    require(len(old) == len(new), "Physical line count changed")
    chinese = {i for i, text in enumerate(old, 1) if audit.HAN.search(text)}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    replacements = {int(k): v for k, v in manifest["replacements"].items()}
    retained = set(manifest["reviewed_unchanged_lines"])
    held = {int(k) for k in manifest["held_lines"]}
    require(set(replacements) == changed, "Replacement keys differ from actual changes")
    require(manifest["reviewed_unchanged_lines"] == RETAINED, "Retained review record changed")
    require(manifest["held_lines"] == HOLDS, "Hold record changed")
    require(not (changed & retained or changed & held or retained & held), "Coverage overlap")
    require(changed | retained | held == chinese, "Incomplete Chinese coverage")
    require(len(retained) == len(RETAINED), "Duplicate retained line")

    for number, (before, after) in enumerate(zip(old, new), 1):
        require(
            re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0],
            f"Indentation or blank line changed: {number}",
        )
        require(
            re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
            f"Line ending or trailing whitespace changed: {number}",
        )
        if number not in changed:
            continue
        require(number in chinese, f"Non-Chinese line changed: {number}")
        value = replacements[number]
        require(isinstance(value, str) and "\n" not in value and "\r" not in value,
                f"Invalid replacement: {number}")
        require(after.rstrip("\r\n") == value, f"Replacement text differs: {number}")
        require(bool(audit.HAN.search(after)), f"Chinese content removed: {number}")
        require(normalize_punctuation(value) == value, f"Punctuation residual: {number}")
        if re.match(r"^\s*(?:#|\*{1,2})", before):
            prefix = before[:audit.HAN.search(before).start()]
            require(after.startswith(prefix), f"English heading prefix changed: {number}")
        require(INLINE.findall(before) == INLINE.findall(after),
                f"Inline code, markup or link changed: {number}")

    for number, literals in SAMPLE_LITERALS.items():
        for literal in literals:
            require(literal in old[number - 1], f"Invalid sample guard: {number}")
            require(old[number - 1].count(literal) == new[number - 1].count(literal),
                    f"Documentation sample literal changed: {number}: {literal}")

    before_doc = audit.parse_document(SOURCE, old_text)
    after_doc = audit.parse_document(SOURCE, new_text)
    before, after = audit.protected(before_doc), audit.protected(after_doc)
    require(before == baseline["files"][SOURCE], "Original parser output differs from baseline")
    for key in before:
        if key != "sha256":
            require(before[key] == after[key], f"Protected field changed: {key}")
    require(markdown_shape(old_text) == markdown_shape(new_text), "Markdown token structure changed")
    for key in ("codes", "links", "html", "footnotes", "explicit_ids"):
        require(before_doc[key] == after_doc[key], f"Content or position changed: {key}")

    return {
        "status": "pass",
        "editorial_status": "complete_except_protected_holds",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(current),
        "physical_lines": len(old),
        "inspected_chinese_lines": len(chinese),
        "completed_chinese_lines": len(changed | retained),
        "edited_chinese_lines": len(changed),
        "reviewed_unchanged_lines": sorted(retained),
        "held_lines": manifest["held_lines"],
        "english_source_lines": len(before["english_line_hashes"]),
        "english_segments": len(before["english_segment_hashes"]),
        "protected_code_items": len(before["code_hashes"]),
        "links": len(before["links"]),
        "structural_items": len(before["structures"]),
        "html_items": len(before["html_hashes"]),
        "footnote_markers": len(before["footnotes"]),
        "punctuation_residuals_on_completed_chinese_lines": 0,
        "protection_exceptions": [],
        "chapter_only": True,
        "checks": [
            "Fixed Git snapshot, baseline file hash and parsed baseline agree.",
            "Chinese changed, retained and held lines form a disjoint complete partition.",
            "Replacement lines match the edited chapter exactly.",
            "All non-Chinese source lines remain byte-identical.",
            "English heading prefixes, inline markup and sample literals are preserved.",
            "All shared audit protection fields except the chapter hash match.",
            "Markdown block and inline token shapes, attributes and source maps match.",
            "Code, HTML, links and footnotes match, including source positions.",
            "Indentation, blank lines, line endings and trailing whitespace match.",
            "Chinese punctuation normalization leaves all completed Chinese lines unchanged.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Baseline commit mismatch")
    original = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"])
    current = (ROOT / SOURCE).read_bytes()
    if args.write_manifest:
        old, new = original.decode().splitlines(), current.decode().splitlines()
        manifest = {
            "source": SOURCE,
            "baseline_sha256": baseline["files"][SOURCE]["sha256"],
            "replacements": {str(i): b for i, (a, b) in enumerate(zip(old, new), 1) if a != b},
            "reviewed_unchanged_lines": RETAINED,
            "held_lines": HOLDS,
        }
    else:
        manifest = json.loads((REVIEW / "edits.json").read_text())
    result = validate(original, current, manifest, baseline)
    # Retained lines are also checked; held samples are deliberately not normalized.
    for number in RETAINED:
        text = current.decode().splitlines()[number - 1]
        require(normalize_punctuation(text) == text, f"Retained punctuation residual: {number}")
    if args.write_manifest:
        audit.dump(REVIEW / "edits.json", manifest)
    if args.write_report:
        audit.dump(REVIEW / "verification.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
