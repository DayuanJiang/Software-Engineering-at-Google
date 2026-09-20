"""Validate only Chapter 25; optionally generate its mechanical review artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCE = "zh-cn/Chapter-25_Compute_as_a_Service/Chapter-25_Compute_as_a_Service.md"
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
sys.path.insert(0, str(ROOT / "tools"))

import book_review
import translation_audit as audit


RETAINED = [
    7, 61, 89, 107, 129, 173, 183, 184, 185, 289,
    323, 345, 371, 509, 613, 635, 661, 679, 717, 731,
]
HOLDS = {
    "449": (
        "English line 447 says 'without significant latency decreases', which "
        "conflicts with the surrounding capacity/latency argument. The full "
        "Chinese paragraph is retained verbatim pending parent/source review; "
        "it is not counted as completed polishing."
    )
}

# These checks supplement, rather than replace, the full contextual numeric review.
RESOURCE_AND_HISTORY = {
    31: ["523", "15年"],
    50: ["2002", "Jeff Dean"],
    133: ["一个 CPU", "200 MB"],
    145: ["2003", "2007", "cgroups", "Linux"],
    149: ["2011", "32,000"],
    163: ["2006"],
    189: ["过去10年", "GPU", "TPU"],
    193: ["十年前", "几周"],
    205: ["100万", "一秒钟", "12天", "200台", "100分钟"],
    213: ["100个"],
    225: ["200台", "50分钟", "100万", "1,000块", "1,000份"],
    271: ["100台", "1%"],
    301: ["3到5份"],
    313: ["100%"],
    353: ["过去一天", "1 GB"],
    357: ["过去一年", "1 TB", "几百个核心"],
    361: ["一千核心小时", "工作一天"],
    369: ["一千台", "8,000", "一整台机器"],
    409: ["20,000", "PickUnu sedPortOrDie"],
    423: ["2011", "32位", "64位", "PID_MAX-1", "32,000"],
    427: ["0...32,000", "两阶段", "第三阶段", "八年后"],
    441: ["2003"],
    453: ["30%", "70%", "CPU", "RAM"],
    472: ["50%"],
    503: ["下线", "5%"],
    553: ["2012"],
    573: ["2011年左右"],
    581: ["2012年后"],
    621: ["至少", "三个副本"],
    647: ["不能缩减到零", "缩容到零"],
    651: ["100,000个核心", "100,000个物理核心"],
    699: ["Zimki", "2007", "三个月"],
}
LITERALS = {
    79: ["while true; do run && break; done"],
    137: ["/tmp"],
    393: ["*/bin/foo/bar*"],
    427: ["{hostname, timestamp, pid}"],
    521: ["`while true; do ./ my_binary; done`", "/usr/bin/bash -c $USER_COMMAND"],
    525: ["`/usr/bin/ash -c $USER_COMMAND`"],
}
PUNCTUATION = {",": "，", ";": "；", ":": "：", "?": "？", "!": "！", "(": "（", ")": "）"}
CJK_EXTRA = set("“”‘’·—…《》〈〉「」『』【】、。，！？；：（）")


def check(condition, message):
    if not condition:
        raise ValueError(message)


def is_cjk(char):
    return bool(char) and (
        "\u3400" <= char <= "\u9fff"
        or "\u3000" <= char <= "\u303f"
        or "\uff00" <= char <= "\uffef"
        or char in CJK_EXTRA
    )


def normalize_punctuation(number, line):
    """Apply the skill's CJK-adjacent rules with code/source spans protected."""
    spans = []
    if line.startswith("#"):
        spans.append((0, audit.HAN.search(line).start()))
    for match in re.finditer(r"`[^`]*`|!?\[[^\]]*\]\([^)]*\)|<[^>]*>", line):
        spans.append(match.span())
    for literal in LITERALS.get(number, []):
        start = line.find(literal)
        if start >= 0:
            spans.append((start, start + len(literal)))
    if number == 283:
        # This prefix is an existing all-English bibliographic citation.
        spans.append((0, line.index("ACM SIGPLAN") + len("ACM SIGPLAN")))
    protected = {i for start, end in spans for i in range(start, end)}
    result = list(line)
    opened = False
    for index, char in enumerate(line):
        if index in protected:
            continue
        if char in PUNCTUATION and (
            is_cjk(line[index - 1] if index else "")
            or is_cjk(line[index + 1] if index + 1 < len(line) else "")
        ):
            result[index] = PUNCTUATION[char]
        elif char == '"':
            result[index] = "”" if opened else "“"
            opened = not opened
        elif char in "「『":
            result[index] = {"「": "“", "『": "‘"}[char]
        elif char in "」』":
            result[index] = {"」": "”", "』": "’"}[char]
    return "".join(result)


