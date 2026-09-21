"""Build and validate the static reader's chapter/SVG manifest without modifying book text."""

import ast
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import translation_audit as audit
import reader_content

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "assets" / "diagrams"
REVIEWS = ROOT / "assets" / "reader-review"
VARIANTS = ROOT / "assets" / "code-variants"
VARIANT_LANGUAGES = {".java": "java", ".cpp": "cpp", ".c": "c", ".go": "go"}

PEDAGOGY_FIELDS = (
    "readerQuestion", "expectedAnswer", "visualEncoding", "sourceEvidence",
    "beforeProblem", "whyBetter", "limits",
)


def check_pedagogy(metadata, overview=False):
    review = metadata.get("pedagogy", {})
    action = review.get("action")
    if action not in {"keep", "revise", "replace", "retire"}:
        raise ValueError(f"Missing diagram review decision: {metadata.get('id', metadata.get('chapter'))}")
    for key in PEDAGOGY_FIELDS:
        if not isinstance(review.get(key), str) or not review[key].strip():
            raise ValueError(f"Missing diagram review field {key}: {metadata.get('id', metadata.get('chapter'))}")
    retired = metadata.get("enabled") is False
    if overview and retired:
        raise ValueError("A chapter overview must remain available.")
    if retired != (action == "retire"):
        raise ValueError(f"Diagram status and review decision disagree: {metadata.get('id')}")
    if retired and not metadata.get("removalReason"):
        raise ValueError(f"Retired diagram has no explanation: {metadata.get('id')}")
    return not retired


def load_reader_review(key, text):
    path = ROOT / "assets" / "reader-content" / f"{key}.json"
    if not path.exists():
        return None
    review = json.loads(path.read_text())
    if audit.digest(text) != review["sourceSha256"]:
        raise ValueError(f"Reader corrections need re-review after source changes: {key}")
    if review.get("format") == 2:
        return reader_content.compile_review(key, text, review)
    tokens = audit.MD.parse(text)
    code = [t.content.strip() for t in tokens if t.type in {"fence", "code_block"}]
    for item in review.get("proseCodeBlocks", []) + review.get("translatorNotes", []):
        if code.count(item["text"]) != 1:
            raise ValueError(f"Reader correction does not identify one code block: {key}")
    expected = set(re.findall(r"^>\s*\[\^(\d+)\]:", text, re.MULTILINE))
    ids = [note["id"] for note in review["footnotes"]]
    if len(ids) != len(set(ids)) or set(ids) != expected:
        raise ValueError(f"Incomplete or duplicate reviewed footnotes: {key}")
    for note in review["footnotes"]:
        if "after" in note and text.count(note["after"]) != 1:
            raise ValueError(f"Ambiguous Chinese footnote anchor: {key}: {note['id']}")
    return review


def compile_code_variants(folder, text):
    """Pair each <n>.<lang> code example with its <n>.py rewrite or <n>.skip note and check them."""
    if not folder.is_dir():
        return None
    # The Markdown renderer expands tabs to four spaces, so compare and publish sources that way.
    fences = {t.content.replace("\t", "    ").strip() for t in audit.MD.parse(text) if t.type == "fence"}
    entries = []
    for source_path in sorted(p for p in folder.iterdir() if p.suffix in VARIANT_LANGUAGES):
        source = source_path.read_text().replace("\t", "    ").strip()
        if source not in fences:
            raise ValueError(f"Code variant source is not a code block of the chapter: {source_path}")
        entry = {"language": VARIANT_LANGUAGES[source_path.suffix], "source": source}
        rewrite, skip = source_path.with_suffix(".py"), source_path.with_suffix(".skip")
        if rewrite.exists():
            entry["python"] = rewrite.read_text().strip()
            try:
                ast.parse(entry["python"], filename=str(rewrite))
            except SyntaxError as error:
                raise ValueError(f"Python rewrite does not parse: {rewrite}: {error}") from error
        elif skip.read_text().strip() if skip.exists() else False:
            entry["note"] = skip.read_text().strip()
        else:
            raise ValueError(f"Code example needs a Python rewrite or a skip note with a reason: {source_path}")
        entries.append(entry)
    return entries or None


