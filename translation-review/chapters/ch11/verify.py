"""Chapter 11 only: verify the reviewed manifest against the fixed Git snapshot."""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
SOURCE = "zh-cn/Chapter-11_Testing_Overview/Chapter-11_Testing_Overview.md"
COMMIT = "110720f031b43e18708fdc38af03269b65b3cc41"
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

PUNCTUATION = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))
QUOTES = dict(zip("\u300c\u300d\u300e\u300f", "\u201c\u201d\u2018\u2019"))
PROTECTED_INLINE = re.compile(
    r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>]+"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def chinese(char):
    return bool(audit.HAN.search(char)) or (
        bool(char) and ("\u3000" <= char <= "\u303f" or "\uff00" <= char <= "\uffef")
    ) or char in {
        "\u201c", "\u201d", "\u2018", "\u2019",
        "\u00b7", "\u2014", "\u2026",
    }


def prefix(line):
    if line.startswith("#") or re.match(r"\*(?:Figure|Example) ", line):
        return line[:audit.HAN.search(line).start()]
    return ""


def normalize_punctuation(line):
    chars = list(line)
    protected = set(range(len(prefix(line))))
    for match in PROTECTED_INLINE.finditer(line):
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
            if chinese(left) or chinese(right):
                chars[i] = PUNCTUATION[char]
    return "".join(chars)


def block_shape(text):
    return [
        (token.type, token.tag, token.nesting, token.level, token.map, token.markup)
        for token in audit.MD.parse(text)
    ]


def validate(original, current, manifest, baseline_entry):
    require(manifest["source"] == SOURCE, "Manifest source mismatch")
    require(
        audit.digest(original) == manifest["baseline_sha256"] == baseline_entry["sha256"],
        "Baseline SHA-256 mismatch",
    )
    old_text, new_text = original.decode("utf-8"), current.decode("utf-8")
    old = old_text.splitlines(keepends=True)
    new = new_text.splitlines(keepends=True)
    require(len(old) == len(new), "Physical line count changed")
    chinese_lines = {i for i, text in enumerate(old, 1) if audit.HAN.search(text)}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    replacements = {int(k): v for k, v in manifest["replacements"].items()}
    retained = set(manifest["reviewed_unchanged_lines"])
    held = {int(k) for k in manifest["held_lines"]}
    require(changed == set(replacements), "Manifest does not match changed lines")
    require(len(replacements) == len(manifest["replacements"]), "Duplicate replacement")
    require(len(retained) == len(manifest["reviewed_unchanged_lines"]), "Duplicate retained line")
    require(not (changed & retained or changed & held or retained & held), "Coverage overlap")
    require(changed | retained | held == chinese_lines, "Incomplete Chinese coverage")
    require(all(isinstance(v, str) and v.strip() for v in manifest["held_lines"].values()),
            "Held lines require reasons")
    reconstructed = old.copy()
    for number, (before, after) in enumerate(zip(old, new), 1):
        require(re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0],
                f"Indentation/blank line changed: {number}")
        require(re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
                f"Trailing whitespace/line ending changed: {number}")
        if number not in changed:
            require(before == after, f"Unexpected edit: {number}")
        else:
            value = replacements[number]
            require(isinstance(value, str) and "\n" not in value and "\r" not in value,
                    f"Invalid replacement: {number}")
            require(audit.HAN.search(value), f"Chinese removed: {number}")
            require(value == after.rstrip("\r\n"), f"Replacement mismatch: {number}")
            ending = before[len(before.rstrip("\r\n")):]
            reconstructed[number - 1] = value + ending
        if number in chinese_lines:
            require(after.startswith(prefix(before)), f"English prefix changed: {number}")
            require(PROTECTED_INLINE.findall(before) == PROTECTED_INLINE.findall(after),
                    f"Protected inline text changed: {number}")
            require(before.count("*") == after.count("*"), f"Emphasis markers changed: {number}")
            if number not in held:
                require(normalize_punctuation(after) == after, f"Punctuation residual: {number}")
    require("".join(reconstructed).encode("utf-8") == current, "Reconstruction mismatch")

    old_doc = audit.parse_document(SOURCE, old_text)
    new_doc = audit.parse_document(SOURCE, new_text)
    old_protected, new_protected = audit.protected(old_doc), audit.protected(new_doc)
    require(old_protected == baseline_entry, "Original parse differs from recorded baseline")
    for key in old_protected:
        if key != "sha256":
            require(old_protected[key] == new_protected[key], f"Protected field changed: {key}")
    require(block_shape(old_text) == block_shape(new_text), "Markdown block structure changed")
    for key in ("codes", "links", "footnotes", "html", "explicit_ids"):
        require(old_doc[key] == new_doc[key], f"Content/position changed: {key}")
    return {
        "status": "pass",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(current),
        "physical_lines": len(old),
        "original_chinese_lines": len(chinese_lines),
        "reviewed_chinese_lines": len(changed | retained),
        "changed_chinese_lines": len(changed),
        "reviewed_unchanged_count": len(retained),
        "reviewed_unchanged_lines": sorted(retained),
        "held_count": len(held),
        "held_lines": manifest["held_lines"],
        "coverage_complete": True,
        "english_source_lines": len(old_protected["english_line_hashes"]),
        "english_segments": len(old_protected["english_segment_hashes"]),
        "protected_code_items": len(old_protected["code_hashes"]),
        "links": len(old_protected["links"]),
        "footnote_markers": len(old_protected["footnotes"]),
        "structural_items": len(old_protected["structures"]),
        "html_items": len(old_protected["html_hashes"]),
        "punctuation_residuals": 0,
        "protection_exceptions": [],
        "chapter_only": True,
        "checks": [
            "Git snapshot, recorded baseline and manifest SHA-256 agree",
            "changed, reviewed-unchanged and held coverage is complete and disjoint",
            "manifest reconstructs the edited chapter byte-for-byte",
            "non-Chinese lines and mixed heading/caption English prefixes unchanged",
            "all translation_audit protected fields except file SHA-256 unchanged",
            "Markdown block types, levels, nesting, markup and line maps unchanged",
            "code, links, footnotes and their positions unchanged",
            "HTML, emphasis markers, indentation, blank lines and hard breaks unchanged",
            "mechanical Chinese punctuation normalization is idempotent",
        ],
    }


