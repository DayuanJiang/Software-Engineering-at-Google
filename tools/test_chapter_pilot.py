import unittest

import chapter_pilot as pilot
import translation_audit as audit


class PilotTests(unittest.TestCase):
    def test_chinese_punctuation_normalization(self):
        self.assertEqual(pilot.normalize_chinese_line("中文,标点(示例)!"), "中文，标点（示例）！")

    def test_english_heading_prefix_is_not_normalized(self):
        line = '### Why “Nothing Changes”? 中文标题？'
        self.assertEqual(pilot.normalize_chinese_line(line), line)

    def test_technical_punctuation_is_preserved(self):
        line = "C++ 的 std::string 使用5 GiB 内存。"
        self.assertEqual(pilot.normalize_chinese_line(line), line)

    def test_inline_code_requires_separate_review(self):
        with self.assertRaises(ValueError):
            pilot.normalize_chinese_line("中文 `x,y`。")

    def test_links_require_separate_review(self):
        with self.assertRaises(ValueError):
            pilot.normalize_chinese_line("[中文](https://example.com/x)。")

    def test_materialization_rejects_english_edits(self):
        original = "English source.\n中文。\n".encode()
        manifest = {"baseline_sha256": audit.digest(original), "replacements": {"1": "英文改写。"}}
        with self.assertRaises(ValueError):
            pilot.materialize(manifest, original)

    def test_materialization_rejects_wrong_snapshot(self):
        with self.assertRaises(ValueError):
            pilot.materialize({"baseline_sha256": "wrong", "replacements": {}}, b"anything")

    def test_indented_chinese_quote_is_explicit_exception(self):
        before = "    中文引文。\n".encode()
        after = "    修改引文。\n".encode()
        with self.assertRaises(ValueError):
            pilot.validate_protected("sample.md", before, after, [])
        result = pilot.validate_protected("sample.md", before, after, [1])
        self.assertEqual(len(result["prose_code_exceptions"]), 1)

    def test_executable_code_cannot_be_exempted(self):
        before = b"```python\nprint(1)\n```\n"
        after = b"```python\nprint(2)\n```\n"
        with self.assertRaises(ValueError):
            pilot.validate_protected("sample.md", before, after, [1])

    def test_chapter_matches_reviewed_manifest(self):
        result = pilot.verify(check_other_sources=False)
        self.assertEqual(result["reviewed_chinese_lines"], 159)
        self.assertEqual(result["edited_chinese_lines"], 135)
        self.assertEqual(result["scope"], "chapter_only")
        self.assertIsNone(result["other_source_files_unchanged"])
        self.assertEqual(result["punctuation_residuals"], 0)

    def test_known_mistranslations_are_fixed(self):
        manifest, _, _, expected = pilot.load()
        lines = expected.decode().splitlines()
        expected_phrases = {
            29: "执行生命周期",
            264: "变更适配规则",
            300: "回归缺陷",
            356: "更低",
            450: "5 GiB",
            527: "语义化版本管理",
            561: "都不可避免",
        }
        for line, phrase in expected_phrases.items():
            self.assertIn(phrase, lines[line - 1])
        self.assertEqual(manifest["source_gap"]["line"], 136)

    def test_trailing_spaces_only_preserve_existing_markdown_breaks(self):
        _, _, original, expected = pilot.load()
        for before, after in zip(original.decode().splitlines(), expected.decode().splitlines()):
            if after.endswith(" ") and before != after:
                self.assertTrue(before.endswith("  "))
                self.assertTrue(after.endswith("  "))


if __name__ == "__main__":
    unittest.main()
