import json
import tempfile
import unittest
from pathlib import Path

import build_reader_manifest as reader

TRANSLATED = {"java", "Java", "C++", "golang"}


class CodeVariantTests(unittest.TestCase):
    def test_every_java_cpp_and_go_example_has_a_python_rewrite_or_a_reason(self):
        manifest = json.loads((reader.ROOT / "assets/reader-manifest.json").read_text())
        for chapter in manifest["chapters"]:
            text = (reader.ROOT / chapter["source"]).read_text()
            expected = {t.content.replace("\t", "    ").strip() for t in reader.audit.MD.parse(text)
                        if t.type == "fence" and t.info.strip() in TRANSLATED}
            if not expected:
                self.assertNotIn("codeVariants", chapter, chapter["id"])
                continue
            variants = json.loads((reader.ROOT / chapter["codeVariants"]).read_text())
            self.assertEqual({v["source"] for v in variants}, expected, chapter["id"])
            for variant in variants:
                self.assertIn(variant["language"], {"java", "cpp", "go"})
                self.assertTrue(variant.get("python") or variant.get("note"), chapter["id"])

    def test_rewrite_must_parse_and_match_a_code_block(self):
        text = "Intro\n\n```java\nint x = 1;\n```\n"
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            (folder / "01.java").write_text("int x = 1;\n")
            with self.assertRaisesRegex(ValueError, "needs a Python rewrite"):
                reader.compile_code_variants(folder, text)
            (folder / "01.py").write_text("x = 1\n")
            self.assertEqual(reader.compile_code_variants(folder, text),
                             [{"language": "java", "source": "int x = 1;", "python": "x = 1"}])
            (folder / "01.py").write_text("x = = 1\n")
            with self.assertRaisesRegex(ValueError, "does not parse"):
                reader.compile_code_variants(folder, text)
            (folder / "01.py").unlink()
            (folder / "01.skip").write_text("No Python equivalent.\n")
            self.assertEqual(reader.compile_code_variants(folder, text)[0]["note"], "No Python equivalent.")
            (folder / "01.java").write_text("int y = 2;\n")
            with self.assertRaisesRegex(ValueError, "not a code block"):
                reader.compile_code_variants(folder, text)


if __name__ == "__main__":
    unittest.main()