def self_test(original, current, manifest, entry):
    tests = [
        ("English source", 13, "Testing", "TESTING"),
        ("English heading prefix", 77, "Story", "Stories"),
        ("English caption prefix", 117, "two", "three"),
        ("code comment", 132, "Verifies", "Checks"),
        ("inline code", 468, "sleep()", "pause()"),
        ("image target", 113, ".png", ".jpg"),
        ("footnote marker", 354, "[^6]", "[^7]"),
        ("list indentation", 194, "\t", "  "),
        ("hard line break", 202, "  \n", "\n"),
        ("heading level", 77, "### ", "## "),
        ("Chinese punctuation", 15, "\uff0c", ","),
    ]
    checked = []
    for name, number, needle, replacement in tests:
        lines = current.decode("utf-8").splitlines(keepends=True)
        require(needle in lines[number - 1], f"Invalid self-test fixture: {name}")
        lines[number - 1] = lines[number - 1].replace(needle, replacement, 1)
        bad_manifest = deepcopy(manifest)
        bad_manifest["replacements"][str(number)] = lines[number - 1].rstrip("\r\n")
        try:
            validate(original, "".join(lines).encode("utf-8"), bad_manifest, entry)
        except ValueError:
            checked.append(name)
        else:
            raise ValueError(f"Failed to reject mutation: {name}")
    for name in ("missing coverage", "overlapping coverage", "missing replacement"):
        bad_manifest = deepcopy(manifest)
        if name == "missing coverage":
            bad_manifest["reviewed_unchanged_lines"].remove(54)
        elif name == "overlapping coverage":
            bad_manifest["reviewed_unchanged_lines"].append(15)
        else:
            del bad_manifest["replacements"]["15"]
        try:
            validate(original, current, bad_manifest, entry)
        except ValueError:
            checked.append(name)
        else:
            raise ValueError(f"Failed to reject mutation: {name}")
    return {"status": "pass", "rejected_mutations": len(checked), "cases": checked}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Unexpected baseline commit")
    manifest = json.loads((REVIEW / "edits.json").read_text())
    original = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"])
    current = (ROOT / SOURCE).read_bytes()
    result = validate(original, current, manifest, baseline["files"][SOURCE])
    assets = {
        path: value for path, value in baseline["assets"].items()
        if path.startswith(str(Path(SOURCE).parent) + "/")
    }
    for path, expected in assets.items():
        require(audit.digest((ROOT / path).read_bytes()) == expected, f"Asset changed: {path}")
    result["unchanged_chapter_assets"] = len(assets)
    if args.self_test:
        result["validator_self_test"] = self_test(
            original, current, manifest, baseline["files"][SOURCE]
        )
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.write_report:
        (REVIEW / "verification.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
