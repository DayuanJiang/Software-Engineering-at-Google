import unittest

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

    def test_link_target_change_rejected(self):
        before = "[中文](one.md)\n".encode()
        after = "[中文](two.md)\n".encode()
        manifest = {"replacements": {"1": "[中文](two.md)"}, "reviewed_unchanged_lines": [], "held_lines": {}}
        with self.assertRaises(ValueError):
            book.validate("fixture.md", before, after, manifest)


if __name__ == "__main__":
    unittest.main()
