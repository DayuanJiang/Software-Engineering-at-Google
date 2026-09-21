"""One-off migration: split the interleaved bilingual chapters into English sources and Chinese translations.

Reads the legacy interleaved zh-cn/*.md files (English paragraph followed by its translation, headings written
as "English 中文") and the reviewed reader mappings from the last commit that held them, and writes:

    en/<chapter>/<chapter>.md      English source blocks; code, images and rules live only here
    zh-cn/<chapter>/<chapter>.md   Chinese translation blocks in the same order, one per translatable source block

Footnotes become standard `[^n]:` definitions at the end of each file. Translator notes become `[^tN]:`
definitions in the Chinese file. Run with `uv run --project tools python tools/split_book.py [--out DIR]`.
"""

import argparse
import json
from pathlib import Path
import re
import subprocess

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "83df794"  # last revision with the interleaved chapters and assets/reader-content mappings
MD = MarkdownIt("commonmark").enable("table")


def git_show(path):
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{SOURCE_COMMIT}:{path}"]).decode()


def source_paths():
    listing = subprocess.check_output(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", SOURCE_COMMIT, "--", "zh-cn"]).decode()
    return sorted(line for line in listing.splitlines() if line.endswith(".md"))
HAN = re.compile(r"[㐀-鿿]")
LATIN = re.compile(r"[A-Za-z]")
CAPTION_EN = re.compile(r"^(Figure|Example|Table)\s*(\d+[-.]\d+)\.?")
CAPTION_LABEL = {"Figure": "图", "Example": "例", "Table": "表"}
ATTRIBUTION = re.compile(r"^(?:—|--|——)\s*\S")
KICKER = re.compile(r"^[*\s]*CHAPTER[*\s]*\d+[*\s]*$")
CREDIT = re.compile(r"^\**\s*(Written|Edited) by\b")
CODE_LABEL = re.compile(r"^[\w./-]+\.\w+:$")
TRANSLATABLE = {"paragraph", "list", "quote", "table"}

# Text the interleaved source lacked. English comes from the official chapter HTML at abseil.io; the
# missing English heading and paragraph are supplied verbatim.
MISSING_ENGLISH = {
    "ch18": [("从根本上看，这似乎与基于任务的构建系统差别不大",
              "Fundamentally, it might not seem like what’s happening here is that much different than what happened when "
              "using a task-based build system. Indeed, the end result is the same binary, and the process for producing it "
              "involved analyzing a bunch of steps to find dependencies among them, and then running those steps in order. "
              "But there are critical differences. The first one appears in step 3: because Bazel knows that each target will "
              "only produce a Java library, it knows that all it has to do is run the Java compiler rather than an arbitrary "
              "user-defined script, so it knows that it’s safe to run these steps in parallel. This can produce an order of "
              "magnitude performance improvement over building targets one at a time on a multicore machine, and is only "
              "possible because the artifact-based approach leaves the build system in charge of its own execution strategy "
              "so that it can make stronger guarantees about parallelism.")],
}
HEADING_ENGLISH = {"有效静态分析的特点": "Characteristics of Effective Static Analysis"}


def language(text):
    text = re.sub(r"\[\^?\w+\^?\]", "", text or "")
    if HAN.search(text):
        return "zh"
    return "en" if LATIN.search(text) else "-"


def normalize(text):
    return " ".join((text or "").split())


def bilingual_heading(text):
    """Port of the reader's bilingualHeading(): split "English 中文" (any separator) or "中文 (English)"."""
    text = text.strip()
    match = HAN.search(text)
    if not match:
        return None
    first = match.start()
    if first == 0:
        wrapped = re.match(r"^(.+?)\s*[（(]([^()（）]*[A-Za-z][^()（）]*)[)）]$", text)
        if not wrapped or LATIN.search(wrapped[1]):
            return None
        return wrapped[2].strip(), wrapped[1].strip()
    english = text[:first]
    if not re.search(r"\s$", english):
        gap = re.search(r"\s{2,}", text)
        tail = re.search(r"\S+$", english)[0]
        head = english[:-len(tail)]
        word = re.match(r"^[A-Za-z0-9-]+", tail)
        if gap and 0 < gap.start() < first:
            english = text[:gap.start()]
        elif not word or re.search(r"\b" + re.escape(word[0]) + r"\b", head):
            english = head
    english = english.strip()
    if not LATIN.search(english):
        return None
    return english, text[len(english):].strip()


class Block:
    def __init__(self, kind, text, start, end, **extra):
        self.kind = kind          # heading, paragraph, list, table, quote, code, image, rule, html
        self.text = text          # raw markdown of the block
        self.start, self.end = start, end
        self.extra = extra

    @property
    def lang(self):
        return self.extra.get("force_lang") or language(self.plain)

    @property
    def plain(self):
        return self.extra.get("plain", self.text)

    def set_text(self, text):
        self.text = text
        self.extra["plain"] = raw_plain(text)

    def __repr__(self):
        return f"<{self.kind} L{self.start + 1} {self.lang} {normalize(self.plain)[:50]!r}>"


def inline_plain(tokens):
    parts = []
    for token in tokens or []:
        if token.type in {"text", "code_inline"}:
            parts.append(token.content)
        elif token.type in {"softbreak", "hardbreak"}:
            parts.append(" ")
    return "".join(parts)


def raw_plain(raw):
    """Plain text of a raw markdown block (footnote markers kept)."""
    raw = re.sub(r"^\s*>\s?", "", raw, flags=re.M)
    tokens = MD.parse(raw)
    return normalize(" ".join(inline_plain(t.children) for t in tokens if t.type == "inline"))


def parse_blocks(text):
    """Top-level blocks with raw text and line ranges."""
    lines = text.splitlines()
    tokens = MD.parse(text)
    blocks = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.level != 0 or token.nesting == -1:
            i += 1
            continue
        start, end = token.map
        raw = "\n".join(lines[start:end]).rstrip()
        if token.type == "heading_open":
            blocks.append(Block("heading", raw, start, end, level=int(token.tag[1]), plain=inline_plain(tokens[i + 1].children)))
        elif token.type == "paragraph_open":
            inline = tokens[i + 1]
            plain = inline_plain(inline.children)
            image = any(c.type == "image" for c in inline.children) and all(
                c.type in {"image", "softbreak", "hardbreak"} or (c.type == "text" and not c.content.strip()) for c in inline.children)
            blocks.append(Block("image" if image else "paragraph", raw, start, end, plain=plain))
        elif token.type in {"fence", "code_block"}:
            blocks.append(Block("code", raw, start, end, content=token.content, plain=""))
        elif token.type in {"bullet_list_open", "ordered_list_open"}:
            items = []
            j = i + 1
            while not (tokens[j].type in {"bullet_list_close", "ordered_list_close"} and tokens[j].level == 0):
                if tokens[j].type == "list_item_open" and tokens[j].level == 1:
                    s, e = tokens[j].map
                    k = j
                    plain = []
                    while not (tokens[k].type == "list_item_close" and tokens[k].level == 1):
                        if tokens[k].type == "inline":
                            plain.append(inline_plain(tokens[k].children))
                        k += 1
                    items.append({"raw": "\n".join(lines[s:e]).rstrip(), "plain": " ".join(plain), "start": s, "end": e})
                j += 1
            blocks.append(Block("list", raw, start, end, items=items, ordered=token.type == "ordered_list_open",
                                plain=" ".join(item["plain"] for item in items)))
        elif token.type == "blockquote_open":
            j = i + 1
            plain = []
            while not (tokens[j].type == "blockquote_close" and tokens[j].level == 0):
                if tokens[j].type == "inline":
                    plain.append(inline_plain(tokens[j].children))
                j += 1
            blocks.append(Block("quote", raw, start, end, plain=" ".join(plain)))
        elif token.type == "table_open":
            j = i + 1
            plain = []
            rows = 0
            while not (tokens[j].type == "table_close" and tokens[j].level == 0):
                rows += tokens[j].type == "tr_open"
                if tokens[j].type == "inline":
                    plain.append(inline_plain(tokens[j].children))
                j += 1
            blocks.append(Block("table", raw, start, end, rows=rows, plain=" ".join(plain)))
        elif token.type == "hr":
            blocks.append(Block("rule", raw, start, end, plain=""))
        elif token.type == "html_block":
            blocks.append(Block("html", raw, start, end, plain=""))
        i += 1
    return blocks


# ---------------------------------------------------------------------------------------------------------------
# Anchors inside raw markdown
# ---------------------------------------------------------------------------------------------------------------

def strip_marks(text):
    return normalize(re.sub(r"\[(?:\^\w+|\d+\^)\]", "", text or ""))


def find_anchor(raw, anchor):
    """Locate plain-text `anchor` inside raw markdown; return (start, end) or None.

    Emphasis, code spans, links and footnote markers may sit between the anchor's characters.
    """
    needle = normalize(anchor)
    if not needle:
        return None
    if needle in raw:
        start = raw.index(needle)
        return start, start + len(needle)
    between = r"(?:[*_`\[\]]|\]\([^)]*\)|\[\^?\w+\^?\]|\s)*"
    pattern = between.join(re.escape(ch) if ch != " " else r"\s" for ch in needle)
    match = re.search(pattern, raw)
    return (match.start(), match.end()) if match else None


def containing_blocks(blocks, text, lang):
    needle = strip_marks(text)
    return [b for b in blocks if b.kind in TRANSLATABLE and b.lang == lang and needle and needle in strip_marks(b.plain)]


def insert_after_anchor(blocks, anchor, marker, lang):
    hits = [b for b in blocks if b.kind in TRANSLATABLE and b.lang == lang and find_anchor(b.text, anchor)]
    if len(hits) != 1:
        return False
    start, end = find_anchor(hits[0].text, anchor)
    hits[0].set_text(hits[0].text[:end] + marker + hits[0].text[end:])
    return True


def replace_anchor(blocks, anchor, marker, lang):
    hits = [b for b in blocks if b.kind in TRANSLATABLE and b.lang == lang and find_anchor(b.text, anchor)]
    if len(hits) != 1:
        return False
    start, end = find_anchor(hits[0].text, anchor)
    hits[0].set_text(hits[0].text[:start] + marker + hits[0].text[end:])
    return True


def remove_markers(blocks, note_id, lang):
    for block in blocks:
        if block.lang == lang and block.kind in TRANSLATABLE:
            block.set_text(re.sub(r"\[\^" + note_id + r"\]", "", block.text))


# ---------------------------------------------------------------------------------------------------------------
# Review data
# ---------------------------------------------------------------------------------------------------------------

def load_review(key):
    try:
        return json.loads(git_show(f"assets/reader-content/{key}.json"))
    except subprocess.CalledProcessError:
        return {}


def legacy_footnotes(blocks):
    """ch01-style definitions inside blockquotes: `> [^n]: English` then `> [n] 中文`, `> n 中文` or a bare Chinese line."""
    notes = {}
    remaining = []
    for block in blocks:
        if block.kind != "quote":
            remaining.append(block)
            continue
        lines = [re.sub(r"^\s*(?:>\s*)+", "", line) for line in block.text.splitlines()]
        parsed, current, ok = {}, None, True
        for line in lines:
            if not line.strip():
                continue
            en = re.match(r"^\[\^?(\d+)\^?\]\s*:?\s*(.*)$", line)
            zh = re.match(r"^(?:\[(\d+)\]|(\d+))\s+(.*)$", line)
            if en and not HAN.search(line[:8]):
                current = en[1]
                parsed.setdefault(current, {"en": "", "zh": ""})
                parsed[current]["en"] = (parsed[current]["en"] + " " + en[2]).strip()
            elif zh and current and (zh[1] or zh[2]) == current and HAN.search(zh[3]):
                parsed[current]["zh"] = (parsed[current]["zh"] + " " + zh[3]).strip()
            elif current and HAN.search(line):
                parsed[current]["zh"] = (parsed[current]["zh"] + " " + line.strip()).strip()
            elif current and not parsed[current]["zh"]:
                parsed[current]["en"] += " " + line.strip()
            else:
                ok = False
        if parsed and ok and all(v["en"] and v["zh"] for v in parsed.values()):
            notes.update(parsed)
        else:
            remaining.append(block)
    return notes, remaining


def quote_lines(text):
    return "\n".join("> " + line if line.strip() else ">" for line in text.strip().splitlines())


def unquote(text):
    return re.sub(r"^\s*>\s?", "", text, flags=re.M).strip()


def prose_code_to_quotes(blocks, items, report, key):
    """Reviewed code blocks that are really quotations become blockquote blocks (English and Chinese halves)."""
    if not items:
        return blocks
    result = []
    for block in blocks:
        if block.kind != "code":
            result.append(block)
            continue
        content = block.extra["content"].strip()
        matched = [item for item in items if item["text"].strip() in content]
        if not matched:
            result.append(block)
            continue
        remaining = content
        for item in matched:
            remaining = remaining.replace(item["text"].strip(), "", 1)
            runs = []
            if item["language"] == "bilingual":
                for line in item["text"].splitlines():
                    if not line.strip():
                        continue
                    lang = "zh" if HAN.search(line) else "en"
                    if runs and runs[-1][0] == lang:
                        runs[-1][1].append(line)
                    else:
                        runs.append((lang, [line]))
            else:
                runs.append((item["language"], item["text"].strip().splitlines()))
            for _, run_lines in runs:
                text = "\n".join(run_lines).strip()
                result.append(Block("quote", quote_lines(text), block.start, block.end, plain=raw_plain(text), quotation=True))
        if remaining.strip():
            report.append(f"{key}: prose code block partially reviewed L{block.start + 1}: {remaining.strip()[:60]}")
    return result


def epigraph_pair(english, chinese, author, start, end):
    text, sep, en_author = english.strip().partition(" --")
    if not sep:
        text, sep, en_author = english.strip().partition(" —")
    text = text.strip().strip("*").strip()
    en = f"> *{text}*\n>\n> — {(en_author or author).strip()}"
    zh = f"> {chinese.strip()}\n>\n> — {author.strip()}"
    return (Block("quote", en, start, end, plain=raw_plain(en), epigraph=True),
            Block("quote", zh, start, end, plain=raw_plain(zh), epigraph=True))


def credit_chinese(text):
    text = normalize(text.replace("*", ""))
    zh = re.sub(r"(?:^|\s)Edited by\s*", "；编辑：", re.sub(r"^Written by\s*", "作者：", text))
    return "**" + re.sub(r"^；", "", zh) + "**"


def emphasis_wrapper(raw):
    raw = raw.strip()
    if re.fullmatch(r"\*\*.+\*\*", raw):
        return "**"
    if re.fullmatch(r"\*[^*].*\*", raw):
        return "*"
    return ""


def split_caption(block):
    """`*Figure 1-2. Text*  *图1-2：文字*` -> (english or None, chinese)."""
    text = normalize(block.plain).strip("* ")
    english = CAPTION_EN.match(text)
    if not english or not HAN.search(text):
        return None
    first = HAN.search(text).start()
    prefix = text[:first].strip().rstrip("* ").strip()
    translated = text[first:].strip().rstrip("* ").strip()
    if not re.match(r"^[图表例]\s*\d", translated):
        repeated = re.compile(re.escape(english[1]) + r"\s*" + re.escape(english[2]) + r"\.?\s*$")
        prefix = repeated.sub("", prefix).strip()
        translated = CAPTION_LABEL[english[1]] + english[2] + " " + translated
    return (prefix or None), translated


# ---------------------------------------------------------------------------------------------------------------
# Pairing
# ---------------------------------------------------------------------------------------------------------------

class Unit:
    def __init__(self, kind, en=None, zh=None, **extra):
        self.kind, self.en, self.zh, self.extra = kind, en, zh, extra

    def __repr__(self):
        return f"<Unit {self.kind} en={normalize(self.en or '')[:40]!r} zh={normalize(self.zh or '')[:30]!r}>"


def code_key(text):
    body = "\n".join(line.strip() for line in text.splitlines() if not line.strip().startswith("```"))
    return re.sub(r"\s+", "", re.sub(r"^\s*\$\s*", "", body, flags=re.M)).rstrip(".。;")


def compatible(en, zh):
    if en.kind == zh.kind:
        return en.kind != "list" or len(en.extra["items"]) == len(zh.extra["items"])
    return {en.kind, zh.kind} == {"paragraph", "quote"}


def as_kind(block, kind):
    """Re-express a paragraph as a quote or a quote as a paragraph so a pair shares one kind."""
    if block.kind == kind:
        return block.text
    return quote_lines(block.text) if kind == "quote" else unquote(block.text)


def expand(blocks):
    """Lists and blockquotes that hold both languages become two blocks."""
    result = []
    for block in blocks:
        if block.kind == "list":
            items = block.extra["items"]
            langs = [language(item["plain"]) for item in items]
            en_items = [it for it, l in zip(items, langs) if l != "zh"]
            zh_items = [it for it, l in zip(items, langs) if l == "zh"]
            if en_items and zh_items and langs == [l for l in langs if l != "zh"] + ["zh"] * len(zh_items):
                for its in (en_items, zh_items):
                    result.append(Block("list", "\n".join(i["raw"] for i in its), its[0]["start"], its[-1]["end"],
                                        items=its, ordered=block.extra["ordered"], plain=" ".join(i["plain"] for i in its)))
                continue
        if block.kind == "quote" and not block.extra.get("quotation"):
            parts = [p for p in re.split(r"\n\s*>\s*\n", block.text) if p.strip()]
            langs = [language(raw_plain(p)) for p in parts]
            if "en" in langs and "zh" in langs:
                runs = []
                for part, lang in zip(parts, langs):
                    if runs and runs[-1][0] == lang:
                        runs[-1][1].append(part)
                    else:
                        runs.append((lang, [part]))
                for _, run in runs:
                    text = "\n>\n".join(run)
                    result.append(Block("quote", text, block.start, block.end, plain=raw_plain(text)))
                continue
        result.append(block)
    return result


def pair_blocks(blocks, report, hints, key):
    """Turn the interleaved block list into ordered units. Source-only blocks follow the pair they interrupt."""
    blocks = expand(blocks)
    forced = {}
    for english, chinese in hints:
        en = containing_blocks(blocks, english, "en")
        zh = containing_blocks(blocks, chinese, "zh")
        if len(en) == 1 and len(zh) == 1:
            forced[id(en[0])] = zh[0]
        else:
            report.append(f"{key}: hint not matched ({len(en)} en, {len(zh)} zh): {normalize(english)[:60]}")
    forced_targets = {id(z) for z in forced.values()}
    order = {id(b): idx for idx, b in enumerate(blocks)}

    units, pending = [], []

    def flush():
        # The translation sometimes repeats a code block after the Chinese paragraph; keep one copy per group.
        seen_code = set()
        for block in pending:
            if block.kind == "code":
                digest = code_key(block.text)
                if digest in seen_code:
                    continue
                seen_code.add(digest)
            units.append(Unit(block.kind, en=block.text))
        pending.clear()

    def emit(en_block, zh_block):
        kind = en_block.kind if en_block.kind != "paragraph" or zh_block.kind == "paragraph" else zh_block.kind
        if en_block.extra.get("quotation") or zh_block.extra.get("quotation"):
            kind = "quote"
        units.append(Unit(kind, en=as_kind(en_block, kind), zh=as_kind(zh_block, kind), en_block=en_block, zh_block=zh_block))

    i, n = 0, len(blocks)
    while i < n:
        block = blocks[i]
        if block.kind == "heading":
            flush()
            units.append(Unit("heading", en=block.plain.strip(), zh=block.extra.get("zh"), level=block.extra["level"]))
            i += 1
            continue
        if block.kind not in TRANSLATABLE or block.extra.get("source_only"):
            pending.append(block)
            i += 1
            continue
        if block.extra.get("credit"):
            flush()
            units.append(Unit("paragraph", en=block.text, zh=credit_chinese(block.plain), en_block=block))
            i += 1
            continue
        if id(block) in forced_targets:
            i += 1
            continue
        if block.lang != "en":
            flush()
            if not (block.kind == "quote" and block.lang == "zh"):
                report.append(f"{key}: unpaired {block.lang} {block.kind} L{block.start + 1}: {normalize(block.plain)[:70]}")
            units.append(Unit(block.kind, zh=block.text) if block.lang == "zh" else Unit(block.kind, en=block.text))
            i += 1
            continue
        en_run, j = [], i
        while j < n and blocks[j].kind != "heading":
            b = blocks[j]
            if b.kind in TRANSLATABLE and not b.extra.get("source_only"):
                if b.lang == "en" and id(b) not in forced_targets and not b.extra.get("credit"):
                    en_run.append(b)
                else:
                    break
            else:
                pending.append(b)
            j += 1
        free_en = [b for b in en_run if id(b) not in forced]
        zh_run, k = [], j
        while k < n and blocks[k].kind != "heading" and len(zh_run) < len(free_en):
            b = blocks[k]
            if b.kind in TRANSLATABLE and not b.extra.get("source_only"):
                if b.lang == "zh":
                    if id(b) not in forced_targets:
                        zh_run.append(b)
                else:
                    break
            else:
                pending.append(b)
            k += 1
        # An attribution or byline the translation left out keeps the same text in Chinese.
        if len(free_en) == len(zh_run) + 1:
            for position, b in enumerate(free_en):
                plain = normalize(b.plain)
                byline = emphasis_wrapper(b.text) and len(plain.split()) <= 4 and not re.search(r"[.!?:,]", plain)
                if b.kind != "paragraph" or not (ATTRIBUTION.match(plain) or byline):
                    continue
                trial = zh_run[:position] + [Block("paragraph", b.text, b.start, b.end, plain=b.plain, force_lang="zh")] + zh_run[position:]
                if all(compatible(a, z) for a, z in zip(free_en, trial)):
                    zh_run = trial
                    break
        pairs = [(b, forced[id(b)]) for b in en_run if id(b) in forced]
        if len(free_en) == len(zh_run) and all(compatible(a, z) for a, z in zip(free_en, zh_run)):
            pairs.extend(zip(free_en, zh_run))
        else:
            for b in free_en:
                report.append(f"{key}: unpaired en {b.kind} L{b.start + 1}: {normalize(b.plain)[:70]}")
                pairs.append((b, None))
            for z in zh_run:
                report.append(f"{key}: unpaired zh {z.kind} L{z.start + 1}: {normalize(z.plain)[:70]}")
        pairs.sort(key=lambda p: order.get(id(p[0]), 0))
        for en_block, zh_block in pairs:
            if zh_block is None:
                units.append(Unit(en_block.kind, en=en_block.text, en_block=en_block))
            else:
                emit(en_block, zh_block)
        for z in zh_run:
            if not any(z is p[1] for p in pairs):
                units.append(Unit(z.kind, zh=z.text))
        flush()
        i = k
    flush()
    return units


# ---------------------------------------------------------------------------------------------------------------
# Chapter driver
# ---------------------------------------------------------------------------------------------------------------

def chapter_key(path):
    number = re.search(r"Chapter-(\d+)_", str(path))
    return f"ch{int(number[1]):02d}" if number else Path(path).stem.lower()


def normalize_markers(text):
    return re.sub(r"\[(\d+)\^\]", r"[^\1]", text)


def split_attribution(block):
    """`Quote text. —Author` written on one line becomes a text block and an attribution block."""
    plain = normalize(block.plain)
    match = re.match(r"^(.*?[.!?。！？”\"*])\s+(—|--|——)\s*([^—]{1,50})$", plain)
    if not match or HAN.search(plain):
        return None
    text = match[1].strip()
    text = f"*{text.strip('*').strip()}*" if "*" in block.text else text
    return (Block("paragraph", text, block.start, block.end, plain=raw_plain(text), epigraph=True),
            Block("paragraph", f"— {match[3].strip()}", block.start, block.end, plain=f"— {match[3].strip()}"))


def prepare_blocks(blocks, key, report):
    """Drop the kicker; split combined headings, captions, run-in labels and bilingual subheadings; mark credits."""
    shift = 1 if key in {"foreword", "preface"} else 0
    prepared = []
    idx = 0
    seen_h2 = False
    while idx < len(blocks):
        block = blocks[idx]
        nxt = blocks[idx + 1] if idx + 1 < len(blocks) else None
        plain = normalize(block.plain)
        if block.kind in {"quote", "paragraph"} and not plain:
            idx += 1
            continue
        if block.kind == "paragraph" and KICKER.match(plain):
            idx += 1
            continue
        if block.kind == "heading":
            level = max(1, block.extra["level"] - shift)
            seen_h2 = seen_h2 or level >= 2
            if block.lang == "en" and nxt and nxt.kind == "heading" and nxt.lang == "zh" and nxt.extra["level"] == block.extra["level"]:
                prepared.append(Block("heading", block.plain.strip(), block.start, block.end, level=level, zh=nxt.plain.strip(), plain=block.plain))
                idx += 2
                continue
            parts = bilingual_heading(block.plain)
            if parts:
                prepared.append(Block("heading", parts[0], block.start, block.end, level=level, zh=parts[1], plain=parts[0]))
            elif block.lang == "zh" and key == "afterword" and level == 1:
                prepared.append(Block("heading", "Afterword", block.start, block.end, level=1, zh=block.plain.strip(), plain="Afterword"))
            elif block.lang == "zh" and plain in HEADING_ENGLISH:
                report.append(f"{key}: supplied English heading from the official text: {plain}")
                prepared.append(Block("heading", HEADING_ENGLISH[plain], block.start, block.end, level=level, zh=plain, plain=HEADING_ENGLISH[plain]))
            elif not HAN.search(plain):
                # names such as C++ or Boost read the same in both languages
                prepared.append(Block("heading", plain, block.start, block.end, level=level, zh=plain, plain=plain))
            else:
                report.append(f"{key}: heading without pair L{block.start + 1}: {plain[:60]}")
                prepared.append(Block("heading", plain, block.start, block.end, level=level, zh=None, plain=plain))
            idx += 1
            continue
        if block.kind == "paragraph" and CREDIT.match(plain):
            continued = nxt if (nxt and nxt.kind == "paragraph" and emphasis_wrapper(nxt.text) and " Edited by " in normalize(nxt.plain)
                                and not CREDIT.match(normalize(nxt.plain))) else None
            if continued:
                # "**Written by A**" + "**B Edited by C**" -> "**Written by A, B**" + "**Edited by C**"
                more, _, editor = normalize(continued.plain).replace("*", "").partition(" Edited by ")
                first = Block("paragraph", f"**{plain.replace('*', '').strip()}, {more.strip()}**", block.start, block.end,
                              plain=f"{plain.replace('*', '').strip()}, {more.strip()}", credit=True)
                second = Block("paragraph", f"**Edited by {editor.strip()}**", continued.start, continued.end, plain=f"Edited by {editor.strip()}", credit=True)
                prepared.extend([first, second])
                idx += 2
                continue
            block.extra["credit"] = True
            prepared.append(block)
            idx += 1
            continue
        if block.kind == "paragraph" and block.lang == "en" and CODE_LABEL.match(plain) and nxt and nxt.kind == "code":
            block.extra["source_only"] = True
            prepared.append(block)
            idx += 1
            continue
        if block.kind == "paragraph" and block.lang == "en" and not seen_h2 and split_attribution(block):
            prepared.extend(split_attribution(block))
            idx += 1
            continue
        if block.kind == "paragraph" and block.lang == "zh" and CAPTION_EN.match(plain.strip("* ")):
            split = split_caption(block)
            if split:
                en_text, zh_text = split
                if en_text:
                    prepared.append(Block("paragraph", f"*{en_text}*", block.start, block.end, plain=en_text, caption=True))
                prepared.append(Block("paragraph", f"*{zh_text}*", block.start, block.end, plain=zh_text, caption=True))
                idx += 1
                continue
        if block.kind == "paragraph" and block.lang == "zh" and LATIN.search(plain):
            raw_lines = [l for l in block.text.strip().splitlines() if l.strip()]
            line_langs = [language(raw_plain(l)) for l in raw_lines]
            if len(raw_lines) > 1 and "zh" in line_langs and line_langs == ["en"] * line_langs.index("zh") + ["zh"] * (len(raw_lines) - line_langs.index("zh")) and line_langs[0] == "en":
                # English line(s) then Chinese line(s) inside one paragraph
                cut = line_langs.index("zh")
                en_text, zh_text = "\n".join(raw_lines[:cut]).strip(), "\n".join(raw_lines[cut:]).strip()
                prepared.append(Block("paragraph", en_text, block.start, block.end, plain=raw_plain(en_text)))
                prepared.append(Block("paragraph", zh_text, block.start, block.end, plain=raw_plain(zh_text)))
                idx += 1
                continue
            first = raw_lines[0].rstrip()
            wrapper = emphasis_wrapper(first)
            label = normalize(first.replace("*", ""))
            parts = bilingual_heading(label) if not HAN.search(first[:1]) else None
            rest = "\n".join(raw_lines[1:]).strip()
            prose = parts and (re.search(r"[。！？，；]", parts[1]) or parts[1].endswith("："))
            if parts and not prose and len(raw_lines) == 1 and len(plain) < (160 if wrapper else 120):
                prepared.append(Block("paragraph", f"{wrapper}{parts[0]}{wrapper}", block.start, block.end, plain=parts[0], subheading=True))
                prepared.append(Block("paragraph", f"{wrapper}{parts[1]}{wrapper}", block.start, block.end, plain=parts[1], subheading=True))
                idx += 1
                continue
            if parts and not prose and rest and not HAN.search(rest):
                en_text = f"{wrapper}{parts[0]}{wrapper}  \n{rest}"
                zh_label = f"{wrapper}{parts[1]}{wrapper}"
                prepared.append(Block("paragraph", en_text, block.start, block.end, plain=raw_plain(en_text)))
                if nxt and nxt.kind == "paragraph" and nxt.lang == "zh":
                    nxt.set_text(f"{zh_label}  \n{nxt.text.strip()}")
                else:
                    zh_text = f"{zh_label}  \n{rest}"
                    prepared.append(Block("paragraph", zh_text, block.start, block.end, plain=raw_plain(zh_text)))
                idx += 1
                continue
        prepared.append(block)
        idx += 1
    return prepared


def detach_list_lines(blocks, report, key):
    """A paragraph whose later line starts a numbered step ("4. Test ...") is a paragraph plus a one-item list."""
    result = []
    for block in blocks:
        lines = block.text.strip().splitlines() if block.kind == "paragraph" else []
        cut = next((i for i, l in enumerate(lines) if i and re.match(r"^\s*\d+\.\s", l)), None)
        if cut is None:
            result.append(block)
            continue
        head = "\n".join(lines[:cut]).strip()
        tail = "\n".join(lines[cut:]).strip()
        result.append(Block("paragraph", head, block.start, block.end, plain=raw_plain(head)))
        result.extend(parse_blocks(tail))
        report.append(f"{key}: detached numbered step from paragraph L{block.start + 1}: {tail[:40]}")
    return result


def split_multiline_paragraph(blocks, report, key):
    """An English paragraph written as N lines followed by N Chinese paragraphs is N source paragraphs."""
    result = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block.kind == "paragraph" and block.lang == "en" and "\n" in block.text.strip():
            lines = [l for l in block.text.strip().splitlines() if l.strip()]
            following = []
            j = i + 1
            while j < len(blocks) and blocks[j].kind == "paragraph" and blocks[j].lang == "zh" and len(following) < len(lines):
                following.append(blocks[j])
                j += 1
            sentences = all(re.search(r"[.?!:”\"]\s*$", l) for l in lines)
            if len(lines) > 1 and sentences and len(following) == len(lines) and (j >= len(blocks) or blocks[j].lang != "zh"):
                report.append(f"{key}: split {len(lines)}-line English paragraph L{block.start + 1} to match {len(lines)} Chinese paragraphs")
                for line in lines:
                    text = line.strip()
                    result.append(Block("paragraph", text, block.start, block.end, plain=raw_plain(text)))
                i += 1
                continue
        result.append(block)
        i += 1
    return result


def migrate_chapter(path, report):
    """`path` is the chapter's repository path (zh-cn/...md) inside SOURCE_COMMIT."""
    key = chapter_key(path)
    review = load_review(key)
    text = normalize_markers(re.sub(r"\[\d+\]\(#_bookmark\d+\)", "", git_show(path)))
    lines = text.splitlines()
    footnotes = {}
    if review.get("format") == 2:
        drop = set()
        for note in review.get("footnotes", []):
            start, end = note["definitionLines"]
            drop.update(range(start - 1, end))
            footnotes[str(note["id"])] = {"en": note["english"].strip(), "zh": note["chinese"].strip(), "after": note.get("after"),
                                          "englishAfter": note.get("englishAfter"), "relocateEnglish": note.get("relocateEnglish"),
                                          "relocateChinese": note.get("relocateChinese")}
        lines = ["" if i in drop else line for i, line in enumerate(lines)]
        text = "\n".join(lines)
    for edit in review.get("textEdits", []):
        if text.count(edit["source"]) != 1 and not (text.count(edit["source"]) == 0 and edit["replacement"] in text):
            report.append(f"{key}: text edit source not unique: {edit['source'][:50]}")
        text = text.replace(edit["source"], edit["replacement"])
    blocks = parse_blocks(text)
    if review.get("format") != 2:
        legacy, blocks = legacy_footnotes(blocks)
        for note_id, body in legacy.items():
            footnotes[note_id] = {"en": body["en"], "zh": body["zh"], "after": None, "englishAfter": None}
        for note in review.get("footnotes", []):
            if str(note["id"]) in footnotes:
                footnotes[str(note["id"])]["after"] = note.get("after")
                footnotes[str(note["id"])]["englishAfter"] = note.get("englishAfter")
    blocks = prose_code_to_quotes(blocks, review.get("proseCodeBlocks", []), report, key)
    # translator notes stored as code blocks or whole blockquotes are removed here and attached to a Chinese block later
    translator_notes = list(review.get("translatorNotes", []))
    block_notes = {}
    remaining = []
    for block in blocks:
        matched = None
        for idx, item in enumerate(translator_notes):
            if block.kind == "code" and item["text"].strip() == block.extra["content"].strip():
                matched = idx
            elif block.kind == "quote" and strip_marks(block.plain) == strip_marks(raw_plain(item["text"])):
                matched = idx
        if matched is not None:
            block_notes[matched] = len(remaining)
            continue
        remaining.append(block)
    blocks = prepare_blocks(remaining, key, report)
    hints = []
    for anchor, english in MISSING_ENGLISH.get(key, []):
        hits = [b for b in blocks if b.kind == "paragraph" and b.lang == "zh" and strip_marks(b.plain).startswith(anchor)]
        if len(hits) == 1:
            blocks.insert(blocks.index(hits[0]), Block("paragraph", english, hits[0].start, hits[0].end, plain=english))
            report.append(f"{key}: inserted English paragraph from the official text: {english[:50]}")
        else:
            report.append(f"{key}: missing-English anchor not found: {anchor}")
    inserted = []
    for item in review.get("translations", []):
        if item.get("kind") == "heading":
            continue
        en = containing_blocks(blocks, item["english"], "en")
        if len(en) != 1:
            report.append(f"{key}: reviewed translation source not found ({len(en)}): {item['english'][:60]}")
            continue
        existing = [b for b in blocks if b.kind in TRANSLATABLE and b.lang == "zh" and strip_marks(b.plain) == strip_marks(raw_plain(item["chinese"]))]
        if existing and item.get("kind") != "epigraph":
            hints.append((item["english"], item["chinese"]))
            continue
        zh_block = Block("paragraph", item["chinese"].strip(), en[0].start, en[0].end, plain=raw_plain(item["chinese"]))
        inserted.append((en[0], [zh_block]))
        if item.get("kind") == "epigraph":
            en[0].extra["epigraph"] = True
            zh_block.extra["epigraph"] = True
            pos = blocks.index(en[0])
            nxt = blocks[pos + 1] if pos + 1 < len(blocks) else None
            author = item.get("author")
            if author:
                zh_author = Block("paragraph", f"— {author}", en[0].start, en[0].end, plain=f"— {author}", force_lang="zh")
                if nxt and nxt.kind == "paragraph" and ATTRIBUTION.match(normalize(nxt.plain)):
                    inserted.append((nxt, [zh_author]))
                else:
                    inserted[-1][1].append(zh_author)
    for en_block, zh_blocks in inserted:
        pos = blocks.index(en_block)
        blocks[pos + 1:pos + 1] = zh_blocks
    if review.get("epigraph"):
        epi = review["epigraph"]
        english = epi["english"].split(" --")[0].strip().strip("*")
        hits = [b for b in blocks if b.kind == "paragraph" and b.lang == "en" and find_anchor(b.text, english)]
        if len(hits) == 1:
            pos = blocks.index(hits[0])
            author_en = epi["english"].partition(" --")[2].strip() or epi.get("author", "")
            author_zh = epi.get("author") or author_en
            hits[0].set_text(f"*{english}*")
            hits[0].extra["epigraph"] = True
            zh_text = Block("paragraph", epi["chinese"].strip(), hits[0].start, hits[0].end, plain=epi["chinese"].strip(), epigraph=True)
            zh_author = Block("paragraph", f"— {author_zh}", hits[0].start, hits[0].end, plain=f"— {author_zh}", force_lang="zh")
            nxt = blocks[pos + 1] if pos + 1 < len(blocks) else None
            if nxt and nxt.kind == "paragraph" and ATTRIBUTION.match(normalize(nxt.plain)):
                blocks[pos + 1:pos + 2] = [zh_text, nxt, zh_author]
            else:
                en_author = Block("paragraph", f"— {author_en}", hits[0].start, hits[0].end, plain=f"— {author_en}")
                blocks[pos + 1:pos + 1] = [zh_text, en_author, zh_author]
        else:
            report.append(f"{key}: epigraph source not found")
    for pair in review.get("pairedSources", []):
        hints.append((pair["english"], pair["chinese"]))
    tables = [b for b in blocks if b.kind == "table"]
    for pair in review.get("pairedTables", []):
        hints.append((tables[pair["englishIndex"]].plain, tables[pair["chineseIndex"]].plain))
    blocks = split_multiline_paragraph(detach_list_lines(blocks, report, key), report, key)
    # footnote references: relocate or add at reviewed anchors
    for note_id, note in footnotes.items():
        for lang, anchor_key, relocate_key in (("en", "englishAfter", "relocateEnglish"), ("zh", "after", "relocateChinese")):
            if note.get(relocate_key):
                remove_markers(blocks, note_id, lang)
            if any(b.lang == lang and b.kind in TRANSLATABLE and re.search(r"\[\^" + note_id + r"\]", b.text) for b in blocks):
                continue
            anchor = note.get(anchor_key)
            if anchor and insert_after_anchor(blocks, anchor, f"[^{note_id}]", lang):
                continue
            report.append(f"{key}: footnote {note_id} has no {lang} reference" + (f" (anchor: {anchor[:40]})" if anchor else ""))
    # translator notes
    note_defs = []

    def attach(position, marker):
        target = next((b for b in reversed(blocks[:position]) if b.lang == "zh" and b.kind in TRANSLATABLE), None)
        if target is None:
            target = next((b for b in blocks[position:] if b.lang == "zh" and b.kind in TRANSLATABLE), None)
        if target is None:
            return False
        target.set_text(target.text.rstrip() + marker)
        return True

    for number, item in enumerate(translator_notes, 1):
        marker = f"[^t{number}]"
        title = item.get("title") or "译者注"
        body = normalize(item.get("body", ""))
        link = f" [{item.get('linkText') or '参考来源'}]({item['href']})" if item.get("href") else ""
        note_defs.append(f"[^t{number}]: **{title}** {body}{link}".rstrip())
        if number - 1 in block_notes:
            if not attach(block_notes[number - 1], marker):
                report.append(f"{key}: translator note {number} has no Chinese block to attach to")
            continue
        anchor = raw_plain(item["text"])
        if not replace_anchor(blocks, anchor, marker, "zh"):
            report.append(f"{key}: translator note {number} anchor not found: {anchor[:50]}")
    units = pair_blocks(blocks, report, hints, key)
    kept = []
    for idx, unit in enumerate(units):
        if unit.kind == "quote" and unit.en is None and unit.zh:
            body = re.sub(r"^译者注[：:]\s*", "", unquote(unit.zh))
            number = len(note_defs) + 1
            note_defs.append(f"[^t{number}]: **译者注** {normalize(body)}")
            target = next((u for u in reversed(kept) if u.zh and u.kind in TRANSLATABLE), None) or \
                next((u for u in units[idx + 1:] if u.zh and u.kind in TRANSLATABLE), None)
            if target is None:
                report.append(f"{key}: Chinese-only quotation has no block to attach to: {body[:40]}")
            else:
                target.zh = target.zh.rstrip() + f"[^t{number}]"
                report.append(f"{key}: Chinese-only quotation became translator note {number}")
            continue
        kept.append(unit)
    units = kept
    return key, units, footnotes, note_defs


def write_chapter(path, out_root, units, footnotes, note_defs):
    relative = Path(path).relative_to("zh-cn")
    en_lines, zh_lines = [], []
    for unit in units:
        if unit.kind == "heading":
            en_lines.append("#" * unit.extra["level"] + " " + unit.en.strip())
            zh_lines.append("#" * unit.extra["level"] + " " + (unit.zh or unit.en).strip())
            continue
        if unit.en is not None:
            en_lines.append(unit.en.strip("\n"))
        if unit.zh is not None:
            zh_lines.append(unit.zh.strip("\n"))
    for note_id in sorted(footnotes, key=int):
        en_lines.append(f"[^{note_id}]: {normalize(footnotes[note_id]['en'])}")
        zh_lines.append(f"[^{note_id}]: {normalize(footnotes[note_id]['zh'])}")
    zh_lines.extend(note_defs)
    for folder, content in (("en", en_lines), ("zh-cn", zh_lines)):
        target = out_root / folder / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n\n".join(content).rstrip() + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / ".cache" / "split"))
    parser.add_argument("--only", default=None)
    args = parser.parse_args()
    out_root = Path(args.out)
    report, summary = [], []
    for path in source_paths():
        if args.only and args.only not in path:
            continue
        key, units, footnotes, note_defs = migrate_chapter(path, report)
        write_chapter(path, out_root, units, footnotes, note_defs)
        pairs = sum(1 for u in units if u.en and u.zh)
        en_only = sum(1 for u in units if u.kind in TRANSLATABLE and u.en and not u.zh)
        zh_only = sum(1 for u in units if u.en is None)
        summary.append(f"{key}: units {len(units)}, pairs {pairs}, en-only {en_only}, zh-only {zh_only}, footnotes {len(footnotes)}, notes {len(note_defs)}")
    print("\n".join(summary))
    print(f"\n{len(report)} report lines")
    (out_root / "report.txt").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
