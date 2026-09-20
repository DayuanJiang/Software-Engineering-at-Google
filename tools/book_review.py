"""Offline chapter-manifest validation and book progress; no inference/API calls."""

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path
import re
import subprocess

import chapter_pilot
import translation_audit as audit

DIRECTORY = audit.DEFAULT_OUT / "chapters"
NAV_LINK = re.compile(r"\[([^\]\n]+)\]\(((?:\./)?zh-cn/[^)\n]+)\)")


def without_nav_labels(text):
    return NAV_LINK.sub(lambda m: "[CHAPTER_LABEL](" + m[2] + ")", text)


def identifier(file):
    match = re.search(r"Chapter-(\d+)_", file)
    return f"ch{int(match[1]):02d}" if match else Path(file).stem.lower()


def original(file, baseline):
    raw = subprocess.check_output(
        ["git", "-C", str(audit.ROOT), "show", f"{baseline['git_commit']}:{file}"]
    )
    if audit.digest(raw) != baseline["files"][file]["sha256"]:
        raise ValueError(f"Original snapshot mismatch: {file}")
    return raw


def reconstruct(raw, replacements):
    lines = raw.decode("utf-8").splitlines(keepends=True)
    for number, text in replacements.items():
        number = int(number)
        if not 1 <= number <= len(lines):
            raise ValueError(f"Invalid line: {number}")
        old = lines[number - 1]
        if (not audit.HAN.search(old) or not isinstance(text, str) or not audit.HAN.search(text)
                or "\n" in text or "\r" in text):
            raise ValueError(f"Not a Chinese single-line edit: {number}")
        ending = "\r\n" if old.endswith("\r\n") else "\n" if old.endswith("\n") else ""
        lines[number - 1] = text + ending
    return "".join(lines).encode("utf-8")


def validate(file, before, after, manifest):
    old = audit.parse_document(file, before.decode("utf-8"))
    new = audit.parse_document(file, after.decode("utf-8"))
    a, b = audit.protected(old), audit.protected(new)
    exceptions_path = audit.DEFAULT_OUT / "prose-code-exceptions.json"
    exceptions = json.loads(exceptions_path.read_text()).get(file, []) if exceptions_path.exists() else []
    link_path = audit.DEFAULT_OUT / "link-syntax-exceptions.json"
    link_exceptions = json.loads(link_path.read_text()).get(file, []) if link_path.exists() else []
    for key in a:
        if key == "links" and a[key] != b[key] and link_exceptions:
            if len(a[key]) != len(b[key]):
                raise ValueError(f"{file}: link count changed")
            for index, (first, second) in enumerate(zip(a[key], b[key])):
                if first == second:
                    continue
                expected = next((e for e in link_exceptions if e["link_index"] == index), None)
                if not expected or first != expected["before"] or second != expected["after"]:
                    raise ValueError(f"{file}: unapproved link change")
            continue
        if key == "code_hashes" and a[key] != b[key] and exceptions:
            if len(old["codes"]) != len(new["codes"]):
                raise ValueError(f"{file}: code item count changed")
            for index, (first, second) in enumerate(zip(old["codes"], new["codes"])):
                fields = ("kind", "info", "content")
                if all(first[k] == second[k] for k in fields):
                    continue
                expected = next((e for e in exceptions if e["code_index"] == index), None)
                if (not expected or first["kind"] != "code_block" or second["kind"] != "code_block"
                        or first["content"] != expected["before"] or second["content"] != expected["after"]):
                    raise ValueError(f"{file}: unapproved code item change {index}")
            continue
        if key != "sha256" and a[key] != b[key]:
            raise ValueError(f"{file}: protected {key} changed")
    if len(before.decode().splitlines()) != len(after.decode().splitlines()):
        raise ValueError(f"{file}: line count changed")
    chinese = {i + 1 for i, text in enumerate(before.decode().splitlines()) if audit.HAN.search(text)}
    changed = {int(i) for i in manifest["replacements"]}
    unchanged = set(manifest.get("reviewed_unchanged_lines", []))
    holds = manifest.get("held_lines", {})
    held = {int(i) for i in holds} if isinstance(holds, dict) else {
        int(i["line"] if isinstance(i, dict) else i) for i in holds
    }
    if changed & unchanged or changed & held or (changed | unchanged | held) != chinese:
        raise ValueError(f"{file}: incomplete/overlapping review coverage; missing {sorted(chinese - changed - unchanged - held)}")
    if reconstruct(before, manifest["replacements"]) != after:
        raise ValueError(f"{file}: file does not match the edit manifest")
    return {
        "reviewed_chinese_lines": len(chinese), "changed_lines": len(changed),
        "english_lines": len(a["english_line_hashes"]), "english_segments": len(a["english_segment_hashes"]),
        "code_items": len(a["code_hashes"]), "links": len(a["links"]),
        "footnote_markers": len(a["footnotes"]), "structural_items": len(a["structures"]),
        "holds": holds, "held_line_count": len(held), "prose_code_exceptions": exceptions,
        "link_syntax_exceptions": link_exceptions,
    }


