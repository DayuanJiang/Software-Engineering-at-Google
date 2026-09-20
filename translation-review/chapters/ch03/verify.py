"""Record and verify only Chapter 3; never modify the chapter or shared artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

SOURCE = "zh-cn/Chapter-3_Knowledge_Sharing/Chapter-3_Knowledge_Sharing.md"
COMMIT = "679725c08143c724598a2b89b94b8c8e4fa47688"
HOLDS = {
    87: "Existing translator explanation in a fenced code block; preserved verbatim under the code-protection rule, not counted as completed prose.",
    433: "Chinese footnote continuation parsed as an indented code block; preserved verbatim pending parent review of the markup, not counted as completed prose.",
}
LINK = re.compile(r"!?\[[^\]\n]*\]\([^)\n]*\)")
INLINE = re.compile(r"(`+).*?\1")
LEADING = re.compile(r"^\s*(?:>\s*)*(?:(?:#{1,6}|[-+*]|\d+[.)])\s+)?")
PUNCTUATION = {",": "\uff0c", ":": "\uff1a", ";": "\uff1b", "?": "\uff1f",
               "!": "\uff01", "(": "\uff08", ")": "\uff09"}
EXTRA = set("\u201c\u201d\u2018\u2019\u00b7\u2014\u2026")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def is_cjk(char: str) -> bool:
    return bool(char) and (
        "\u3400" <= char <= "\u9fff"
        or "\u3000" <= char <= "\u303f"
        or "\uff00" <= char <= "\uffef"
        or char in EXTRA
    )


def normalized_punctuation(line: str) -> str:
    """Apply the skill's punctuation pass only outside protected inline content."""
    prefix = ""
    if line.lstrip().startswith("#"):
        first_han = audit.HAN.search(line)
        if first_han:
            prefix, line = line[:first_han.start()], line[first_han.start():]
    stored = []

    def protect(match):
        stored.append(match[0])
        return f"\x00{len(stored) - 1}\x00"

    for pattern in (LINK, INLINE, audit.URL):
        line = pattern.sub(protect, line)
    chars = []
    opening = True
    for char in line:
        if char == '"':
            chars.append("\u201c" if opening else "\u201d")
            opening = not opening
        elif char in "\u300c\u300d\u300e\u300f":
            chars.append(dict(zip("\u300c\u300d\u300e\u300f", "\u201c\u201d\u2018\u2019"))[char])
        else:
            chars.append(char)
    for index, char in enumerate(chars):
        if char in PUNCTUATION and (
            is_cjk(chars[index - 1] if index else "")
            or is_cjk(chars[index + 1] if index + 1 < len(chars) else "")
        ):
            chars[index] = PUNCTUATION[char]
    return prefix + re.sub(r"\x00(\d+)\x00", lambda m: stored[int(m[1])], "".join(chars))


def token_shape(source: str):
    tokens = audit.MD.parse(source)
    return [
        (token.type, token.tag, token.nesting, token.markup, token.map,
         [(child.type, child.tag, child.nesting, child.markup)
          for child in token.children or []])
        for token in tokens
    ]


def bare_urls(line: str):
    return [
        url
        for token in audit.MD.parseInline(line)
        for child in token.children or []
        if child.type == "text"
        for url in audit.URL.findall(child.content)
    ]


