import json
import unittest

import build_search_index as search


class SearchIndexTests(unittest.TestCase):
    def test_english_heading_stays_searchable_under_the_chinese_title(self):
        text = ("**CHAPTER 1**\n\n# Title\n\n# 标题\n\nEnglish paragraph.\n\n中文段落。\n\n"
                "## Sub\n\n## 小节\n\n- item\n\n#### deep\n\nMore.\n\n```\ncode\n```\n")
        self.assertEqual(list(search.sections(text)), [
            ("", "CHAPTER 1"),
            ("标题", "Title\nEnglish paragraph.\n中文段落。"),
            ("小节", "Sub\nitem\ndeep\nMore."),
        ])

    def test_index_covers_every_chapter_with_non_empty_entries(self):
        index = json.loads((search.ROOT / "assets/search-index.json").read_text())
        manifest = json.loads((search.ROOT / "assets/reader-manifest.json").read_text())
        self.assertEqual({e["route"] for e in index}, {c["route"] for c in manifest["chapters"]})
        for entry in index:
            self.assertEqual(set(entry), {"route", "chapter", "title", "text"})
            self.assertTrue(entry["title"] and entry["text"], entry["route"])


if __name__ == "__main__":
    unittest.main()