def verify_chapter(path, baseline):
    file = str(path.relative_to(audit.ROOT))
    name = identifier(file)
    if name == "ch01":
        manifest, _, before, expected = chapter_pilot.load()
        actual = path.read_bytes()
        if actual != expected:
            raise ValueError("Approved Chapter 1 differs from its manifest")
        counts = chapter_pilot.validate_protected(file, before, actual, manifest["prose_code_lines"])
        return {"id": name, "file": file, "status": "verified",
                "changed_lines": len(manifest["replacements"]),
                "reviewed_chinese_lines": len(manifest["replacements"]) + len(manifest["reviewed_unchanged_lines"]),
                "held_line_count": 0, "holds": [], **counts}
    manifest_path = DIRECTORY / name / "edits.json"
    before = original(file, baseline)
    after = path.read_bytes()
    if not manifest_path.exists():
        return {"id": name, "file": file, "status": "editing" if before != after else "pending"}
    manifest = json.loads(manifest_path.read_text())
    if manifest["source"] != file or manifest["baseline_sha256"] != audit.digest(before):
        raise ValueError(f"{name}: manifest source/hash mismatch")
    counts = validate(file, before, after, manifest)
    result = {"id": name, "file": file, "status": "verified_with_holds" if counts["held_line_count"] else "verified",
              "after_sha256": audit.digest(after), **counts}
    audit.dump(DIRECTORY / name / "verification.json", result)
    return result


def verify_all(final=False):
    baseline = json.loads((audit.DEFAULT_OUT / "baseline.json").read_text())
    rows = []
    for path in audit.book_files(audit.ROOT):
        try:
            rows.append(verify_chapter(path, baseline))
        except (ValueError, KeyError, json.JSONDecodeError) as error:
            rows.append({"id": identifier(str(path)), "file": str(path.relative_to(audit.ROOT)),
                         "status": "needs_validation", "error": str(error)})
    asset_errors = []
    for file, expected in baseline["assets"].items():
        if audit.digest((audit.ROOT / file).read_bytes()) != expected:
            asset_errors.append(file)
    nav_record = audit.DEFAULT_OUT / "navigation-edits.json"
    navigation = json.loads(nav_record.read_text()) if nav_record.exists() else {}
    site_errors = []
    for file in ("README.md", "_sidebar.md", "_coverpage.md", "index.html"):
        expected = navigation[file]["after_sha256"] if file in navigation else baseline["files"][file]["sha256"]
        if audit.digest((audit.ROOT / file).read_bytes()) != expected:
            site_errors.append(file)
        if file in navigation:
            if file not in {"README.md", "_sidebar.md"}:
                site_errors.append(file + ": not an allowed navigation file")
            elif without_nav_labels(original(file, baseline).decode()) != without_nav_labels((audit.ROOT / file).read_text()):
                site_errors.append(file + ": edits outside chapter labels")
    result = {
        "verified_documents": sum(r["status"] in {"verified", "verified_with_holds"} for r in rows),
        "held_chinese_lines": sum(r.get("held_line_count", 0) for r in rows),
        "reviewed_chinese_lines": sum(r.get("reviewed_chinese_lines", 0) for r in rows),
        "total_documents": len(rows), "changed_chinese_lines": sum(r.get("changed_lines", 0) for r in rows),
        "asset_errors": asset_errors, "site_errors": site_errors, "documents": rows,
        "workflow": "chapter-scoped Codex subagents and parent editing; offline verification",
    }
    audit.dump(audit.DEFAULT_OUT / "book-verification.json", result)
    lines = ["# 全书润色进度", "", "状态根据实际文件、逐行清单和保护校验生成。第一章使用已批准样稿。",
             "不调用独立模型 API。原文疑点或未改动的保护内容见各章 notes.md。", "",
             "| 文档 | 状态 | 修改中文行 |", "| --- | --- | ---: |"]
    for row in rows:
        lines.append(f"| {row['id']} | {row['status']} | {row.get('changed_lines', 0)} |")
    (audit.DEFAULT_OUT / "book-progress.md").write_text("\n".join(lines) + "\n")
    if final and (result["verified_documents"] != len(rows) or result["held_chinese_lines"] or asset_errors or site_errors):
        raise ValueError("Book not fully validated. See translation-review/book-verification.json")
    return result


