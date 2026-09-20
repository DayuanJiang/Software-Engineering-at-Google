"""Strict offline validation and artifact generation for Chapter 20 only."""

from __future__ import annotations

import argparse
import copy
import difflib
import json
from pathlib import Path
import re
import subprocess
import sys

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
SOURCE = "zh-cn/Chapter-20_Static_Analysis/Chapter-20_Static_Analysis.md"
COMMIT = "110720f031b43e18708fdc38af03269b65b3cc41"
RETAINED = [
    5, 21, 37, 43, 67, 85, 109, 136, 137, 138, 142,
    157, 161, 191, 205, 215, 243, 275, 281,
]
HELD = {}
PROTECTED_HOLDS = {
    "27,29": "The existing Gernamy spelling in the bibliography is retained.",
    "139,141,143": "Existing zero-width spaces before list continuation indentation are retained.",
    "155": "The existing inline-code URL has a space after https:// and remains unchanged.",
    "165,171": "Both original C++ fence labels are retained despite the Java-context example.",
}
INLINE = re.compile(r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>]+")
LINK = re.compile(r"!?\[[^\]]*\]\([^)\n]*\)")
PUNCTUATION = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))
QUOTES = {"\u300c": "\u201c", "\u300d": "\u201d", "\u300e": "\u2018", "\u300f": "\u2019"}
ENGLISH_LITERALS = {
    29: ["Gernamy: Springer, 2004"],
    155: [
        "\u201cLessons from Building Static Analysis Tools at Google\u201d,",
        "61 No. 4 (April 2018): 58\u201366,",
    ],
}

sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit
import book_review


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prefix(line):
    if line.lstrip().startswith(("#", "*Figure", "Figure ", "Example ")):
        first = audit.HAN.search(line)
        if first:
            return line[:first.start()]
    return ""


def cjk(char):
    return bool(char) and (
        bool(audit.HAN.search(char))
        or char in "\u201c\u201d\u2018\u2019\u00b7\u2014\u2026"
        "\u300a\u300b\u3008\u3009\u3010\u3011\u3001\u3002"
        "\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09"
    )


def normalize(line, number):
    protected = set(range(len(prefix(line))))
    for match in INLINE.finditer(line):
        protected.update(range(match.start(), match.end()))
    for literal in ENGLISH_LITERALS.get(number, []):
        start = line.find(literal)
        require(start >= 0, f"Missing English literal at line {number}: {literal}")
        protected.update(range(start, start + len(literal)))
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
            left, right = chars[i - 1] if i else "", chars[i + 1] if i + 1 < len(chars) else ""
            if cjk(left) or cjk(right):
                chars[i] = PUNCTUATION[char]
    return "".join(chars)


def shape(text):
    tokens = audit.MD.parse(text)
    blocks = [(t.type, t.tag, t.nesting, t.level, t.map, t.markup, t.info) for t in tokens]
    inlines = [
        (t.map, [(c.type, c.tag, c.nesting, c.markup, c.attrs)
                 for c in t.children if c.type != "text"])
        for t in tokens if t.type == "inline"
    ]
    return blocks, inlines


def inputs():
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Unexpected baseline commit")
    original = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"])
    require(audit.digest(original) == baseline["files"][SOURCE]["sha256"], "Baseline SHA mismatch")
    return baseline, original, (ROOT / SOURCE).read_bytes()


def manifest_for(original, current):
    old, new = original.decode().splitlines(), current.decode().splitlines()
    require(len(old) == len(new), "Line count changed")
    return {
        "source": SOURCE,
        "baseline_sha256": audit.digest(original),
        "replacements": {str(i): b for i, (a, b) in enumerate(zip(old, new), 1) if a != b},
        "reviewed_unchanged_lines": RETAINED,
        "held_lines": HELD,
    }


