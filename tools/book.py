"""The bilingual book as data: English sources in en/, translations in zh-cn/, aligned block by block.

Each chapter is a pair of Markdown files with the same block structure. Every translatable source block
(heading, paragraph, list, blockquote, table) has exactly one translation block at the same position; code,
images and rules belong to the source only. Footnotes are `[^n]:` definitions matched by id; `[^tN]:`
definitions in the translation are translator notes. `compile_chapter` turns a pair into the ordered units
the reader renders, and raises ValueError with the offending block when the two files disagree.
"""

import hashlib
import html
import re

from markdown_it import MarkdownIt

PARSE = MarkdownIt("commonmark").enable("table")
RENDER = MarkdownIt("commonmark", {"html": True}).enable("table")
HAN = re.compile(r"[㐀-鿿]")
TRANSLATABLE = {"heading", "paragraph", "list", "quote", "table"}
FOOTNOTE = re.compile(r"^\[\^(\w+)\]:\s*(.*)$")
MARKER = re.compile(r"\[\^(\w+)\]")
CAPTION = re.compile(r"^\**(Figure|Example|Table)\s*\d+[-.]\d+")
CREDIT = re.compile(r"^\**\s*(Written|Edited) by\b")
ATTRIBUTION = re.compile(r"^(?:—|--|——)\s*\S")
CODE_LABEL = re.compile(r"^[\w./-]+\.\w+:$")
PRISM_ALIASES = {"c++": "cpp", "golang": "go", "sh": "bash", "shell": "bash"}


def normalize(text):
    return " ".join((text or "").split())


def inline_plain(tokens):
    parts = []
    for token in tokens or []:
        if token.type in {"text", "code_inline"}:
            parts.append(token.content)
        elif token.type in {"softbreak", "hardbreak"}:
            parts.append(" ")
    return "".join(parts)


class Block:
    def __init__(self, kind, raw, line, **extra):
        self.kind, self.raw, self.line, self.extra = kind, raw, line, extra

    @property
    def plain(self):
        return self.extra.get("plain", "")

    def __repr__(self):
        return f"<{self.kind} line {self.line}: {normalize(self.plain)[:60]!r}>"


def parse(text):
    """Split a chapter file into (blocks, footnotes). Footnote definitions are single lines anywhere in the file."""
    footnotes = {}
    body = []
    for line in text.splitlines():
        match = FOOTNOTE.match(line)
        if match:
            footnotes[match[1]] = match[2].strip()
        else:
            body.append(line)
    text = "\n".join(body)
    lines = text.splitlines()
    tokens = PARSE.parse(text)
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
            blocks.append(Block("heading", raw, start + 1, level=int(token.tag[1]), plain=inline_plain(tokens[i + 1].children),
                                markdown=tokens[i + 1].content))
        elif token.type == "paragraph_open":
            inline = tokens[i + 1]
            image = any(c.type == "image" for c in inline.children) and all(
                c.type in {"image", "softbreak", "hardbreak"} or (c.type == "text" and not c.content.strip()) for c in inline.children)
            blocks.append(Block("image" if image else "paragraph", raw, start + 1, plain=inline_plain(inline.children)))
        elif token.type in {"fence", "code_block"}:
            blocks.append(Block("code", raw, start + 1, content=token.content, info=(token.info or "").strip().lower()))
        elif token.type in {"bullet_list_open", "ordered_list_open"}:
            items = 0
            j = i + 1
            plain = []
            while not (tokens[j].type in {"bullet_list_close", "ordered_list_close"} and tokens[j].level == 0):
                items += tokens[j].type == "list_item_open" and tokens[j].level == 1
                if tokens[j].type == "inline":
                    plain.append(inline_plain(tokens[j].children))
                j += 1
            blocks.append(Block("list", raw, start + 1, items=items, plain=" ".join(plain)))
        elif token.type == "blockquote_open":
            j = i + 1
            plain = []
            paragraphs = 0
            while not (tokens[j].type == "blockquote_close" and tokens[j].level == 0):
                paragraphs += tokens[j].type == "paragraph_open" and tokens[j].level == 1
                if tokens[j].type == "inline":
                    plain.append(inline_plain(tokens[j].children))
                j += 1
            blocks.append(Block("quote", raw, start + 1, paragraphs=paragraphs, plain=" ".join(plain)))
        elif token.type == "table_open":
            j = i + 1
            rows = 0
            plain = []
            while not (tokens[j].type == "table_close" and tokens[j].level == 0):
                rows += tokens[j].type == "tr_open"
                if tokens[j].type == "inline":
                    plain.append(inline_plain(tokens[j].children))
                j += 1
            blocks.append(Block("table", raw, start + 1, rows=rows, plain=" ".join(plain)))
        elif token.type == "hr":
            blocks.append(Block("rule", raw, start + 1))
        elif token.type == "html_block":
            blocks.append(Block("html", raw, start + 1))
        i += 1
    return blocks, footnotes


