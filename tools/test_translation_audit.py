import json
import re
from pathlib import Path
import tempfile
import unittest

import translation_audit as audit


class MarkdownTests(unittest.TestCase):
    def test_bilingual_quote_is_not_all_english(self):
        doc = audit.parse_document("chapter.md", "> An English sentence.\n>\n> 一句中文。\n")
        self.assertEqual([s["language"] for s in doc["segments"]], ["en", "zh"])
        groups = audit.align_segments(doc["segments"])
        self.assertEqual(groups[0]["status"], "adjacent_1_to_1")

    def test_code_is_not_counted_as_prose(self):
        doc = audit.parse_document("chapter.md", "```python\nprint('test double')\n```\n")
        self.assertEqual(doc["segments"], [])
        self.assertEqual(len(doc["codes"]), 1)

    def test_inline_code_links_and_images_are_protected(self):
        doc = audit.parse_document("chapter.md", "Use `containsKey()` and [link](a.md).\n\n![图](img%20one.png)\n")
        self.assertEqual(doc["codes"][0]["content"], "containsKey()")
        self.assertEqual([r["target"] for r in doc["links"]], ["a.md", "img%20one.png"])

    def test_mixed_heading(self):
        doc = audit.parse_document("chapter.md", "## Test Doubles 测试替代\n")
        self.assertEqual([s["text"] for s in doc["segments"]], ["Test Doubles", "测试替代"])
        self.assertEqual(audit.align_segments(doc["segments"])[0]["status"], "adjacent_1_to_1")

    def test_parallel_lists(self):
        doc = audit.parse_document("chapter.md", "- First item\n- Second item\n\n- 第一项\n- 第二项\n")
        groups = audit.align_segments(doc["segments"])
        self.assertEqual([g["status"] for g in groups], ["ordered_run", "ordered_run"])

    def test_mismatched_runs_are_ambiguous(self):
        doc = audit.parse_document("chapter.md", "First paragraph.\n\nSecond paragraph.\n\n中文合段。\n")
        self.assertEqual(audit.align_segments(doc["segments"])[0]["status"], "ambiguous")

    def test_never_pair_across_files(self):
        first = audit.parse_document("a.md", "English paragraph.\n")
        second = audit.parse_document("b.md", "中文段落。\n")
        groups = audit.align_segments(first["segments"] + second["segments"])
        self.assertEqual(groups[0]["status"], "unpaired")

    def test_never_pair_heading_with_body(self):
        doc = audit.parse_document("chapter.md", "# Heading\n\n中文正文。\n")
        self.assertEqual(audit.align_segments(doc["segments"])[0]["status"], "unpaired")

    def test_footnote_markers_not_in_code(self):
        doc = audit.parse_document("chapter.md", "See note[^1].\n\n> [^1]: A definition.\n\n```\n[^2]\n```\n")
        self.assertEqual([(f["id"], f["definition"]) for f in doc["footnotes"]], [("1", False), ("1", True)])

    def test_source_position_for_table(self):
        doc = audit.parse_document("chapter.md", "| English | 中文 |\n| --- | --- |\n| Test | 测试 |\n")
        self.assertTrue(all(s["line"] > 0 for s in doc["segments"]))
        self.assertEqual({s["kind"] for s in doc["segments"]}, {"table"})

    def test_chinese_edit_does_not_change_protected_english(self):
        a = audit.protected(audit.parse_document("a.md", "English *text*.\n\n中文原稿。\n"))
        b = audit.protected(audit.parse_document("a.md", "English *text*.\n\n中文修改稿。\n"))
        self.assertNotEqual(a.pop("sha256"), b.pop("sha256"))
        self.assertEqual(a, b)

    def test_english_markdown_edit_detected(self):
        a = audit.protected(audit.parse_document("a.md", "English *text*.\n\n中文。\n"))
        b = audit.protected(audit.parse_document("a.md", "English text.\n\n中文。\n"))
        self.assertNotEqual(a["english_line_hashes"], b["english_line_hashes"])

    def test_alias_longest_first(self):
        counts = audit.alias_matches("测试替代和测试替代品", ["测试替代", "测试替代品"])
        self.assertEqual(counts, {"测试替代": 1, "测试替代品": 1})

    def test_scan_preserves_raw_line_endings_in_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "zh-cn").mkdir()
            raw = b"English paragraph.\r\n\r\n"
            (root / "zh-cn" / "sample.md").write_bytes(raw)
            documents, _, _ = audit.scan(root)
            self.assertEqual(documents[0]["sha256"], audit.digest(raw))


class NLPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import spacy
        cls.nlp = spacy.load("en_core_web_sm")

    def test_plural_terms_normalized_and_occurrences_deduplicated(self):
        text = "A test double replaces a dependency. Test doubles are useful."
        terms = audit.extract_terms(self.nlp(text))
        doubles = [r for r in terms if r["term"] == "test double"]
        self.assertTrue(any(len(r["signals"]) > 1 for r in doubles))
        segment = {"id": "test:s1", "file": "test.md", "kind": "body", "text": text}
        definitions = {"test double": {"forms": {"test double", "Test doubles"}, "signals": set()}}
        counted = audit.count_surface_forms([segment], definitions)
        self.assertEqual(counted["test double"]["frequency"], 2)

    def test_recount_ignores_pos_and_handles_footnotes(self):
        segment = {"id": "test:s1", "file": "test.md", "kind": "body",
                   "text": "Code Reviews; code review[^13]; code reviewer. Critique displays results."}
        definitions = {
            "code review": {"forms": {"code review", "code reviews"}, "signals": set()},
            "critique": {"forms": {"Critique"}, "signals": set()},
        }
        counted = audit.count_surface_forms([segment], definitions)
        self.assertEqual(counted["code review"]["frequency"], 2)
        self.assertEqual(counted["critique"]["frequency"], 1)

    def test_brittle_and_flaky_are_different(self):
        terms = {r["term"] for r in audit.extract_terms(self.nlp("Brittle tests and flaky tests cause problems."))}
        self.assertIn("brittle test", terms)
        self.assertIn("flaky test", terms)

    def test_acronym_and_proper_name(self):
        terms = audit.extract_terms(self.nlp("Critique uses an API for code review."))
        api = next(r for r in terms if r["term"] == "api")
        self.assertIn("acronym", api["signals"])
        self.assertTrue(any(r["term"] == "critique" for r in terms))

    def test_prepositional_term(self):
        terms = {r["term"] for r in audit.extract_terms(self.nlp("This repository is the source of truth."))}
        self.assertIn("source of truth", terms)

    def test_chinese_negation_is_preserved(self):
        import jieba
        import jieba.posseg
        tokenizer = jieba.Tokenizer()
        tokenizer.tmp_dir = str(audit.ROOT / ".cache")
        counts = audit.chinese_candidates("不稳定测试", jieba.posseg.POSTokenizer(tokenizer))
        self.assertIn("不稳定测试", counts)
        self.assertNotIn("稳定测试", counts)


@unittest.skipUnless((audit.DEFAULT_OUT / "candidates.json").exists(), "Generate corpus artifacts first.")
class ArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = json.loads((audit.DEFAULT_OUT / "candidates.json").read_text())
        cls.segments = [
            json.loads(line) for line in (audit.DEFAULT_OUT / "segments.jsonl").read_text().splitlines()
        ]
        cls.index = {s["id"]: s for s in cls.segments}

    def test_unique_segment_ids(self):
        self.assertEqual(len(self.index), len(self.segments))

    def test_every_frequency_has_unique_evidence_and_consistent_totals(self):
        for row in self.rows:
            with self.subTest(term=row["term"]):
                self.assertEqual(row["frequency"], len(row["evidence"]))
                for field in ("forms", "documents", "sections"):
                    self.assertEqual(row["frequency"], sum(row[field].values()))
                occurrences = {(e["segment"], e["start"], e["end"]) for e in row["evidence"]}
                self.assertEqual(len(occurrences), len(row["evidence"]))
                for segment_id, start, end in occurrences:
                    segment = self.index[segment_id]
                    self.assertEqual(segment["language"], "en")
                    self.assertLess(start, end)
                    self.assertGreaterEqual(start, 0)
                    self.assertLessEqual(end, len(segment["text"]))

    def test_core_phrase_counts_against_independent_search(self):
        patterns = {
            "test double": r"\btest doubles?\b",
            "brittle test": r"\bbrittle tests?\b",
            "flaky test": r"\bflaky tests?\b",
            "code review": r"\bcode reviews?\b",
            "critique": r"\bcritique\b",
        }
        english = [s["text"] for s in self.segments if s["language"] == "en" and s["kind"] != "metadata"]
        rows = {r["term"]: r for r in self.rows}
        for key, pattern in patterns.items():
            expected = sum(len(re.findall(pattern, text, re.I)) for text in english)
            self.assertEqual(rows[key]["frequency"], expected, key)

    def test_alignment_covers_each_nonmetadata_english_segment_once(self):
        groups = json.loads((audit.DEFAULT_OUT / "alignments.json").read_text())
        expected = {s["id"] for s in self.segments if s["language"] == "en" and s["kind"] != "metadata"}
        covered = [sid for group in groups for sid in group["english"]]
        self.assertEqual(set(covered), expected)
        self.assertEqual(len(covered), len(set(covered)))

    def test_book_files_still_match_reviewed_state(self):
        baseline = json.loads((audit.DEFAULT_OUT / "baseline.json").read_text())
        if (audit.DEFAULT_OUT / "chapters").exists():
            import book_review
            result = book_review.verify_all(final=True)
            self.assertEqual(result["verified_documents"], 28)
        elif (audit.DEFAULT_OUT / "chapter-01" / "edits.json").exists():
            import chapter_pilot
            result = chapter_pilot.verify()
            self.assertEqual(result["other_source_files_unchanged"], len(baseline["files"]) - 1)
        else:
            self.assertEqual(audit.verify_baseline(audit.ROOT, baseline, exact=True), [])


if __name__ == "__main__":
    unittest.main()