def read_inputs():
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Baseline commit changed")
    original = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"])
    current = (ROOT / SOURCE).read_bytes()
    before = audit.parse_document(SOURCE, original.decode())
    after = audit.parse_document(SOURCE, current.decode())
    old_protected, new_protected = audit.protected(before), audit.protected(after)
    require(old_protected == baseline["files"][SOURCE], "Git snapshot differs from baseline")
    mismatches = [
        key for key in old_protected
        if key != "sha256" and old_protected[key] != new_protected[key]
    ]
    require(not mismatches, f"Protected content changed: {mismatches}")
    require(token_shape(original.decode()) == token_shape(current.decode()),
            "Markdown block or inline token structure changed")
    old_lines = original.decode().splitlines(keepends=True)
    new_lines = current.decode().splitlines(keepends=True)
    require(len(old_lines) == len(new_lines), "Physical line count changed")
    chinese = {i for i, line in enumerate(old_lines, 1) if audit.HAN.search(line)}
    changed = {}
    for number, (old, new) in enumerate(zip(old_lines, new_lines), 1):
        if old == new:
            continue
        require(number in chinese, f"Non-Chinese line changed: {number}")
        require(number not in HOLDS, f"Held line changed: {number}")
        require(LEADING.match(old)[0] == LEADING.match(new)[0],
                f"Leading Markdown or indentation changed: {number}")
        require(re.search(r"\s*$", old)[0] == re.search(r"\s*$", new)[0],
                f"Trailing whitespace or line ending changed: {number}")
        require(LINK.findall(old) == LINK.findall(new), f"Raw link markup changed: {number}")
        require(bare_urls(old) == bare_urls(new), f"Raw URL changed: {number}")
        require(audit.FOOTNOTE.findall(old) == audit.FOOTNOTE.findall(new),
                f"Footnote sequence changed: {number}")
        if old.lstrip().startswith("#"):
            first = audit.HAN.search(old).start()
            require(old[:first] == new[:first], f"English heading prefix changed: {number}")
        require(normalized_punctuation(new) == new, f"Punctuation residue: {number}")
        changed[str(number)] = new.rstrip("\r\n")
    code_lines = set()
    for token in audit.MD.parse(original.decode()):
        if token.type in {"fence", "code_block"}:
            code_lines.update(range(token.map[0] + 1, token.map[1] + 1))
    require(chinese & code_lines == set(HOLDS), "Protected Chinese lines differ from holds")
    return original, current, old_protected, chinese, changed, len(old_lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true",
                        help="Create the mechanically derived manifest and verification report")
    args = parser.parse_args()
    original, current, protected, chinese, replacements, line_count = read_inputs()
    expected = {
        "source": SOURCE,
        "baseline_sha256": audit.digest(original),
        "replacements": replacements,
        "reviewed_unchanged_lines": sorted(chinese - {int(n) for n in replacements} - set(HOLDS)),
        "held_lines": {str(number): reason for number, reason in HOLDS.items()},
    }
    manifest_path = OUT / "edits.json"
    if args.record:
        require(not manifest_path.exists(), "Refusing to overwrite an existing review manifest")
        manifest_path.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n")
    manifest = json.loads(manifest_path.read_text())
    require(manifest == expected, "Chapter and review manifest differ")
    reconstructed = original.decode().splitlines(keepends=True)
    for key, text in manifest["replacements"].items():
        index = int(key) - 1
        ending = reconstructed[index][len(reconstructed[index].rstrip("\r\n")):]
        reconstructed[index] = text + ending
    require("".join(reconstructed).encode() == current, "Manifest does not reproduce chapter bytes")
    result = {
        "status": "PASS_WITH_HOLDS",
        "source": SOURCE,
        "git_commit": COMMIT,
        "baseline_sha256": audit.digest(original),
        "result_sha256": audit.digest(current),
        "physical_lines": line_count,
        "chinese_lines_encountered": len(chinese),
        "edited_chinese_lines": len(replacements),
        "reviewed_unchanged_lines": len(manifest["reviewed_unchanged_lines"]),
        "completed_chinese_lines": len(chinese) - len(HOLDS),
        "held_chinese_lines": len(HOLDS),
        "held_lines": manifest["held_lines"],
        "protected_counts": {key: len(value) for key, value in protected.items()
                             if isinstance(value, list)},
        "protection_mismatches": [],
        "markdown_token_shape_unchanged": True,
        "raw_links_and_urls_unchanged": True,
        "line_endings_and_hard_breaks_unchanged": True,
        "non_chinese_lines_byte_identical": True,
        "english_heading_prefixes_unchanged": True,
        "manifest_reproduces_chapter_bytes": True,
        "punctuation_normalization_changes_needed": 0,
        "scope": "Only Chapter 3; no whole-repository assertions, code exceptions, or baseline changes.",
    }
    report_path = OUT / "verification.json"
    if args.record:
        report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    else:
        require(json.loads(report_path.read_text()) == result, "Verification report is stale")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
