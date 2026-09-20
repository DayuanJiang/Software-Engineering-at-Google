"""Record or verify only Chapter 5; never apply edits or inspect other chapters."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import chapter_pilot
import translation_audit as audit

DIRECTORY = Path(__file__).resolve().parent
SOURCE = "zh-cn/Chapter-5_How_to_Lead_a_Team/Chapter-5_How_to_Lead_a_Team.md"
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
RETAINED = [
    6, 34, 44, 82, 124, 134, 159, 196, 212, 256, 270, 278, 284, 294,
    300, 348, 361, 371, 381, 391, 436, 450, 468, 495, 524, 580, 586,
]
HOLDS = [
    {
        "line": 407,
        "reason": "Chinese quotation parsed as an indented code block. Preserve "
        "under the brief; the T-shirt collection wording still needs correction.",
    },
    {
        "line": 430,
        "reason": "Chinese quotation parsed as an indented code block. Preserve "
        "under the brief; jumping in front of trains, train drivers, and one "
        "driver's reaction still need correction.",
    },
]


def token_shape(source):
    result = []
    for token in audit.MD.parse(source):
        result.append((
            token.type, token.tag, token.nesting, token.level,
            token.markup, token.map, token.attrs,
            [(child.type, child.tag, child.nesting, child.markup, child.attrs)
             for child in token.children or []],
        ))
    return result


def verify(original, current, manifest):
    old_text, new_text = original.decode("utf-8"), current.decode("utf-8")
    old, new = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
    assert len(old) == len(new) == 594, "Physical line count changed"
    assert manifest["source"] == SOURCE
    assert manifest["baseline_sha256"] == audit.digest(original)
    replacements = {int(k): v for k, v in manifest["replacements"].items()}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    chinese = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    retained = set(manifest["reviewed_unchanged_lines"])
    held = {item["line"] for item in manifest["held_lines"]}
    assert manifest["reviewed_unchanged_lines"] == RETAINED
    assert manifest["held_lines"] == HOLDS
    assert len(chinese) == 168 and len(changed) == 139
    assert changed == set(replacements)
    assert not (changed & retained or changed & held or retained & held)
    assert chinese == changed | retained | held, "Incomplete Chinese coverage"
    expected = list(old)
    for number, replacement in replacements.items():
        before, after = old[number - 1], new[number - 1]
        assert audit.HAN.search(before) and audit.HAN.search(replacement)
        assert "\n" not in replacement and "\r" not in replacement
        ending = before[len(before.rstrip("\r\n")):]
        expected[number - 1] = replacement + ending
        assert re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0]
        assert re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0]
        assert re.findall(r"\*+|_+", before) == re.findall(r"\*+|_+", after)
        if before.lstrip().startswith("#"):
            prefix = before[:audit.HAN.search(before).start()]
            assert after.startswith(prefix), f"Heading prefix changed: {number}"
    assert "".join(expected).encode("utf-8") == current, "Manifest mismatch"
    for number in retained | held:
        assert old[number - 1] == new[number - 1]

    # Protect the complete inline URL before using the pilot's prose normalizer.
    for number in chinese - held:
        line = audit.URL.sub("URL", new[number - 1].rstrip("\r\n"))
        assert chapter_pilot.normalize_chinese_line(line) == line, number
        assert not re.search(r'["\u300c\u300d\u300e\u300f]|\.\.\.', line), number

    before = audit.parse_document(SOURCE, old_text)
    after = audit.parse_document(SOURCE, new_text)
    protected_before, protected_after = audit.protected(before), audit.protected(after)
    mismatches = [
        key for key in protected_before
        if key != "sha256" and protected_before[key] != protected_after[key]
    ]
    assert not mismatches, f"Protected content mismatch: {mismatches}"
    assert token_shape(old_text) == token_shape(new_text), "Markdown token shape changed"
    protected_chinese = set()
    for token in audit.MD.parse(old_text):
        if token.type in {"fence", "code_block", "html_block"} and token.map:
            for index in range(*token.map):
                if audit.HAN.search(old[index]):
                    protected_chinese.add(index + 1)
                    assert old[index] == new[index]
    assert held == protected_chinese
    return {
        "source": SOURCE,
        "git_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "after_sha256": audit.digest(current),
        "validation": "PASS",
        "editorial_status": "complete_except_two_protected_prose_holds",
        "physical_lines": len(old),
        "chinese_lines_inspected": len(chinese),
        "chinese_lines_completed": len(changed | retained),
        "changed_lines": len(changed),
        "reviewed_unchanged_lines": len(retained),
        "held_line_count": len(held),
        "held_lines": sorted(held),
        "unaccounted_chinese_lines": 0,
        "protected_mismatches": mismatches,
        "english_lines": len(protected_before["english_line_hashes"]),
        "english_segments": len(protected_before["english_segment_hashes"]),
        "protected_code_items": len(protected_before["code_hashes"]),
        "links": len(protected_before["links"]),
        "footnote_markers": len(protected_before["footnotes"]),
        "structural_items": len(protected_before["structures"]),
        "markdown_token_shape_unchanged": True,
        "line_endings_indentation_and_hard_breaks_unchanged": True,
        "punctuation_residuals_completed_lines": 0,
        "code_exceptions": [],
        "scope": "Only the assigned chapter is validated; no all-repository assertions.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true",
                        help="Derive the initial manifest and validation artifact.")
    args = parser.parse_args()
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    original = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"])
    assert audit.digest(original) == baseline["files"][SOURCE]["sha256"]
    current = (ROOT / SOURCE).read_bytes()
    manifest_path = DIRECTORY / "edits.json"
    if args.record:
        assert not manifest_path.exists(), "Refusing to overwrite an existing review manifest"
        old, new = original.decode().splitlines(), current.decode().splitlines()
        manifest = {
            "source": SOURCE,
            "baseline_sha256": baseline["files"][SOURCE]["sha256"],
            "replacements": {
                str(i): b for i, (a, b) in enumerate(zip(old, new), 1) if a != b
            },
            "reviewed_unchanged_lines": RETAINED,
            "held_lines": HOLDS,
        }
    else:
        manifest = json.loads(manifest_path.read_text())
    result = verify(original, current, manifest)
    if args.record:
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        (DIRECTORY / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    else:
        assert result == json.loads((DIRECTORY / "verification.json").read_text())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