def stamp_index():
    """Append a content hash to the reader's script and stylesheet URLs so browsers never serve stale copies."""
    index = ROOT / "index.html"
    html = index.read_text()
    for name in ("assets/reader.css", "assets/reader.js"):
        digest = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()[:8]
        html = re.sub(re.escape(name) + r'(\?v=[0-9a-f]+)?"', f'{name}?v={digest}"', html)
    if html != index.read_text():
        index.write_text(html)


def compiled_review(chapter):
    """Load the per-chapter review file that the reader fetches on demand."""
    return json.loads((ROOT / chapter["review"]).read_text()) if "review" in chapter else None


def check_svg(path, chapter, mobile, section=None, story=False):
    """Section figures have fixed sizes; generated chapter maps and storylines have a fixed width and any height."""
    root = ET.parse(path).getroot()
    key = section or f"ch{chapter:02d}" + ("-story" if story else "")
    if section:
        valid = root.get("viewBox") == ("0 0 420 600" if mobile else "0 0 960 480")
    else:
        valid = re.fullmatch(r"0 0 (420|960) \d+", root.get("viewBox", "")) and root.get("viewBox").startswith("0 0 420 " if mobile else "0 0 960 ")
    if not valid or root.get("role") != "img":
        raise ValueError(f"Invalid SVG dimensions/accessibility: {path}")
    classes = set(root.get("class", "").split())
    if "chapter-svg" not in classes or "cg-" + key not in classes:
        raise ValueError(f"Missing responsive/scoped SVG class: {path}")
    if len(root.get("aria-labelledby", "").split()) < 2:
        raise ValueError(f"Missing SVG title/description labels: {path}")
    ids = [e.get("id") for e in root.iter() if e.get("id")]
    prefix = f"{key}{'m' if mobile else ''}-"
    if len(ids) != len(set(ids)) or any(not identifier.startswith(prefix) for identifier in ids):
        raise ValueError(f"Invalid or duplicate SVG IDs: {path}")
    for identifier in root.get("aria-labelledby", "").split():
        if identifier not in ids:
            raise ValueError(f"Missing accessible label: {path}")
    for element in root.iter():
        tag = element.tag.split("}")[-1]
        if tag in {"script", "foreignObject", "image", "a"}:
            raise ValueError(f"Unsupported active/external element: {path}")
        for name, value in element.attrib.items():
            if name.lower().startswith("on"):
                raise ValueError(f"Event attribute in SVG: {path}")
            if name.split("}")[-1] == "href" and not value.startswith("#"):
                raise ValueError(f"External SVG reference: {path}")
        for ref in re.findall(r"url\(#([^)]+)\)", ET.tostring(element, encoding="unicode")):
            if ref not in ids:
                raise ValueError(f"Missing marker: {path}: {ref}")