def apply_manifest(name):
    baseline = json.loads((audit.DEFAULT_OUT / "baseline.json").read_text())
    manifest = json.loads((DIRECTORY / name / "edits.json").read_text())
    file = manifest["source"]
    before = original(file, baseline)
    after = reconstruct(before, manifest["replacements"])
    validate(file, before, after, manifest)
    target = audit.ROOT / file
    if target.read_bytes() not in {before, after}:
        raise ValueError("Refusing to overwrite changes not represented by this manifest.")
    target.write_bytes(after)


def record(name):
    baseline = json.loads((audit.DEFAULT_OUT / "baseline.json").read_text())
    path = next(p for p in audit.book_files(audit.ROOT) if identifier(str(p)) == name)
    file = str(path.relative_to(audit.ROOT))
    before, after = original(file, baseline), path.read_bytes()
    old_lines, new_lines = before.decode().splitlines(), after.decode().splitlines()
    if len(old_lines) != len(new_lines):
        raise ValueError("Line count changed.")
    replacements = {str(i + 1): b for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b}
    kept = [i + 1 for i, (a, b) in enumerate(zip(old_lines, new_lines)) if audit.HAN.search(a) and a == b]
    manifest = {"source": file, "baseline_sha256": audit.digest(before),
                "replacements": replacements, "reviewed_unchanged_lines": kept, "held_lines": []}
    validate(file, before, after, manifest)
    destination = DIRECTORY / name / "edits.json"
    if destination.exists():
        raise ValueError("Refusing to overwrite an existing review manifest.")
    audit.dump(destination, manifest)


def reports():
    baseline = json.loads((audit.DEFAULT_OUT / "baseline.json").read_text())
    for path in audit.book_files(audit.ROOT):
        name = identifier(str(path))
        manifest_path = DIRECTORY / name / "edits.json"
        if not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text())
        before = original(manifest["source"], baseline).decode().splitlines()
        after = path.read_text().splitlines()
        lines = ["# 中文修改对照", "", f"文件：`{manifest['source']}`", ""]
        for key in sorted(manifest["replacements"], key=int):
            i = int(key)
            lines.extend([f"## 原第{i}行", "", "**修改前**", "",
                          "> " + before[i - 1].lstrip("> "), "", "**修改后**", "",
                          "> " + after[i - 1].lstrip("> "), ""])
        (DIRECTORY / name / "all-changes.md").write_text("\n".join(lines) + "\n")
        (DIRECTORY / name / "changes.diff").write_text("\n".join(difflib.unified_diff(
            before, after, fromfile="before/" + manifest["source"], tofile="after/" + manifest["source"], lineterm=""
        )) + "\n")


