import unittest
from unittest import mock

import book_review as book
import translation_audit as audit


class BookReviewTests(unittest.TestCase):
    def test_reconstruct_preserves_english_and_eof(self):
        before = "English.\n\n中文原稿。".encode()
        after = book.reconstruct(before, {"3": "中文修改稿。"})
        self.assertEqual(after, "English.\n\n中文修改稿。".encode())

    def test_reconstruct_rejects_non_chinese_and_empty_edits(self):
        before = "English.\n中文。\n".encode()
        for edits in ({"1": "英文。"}, {"2": ""}, {"2": "删除\n换行"}, {"5": "越界"}):
            with self.assertRaises(ValueError):
                book.reconstruct(before, edits)

    def test_complete_chinese_coverage(self):
        before = "English.\n\n中文。\n".encode()
        after = "English.\n\n修改中文。\n".encode()
        manifest = {"replacements": {"3": "修改中文。"}, "reviewed_unchanged_lines": [], "held_lines": {}}
        self.assertEqual(book.validate("fixture.md", before, after, manifest)["changed_lines"], 1)
        manifest["replacements"] = {}
        with self.assertRaises(ValueError):
            book.validate("fixture.md", before, after, manifest)

    def test_holds_are_visible_not_completed(self):
        before = "English.\n\n中文。\n".encode()
        manifest = {"replacements": {}, "reviewed_unchanged_lines": [], "held_lines": {"3": "Needs source review"}}
        result = book.validate("fixture.md", before, before, manifest)
        self.assertEqual(result["held_line_count"], 1)

    def test_english_change_rejected(self):
        before = "English.\n\n中文。\n".encode()
        after = "Altered English.\n\n中文。\n".encode()
        manifest = {"replacements": {}, "reviewed_unchanged_lines": [3], "held_lines": {}}
        with self.assertRaises(ValueError):
            book.validate("fixture.md", before, after, manifest)

    def test_code_change_rejected(self):
        before = "```python\nprint('中文')\n```\n".encode()
        after = "```python\nprint('修改')\n```\n".encode()
        manifest = {"replacements": {"2": "print('修改')"}, "reviewed_unchanged_lines": [], "held_lines": {}}
        with self.assertRaises(ValueError):
            book.validate("fixture.md", before, after, manifest)

    def test_navigation_only_labels_are_ignored(self):
        before = "[旧名称](./zh-cn/Foreword.md)"
        after = "[序言](./zh-cn/Foreword.md)"
        wrong = "[序言](./zh-cn/Preface.md)"
        self.assertEqual(book.without_nav_labels(before), book.without_nav_labels(after))
        self.assertNotEqual(book.without_nav_labels(before), book.without_nav_labels(wrong))

    def test_english_trailing_whitespace_fix_is_applied_but_text_changes_are_rejected(self):
        before = "- *Term*\n    Text.\n\n中文。\n".encode()
        fix = {"line": 1, "before": "- *Term*", "after": "- *Term*  "}
        after = book.reconstruct(before, {}, [fix])
        self.assertEqual(after, "- *Term*  \n    Text.\n\n中文。\n".encode())
        for bad in ({"line": 1, "before": "- *Term*", "after": "- *Word*  "},
                    {"line": 1, "before": "- *Other*", "after": "- *Other*  "},
                    {"line": 4, "before": "中文。", "after": "中文。  "}):
            with self.assertRaises(ValueError):
                book.reconstruct(before, {}, [bad])
        manifest = {"replacements": {}, "reviewed_unchanged_lines": [4], "held_lines": {}}
        with self.assertRaises(ValueError):
            book.validate("fixture.md", before, after, manifest)
        with mock.patch.object(book, "english_format_fixes", return_value=[fix]):
            self.assertEqual(book.validate("fixture.md", before, after, manifest)["english_format_exceptions"], [fix])

    def test_registered_heading_edit_keeps_level_and_counts_as_reviewed(self):
        before = "### UAT\n\nText.\n\n## 内容提要\n\n中文。\n".encode()
        fixes = [
            {"line": 1, "kind": "heading", "before": "### UAT", "after": "### UAT 用户验收测试", "reason": "补译"},
            {"line": 5, "kind": "heading", "before": "## 内容提要", "after": "## TL;DRs  内容提要", "reason": "统一"},
        ]
        after = book.reconstruct(before, {}, fixes)
        self.assertEqual(after.decode().splitlines()[0], "### UAT 用户验收测试")
        manifest = {"replacements": {"7": "中文。"}, "reviewed_unchanged_lines": [], "held_lines": []}
        with mock.patch.object(book, "english_format_fixes", return_value=fixes):
            self.assertEqual(book.validate("fixture.md", before, after, manifest)["english_lines"], 1)
            with self.assertRaises(ValueError):  # a registered line may not also be listed as reviewed-unchanged
                book.validate("fixture.md", before, after, {**manifest, "reviewed_unchanged_lines": [5]})
        with self.assertRaises(ValueError):  # heading level must not change
            book.reconstruct(before, {}, [{**fixes[0], "after": "## UAT 用户验收测试"}])
        with self.assertRaises(ValueError):  # without the heading kind, added text is not a whitespace fix
            book.reconstruct(before, {}, [{k: v for k, v in fixes[0].items() if k != "kind"}])
        with self.assertRaises(ValueError):  # unregistered heading translation
            book.validate("fixture.md", before, after, manifest)

    def test_link_target_change_rejected(self):
        before = "[中文](one.md)\n".encode()
        after = "[中文](two.md)\n".encode()
        manifest = {"replacements": {"1": "[中文](two.md)"}, "reviewed_unchanged_lines": [], "held_lines": {}}
        with self.assertRaises(ValueError):
            book.validate("fixture.md", before, after, manifest)


if __name__ == "__main__":
    unittest.main()
