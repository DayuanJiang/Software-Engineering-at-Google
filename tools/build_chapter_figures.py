"""Generate each chapter's opening map and closing storyline (desktop + mobile SVG) from assets/diagrams/chNN.json.

The opening map answers "what is this chapter about and how do its parts relate" before the reader starts.
Its `form` picks one of seven visual forms (axes, socket, pipeline, pillars, contrast, layers, cycle).
The closing storyline retells the chapter as a sequence of acts and ends with what the chapter insists on.
Every text slot has a width budget; exceeding it fails the build instead of overflowing on the page.
"""

import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "assets" / "diagrams"
ICONS = json.loads((DIAGRAMS / "icons.json").read_text())["icons"]
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"
CLOSING = "，。、；：？！”）》"
INK, MUTED, LINE, BG = "var(--diagram-ink,#242424)", "var(--diagram-muted,#686868)", "var(--diagram-line,#aebbad)", "var(--diagram-bg,#fff)"
TONES = {
    "pri": ("var(--diagram-primary,#0b6f5d)", "var(--diagram-primary-soft,#d6e5dc)"),
    "sec": ("var(--diagram-secondary,#2c6096)", "var(--diagram-secondary-soft,#dce4ed)"),
    "warm": ("var(--diagram-warm,#80531b)", "var(--diagram-warm-soft,#eae2cf)"),
    "danger": ("var(--diagram-danger,#a03946)", "var(--diagram-danger-soft,#ead9dc)"),
}
FORMS = ("axes", "socket", "pipeline", "pillars", "contrast", "layers", "cycle")


# ---------- text measurement ----------

def width(text, size):
    """Estimate rendered width: CJK glyphs are one em, Latin letters roughly half."""
    total = 0
    for ch in text:
        if ch == " ":
            total += 0.28
        elif ch.isdigit():
            total += 0.58
        elif ord(ch) < 128:
            total += 0.64 if ch.isupper() else 0.54
        else:
            total += 1.0
    return total * size


def wrap(text, size, max_width):
    """Greedy wrap that keeps Latin words together and never starts a line with closing punctuation."""
    tokens = re.findall(r"[A-Za-z0-9_./:+#-]+|\s|.", text)
    lines, current = [], ""
    for token in tokens:
        candidate = current + token
        # Full-width closing punctuation has blank space on its right, so it may hang past the edge.
        if width(candidate, size) <= max_width or (token in CLOSING and width(candidate, size) <= max_width + size / 2):
            current = candidate
        elif token in CLOSING and len(current) > 1:
            # Never start a line with closing punctuation: carry the preceding character down with it.
            lines.append(current[:-1].rstrip())
            current = current[-1] + token
        else:
            lines.append(current.rstrip())
            current = token.lstrip()
    lines.append(current.rstrip())
    return [line for line in lines if line]


def fit(text, size, max_width, where):
    if width(text, size) > max_width:
        raise ValueError(f"Text too wide for {where} (max about {int(max_width / size)} CJK chars): {text}")
    return text


def lines(text, size, max_width, max_lines, where):
    wrapped = wrap(text, size, max_width)
    if len(wrapped) > max_lines:
        raise ValueError(f"Text needs {len(wrapped)} lines but {where} allows {max_lines}: {text}")
    return wrapped


# ---------- primitives ----------

def text(x, y, content, cls="", anchor="start", fill=None):
    attrs = (f' class="{cls}"' if cls else "") + (f' fill="{fill}"' if fill else "")
    return f'<text x="{x:.1f}" y="{y:.1f}"{attrs} text-anchor="{anchor}">{html.escape(content)}</text>'


def block(x, y, wrapped, line_height, cls="", anchor="start", fill=None):
    return [text(x, y + i * line_height, line, cls, anchor, fill) for i, line in enumerate(wrapped)]