def validate(baseline, original, current, manifest):
    require(manifest["source"] == SOURCE, "Wrong manifest source")
    require(manifest["baseline_sha256"] == audit.digest(original), "Manifest SHA mismatch")
    require(manifest["reviewed_unchanged_lines"] == RETAINED, "Retained ledger changed")
    require(manifest["held_lines"] == HELD, "Hold ledger changed")
    old_text, new_text = original.decode(), current.decode()
    old, new = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
    require(len(old) == len(new) == 289, "Line count changed")
    chinese = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    require(len(chinese) == 83, "Unexpected baseline Chinese coverage")
    require(changed <= chinese, "Non-Chinese source line changed")
    require(changed == {int(i) for i in manifest["replacements"]}, "Replacement ledger mismatch")
    require(not changed & set(RETAINED), "Changed/retained overlap")
    require(changed | set(RETAINED) == chinese, "Incomplete Chinese review coverage")
    require(book_review.reconstruct(original, manifest["replacements"]) == current,
            "Manifest does not reconstruct chapter byte-for-byte")
    for i, (before, after) in enumerate(zip(old, new), 1):
        require(re.match(r"^[\s\u200b]*", before)[0] == re.match(r"^[\s\u200b]*", after)[0],
                f"Indentation or zero-width prefix changed: {i}")
        require(re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
                f"Trailing whitespace or newline changed: {i}")
        require(prefix(before) == prefix(after), f"English heading/caption prefix changed: {i}")
        require(LINK.findall(before) == LINK.findall(after), f"Raw Markdown link changed: {i}")
        for literal in ENGLISH_LITERALS.get(i, []):
            require(before.count(literal) == after.count(literal), f"English literal changed: {i}")
        if i in chinese:
            require(normalize(after, i) == after, f"Chinese punctuation residual: {i}")
    old_doc, new_doc = audit.parse_document(SOURCE, old_text), audit.parse_document(SOURCE, new_text)
    before, after = audit.protected(old_doc), audit.protected(new_doc)
    require(before == baseline["files"][SOURCE], "Parser output differs from baseline")
    for key in before:
        if key != "sha256":
            require(before[key] == after[key], f"Protected field changed: {key}")
    for key in ("codes", "links", "html", "explicit_ids", "footnotes"):
        require(old_doc[key] == new_doc[key], f"Protected content/positions changed: {key}")
    require(shape(old_text) == shape(new_text), "Markdown block/inline token shape changed")
    code_lines = set()
    for token in audit.MD.parse(old_text):
        if token.type in {"fence", "code_block"}:
            code_lines.update(range(token.map[0] + 1, token.map[1] + 1))
    require(not code_lines & changed, "Code block changed")
    require(not code_lines & chinese, "Unrecorded Chinese code-block hold")
    assets = [p for p in baseline["assets"] if p.startswith(str(Path(SOURCE).parent) + "/")]
    for asset in assets:
        require(audit.digest((ROOT / asset).read_bytes()) == baseline["assets"][asset],
                f"Chapter image changed: {asset}")
    return {
        "status": "protection_pass_with_existing_protected_issues",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(current),
        "physical_lines_read": len(old),
        "original_chinese_lines": len(chinese),
        "completed_chinese_lines": len(chinese),
        "edited_chinese_lines": len(changed),
        "reviewed_unchanged_lines": RETAINED,
        "reviewed_unchanged_count": len(RETAINED),
        "held_lines": HELD,
        "protected_holds": PROTECTED_HOLDS,
        "non_chinese_lines_unchanged": len(old) - len(chinese),
        "protected_field_counts": {k: len(v) for k, v in before.items() if isinstance(v, list)},
        "code_blocks": sum(c["kind"] in {"fence", "code_block"} for c in old_doc["codes"]),
        "inline_code_items": sum(c["kind"] == "inline" for c in old_doc["codes"]),
        "chapter_images_unchanged": len(assets),
        "punctuation_residuals": 0,
        "protection_exceptions": [],
        "shared_validator": book_review.validate(SOURCE, original, current, manifest),
        "checks": [
            "Fixed original Git snapshot matches baseline SHA and all parsed protection fields",
            "Disjoint, complete Chinese line coverage and exact manifest reconstruction",
            "All non-Chinese lines and English heading/caption prefixes preserved",
            "Code, links, HTML, footnotes and their source positions preserved",
            "Raw link labels/targets, source literals and chapter image hashes preserved",
            "Markdown block and inline token shapes, source maps and markup preserved",
            "Line order/count, blanks, indentation, zero-width prefixes and hard breaks preserved",
            "Chinese punctuation normalization is idempotent with source/code protection",
            "Unmodified shared book_review.validate passes for this chapter only",
        ],
        "limitations": [
            "Existing protected bibliography, URL, list and code-label defects remain unresolved",
            "No external-link checks, online source comparison, browser checks or code compilation",
            "Other chapters and shared reports were not validated or modified",
            "Mechanical checks establish preservation, not semantic translation correctness",
        ],
    }


