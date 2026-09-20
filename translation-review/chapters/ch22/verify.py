"""Verify only Chapter 22 and generate its local review artifacts."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

OUT = Path(__file__).resolve().parent
SOURCE = "zh-cn/Chapter-22_Large-Scale_Changes/Chapter-22_Large-Scale_Changes.md"
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
RETAINED = [
    6, 66, 96, 116, 122, 134, 136, 168, 182, 218, 229, 268, 304,
    310, 358, 364, 374, 394, 410, 421, 422, 423, 424, 430, 452,
    486, 506, 542, 556, 566, 576, 586,
]
HELD = {}
PUNCTUATION = {",": "\uff0c", ";": "\uff1b", ":": "\uff1a",
               "?": "\uff1f", "!": "\uff01", "(": "\uff08", ")": "\uff09"}
INLINE = re.compile(r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]*>")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_original():
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Baseline commit mismatch")
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"]
    )
    require(audit.digest(original) == baseline["files"][SOURCE]["sha256"],
            "Baseline SHA-256 mismatch")
    return original, baseline["files"][SOURCE]


def cjk(char):
    return bool(audit.HAN.search(char)) or char in (
        "\u201c\u201d\u2018\u2019\u300a\u300b\u3010\u3011"
        "\u3001\u3002\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09"
    )


def punctuation_changes(line):
    protected = set()
    for match in INLINE.finditer(line):
        protected.update(range(match.start(), match.end()))
    first = audit.HAN.search(line)
    if line.lstrip().startswith("#") and first:
        protected.update(range(first.start()))
    changes = []
    for i, char in enumerate(line):
        if i in protected:
            continue
        left = line[i - 1] if i else ""
        right = line[i + 1] if i + 1 < len(line) else ""
        if char in PUNCTUATION and (cjk(left) or cjk(right)):
            changes.append((i, PUNCTUATION[char]))
        if char in {'"', "\u300c", "\u300d", "\u300e", "\u300f"}:
            raise ValueError("Unnormalized quotation mark in Chinese prose")
    return changes


def token_shape(tokens):
    return [
        (t.type, t.tag, t.nesting, t.level, t.markup, t.info, t.map,
         t.attrs, t.hidden, token_shape(t.children or []))
        for t in tokens
    ]


def validate(original, actual, manifest, snapshot):
    require(manifest["source"] == SOURCE, "Manifest source mismatch")
    require(manifest["baseline_sha256"] == audit.digest(original),
            "Manifest SHA-256 mismatch")
    old = original.decode().splitlines(keepends=True)
    new = actual.decode().splitlines(keepends=True)
    require(len(old) == len(new), "Physical line count changed")
    chinese = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    replacements = manifest["replacements"]
    require(all(str(int(k)) == k for k in replacements), "Invalid line key")
    edited = {int(k) for k in replacements}
    retained = set(manifest["reviewed_unchanged_lines"])
    held = {int(k) for k in manifest["held_lines"]}
    require(manifest["reviewed_unchanged_lines"] == RETAINED,
            "Explicit retained-line review changed")
    require(manifest["held_lines"] == HELD, "Explicit held-line review changed")
    require(not (edited & retained or edited & held or retained & held),
            "Coverage groups overlap")
    require(edited | retained | held == chinese, "Incomplete Chinese coverage")
    require(changed == edited, "Actual edits differ from manifest")
    expected = old.copy()
    for number in edited:
        replacement = replacements[str(number)]
        require(isinstance(replacement, str) and "\n" not in replacement
                and "\r" not in replacement, "Replacement is not one line")
        require(audit.HAN.search(replacement), "Chinese line removed")
        ending = re.search(r"(\r\n|\n|\r)?$", old[number - 1])[0]
        expected[number - 1] = replacement + ending
    require("".join(expected).encode() == actual, "Manifest reconstruction failed")
    for i, (before, after) in enumerate(zip(old, new), 1):
        if i not in chinese:
            require(before == after, f"Non-Chinese source changed at line {i}")
        require(re.match(r"\s*", before)[0] == re.match(r"\s*", after)[0],
                f"Indentation changed at line {i}")
        require(re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
                f"Line ending or trailing spaces changed at line {i}")
        require(INLINE.findall(before) == INLINE.findall(after),
                f"Link, inline code, or HTML text changed at line {i}")
        if before.lstrip().startswith("#") and audit.HAN.search(before):
            prefix = before[:audit.HAN.search(before).start()]
            require(after.startswith(prefix), f"Heading prefix changed at line {i}")
        if i in chinese - held:
            require(not punctuation_changes(after),
                    f"Punctuation normalization required at line {i}")
    before = audit.parse_document(SOURCE, original.decode())
    after = audit.parse_document(SOURCE, actual.decode())
    protected_before = audit.protected(before)
    require(protected_before == snapshot, "Parser does not match original baseline")
    protected_after = audit.protected(after)
    for key, value in protected_before.items():
        if key != "sha256":
            require(value == protected_after[key], f"Protected mismatch: {key}")
    for key in ("codes", "links", "footnotes", "html", "explicit_ids"):
        require(before[key] == after[key], f"Content or source positions changed: {key}")
    require(token_shape(audit.MD.parse(original.decode()))
            == token_shape(audit.MD.parse(actual.decode())),
            "Markdown block or inline token structure changed")
    return {
        "status": "pass",
        "scope": "chapter_only",
        "source": SOURCE,
        "git_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(actual),
        "physical_lines": len(old),
        "reviewed_chinese_lines": len(chinese),
        "edited_chinese_lines": len(edited),
        "retained_chinese_lines": len(retained),
        "held_chinese_lines": len(held),
        "reviewed_unchanged_lines": RETAINED,
        "held_lines": HELD,
        "non_chinese_lines_unchanged": len(old) - len(chinese),
        "english_line_hashes": len(protected_before["english_line_hashes"]),
        "english_segment_hashes": len(protected_before["english_segment_hashes"]),
        "code_items": len(before["codes"]),
        "links": len(before["links"]),
        "footnote_markers": len(before["footnotes"]),
        "structural_items": len(before["structures"]),
        "html_items": len(before["html"]),
        "punctuation_residuals": 0,
        "protection_exceptions": [],
        "manifest_reconstruction": "byte_exact",
        "markdown_token_structure": "unchanged",
        "link_labels_targets_and_positions": "unchanged",
        "line_endings_indentation_and_trailing_spaces": "unchanged",
        "source_notes": [
            "Lines 304 and 410 retain LSC in the protected heading prefix.",
            "Existing English typography and footnote layout are unchanged.",
            "Historical claims are translated, not checked against current tools.",
        ],
    }


def self_test(original, actual, manifest, snapshot):
    rejected = []
    mutations = [
        ("english", 12, "Think for a moment", "Think for two moments"),
        ("heading_prefix", 304, "LSC Infrastructure", "LSC Infrastructure!"),
        ("link_target", 348, "https://oreil.ly/c6xvO", "https://example.invalid"),
        ("link_label", 348, "[ClangMR]", "[ClangXX]"),
        ("inline_code", 390, "refactor.article", "refactor.txt"),
        ("footnote", 26, "[^1]", "[^999]"),
        ("indentation", 14, "", " "),
        ("trailing_space", 14, "\n", "  \n"),
        ("punctuation", 14, "\uff1f", "?"),
        ("markup", 288, "*", "**"),
    ]
    for name, number, old_text, replacement in mutations:
        lines = actual.decode().splitlines(keepends=True)
        lines[number - 1] = lines[number - 1].replace(old_text, replacement, 1)
        bad_manifest = copy.deepcopy(manifest)
        if str(number) in bad_manifest["replacements"]:
            bad_manifest["replacements"][str(number)] = lines[number - 1].rstrip("\r\n")
        try:
            validate(original, "".join(lines).encode(), bad_manifest, snapshot)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError(f"Mutation was not rejected: {name}")
    cases = []
    bad = copy.deepcopy(manifest)
    bad["baseline_sha256"] = "0" * 64
    cases.append(("manifest_hash", actual, bad))
    bad = copy.deepcopy(manifest)
    bad["reviewed_unchanged_lines"].append(14)
    cases.append(("coverage_overlap", actual, bad))
    bad = copy.deepcopy(manifest)
    bad["reviewed_unchanged_lines"].remove(6)
    cases.append(("coverage_gap", actual, bad))
    bad = copy.deepcopy(manifest)
    bad["held_lines"] = {"6": "Unapproved hold"}
    cases.append(("false_hold", actual, bad))
    cases.append(("line_count", actual + b"\n", manifest))
    for name, data, bad in cases:
        try:
            validate(original, data, bad, snapshot)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError(f"Mutation was not rejected: {name}")
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    original, snapshot = load_original()
    actual = (ROOT / SOURCE).read_bytes()
    if args.write_manifest:
        left, right = original.decode().splitlines(), actual.decode().splitlines()
        require(len(left) == len(right), "Cannot generate manifest across line changes")
        manifest = {
            "source": SOURCE,
            "baseline_sha256": audit.digest(original),
            "replacements": {str(i): b for i, (a, b) in enumerate(zip(left, right), 1)
                             if a != b},
            "reviewed_unchanged_lines": RETAINED,
            "held_lines": HELD,
        }
    else:
        manifest = json.loads((OUT / "edits.json").read_text())
    result = validate(original, actual, manifest, snapshot)
    if args.self_test:
        result["negative_tests_passed"] = self_test(
            original, actual, manifest, snapshot
        )
    if args.write_manifest:
        audit.dump(OUT / "edits.json", manifest)
    if args.write_report:
        audit.dump(OUT / "verification.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