def shape(block):
    """The structural signature both languages must share."""
    if block.kind == "heading":
        return ("heading", block.extra["level"])
    if block.kind == "list":
        return ("list", block.extra["items"])
    if block.kind == "table":
        return ("table", block.extra["rows"])
    return (block.kind,)


def align(source_blocks, target_blocks, key):
    """Pair every translatable source block with the next translation block; source-only blocks pass through."""
    pairs = []
    targets = iter(target_blocks)
    remaining = list(target_blocks)
    for block in source_blocks:
        translatable = block.kind in TRANSLATABLE and not (block.kind == "paragraph" and CODE_LABEL.match(normalize(block.plain)))
        if not translatable:
            pairs.append((block, None))
            continue
        if not remaining:
            raise ValueError(f"{key}: translation missing for {block}")
        target = remaining.pop(0)
        if shape(block) != shape(target):
            raise ValueError(f"{key}: structure differs at {block} vs translation {target}")
        if not HAN.search(target.plain) and HAN.search(block.plain):
            raise ValueError(f"{key}: languages swapped at {block}")
        pairs.append((block, target))
    if remaining:
        raise ValueError(f"{key}: translation has extra blocks starting with {remaining[0]}")
    return pairs


def slugify(text, used):
    slug = re.sub(r"[^a-z0-9一-鿿]+", "-", text.lower()).strip("-") or "section"
    candidate, n = slug, 1
    while candidate in used:
        n += 1
        candidate = f"{slug}-{n}"
    used.add(candidate)
    return candidate


def unit_id(key, text, used):
    digest = hashlib.sha1(normalize(text).encode()).hexdigest()[:8]
    candidate, n = f"{key}.{digest}", 1
    while candidate in used:
        n += 1
        candidate = f"{key}.{digest}-{n}"
    used.add(candidate)
    return candidate


def note_button(note_id, language):
    label = "译者注" if note_id.startswith("t") else f"注释 {note_id}"
    mark = "注" if note_id.startswith("t") else html.escape(note_id)
    return (f'<span class="note-reference"><button type="button" class="note-trigger" data-note="{html.escape(note_id)}" '
            f'data-note-language="{language}" data-note-label="{label}" aria-label="查看{label}" aria-haspopup="dialog" '
            f'aria-controls="reader-note-popover" aria-expanded="false"><span class="note-mark" aria-hidden="true">{mark}</span></button></span>')


def with_notes(rendered, language):
    """Footnote markers outside code become popover triggers."""
    parts = re.split(r"(<code[\s\S]*?</code>)", rendered)
    return "".join(part if part.startswith("<code") else MARKER.sub(lambda m: note_button(m[1], language), part) for part in parts)


def render(block, language, image_root):
    if block.kind == "code":
        info = PRISM_ALIASES.get(block.extra["info"], block.extra["info"])
        code = html.escape(block.extra["content"].replace("\t", "    ").rstrip("\n"))
        lang_attr = f' data-lang="{html.escape(info)}"' if info else ""
        cls = f' class="lang-{html.escape(info)}"' if info else ""
        return f"<pre{lang_attr}><code{cls}>{code}</code></pre>"
    if block.kind == "heading":
        return with_notes(RENDER.renderInline(block.extra["markdown"]), language)
    if block.kind == "rule":
        return "<hr>"
    rendered = RENDER.render(block.raw).strip()
    rendered = rendered.replace('src="./images/', f'src="{image_root}/images/').replace('src="images/', f'src="{image_root}/images/')
    return with_notes(rendered, language)


