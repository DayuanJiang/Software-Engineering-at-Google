import json
from pathlib import Path
import subprocess
import unittest
import xml.etree.ElementTree as ET

import book
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
        for folder in ("en", "zh-cn"):
            for path in (reader.ROOT / folder).rglob("*.md"):
                relative = path.relative_to(reader.ROOT).as_posix()
                # The translation-polish tag marks the latest approved book text; move it when the text changes deliberately.
                before = subprocess.check_output(["git", "-C", str(reader.ROOT), "show", "translation-polish:" + relative])
                self.assertEqual(path.read_bytes(), before, relative)

    def test_every_chapter_compiles_from_aligned_files(self):
        manifest = json.loads((reader.ROOT / "assets/reader-manifest.json").read_text())
        self.assertEqual(len(manifest["chapters"]), 28)
        for page in manifest["chapters"]:
            chapter = book.compile_chapter(page["id"], (reader.ROOT / page["source"]).read_text(),
                                           (reader.ROOT / page["file"]).read_text(), "en")
            self.assertEqual(chapter["title"], page["title"])
            for unit in chapter["units"]:
                if unit["kind"] in book.TRANSLATABLE and unit["role"] != "code-label":
                    self.assertTrue(unit["target"], (page["id"], unit["source"][:60]))
            published = json.loads((reader.ROOT / page["content"]).read_text())
            self.assertEqual([u["id"] for u in published["units"]], [u["id"] for u in chapter["units"]], page["id"])

    def test_aligner_rejects_structural_drift(self):
        en = "# Title\n\nOne.\n\n- a\n- b\n\n```java\nx();\n```\n\nTwo.[^1]\n\n[^1]: Note.\n"
        zh = "# 标题\n\n一。\n\n- 甲\n- 乙\n\n二。[^1]\n\n[^1]: 注。\n"
        chapter = book.compile_chapter("fixture", en, zh, "en")
        self.assertEqual([u["kind"] for u in chapter["units"]], ["heading", "paragraph", "list", "code", "paragraph"])
        self.assertEqual(chapter["units"][4]["target"], "二。[^1]")
        self.assertIn("note-trigger", chapter["units"][4]["targetHtml"])
        with self.assertRaisesRegex(ValueError, "structure differs"):
            book.compile_chapter("fixture", en, zh.replace("- 甲\n- 乙", "- 甲"), "en")
        with self.assertRaisesRegex(ValueError, "translation missing"):
            book.compile_chapter("fixture", en + "\nThree.\n", zh, "en")
        with self.assertRaisesRegex(ValueError, "footnotes without translation"):
            book.compile_chapter("fixture", en, zh.replace("[^1]: 注。", ""), "en")
        with self.assertRaisesRegex(ValueError, "never referenced"):
            book.compile_chapter("fixture", en, zh + "[^t1]: **译者注** 多余。\n", "en")

    def test_roles_and_anchors(self):
        en = ("# Unit Testing\n\n**Written by A**\n\n*Quote.*\n\n— Someone\n\nBody.\n\n## Test Sizes\n\n"
              "*Figure 1-1. Sizes*\n\n**Motivations**\n\nfile.py:\n\n```python\npass\n```\n\n## Test Sizes\n")
        zh = "# 单元测试\n\n**作者：A**\n\n引文。\n\n— 某人\n\n正文。\n\n## 测试规模\n\n*图1-1 规模*\n\n**动机**\n\n## 测试规模\n"
        chapter = book.compile_chapter("fixture", en, zh, "en")
        roles = [(u["kind"], u["role"]) for u in chapter["units"]]
        self.assertEqual(roles[1:5], [("paragraph", "credit"), ("paragraph", "epigraph"), ("paragraph", "attribution"), ("paragraph", None)])
        self.assertEqual([u["role"] for u in chapter["units"] if u["kind"] == "paragraph"][4:7], ["caption", "subheading", "code-label"])
        self.assertEqual([u["anchor"] for u in chapter["units"] if u["kind"] == "heading"], ["unit-testing", "test-sizes", "test-sizes-2"])
        self.assertEqual(chapter["englishTitle"], "Unit Testing")

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

    def test_first_chapter_has_source_anchored_reviewed_section_guides(self):
        manifest = json.loads((reader.ROOT / "assets/reader-manifest.json").read_text())
        chapter = next(p for p in manifest["chapters"] if p["id"] == "ch01")
        content = json.loads((reader.ROOT / chapter["content"]).read_text())
        guides = chapter.get("sectionGuides", [])
        self.assertEqual(len({g["afterParagraph"] for g in guides}), len(guides))
        for guide in guides:
            reader.check_pedagogy(guide)
            self.assertEqual(reader.anchor_count(content, guide["afterParagraph"]), 1)
            reader.check_svg(reader.ROOT / guide["desktop"], 1, False, guide["id"])
            reader.check_svg(reader.ROOT / guide["mobile"], 1, True, guide["id"])

    def test_every_numbered_chapter_has_reviewed_explanatory_diagrams(self):
        manifest = json.loads((reader.ROOT / "assets/reader-manifest.json").read_text())
        for page in manifest["chapters"]:
            if not page["number"]:
                continue
            content = json.loads((reader.ROOT / page["content"]).read_text())
            reader.check_pedagogy(json.loads((reader.DIAGRAMS / f"{page['id']}.json").read_text()), overview=True)
            for guide in page.get("sectionGuides", []):
                self.assertTrue(reader.check_pedagogy(guide))
                self.assertEqual(reader.anchor_count(content, guide["afterParagraph"]), 1)
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
