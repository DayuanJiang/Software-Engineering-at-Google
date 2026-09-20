"""Compile reviewed note mappings into display-only edits and popover content."""

import copy
import re

import translation_audit as audit
from markdown_it import MarkdownIt

DEFINITION = re.compile(r"^\s*(?:>\s*)*\[\^?(\d+)\^?\]:", re.MULTILINE)
PROSE_MD = MarkdownIt("commonmark", {"html": False}).enable("table")


def plain(markdown):
    tokens = audit.MD.parseInline(markdown)
    return " ".join(audit.plain(tokens[0].children).split()) if tokens else ""


def without_markers(text):
    return re.sub(r"\[(?:\^\d+|\d+\^)\]", "", text)


def anchor_count(source, anchor, edits=()):
    needle = " ".join(without_markers(anchor).split())
    if not needle:
        return 0
    blocks = [plain(without_markers(token.content)) for token in audit.MD.parse(source) if token.type == "inline"]
    for edit in edits:
        blocks = [block.replace(" ".join(edit["source"].split()), " ".join(edit["replacement"].split())) for block in blocks]
    return sum(block.count(needle) for block in blocks)


def compile_review(key, source, review):
    result = copy.deepcopy(review)
    if result.get("blockingIssues"):
        raise ValueError(f"Unresolved reader mapping issues: {key}: {result['blockingIssues']}")
    lines = source.splitlines(keepends=True)
    expected = set(DEFINITION.findall(source))
    ids = [str(note["id"]) for note in result.get("footnotes", [])]
    if len(ids) != len(set(ids)) or not expected.issubset(ids):
        raise ValueError(f"Footnote coverage mismatch: {key}: expected {sorted(expected)}, got {ids}")
    edits = []
    occupied = set()
    for note in result.get("footnotes", []):
        identifier = str(note["id"])
        start, end = note["definitionLines"]
        if not (isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= len(lines)):
            raise ValueError(f"Invalid definition lines: {key}: {identifier}")
        covered = set(range(start, end + 1))
        if occupied & covered:
            raise ValueError(f"Overlapping definitions: {key}: {identifier}")
        occupied |= covered
        block = "".join(lines[start - 1:end])
        prefix = re.match(r"^\s*(?:>\s*)*(?:\[\^?(\d+)\^?[\]}]\s*[:;]?|(\d+)\s+)", block)
        prefix_id = (prefix[1] or prefix[2]) if prefix else None
        if prefix_id != identifier or not set(DEFINITION.findall(block)).issubset({identifier}):
            raise ValueError(f"Definition range does not identify one note: {key}: {identifier}")
        if identifier not in expected and not note.get("reason"):
            raise ValueError(f"Unexplained nonstandard definition: {key}: {identifier}")
        cleaned = "\n".join(re.sub(r"^\s*(?:>\s*)+", "", line) for line in block.splitlines())
        cleaned = re.sub(r"^\s*(?:\[\^?\d+\^?[\]}]\s*[:;]?\s*|\d+\s+)", "", cleaned)
        remaining = plain(cleaned)
        for language in ["english", "chinese"]:
            text = plain(note.get(language, ""))
            if not text:
                raise ValueError(f"Missing {language} note: {key}: {identifier}")
            if language == "chinese" and note.get("chineseAdded"):
                if not note.get("reason"):
                    raise ValueError(f"Missing reason for added translation: {key}: {identifier}")
                continue
            if text not in remaining:
                raise ValueError(f"{language} note differs from source: {key}: {identifier}")
            remaining = remaining.replace(text, "", 1)
        if re.search(r"[A-Za-z\u3400-\u9fff]", remaining):
            raise ValueError(f"Definition range contains unaccounted text: {key}: {identifier}: {remaining}")
        note["englishHtml"] = PROSE_MD.render(note["english"])
        note["chineseHtml"] = PROSE_MD.render(note["chinese"])
        edits.append({"startLine": start, "endLine": end, "source": block})
    body_lines = lines.copy()
    for edit in sorted(edits, key=lambda item: item["startLine"], reverse=True):
        body_lines[edit["startLine"] - 1:edit["endLine"]] = ["\n"]
    body = "".join(body_lines)
    for edit in result.get("textEdits", []):
        if anchor_count(body, edit["source"]) != 1 or not edit.get("reason"):
            raise ValueError(f"Unverified display text edit: {key}: {edit['source']}")
    for note in result.get("footnotes", []):
        for field in ["after", "englishAfter"]:
            if field == "englishAfter" and not note.get(field):
                continue
            if anchor_count(body, note.get(field, ""), result.get("textEdits", [])) != 1:
                raise ValueError(f"Ambiguous {field} anchor: {key}: {note['id']}: {note.get(field)}")
    for translation in result.get("translations", []):
        if translation.get("kind") == "heading":
            tokens = audit.MD.parse(body)
            count = sum(
                token.type == "inline" and index > 0 and tokens[index - 1].type == "heading_open"
                and plain(token.content) == translation["english"]
                for index, token in enumerate(tokens)
            )
        else:
            count = anchor_count(body, translation["english"])
        if count != 1:
            raise ValueError(f"Translation source is not unique: {key}: {translation['english'][:80]}")
        if not re.search(r"[\u3400-\u9fff]", translation["chinese"]):
            raise ValueError(f"Missing Chinese translation: {key}")
        translation["chineseHtml"] = PROSE_MD.render(translation["chinese"])
    for pair in result.get("pairedSources", []):
        if not pair.get("reason"):
            raise ValueError(f"Missing review reason for prose pair: {key}")
        for language in ["english", "chinese"]:
            count = anchor_count(body, pair[language], result.get("textEdits", []))
            needle = " ".join(without_markers(pair[language]).split())
            count += sum(plain(without_markers(item["text"])).count(needle) for item in result.get("proseCodeBlocks", []))
            if count != 1:
                raise ValueError(f"Reviewed {language} prose pair is not unique: {key}: {pair[language][:90]}")
    tables = []
    current = None
    for token in audit.MD.parse(body):
        if token.type == "table_open":
            current = {"rows": 0, "headers": []}
        elif token.type == "table_close":
            tables.append(current); current = None
        elif current is not None:
            if token.type == "tr_open":
                current["rows"] += 1
            elif token.type == "inline" and current["rows"] == 1:
                current["headers"].append(plain(token.content))
    for pair in result.get("pairedTables", []):
        if not pair.get("reason"):
            raise ValueError(f"Missing table-pair review reason: {key}")
        indices = [pair["englishIndex"], pair["chineseIndex"]]
        if any(not isinstance(index, int) or index < 0 for index in indices) or indices[0] == indices[1]:
            raise ValueError(f"Invalid reviewed table indices: {key}")
        try:
            english = tables[pair["englishIndex"]]
            chinese = tables[pair["chineseIndex"]]
        except IndexError as error:
            raise ValueError(f"Missing reviewed table: {key}") from error
        if english["rows"] != chinese["rows"] or len(english["headers"]) != len(chinese["headers"]):
            raise ValueError(f"Reviewed table structures differ: {key}")
        pair["english"] = english; pair["chinese"] = chinese
    code = [t.content.strip() for t in audit.MD.parse(source) if t.type in {"fence", "code_block"}]
    groups = {}
    for item in result.get("proseCodeBlocks", []):
        matches = [block for block in code if item["text"] in block]
        if len(matches) != 1:
            raise ValueError(f"Ambiguous reviewed prose block: {key}")
        groups.setdefault(matches[0], []).append(item)
    normalized = []
    for block, items in groups.items():
        remaining = block
        parts = []
        for item in items:
            remaining = remaining.replace(item["text"], "", 1)
            if item["language"] == "bilingual":
                runs = []
                for line in item["text"].splitlines():
                    if not line.strip():
                        if runs:
                            runs[-1]["text"] += "\n"
                        continue
                    language = "zh" if re.search(r"[\u3400-\u9fff]", line) else "en"
                    if not runs or runs[-1]["language"] != language:
                        runs.append({"language": language, "text": line})
                    else:
                        runs[-1]["text"] += "\n" + line
                parts.extend({"language": run["language"], "html": PROSE_MD.render(run["text"])} for run in runs)
            else:
                parts.append({"language": item["language"], "html": PROSE_MD.render(item["text"])})
        if remaining.strip():
            raise ValueError(f"Reviewed prose covers only part of a code block: {key}")
        normalized.append({"text": block, "parts": parts})
    result["proseCodeBlocks"] = normalized
    for item in result.get("translatorNotes", []):
        item["renderedText"] = plain(item["text"])
        if code.count(item["text"]) != 1 and anchor_count(body, item["renderedText"]) != 1:
            raise ValueError(f"Translator note source is not unique: {key}")
        item["bodyHtml"] = PROSE_MD.render(item["body"])
    result["sourceEdits"] = edits
    return result