def roles(units):
    """Presentational roles the reader styles: credits, epigraph, captions, subheadings, attributions."""
    first_section = next((i for i, u in enumerate(units) if u["kind"] == "heading" and u["level"] >= 2), len(units))
    for index, unit in enumerate(units):
        if unit["kind"] != "paragraph":
            continue
        plain = normalize(unit["sourcePlain"])
        if CREDIT.match(plain):
            unit["role"] = "credit"
        elif ATTRIBUTION.match(plain):
            unit["role"] = "attribution"
        elif CAPTION.match(plain):
            unit["role"] = "caption"
        elif unit["target"] is None and CODE_LABEL.match(plain):
            unit["role"] = "code-label"
        elif (index < first_section and units[index + 1:index + 2] and ATTRIBUTION.match(normalize(units[index + 1]["sourcePlain"]))
              and all(u["kind"] != "paragraph" or u.get("role") == "credit" for u in units[:index])):
            unit["role"] = "epigraph"
        elif re.fullmatch(r"\*\*.+\*\*|\*[^*].*\*", unit["source"].strip(), flags=re.S) and len(plain) < 120 and "\n" not in unit["source"].strip():
            unit["role"] = "subheading"


def compile_chapter(key, source_text, target_text, image_root):
    source_blocks, source_notes = parse(source_text)
    target_blocks, target_notes = parse(target_text)
    if set(source_notes) - set(target_notes):
        raise ValueError(f"{key}: footnotes without translation: {sorted(set(source_notes) - set(target_notes))}")
    translator = {n: body for n, body in target_notes.items() if n.startswith("t")}
    if set(target_notes) - set(source_notes) - set(translator):
        raise ValueError(f"{key}: translated footnotes without source: {sorted(set(target_notes) - set(source_notes) - set(translator))}")
    used_ids, used_slugs = set(), set()
    units = []
    for block, target in align(source_blocks, target_blocks, key):
        unit = {"id": unit_id(key, block.plain or block.raw, used_ids), "kind": block.kind, "role": None,
                "source": block.raw, "sourcePlain": block.plain, "sourceHtml": render(block, "en", image_root),
                "target": target.raw if target else None, "targetPlain": target.plain if target else None,
                "targetHtml": render(target, "zh", image_root) if target else None}
        if block.kind == "heading":
            unit["level"] = block.extra["level"]
            unit["anchor"] = slugify(block.plain, used_slugs)
        if block.kind == "code":
            unit["language"] = PRISM_ALIASES.get(block.extra["info"], block.extra["info"])
        units.append(unit)
    roles(units)
    for unit in units:
        del unit["sourcePlain"]
        if unit.get("targetPlain") is None:
            unit.pop("targetPlain", None)
    title = next((u for u in units if u["kind"] == "heading" and u["level"] == 1), None)
    if not title or not title["target"]:
        raise ValueError(f"{key}: chapter title missing")
    footnotes = {n: {"sourceHtml": with_notes(RENDER.renderInline(source_notes[n]), "en"),
                     "targetHtml": with_notes(RENDER.renderInline(target_notes[n]), "zh")} for n in source_notes}
    notes = {n: {"html": RENDER.renderInline(body)} for n, body in translator.items()}
    referenced = set()
    for block in source_blocks + target_blocks:
        referenced.update(MARKER.findall(block.raw))
    for n in list(footnotes) + list(notes):
        if n not in referenced:
            raise ValueError(f"{key}: note {n} is defined but never referenced")
    for n in referenced:
        if n not in footnotes and n not in notes:
            raise ValueError(f"{key}: note {n} is referenced but not defined")
    return {"id": key, "title": re.sub(r"^#+\s*", "", title["target"]).strip(), "englishTitle": re.sub(r"^#+\s*", "", title["source"]).strip(),
            "units": units, "footnotes": footnotes, "notes": notes}
