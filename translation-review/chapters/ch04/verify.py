"""Record and verify only the Chapter 4 Chinese edits against the frozen snapshot."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools"))

import translation_audit as audit

SOURCE = "zh-cn/Chapter-4_Engineering_for_Equity/Chapter-4_Engineering_for_Equity.md"
SNAPSHOT = "110720f031b43e18708fdc38af03269b65b3cc41"
RETAINED = [40, 75, 86, 149, 175, 227, 245, 251]
HOLDS = {
    "112": (
        "The English at line 110 joins 'will eliminate the potential ... to experience "
        "shared prosperity' with 'and provide equal access to technology'. The intended "
        "scope and polarity are unclear. Retain the entire Chinese line pending source "
        "review; do not silently replace eliminate with enable or negate it."
    ),
    "137": (
        "Existing Chinese bibliography names Georgetown's Center on Privacy & Technology "
        "and 2016-10-18, but no corresponding English appears in the local chapter. "
        "Retain it pending source/provenance review; do not invent an English counterpart."
    ),
}
PREFIX = re.compile(r"^\s*(?:>\s*)*(?:(?:#{1,6}|[-+*]|\d+[.)])\s+)?")
LINK = re.compile(r"!?\[[^\]]*\]\([^)]*\)")
MASK = re.compile(r"!?\[[^\]]*\]\([^)]*\)|`+[^`]*`+|https?://[^\s<>\"`]+|<[^>]+>")
CJK_EXTRA = set("“”‘’·—…《》〈〉「」『』【】、。，！？；：（）")
PUNCTUATION = str.maketrans({",": "，", ";": "；", ":": "：", "?": "？",
                           "!": "！", "(": "（", ")": "）"})


def is_cjk(char):
    return bool(char) and (
        0x3400 <= ord(char) <= 0x9FFF
        or 0x3000 <= ord(char) <= 0x303F
        or 0xFF00 <= ord(char) <= 0xFFEF
        or char in CJK_EXTRA
    )


def normalize_punctuation(line):
    """Apply the skill's punctuation rules without touching protected inline spans."""
    heading_end = audit.HAN.search(line).start() if line.lstrip().startswith("#") else 0
    prefix, text = line[:heading_end], line[heading_end:]
    stored = []

    def mask(match):
        stored.append(match[0])
        return f"\x00{len(stored) - 1}\x00"

    text = MASK.sub(mask, text)
    chars = []
    opening = True
    quote_map = {"「": "“", "」": "”", "『": "‘", "』": "’"}
    for char in text:
        if char == '"':
            chars.append("“" if opening else "”")
            opening = not opening
        else:
            chars.append(quote_map.get(char, char))
    for index, char in enumerate(chars):
        left = chars[index - 1] if index else ""
        right = chars[index + 1] if index + 1 < len(chars) else ""
        if ord(char) in PUNCTUATION and (is_cjk(left) or is_cjk(right)):
            chars[index] = char.translate(PUNCTUATION)
    text = re.sub(r"\x00(\d+)\x00", lambda m: stored[int(m[1])], "".join(chars))
    return prefix + text


