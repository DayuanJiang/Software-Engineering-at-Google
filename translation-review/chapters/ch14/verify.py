"""Chapter 14 review manifest and strict, chapter-local protection checks."""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import sys

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
SOURCE = "zh-cn/Chapter-14_Larger_Testing/Chapter-14_Larger_Testing.md"
COMMIT = "110720f031b43e18708fdc38af03269b65b3cc41"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

RETAINED = [
    46, 58, 88, 142, 269, 270, 290, 292, 316, 318, 380, 402, 415,
    428, 448, 450, 453, 472, 475, 506, 507, 508, 509, 510, 512,
    513, 547, 553, 578, 589, 590, 600, 626, 668, 687, 689, 718,
    748, 793, 836, 860, 923, 944, 965, 1003, 1009,
]
HELD = {}
PUNCTUATION = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))
QUOTES = dict(zip("\u300c\u300d\u300e\u300f", "\u201c\u201d\u2018\u2019"))
LINK = re.compile(r"!?\[[^\]]*\]\([^)]*\)")
INLINE = re.compile(r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>]+")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def chinese(char):
    return bool(audit.HAN.search(char)) or char in (
        "\u201c\u201d\u2018\u2019\u00b7\u2014\u2026\u300a\u300b"
        "\u3008\u3009\u3010\u3011\u3001\u3002\uff0c\uff01\uff1f"
        "\uff1b\uff1a\uff08\uff09"
    )


def english_prefix(line):
    if line.lstrip().startswith(("#", "*Figure ", "*Example ", "Tip:")):
        match = audit.HAN.search(line)
        if match:
            return line[:match.start()]
    return ""


def normalize_punctuation(line):
    protected = set(range(len(english_prefix(line))))
    for match in INLINE.finditer(line):
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
        "Git snapshot does not match stored baseline",
    )
    return baseline, original, (ROOT / SOURCE).read_bytes()


def manifest_for(original, current):
    old = original.decode("utf-8").splitlines()
    new = current.decode("utf-8").splitlines()
    require(len(old) == len(new), "Line count changed before recording")
    return {
        "source": SOURCE,
        "baseline_sha256": audit.digest(original),
        "replacements": {
            str(i): b for i, (a, b) in enumerate(zip(old, new), 1) if a != b
        },
        "reviewed_unchanged_lines": RETAINED,
        "held_lines": HELD,
    }


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
    require(len(old) == len(new), "Physical line count changed")
    han = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    replacements = {int(k): v for k, v in manifest["replacements"].items()}
    retained = set(manifest["reviewed_unchanged_lines"])
    held = {int(k) for k in manifest["held_lines"]}
    require(manifest["reviewed_unchanged_lines"] == RETAINED, "Retained review list changed")
    require(manifest["held_lines"] == HELD, "Hold record changed")
    require(len(retained) == len(RETAINED), "Duplicate retained lines")
    require(changed == set(replacements), "Actual edits differ from manifest")
    require(changed <= han, "Non-Chinese line changed")
    require(not (changed & retained or changed & held or retained & held), "Coverage overlap")
    require(changed | retained | held == han, "Incomplete Chinese line classification")
    for number, (before, after) in enumerate(zip(old, new), 1):
        require(
            re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0],
            f"Indentation or blank line changed: {number}",
        )
        require(
            re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
            f"Trailing whitespace or line ending changed: {number}",
        )
        require(after.startswith(english_prefix(before)), f"English prefix changed: {number}")
        require(LINK.findall(before) == LINK.findall(after), f"Raw Markdown link changed: {number}")
        require(
            re.findall(r"[*`_]+", before) == re.findall(r"[*`_]+", after),
            f"Inline emphasis/code markers changed: {number}",
        )
        if number in changed:
            replacement = replacements[number]
            require(isinstance(replacement, str), f"Invalid replacement: {number}")
            require("\n" not in replacement and "\r" not in replacement, "Multiline replacement")
            require(after.rstrip("\r\n") == replacement, f"Wrong replacement line: {number}")
            require(audit.HAN.search(replacement), f"Chinese removed: {number}")
        if number in han - held:
            require(normalize_punctuation(after) == after, f"Punctuation residual: {number}")

    old_doc, new_doc = audit.parse_document(SOURCE, old_text), audit.parse_document(SOURCE, new_text)
    before, after = audit.protected(old_doc), audit.protected(new_doc)
    require(before == baseline["files"][SOURCE], "Parser does not match stored baseline")
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
    require(held == han & code_lines, "Chinese code-block hold accounting differs")

    assets = {
        path: sha for path, sha in baseline["assets"].items()
        if path.startswith("zh-cn/Chapter-14_Larger_Testing/")
    }
    for path, sha in assets.items():
        require(audit.digest((ROOT / path).read_bytes()) == sha, f"Chapter image changed: {path}")
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
        "held_count": len(held),
        "held_lines": manifest["held_lines"],
        "non_chinese_lines_unchanged": len(old) - len(han),
        "english_source_lines": len(before["english_line_hashes"]),
        "english_segments": len(before["english_segment_hashes"]),
        "protected_code_items": len(before["code_hashes"]),
        "links": len(before["links"]),
        "structural_items": len(before["structures"]),
        "html_items": len(before["html_hashes"]),
        "footnote_markers": len(before["footnotes"]),
        "chapter_images_unchanged": len(assets),
        "punctuation_residuals_outside_hold": 0,
        "protection_exceptions": [],
        "checks": [
            "fixed Git snapshot SHA-256 and parser output equal stored baseline",
            "exact full-line replacements and disjoint changed/retained/held coverage",
            "all non-Chinese lines and English heading/caption/Tip prefixes unchanged",
            "all translation_audit protection fields except whole-file SHA-256 unchanged",
            "all raw Markdown links, labels, images and inline markup unchanged",
            "Markdown block types, nesting, maps and code-fence information unchanged",
            "code, HTML, links and footnotes including source positions unchanged",
            "line count/order, blank lines, indentation, hard breaks and line endings unchanged",
            "punctuation normalization idempotent on every reviewed Chinese line",
            "all six chapter-local images equal their baseline hashes",
        ],
        "limitations": [
            "Local English ambiguities and inherited omissions are recorded in notes.md",
            "Code examples read but not compiled or corrected",
            "No online source comparison, external-link checks or browser rendering",
            "No all-repository assertions, shared edits, agents, external model APIs or commits",
        ],
    }


