"""Validate Chapter 17 only; optionally record its reviewed edits and report."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
SOURCE = "zh-cn/Chapter-17_Code_Search/Chapter-17_Code_Search.md"
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

RETAINED = [
    6, 40, 56, 72, 86, 96, 102, 112, 122, 128, 162, 196, 210,
    236, 252, 260, 291, 331, 359, 389, 481, 495,
]
HELD = {}
EXAMPLES = {
    (82, 84): ["cool_hash.h"],
    (114, 116): ["Git", "blame"],
    (315, 317): ["include/import"],
    (319, 321): ["include/import", "Kythe"],
    (337, 339): ["Point", "Point *p", "appointed to the council"],
    (341, 343): ["base", "myproject"],
    (345, 347): ["Alert", "Monitor", "absl", "absl::Monitor::Alert"],
    (411, 413): ['\u201ci\u201d'],
    (417, 419): ["head", "Git", "Mercurial"],
    (453, 455): ["function()", "function(x)", "(x ^ y)", "=== myClass"],
    (457, 459): ["CamelCase", "snake_case", "justmashedtogether"],
    (461, 463): ['\u201cr\u201d', '\u201cR\u201d', "searching", "searched", "search"],
}
PUNCTUATION = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))
QUOTES = dict(zip("\u300c\u300d\u300e\u300f", "\u201c\u201d\u2018\u2019"))
PROTECTED_INLINE = re.compile(
    r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>]+"
    r"|\u201c[^\u3400-\u9fff\u201d\n]*[A-Za-z][^\u3400-\u9fff\u201d\n]*\u201d"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def chinese(char):
    return bool(audit.HAN.search(char)) or char in (
        "\u201c\u201d\u2018\u2019\u00b7\u2014\u2026\u300a\u300b"
        "\u3008\u3009\u3010\u3011\u3001\u3002\uff0c\uff01\uff1f"
        "\uff1b\uff1a\uff08\uff09"
    )


def heading_prefix(line):
    match = audit.HAN.search(line)
    return line[:match.start()] if match and line.lstrip().startswith("#") else ""


def normalize_punctuation(line):
    protected = set(range(len(heading_prefix(line))))
    for match in PROTECTED_INLINE.finditer(line):
        protected.update(range(match.start(), match.end()))
    chars = list(line)
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
            if chinese(left) or chinese(right):
                chars[i] = PUNCTUATION[char]
    return "".join(chars)


def markup_shape(tokens):
    return [
        (
            t.type, t.tag, t.nesting, t.level, t.map, t.markup, t.info,
            t.attrs, markup_shape(t.children or []),
        )
        for t in tokens
    ]


def inputs():
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Unexpected baseline commit")
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"]
    )
    require(
        audit.digest(original) == baseline["files"][SOURCE]["sha256"],
        "Original Git snapshot differs from stored baseline",
    )
    return baseline, original, (ROOT / SOURCE).read_bytes()


def validate(baseline, original, current, manifest):
    require(manifest["source"] == SOURCE, "Manifest source mismatch")
    require(manifest["baseline_sha256"] == audit.digest(original), "Manifest hash mismatch")
    old_text, new_text = original.decode("utf-8"), current.decode("utf-8")
    old, new = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
    require(len(old) == len(new), "Physical line count changed")
    han = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    replacements = {int(k): v for k, v in manifest["replacements"].items()}
    retained = set(manifest["reviewed_unchanged_lines"])
    held = {int(k) for k in manifest["held_lines"]}
    require(manifest["reviewed_unchanged_lines"] == RETAINED, "Retained review changed")
    require(manifest["held_lines"] == HELD, "Hold record changed")
    require(changed == set(replacements), "Manifest differs from actual edits")
    require(not (changed & retained or changed & held or retained & held), "Coverage overlaps")
    require(changed | retained | held == han, "Chinese review coverage is incomplete")
    require(changed <= han, "Non-Chinese source line changed")

    categories = Counter()
    for number, (before, after) in enumerate(zip(old, new), 1):
        require(
            re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0],
            f"Indentation or blank line changed: {number}",
        )
        require(
            re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
            f"Trailing whitespace or line ending changed: {number}",
        )
        require(after.startswith(heading_prefix(before)), f"English heading changed: {number}")
        if number in changed:
            value = replacements[number]
            require(isinstance(value, str) and "\n" not in value and "\r" not in value,
                    f"Invalid replacement: {number}")
            require(after.rstrip("\r\n") == value, f"Replacement differs: {number}")
            require(audit.HAN.search(value), f"Chinese line removed: {number}")
        if number in han:
            require(normalize_punctuation(after) == after, f"Punctuation residual: {number}")
            category = (
                "headings" if before.startswith("#") else
                "footnotes" if before.startswith(">") else
                "list_items" if before.startswith("- ") else "body"
            )
            categories[category] += 1

    old_doc = audit.parse_document(SOURCE, old_text)
    new_doc = audit.parse_document(SOURCE, new_text)
    before, after = audit.protected(old_doc), audit.protected(new_doc)
    require(before == baseline["files"][SOURCE], "Parser differs from baseline")
    for key in before:
        if key != "sha256":
            require(before[key] == after[key], f"Protected field differs: {key}")
    for key in ("codes", "links", "footnotes", "html", "explicit_ids"):
        require(old_doc[key] == new_doc[key], f"Content or positions changed: {key}")
    old_tokens, new_tokens = audit.MD.parse(old_text), audit.MD.parse(new_text)
    require(markup_shape(old_tokens) == markup_shape(new_tokens), "Markdown shape changed")
    block_tokens = [t for t in old_tokens if t.type in {"fence", "code_block"}]
    for token in block_tokens:
        start, stop = token.map
        require(old[start:stop] == new[start:stop], "Code block or comment changed")
    for (source_line, chinese_line), literals in EXAMPLES.items():
        for literal in literals:
            require(literal in old[source_line - 1], f"Example absent from English: {literal}")
            require(literal in new[chinese_line - 1], f"Example changed or absent: {literal}")

    assets = {}
    image_directory = str(Path(SOURCE).parent / "images") + "/"
    for path, expected in baseline["assets"].items():
        if not path.startswith(image_directory):
            continue
        original_image = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{COMMIT}:{path}"]
        )
        current_image = (ROOT / path).read_bytes()
        require(audit.digest(original_image) == expected, f"Image baseline mismatch: {path}")
        require(original_image == current_image, f"Image changed: {path}")
        assets[path] = expected
    require(len(assets) == 4, "Expected four Chapter 17 screenshots")
    require(old[290] == new[290], "Protected malformed citation URL changed")
    return {
        "status": "pass",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(current),
        "physical_lines_read": len(old),
        "original_chinese_lines": len(han),
        "completed_chinese_lines": len(changed | retained),
        "edited_chinese_lines": len(changed),
        "reviewed_unchanged_count": len(retained),
        "reviewed_unchanged_lines": sorted(retained),
        "held_lines": manifest["held_lines"],
        "chinese_coverage_by_line_type": dict(categories),
        "non_chinese_lines_unchanged": len(old) - len(han),
        "english_source_lines": len(before["english_line_hashes"]),
        "english_segments": len(before["english_segment_hashes"]),
        "protected_inline_code_items": len(before["code_hashes"]),
        "fenced_or_indented_code_blocks": len(block_tokens),
        "links_including_images_and_bare_urls": len(before["links"]),
        "structural_items": len(before["structures"]),
        "html_items": len(before["html_hashes"]),
        "footnote_markers": len(before["footnotes"]),
        "example_literal_assertions": sum(map(len, EXAMPLES.values())),
        "screenshots_and_embedded_captions_visually_read": 4,
        "unchanged_screenshot_hashes": assets,
        "punctuation_residuals": 0,
        "protection_exceptions": [],
        "chapter_only": True,
        "checks": [
            "Original Git bytes and parser output match the fixed stored baseline",
            "Manifest exactly reconstructs the chapter from the original snapshot",
            "All original Chinese lines are disjointly edited, retained, or held",
            "All non-Chinese lines and English heading prefixes are unchanged",
            "All existing audit protection assertions pass without exceptions",
            "Block and inline Markdown structure and source maps are unchanged",
            "Code, links, HTML, footnotes and their positions are unchanged",
            "Indentation, blank lines, trailing whitespace and line endings are unchanged",
            "Query and identifier literals match the local English source",
            "All four screenshots match both Git and baseline hashes",
            "Chinese punctuation normalization is idempotent with query/code protection",
        ],
        "limitations": [
            "Historical statements retained; no online source or current-product verification",
            "Local English typos, missing text and malformed URLs are recorded, not repaired",
            "No browser rendering or external-link availability checks",
            "Screenshots were read as images; their embedded English was not altered",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    baseline, original, current = inputs()
    if args.record:
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
    report = validate(baseline, original, current, manifest)
    if args.record:
        path = REVIEW / "edits.json"
        if path.exists():
            require(json.loads(path.read_text()) == manifest, "Refusing to replace another manifest")
        else:
            path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.write_report:
        (REVIEW / "verification.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