def icon(name, x, y, size, color):
    if name not in ICONS:
        raise ValueError(f"Unknown icon: {name}")
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({size / 24:.3f})" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def disc(cx, cy, r, tone, name, size):
    stroke, soft = TONES[tone]
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{soft}" stroke="{stroke}" stroke-width="2"/>'
            + icon(name, cx - size / 2, cy - size / 2, size, stroke))


def box(x, y, w, h, fill, rx=12, stroke=None):
    extra = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{extra}/>'


def arrow(prefix, x1, y1, x2, y2, dashed=False):
    dash = ' stroke-dasharray="6 6"' if dashed else ""
    return (f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" fill="none" stroke="{LINE}" stroke-width="2"{dash} '
            f'marker-end="url(#{prefix}-arrow)"/>')


def marker(prefix):
    return (f'<defs><marker id="{prefix}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" '
            f'orient="auto" markerUnits="userSpaceOnUse"><path d="M1 1L9 5L1 9Z" fill="{LINE}"/></marker></defs>')


STYLES = [
    ("text", f"font-family:{FONT};fill:{INK}"),
    (".headline", "font-size:30px;font-weight:600"), (".headline-m", "font-size:23px;font-weight:600"),
    (".story-headline", "font-size:26px;font-weight:600"), (".story-headline-m", "font-size:21px;font-weight:600"),
    (".h22", "font-size:22px;font-weight:600"), (".h20", "font-size:20px;font-weight:600"),
    (".h19", "font-size:19px;font-weight:600"), (".h18", "font-size:18px;font-weight:600"), (".h16", "font-size:16px;font-weight:600"),
    (".t15", "font-size:15px"), (".t14", "font-size:14px"),
    (".c15", f"font-size:15px;fill:{MUTED}"), (".c14", f"font-size:14px;fill:{MUTED}"), (".c13", f"font-size:13px;fill:{MUTED}"),
    (".tag", "font-size:13px;font-weight:600;fill:var(--diagram-primary,#0b6f5d)"),
    (".act", "font-size:12px;font-weight:600;letter-spacing:1px"),
    (".answer", "font-size:21px;font-weight:600"), (".answer-m", "font-size:17px;font-weight:600"),
    (".emph", "font-size:20px;font-weight:600"), (".emph-m", "font-size:18px;font-weight:600"),
]


def document(key, mobile, size, body, title, desc):
    prefix = key + ("m" if mobile else "")
    layout = "mobile" if mobile else "desktop"
    w, h = size
    css = "\n".join(f'    .cg-{key}[data-layout="{layout}"] {selector} {{{rule}}}' for selector, rule in STYLES)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'class="chapter-svg cg-{key}" data-layout="{layout}" role="img" aria-labelledby="{prefix}-title {prefix}-desc">\n'
        f'  <title id="{prefix}-title">{html.escape(title)}</title>\n'
        f'  <desc id="{prefix}-desc">{html.escape(desc)}</desc>\n'
        f'  <style>\n{css}\n  </style>\n'
        f'  <rect x="0" y="0" width="{w}" height="{h}" fill="{BG}"/>\n'
        + "\n".join("  " + line for line in body) + "\n</svg>\n"
    )


# ---------- opening map: shared frame ----------

def map_desc(chart):
    parts = "；".join(f"{p['label']}：{p['text']}" for p in chart["parts"])
    return f"本章概览。{chart['question']} 本章的主要部分：{parts}。一句话：{chart['answer']}"


def answer_band(body, y, chart, mobile):
    margin, pad = (22, 14) if mobile else (32, 18)
    w = (420 if mobile else 960) - 2 * margin
    size, lh = (17, 26) if mobile else (21, 30)
    wrapped = lines(chart["answer"], size, w - 2 * pad, 3 if mobile else 2, "answer band")
    h = 22 + len(wrapped) * lh + 16
    body.append(box(margin, y, w, h, TONES["pri"][1], 10))
    body.append(text(margin + pad, y + 21, "一句话", "tag"))
    body += block(margin + pad, y + 21 + lh, wrapped, lh, "answer-m" if mobile else "answer")
    return y + h


