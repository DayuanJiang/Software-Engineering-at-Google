"""Chapter 13 review manifest and offline protection checks; chapter-only writes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
SOURCE = "zh-cn/Chapter-13_Test_Doubles/Chapter-13_Test_Doubles.md"
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

RETAINED = [
    47, 50, 70, 184, 267, 300, 335, 369, 398, 408, 430, 604,
    621, 627, 637, 643, 726, 792, 799, 812, 836, 843, 934, 948,
]
HELD = {
    "132": (
        "Existing Chinese translator supplement inside the txt fence at lines "
        "131-133. Read for context, preserved byte-for-byte under the code-block "
        "restriction; not counted as completed Chinese polishing."
    ),
}
PUNCTUATION = {",": "，", ";": "；", ":": "：", "?": "？", "!": "！", "(": "（", ")": "）"}
QUOTES = {"「": "“", "」": "”", "『": "‘", "』": "’"}
PROTECTED_INLINE = re.compile(
    r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>]+"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def chinese(char):
    return bool(audit.HAN.search(char)) or char in "“”‘’·—…《》〈〉【】、。，！？；：（）"


def prefix(line):
    if line.lstrip().startswith(("#", "*Example ")):
        match = audit.HAN.search(line)
        if match:
            return line[:match.start()]
    return ""


def normalize_punctuation(line):
    protected = set(range(len(prefix(line))))
    for match in PROTECTED_INLINE.finditer(line):
        protected.update(range(match.start(), match.end()))
    chars = list(line)
    opening = True
    for i, char in enumerate(chars):
        if i in protected:
            continue
        if char == '"':
            chars[i] = "“" if opening else "”"
            opening = not opening
        elif char in QUOTES:
            chars[i] = QUOTES[char]
        elif char in PUNCTUATION:
            left = chars[i - 1] if i else ""
            right = chars[i + 1] if i + 1 < len(chars) else ""
            if chinese(left) or chinese(right):
                chars[i] = PUNCTUATION[char]
    return "".join(chars)


def inputs():
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Unexpected baseline commit")
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"]
    )
    require(
        audit.digest(original) == baseline["files"][SOURCE]["sha256"],
        "Original Git snapshot differs from baseline",
    )
    return baseline, original, (ROOT / SOURCE).read_bytes()


def block_shape(text):
    return [
        (t.type, t.tag, t.nesting, t.level, t.map, t.markup, t.info)
        for t in audit.MD.parse(text)
    ]


def validate(baseline, original, current, manifest):
    require(manifest["source"] == SOURCE, "Unexpected manifest source")
    require(manifest["baseline_sha256"] == audit.digest(original), "Manifest hash mismatch")
    old_text, new_text = original.decode("utf-8"), current.decode("utf-8")
    old, new = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
    require(len(old) == len(new), "Line count changed")
    han = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    replacements = {int(k): v for k, v in manifest["replacements"].items()}
    retained = set(manifest["reviewed_unchanged_lines"])
    held = {int(k) for k in manifest["held_lines"]}
    require(manifest["reviewed_unchanged_lines"] == RETAINED, "Retained review list changed")
    require(manifest["held_lines"] == HELD, "Hold record changed")
    require(changed == set(replacements), "Manifest differs from actual edits")
    require(not (changed & retained or changed & held or retained & held), "Coverage overlap")
    require(changed | retained | held == han, "Incomplete Chinese line accounting")

    for number, (before, after) in enumerate(zip(old, new), 1):
        require(
            re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0],
            f"Indentation/blank line changed: {number}",
        )
        require(
            re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
            f"Trailing whitespace/line ending changed: {number}",
        )
        require(after.startswith(prefix(before)), f"English prefix changed: {number}")
        if number in changed:
            replacement = replacements[number]
            require(isinstance(replacement, str), f"Invalid replacement: {number}")
            require("\n" not in replacement and "\r" not in replacement, "Multiline edit")
            require(audit.HAN.search(replacement), f"Chinese removed: {number}")
            require(after.rstrip("\r\n") == replacement, f"Replacement mismatch: {number}")
        if number in han - held:
            require(normalize_punctuation(after) == after, f"Punctuation residual: {number}")

    old_doc = audit.parse_document(SOURCE, old_text)
    new_doc = audit.parse_document(SOURCE, new_text)
    before, after = audit.protected(old_doc), audit.protected(new_doc)
    require(before == baseline["files"][SOURCE], "Parser differs from stored baseline")
    for key in before:
        if key != "sha256":
            require(before[key] == after[key], f"Protected field changed: {key}")
    require(block_shape(old_text) == block_shape(new_text), "Markdown block shape changed")
    for key in ("codes", "links", "footnotes", "html", "explicit_ids"):
        require(old_doc[key] == new_doc[key], f"Content or positions changed: {key}")

    protected_lines = set()
    for token in audit.MD.parse(old_text):
        if token.type in {"fence", "code_block"}:
            protected_lines.update(range(token.map[0] + 1, token.map[1] + 1))
    require(not changed & protected_lines, "A code-block line changed")
    require(held == han & protected_lines, "Chinese code-block holds are incomplete")
    return {
        "status": "protection_pass_with_editorial_hold",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(current),
        "physical_lines_read": len(old),
        "original_chinese_lines": len(han),
        "chinese_lines_inspected_including_holds": len(han),
        "completed_chinese_lines": len(changed | retained),
        "edited_chinese_lines": len(changed),
        "reviewed_unchanged_count": len(retained),
        "reviewed_unchanged_lines": sorted(retained),
        "held_lines": manifest["held_lines"],
        "non_chinese_lines_unchanged": len(old) - len(han),
        "english_source_lines": len(before["english_line_hashes"]),
        "english_segments": len(before["english_segment_hashes"]),
        "protected_code_items": len(before["code_hashes"]),
        "links": len(before["links"]),
        "structural_items": len(before["structures"]),
        "html_items": len(before["html_hashes"]),
        "footnote_markers": len(before["footnotes"]),
        "punctuation_residuals_outside_hold": 0,
        "protection_exceptions": [],
        "chapter_only": True,
        "checks": [
            "fixed Git snapshot and original parser output match stored baseline",
            "exact replacement manifest and disjoint edited/retained/held coverage",
            "non-Chinese lines and English heading/caption prefixes unchanged",
            "all existing translation_audit protection fields except file hash unchanged",
            "Markdown block types, nesting, levels, source maps and markers unchanged",
            "code, comments, links, HTML and footnotes unchanged including positions",
            "line order/count, blank lines, indentation, trailing whitespace and endings unchanged",
            "mechanical punctuation normalization is idempotent outside held code",
        ],
        "limitations": [
            "Code examples read but not compiled or corrected",
            "Local source ambiguities and protected link-label typo recorded in notes.md",
            "No online source comparison, external-link checks or browser rendering",
            "One Chinese translator supplement held, not marked completed",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--normalize", action="store_true")
    mode.add_argument("--record", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    baseline, original, current = inputs()
    if args.normalize:
        old = original.decode("utf-8").splitlines(keepends=True)
        lines = current.decode("utf-8").splitlines(keepends=True)
        require(len(old) == len(lines), "Line count changed before normalization")
        normalized = [
            normalize_punctuation(line)
            if audit.HAN.search(before) and str(i) not in HELD else line
            for i, (before, line) in enumerate(zip(old, lines), 1)
        ]
        count = sum(a != b for a, b in zip(lines, normalized))
        if count:
            (ROOT / SOURCE).write_bytes("".join(normalized).encode("utf-8"))
        print(json.dumps({"mechanically_normalized_lines": count}))
        return
    if args.record:
        require(not (REVIEW / "edits.json").exists(), "Refusing to overwrite manifest")
        old, new = original.decode("utf-8").splitlines(), current.decode("utf-8").splitlines()
        manifest = {
            "source": SOURCE,
            "baseline_sha256": baseline["files"][SOURCE]["sha256"],
            "replacements": {str(i): b for i, (a, b) in enumerate(zip(old, new), 1) if a != b},
            "reviewed_unchanged_lines": RETAINED,
            "held_lines": HELD,
        }
    else:
        manifest = json.loads((REVIEW / "edits.json").read_text())
    result = validate(baseline, original, current, manifest)
    if args.record:
        (REVIEW / "edits.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.write_report:
        (REVIEW / "verification.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