def main():
    chapters = []
    guides = {}
    REVIEWS.mkdir(exist_ok=True)
    for stale in list(REVIEWS.glob("*.json")) + list(VARIANTS.glob("*.json")):
        stale.unlink()
    paths = sorted((ROOT / "zh-cn").rglob("*.md"))
    for path in paths:
        text = path.read_text()
        number = re.search(r"Chapter-(\d+)_", str(path))
        key = f"ch{int(number[1]):02d}" if number else path.stem.lower()
        title = next(line[re.search(r"[\u3400-\u9fff]", line).start():].strip()
                     for line in text.splitlines() if re.match(r"^#{1,6}\s", line) and re.search(r"[\u3400-\u9fff]", line))
        file = path.relative_to(ROOT).as_posix()
        # These known untranslated paragraphs must remain visible in Chinese-priority mode.
        preserve_lines = {"ch18": [337], "ch23": [673]}.get(key, [])
        chapters.append({"id": key, "number": int(number[1]) if number else None, "title": title,
                         "file": file, "route": "/" + file.removesuffix(".md"),
                         "keepEnglish": [audit.plain(audit.MD.parseInline(text.splitlines()[line - 1])[0].children)
                                         for line in preserve_lines]})
        review = load_reader_review(key, text)
        if review:
            (REVIEWS / f"{key}.json").write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n")
            chapters[-1]["review"] = f"assets/reader-review/{key}.json"
            translated = {reader_content.plain(t["english"]) for t in review.get("translations", [])}
            chapters[-1]["keepEnglish"] = [s for s in chapters[-1]["keepEnglish"] if reader_content.plain(s) not in translated]
        variants = compile_code_variants(VARIANTS / key, text)
        if variants:
            (VARIANTS / f"{key}.json").write_text(json.dumps(variants, ensure_ascii=False, indent=2) + "\n")
            chapters[-1]["codeVariants"] = f"assets/code-variants/{key}.json"
        if number:
            n = int(number[1])
            metadata = json.loads((DIAGRAMS / f"ch{n:02d}.json").read_text())
            if metadata["chapter"] != n or not metadata["title"] or not metadata["summary"]:
                raise ValueError(f"Invalid guide metadata: {key}")
            check_pedagogy(metadata, overview=True)
            if metadata["map"]["question"] != metadata["title"] or not metadata["story"]["acts"]:
                raise ValueError(f"Chapter map/story content missing or inconsistent: {key}")
            headings = {re.sub(r"^#+\s*", "", line).strip() for line in text.splitlines() if line.startswith("#")}
            for heading in metadata["sourceSections"]:
                if re.sub(r"^#+\s*", "", heading).strip() not in headings:
                    raise ValueError(f"Unknown source heading in {key}: {heading}")
            check_svg(ROOT / metadata["desktop"], n, False)
            check_svg(ROOT / metadata["mobile"], n, True)
            check_svg(ROOT / metadata["storyDesktop"], n, False, story=True)
            check_svg(ROOT / metadata["storyMobile"], n, True, story=True)
            # The reader only needs titles and file paths; the map text, storyline and review notes stay in the metadata file.
            guides[key] = {field: metadata[field] for field in ("chapter", "title", "summary", "desktop", "mobile", "storyDesktop", "storyMobile")}
            guides[key]["storyTitle"] = metadata["story"]["headline"]
            sections = []
            retired = []
            for section_path in sorted((DIAGRAMS / "sections").glob(f"{key}-*.json")):
                section = json.loads(section_path.read_text())
                if section["id"] != section_path.stem or section["chapter"] != n:
                    raise ValueError(f"Invalid section guide identity: {section_path}")
                if not check_pedagogy(section):
                    retired.append(section)
                    continue
                if reader_content.anchor_count(text, section["afterParagraph"]) != 1:
                    raise ValueError(f"Ambiguous section insertion point: {section_path}")
                for heading in section["sourceSections"]:
                    if re.sub(r"^#+\s*", "", heading).strip() not in headings:
                        raise ValueError(f"Unknown section guide heading: {section_path}: {heading}")
                check_svg(ROOT / section["desktop"], n, False, section["id"])
                check_svg(ROOT / section["mobile"], n, True, section["id"])
                sections.append(section)
            if sections:
                chapters[-1]["sectionGuides"] = sections
            if retired:
                chapters[-1]["retiredSectionGuides"] = retired
    chapters.sort(key=lambda c: c["number"] if c["number"] else {"foreword": -2, "preface": -1, "afterword": 99}[c["id"]])
    if len(guides) != 25:
        raise ValueError("Every numbered chapter must have both SVG layouts.")
    (ROOT / "assets" / "reader-manifest.json").write_text(
        json.dumps({"chapters": chapters, "guides": guides}, ensure_ascii=False, indent=2) + "\n"
    )
    stamp_index()
    layouts = 2 * (len(guides) + sum(len(c.get("sectionGuides", [])) for c in chapters))
    print(f"Validated {len(chapters)} chapters and {layouts} SVG layouts.")


if __name__ == "__main__":
    main()