def desktop_map(key, chart):
    body = [marker(key), text(32, 52, fit(chart["question"], 30, 896, "question"), "headline")]
    bottom = FORM_DESKTOP[chart["form"]](key, chart, body, 84)
    height = answer_band(body, bottom + 22, chart, False) + 28
    return document(key, False, (960, height), body, chart["question"], map_desc(chart))


def mobile_map(key, chart):
    margin, pad, inner = 22, 14, 376
    prefix = key + "m"  # ids inside the mobile layout carry the layout suffix
    body = [marker(prefix)]
    head = lines(chart["question"], 23, inner, 2, "mobile question")
    body += block(margin, 44, head, 31, "headline-m")
    y = 44 + (len(head) - 1) * 31 + 24
    for row in FORM_ROWS[chart["form"]](chart):
        if row["kind"] == "group":
            stroke, _ = TONES[row.get("tone", "pri")]
            body.append(text(margin, y + 14, row["label"], "h16", fill=stroke))
            y += 30
            continue
        if row["kind"] == "note":
            wrapped = lines(row["text"], 13, inner, 3, "mobile note")
            body += block(margin, y + 12, wrapped, 20, "c13")
            y += len(wrapped) * 20 + 10
            continue
        tone = row.get("tone", "sec")
        label = lines(row["label"], 18, inner - 2 * pad - 44, 2, f"mobile label {row['label']}")
        wrapped = lines(row["text"], 15, inner - 2 * pad - 44, row.get("maxLines", 3), f"mobile row {row['label']}")
        h = 30 + (len(label) - 1) * 24 + len(wrapped) * 22 + 14
        body.append(box(margin, y, inner, h, TONES[tone][1], 9))
        body.append(disc(margin + pad + 14, y + 26, 14, tone, row["icon"], 16))
        body += block(margin + pad + 38, y + 31, label, 24, "h18")
        body += block(margin + pad + 38, y + 56 + (len(label) - 1) * 24, wrapped, 22, "c15")
        y += h + (26 if row.get("arrow") else 10)
        if row.get("arrow"):
            body.append(arrow(prefix, 210, y - 24, 210, y - 8))
    height = answer_band(body, y + 8, chart, True) + 22
    return document(key, True, (420, height), body, chart["question"], map_desc(chart))


def part_rows(chart, arrows=False, tone="sec"):
    return [{"kind": "part", "icon": p["icon"], "label": p["label"], "text": p["text"], "tone": p.get("tone", tone), "arrow": arrows}
            for p in chart["parts"]]


# ---------- form: axes ----------

def axes_desktop(key, chart, body, top):
    fig = chart["figure"]
    x_axis, y_axis = chart["parts"][0], chart["parts"][1]
    ox, oy, right, ceiling = 120, top + 212, 900, top + 8
    body.append(arrow(key, ox, oy, right, oy)); body.append(arrow(key, ox, oy, ox, ceiling))
    body.append(icon(x_axis["icon"], 560, oy + 10, 22, MUTED))
    body.append(text(588, oy + 28, fit(f"{x_axis['label']}：{x_axis['text']}", 16, 300, "x axis"), "h16"))
    body.append(text(ox + 14, oy + 20, fig["xTicks"][0], "c13")); body.append(text(850, oy + 20, fig["xTicks"][1], "c13", "end"))
    body.append(icon(y_axis["icon"], 30, ceiling - 10, 22, MUTED))
    body.append(text(58, ceiling + 7, fit(f"{y_axis['label']}：{y_axis['text']}", 16, 330, "y axis"), "h16"))
    body.append(text(ox - 8, oy - 10, fig["yTicks"][0], "c13", "end")); body.append(text(ox - 8, ceiling + 34, fig["yTicks"][1], "c13", "end"))
    origin = fig["origin"]
    body.append(disc(182, oy - 40, 24, "sec", origin["icon"], 28))
    body.append(text(216, oy - 44, origin["label"], "h20"))
    body.append(text(216, oy - 22, fit(origin["text"], 15, 196, "origin text"), "c15"))
    body.append(f'<path d="M212 {oy - 60} C 300 {oy - 106}, 340 {oy - 120}, 408 {oy - 128}" fill="none" stroke="{LINE}" '
                f'stroke-width="2" stroke-dasharray="6 6" marker-end="url(#{key}-arrow)"/>')
    body.append(text(298, oy - 70, fit(fig["arrow"], 13, 118, "arrow caption"), "c13"))
    region = fig["region"]
    body.append(box(420, ceiling + 16, 470, 176, TONES["pri"][1], 14))
    body.append(text(444, ceiling + 50, region["label"], "h22"))
    body.append(text(444, ceiling + 74, fit(region["text"], 15, 430, "region text"), "c15"))
    items = chart["parts"][2:]
    slot = 446 / max(len(items), 1)
    for i, item in enumerate(items):
        x = 446 + i * slot
        body.append(icon(item["icon"], x, ceiling + 108, 40, TONES["pri"][0]))
        body.append(text(x + 52, ceiling + 130, item["label"], "h18"))
        body.append(text(x + 52, ceiling + 154, fit(item["text"], 15, slot - 60, f"region item {item['label']}"), "c15"))
    return oy + 34


