"""Validate Chapter 9 only; optionally regenerate its review artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCE = "zh-cn/Chapter-9_Code_Review/Chapter-9_Code_Review.md"
SNAPSHOT = "679725c08143c724598a2b89b94b8c8e4fa47688"
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit


REVIEWED_UNCHANGED = [
    6, 32, 58, 122, 128, 154, 175, 177, 180, 190, 224, 238, 260,
    282, 364, 397, 399, 409, 481, 487, 499,
]
HELD_LINES = {}
PREFIX = re.compile(r"^[ \t]*(?:> ?)*(?:#{1,6} |(?:[-+*]|\d+[.)])[ \t]+)?")
LINK = re.compile(r"!?\[[^\]\n]*\]\([^)\n]*\)")
INLINE = re.compile(r"`+[^`\n]*`+|<[^>\n]+>")
PUNCTUATION = {",": "\uff0c", ";": "\uff1b", ":": "\uff1a",
               "?": "\uff1f", "!": "\uff01", "(": "\uff08", ")": "\uff09"}
CJK_EXTRA = set("\u201c\u201d\u2018\u2019\u00b7\u2014\u2026"
                "\u300a\u300b\u3008\u3009\u300c\u300d\u300e\u300f"
                "\u3010\u3011\u3001\u3002\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09")


def is_cjk(char):
    return bool(char) and (
        "\u3400" <= char <= "\u9fff" or "\u3000" <= char <= "\u303f"
        or "\uff00" <= char <= "\uffef" or char in CJK_EXTRA
    )


def normalized_chinese(line):
    """Apply skill punctuation rules without touching source/Markdown spans."""
    first_han = audit.HAN.search(line)
    if not first_han:
        return line
    prefix, prose = line[:first_han.start()], line[first_han.start():]
    saved = []

    def protect(match):
        saved.append(match.group())
        return f"\x00{len(saved) - 1}\x00"

    prose = LINK.sub(protect, prose)
    prose = INLINE.sub(protect, prose)
    result = []
    opening = True
    for char in prose:
        if char == '"':
            result.append("\u201c" if opening else "\u201d")
            opening = not opening
        else:
            result.append({
                "\u300c": "\u201c", "\u300d": "\u201d",
                "\u300e": "\u2018", "\u300f": "\u2019",
            }.get(char, char))
    for i, char in enumerate(result):
        previous = result[i - 1] if i else ""
        following = result[i + 1] if i + 1 < len(result) else ""
        if char in PUNCTUATION and (is_cjk(previous) or is_cjk(following)):
            result[i] = PUNCTUATION[char]
    prose = re.sub(r"\x00(\d+)\x00", lambda m: saved[int(m[1])], "".join(result))
    return prefix + prose


def validate(original, current, baseline, edits):
    before = original.splitlines(keepends=True)
    after = current.splitlines(keepends=True)
    old_doc = audit.parse_document(SOURCE, original)
    new_doc = audit.parse_document(SOURCE, current)
    old_protected, new_protected = audit.protected(old_doc), audit.protected(new_doc)
    chinese = {i for i, line in enumerate(before, 1) if audit.HAN.search(line)}
    changed = {i for i, (a, b) in enumerate(zip(before, after), 1) if a != b}
    retained = set(edits["reviewed_unchanged_lines"])
    held = {int(i) for i in edits["held_lines"]}
    replacements = {int(i): line for i, line in edits["replacements"].items()}
    protected_keys = [key for key in old_protected if key != "sha256"]
    punctuation_lines = [
        i for i in sorted(chinese - held)
        if i <= len(after) and normalized_chinese(after[i - 1]) != after[i - 1]
    ]
    checks = {
        "snapshot_matches_baseline": old_protected == baseline,
        "manifest_source": edits["source"] == SOURCE,
        "manifest_baseline_sha256": edits["baseline_sha256"] == audit.digest(original),
        "physical_line_count": len(before) == len(after),
        "line_endings_and_trailing_whitespace": all(
            re.search(r"[ \t]*(?:\r?\n)?$", a)[0]
            == re.search(r"[ \t]*(?:\r?\n)?$", b)[0]
            for a, b in zip(before, after)
        ),
        "non_chinese_lines_byte_identical": all(
            a == b for i, (a, b) in enumerate(zip(before, after), 1) if i not in chinese
        ),
        "only_original_chinese_lines_changed": changed <= chinese,
        "chinese_line_positions": chinese == {
            i for i, line in enumerate(after, 1) if audit.HAN.search(line)
        },
        "heading_english_prefixes": all(
            bool(audit.HAN.search(b))
            and a[:audit.HAN.search(a).start()] == b[:audit.HAN.search(b).start()]
            for a, b in zip(before, after)
            if a.startswith("#") and audit.HAN.search(a)
        ),
        "markdown_line_prefixes": all(
            PREFIX.match(a)[0] == PREFIX.match(b)[0] for a, b in zip(before, after)
        ),
        "emphasis_and_backtick_markers": all(
            re.findall(r"\*+|`+", a) == re.findall(r"\*+|`+", b)
            for a, b in zip(before, after)
        ),
        "literal_markdown_links": LINK.findall(original) == LINK.findall(current),
        "footnote_line_locations": old_doc["footnotes"] == new_doc["footnotes"],
        "replacement_line_numbers": set(replacements) == changed,
        "replacement_lines_exact": all(
            1 <= i <= len(after) and after[i - 1].rstrip("\r\n") == text
            and "\n" not in text and "\r" not in text
            for i, text in replacements.items()
        ),
        "reviewed_unchanged_lines_exact": retained == set(REVIEWED_UNCHANGED)
        and len(retained) == len(edits["reviewed_unchanged_lines"])
        and retained <= chinese and not retained & changed,
        "held_lines_exact": edits["held_lines"] == HELD_LINES,
        "complete_disjoint_chinese_coverage": (
            set(replacements) | retained | held == chinese
            and not (set(replacements) & retained or set(replacements) & held or retained & held)
        ),
        "chinese_punctuation_normalization": not punctuation_lines,
    }
    checks.update({
        key: old_protected[key] == new_protected[key] for key in protected_keys
    })
    # Replaying the manifest verifies every byte, including unchanged and blank lines.
    replay = before.copy()
    for i, text in replacements.items():
        if 1 <= i <= len(before):
            ending = re.search(r"(?:\r?\n)?$", before[i - 1])[0]
            replay[i - 1] = text + ending
    checks["manifest_replay_byte_identical"] = "".join(replay) == current
    return {
        "source": SOURCE,
        "snapshot": SNAPSHOT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(current),
        "coverage": {
            "physical_lines_read": len(before),
            "original_chinese_lines": len(chinese),
            "edited_chinese_lines": len(changed & chinese),
            "reviewed_unchanged_chinese_lines": len(retained),
            "held_chinese_lines": len(held),
            "reviewed_chinese_lines": len((changed | retained) & chinese),
        },
        "protected_counts": {
            key: len(old_protected[key]) for key in protected_keys
        },
        "checks": checks,
        "punctuation_residual_lines": punctuation_lines,
        "mismatches": [key for key, passed in checks.items() if not passed],
        "limitations": [
            "Chapter 9 only; no assertion about concurrently edited files.",
            "Semantic review is manual, not established by structural checks.",
            "No browser rendering or external-link reachability validation.",
        ],
    }


def negative_tests(original, current, baseline, edits):
    probes = {
        "english_source": (
            current.replace("# Code Review", "# Changed Review", 1),
            "english_line_hashes",
        ),
        "heading_prefix": (
            current.replace("## Code Review Flow", "## Changed Review Flow", 1),
            "heading_english_prefixes",
        ),
        "line_count": (current + "\n", "physical_line_count"),
        "hard_line_break": (
            current.replace("# Code Review\n", "# Code Review  \n", 1),
            "line_endings_and_trailing_whitespace",
        ),
        "link_target": (
            current.replace("https://oreil.ly/TmoWX", "https://example.invalid/", 1),
            "links",
        ),
        "footnote_marker": (current.replace("[^1]", "[^999]", 1), "footnotes"),
        "inline_code": (current.replace("Critique", "`Critique`", 1), "code_hashes"),
        "html": (current.replace("Critique", "<b>Critique</b>", 1), "html_hashes"),
        "emphasis": (
            current.replace("***Hyrum Wright***", "**Hyrum Wright**", 1),
            "emphasis_and_backtick_markers",
        ),
        "line_order": (current.replace(
            "**CHAPTER 9**\n\n# Code Review", "# Code Review\n\n**CHAPTER 9**", 1
        ), "non_chinese_lines_byte_identical"),
    }
    results = {}
    for name, (mutated, expected_failure) in probes.items():
        assert mutated != current, name
        result = validate(original, mutated, baseline, edits)
        results[name] = expected_failure in result["mismatches"]
    missing = json.loads(json.dumps(edits))
    missing["reviewed_unchanged_lines"].remove(6)
    results["coverage_omission"] = "complete_disjoint_chinese_coverage" in validate(
        original, current, baseline, missing
    )["mismatches"]
    altered = json.loads(json.dumps(edits))
    altered["replacements"]["14"] += " "
    results["manifest_tampering"] = "replacement_lines_exact" in validate(
        original, current, baseline, altered
    )["mismatches"]
    assert all(results.values()), results
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-artifacts", action="store_true")
    args = parser.parse_args()
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{SNAPSHOT}:{SOURCE}"]
    ).decode("utf-8")
    current = (ROOT / SOURCE).read_bytes().decode("utf-8")
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())["files"][SOURCE]
    if args.write_artifacts:
        edits = {
            "source": SOURCE,
            "baseline_sha256": baseline["sha256"],
            "replacements": {
                str(i): b for i, (a, b) in enumerate(
                    zip(original.splitlines(), current.splitlines()), 1
                ) if a != b
            },
            "reviewed_unchanged_lines": REVIEWED_UNCHANGED,
            "held_lines": HELD_LINES,
        }
    else:
        edits = json.loads((OUT / "edits.json").read_text())
    report = validate(original, current, baseline, edits)
    report["negative_tests"] = negative_tests(original, current, baseline, edits)
    report["passed"] = not report["mismatches"]
    if args.write_artifacts and report["passed"]:
        for name, data in (("edits.json", edits), ("verification.json", report)):
            (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    elif not args.write_artifacts and report["passed"]:
        saved = json.loads((OUT / "verification.json").read_text())
        assert saved == report, "Saved verification report is stale."
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
