"""Build the reader's full-text search index; the browser downloads it only when someone searches."""

import json
from pathlib import Path

import translation_audit as audit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "search-index.json"


def sections(text):
    """Yield (title, text) per h1 to h3 section.

    Headings without a body of their own (the English half of a bilingual heading pair)
    stay searchable inside the following section's text, whose title is the last heading.
    """
    headings, body = [], []
    for token in audit.MD.parse(text):
        if token.type == "heading_open" and token.tag in {"h1", "h2", "h3"}:
            if body:
                yield headings[-1] if headings else "", "\n".join(headings[:-1] + body)
                headings, body = [], []
            headings.append(None)
        elif token.type == "inline":
            content = " ".join(audit.plain(token.children).split())
            if headings and headings[-1] is None:
                headings[-1] = content
            elif content:
                body.append(content)
    if body:
        yield headings[-1] if headings else "", "\n".join(headings[:-1] + body)


def main():
    manifest = json.loads((ROOT / "assets" / "reader-manifest.json").read_text())
    entries = []
    for chapter in manifest["chapters"]:
        text = (ROOT / chapter["file"]).read_text()
        for title, body in sections(text):
            entries.append({"route": chapter["route"], "chapter": chapter["title"],
                            "title": title or chapter["title"], "text": body})
    OUTPUT.write_text(json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"Indexed {len(entries)} sections across {len(manifest['chapters'])} chapters.")


if __name__ == "__main__":
    main()