def axes_rows(chart):
    fig = chart["figure"]
    rows = [{"kind": "group", "label": "两个变化的方向", "tone": "pri"}]
    rows += part_rows({"parts": chart["parts"][:2]})
    rows.append({"kind": "group", "label": f"从{fig['origin']['label']}到{fig['region']['label']}", "tone": "pri"})
    rows.append({"kind": "part", "icon": fig["origin"]["icon"], "label": fig["origin"]["label"], "text": fig["origin"]["text"], "tone": "sec", "arrow": True})
    rows.append({"kind": "part", "icon": chart["parts"][2]["icon"], "label": fig["region"]["label"], "text": fig["region"]["text"], "tone": "pri"})
    rows += part_rows({"parts": chart["parts"][2:]}, tone="pri")
    return rows


# ---------- form: socket ----------

def socket_desktop(key, chart, body, top):
    fig = chart["figure"]
    body.append(box(40, top + 20, 320, 196, TONES["sec"][1], 14))
    body.append(text(64, top + 62, fig["box"]["label"], "h22"))
    body.append(text(64, top + 88, fit(fig["box"]["text"], 15, 272, "socket box text"), "c15"))
    body.append(icon(fig["box"]["icon"], 64, top + 122, 56, TONES["sec"][0]))
    sec = TONES["sec"][0]
    body.append(box(338, top + 84, 52, 68, BG, 10, sec))
    body.append(f'<rect x="352" y="{top + 102}" width="8" height="20" rx="2" fill="{sec}"/><rect x="368" y="{top + 102}" width="8" height="20" rx="2" fill="{sec}"/>')
    body.append(text(364, top + 174, fig["socket"]["label"], "h18", "middle"))
    body.append(text(364, top + 196, fit(fig["socket"]["text"], 13, 150, "socket caption"), "c13", "middle"))
    body.append(arrow(key, 470, top + 118, 400, top + 118, dashed=True))
    body.append(text(484, top + 38, fit(fig["header"], 15, 440, "socket header"), "c15"))
    y = top + 56
    highlight = fig.get("highlight")
    for i, part in enumerate(chart["parts"]):
        first = i == highlight
        if first:
            body.append(box(472, y, 440, 42, TONES["pri"][1], 9))
        body.append(icon(part["icon"], 486, y + 7, 28, TONES["pri"][0] if first else MUTED))
        body.append(text(528, y + 28, fit(part["label"], 18, 100, "plug label"), "h18"))
        body.append(text(636, y + 28, fit(part["text"], 15, 276, f"plug text {part['label']}"), "c15"))
        y += 48
    if fig.get("bracket"):
        start = top + 56 + 48 * fig["bracket"]["from"] + 4
        span = 48 * (len(chart["parts"]) - fig["bracket"]["from"]) - 8
        body.append(f'<path d="M918 {start} h6 v{span} h-6" fill="none" stroke="{LINE}" stroke-width="2"/>')
        body.append(text(930, start + span / 2 + 5, fit(fig["bracket"]["label"], 13, 26, "bracket label"), "c13"))
    body.append(text(484, y + 14, fit(fig["footer"], 13, 440, "socket footer"), "c13"))
    return max(y + 22, top + 216)


