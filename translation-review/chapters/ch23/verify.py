"""Offline, chapter-only manifest generation and strict protection checks."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[2]
SOURCE = "zh-cn/Chapter-23_Continuous_Integration/Chapter-23_Continuous_Integration.md"
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
RETAINED = [5, 62, 68, 138, 212, 291, 297, 405, 445, 493, 549, 583, 731, 737]
HELD = {
    "30": "Chinese CI definition is parsed as an indented code block; preserve verbatim pending parent review.",
    "182": "Chinese CD definition is parsed as an indented code block; preserve wording, punctuation and markup pending parent review.",
    "413": "Chinese hermetic-test definition is parsed as an indented code block; preserve verbatim pending parent review.",
}
SOURCE_GAPS = {
    "673": "The English Future improvement paragraph has no Chinese counterpart; adding one would violate Chinese-line-only and line-structure constraints.",
}
SOURCE_ISSUES = {
    "188": "Footnote 7 is attached to selective Continuous Deployment, but its text at 208 concerns mid-air collisions. References are not relocated.",
    "437": "False positives labels a passing test that should probably not pass; False negatives at 440 labels a failing test that should probably not fail. Preserve local labels and phenomena, not the usual defect-detection interpretation.",
    "483": "Original complexity uses N2 without a superscript; retain O(N2), O(N), N and N-1 in Chinese rather than silently repair source notation.",
    "609": "Existing extra unmatched ** marker retained; prose edited without changing markup.",
    "675": "Scenario 4 is an H2 although scenarios 1-3 are H4; preserve the existing hierarchy.",
    "701": "Existing English stray closing punctuation and _bookmark references remain unchanged.",
    "footnotes": "Existing malformed [4^]-style definitions and unmatched [^n] references retained.",
    "english_only": "English-only CI Challenges heading, figure captions 23-1/2/3, credits and citation material receive no new Chinese lines.",
}
IDENTIFIERS = {
    16: ["HTTP", "RPC"],
    48: ["SUT"],
    56: ["TAP"],
    60: ["IT Revolution"],
    124: ["PII"],
    156: ["true head", "green head", "CB", "UI"],
    162: ["true head", "green head"],
    194: ["RC", "Docker", "Kubernetes", "Borg"],
    198: ["Head", "head", "master", "mainline", "trunk"],
    202: ["TAP", "RC", "Rapid", "O'Reilly"],
    295: ["cherry-pick", "RC", "CB"],
    304: ["probers"],
    325: ["SLO", "SUT"],
    337: ["SRE", "JPEG"],
    391: ["hotlists", "Google Web Server", "GWS"],
    429: ["fake"],
    433: ["DisplayAds"],
    485: ["N-1", "O(N2)", "O(N)", "hotswapping", "head"],
    497: ["TAP", "Google Takeout"],
    533: ["Build Cop"],
    571: ["Forge", "TAP"],
    575: ["Forge", "Blaze", "TAP"],
    593: ["Google Drive", "Gmail", "ZIP", "Google Takeout", "API"],
    597: ["Drive API"],
    601: ["ACL", "Drive", "Gmail"],
    621: ["green head", "RC"],
    645: ["Gmail", "ID", "Takeout"],
    683: ["YouTube"],
    695: ["ID"],
    699: ["API", "flaky"],
    711: ["DevOps", "MTTCU"],
    719: ["Drive folder downloads", "API"],
}
FIGURES = {
    60: ["2018"],
    347: ["100%"],
    359: ["100%", "99.9%", "99.999%"],
    433: ["400"],
    469: ["超过50", "1/14"],
    485: ["N-1", "O(N2)", "O(N)"],
    507: ["超过50,000", "超过40亿"],
    521: ["95%+"],
    537: ["约为11分钟"],
    543: ["每秒超过一项"],
    565: ["两次"],
    579: ["100", "1,000", "几十分钟"],
    587: ["2011"],
    593: ["至少10"],
    609: ["95%", "50%"],
    617: ["每两小时"],
    621: ["每两小时"],
    630: ["95%", "50%"],
    631: ["两小时", "1/12"],
    637: ["超过*90"],
    641: ["90"],
    653: ["35%"],
    659: ["90多"],
    719: ["490"],
}
INLINE = re.compile(r"`+[^`]*`+|!?\[[^\]]*\]\([^)]*\)|<[^>]+>|https?://[^\s<>]+")
LINK = re.compile(r"!?\[[^\]]*\]\([^)\n]*\)")
PUNCT = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))
QUOTES = {"\u300c": "\u201c", "\u300d": "\u201d", "\u300e": "\u2018", "\u300f": "\u2019"}

sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit
import book_review


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prefix(line, number):
    if line.lstrip().startswith(("#", "*Figure")) or number in {312, 503}:
        first = audit.HAN.search(line)
        if first:
            return line[:first.start()]
    return ""


def cjk(char):
    return bool(char) and (
        bool(audit.HAN.search(char))
        or char in "\u201c\u201d\u2018\u2019\u00b7\u2014\u2026\u300a\u300b"
        "\u3008\u3009\u3010\u3011\u3001\u3002\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09"
    )


def normalize(line, number):
    protected = set(range(len(prefix(line, number))))
    for match in INLINE.finditer(line):
        protected.update(range(match.start(), match.end()))
    for literal in IDENTIFIERS.get(number, []):
        for match in re.finditer(re.escape(literal), line):
            protected.update(range(match.start(), match.end()))
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
        elif char in PUNCT:
            if cjk(chars[i - 1] if i else "") or cjk(chars[i + 1] if i + 1 < len(chars) else ""):
                chars[i] = PUNCT[char]
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
    require(baseline["git_commit"] == COMMIT, "Wrong baseline commit")
    original = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"])
    require(audit.digest(original) == baseline["files"][SOURCE]["sha256"], "Baseline hash mismatch")
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
    require(manifest["source"] == SOURCE, "Manifest source mismatch")
    require(manifest["baseline_sha256"] == audit.digest(original), "Manifest hash mismatch")
    require(manifest["reviewed_unchanged_lines"] == RETAINED, "Retained ledger mismatch")
    require(manifest["held_lines"] == HELD, "Hold ledger mismatch")
    old_text, new_text = original.decode(), current.decode()
    old, new = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
    require(len(old) == len(new), "Line count changed")
    chinese = {i for i, line in enumerate(old, 1) if audit.HAN.search(line)}
    changed = {i for i, (a, b) in enumerate(zip(old, new), 1) if a != b}
    retained, held = set(RETAINED), {int(i) for i in HELD}
    require(changed <= chinese, "Non-Chinese line changed")
    require(changed == {int(i) for i in manifest["replacements"]}, "Replacement ledger mismatch")
    require(not (changed & retained or changed & held or retained & held), "Coverage overlap")
    require(changed | retained | held == chinese, "Chinese coverage incomplete")
    require(book_review.reconstruct(original, manifest["replacements"]) == current, "Reconstruction mismatch")

    for i, (before, after) in enumerate(zip(old, new), 1):
        require(re.match(r"^\s*", before)[0] == re.match(r"^\s*", after)[0], f"Leading whitespace: {i}")
        require(re.search(r"\s*$", before)[0] == re.search(r"\s*$", after)[0], f"Trailing whitespace: {i}")
        require(prefix(before, i) == prefix(after, i), f"English prefix: {i}")
        require(LINK.findall(before) == LINK.findall(after), f"Raw Markdown link: {i}")
        require(re.findall(r"\*+|_+", before) == re.findall(r"\*+|_+", after), f"Emphasis markup: {i}")
        if i in chinese - held:
            require(normalize(after, i) == after, f"Punctuation residual: {i}")
        for literal in IDENTIFIERS.get(i, []):
            require(literal in after, f"Identifier lost at {i}: {literal}")
        for literal in FIGURES.get(i, []):
            require(literal in after, f"Historical figure lost at {i}: {literal}")

    old_doc = audit.parse_document(SOURCE, old_text)
    new_doc = audit.parse_document(SOURCE, new_text)
    a, b = audit.protected(old_doc), audit.protected(new_doc)
    require(a == baseline["files"][SOURCE], "Parser baseline mismatch")
    for key in a:
        if key != "sha256":
            require(a[key] == b[key], f"Protected field: {key}")
    for key in ("codes", "links", "html", "explicit_ids", "footnotes"):
        require(old_doc[key] == new_doc[key], f"Protected content or location: {key}")
    require(shape(old_text) == shape(new_text), "Markdown block/inline shape changed")
    code_lines = set()
    for token in audit.MD.parse(old_text):
        if token.type in {"fence", "code_block"}:
            code_lines.update(range(token.map[0] + 1, token.map[1] + 1))
    require(not changed & code_lines, "Code block edited")
    require(code_lines & chinese == held, "Chinese code-block holds incomplete")
    assets = []
    for link in old_doc["links"]:
        if link["kind"] == "image":
            path = ((ROOT / SOURCE).parent / unquote(link["target"])).resolve()
            relative = str(path.relative_to(ROOT))
            sha = audit.digest(path.read_bytes())
            require(sha == baseline["assets"][relative], f"Chapter image changed: {relative}")
            assets.append({"path": relative, "sha256": sha})
    shared = book_review.validate(SOURCE, original, current, manifest)
    return {
        "status": "verified_with_holds",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(current),
        "physical_lines_read": len(old),
        "original_chinese_lines": len(chinese),
        "inspected_chinese_lines": len(chinese),
        "completed_chinese_lines": len(chinese - held),
        "edited_chinese_lines": len(changed),
        "reviewed_unchanged_count": len(retained),
        "reviewed_unchanged_lines": RETAINED,
        "held_line_count": len(held),
        "held_lines": HELD,
        "untranslated_source_paragraphs": SOURCE_GAPS,
        "source_issues": SOURCE_ISSUES,
        "non_chinese_lines_unchanged": len(old) - len(chinese),
        "punctuation_residuals_in_completed_chinese_lines": 0,
        "html_items": len(old_doc["html"]),
        "code_blocks": sum(c["kind"] in {"fence", "code_block"} for c in old_doc["codes"]),
        "inline_code_items": sum(c["kind"] == "inline" for c in old_doc["codes"]),
        "historical_figure_checks": FIGURES,
        "identifier_checks": IDENTIFIERS,
        "chapter_image_checks": assets,
        "protected_mismatches": [],
        "protection_exceptions": [],
        "shared_validator": shared,
        "checks": [
            "Fixed Git snapshot and stored baseline SHA-256 agree",
            "Replacements reconstruct the edited chapter byte for byte",
            "Changed, retained and held Chinese lines are disjoint and exhaustive",
            "All non-Chinese lines and mixed English prefixes are unchanged",
            "All audit protection fields except whole-file SHA-256 are unchanged",
            "Code, links, HTML and footnotes retain contents and source positions",
            "Markdown block/inline types, source maps and raw emphasis markers are unchanged",
            "Line count, blank lines, indentation, hard breaks and final newline are unchanged",
            "Punctuation normalization is idempotent on all completed Chinese lines",
            "Historical figures, named tools and restored API identifiers pass explicit checks",
            "All five referenced chapter images match baseline byte hashes",
            "Unmodified shared book_review.validate passes for this chapter only",
        ],
        "limitations": [
            "Three protected Chinese definitions remain pending, not completed",
            "English paragraph 673 remains untranslated; no new Chinese lines added",
            "Original source ambiguities and malformed markup remain as documented",
            "No external source check, external API/model calls or browser rendering",
        ],
    }


def self_test(baseline, original, current, manifest):
    def mutate(number, before, after):
        lines = current.decode().splitlines(keepends=True)
        require(before in lines[number - 1], f"Missing self-test fixture: {number}")
        lines[number - 1] = lines[number - 1].replace(before, after, 1)
        return "".join(lines).encode()

    cases = {
        "English source": mutate(10, "Continuous Integration", "Continuous Delivery"),
        "English heading prefix": mutate(148, "Build", "Test"),
        "Chinese protected code": mutate(30, "\u6301\u7eed", "\u4e0d\u65ad"),
        "English protected code": mutate(26, "ecosystem", "system"),
        "link target": mutate(194, "89yPv", "changed"),
        "link label": mutate(194, "[Borg]", "[Changed]"),
        "footnote marker": mutate(22, "[^1]", "[^99]"),
        "hard line break": mutate(288, "  \n", "\n"),
        "list indentation": mutate(289, "    ", "   "),
        "line count": current + b"\n",
        "HTML insertion": mutate(124, "CI", "<b>CI</b>"),
        "historical figure": mutate(507, "50,000", "60,000"),
        "tool identifier": mutate(575, "Blaze", "Changed"),
        "API identifier": mutate(719, "Drive folder downloads", "Changed"),
        "punctuation": mutate(72, "\uff0c", ","),
        "existing malformed markup": mutate(609, "\u3002**", "\u3002"),
    }
    passed = []
    for label, variant in cases.items():
        try:
            validate(baseline, original, variant, manifest_for(original, variant))
        except ValueError:
            passed.append(label)
        else:
            raise ValueError(f"Accepted prohibited mutation: {label}")
    for label, field, value in [
        ("manifest hash", "baseline_sha256", "0" * 64),
        ("manifest replacements", "replacements", {}),
        ("manifest holds", "held_lines", {}),
        ("manifest retained coverage", "reviewed_unchanged_lines", RETAINED[:-1]),
    ]:
        variant = copy.deepcopy(manifest)
        variant[field] = value
        try:
            validate(baseline, original, current, variant)
        except ValueError:
            passed.append(label)
        else:
            raise ValueError(f"Accepted corrupt ledger: {label}")
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
            normalize(after, i) if before != after and audit.HAN.search(before) and str(i) not in HELD else after
            for i, (before, after) in enumerate(zip(old, new), 1)
        ]
        count = sum(a != b for a, b in zip(new, normalized))
        if count:
            (ROOT / SOURCE).write_bytes("".join(normalized).encode())
        print(json.dumps({"mechanically_normalized_lines": count}))
        return
    if args.record:
        require(not (REVIEW / "edits.json").exists(), "Refusing to overwrite manifest")
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
