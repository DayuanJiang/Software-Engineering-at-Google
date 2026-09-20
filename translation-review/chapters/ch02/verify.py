"""Verify only Chapter 2; optionally derive its manifest and verification record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCE = "zh-cn/Chapter-2_How_to_Work_Well_on_Teams/Chapter-2_How_to_Work_Well_on_Teams.md"
COMMIT = "110720f031b43e18708fdc38af03269b65b3cc41"
REVIEWED_UNCHANGED = [
    28, 51, 102, 103, 107, 120, 156, 172, 186, 200, 275, 294, 297, 298,
    300, 310, 320, 328, 334, 352, 374, 403, 423, 425, 426, 429, 431, 497,
    503, 505, 512, 518,
]

sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit


def normalize_punctuation(line: str) -> str:
    """Apply the skill's adjacent-CJK rules outside protected inline syntax."""
    prefix = ""
    if line.lstrip().startswith("#"):
        offset = audit.HAN.search(line).start()
        prefix, line = line[:offset], line[offset:]
    protected = re.compile(r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]*>|&\w+;")
    pieces = []
    end = 0
    punctuation = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))

    def is_cjk(char: str) -> bool:
        return bool(char) and (
            "\u3400" <= char <= "\u9fff"
            or "\u3000" <= char <= "\u303f"
            or "\uff00" <= char <= "\uffef"
            or char in "\u201c\u201d\u2018\u2019\u00b7\u2014\u2026"
        )

    def normalize(text: str) -> str:
        chars = list(text)
        opening = True
        for i, char in enumerate(chars):
            if char == '"':
                chars[i] = "\u201c" if opening else "\u201d"
                opening = not opening
            elif char in "\u300c\u300e":
                chars[i] = "\u201c" if char == "\u300c" else "\u2018"
            elif char in "\u300d\u300f":
                chars[i] = "\u201d" if char == "\u300d" else "\u2019"
        for i, char in enumerate(chars):
            before = chars[i - 1] if i else ""
            after = chars[i + 1] if i + 1 < len(chars) else ""
            if char in punctuation and (is_cjk(before) or is_cjk(after)):
                chars[i] = punctuation[char]
        return "".join(chars)

    for match in protected.finditer(line):
        pieces.extend((normalize(line[end:match.start()]), match[0]))
        end = match.end()
    pieces.append(normalize(line[end:]))
    return prefix + "".join(pieces)


def verify(write_artifacts: bool) -> dict:
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"]
    )
    current = (ROOT / SOURCE).read_bytes()
    assert baseline["git_commit"] == COMMIT
    assert audit.digest(original) == baseline["files"][SOURCE]["sha256"]
    old_lines = original.decode().splitlines(keepends=True)
    new_lines = current.decode().splitlines(keepends=True)
    assert len(old_lines) == len(new_lines) == 526
    before_doc = audit.parse_document(SOURCE, original.decode())
    after_doc = audit.parse_document(SOURCE, current.decode())
    before, after = audit.protected(before_doc), audit.protected(after_doc)
    assert before == baseline["files"][SOURCE]
    for key in before:
        if key != "sha256":
            assert before[key] == after[key], f"Protected field changed: {key}"

    replacements = {}
    chinese_lines = set()
    for number, (old, new) in enumerate(zip(old_lines, new_lines), 1):
        if audit.HAN.search(old):
            chinese_lines.add(number)
        else:
            assert old == new, f"Non-Chinese line changed: {number}"
        assert re.match(r"^\s*", old)[0] == re.match(r"^\s*", new)[0]
        assert re.search(r"\s*$", old)[0] == re.search(r"\s*$", new)[0]
        assert re.findall(r"\[\^[^\]]+\]", old) == re.findall(r"\[\^[^\]]+\]", new)
        assert re.findall(r"&\w+;", old) == re.findall(r"&\w+;", new)
        assert re.findall(r"[*`]", old) == re.findall(r"[*`]", new)
        if old.lstrip().startswith("#") and audit.HAN.search(old):
            offset = audit.HAN.search(old).start()
            assert old[:offset] == new[:offset], f"Heading prefix changed: {number}"
        if old != new:
            assert number in chinese_lines
            replacement = new.removesuffix("\n").removesuffix("\r")
            assert normalize_punctuation(replacement) == replacement, (
                f"Punctuation normalization needed: {number}"
            )
            replacements[str(number)] = replacement

    edited = {int(number) for number in replacements}
    retained = set(REVIEWED_UNCHANGED)
    assert not edited & retained
    assert edited | retained == chinese_lines
    assert all(old_lines[n - 1] == new_lines[n - 1] for n in retained)
    manifest = {
        "source": SOURCE,
        "baseline_sha256": baseline["files"][SOURCE]["sha256"],
        "replacements": replacements,
        "reviewed_unchanged_lines": REVIEWED_UNCHANGED,
        "held_lines": [],
    }
    if not write_artifacts:
        assert json.loads((OUT / "edits.json").read_text()) == manifest
    replay = old_lines[:]
    for number, replacement in replacements.items():
        index = int(number) - 1
        newline = "\r\n" if old_lines[index].endswith("\r\n") else (
            "\n" if old_lines[index].endswith("\n") else ""
        )
        replay[index] = replacement + newline
    assert "".join(replay).encode() == current
    report = {
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "result_sha256": audit.digest(current),
        "physical_lines": len(old_lines),
        "chinese_lines_reviewed": len(chinese_lines),
        "chinese_lines_edited": len(edited),
        "chinese_lines_retained": len(retained),
        "held_lines": [],
        "protected_item_counts": {
            key: len(value) for key, value in before.items() if isinstance(value, list)
        },
        "protected_mismatches": [],
        "non_chinese_lines_unchanged": True,
        "line_endings_and_boundary_whitespace_unchanged": True,
        "english_heading_prefixes_unchanged": True,
        "inline_entities_and_markers_unchanged": True,
        "manifest_replay_matches": True,
        "changed_line_punctuation_residuals": 0,
        "external_links_checked": False,
        "scope": "Chapter 2 only; no assertions about concurrently edited chapters",
        "status": "passed",
    }
    if write_artifacts:
        for filename, data in (("edits.json", manifest), ("verification.json", report)):
            (OUT / filename).write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
    else:
        assert json.loads((OUT / "verification.json").read_text()) == report
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-artifacts", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.write_artifacts), ensure_ascii=False, indent=2))