def socket_rows(chart):
    fig = chart["figure"]
    rows = [{"kind": "part", "icon": fig["box"]["icon"], "label": fig["box"]["label"], "text": fig["box"]["text"] + "；" + fig["socket"]["label"] + "：" + fig["socket"]["text"], "tone": "sec"},
            {"kind": "group", "label": fig["header"], "tone": "pri"}]
    for i, p in enumerate(chart["parts"]):
        rows.append({"kind": "part", "icon": p["icon"], "label": p["label"], "text": p["text"], "tone": "pri" if i == fig.get("highlight") else "sec"})
    rows.append({"kind": "note", "text": fig["footer"]})
    return rows


# ---------- form: pipeline ----------

def pipeline_desktop(key, chart, body, top):
    fig = chart.get("figure", {})
    y = top
    if fig.get("header"):
        body.append(text(32, y + 10, fit(fig["header"], 15, 896, "pipeline header"), "c15")); y += 30
    n = len(chart["parts"])
    gap = 26
    slot = (896 - (n - 1) * gap) / n
    size = 15 if n <= 4 else 14
    lh = 22 if n <= 4 else 21
    wrapped = [lines(p["text"], size, slot - 16, 3, f"pipeline step {p['label']}") for p in chart["parts"]]
    depth = max(map(len, wrapped))
    for i, (part, w) in enumerate(zip(chart["parts"], wrapped)):
        x = 32 + i * (slot + gap)
        cx = x + slot / 2
        body.append(disc(cx, y + 36, 30, part.get("tone", "pri"), part["icon"], 30))
        body.append(text(cx, y + 96, fit(part["label"], 18, slot, "pipeline label"), "h18", "middle"))
        body += block(cx, y + 122, w, lh, "c15" if size == 15 else "c14", "middle")
        if i < n - 1:
            body.append(arrow(key, x + slot + 4, y + 36, x + slot + gap - 4, y + 36))
    y += 122 + depth * lh
    if fig.get("footer"):
        body.append(text(32, y + 14, fit(fig["footer"], 14, 896, "pipeline footer"), "c14")); y += 24
    return y


def pipeline_rows(chart):
    fig = chart.get("figure", {})
    rows = ([{"kind": "note", "text": fig["header"]}] if fig.get("header") else []) + part_rows(chart, arrows=True, tone="pri")
    rows[-1]["arrow"] = False
    if fig.get("footer"):
        rows.append({"kind": "note", "text": fig["footer"]})
    return rows


# ---------- form: pillars ----------

def pillars_desktop(key, chart, body, top):
    goal = chart["figure"]["goal"]
    body.append(box(32, top, 896, 70, TONES["pri"][1], 12))
    body.append(icon("target", 52, top + 21, 28, TONES["pri"][0]))
    body.append(text(94, top + 30, fit(goal["label"], 20, 800, "goal label"), "h20"))
    body.append(text(94, top + 54, fit(goal["text"], 15, 800, "goal text"), "c15"))
    n = len(chart["parts"])
    gap = 18
    slot = (896 - (n - 1) * gap) / n
    size = 15 if n <= 4 else 14
    lh = 22 if n <= 4 else 21
    wrapped = [lines(p["text"], size, slot - 28, 4, f"pillar {p['label']}") for p in chart["parts"]]
    depth = max(map(len, wrapped))
    h = 118 + depth * lh
    y = top + 88
    for i, (part, w) in enumerate(zip(chart["parts"], wrapped)):
        x = 32 + i * (slot + gap)
        body.append(box(x, y, slot, h, TONES["sec"][1], 10))
        body.append(f'<rect x="{x + 14:.1f}" y="{y + 88}" width="{slot - 28:.1f}" height="1" fill="{LINE}"/>')
        body.append(icon(part["icon"], x + 14, y + 16, 32, TONES["pri"][0]))
        body.append(text(x + 14, y + 76, fit(part["label"], 18, slot - 28, "pillar label"), "h18"))
        body += block(x + 14, y + 110, w, lh, "c15" if size == 15 else "c14")
    return y + h


