"""Read-only corpus analysis; only explicit output commands write review artifacts."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import importlib.metadata
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "translation-review"
HAN = re.compile(r"[\u3400-\u9fff]")
ENGLISH = re.compile(r"[A-Za-z]")
URL = re.compile(r"https?://[^\s<>\"`]+")
FOOTNOTE = re.compile(r"\[\^([^\]]+)\](:)?")
ZH_STOP = set(
    "我们 你们 他们 它们 这个 那个 这些 那些 一个 一种 一些 所有 其他 "
    "可以 可能 能够 需要 应该 必须 进行 使用 例如 如果 因为 所以 但是 "
    "没有 已经 不是 就是 这样 这种 什么 如何 更加 非常 通常 时候 方面 "
    "情况 问题 方式 事情 这里 其中 通过 以及 或者 并且 作为 对于 "
    "来说 之间 之中 本章".split()
)
META = re.compile(r"^(?:CHAPTER\s+\d+|Written by\b|Edited by\b|PART\s+[IVX\d]+\b)")
MD = MarkdownIt("commonmark").enable("table")


def digest(data: str | bytes) -> str:
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def dump_rows(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("[\n" + ",\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n]\n")


def book_files(root: Path) -> list[Path]:
    def order(path):
        match = re.search(r"Chapter-(\d+)_", str(path))
        return (int(match[1]) if match else {"Foreword.md": -2, "Preface.md": -1}.get(path.name, 99), str(path))

    return sorted((root / "zh-cn").rglob("*.md"), key=order)


def plain(children) -> str:
    parts = []
    for child in children or []:
        if child.type in {"text", "code_inline"}:
            # Inline identifiers remain useful in prose. Fenced examples do not enter NLP.
            parts.append(child.content)
        elif child.type in {"softbreak", "hardbreak"}:
            parts.append("\n")
    return "".join(parts)


def term_lines_without_break(source: str) -> list[int]:
    """1-based lines made only of emphasized text (a term or run-in label) that end in a soft line break.

    The next line then renders on the same line as the term, while siblings written with a hard
    break (two trailing spaces) do not. Lists and plain paragraphs are checked in both languages.
    """
    lines = []
    for token in MD.parse(source):
        if token.type != "inline" or not token.map:
            continue
        line, depth, emphasized, pure = token.map[0] + 1, 0, False, True
        for child in token.children or []:
            if child.type in {"softbreak", "hardbreak"}:
                if child.type == "softbreak" and pure and emphasized and depth == 0:
                    lines.append(line)
                line, emphasized, pure = line + 1, False, True
            elif child.type in {"em_open", "strong_open"}:
                depth += 1
                emphasized = True
            elif child.type in {"em_close", "strong_close"}:
                depth -= 1
            elif depth == 0 and not (child.type == "text" and not child.content.strip()):
                pure = False
    return lines


def literal_emphasis_markers(source: str) -> list[int]:
    """1-based lines where an asterisk survives parsing as plain text: an emphasis marker that did not pair.

    CommonMark pairs a closing ``*`` or ``**`` that follows punctuation only when whitespace or
    punctuation comes next, so ``**标题。**正文`` shows its asterisks. Code spans are not text.
    """
    lines = []
    for token in MD.parse(source):
        if token.type != "inline" or not token.map:
            continue
        line = token.map[0] + 1
        for child in token.children or []:
            if child.type in {"softbreak", "hardbreak"}:
                line += 1
            elif child.type == "text" and "*" in child.content and line not in lines:
                lines.append(line)
    return lines


def language_runs(text: str, heading: bool = False) -> list[tuple[str, str]]:
    """Language detection is a heuristic; mixed non-heading lines remain Chinese context."""
    runs = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        pieces = [line]
        first_han = HAN.search(line)
        if heading and first_han and ENGLISH.search(line[: first_han.start()]):
            pieces = [line[: first_han.start()].strip(), line[first_han.start() :]]
        for piece in pieces:
            lang = "zh" if HAN.search(piece) else "en" if ENGLISH.search(piece) else "other"
            if runs and runs[-1][0] == lang:
                runs[-1] = (lang, runs[-1][1] + "\n" + piece)
            else:
                runs.append((lang, piece))
    return runs


class HTMLRefs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "a" and values.get("name"):
            self.ids.append(values["name"])
        for attr in ("href", "src"):
            if values.get(attr):
                self.refs.append(("image" if tag == "img" else "link", values[attr]))


def parse_document(path: str, source: str) -> dict:
    lines = source.splitlines(keepends=True)
    env = {}
    tokens = MD.parse(source, env)
    segments, codes, links, structures, html, explicit_ids = [], [], [], [], [], []
    stack = []
    code_lines = set()
    serial = 0
    chapter = re.search(r"Chapter-(\d+)_", path)
    document_id = f"ch{int(chapter[1]):02d}" if chapter else Path(path).stem

    def add_link(kind, target, line):
        links.append({"kind": kind, "target": target, "line": line})

    for token in tokens:
        if token.nesting == -1:
            if stack:
                stack.pop()
            continue
        if token.nesting == 1:
            stack.append(token)
            if token.type in {
                "heading_open", "bullet_list_open", "ordered_list_open",
                "list_item_open", "table_open", "tr_open", "th_open", "td_open", "blockquote_open",
            }:
                structures.append({"type": token.type, "tag": token.tag})
            continue
        parent_map = next((s.map for s in reversed(stack) if s.map), [0, 0])
        span = token.map or parent_map
        line_number = span[0] + 1
        if token.type in {"fence", "code_block"}:
            codes.append({"kind": token.type, "info": token.info, "content": token.content, "line": line_number})
            code_lines.update(range(span[0], span[1]))
            continue
        if token.type == "html_block":
            html.append(token.content)
            parser = HTMLRefs()
            parser.feed(token.content)
            explicit_ids.extend(parser.ids)
            for kind, target in parser.refs:
                add_link(kind, target, line_number)
            continue
        if token.type != "inline":
            continue
        types = {s.type for s in stack}
        kind = (
            "heading" if "heading_open" in types else
            "table" if "table_open" in types else
            "quote" if "blockquote_open" in types else "body"
        )
        is_list = "list_item_open" in types
        for child in token.children or []:
            if child.type == "code_inline":
                codes.append({"kind": "inline", "info": "", "content": child.content, "line": line_number})
            if child.type in {"link_open", "image"}:
                add_link("image" if child.type == "image" else "link",
                         child.attrGet("src" if child.type == "image" else "href"), line_number)
            if child.type == "html_inline":
                html.append(child.content)
                parser = HTMLRefs()
                parser.feed(child.content)
                explicit_ids.extend(parser.ids)
                for ref_kind, target in parser.refs:
                    add_link(ref_kind, target, line_number)
            if child.type in {"text", "code_inline"}:
                for url in URL.findall(child.content):
                    add_link("bare_url", url.rstrip(".,;!?)"), line_number)
        text = plain(token.children)
        if not text.strip():
            continue
        for lang, part in language_runs(text, kind == "heading"):
            if lang == "other":
                continue
            current_kind = kind
            if META.match(part):
                current_kind = "metadata"
            elif kind == "quote" and re.match(r"^(?:\[\^?\d+\]:?|\d+\s)", part):
                current_kind = "footnote"
            elif re.match(r"^(?:Figure|Example)\s+\d+[-.]\d+", part):
                current_kind = "caption"
            serial += 1
            segments.append({
                "id": f"{document_id}:s{serial:04d}", "file": path,
                "line": line_number, "end_line": span[1],
                "kind": current_kind, "list_item": is_list,
                "language": lang, "text": part,
                "language_status": "heuristic",
            })
    # Also capture definitions which CommonMark consumes without emitting inline tokens.
    for definition in env.get("references", {}).values():
        add_link("reference_definition", definition["href"], definition.get("map", [0])[0] + 1)
    footnotes = []
    english_lines = []
    for i, line in enumerate(lines):
        if i in code_lines:
            continue
        for match in FOOTNOTE.finditer(line):
            footnotes.append({"id": match[1], "definition": bool(match[2]), "line": i + 1})
        if ENGLISH.search(line) and not HAN.search(line):
            english_lines.append(digest(line))
    return {
        "file": path, "sha256": digest(source), "segments": segments,
        "codes": codes, "links": links, "structures": structures, "html": html,
        "explicit_ids": explicit_ids, "footnotes": footnotes,
        "english_line_hashes": english_lines,
    }


def align_segments(segments: list[dict]) -> list[dict]:
    """Adjacent language runs are candidates, never human-verified translations."""
    runs = []
    for segment in segments:
        # Headings and metadata must not accidentally pair with a body paragraph.
        boundary = "heading" if segment["kind"] == "heading" else (
            "metadata" if segment["kind"] == "metadata" else "content"
        )
        key = (segment["file"], boundary, segment["language"])
        if runs and runs[-1][0] == key:
            runs[-1][1].append(segment)
        else:
            runs.append((key, [segment]))
    groups = []
    paired = set()
    for i in range(len(runs) - 1):
        akey, english = runs[i]
        bkey, chinese = runs[i + 1]
        if akey[:2] != bkey[:2] or akey[2] != "en" or bkey[2] != "zh" or akey[1] == "metadata":
            continue
        signature = lambda s: (s["kind"], s["list_item"])
        if len(english) == len(chinese) and all(signature(a) == signature(b) for a, b in zip(english, chinese)):
            for en, zh in zip(english, chinese):
                status = "adjacent_1_to_1" if len(english) == 1 else "ordered_run"
                groups.append({"id": en["id"], "english": [en["id"]], "chinese": [zh["id"]], "status": status})
                paired.add(en["id"])
        else:
            groups.append({
                "id": english[0]["id"],
                "english": [s["id"] for s in english], "chinese": [s["id"] for s in chinese],
                "status": "ambiguous",
            })
            paired.update(s["id"] for s in english)
    for segment in segments:
        if segment["language"] == "en" and segment["id"] not in paired and segment["kind"] != "metadata":
            groups.append({"id": segment["id"], "english": [segment["id"]], "chinese": [], "status": "unpaired"})
    return groups


def scan(root: Path):
    documents = [
        parse_document(str(path.relative_to(root)), path.read_bytes().decode("utf-8"))
        for path in book_files(root)
    ]
    segments = [s for d in documents for s in d["segments"]]
    return documents, segments, align_segments(segments)


def protected(document: dict) -> dict:
    return {
        "sha256": document["sha256"],
        "english_line_hashes": document["english_line_hashes"],
        "english_segment_hashes": [
            digest(s["text"]) for s in document["segments"] if s["language"] == "en"
        ],
        "code_hashes": [digest(json.dumps({k: c[k] for k in ("kind", "info", "content")}, sort_keys=True))
                        for c in document["codes"]],
        "links": [{k: ref[k] for k in ("kind", "target")} for ref in document["links"]],
        "structures": document["structures"],
        "html_hashes": [digest(h) for h in document["html"]],
        "footnotes": [{k: f[k] for k in ("id", "definition")} for f in document["footnotes"]],
    }


def make_baseline(root: Path, documents: list[dict]) -> dict:
    files = {doc["file"]: protected(doc) for doc in documents}
    for name in ("README.md", "_sidebar.md", "_coverpage.md", "index.html"):
        if (root / name).is_file():
            files[name] = {"sha256": digest((root / name).read_bytes())}
    assets = {}
    for folder in (root / "assets", root / "zh-cn"):
        for path in sorted(folder.rglob("*")):
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
                assets[str(path.relative_to(root))] = digest(path.read_bytes())
    return {
        "schema": 1,
        "git_commit": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": files, "assets": assets,
        "limitations": [
            "Language identification and bilingual alignment are heuristics, not semantic validation.",
            "English embedded in Chinese prose requires manual diff review; inline code is protected.",
            "Structure changes are flagged for review, not silently accepted.",
            "External link reachability is not checked by this offline tool.",
        ],
    }


def verify_baseline(root: Path, baseline: dict, exact: bool = False) -> list[str]:
    documents, _, _ = scan(root)
    current = make_baseline(root, documents)
    errors = []
    for section in ("files", "assets"):
        old, new = baseline[section], current[section]
        for file in sorted(old.keys() | new.keys()):
            if file not in old or file not in new:
                errors.append(f"{section}: added/deleted {file}")
                continue
            if section == "assets":
                if old[file] != new[file]:
                    errors.append(f"asset changed: {file}")
                continue
            for key in old[file]:
                if key == "sha256" and not exact and len(old[file]) > 1:
                    continue
                if old[file][key] != new[file].get(key):
                    errors.append(f"{file}: {key} changed")
    return errors


def link_issues(root: Path, documents: list[dict]) -> list[dict]:
    issues = []
    by_path = {d["file"]: d for d in documents}
    for name in ("README.md", "_sidebar.md", "_coverpage.md"):
        if (root / name).is_file():
            by_path[name] = parse_document(name, (root / name).read_text())
    for file, doc in by_path.items():
        seen = set()
        for ref in doc["links"]:
            target = ref["target"]
            if (ref["line"], target) in seen:
                continue
            seen.add((ref["line"], target))
            split = urlsplit(target)
            if split.scheme or split.netloc or target.startswith("//"):
                continue
            decoded = unquote(split.path)
            if target == "Ibid." or ("https://" in decoded or "http://" in decoded):
                issues.append({
                    "file": file, "line": ref["line"], "type": "footnote_parsed_as_relative_link",
                    "target": target, "status": "observed_in_markdown_it_requires_site_check",
                })
                continue
            destination = (root / decoded.lstrip("/") if decoded.startswith("/") else
                           (root / file).parent / decoded) if decoded else root / file
            if not destination.exists():
                issues.append({"file": file, "line": ref["line"], "type": "missing_local_target",
                               "target": target, "status": "confirmed_local"})
            elif split.fragment:
                relative = str(destination.resolve().relative_to(root.resolve()))
                dest_doc = by_path.get(relative)
                fragment = unquote(split.fragment)
                if dest_doc and fragment.startswith("_bookmark") and fragment not in dest_doc["explicit_ids"]:
                    issues.append({
                        "file": file, "line": ref["line"], "type": "legacy_bookmark_without_explicit_id",
                        "target": target, "status": "suspected_requires_render_check",
                    })
                elif dest_doc and fragment not in dest_doc["explicit_ids"]:
                    issues.append({
                        "file": file, "line": ref["line"], "type": "generated_anchor_not_verified",
                        "target": target, "status": "requires_render_check",
                    })
        refs = Counter(f["id"] for f in doc["footnotes"] if not f["definition"])
        definitions = Counter(f["id"] for f in doc["footnotes"] if f["definition"])
        for key in sorted(refs.keys() - definitions.keys()):
            issues.append({"file": file, "line": next(f["line"] for f in doc["footnotes"] if f["id"] == key),
                           "type": "footnote_reference_without_definition",
                           "target": key, "status": "confirmed_raw_markers"})
    return issues


def canonical(tokens) -> str:
    words = []
    for token in tokens:
        if token.is_space:
            continue
        value = token.lemma_ if token.pos_ == "NOUN" else token.text
        words.append(value.lower().replace("\u2010", "-").replace("\u2011", "-"))
    return re.sub(r"\s*-\s*", "-", " ".join(words)).strip()


def extract_terms(doc) -> list[dict]:
    occurrences = {}

    def add(start, end, signal):
        span = doc[start:end]
        while len(span) and (span[0].pos_ in {"DET", "PRON", "NUM"} or span[0].is_stop):
            span = doc[span.start + 1:span.end]
        if not len(span) or len(span) > 8:
            return
        if not any(t.pos_ in {"NOUN", "PROPN"} for t in span):
            return
        if any(t.like_url or t.like_email for t in span):
            return
        key = canonical(span)
        if not ENGLISH.search(key) or len(key) < 2 or key in {"figure", "example", "chapter", "section"}:
            return
        identity = (span.start_char, span.end_char, key)
        if identity not in occurrences:
            occurrences[identity] = {"term": key, "form": span.text, "signals": set(),
                                     "start": span.start_char, "end": span.end_char}
        occurrences[identity]["signals"].add(signal)
        following = doc[span.end: min(span.end + 4, len(doc))]
        if following and (following[0].lemma_ in {"be", "refer", "mean"}):
            occurrences[identity]["signals"].add("definition_context")

    for token in doc:
        if token.pos_ in {"NOUN", "PROPN"} and not token.is_stop and token.is_alpha:
            add(token.i, token.i + 1, "noun")
        if re.fullmatch(r"[A-Z][A-Z0-9+]{1,11}", token.text):
            add(token.i, token.i + 1, "acronym")
    for chunk in doc.noun_chunks:
        add(chunk.start, chunk.end, "noun_phrase")
    for start in range(len(doc)):
        if doc[start].pos_ not in {"NOUN", "PROPN"}:
            continue
        if start + 2 < len(doc) and doc[start + 1].text.lower() == "of":
            for end in range(start + 3, min(start + 6, len(doc)) + 1):
                tail = doc[start + 2:end]
                if tail[-1].pos_ in {"NOUN", "PROPN"} and all(
                    t.pos_ in {"DET", "ADJ", "NOUN", "PROPN"} for t in tail
                ):
                    add(start, end, "of_phrase")
    # Short compound phrases recover terms nested inside longer noun chunks.
    for start in range(len(doc)):
        for end in range(start + 2, min(start + 6, len(doc)) + 1):
            span = doc[start:end]
            if span[-1].pos_ not in {"NOUN", "PROPN"}:
                continue
            if all((t.pos_ in {"ADJ", "NOUN", "PROPN"} and not t.is_stop) or t.text in {"-", "\u2010", "\u2011"}
                   for t in span) and span[0].text not in {"-", "\u2010", "\u2011"}:
                add(start, end, "compound_ngram")
    for ent in doc.ents:
        if ent.label_ in {"ORG", "PRODUCT", "LAW"}:
            add(ent.start, ent.end, "named_entity")
    return list(occurrences.values())


def count_surface_forms(segments: list[dict], definitions: dict) -> dict:
    """Recount observed inflections, including occurrences with incorrect model POS tags."""
    by_first_word = defaultdict(set)
    for i, segment in enumerate(segments):
        for word in set(re.findall(r"\w+", segment["text"].lower())):
            by_first_word[word].add(i)
    terms = {}
    for key, definition in definitions.items():
        forms = sorted(definition["forms"], key=lambda form: (-len(form), form))
        patterns = [r"\s+".join(re.escape(part) for part in form.split()) for form in forms]
        pattern = re.compile(r"(?<!\w)(?:" + "|".join(patterns) + r")(?!\w)", re.I)
        possible = set()
        for form in forms:
            first = re.search(r"\w+", form.lower())
            if first:
                possible.update(by_first_word[first[0]])
        row = {
            "term": key, "frequency": 0, "documents": Counter(), "sections": Counter(),
            "forms": Counter(), "signals": set(definition["signals"]) | {"surface_recount"},
            "segment_ids": set(), "evidence": [],
        }
        for i in sorted(possible):
            segment = segments[i]
            for match in pattern.finditer(segment["text"]):
                row["frequency"] += 1
                row["documents"][segment["file"]] += 1
                row["sections"][segment["kind"]] += 1
                row["forms"][match[0]] += 1
                row["segment_ids"].add(segment["id"])
                row["evidence"].append({"segment": segment["id"], "start": match.start(), "end": match.end()})
        if row["frequency"]:
            terms[key] = row
    return terms


def chinese_candidates(text, segmenter) -> Counter:
    tokens = list(segmenter.cut(text, HMM=True))
    result = Counter()
    for start in range(len(tokens)):
        if start and tokens[start - 1].word in {"不", "非", "无", "未"}:
            continue
        phrase = ""
        for end in range(start, min(start + 4, len(tokens))):
            token = tokens[end]
            if not re.fullmatch(r"[\u3400-\u9fff]+", token.word) or token.word in ZH_STOP:
                break
            negation_prefix = end == start and token.word in {"不", "非", "无", "未"}
            if token.flag[0] not in {"n", "v", "a", "j", "l", "i"} and not negation_prefix:
                break
            phrase += token.word
            if 2 <= len(phrase) <= 12 and token.flag[0] in {"n", "v", "j", "l", "i"}:
                result[phrase] += 1
            if len(phrase) > 12:
                break
    return result


def analyze(root: Path, out: Path):
    import jieba
    import jieba.posseg
    import spacy

    documents, segments, groups = scan(root)
    index = {s["id"]: s for s in segments}
    print(f"Parsed {len(documents)} documents, {len(segments)} language segments.", flush=True)
    eligible = [s for s in segments if s["language"] == "en" and s["kind"] != "metadata"]
    nlp = spacy.load("en_core_web_sm")
    vocabulary = defaultdict(lambda: {"forms": set(), "signals": set()})
    for doc in nlp.pipe((s["text"] for s in eligible), batch_size=64):
        for occurrence in extract_terms(doc):
            vocabulary[occurrence["term"]]["forms"].add(occurrence["form"])
            vocabulary[occurrence["term"]]["signals"].update(occurrence["signals"])
    print(f"Discovered {len(vocabulary)} candidates; recounting across the corpus.", flush=True)
    terms = count_surface_forms(eligible, vocabulary)
    print(f"English extraction: {len(terms)} distinct raw candidates.", flush=True)
    tokenizer = jieba.Tokenizer()
    tokenizer.tmp_dir = str(root / ".cache")
    (root / ".cache").mkdir(exist_ok=True)
    segmenter = jieba.posseg.POSTokenizer(tokenizer)
    zh_counts = {s["id"]: chinese_candidates(s["text"], segmenter) for s in segments if s["language"] == "zh"}
    total_zh = Counter()
    for counts in zh_counts.values():
        total_zh.update(counts)
    usable = [g for g in groups if g["status"] in {"adjacent_1_to_1", "ordered_run"}]
    group_by_en = {s: g["id"] for g in usable for s in g["english"]}
    zh_by_group = {g["id"]: set().union(*(set(zh_counts[z]) for z in g["chinese"])) for g in usable}
    zh_group_frequency = Counter(word for words in zh_by_group.values() for word in words)
    rows = []
    for key, row in terms.items():
        if row["frequency"] < 2 and not row["sections"]["heading"] and not (
            row["signals"] & {"acronym", "named_entity", "definition_context"}
        ):
            continue
        group_ids = {group_by_en[s] for s in row["segment_ids"] if s in group_by_en}
        support = Counter(word for group in group_ids for word in zh_by_group[group])
        associates = []
        for word, count in support.items():
            if count < 2 and len(group_ids) >= 3:
                continue
            dice = 2 * count / (len(group_ids) + zh_group_frequency[word])
            associates.append({"text": word, "support_groups": count,
                               "all_chinese_groups": zh_group_frequency[word], "dice": round(dice, 4)})
        associates.sort(key=lambda r: (-r["dice"], -r["support_groups"], -len(r["text"]), r["text"]))
        row["document_frequency"] = len(row["documents"])
        row["chapter_frequency"] = sum("Chapter-" in p for p in row["documents"])
        row["priority_score"] = round(math.log1p(row["frequency"]) * (1 + math.log1p(len(row["documents"])))
                                      + 2 * math.log1p(row["sections"]["heading"]), 4)
        row["aligned_group_count"] = len(group_ids)
        row["chinese_cooccurrence_candidates"] = associates[:8]
        row["signals"] = sorted(row["signals"])
        row["forms"] = dict(sorted(row["forms"].items(), key=lambda x: (-x[1], x[0])))
        row["documents"] = dict(sorted(row["documents"].items()))
        row["sections"] = dict(sorted(row["sections"].items()))
        row["segment_ids"] = sorted(row["segment_ids"])
        row["status"] = "unreviewed_candidate"
        rows.append(row)
    rows.sort(key=lambda r: (-r["priority_score"], -r["frequency"], r["term"]))
    summary = {
        "documents": len(documents), "segments": len(segments),
        "english_segments_analyzed": len(eligible), "chinese_segments": len(zh_counts),
        "alignment_groups": dict(Counter(g["status"] for g in groups)),
        "raw_english_candidates": len(terms), "retained_english_candidates": len(rows),
        "chinese_candidate_phrases": len(total_zh),
        "retention_rule": "frequency >= 2 OR heading occurrence OR acronym/named_entity/definition_context signal",
        "association_status": "Cooccurrence only; neither bilingual alignment nor candidate translations are verified.",
        "frequency_definition": "Observed inflected surface forms grouped by candidate lemma, recounted with word boundaries; not semantic sense counts.",
        "priority_formula": "log(1 + frequency) * (1 + log(1 + document_frequency)) + 2 * log(1 + heading_frequency)",
        "tool_sha256": digest(Path(__file__).read_bytes()),
        "versions": {name: importlib.metadata.version(name) for name in
                     ("spacy", "en-core-web-sm", "jieba", "markdown-it-py")},
        "source_hashes": {d["file"]: d["sha256"] for d in documents},
    }
    out.mkdir(parents=True, exist_ok=True)
    with (out / "segments.jsonl").open("w") as stream:
        for segment in segments:
            stream.write(json.dumps(segment, ensure_ascii=False) + "\n")
    dump(out / "alignments.json", groups)
    dump_rows(out / "candidates.json", rows)
    dump(out / "chinese-frequency.json", dict(sorted(total_zh.items(), key=lambda x: (-x[1], x[0]))))
    dump(out / "summary.json", summary)
    dump(out / "existing-issues.json", link_issues(root, documents))
    lines = [
        "# 术语候选统计", "",
        "自动生成，尚未人工审定。中文栏只是对齐上下文中的共现候选，不是已确认译法。",
        "频次包含英文正文、标题、引文、脚注、表格和图注；不含署名及代码块。",
        "相同位置由多种方法抽取时只计一次；同一术语在不同位置重复出现仍分别计数。",
        "下表展示排序前 200 项；全部候选、逐章频次及出现位置见 `candidates.json`。", "",
        "| 英文候选 | 出现次数 | 文档数 | 正文章节数 | 标题次数 | 中文共现候选（组数） |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows[:200]:
        zh = "；".join(f"{x['text']}（{x['support_groups']}）" for x in row["chinese_cooccurrence_candidates"][:4])
        lines.append(f"| {escape_md(row['term'])} | {row['frequency']} | {row['document_frequency']} | "
                     f"{row['chapter_frequency']} | {row['sections'].get('heading', 0)} | {escape_md(zh)} |")
    (out / "candidate-report.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


def escape_md(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def alias_matches(text: str, aliases: list[str]) -> Counter:
    if not aliases:
        return Counter()
    # Longest-first prevents the shorter alias from double-counting the same occurrence.
    pattern = re.compile("|".join(re.escape(a) for a in sorted(aliases, key=lambda a: (-len(a), a))), re.I)
    return Counter(match.group(0) for match in pattern.finditer(text))


def render_glossary(root: Path, out: Path, decisions_path: Path):
    decisions = json.loads(decisions_path.read_text())
    candidates = {r["term"]: r for r in json.loads((out / "candidates.json").read_text())}
    segments = {s["id"]: s for s in map(json.loads, (out / "segments.jsonl").read_text().splitlines())}
    groups = json.loads((out / "alignments.json").read_text())
    by_en = {s: g for g in groups if g["status"] in {"adjacent_1_to_1", "ordered_run"} for s in g["english"]}
    results = []
    for decision in decisions:
        missing = set(decision["keys"]) - candidates.keys()
        if missing:
            raise ValueError(f"Decision has no measured candidate: {missing}")
        for evidence in decision["evidence"]:
            if "file" not in evidence:
                evidence["file"] = str(next(
                    p.relative_to(root) for p in book_files(root)
                    if f"Chapter-{evidence['chapter']}_" in str(p)
                ))
            source = (root / evidence["file"]).read_text()
            if evidence["quote"] not in source:
                raise ValueError(f"Missing decision evidence: {evidence}")
            evidence["line"] = source[:source.index(evidence["quote"])].count("\n") + 1
        rows = [candidates[key] for key in decision["keys"]]
        source_ids = set().union(*(set(r["segment_ids"]) for r in rows))
        target_ids = set()
        for source_id in source_ids:
            if source_id in by_en:
                target_ids.update(by_en[source_id]["chinese"])
        counts = Counter()
        locations = defaultdict(list)
        for target_id in sorted(target_ids):
            found = alias_matches(segments[target_id]["text"], decision["observed_aliases"])
            counts.update(found)
            for alias, count in found.items():
                locations[alias].append({"segment": target_id, "count": count})
        documents = Counter()
        for row in rows:
            documents.update(row["documents"])
        results.append({
            **decision, "frequency": sum(r["frequency"] for r in rows),
            "documents": dict(sorted(documents.items())),
            "document_frequency": len(documents), "source_segment_count": len(source_ids),
            "usable_target_segment_count": len(target_ids),
            "observed_alias_counts_in_aligned_context": dict(counts),
            "alias_locations": dict(locations),
            "count_limit": "Counts are exact substring matches in heuristic aligned context, not verified token-level translations.",
        })
    dump(out / "glossary-statistics.json", results)
    lines = [
        "# 核心术语表", "",
        "这是基于自动候选和原文抽样审定的首批术语，不是全书完整词典。",
        "首选译法适用于注明的语境，不授权全局替换。",
        "英文频次为列出 keys 的合计；异译计数是候选对齐中文段内的精确字符串命中，不能视为逐词对齐后的译法频次。",
        "未命中已列异译不等于漏译。全部定义、例外、证据和计数位置见 `glossary-statistics.json`。", "",
        "| 英文术语 | 首选译法 | 英文次数 / 文档数 | 对齐中文中的已有异译命中 | 使用边界 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in results:
        variants = "；".join(f"{a}：{n}" for a, n in row["observed_alias_counts_in_aligned_context"].items()) or "未命中"
        lines.append(f"| {escape_md(row['term'])} | {escape_md(row['preferred'])} | "
                     f"{row['frequency']} / {row['document_frequency']} | {escape_md(variants)} | "
                     f"{escape_md(row['scope'])} |")
    lines.extend(["", "## 审定依据", ""])
    for row in results:
        lines.append(f"### {row['term']}")
        lines.extend(["", row["definition"], "", f"例外：{row['exceptions']}", ""])
        for evidence in row["evidence"]:
            lines.append(f"- `{evidence['file']}:{evidence['line']}`：{evidence['quote']}")
        lines.append("")
    (out / "glossary.md").write_text("\n".join(lines) + "\n")
    print(f"Rendered {len(results)} reviewed glossary entries.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("baseline", "analyze", "verify", "glossary"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--exact", action="store_true", help="Also require every source file byte to match.")
    args = parser.parse_args()
    root, out = args.root.resolve(), args.out.resolve()
    if args.command == "baseline":
        destination = out / "baseline.json"
        if destination.exists():
            parser.error("Refusing to overwrite the baseline. Choose a new --out explicitly.")
        documents, _, _ = scan(root)
        dump(destination, make_baseline(root, documents))
        print(f"Recorded baseline for {len(documents)} book documents.")
    elif args.command == "analyze":
        analyze(root, out)
    elif args.command == "verify":
        errors = verify_baseline(root, json.loads((out / "baseline.json").read_text()), args.exact)
        for error in errors:
            print(error)
        if errors:
            sys.exit(1)
        print("PASS: baseline matches" + (" byte-for-byte." if args.exact else " protected content."))
    else:
        render_glossary(root, out, out / "glossary-decisions.json")


if __name__ == "__main__":
    main()
