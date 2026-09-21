import json
from pathlib import Path
import subprocess
import unittest
import xml.etree.ElementTree as ET

import build_reader_manifest as reader


class ReaderAssetsTests(unittest.TestCase):
    def test_all_chapters_have_both_svg_layouts(self):
        manifest = json.loads((reader.ROOT / "assets/reader-manifest.json").read_text())
        self.assertEqual(len(manifest["chapters"]), 28)
        self.assertEqual(len(manifest["guides"]), 25)
        for number in range(1, 26):
            key = f"ch{number:02d}"
            guide = manifest["guides"][key]
            self.assertTrue(guide["storyTitle"])
            for mobile, field in [(False, "desktop"), (True, "mobile")]:
                reader.check_svg(reader.ROOT / guide[field], number, mobile)
            for mobile, field in [(False, "storyDesktop"), (True, "storyMobile")]:
                reader.check_svg(reader.ROOT / guide[field], number, mobile, story=True)

    def test_existing_book_text_is_byte_identical_to_translation_commit(self):
        for path in (reader.ROOT / "zh-cn").rglob("*.md"):
            relative = path.relative_to(reader.ROOT).as_posix()
            # The translation-polish tag marks the latest approved book text; move it when the text changes deliberately.
            before = subprocess.check_output(["git", "-C", str(reader.ROOT), "show", "translation-polish:" + relative])
            self.assertEqual(path.read_bytes(), before, relative)

    def test_book_font_subset_covers_every_book_character(self):
        import build_fonts
        fonts = reader.ROOT / "assets/fonts"
        covered = set((fonts / "charset.txt").read_text())
        missing = sorted(set(build_fonts.book_characters()) - covered)
        self.assertEqual(missing, [], "rebuild the font subset: tools/build_fonts.py")
        for name in build_fonts.FACES:
            self.assertGreater((fonts / f"{name}.woff2").stat().st_size, 100_000, name)
        css = (reader.ROOT / "assets/reader.css").read_text()
        self.assertIn('src: url("fonts/NotoSerifSC-Regular.woff2")', css)
        self.assertIn('src: url("fonts/NotoSerifSC-SemiBold.woff2")', css)

    def test_lucide_sprite_contains_required_controls(self):
        root = ET.parse(reader.ROOT / "assets/reader-icons.svg").getroot()
        ids = {node.get("id") for node in root}
        for name in ["menu", "sun", "moon", "minus", "plus", "maximize-2", "minimize-2", "x", "download", "list"]:
            self.assertIn("icon-" + name, ids)

    def test_reader_core_dependencies_are_local(self):
        index = (reader.ROOT / "index.html").read_text()
        self.assertIn('src="assets/vendor/docsify.min.js"', index)
        self.assertRegex(index, r'href="assets/reader\.css\?v=[0-9a-f]{8}"')
        self.assertRegex(index, r'src="assets/reader\.js\?v=[0-9a-f]{8}"')
        self.assertNotIn('src="//cdn.jsdelivr.net/npm/docsify', index)
        self.assertNotIn("NewGitalk().render", index)

    def test_known_missing_translations_are_completed_without_removing_source(self):
        manifest = json.loads((reader.ROOT / "assets/reader-manifest.json").read_text())
        for key, line in [("ch18", 337), ("ch23", 673)]:
            page = next(p for p in manifest["chapters"] if p["id"] == key)
            source = (reader.ROOT / page["file"]).read_text().splitlines()[line - 1]
            translations = reader.compiled_review(page)["translations"]
            matches = [t for t in translations if reader.reader_content.plain(t["english"]) == reader.reader_content.plain(source)]
            self.assertEqual(len(matches), 1)
            self.assertGreater(len(matches[0]["chinese"]), 100)
            self.assertEqual(page["keepEnglish"], [])

    def test_chapter_review_is_bound_to_unchanged_source(self):
        manifest = json.loads((reader.ROOT / "assets/reader-manifest.json").read_text())
        chapter = next(p for p in manifest["chapters"] if p["id"] == "ch01")
        text = (reader.ROOT / chapter["file"]).read_text()
        self.assertEqual(reader.load_reader_review("ch01", text), reader.compiled_review(chapter))
        with self.assertRaisesRegex(ValueError, "re-review"):
            reader.load_reader_review("ch01", text + "\n")

    def test_chapter_review_covers_every_original_footnote(self):
        manifest = json.loads((reader.ROOT / "assets/reader-manifest.json").read_text())
        chapter = next(p for p in manifest["chapters"] if p["id"] == "ch01")
        review = reader.compiled_review(chapter)
        self.assertEqual({n["id"] for n in review["footnotes"]}, {str(n) for n in range(1, 18)})
        self.assertEqual(len(review["proseCodeBlocks"]), 2)
        self.assertEqual(len(review["translatorNotes"]), 1)

    def test_first_chapter_has_source_anchored_reviewed_section_guides(self):
        manifest = json.loads((reader.ROOT / "assets/reader-manifest.json").read_text())
        chapter = next(p for p in manifest["chapters"] if p["id"] == "ch01")
        source = (reader.ROOT / chapter["file"]).read_text()
        guides = chapter.get("sectionGuides", [])
        self.assertEqual(len({g["afterParagraph"] for g in guides}), len(guides))
        for guide in guides:
            reader.check_pedagogy(guide)
            self.assertEqual(source.count(guide["afterParagraph"]), 1)
            reader.check_svg(reader.ROOT / guide["desktop"], 1, False, guide["id"])
            reader.check_svg(reader.ROOT / guide["mobile"], 1, True, guide["id"])

    def test_every_numbered_chapter_has_reviewed_explanatory_diagrams(self):
        manifest = json.loads((reader.ROOT / "assets/reader-manifest.json").read_text())
        for page in manifest["chapters"]:
            if not page["number"]:
                continue
            source = (reader.ROOT / page["file"]).read_text()
            self.assertIn("review", page, page["id"])
            self.assertEqual(reader.load_reader_review(page["id"], source), reader.compiled_review(page))
            reader.check_pedagogy(json.loads((reader.DIAGRAMS / f"{page['id']}.json").read_text()), overview=True)
            for guide in page.get("sectionGuides", []):
                self.assertTrue(reader.check_pedagogy(guide))
                self.assertEqual(reader.reader_content.anchor_count(source, guide["afterParagraph"]), 1)
                reader.check_svg(reader.ROOT / guide["desktop"], page["number"], False, guide["id"])
                reader.check_svg(reader.ROOT / guide["mobile"], page["number"], True, guide["id"])
            for guide in page.get("retiredSectionGuides", []):
                self.assertFalse(reader.check_pedagogy(guide))

    def test_diagram_review_requires_question_and_visual_reasoning(self):
        metadata = {"id": "fixture", "pedagogy": {"action": "keep"}}
        with self.assertRaisesRegex(ValueError, "readerQuestion"):
            reader.check_pedagogy(metadata)
        metadata["pedagogy"].update({field: "Reviewed fixture." for field in reader.PEDAGOGY_FIELDS})
        self.assertTrue(reader.check_pedagogy(metadata))
        metadata["enabled"] = False
        with self.assertRaisesRegex(ValueError, "disagree"):
            reader.check_pedagogy(metadata)
        metadata["pedagogy"]["action"] = "retire"
        metadata["removalReason"] = "Redundant with a more concrete example."
        self.assertFalse(reader.check_pedagogy(metadata))


if __name__ == "__main__":
    unittest.main()