def pillars_rows(chart):
    goal = chart["figure"]["goal"]
    return ([{"kind": "part", "icon": "target", "label": goal["label"], "text": goal["text"], "tone": "pri"},
             {"kind": "group", "label": "靠什么支撑", "tone": "pri"}] + part_rows(chart))


# ---------- form: contrast ----------

def contrast_desktop(key, chart, body, top):
    fig = chart["figure"]
    y = top
    if fig.get("header"):
        body.append(text(32, y + 10, fit(fig["header"], 15, 896, "contrast header"), "c15")); y += 30
    colw = 418
    sides = [(32, fig["left"], "circle-x"), (32 + colw + 60, fig["right"], "circle-check")]
    depth = max(len(fig["left"]["items"]), len(fig["right"]["items"]))
    h = 72 + depth * 30
    for x, side, mark in sides:
        stroke, soft = TONES[side.get("tone", "pri")]
        body.append(box(x, y, colw, h, soft, 12))
        body.append(icon(side["icon"], x + 20, y + 18, 26, stroke))
        body.append(text(x + 56, y + 38, fit(side["title"], 20, colw - 70, "contrast title"), "h20"))
        for i, item in enumerate(side["items"]):
            body.append(icon(mark, x + 20, y + 62 + i * 30, 16, stroke))
            body.append(text(x + 44, y + 75 + i * 30, fit(item, 15, colw - 60, "contrast item"), "t15"))
    mid = 32 + colw + 30
    body.append(arrow(key, mid - 18, y + h / 2, mid + 18, y + h / 2))
    if fig.get("arrow"):
        body.append(text(mid, y + h / 2 - 14, fit(fig["arrow"], 12, 56, "contrast arrow label"), "c13", "middle"))
    y += h
    if fig.get("footer"):
        body.append(text(32, y + 24, fit(fig["footer"], 14, 896, "contrast footer"), "c14")); y += 30
    return y


def contrast_rows(chart):
    fig = chart["figure"]
    rows = [{"kind": "note", "text": fig["header"]}] if fig.get("header") else []
    for side in (fig["left"], fig["right"]):
        rows.append({"kind": "part", "icon": side["icon"], "label": side["title"], "text": "；".join(side["items"]), "tone": side.get("tone", "pri"), "maxLines": 6})
    if fig.get("footer"):
        rows.append({"kind": "note", "text": fig["footer"]})
    return rows


# ---------- form: layers ----------

def layers_desktop(key, chart, body, top):
    fig = chart.get("figure", {})
    y = top
    if fig.get("header"):
        body.append(text(32, y + 10, fit(fig["header"], 15, 896, "layers header"), "c15")); y += 30
    n = len(chart["parts"])
    widths = fig.get("widths") or [896] * n
    h = 64
    total = n * h + (n - 1) * 8
    for i, part in enumerate(reversed(chart["parts"])):  # parts run bottom-up; draw top-down
        w = widths[n - 1 - i]
        x = 32 + (896 - w) / 2
        ly = y + i * (h + 8)
        stroke, soft = TONES[part.get("tone", "sec")]
        body.append(box(x, ly, w, h, soft, 10))
        body.append(icon(part["icon"], x + 18, ly + 18, 28, stroke))
        body.append(text(x + 60, ly + 28, fit(part["label"], 18, w - 80, "layer label"), "h18"))
        body.append(text(x + 60, ly + 50, fit(part["text"], 15, w - 80, f"layer text {part['label']}"), "c15"))
    if fig.get("side"):
        body.append(text(928, y + total + 2, fit(fig["side"], 13, 896, "layers side note"), "c13", "end"))
    y += total
    if fig.get("footer"):
        body.append(text(32, y + 26, fit(fig["footer"], 14, 896, "layers footer"), "c14")); y += 32
    return y + (16 if fig.get("side") else 0)


