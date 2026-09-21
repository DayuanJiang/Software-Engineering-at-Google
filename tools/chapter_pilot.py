"""Apply reviewed Chinese line edits and verify the chapter against its original snapshot."""

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path
import re
import subprocess

import translation_audit as audit

PILOT = audit.DEFAULT_OUT / "chapter-01"
PUNCTUATION = {",": "，", ";": "；", ":": "：", "?": "？", "!": "！", "(": "（", ")": "）"}


def is_chinese(char: str) -> bool:
    return bool(audit.HAN.search(char)) or char in "“”‘’《》【】、。，！？；：（）"


def normalize_chinese_line(line: str) -> str:
    # This pilot edits plain prose only. Do not run this normalizer on arbitrary Markdown.
    tokens = audit.MD.parseInline(line)
    forbidden = {"code_inline", "link_open", "image", "html_inline"}
    if any(c.type in forbidden for t in tokens for c in t.children or []) or audit.URL.search(line):
        raise ValueError("Protected inline content requires a separately reviewed edit.")
    chars = list(line)
    chinese_start = audit.HAN.search(line)
    protected_prefix = chinese_start.start() if line.lstrip().startswith("#") and chinese_start else 0
    for i, char in enumerate(chars):
        if i < protected_prefix:
            continue
        left = chars[i - 1] if i else ""
        right = chars[i + 1] if i + 1 < len(chars) else ""
        if char in PUNCTUATION and (is_chinese(left) or is_chinese(right)):
            chars[i] = PUNCTUATION[char]
    return "".join(chars)


def materialize(manifest: dict, original: bytes) -> bytes:
    if audit.digest(original) != manifest["baseline_sha256"]:
        raise ValueError("Original chapter hash does not match the reviewed snapshot.")
    lines = original.decode("utf-8").splitlines(keepends=True)
    for key, replacement in manifest["replacements"].items():
        number = int(key)
        old = lines[number - 1]
        if not audit.HAN.search(old) or "\n" in replacement or "\r" in replacement:
            raise ValueError(f"Not a single Chinese line: {number}")
        if not audit.HAN.search(replacement):
            raise ValueError(f"Chinese translation removed: {number}")
        eol = "\r\n" if old.endswith("\r\n") else "\n" if old.endswith("\n") else ""
        lines[number - 1] = normalize_chinese_line(replacement) + eol
    return "".join(lines).encode("utf-8")


def load():
    manifest = json.loads((PILOT / "edits.json").read_text())
    baseline = json.loads((audit.DEFAULT_OUT / "baseline.json").read_text())
    source = manifest["source"]
    original = subprocess.check_output(
        ["git", "-C", str(audit.ROOT), "show", f"{baseline['git_commit']}:{source}"]
    )
    if audit.digest(original) != baseline["files"][source]["sha256"]:
        raise ValueError("Git snapshot differs from the preserved baseline.")
    return manifest, baseline, original, materialize(manifest, original)


def validate_protected(source: str, original: bytes, result: bytes, prose_code_lines: list[int]) -> dict:
    old = audit.parse_document(source, original.decode("utf-8"))
    new = audit.parse_document(source, result.decode("utf-8"))
    before, after = audit.protected(old), audit.protected(new)
    for key in before:
        if key in {"sha256", "code_hashes"}:
            continue
        if before[key] != after[key]:
            raise ValueError(f"Protected content changed: {key}")
    if len(old["codes"]) != len(new["codes"]):
        raise ValueError("Code block count changed.")
    exceptions = []
    for a, b in zip(old["codes"], new["codes"]):
        changed = any(a[k] != b[k] for k in ("kind", "info", "content"))
        if not changed:
            continue
        if a["line"] not in prose_code_lines:
            raise ValueError(f"Code changed at original line {a['line']}")
        if a["kind"] != "code_block" or b["kind"] != "code_block" or not audit.HAN.search(a["content"]):
            raise ValueError("Only explicitly identified indented Chinese prose can be exempted.")
        exceptions.append({
            "line": a["line"], "reason": "Indented Chinese quotation, not executable code.",
            "before_sha256": audit.digest(a["content"]), "after_sha256": audit.digest(b["content"]),
            "before": a["content"], "after": b["content"],
        })
    return {
        "english_lines": len(before["english_line_hashes"]),
        "english_segments": len(before["english_segment_hashes"]),
        "protected_code_items": len(old["codes"]) - len(exceptions),
        "links": len(before["links"]), "footnote_markers": len(before["footnotes"]),
        "structural_items": len(before["structures"]),
        "prose_code_exceptions": exceptions,
    }