def save(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-edits", action="store_true")
    parser.add_argument("--write-verification", action="store_true")
    args = parser.parse_args()
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    original = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{SNAPSHOT}:{SOURCE}"])
    current = (ROOT / SOURCE).read_bytes()
    original_hash = audit.digest(original)
    assert baseline["git_commit"] == SNAPSHOT
    assert baseline["files"][SOURCE]["sha256"] == original_hash
    old = original.decode().splitlines(keepends=True)
    new = current.decode().splitlines(keepends=True)
    assert len(old) == len(new), "Physical line count changed"
    chinese = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changes = {
        str(i): after.rstrip("\r\n")
        for i, (before, after) in enumerate(zip(old, new), 1)
        if before != after
    }
    changed = set(map(int, changes))
    held = set(map(int, HOLDS))
    retained = set(RETAINED)
    assert changed <= chinese, "Non-Chinese line edited"
    assert not (changed & held or changed & retained or held & retained)
    assert changed | retained | held == chinese, "Incomplete or overlapping coverage"
    for number, (before, after) in enumerate(zip(old, new), 1):
        assert re.search(r"\r?\n?$", before)[0] == re.search(r"\r?\n?$", after)[0]
        assert re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0]
        assert PREFIX.match(before)[0] == PREFIX.match(after)[0], number
        assert LINK.findall(before) == LINK.findall(after), number
        assert audit.URL.findall(before) == audit.URL.findall(after), number
        assert audit.FOOTNOTE.findall(before) == audit.FOOTNOTE.findall(after), number
        assert re.findall(r"[*_`]+", before) == re.findall(r"[*_`]+", after), number
        if before.lstrip().startswith("#") and audit.HAN.search(before):
            first_han = audit.HAN.search(before).start()
            assert before[:first_han] == after[:first_han], number
    before = audit.parse_document(SOURCE, original.decode())
    after = audit.parse_document(SOURCE, current.decode())
    expected_protected = audit.protected(before)
    actual_protected = audit.protected(after)
    assert expected_protected == baseline["files"][SOURCE], "Baseline parser mismatch"
    mismatches = [
        key for key in expected_protected
        if key != "sha256" and expected_protected[key] != actual_protected[key]
    ]
    assert not mismatches, mismatches
    assert before["codes"] == after["codes"]
    assert before["links"] == after["links"]
    assert before["footnotes"] == after["footnotes"]
    normalization_residuals = [
        i for i in sorted(chinese - held)
        if normalize_punctuation(new[i - 1].rstrip("\r\n")) != new[i - 1].rstrip("\r\n")
    ]
    assert not normalization_residuals, normalization_residuals
    manifest = {
        "source": SOURCE,
        "baseline_sha256": original_hash,
        "replacements": changes,
        "reviewed_unchanged_lines": RETAINED,
        "held_lines": HOLDS,
    }
    if args.record_edits:
        save("edits.json", manifest)
    assert json.loads((HERE / "edits.json").read_text()) == manifest, "Manifest mismatch"
    reconstructed = old.copy()
    for number, replacement in changes.items():
        ending = re.search(r"\r?\n?$", old[int(number) - 1])[0]
        reconstructed[int(number) - 1] = replacement + ending
    assert "".join(reconstructed).encode() == current, "Manifest reconstruction mismatch"
    result = {
        "source": SOURCE,
        "snapshot": SNAPSHOT,
        "baseline_sha256": original_hash,
        "current_sha256": audit.digest(current),
        "validation": "PASS",
        "editorial_status": "74 completed; 2 held pending source review",
        "physical_lines": len(old),
        "chinese_lines_inspected": len(chinese),
        "completed_chinese_lines": len(changed | retained),
        "changed_chinese_lines": len(changed),
        "reviewed_unchanged_lines": RETAINED,
        "held_lines": HOLDS,
        "protected_counts": {
            key: len(value) for key, value in expected_protected.items()
            if isinstance(value, list)
        },
        "protection_mismatches": mismatches,
        "punctuation_normalization_residuals": normalization_residuals,
        "manifest_reconstructs_current_bytes": True,
        "checks": [
            "Exact original Git snapshot SHA-256 equals the recorded baseline",
            "All 76 Chinese physical lines explicitly partitioned; holds not counted complete",
            "All non-Chinese lines byte-identical; mixed-heading English prefixes unchanged",
            "Line endings, trailing whitespace and Markdown prefixes unchanged",
            "Raw links, URLs, emphasis delimiters and footnote markers unchanged per line",
            "All translation_audit.protected fields unchanged except document SHA-256",
            "Parsed code, link and footnote records including positions unchanged",
            "Punctuation normalization is idempotent on every completed Chinese line",
        ],
        "limits": [
            "Only Chapter 4 validated; no all-repository assertion or shared-file writes",
            "No browser rendering or external source/link verification",
            "No agents or external model APIs used",
            "Semantic review performed by the editor, not established by mechanical checks",
            "No fenced or indented code, inline code, HTML or image items in this chapter",
        ],
    }
    if args.write_verification:
        save("verification.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
