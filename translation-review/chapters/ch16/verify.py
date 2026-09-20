"""Chapter 16 manifest generation and strict, offline protection checks."""

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
    "zh-cn/Chapter-16_Version_Control_and_Branch_Management/"
    "Chapter-16_Version_Control_and_Branch_Management.md"
)
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

RETAINED = [
    6, 24, 50, 214, 220, 226, 252, 270, 284, 302, 334, 373,
    415, 417, 455, 469, 503, 521,
]
HELD = {
    "359": (
        "Chinese One-Version Rule quotation inside the indented code block at "
        "lines 358-359. Read for context and retained byte-for-byte, including "
        "ASCII quotation marks. The brief forbids editing Chinese prose parsed "
        "as code; not counted as completed polishing."
    ),
}
PUNCTUATION_PRESERVED = {
    "373": (
        "The opening parenthesis in the original Chinese heading is included "
        "in the baseline English segment. Retain the complete original heading "
        "and its matched ASCII parentheses; the Chinese wording is approved."
    ),
}
PUNCTUATION = {
    ",": "\uff0c", ";": "\uff1b", ":": "\uff1a", "?": "\uff1f",
    "!": "\uff01", "(": "\uff08", ")": "\uff09",
}
QUOTES = {
    "\u300c": "\u201c", "\u300d": "\u201d",
    "\u300e": "\u2018", "\u300f": "\u2019",
}
INLINE = re.compile(
    r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>]+"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prefix(line):
    if line.lstrip().startswith(("#", "*Figure ")):
        match = audit.HAN.search(line)
        if match:
            return line[:match.start()]
    return ""


def chinese(char):
    return bool(audit.HAN.search(char)) or char in (
        "\u201c\u201d\u2018\u2019\u00b7\u2014\u2026"
        "\u300a\u300b\u3008\u3009\u3010\u3011\u3001\u3002"
        "\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09"
    )


def normalize_punctuation(line, number):
    protected = set(range(len(prefix(line))))
    for match in INLINE.finditer(line):
        protected.update(range(match.start(), match.end()))
    if str(number) in PUNCTUATION_PRESERVED:
        match = re.search(r"\(\u51e0\u4e4e\)", line)
        require(match is not None, "Original heading punctuation changed")
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


def inputs():
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Unexpected baseline commit")
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"]
    )
    require(
        audit.digest(original) == baseline["files"][SOURCE]["sha256"],
        "Git snapshot differs from baseline",
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
    require(manifest["reviewed_unchanged_lines"] == RETAINED, "Retained list changed")
    require(manifest["held_lines"] == HELD, "Hold record changed")
    require(changed == set(replacements), "Manifest differs from edits")
    require(not (changed & retained or changed & held or retained & held), "Coverage overlaps")
    require(changed | retained | held == han, "Incomplete Chinese coverage")

    for number, (before, after) in enumerate(zip(old, new), 1):
        if number not in han:
            require(before == after, f"Non-Chinese line changed: {number}")
        require(
            re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0],
            f"Leading whitespace changed: {number}",
        )
        require(
            re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
            f"Trailing whitespace or line ending changed: {number}",
        )
        require(after.startswith(prefix(before)), f"English prefix changed: {number}")
        require(INLINE.findall(before) == INLINE.findall(after), f"Inline item changed: {number}")
        require(before.count("*") == after.count("*"), f"Emphasis markers changed: {number}")
        if number in changed:
            replacement = replacements[number]
            require(isinstance(replacement, str), f"Invalid replacement: {number}")
            require("\n" not in replacement and "\r" not in replacement, "Multiline edit")
            require(audit.HAN.search(replacement), f"Chinese removed: {number}")
            require(after.rstrip("\r\n") == replacement, f"Replacement mismatch: {number}")
        if number in han - held:
            require(normalize_punctuation(after, number) == after, f"Punctuation residual: {number}")
        if str(number) in PUNCTUATION_PRESERVED:
            require(before == after, "Preserved heading changed")

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

    code_lines = set()
    for token in audit.MD.parse(old_text):
        if token.type in {"fence", "code_block"}:
            code_lines.update(range(token.map[0] + 1, token.map[1] + 1))
    require(not changed & code_lines, "Code-block line changed")
    require(held == han & code_lines, "Chinese code holds incomplete")
    assets = {
        path: sha for path, sha in baseline["assets"].items()
        if path.startswith(str(Path(SOURCE).parent) + "/")
    }
    for path, sha in assets.items():
        require(audit.digest((ROOT / path).read_bytes()) == sha, f"Chapter image changed: {path}")

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
        "chapter_images": len(assets),
        "punctuation_preserved_lines": PUNCTUATION_PRESERVED,
        "punctuation_residuals_outside_protected_content": 0,
        "protection_exceptions": [],
        "chapter_only": True,
        "checks": [
            "Git snapshot hash and original parser output match stored baseline",
            "manifest replacements exactly match actual edited lines",
            "edited, retained and held lines are disjoint and cover every Chinese line",
            "non-Chinese lines and English heading/caption prefixes unchanged",
            "all translation_audit protection fields except file hash unchanged",
            "Markdown block types, nesting, maps and markers unchanged",
            "code, links, HTML and footnotes unchanged including positions",
            "raw inline links, images, code and emphasis marker counts unchanged",
            "line count/order, indentation, blank lines, trailing spaces and endings unchanged",
            "chapter image hashes match baseline",
            "mechanical punctuation normalization is idempotent outside protected content",
        ],
        "limitations": [
            "One Chinese quotation is held inside a protected indented code block",
            "Original ASCII parentheses in the retained heading at line 373 are protected",
            "Historical and technically simplified source claims were not modernized",
            "No online source comparison, link reachability check or browser rendering",
            "No other chapters or shared files are validated or changed by this script",
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
    old = original.decode("utf-8").splitlines(keepends=True)
    new = current.decode("utf-8").splitlines(keepends=True)
    require(len(old) == len(new), "Line count changed")
    if args.normalize:
        result = [
            normalize_punctuation(line, i)
            if audit.HAN.search(before) and str(i) not in HELD else line
            for i, (before, line) in enumerate(zip(old, new), 1)
        ]
        count = sum(a != b for a, b in zip(new, result))
        if count:
            (ROOT / SOURCE).write_bytes("".join(result).encode("utf-8"))
        print(json.dumps({"mechanically_normalized_lines": count}))
        return
    if args.record:
        require(not (REVIEW / "edits.json").exists(), "Refusing to overwrite manifest")
        manifest = {
            "source": SOURCE,
            "baseline_sha256": baseline["files"][SOURCE]["sha256"],
            "replacements": {
                str(i): after.rstrip("\r\n")
                for i, (before, after) in enumerate(zip(old, new), 1) if before != after
            },
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