def integrate_parent():
    decisions = json.loads((audit.DEFAULT_OUT / "parent-decisions.json").read_text())
    baseline = json.loads((audit.DEFAULT_OUT / "baseline.json").read_text())
    registry_path = audit.DEFAULT_OUT / "prose-code-exceptions.json"
    registry = json.loads(registry_path.read_text()) if registry_path.exists() else {}
    link_path = audit.DEFAULT_OUT / "link-syntax-exceptions.json"
    link_registry = json.loads(link_path.read_text()) if link_path.exists() else {}
    for name, decision in decisions.items():
        directory = DIRECTORY / name
        path = directory / "edits.json"
        manifest = json.loads(path.read_text())
        file = manifest["source"]
        raw = original(file, baseline)
        prior = reconstruct(raw, manifest["replacements"])
        if (audit.ROOT / file).read_bytes() != prior:
            raise ValueError(f"{name}: changes outside reviewed manifest")
        if not (directory / "subagent-edits.json").exists():
            audit.dump(directory / "subagent-edits.json", manifest)
        additions = {str(k): v for k, v in decision["replacements"].items()}
        manifest["replacements"].update(additions)
        changed = {int(k) for k in manifest["replacements"]}
        retained = set(manifest["reviewed_unchanged_lines"]) | set(decision["retained"])
        manifest["reviewed_unchanged_lines"] = sorted(retained - changed)
        held = manifest.get("held_lines", {})
        if not isinstance(held, dict):
            held = {str(h["line"]): h["reason"] for h in held}
        handled = {int(k) for k in additions} | set(decision["retained"])
        manifest["held_lines"] = {k: v for k, v in held.items() if int(k) not in handled}
        manifest["parent_review_notes"] = decision["notes"]
        candidate = reconstruct(raw, manifest["replacements"])
        old = audit.parse_document(file, raw.decode())
        new = audit.parse_document(file, candidate.decode())
        exceptions = []
        for index, (before, after) in enumerate(zip(old["codes"], new["codes"])):
            if before["content"] == after["content"]:
                continue
            permitted = [line for line in decision["prose_code_lines"]
                         if before["line"] <= line < before["line"] + len(before["content"].splitlines())]
            if not permitted or before["kind"] != "code_block" or after["kind"] != "code_block":
                raise ValueError(f"{name}: unexpected code difference")
            exceptions.append({"code_index": index, "lines": permitted,
                               "before": before["content"], "after": after["content"],
                               "reason": "Parent reviewed natural-language quotation, not executable code."})
        registry[file] = exceptions
        audit.dump(registry_path, registry)
        if decision.get("link_syntax_fix"):
            expected_url = decision["link_syntax_fix"]["url"]
            old_links, new_links = audit.protected(old)["links"], audit.protected(new)["links"]
            if len(old_links) != len(new_links):
                raise ValueError(f"{name}: unexpected link-count difference")
            fixes = []
            for index, (a, b) in enumerate(zip(old_links, new_links)):
                if a == b:
                    continue
                if not a["target"].startswith(expected_url) or b != {"kind": "link", "target": expected_url}:
                    raise ValueError(f"{name}: unexpected link repair")
                fixes.append({"link_index": index, "before": a, "after": b,
                              "reason": "Repair full-width Markdown brackets; intended visible URL unchanged."})
            if len(fixes) != 1:
                raise ValueError(f"{name}: expected exactly one syntax repair")
            link_registry[file] = fixes
            audit.dump(link_path, link_registry)
        validate(file, raw, candidate, manifest)
        (audit.ROOT / file).write_bytes(candidate)
        audit.dump(path, manifest)
        (directory / "parent-review.md").write_text(
            "# 父任务复核\n\n" + "\n\n".join(decision["notes"]) +
            "\n\n原子代理清单保存在 `subagent-edits.json`。当前结果以全书校验器 `tools/book_review.py` 为准。\n"
        )


def sync_navigation():
    baseline = json.loads((audit.DEFAULT_OUT / "baseline.json").read_text())
    titles = {}
    for path in audit.book_files(audit.ROOT):
        for line in path.read_text().splitlines():
            if re.match(r"^#{1,6}\s", line) and audit.HAN.search(line):
                titles[str(path.relative_to(audit.ROOT))] = line[audit.HAN.search(line).start():].strip()
                break
    destination = audit.DEFAULT_OUT / "navigation-edits.json"
    previous = json.loads(destination.read_text()) if destination.exists() else {}
    records = {}
    for file in ("README.md", "_sidebar.md"):
        before = original(file, baseline)
        current = (audit.ROOT / file).read_bytes()
        if current != before and audit.digest(current) != previous.get(file, {}).get("after_sha256"):
            raise ValueError(f"Unrecorded navigation changes: {file}")
        changes = []

        def replacement(match):
            old, target = match[1], match[2]
            title = titles.get(target.removeprefix("./"))
            if title is None:
                raise ValueError(f"Navigation target missing: {target}")
            prefix = re.match(r"^(第[^章]+章)([:：]?\s*)", old)
            if prefix:
                body = re.sub(r"^第[^章]+章[:：]?\s*", "", title)
                title = prefix[1] + prefix[2] + body
            if title != old:
                changes.append({"target": target, "before": old, "after": title})
            return "[" + title + "](" + target + ")"

        after = NAV_LINK.sub(replacement, before.decode()).encode()
        if without_nav_labels(before.decode()) != without_nav_labels(after.decode()):
            raise ValueError("Unexpected navigation mutation")
        records[file] = {"before_sha256": audit.digest(before), "after_sha256": audit.digest(after),
                         "changes": changes}
        (audit.ROOT / file).write_bytes(after)
    audit.dump(destination, records)