def self_test(baseline, original, current, manifest):
    def mutate_line(number, old, new):
        lines = current.decode().splitlines(keepends=True)
        require(old in lines[number - 1], f"Missing self-test fixture: {number}")
        lines[number - 1] = lines[number - 1].replace(old, new, 1)
        return "".join(lines).encode()

    cases = {
        "English source": mutate_line(11, "Static analysis", "Changed analysis"),
        "English heading prefix": mutate_line(61, "Key Lessons", "Changed Lessons"),
        "English caption prefix": mutate_line(117, "gray", "black"),
        "executable code": mutate_line(166, "31", "32"),
        "fence language": mutate_line(171, "C++", "java"),
        "inline code": mutate_line(79, "`containsKey`", "`containsValue`"),
        "link target": mutate_line(163, "http://errorprone.info/", "https://example.invalid/"),
        "link label": mutate_line(163, "[Error Prone]", "[Changed]"),
        "footnote marker": mutate_line(19, "[^1]", "[^9]"),
        "bibliography literal": mutate_line(29, "Gernamy", "Germany"),
        "zero-width prefix": mutate_line(139, "\u200b", ""),
        "hard line break": mutate_line(140, "  \n", "\n"),
        "punctuation": mutate_line(13, "\uff0c", ","),
        "HTML insertion": mutate_line(13, "\u9759\u6001", "<b>\u9759\u6001</b>"),
        "line count": current + b"\n",
    }
    passed = []
    for label, variant in cases.items():
        try:
            validate(baseline, original, variant, manifest_for(original, variant))
        except ValueError:
            passed.append(label)
        else:
            raise ValueError(f"Self-test accepted forbidden mutation: {label}")
    for label, field, value in [
        ("manifest SHA", "baseline_sha256", "0" * 64),
        ("hold ledger", "held_lines", {"13": "unapproved hold"}),
        ("retained ledger", "reviewed_unchanged_lines", RETAINED[:-1]),
        ("replacement ledger", "replacements", {}),
    ]:
        variant = copy.deepcopy(manifest)
        variant[field] = value
        try:
            validate(baseline, original, current, variant)
        except ValueError:
            passed.append(label)
        else:
            raise ValueError(f"Self-test accepted forbidden mutation: {label}")
    return passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--normalize", action="store_true")
    mode.add_argument("--record", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    baseline, original, current = inputs()
    if args.normalize:
        old, new = original.decode().splitlines(keepends=True), current.decode().splitlines(keepends=True)
        require(len(old) == len(new), "Line count changed before normalization")
        normalized = [
            normalize(line, i) if audit.HAN.search(before) else line
            for i, (before, line) in enumerate(zip(old, new), 1)
        ]
        changes = sum(a != b for a, b in zip(new, normalized))
        if changes:
            (ROOT / SOURCE).write_bytes("".join(normalized).encode())
        print(json.dumps({"mechanically_normalized_lines": changes}))
        return
    if args.record:
        require(not (REVIEW / "edits.json").exists(), "Refusing to overwrite an existing manifest")
        manifest = manifest_for(original, current)
    else:
        manifest = json.loads((REVIEW / "edits.json").read_text())
    result = validate(baseline, original, current, manifest)
    if args.self_test:
        result["negative_tests_passed"] = self_test(baseline, original, current, manifest)
    if args.record:
        audit.dump(REVIEW / "edits.json", manifest)
    if args.write_report:
        audit.dump(REVIEW / "verification.json", result)
        (REVIEW / "changes.diff").write_text("".join(difflib.unified_diff(
            original.decode().splitlines(keepends=True),
            current.decode().splitlines(keepends=True),
            fromfile="before/" + SOURCE, tofile="after/" + SOURCE,
        )))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