def layout(source):
    tokens = audit.MD.parse(source)
    rows = []
    for token in tokens:
        rows.append((token.type, token.tag, token.nesting, token.map, token.markup))
        for child in token.children or []:
            rows.append((child.type, child.tag, child.nesting, child.markup))
    return rows


def validate(before, after, manifest):
    old = before.decode("utf-8")
    new = after.decode("utf-8")
    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    check(len(old_lines) == len(new_lines) == 741, "Physical line count changed")
    check(manifest["source"] == SOURCE, "Wrong manifest source")
    check(manifest["baseline_sha256"] == audit.digest(before), "Wrong manifest baseline hash")
    check(manifest["reviewed_unchanged_lines"] == RETAINED, "Retained review list changed")
    check(manifest["held_lines"] == HOLDS, "Hold list changed")
    changed = {int(number) for number in manifest["replacements"]}
    chinese = {i for i, line in enumerate(old_lines, 1) if audit.HAN.search(line)}
    check(not (set(RETAINED) & {int(i) for i in HOLDS}), "Overlapping retained/held lines")
    check(changed | set(RETAINED) | {int(i) for i in HOLDS} == chinese, "Incomplete coverage")
    for number, (first, second) in enumerate(zip(old_lines, new_lines), 1):
        check(bool(first.strip()) == bool(second.strip()), f"Blank line moved at {number}")
        check(re.match(r"^\s*", first)[0] == re.match(r"^\s*", second)[0],
              f"Indentation changed at {number}")
        check(re.search(r"\s*$", first)[0] == re.search(r"\s*$", second)[0],
              f"Line ending or hard break changed at {number}")
        if number not in chinese:
            check(first == second, f"Non-Chinese source changed at {number}")
        if first.startswith("#") and number in chinese:
            check(first[:audit.HAN.search(first).start()] == second[:audit.HAN.search(second).start()],
                  f"English heading prefix changed at {number}")
        if number in set(RETAINED) | {int(i) for i in HOLDS}:
            check(first == second, f"Retained/held content changed at {number}")
        if number in changed:
            check(first != second, f"No-op replacement at {number}")
            check(normalize_punctuation(number, second) == second,
                  f"Non-normalized Chinese punctuation at {number}")
    a = audit.protected(audit.parse_document(SOURCE, old))
    b = audit.protected(audit.parse_document(SOURCE, new))
    for key in a:
        if key != "sha256":
            check(a[key] == b[key], f"Protected {key} changed")
    check(layout(old) == layout(new), "Markdown token layout changed")
    for requirements in (LITERALS, RESOURCE_AND_HISTORY):
        for number, literals in requirements.items():
            for literal in literals:
                check(literal in new_lines[number - 1],
                      f"Missing resource/history/literal at {number}: {literal}")
    # The standard validator also enforces manifest reconstruction and coverage.
    counts = book_review.validate(SOURCE, before, after, manifest)
    return {
        "status": "verified_with_holds",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(before),
        "after_sha256": audit.digest(after),
        "physical_lines": len(old_lines),
        "coverage": {
            "chinese_lines_inspected": len(chinese),
            "edited_lines": len(changed),
            "reviewed_unchanged_lines": len(RETAINED),
            "held_lines": len(HOLDS),
            "completed_lines": len(changed) + len(RETAINED),
            "unaccounted_lines": 0,
        },
        "protection": {
            "english_line_hashes": counts["english_lines"],
            "english_segment_hashes": counts["english_segments"],
            "code_items": counts["code_items"],
            "links": counts["links"],
            "html_items": len(a["html_hashes"]),
            "footnote_markers": counts["footnote_markers"],
            "structural_items": counts["structural_items"],
            "markdown_token_layout": "unchanged",
            "english_heading_prefixes": "byte-identical",
            "indentation_line_endings_hard_breaks": "byte-identical",
            "non_chinese_lines": "byte-identical",
            "manifest_reconstruction": "byte-identical",
            "prose_code_exceptions": [],
        },
        "punctuation": {
            "changed_lines_normalized_and_checked": len(changed),
            "normalization_residuals": 0,
            "retained_english_citation_line": 283,
            "held_lines_excluded": [449],
        },
        "resource_and_history_assertions": sum(map(len, RESOURCE_AND_HISTORY.values())),
        "held_lines": HOLDS,
        "scope": "Chapter 25 only; no all-repository assertions",
    }