def negative_controls(baseline, original, current, manifest):
    text = current.decode("utf-8")
    cases = [
        ("English source", text.replace("**CHAPTER 14**", "**CHAPTER 15**", 1)),
        ("Executable code", text.replace('response.Contains("Colossal Cave")', 'response.Contains("changed")', 1)),
        ("Link target", text.replace("https://martinfowler.com/bliki/TestDouble.html", "https://example.invalid", 1)),
        ("English heading prefix", text.replace("What Are Larger Tests?", "What Are Smaller Tests?", 1)),
        ("Final blank line", text[:-1]),
        ("Hard line break", text.replace("- *\u53ef\u9760*  \n", "- *\u53ef\u9760*\n", 1)),
        ("HTML injection", text.replace("\u524d\u51e0\u7ae0\u4ecb\u7ecd", "<b></b>\u524d\u51e0\u7ae0\u4ecb\u7ecd", 1)),
    ]
    rejected = {}
    for name, mutated in cases:
        require(mutated != text, f"Negative control did not mutate: {name}")
        try:
            candidate = manifest_for(original, mutated.encode("utf-8"))
            validate(baseline, original, mutated.encode("utf-8"), candidate)
        except ValueError as error:
            rejected[name] = str(error)
        else:
            raise ValueError(f"Negative control incorrectly passed: {name}")
    missing = deepcopy(manifest)
    missing["reviewed_unchanged_lines"].remove(46)
    try:
        validate(baseline, original, current, missing)
    except ValueError as error:
        rejected["Missing Chinese classification"] = str(error)
    else:
        raise ValueError("Missing classification incorrectly passed")
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--normalize", action="store_true")
    modes.add_argument("--record", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    baseline, original, current = inputs()
    if args.normalize:
        old, new = original.decode().splitlines(keepends=True), current.decode().splitlines(keepends=True)
        require(len(old) == len(new), "Line count changed before normalization")
        normalized = [
            normalize_punctuation(after) if audit.HAN.search(before) and str(i) not in HELD else after
            for i, (before, after) in enumerate(zip(old, new), 1)
        ]
        changed = sum(a != b for a, b in zip(new, normalized))
        if changed:
            (ROOT / SOURCE).write_bytes("".join(normalized).encode("utf-8"))
        print(json.dumps({"mechanically_normalized_lines": changed}))
        return
    if args.record:
        require(not (REVIEW / "edits.json").exists(), "Refusing to overwrite edits.json")
        manifest = manifest_for(original, current)
    else:
        manifest = json.loads((REVIEW / "edits.json").read_text())
    result = validate(baseline, original, current, manifest)
    result["negative_controls_rejected"] = negative_controls(baseline, original, current, manifest)
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
