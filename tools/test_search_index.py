import json
import unittest

import build_search_index as search


class SearchIndexTests(unittest.TestCase):
    def test_english_heading_stays_searchable_under_the_chinese_title(self):
        chapter = {"units": [
            {"kind": "heading", "level": 1, "anchor": "title", "source": "# Title", "target": "# 标题"},
            {"kind": "paragraph", "source": "English paragraph.[^1]", "target": "中文段落。"},
            {"kind": "heading", "level": 2, "anchor": "sub", "source": "## Sub", "target": "## 小节"},
            {"kind": "list", "source": "- item", "target": "- 条目"},
            {"kind": "heading", "level": 4, "anchor": "deep", "source": "#### deep", "target": "#### 深"},
            {"kind": "code", "source": "```\ncode\n```", "target": None},
            {"kind": "paragraph", "source": "More.", "target": "更多。"},
        ]}
        self.assertEqual(list(search.sections(chapter)), [
            ("标题", "title", "Title\nEnglish paragraph.\n中文段落。"),
            ("小节", "sub", "Sub\n- item\n- 条目\n#### deep\n#### 深\nMore.\n更多。"),
        ])

    def test_index_covers_every_chapter_with_non_empty_entries(self):
        index = json.loads((search.ROOT / "assets/search-index.json").read_text())
        manifest = json.loads((search.ROOT / "assets/reader-manifest.json").read_text())
        self.assertEqual({e["route"] for e in index}, {c["route"] for c in manifest["chapters"]})
        for entry in index:
            self.assertEqual(set(entry), {"route", "chapter", "title", "anchor", "text"})
            self.assertTrue(entry["title"] and entry["text"], entry["route"])


if __name__ == "__main__":
    unittest.main()