def verify(check_other_sources: bool = True) -> dict:
    manifest, baseline, original, expected = load()
    actual = (audit.ROOT / manifest["source"]).read_bytes()
    if actual != expected:
        raise ValueError("Chapter differs from the reviewed edit manifest.")
    counts = validate_protected(manifest["source"], original, actual, manifest["prose_code_lines"])
    if check_other_sources:
        for file, snapshot in baseline["files"].items():
            if file != manifest["source"] and audit.digest((audit.ROOT / file).read_bytes()) != snapshot["sha256"]:
                raise ValueError(f"Unrelated source changed: {file}")
    for file, expected_hash in baseline["assets"].items():
        if audit.digest((audit.ROOT / file).read_bytes()) != expected_hash:
            raise ValueError(f"Image changed: {file}")
    lines = original.decode("utf-8").splitlines()
    chinese_lines = {i + 1 for i, line in enumerate(lines) if audit.HAN.search(line)}
    changed = {int(i) for i in manifest["replacements"]}
    covered = changed | set(manifest["reviewed_unchanged_lines"])
    if covered != chinese_lines:
        raise ValueError(f"Coverage mismatch: missing {chinese_lines - covered}, extra {covered - chinese_lines}")
    for number in chinese_lines - changed:
        if actual.decode("utf-8").splitlines()[number - 1] != lines[number - 1]:
            raise ValueError(f"Unreviewed change at line {number}")
    for number in changed:
        line = actual.decode("utf-8").splitlines()[number - 1]
        if normalize_chinese_line(line) != line:
            raise ValueError(f"Non-normalized punctuation at line {number}")
        if '"' in line:
            raise ValueError(f"Ambiguous ASCII double quote at line {number}")
    return {
        "source": manifest["source"], "baseline_sha256": audit.digest(original),
        "current_sha256": audit.digest(actual),
        "reviewed_chinese_lines": len(chinese_lines), "edited_chinese_lines": len(changed),
        "unchanged_reviewed_lines": sorted(chinese_lines - changed),
        "other_source_files_unchanged": len(baseline["files"]) - 1 if check_other_sources else None,
        "scope": "book_preparation" if check_other_sources else "chapter_only",
        "images_unchanged": len(baseline["assets"]),
        "punctuation_residuals": 0, **counts,
    }


def write_report(check_other_sources: bool = True):
    result = verify(check_other_sources)
    manifest, _, original, expected = load()
    before = original.decode("utf-8").splitlines()
    after = expected.decode("utf-8").splitlines()
    audit.dump(PILOT / "verification.json", result)
    diff = difflib.unified_diff(before, after, fromfile="before/" + manifest["source"],
                                tofile="after/" + manifest["source"], lineterm="")
    (PILOT / "changes.diff").write_text("\n".join(diff) + "\n")
    sections = [
        "# 第一章全部中文修改对照", "",
        "按基线行号生成；英文、代码及链接的保护结果见 `verification.json`。",
        "此文件为审阅产物，实际译文仍以原章节文件为准。", "",
    ]
    for number in sorted(int(n) for n in manifest["replacements"]):
        sections.extend([
            f"## 原第 {number} 行", "", "**修改前**", "",
            "> " + before[number - 1].lstrip("> ").strip(),
            "", "**修改后**", "",
            "> " + after[number - 1].lstrip("> ").strip(), "",
        ])
    (PILOT / "all-changes.md").write_text("\n".join(sections) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("apply", "verify", "report"))
    parser.add_argument("--chapter-only", action="store_true")
    args = parser.parse_args()
    if args.command == "apply":
        manifest, _, original, expected = load()
        target = audit.ROOT / manifest["source"]
        if target.read_bytes() not in {original, expected}:
            raise ValueError("Refusing to overwrite changes outside this reviewed manifest.")
        validate_protected(manifest["source"], original, expected, manifest["prose_code_lines"])
        target.write_bytes(expected)
        print("Applied reviewed Chinese edits; English and executable code preserved.")
    elif args.command == "verify":
        print(json.dumps(verify(check_other_sources=not args.chapter_only), ensure_ascii=False, indent=2))
    else:
        write_report(check_other_sources=not args.chapter_only)


if __name__ == "__main__":
    main()