def layers_rows(chart):
    fig = chart.get("figure", {})
    rows = [{"kind": "note", "text": fig["header"]}] if fig.get("header") else []
    rows.append({"kind": "group", "label": "从上到下", "tone": "pri"})
    rows += part_rows({"parts": list(reversed(chart["parts"]))})
    for key in ("side", "footer"):
        if fig.get(key):
            rows.append({"kind": "note", "text": fig[key]})
    return rows


# ---------- form: cycle ----------

def cycle_desktop(key, chart, body, top):
    import math
    fig = chart.get("figure", {})
    y = top
    if fig.get("header"):
        body.append(text(32, y + 10, fit(fig["header"], 15, 896, "cycle header"), "c15")); y += 30
    n = len(chart["parts"])
    cx, cy, rx, ry = 480, y + 232, 310, 100
    points = []
    for i in range(n):
        angle = -math.pi / 2 + 2 * math.pi * i / n
        points.append((cx + rx * math.cos(angle), cy + ry * math.sin(angle)))
    for i, (px, py) in enumerate(points):
        nx, ny = points[(i + 1) % n]
        dx, dy = nx - px, ny - py
        dist = math.hypot(dx, dy)
        ux, uy = dx / dist, dy / dist
        body.append(arrow(key, px + ux * 36, py + uy * 36, nx - ux * 38, ny - uy * 38))
    for (px, py), part in zip(points, chart["parts"]):
        body.append(disc(px, py, 28, part.get("tone", "pri"), part["icon"], 28))
        # Captions sit above nodes in the upper half and below nodes in the lower half, centred and kept on the canvas.
        above = py < cy - 10
        text_w = 320 if abs(px - cx) < 60 else min(230, 2 * min(px, 960 - px) - 16)
        wrapped = lines(part["text"], 14, text_w, 3, f"cycle step {part['label']}")
        ty = py - 42 - len(wrapped) * 20 if above else py + 54
        body.append(text(px, ty, fit(part["label"], 18, text_w, "cycle label"), "h18", "middle"))
        body += block(px, ty + 22, wrapped, 20, "c14", "middle")
    y = cy + ry + 54 + 22 + 3 * 20
    if fig.get("footer"):
        body.append(text(32, y + 8, fit(fig["footer"], 14, 896, "cycle footer"), "c14")); y += 24
    return y


def cycle_rows(chart):
    fig = chart.get("figure", {})
    rows = ([{"kind": "note", "text": fig["header"]}] if fig.get("header") else []) + part_rows(chart, arrows=True, tone="pri")
    rows.append({"kind": "note", "text": "然后回到第一步，循环往复。" + (fig.get("footer") or "")})
    return rows


FORM_DESKTOP = {"axes": axes_desktop, "socket": socket_desktop, "pipeline": pipeline_desktop, "pillars": pillars_desktop,
                "contrast": contrast_desktop, "layers": layers_desktop, "cycle": cycle_desktop}
FORM_ROWS = {"axes": axes_rows, "socket": socket_rows, "pipeline": pipeline_rows, "pillars": pillars_rows,
             "contrast": contrast_rows, "layers": layers_rows, "cycle": cycle_rows}


# ---------- closing storyline ----------

def story_desc(story):
    acts = "；".join(f"{a['act']}：{a['title']}。{a['text']}" for a in story["acts"])
    return f"本章回顾。{story['headline']}。{acts}。这一章最想强调的：{story['emphasis']} {story['emphasis2']}"