def self_test(before, after, manifest):
    def change_line(number, transform):
        lines = after.decode().splitlines(keepends=True)
        lines[number - 1] = transform(lines[number - 1])
        return "".join(lines).encode()

    mutations = {
        "english": change_line(17, lambda line: line.replace("hardware", "software", 1)),
        "inline_code": change_line(525, lambda line: line.replace("/usr/bin/ash", "/usr/bin/bash")),
        "link_target": change_line(665, lambda line: line.replace("/bigquery", "/changed")),
        "heading_prefix": change_line(39, lambda line: line.replace("Taming", "Changing")),
        "hard_break": change_line(50, lambda line: line.rstrip() + "\n"),
        "paragraph_structure": change_line(19, lambda line: "- " + line),
        "resource_unit": change_line(133, lambda line: line.replace("200 MB", "200 GB")),
        "historical_claim": change_line(699, lambda line: line.replace("2007", "2026")),
        "held_content": change_line(449, lambda line: line.replace("延迟下降", "延迟上升")),
    }
    for name, mutated in mutations.items():
        try:
            validate(before, mutated, manifest)
        except ValueError:
            continue
        raise ValueError(f"Negative self-test accepted mutation: {name}")
    invalid = json.loads(json.dumps(manifest))
    invalid["reviewed_unchanged_lines"] = RETAINED[:-1]
    try:
        validate(before, after, invalid)
    except ValueError:
        return list(mutations) + ["missing_coverage"]
    raise ValueError("Negative self-test accepted missing coverage")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-artifacts", action="store_true")
    args = parser.parse_args()
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    check(baseline["git_commit"] == COMMIT, "Unexpected original Git snapshot")
    before = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"])
    check(audit.digest(before) == baseline["files"][SOURCE]["sha256"], "Baseline SHA mismatch")
    after = (ROOT / SOURCE).read_bytes()
    if args.write_artifacts:
        old_lines, new_lines = before.decode().splitlines(), after.decode().splitlines()
        check(len(old_lines) == len(new_lines), "Cannot generate manifest after a line-count change")
        manifest = {
            "source": SOURCE,
            "baseline_sha256": audit.digest(before),
            "replacements": {
                str(i): new for i, (old, new) in enumerate(zip(old_lines, new_lines), 1) if old != new
            },
            "reviewed_unchanged_lines": RETAINED,
            "held_lines": HOLDS,
        }
    else:
        manifest = json.loads((OUT / "edits.json").read_text())
    report = validate(before, after, manifest)
    report["negative_self_tests_passed"] = self_test(before, after, manifest)
    if args.write_artifacts:
        audit.dump(OUT / "edits.json", manifest)
        audit.dump(OUT / "verification.json", report)
    else:
        check(json.loads((OUT / "verification.json").read_text()) == report,
              "Recorded verification report is stale")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
