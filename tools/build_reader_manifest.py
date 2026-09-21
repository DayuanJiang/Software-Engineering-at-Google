"""Build the reader's data: aligned chapter units, the chapter/SVG manifest and code variants, without modifying book text."""

import ast
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import translation_audit as audit
import book

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "assets" / "diagrams"
CONTENT = ROOT / "assets" / "reader-content"
VARIANTS = ROOT / "assets" / "code-variants"
VARIANT_LANGUAGES = {".java": "java", ".cpp": "cpp", ".c": "c", ".go": "go"}

PEDAGOGY_FIELDS = (
    "readerQuestion", "expectedAnswer", "visualEncoding", "sourceEvidence",
    "beforeProblem", "whyBetter", "limits",
)


def check_pedagogy(metadata):
    review = metadata.get("pedagogy", {})
    if review.get("action") not in {"keep", "revise", "replace"}:
        raise ValueError(f"Missing diagram review decision: {metadata.get('id', metadata.get('chapter'))}")
    for key in PEDAGOGY_FIELDS:
        if not isinstance(review.get(key), str) or not review[key].strip():
            raise ValueError(f"Missing diagram review field {key}: {metadata.get('id', metadata.get('chapter'))}")


def anchor_count(chapter, anchor):
    """How many translation blocks contain the anchor text (footnote markers ignored on both sides)."""
    needle = " ".join(re.sub(r"\[\^\w+\]", "", anchor).split())
    if not needle:
        return 0
    return sum(needle in " ".join(re.sub(r"\[\^\w+\]", "", u.get("targetPlain") or "").split()) for u in chapter["units"])


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
    for name in ("assets/reader.css", "assets/reader.js", "assets/vendor/docsify-vue.css"):
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
    CONTENT.mkdir(exist_ok=True)
    for stale in list(CONTENT.glob("*.json")) + list(VARIANTS.glob("*.json")):
        stale.unlink()
    paths = sorted((ROOT / "en").rglob("*.md"))
    for path in paths:
        relative = path.relative_to(ROOT / "en")
        translation = ROOT / "zh-cn" / relative
        if not translation.exists():
            raise ValueError(f"Translation file missing: zh-cn/{relative.as_posix()}")
        text = path.read_text()
        number = re.search(r"Chapter-(\d+)_", str(path))
        key = f"ch{int(number[1]):02d}" if number else path.stem.lower()
        image_root = "en/" + relative.parent.as_posix() if relative.parent.as_posix() != "." else "en"
        chapter = book.compile_chapter(key, text, translation.read_text(), image_root)
        (CONTENT / f"{key}.json").write_text(json.dumps(chapter, ensure_ascii=False) + "\n")
        file = translation.relative_to(ROOT).as_posix()
        chapters.append({"id": key, "number": int(number[1]) if number else None, "title": chapter["title"],
                         "englishTitle": chapter["englishTitle"], "file": file, "source": path.relative_to(ROOT).as_posix(),
                         "route": "/" + file.removesuffix(".md"), "content": f"assets/reader-content/{key}.json"})
        variants = compile_code_variants(VARIANTS / key, text)
        if variants:
            (VARIANTS / f"{key}.json").write_text(json.dumps(variants, ensure_ascii=False, indent=2) + "\n")
            chapters[-1]["codeVariants"] = f"assets/code-variants/{key}.json"
        if number:
            n = int(number[1])
            metadata = json.loads((DIAGRAMS / f"ch{n:02d}.json").read_text())
            if metadata["chapter"] != n or not metadata["title"] or not metadata["summary"]:
                raise ValueError(f"Invalid guide metadata: {key}")
            check_pedagogy(metadata)
            if metadata["map"]["question"] != metadata["title"] or not metadata["story"]["acts"]:
                raise ValueError(f"Chapter map/story content missing or inconsistent: {key}")
            headings = {" ".join(re.sub(r"^#+\s*", "", u["source"]).split()) for u in chapter["units"] if u["kind"] == "heading"}
            for heading in metadata["sourceSections"]:
                if " ".join(heading.split()) not in headings:
                    raise ValueError(f"Unknown source heading in {key}: {heading}")
            check_svg(ROOT / metadata["desktop"], n, False)
            check_svg(ROOT / metadata["mobile"], n, True)
            check_svg(ROOT / metadata["storyDesktop"], n, False, story=True)
            check_svg(ROOT / metadata["storyMobile"], n, True, story=True)
            # The reader only needs titles and file paths; the map text, storyline and review notes stay in the metadata file.
            guides[key] = {field: metadata[field] for field in ("chapter", "title", "summary", "desktop", "mobile", "storyDesktop", "storyMobile")}
            guides[key]["storyTitle"] = metadata["story"]["headline"]
            sections = []
            for section_path in sorted((DIAGRAMS / "sections").glob(f"{key}-*.json")):
                section = json.loads(section_path.read_text())
                if section["id"] != section_path.stem or section["chapter"] != n:
                    raise ValueError(f"Invalid section guide identity: {section_path}")
                check_pedagogy(section)
                if anchor_count(chapter, section["afterParagraph"]) != 1:
                    raise ValueError(f"Ambiguous section insertion point: {section_path}")
                for heading in section["sourceSections"]:
                    if " ".join(heading.split()) not in headings:
                        raise ValueError(f"Unknown section guide heading: {section_path}: {heading}")
                check_svg(ROOT / section["desktop"], n, False, section["id"])
                check_svg(ROOT / section["mobile"], n, True, section["id"])
                sections.append(section)
            if sections:
                chapters[-1]["sectionGuides"] = sections
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