def summary():
    result = verify_all(final=True)
    reports()
    lines = [
        "# 全书中文润色结果", "",
        f"已复核{result['verified_documents']}篇文档中的全部现有中文：第1至25章及序言、前言、后记。",
        f"共复核{result['reviewed_chinese_lines']}个含中文的原始物理行，修改{result['changed_chinese_lines']}行。",
        "行数不是段落数或句子数，也不是语义准确率。原先没有译文的英文段落、图注和题记未擅自增译。",
        "",
        "第1章采用用户已批准的样稿；第2至25章由按章节隔离的子代理处理；父任务完成卷首卷尾、保留项复核、跨章检查和全书验收。",
        "没有使用独立的模型 API 批处理，没有提交或推送。",
        "",
        "| 文档 | 复核中文行 | 修改行 | 说明 | 对照 |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for row in result["documents"]:
        directory = "chapter-01" if row["id"] == "ch01" else "chapters/" + row["id"]
        note = "README.md" if row["id"] == "ch01" else "notes.md"
        lines.append(f"| [{row['id']}](../{row['file']}) | {row['reviewed_chinese_lines']} | "
                     f"{row['changed_lines']} | [审校说明]({directory}/{note}) | "
                     f"[完整对照]({directory}/all-changes.md) |")
    lines.extend([
        "", "## 校验与保留边界", "",
        "- 逐章清单可从固定 Git 快照精确重建当前文件；所有现有中文行均有修改或审阅保留记录。",
        "- 英文源文、程序代码块及行内代码、图片、脚注标记和章节结构保持；自然语言代码块例外单独登记。",
        "- 已有有效链接的目标保持不变。第21章一处全角括号损坏的链接语法已单独修复，原可见目标网址未变；解析差异记录于 `link-syntax-exceptions.json`。",
        "- 42个图片资源逐字节保持不变。README 和侧栏仅同步章节链接文字，其他内容及目标路径不变。",
        "- 结构检查不能证明语义正确；各章完成逐段语义审阅，父任务另做交叉复核和保留项处理。",
        "- 原文缺损、未译英文、错误章号、损坏链接、代码样例的既有缺陷和不明确措辞，见各章说明；未把这些问题冒称为已修复。",
        "- 第18章原第337行、第23章原第673行有既有英文缺译，本轮未添加新段落。第4章原文逻辑歧义、第25章延迟方向疑点已明确加译注。第一章缺句的中文已按官方版校正，但本地英文未补写。",
        "- 独立只读代理复核了第11至14章全部3,591行，未提出实质性中文误译，详见 `cross-review.md`。",
        "",
        "## 复核命令", "",
        "```sh",
        "uv run --offline --locked --project tools --cache-dir .cache/uv python tools/book_review.py verify --final",
        "uv run --offline --locked --project tools --cache-dir .cache/uv python -m unittest discover -s tools -p 'test_*.py' -v",
        "git -c core.whitespace=-blank-at-eol diff --check",
        "```", "",
        "当前结果以 `book-verification.json` 和全书校验器为准。各目录的原子代理验证脚本及记录保留其交付时的状态；有父任务修订时，另见 `parent-review.md` 和 `subagent-edits.json`。",
    ])
    (audit.DEFAULT_OUT / "book-summary.md").write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("verify", "apply", "record", "reports", "integrate-parent", "sync-navigation", "summary"))
    parser.add_argument("--chapter")
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    if args.command == "apply":
        apply_manifest(args.chapter)
    elif args.command == "record":
        record(args.chapter)
    elif args.command == "reports":
        reports()
    elif args.command == "integrate-parent":
        integrate_parent()
    elif args.command == "sync-navigation":
        sync_navigation()
    elif args.command == "summary":
        summary()
    else:
        print(json.dumps(verify_all(args.final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
