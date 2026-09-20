"""Record and strictly verify only the Chapter 21 Chinese review."""

from __future__ import annotations

import argparse
from itertools import zip_longest
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import book_review
import translation_audit as audit

SOURCE = "zh-cn/Chapter-21_Dependency_Management/Chapter-21_Dependency_Management.md"
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
OUT = Path(__file__).resolve().parent
UNCHANGED = [
    6, 44, 62, 88, 141, 160, 161, 163, 164, 165, 178, 180, 181,
    192, 231, 261, 315, 378, 400, 426, 452, 474, 550, 607, 627, 637,
]
HOLDS = {
    "186": (
        "The original full-width link parentheses cause the baseline URL parser "
        "to include the following Chinese sentence in the protected bare URL. "
        "The complete original line is retained pending parent authorization "
        "to repair the link and review the resulting protected-content change. "
        "A proposed translation is in notes.md; this line is not completed."
    )
}
SECTIONS = [
    ("Introduction", 1, 43),
    ("Challenges and diamond dependencies", 44, 87),
    ("Importing dependencies", 88, 230),
    ("Four management models", 231, 341),
    ("SemVer limitations and MVS", 342, 473),
    ("Infinite-resources thought experiment", 474, 549),
    ("Exporting dependencies and case studies", 550, 626),
    ("Conclusion and TLDR", 627, 659),
]
PUNCTUATION = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))
QUOTES = str.maketrans({
    "\u300c": "\u201c", "\u300d": "\u201d",
    "\u300e": "\u2018", "\u300f": "\u2019",
})
# These exact inline forms cover this chapter; the parsed protection checks below
# independently verify all code, links, HTML, and source text without exceptions.
INLINE = re.compile(
    r"`[^`\n]+`|!?\[[^\]\n]*\]\([^)\n]*\)|https?://[^\s<>\"`]+"
)


def is_chinese(char: str) -> bool:
    return bool(audit.HAN.search(char)) or char in (
        "\u201c\u201d\u2018\u2019\u300a\u300b\u3010\u3011"
        "\u3001\u3002\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09"
    )


def normalized_punctuation(line: str) -> str:
    protected = set()
    if line.startswith(("#", "*Figure")):
        first = audit.HAN.search(line)
        if first:
            protected.update(range(first.start()))
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
        else:
            chars[i] = char.translate(QUOTES)
    for i, char in enumerate(chars):
        if i not in protected and char in PUNCTUATION:
            left = chars[i - 1] if i else ""
            right = chars[i + 1] if i + 1 < len(chars) else ""
            if is_chinese(left) or is_chinese(right):
                chars[i] = PUNCTUATION[char]
    return "".join(chars)


def inline_structure(source: str) -> list:
    return [
        (token.type, token.tag, token.nesting, token.markup,
         [(child.type, child.tag, child.nesting, child.markup)
          for child in token.children or []])
        for token in audit.MD.parse(source)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true",
                        help="Generate the manifest from the reviewed chapter diff.")
    args = parser.parse_args()
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    assert baseline["git_commit"] == COMMIT
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"]
    )
    assert audit.digest(original) == baseline["files"][SOURCE]["sha256"]
    actual = (ROOT / SOURCE).read_bytes()
    old, new = [data.decode("utf-8").splitlines(keepends=True)
                for data in (original, actual)]
    assert len(old) == len(new) == 659, (len(old), len(new))
    chinese = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changed = {}
    for i, (before, after) in enumerate(zip(old, new, strict=True), 1):
        assert re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0], (
            "Line ending or trailing whitespace changed", i
        )
        assert re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0], (
            "Indentation changed", i
        )
        if before == after:
            continue
        assert i in chinese and audit.HAN.search(after), ("Non-Chinese edit", i)
        if before.startswith(("#", "*Figure")):
            assert before[:audit.HAN.search(before).start()] == (
                after[:audit.HAN.search(after).start()]
            ), ("English heading/caption prefix changed", i)
        changed[str(i)] = after.rstrip("\r\n")
    candidate = {
        "source": SOURCE,
        "baseline_sha256": baseline["files"][SOURCE]["sha256"],
        "replacements": changed,
        "reviewed_unchanged_lines": UNCHANGED,
        "held_lines": HOLDS,
    }
    manifest_path = OUT / "edits.json"
    manifest = candidate if args.record else json.loads(manifest_path.read_text())
    assert manifest == candidate, "Manifest differs from reviewed line decisions."
    groups = [set(map(int, changed)), set(UNCHANGED), set(map(int, HOLDS))]
    assert sum(map(len, groups)) == len(set.union(*groups)) == len(chinese)
    assert set.union(*groups) == chinese
    assert len(UNCHANGED) == len(set(UNCHANGED))
    for i in groups[1] | groups[2]:
        assert old[i - 1] == new[i - 1]
    documents = [audit.parse_document(SOURCE, data.decode("utf-8"))
                 for data in (original, actual)]
    before, after = map(audit.protected, documents)
    assert before == baseline["files"][SOURCE]
    for key in before:
        if key != "sha256":
            assert before[key] == after[key], ("Protected content changed", key)
    for key in ("codes", "links", "html", "explicit_ids", "footnotes"):
        assert documents[0][key] == documents[1][key], ("Positions changed", key)
    skeletons = [inline_structure(data.decode("utf-8")) for data in (original, actual)]
    differences = [i for i, (a, b) in enumerate(
        zip_longest(*skeletons), 1
    ) if a != b]
    assert not differences, ("Markdown token structure changed", differences)
    residuals = [i for i in sorted(chinese - groups[2])
                 if normalized_punctuation(new[i - 1]) != new[i - 1]]
    assert not residuals, ("Chinese punctuation residuals", residuals)
    counts = book_review.validate(SOURCE, original, actual, manifest)
    assert not counts["prose_code_exceptions"], "No protection exceptions permitted."
    coverage = []
    for title, start, end in SECTIONS:
        region = chinese & set(range(start, end + 1))
        coverage.append({
            "section": title, "lines": [start, end], "chinese_lines": len(region),
            "edited": len(region & groups[0]), "unchanged": len(region & groups[1]),
            "held": len(region & groups[2]),
        })
    report = {
        "source": SOURCE, "git_commit": COMMIT,
        "baseline_sha256": audit.digest(original), "after_sha256": audit.digest(actual),
        "status": "verified_with_holds", "physical_lines": len(old), **counts,
        "completed_chinese_lines": len(chinese - groups[2]),
        "reviewed_unchanged_line_count": len(UNCHANGED),
        "coverage_percent_including_holds": 100,
        "punctuation_residual_lines": residuals,
        "punctuation_excluded_held_lines": sorted(groups[2]),
        "strict_protection_mismatches": [],
        "english_heading_caption_prefixes_preserved": True,
        "all_non_chinese_lines_byte_identical": True,
        "indentation_line_endings_trailing_whitespace_preserved": True,
        "markdown_token_structure_preserved": True,
        "protected_item_positions_preserved": True,
        "exceptions_used": [],
        "coverage": coverage,
        "limitations": [
            "The held line is reviewed but not completed.",
            "No browser, network, external link, or current-fact verification.",
            "Only this chapter is compared with the original Git snapshot.",
            "Semantic review is manual; structural checks do not prove translation accuracy.",
        ],
    }
    if args.record:
        audit.dump(manifest_path, manifest)
    audit.dump(OUT / "verification.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
