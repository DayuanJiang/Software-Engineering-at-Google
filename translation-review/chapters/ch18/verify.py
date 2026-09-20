"""Chapter 18 manifest generation and strict, offline, chapter-only validation."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import sys

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
SOURCE = (
    "zh-cn/Chapter-18_Build_Systems_and_Build_Philosophy/"
    "Chapter-18_Build_Systems_and_Build_Philosophy.md"
)
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
RETAINED = [
    24, 38, 65, 139, 191, 239, 397, 411,
    421, 485, 503, 527, 537, 573, 643, 661,
]
HELD = {}
SOURCE_HOLDS = {
    "337": (
        "Existing English paragraph on incremental reuse has no Chinese translation. "
        "Chinese line 339 translates English line 328, not 337. Adding or relocating "
        "paragraphs is deferred under the line/paragraph-preservation constraint."
    ),
}
EXAMPLES = {
    320: ['":mylib "', '"//java/com/example/common "', '"@com_google_common_guava_guava//jar "'],
    581: ['"1.1.4"', '"1.+"'],
}
INLINE = re.compile(r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>]+")
LINK = re.compile(r"!?\[[^\]]*\]\([^)\n]*\)")
PSEUDO_LINK = re.compile(r"\[[^\]]*\]\uff08#[^)\uff09]*\uff09")
PUNCTUATION = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))
QUOTES = {"\u300c": "\u201c", "\u300d": "\u201d", "\u300e": "\u2018", "\u300f": "\u2019"}

sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit
import book_review


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prefix(line):
    if line.lstrip().startswith(("#", "Figure ", "*Figure", "Example ")):
        first = audit.HAN.search(line)
        if first:
            return line[:first.start()]
    return ""


def cjk(char):
    return bool(char) and (bool(audit.HAN.search(char)) or char in (
        "\u201c\u201d\u2018\u2019\u00b7\u2014\u2026"
        "\u300a\u300b\u3008\u3009\u3010\u3011\u3001"
        "\u3002\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09"
    ))


def normalize(line, number):
    protected = set(range(len(prefix(line))))
    for match in INLINE.finditer(line):
        protected.update(range(match.start(), match.end()))
    for literal in EXAMPLES.get(number, []):
        start = line.find(literal)
        require(start >= 0, f"Missing protected literal at {number}: {literal}")
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
            left = chars[i - 1] if i else ""
            right = chars[i + 1] if i + 1 < len(chars) else ""
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
    original = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"]
    )
    require(audit.digest(original) == baseline["files"][SOURCE]["sha256"], "Baseline SHA mismatch")
    return baseline, original, (ROOT / SOURCE).read_bytes()


def manifest_for(original, current):
    old, new = original.decode().splitlines(), current.decode().splitlines()
    require(len(old) == len(new), "Cannot record changed line count")
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
    require(manifest["reviewed_unchanged_lines"] == RETAINED, "Retained coverage changed")
    require(manifest["held_lines"] == HELD, "Held coverage changed")
    old_text, new_text = original.decode(), current.decode()
    old, new = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
    require(len(old) == len(new), "Line count changed")
    chinese = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    require(changed <= chinese, "Non-Chinese source line changed")
    require(changed == {int(i) for i in manifest["replacements"]}, "Replacement lines mismatch")
    require(not (changed & set(RETAINED)), "Changed/retained overlap")
    require(changed | set(RETAINED) == chinese, "Incomplete Chinese coverage")
    require(book_review.reconstruct(original, manifest["replacements"]) == current,
            "Manifest does not exactly reconstruct chapter")

    for i, (before, after) in enumerate(zip(old, new), 1):
        require(re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0],
                f"Indentation or blank line changed: {i}")
        require(re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0],
                f"Trailing whitespace or newline changed: {i}")
        require(prefix(before) == prefix(after), f"English heading/caption prefix changed: {i}")
        require(LINK.findall(before) == LINK.findall(after), f"Raw Markdown link changed: {i}")
        require(PSEUDO_LINK.findall(before) == PSEUDO_LINK.findall(after),
                f"Existing pseudo-link changed: {i}")
        for literal in EXAMPLES.get(i, []):
            require(before.count(literal) == after.count(literal), f"Build literal changed: {i}")
        if i in chinese:
            require(normalize(after, i) == after, f"Chinese punctuation residual: {i}")

    old_doc = audit.parse_document(SOURCE, old_text)
    new_doc = audit.parse_document(SOURCE, new_text)
    before, after = audit.protected(old_doc), audit.protected(new_doc)
    require(before == baseline["files"][SOURCE], "Original parser output differs from baseline")
    for key in before:
        if key != "sha256":
            require(before[key] == after[key], f"Protected field changed: {key}")
    for key in ("codes", "links", "html", "explicit_ids", "footnotes"):
        require(old_doc[key] == new_doc[key], f"Protected content/positions changed: {key}")
    require(shape(old_text) == shape(new_text), "Block or inline Markdown shape changed")
    code_lines = set()
    for token in audit.MD.parse(old_text):
        if token.type in {"fence", "code_block"}:
            code_lines.update(range(token.map[0] + 1, token.map[1] + 1))
    require(not code_lines & changed, "Code block changed")
    require(not code_lines & chinese, "Unrecorded Chinese code-block hold")
    shared = book_review.validate(SOURCE, original, current, manifest)
    return {
        "status": "protection_pass_with_source_gap",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(current),
        "physical_lines_read": len(old),
        "original_chinese_lines": len(chinese),
        "completed_existing_chinese_lines": len(chinese),
        "edited_chinese_lines": len(changed),
        "reviewed_unchanged_count": len(RETAINED),
        "reviewed_unchanged_lines": RETAINED,
        "held_lines": HELD,
        "source_holds": SOURCE_HOLDS,
        "non_chinese_lines_unchanged": len(old) - len(chinese),
        "protected_code_blocks": sum(c["kind"] in {"fence", "code_block"} for c in old_doc["codes"]),
        "protected_inline_code_items": sum(c["kind"] == "inline" for c in old_doc["codes"]),
        "html_items": len(old_doc["html"]),
        "punctuation_residuals": 0,
        "protection_exceptions": [],
        "shared_validator": shared,
        "checks": [
            "Baseline hash and protected fields match fixed original Git snapshot",
            "Exact replacement manifest with disjoint, complete Chinese coverage",
            "All non-Chinese lines and English heading/caption prefixes unchanged",
            "All audit protected fields except whole-file SHA unchanged",
            "Code, comments, links, HTML and footnotes unchanged including positions",
            "Raw Markdown links, pseudo-links and build-language literals unchanged",
            "Block and inline Markdown token shapes, source maps and markup unchanged",
            "Line count/order, blank lines, indentation, trailing whitespace and newlines unchanged",
            "Chinese punctuation normalization idempotent, with literal/code protection",
            "Unmodified shared book_review.validate passed for Chapter 18 only",
        ],
        "limitations": [
            "Existing English paragraph at line 337 remains untranslated",
            "Existing code/example, pseudo-link and emphasis defects remain in place",
            "English-only captions were not given new translation lines",
            "No online comparison, external-link reachability checks or code compilation",
        ],
    }


def self_test(baseline, original, current, manifest):
    def mutate_line(number, old, new):
        lines = current.decode().splitlines(keepends=True)
        require(old in lines[number - 1], f"Self-test fixture missing: {number}")
        lines[number - 1] = lines[number - 1].replace(old, new, 1)
        return "".join(lines).encode()

    cases = {
        "English source": mutate_line(12, "Google", "Changed"),
        "code comment": mutate_line(154, "global", "local"),
        "English heading prefix": mutate_line(101, "Rescue?", "Rescue!"),
        "link target": mutate_line(437, "D9doX", "CHANGED"),
        "link label": mutate_line(581, "\u8bed\u4e49", "\u6539\u52a8"),
        "pseudo-link": mutate_line(447, "#_bookmark1676", "#_bookmark0"),
        "build-language literal": mutate_line(320, '":mylib "', '":mylib"'),
        "indentation": mutate_line(37, "    ", "   "),
        "punctuation": mutate_line(14, "\uff1a", ":"),
        "HTML": mutate_line(14, "\u8c37\u6b4c", "<b>\u8c37\u6b4c</b>"),
        "line count": current + b"\n",
    }
    passed = []
    for label, variant in cases.items():
        try:
            test_manifest = manifest_for(original, variant)
            validate(baseline, original, variant, test_manifest)
        except ValueError:
            passed.append(label)
        else:
            raise ValueError(f"Self-test accepted prohibited mutation: {label}")
    for label, field, value in [
        ("manifest SHA", "baseline_sha256", "0" * 64),
        ("hold ledger", "held_lines", {"14": "unapproved hold"}),
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
            raise ValueError(f"Self-test accepted prohibited mutation: {label}")
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
        require(not (REVIEW / "edits.json").exists(), "Refusing to overwrite existing manifest")
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
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
