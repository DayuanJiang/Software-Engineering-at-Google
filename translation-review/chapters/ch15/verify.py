"""Verify Chapter 15 only; never change chapter text or shared review files."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

SOURCE = "zh-cn/Chapter-15_Deprecation/Chapter-15_Deprecation.md"
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
SHA256 = "114e9618b455fd7906c8d93c0a69bd98706e4c785a348d927103ff5d88427278"
UNCHANGED = [5, 118, 132, 186, 232, 252, 266, 286, 296]
HELD = {}
REVIEWED = {
    5, 13, 15, 19, 23, 27, 31, 33, 37, 41, 45, 49, 54, 60, 62, 66,
    70, 74, 80, 86, 90, 92, 96, 100, 104, 111, 113, 114, 118, 122,
    126, 130, 132, 136, 138, 142, 146, 150, 154, 156, 160, 164, 168,
    172, 176, 180, 184, 186, 190, 194, 198, 202, 206, 210, 212, 216,
    218, 222, 226, 230, 232, 236, 240, 244, 246, 250, 252, 256, 260,
    264, 266, 270, 272, 276, 280, 284, 286, 292, 294, 296, 303, 304,
    305, 306,
}
PUNCTUATION = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))
QUOTES = {
    "\u300c": "\u201c", "\u300d": "\u201d",
    "\u300e": "\u2018", "\u300f": "\u2019",
}
CHINESE_PUNCTUATION = "\u201c\u201d\u2018\u2019\u300a\u300b\u3010\u3011\u3001\u3002\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def cjk(char):
    return bool(char) and (bool(audit.HAN.search(char)) or char in CHINESE_PUNCTUATION)


def normalize_text(text):
    chars = [QUOTES.get(char, char) for char in text]
    for i, char in enumerate(chars):
        left = chars[i - 1] if i else ""
        right = chars[i + 1] if i + 1 < len(chars) else ""
        if char in PUNCTUATION and (cjk(left) or cjk(right)):
            chars[i] = PUNCTUATION[char]
    return "".join(chars)


def punctuation_residuals(line):
    # Only text nodes are checked; inline code, URLs and markup stay protected.
    residuals = 0
    for token in audit.MD.parseInline(line):
        for child in token.children or []:
            if child.type != "text":
                continue
            text = child.content
            normalized = normalize_text(text)
            residuals += sum(a != b for a, b in zip(text, normalized))
            residuals += text.count('"')
    return residuals


def block_skeleton(text):
    return [
        (token.type, token.tag, token.nesting, token.level, token.map,
         token.markup, token.block, token.hidden, token.attrs)
        for token in audit.MD.parse(text)
    ]


def eol(line):
    return "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""


def verify(manifest, original, current, baseline):
    require(manifest["source"] == SOURCE, "Unexpected source")
    require(manifest["baseline_sha256"] == SHA256, "Manifest baseline mismatch")
    old_lines = original.decode("utf-8").splitlines(keepends=True)
    new_lines = current.decode("utf-8").splitlines(keepends=True)
    require(len(old_lines) == len(new_lines) == 306, "Line count changed")
    chinese = {i for i, line in enumerate(old_lines, 1) if audit.HAN.search(line)}
    changed = {int(n) for n in manifest["replacements"]}
    unchanged = set(manifest["reviewed_unchanged_lines"])
    held = {int(n) for n in manifest["held_lines"]}
    require(chinese == REVIEWED, "Chinese line inventory changed")
    require(unchanged == set(UNCHANGED) and manifest["held_lines"] == HELD,
            "Review decisions changed")
    require(not (changed & unchanged or changed & held or unchanged & held),
            "Coverage categories overlap")
    require(changed | unchanged | held == chinese, "Incomplete coverage")
    expected = list(old_lines)
    for number in changed:
        replacement = manifest["replacements"][str(number)]
        require("\n" not in replacement and "\r" not in replacement,
                f"Multiline replacement: {number}")
        require(audit.HAN.search(replacement), f"Chinese removed: {number}")
        require(replacement != old_lines[number - 1].rstrip("\r\n"),
                f"No-op replacement: {number}")
        expected[number - 1] = replacement + eol(old_lines[number - 1])
    require("".join(expected).encode("utf-8") == current, "Manifest replay differs")

    for number, (old, new) in enumerate(zip(old_lines, new_lines), 1):
        require(eol(old) == eol(new), f"Line ending changed: {number}")
        require(re.match(r"^[ \t]*", old)[0] == re.match(r"^[ \t]*", new)[0],
                f"Indentation changed: {number}")
        require(re.search(r"[ \t]*$", old.rstrip("\r\n"))[0]
                == re.search(r"[ \t]*$", new.rstrip("\r\n"))[0],
                f"Trailing whitespace/hard break changed: {number}")
        if number not in changed:
            require(old == new, f"Unlisted change: {number}")
        if old.startswith("#") and audit.HAN.search(old):
            prefix = re.match(r"^#+[ \t]+(?:[A-Za-z][\x20-\x7e]*[ \t]+)?", old)[0]
            require(new.startswith(prefix), f"Heading prefix changed: {number}")
            suffix = re.search(r"(\([A-Za-z][^\n]*\))\s*$", old)
            if suffix:
                require(new.rstrip().endswith(suffix[1]),
                        f"English heading suffix changed: {number}")
        require(audit.FOOTNOTE.findall(old) == audit.FOOTNOTE.findall(new),
                f"Footnote markers moved: {number}")

    before = audit.parse_document(SOURCE, original.decode("utf-8"))
    after = audit.parse_document(SOURCE, current.decode("utf-8"))
    a, b = audit.protected(before), audit.protected(after)
    require(a == baseline, "Git snapshot does not reproduce saved baseline")
    for key in a:
        if key != "sha256":
            require(a[key] == b[key], f"Protected field changed: {key}")
    for key in ("codes", "links", "html", "explicit_ids", "footnotes"):
        require(before[key] == after[key], f"Protected locations changed: {key}")
    require(block_skeleton(original.decode()) == block_skeleton(current.decode()),
            "Markdown block skeleton changed")
    residuals = {
        str(n): punctuation_residuals(new_lines[n - 1])
        for n in REVIEWED
        if punctuation_residuals(new_lines[n - 1])
    }
    require(not residuals, f"Chinese punctuation residuals: {residuals}")

    return {
        "status": "passed",
        "scope": "chapter_only",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": SHA256,
        "current_sha256": audit.digest(current),
        "physical_lines": len(old_lines),
        "reviewed_chinese_lines": len(REVIEWED),
        "edited_chinese_lines": len(changed),
        "reviewed_unchanged_lines": sorted(unchanged),
        "held_lines": manifest["held_lines"],
        "completed_chinese_lines": len(changed | unchanged),
        "english_lines": len(a["english_line_hashes"]),
        "english_segments": len(a["english_segment_hashes"]),
        "protected_code_items": len(a["code_hashes"]),
        "code_kinds": dict(Counter(c["kind"] for c in before["codes"])),
        "links": len(a["links"]),
        "footnote_markers": len(a["footnotes"]),
        "structural_items": len(a["structures"]),
        "html_items": len(a["html_hashes"]),
        "image_references": sum(link["kind"] == "image" for link in a["links"]),
        "indented_chinese_code_holds": [],
        "protected_mismatches": [],
        "protection_exceptions": [],
        "punctuation_residuals": 0,
        "punctuation_normalization": "idempotent_on_all_reviewed_chinese_text_nodes",
        "manifest_replay_exact": True,
        "line_endings_and_hard_breaks_unchanged": True,
        "block_skeleton_unchanged": True,
        "english_heading_prefixes_and_suffixes_unchanged": True,
        "source_issues": [
            {"lines": [47, 49], "status": "parent_review_pending",
             "issue": "English starts with a truncated duplicate; Chinese renders the complete content once."},
            {"lines": [52, 78], "status": "parent_review_pending",
             "issue": "Existing English sentence joins and missing spaces are retained."},
            {"lines": [116, 118, 258, 260], "status": "parent_review_pending",
             "issue": "Chapter 16 and Chapter 23 cross-references are retained, not reassigned."},
            {"lines": [98, 100, 128, 130, 196, 198, 208, 210],
             "status": "parent_review_pending",
             "issue": "Chinese lacks mirrored footnote markers; English footnote 2 lacks a definition colon. Original markers and layout retained."},
            {"lines": [228, 230], "status": "parent_review_pending",
             "issue": "Source recommends both primary-team ownership and 20% time; both claims retained without inventing a reconciliation."},
        ],
        "limitations": [
            "Semantic coverage is the editor's bilingual review, not a machine translation-quality proof.",
            "No other chapter, asset directory, shared report or shared test suite is validated or rewritten.",
            "No official-source, external-link-reachability or browser-render check was performed.",
            "Source issues are preserved pending parent review, not counted as repaired.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-artifacts", action="store_true")
    args = parser.parse_args()
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Baseline commit changed")
    require(baseline["files"][SOURCE]["sha256"] == SHA256, "Baseline hash changed")
    original = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"])
    require(audit.digest(original) == SHA256, "Git content hash mismatch")
    current = (ROOT / SOURCE).read_bytes()
    if args.write_artifacts:
        old = original.decode().splitlines()
        new = current.decode().splitlines()
        require(len(old) == len(new), "Cannot record a line-structure change")
        manifest = {
            "source": SOURCE,
            "baseline_sha256": SHA256,
            "replacements": {str(i): b for i, (a, b) in enumerate(zip(old, new), 1) if a != b},
            "reviewed_unchanged_lines": UNCHANGED,
            "held_lines": HELD,
        }
    else:
        manifest = json.loads((OUT / "edits.json").read_text())
    result = verify(manifest, original, current, baseline["files"][SOURCE])
    if args.write_artifacts:
        audit.dump(OUT / "edits.json", manifest)
        audit.dump(OUT / "verification-detailed.json", result)
    else:
        saved = json.loads((OUT / "verification-detailed.json").read_text())
        require(saved == result, "Saved verification report is stale")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