def storyline(key, story, mobile):
    w = 420 if mobile else 960
    margin = 22 if mobile else 32
    rail = 40 if mobile else 74
    tx = 76 if mobile else 118
    text_w = w - tx - (18 if mobile else 32)
    body = [text(margin, 30, "本章回顾", "tag")]
    head = lines(story["headline"], 21 if mobile else 26, w - 2 * margin, 2 if mobile else 1, "story headline")
    body += block(margin, 62 if mobile else 62, head, 28, "story-headline-m" if mobile else "story-headline")
    y = 62 + (len(head) - 1) * 28 + (56 if mobile else 60)
    centers = []
    for act in story["acts"]:
        stroke, soft = TONES[act.get("tone", "pri")]
        title = lines(act["title"], 18 if mobile else 19, text_w, 2 if mobile else 1, f"act title {act['act']}")
        narrative = lines(act["text"], 15, text_w, 4 if mobile else 2, f"act text {act['act']}")
        centers.append(y)
        body.append(disc(rail, y, 18 if mobile else 22, act.get("tone", "pri"), act["icon"], 18 if mobile else 22))
        body.append(text(tx, y - 12, act["act"], "act", fill=stroke))
        body += block(tx, y + 12, title, 24, "h18" if mobile else "h19")
        ny = y + 12 + (len(title) - 1) * 24 + 26
        body += block(tx, ny, narrative, 23, "t15")
        y = ny + (len(narrative) - 1) * 23 + 62
    body.insert(1, f'<path d="M{rail} {centers[0] + 22} V {centers[-1] - 22}" stroke="{LINE}" stroke-width="2"/>')
    top = y - 24
    ex = margin + (56 if mobile else 60)
    ew = w - ex - margin - 14
    emphasis = lines(story["emphasis"], 18 if mobile else 20, ew, 3 if mobile else 1, "emphasis")
    emphasis2 = lines(story["emphasis2"], 14 if mobile else 15, ew, 3 if mobile else 1, "emphasis note")
    h = 40 + len(emphasis) * (24 if mobile else 26) + len(emphasis2) * 21 + 14
    body.append(box(margin, top, w - 2 * margin, h, TONES["pri"][1], 12))
    body.append(icon("flag", margin + 18, top + 20, 24, TONES["pri"][0]))
    body.append(text(ex, top + 28, "这一章最想强调的", "tag"))
    body += block(ex, top + 54, emphasis, 24 if mobile else 26, "emph-m" if mobile else "emph")
    body += block(ex, top + 54 + len(emphasis) * (24 if mobile else 26), emphasis2, 21, "c14" if mobile else "c15")
    return document(key, mobile, (w, top + h + 28), body, story["headline"], story_desc(story))


# ---------- entry points ----------

def build(metadata):
    """Return {relative path: svg text} for one chapter's four figures."""
    chart, story = metadata["map"], metadata["story"]
    key = f"ch{metadata['chapter']:02d}"
    if chart["form"] not in FORMS:
        raise ValueError(f"Unknown map form: {key}: {chart['form']}")
    if chart["question"] != metadata["title"] or chart["answer"] != metadata["summary"]:
        raise ValueError(f"Map question/answer must match the guide title/summary: {key}")
    if not 3 <= len(story["acts"]) <= 6:
        raise ValueError(f"A storyline needs 3 to 6 acts: {key}")
    return {
        metadata["desktop"]: desktop_map(key, chart),
        metadata["mobile"]: mobile_map(key, chart),
        metadata["storyDesktop"]: storyline(key + "-story", story, False),
        metadata["storyMobile"]: storyline(key + "-story", story, True),
    }


def main():
    count, errors = 0, []
    for path in sorted(DIAGRAMS.glob("ch??.json")):
        try:
            for relative, svg in build(json.loads(path.read_text())).items():
                (ROOT / relative).write_text(svg)
            count += 1
        except ValueError as error:
            errors.append(f"{path.name}: {error}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Generated opening maps and closing storylines for {count} chapters in both layouts.")


if __name__ == "__main__":
    main()
