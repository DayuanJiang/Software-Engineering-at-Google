import unittest

import reader_content as reader


class ReaderContentTests(unittest.TestCase):
    source = (
        "The compiler checks `types`.[^1]\n\n"
        "编译器会检查 `类型`。\n\n"
        "> [^1]: A **type** check.  \n"
        "> 1 一次**类型**检查。\n\n"
        "Keep the rest.\n"
    )

    def review(self):
        return {"format": 2, "footnotes": [{
            "id": "1", "definitionLines": [5, 6],
            "english": "A **type** check.", "chinese": "一次**类型**检查。",
            "after": "编译器会检查 类型。"
        }]}

    def test_compiles_source_bound_notes_without_mutating_input(self):
        review = self.review()
        result = reader.compile_review("fixture", self.source, review)
        self.assertIn("<strong>type</strong>", result["footnotes"][0]["englishHtml"])
        self.assertEqual(result["sourceEdits"][0]["source"], "".join(self.source.splitlines(keepends=True)[4:6]))
        self.assertNotIn("englishHtml", review["footnotes"][0])

    def test_rejects_unreviewed_note_text(self):
        review = self.review()
        review["footnotes"][0]["chinese"] = "错误的内容。"
        with self.assertRaisesRegex(ValueError, "differs from source"):
            reader.compile_review("fixture", self.source, review)

    def test_does_not_remove_adjacent_body_with_definition(self):
        review = self.review()
        review["footnotes"][0]["definitionLines"] = [5, 8]
        with self.assertRaisesRegex(ValueError, "unaccounted"):
            reader.compile_review("fixture", self.source, review)

    def test_ambiguous_anchor_rejected(self):
        with self.assertRaisesRegex(ValueError, "Ambiguous"):
            reader.compile_review("fixture", self.source + "\n编译器会检查 `类型`。\n", self.review())

    def test_missing_note_cannot_be_reported_complete(self):
        with self.assertRaisesRegex(ValueError, "coverage"):
            reader.compile_review("fixture", self.source, {"format": 2, "footnotes": []})

    def test_inline_markup_and_existing_reference_do_not_break_anchor(self):
        self.assertEqual(reader.anchor_count("检查 **类型**[^1]。", "检查 类型。"), 1)
        self.assertEqual(reader.anchor_count("```text\n检查类型。\n```\n", "检查类型。"), 0)
        self.assertEqual(reader.anchor_count("XML 的 `<target>` 标签。", "XML 的 <target> 标签。"), 1)

    def test_reviewed_display_edit_is_applied_before_anchor_validation(self):
        source = self.source.replace("编译器会检查 `类型`。", "编译器会检查 `类型`（注1）。")
        review = self.review()
        review["textEdits"] = [{"source": "（注1）", "replacement": "", "reason": "Legacy note label."}]
        self.assertEqual(len(reader.compile_review("fixture", source, review)["sourceEdits"]), 1)

    def test_historical_disclosure_does_not_hide_blocking_mapping_issue(self):
        review = self.review()
        review["issues"] = ["An external source URL has not been checked."]
        reader.compile_review("fixture", self.source, review)
        review["blockingIssues"] = ["The note's corresponding sentence is unknown."]
        with self.assertRaisesRegex(ValueError, "mapping issues"):
            reader.compile_review("fixture", self.source, review)

    def test_malformed_definition_requires_reviewed_reason(self):
        source = self.source.replace("> [^1]:", "> 1")
        review = self.review()
        with self.assertRaisesRegex(ValueError, "Unexplained"):
            reader.compile_review("fixture", source, review)
        review["footnotes"][0]["reason"] = "The source uses a bare note number."
        reader.compile_review("fixture", source, review)

    def test_reviewed_pair_requires_existing_unique_chinese_counterpart(self):
        review = self.review()
        review["pairedSources"] = [{
            "english": "The compiler checks types.",
            "chinese": "编译器会检查 类型。",
            "reason": "Reviewed existing bilingual paragraphs."
        }]
        reader.compile_review("fixture", self.source, review)
        review["pairedSources"][0]["chinese"] = "不存在的译文。"
        with self.assertRaisesRegex(ValueError, "chinese prose pair"):
            reader.compile_review("fixture", self.source, review)

    def test_reviewed_tables_keep_matching_structure(self):
        source = "|Metric|Value|\n|---|---|\n|Speed|Fast|\n\n|指标|值|\n|---|---|\n|速度|快|\n"
        review = {"format": 2, "footnotes": [], "pairedTables": [
            {"englishIndex": 0, "chineseIndex": 1, "reason": "Reviewed corresponding rows."}
        ]}
        result = reader.compile_review("fixture", source, review)
        self.assertEqual(result["pairedTables"][0]["english"]["rows"], 2)
        with self.assertRaisesRegex(ValueError, "structures differ"):
            reader.compile_review("fixture", source + "|额外|行|\n", review)
        review["pairedTables"][0]["chineseIndex"] = 0
        with self.assertRaisesRegex(ValueError, "indices"):
            reader.compile_review("fixture", source, review)


if __name__ == "__main__":
    unittest.main()
