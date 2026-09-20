"""Validate Chapter 12 only; serialize the completed manual review on request."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
SOURCE = "zh-cn/Chapter-12_Unit_Testing/Chapter-12_Unit_Testing.md"
COMMIT = "110720f031b43e18708fdc38af03269b65b3cc41"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

# Explicit decisions from the full bilingual review, not inferred coverage.
RETAINED = [
    6, 40, 89, 92, 95, 105, 166, 219, 253, 271, 311, 341, 361, 381,
    404, 416, 453, 487, 543, 553, 569, 588, 615, 631, 640, 654, 739,
    745, 778, 882, 896, 933, 957, 959, 963, 969, 971,
]
PUNCTUATION = {
    ",": "\uff0c", ";": "\uff1b", ":": "\uff1a", "?": "\uff1f",
    "!": "\uff01", "(": "\uff08", ")": "\uff09",
}
QUOTES = {
    "\u300c": "\u201c", "\u300d": "\u201d",
    "\u300e": "\u2018", "\u300f": "\u2019",
}
INLINE = re.compile(r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>]+")
LATIN = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_cjk(char):
    return bool(char) and (
        bool(audit.HAN.search(char))
        or "\u3000" <= char <= "\u303f"
        or "\uff00" <= char <= "\uffef"
        or char in "\u201c\u201d\u2018\u2019\u00b7\u2014\u2026"
    )


def normalize_punctuation(line):
    chars = list(line)
    protected = set()
    if line.startswith(("#", "*Example")):
        protected.update(range(audit.HAN.search(line).start()))
    for match in INLINE.finditer(line):
        protected.update(range(match.start(), match.end()))
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
            if is_cjk(left) or is_cjk(right):
                chars[i] = PUNCTUATION[char]
    return "".join(chars)


def shape(text):
    return [
        (
            token.type, token.tag, token.nesting, token.level, token.map,
            [
                (child.type, child.tag, child.nesting, child.markup, child.attrs)
                for child in token.children or [] if child.type != "text"
            ],
        )
        for token in audit.MD.parse(text)
    ]


def source_texts():
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"]
    ).decode("utf-8")
    current = (ROOT / SOURCE).read_bytes().decode("utf-8")
    return original, current


def build_manifest(original, current):
    old, new = original.splitlines(), current.splitlines()
    require(len(old) == len(new) == 973, "Unexpected physical line count")
    replacements = {
        str(i): after
        for i, (before, after) in enumerate(zip(old, new), 1)
        if before != after
    }
    chinese = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    require(len(chinese) == 168, "Unexpected original Chinese line count")
    require(set(map(int, replacements)) == chinese - set(RETAINED),
            "Edits do not match the completed manual review")
    return {
        "source": SOURCE,
        "baseline_sha256": audit.digest(original),
        "replacements": replacements,
        "reviewed_unchanged_lines": RETAINED,
        "held_lines": {},
    }


def verify(original, current, manifest):
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Unexpected baseline commit")
    require(manifest["source"] == SOURCE, "Unexpected manifest source")
    require(
        audit.digest(original) == baseline["files"][SOURCE]["sha256"]
        == manifest["baseline_sha256"], "Original SHA-256 mismatch",
    )
    old, new = original.splitlines(keepends=True), current.splitlines(keepends=True)
    require(len(old) == len(new) == 973, "Physical line count changed")
    chinese = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    replacements = {int(k): v for k, v in manifest["replacements"].items()}
    retained = set(manifest["reviewed_unchanged_lines"])
    held = {int(k) for k in manifest["held_lines"]}
    require(changed == set(replacements), "Replacement manifest mismatch")
    require(not (changed & retained or changed & held or retained & held),
            "Overlapping review decisions")
    require(changed | retained | held == chinese, "Incomplete Chinese coverage")
    require(manifest["reviewed_unchanged_lines"] == RETAINED,
            "Retained lines differ from manual review")
    require(not held, "This review has no held Chinese content")

    for number, (before, after) in enumerate(zip(old, new), 1):
        require(re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0],
                f"Indentation or blank line changed: {number}")
        require(re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
                f"Trailing whitespace or line ending changed: {number}")
        if number not in chinese:
            require(before == after, f"Non-Chinese source changed: {number}")
        require(Counter(LATIN.findall(before)) == Counter(LATIN.findall(after)),
                f"Embedded English token inventory changed: {number}")
        require(INLINE.findall(before) == INLINE.findall(after),
                f"Raw inline code/link/HTML changed: {number}")
        if number in chinese:
            require(normalize_punctuation(after) == after,
                    f"Chinese punctuation residual: {number}")
        if number in changed:
            require(audit.HAN.search(after), f"Chinese content removed: {number}")
            require(after.rstrip("\r\n") == replacements[number],
                    f"Replacement differs from file: {number}")
            require("\n" not in replacements[number] and "\r" not in replacements[number],
                    f"Multiline replacement: {number}")
            if before.startswith(("#", "*Example")):
                prefix = before[:audit.HAN.search(before).start()]
                require(after.startswith(prefix), f"English prefix changed: {number}")

    before_doc = audit.parse_document(SOURCE, original)
    after_doc = audit.parse_document(SOURCE, current)
    before, after = audit.protected(before_doc), audit.protected(after_doc)
    require(before == baseline["files"][SOURCE], "Original parser baseline mismatch")
    for key in before:
        if key != "sha256":
            require(before[key] == after[key], f"Protected field changed: {key}")
    require(shape(original) == shape(current), "Markdown token structure changed")
    for key in ("codes", "links", "footnotes", "html", "explicit_ids"):
        require(before_doc[key] == after_doc[key], f"Content or position changed: {key}")
    require(
        not any(audit.HAN.search(item["content"]) for item in before_doc["codes"]),
        "Chinese in a protected code item needs an explicit hold",
    )
    return {
        "status": "pass",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(current),
        "physical_lines": len(old),
        "original_chinese_lines": len(chinese),
        "reviewed_chinese_lines": len(changed | retained),
        "edited_chinese_lines": len(changed),
        "reviewed_unchanged_count": len(retained),
        "reviewed_unchanged_lines": sorted(retained),
        "held_lines": {},
        "english_source_lines": len(before["english_line_hashes"]),
        "english_segments": len(before["english_segment_hashes"]),
        "protected_code_items": len(before["code_hashes"]),
        "fenced_code_blocks": sum(item["kind"] == "fence" for item in before_doc["codes"]),
        "links": len(before["links"]),
        "structural_items": len(before["structures"]),
        "html_items": len(before["html_hashes"]),
        "footnote_markers": len(before["footnotes"]),
        "punctuation_residuals": 0,
        "protection_exceptions": [],
        "chapter_only": True,
        "checks": [
            "fixed Git snapshot and baseline SHA-256 match",
            "168 Chinese lines have complete disjoint manual review decisions",
            "replacement manifest reproduces the edited chapter exactly",
            "non-Chinese source lines are byte-for-byte unchanged",
            "English heading/caption prefixes and embedded Latin token inventories unchanged",
            "all shared audit protection fields except whole-file hash unchanged",
            "block and nontext inline token structure, nesting and source maps unchanged",
            "code including comments, links, HTML, footnotes and positions unchanged",
            "raw inline code, Markdown links and HTML fragments unchanged",
            "blank lines, indentation, hard breaks and line endings unchanged",
            "Chinese punctuation normalization is idempotent on every Chinese line",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-artifacts", action="store_true")
    args = parser.parse_args()
    original, current = source_texts()
    manifest = (
        build_manifest(original, current) if args.write_artifacts
        else json.loads((REVIEW / "edits.json").read_text())
    )
    report = verify(original, current, manifest)
    if args.write_artifacts:
        for name, value in (("edits.json", manifest), ("verification.json", report)):
            (REVIEW / name).write_text(
                json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
    print(json.dumps(report, ensure_ascii=False, indent=2))
