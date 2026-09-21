import json
import unittest

import build_chapter_figures as figures
import build_reader_manifest as reader


class ChapterFigureTests(unittest.TestCase):
    def test_wrap_respects_width_and_punctuation(self):
        wrapped = figures.wrap("测试代码宁可重复也要直白，别把逻辑和条件放进测试里。", 15, 150)
        for line in wrapped:
            self.assertLessEqual(figures.width(line, 15), 150 + 15)
            self.assertNotIn(line[0], figures.CLOSING)
        self.assertEqual(figures.wrap("Live at Head：一起改、一起测", 15, 400), ["Live at Head：一起改、一起测"])

    def test_text_budgets_fail_the_build_instead_of_overflowing(self):
        with self.assertRaisesRegex(ValueError, "too wide"):
            figures.fit("这一行文字明显超过了给它的宽度预算", 20, 100, "fixture")
        with self.assertRaisesRegex(ValueError, "allows 1"):
            figures.lines("需要换行的长句子，需要换行的长句子，需要换行的长句子", 15, 120, 1, "fixture")

    def test_every_chapter_builds_four_valid_figures(self):
        for path in sorted(figures.DIAGRAMS.glob("ch??.json")):
            metadata = json.loads(path.read_text())
            built = figures.build(metadata)
            self.assertEqual(set(built), {metadata["desktop"], metadata["mobile"], metadata["storyDesktop"], metadata["storyMobile"]})
            for relative, svg in built.items():
                self.assertEqual((figures.ROOT / relative).read_text(), svg, f"{relative} is stale; run build_chapter_figures.py")
            self.assertIn(metadata["map"]["form"], figures.FORMS)
            for part in metadata["map"]["parts"]:
                self.assertIn(part["icon"], figures.ICONS)
            for act in metadata["story"]["acts"]:
                self.assertIn(act["icon"], figures.ICONS)
                self.assertIn(act.get("tone", "pri"), figures.TONES)

    def test_generated_svg_passes_reader_checks(self):
        metadata = json.loads((figures.DIAGRAMS / "ch13.json").read_text())
        for relative in figures.build(metadata):
            mobile = relative.endswith("-mobile.svg")
            reader.check_svg(figures.ROOT / relative, 13, mobile, story="story" in relative)


if __name__ == "__main__":
    unittest.main()
