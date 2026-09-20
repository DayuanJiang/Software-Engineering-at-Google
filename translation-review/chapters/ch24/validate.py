"""Record and strictly validate only the Chapter 24 translation edits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import translation_audit as audit

DIRECTORY = Path(__file__).resolve().parent
SOURCE = "zh-cn/Chapter-24_Continuous_Delivery/Chapter-24_Continuous_Delivery.md"
COMMIT = "110720f031b43e18708fdc38af03269b65b3cc41"
RETAINED = [6, 58, 61, 62, 64, 67, 70, 130, 184, 244, 254]
HOLDS = {
    "27": "Chinese quotation is inside the original indented code block. "
    "Its literal launch/landing wording and missing extraordinary-outcomes clause "
    "need review, but the brief prohibits changing this protected prose.",
    "28": "Chinese attribution belongs to the same protected indented code block. "
    "Kept byte-for-byte pending review of the quotation as a whole; not completed.",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_original():
    baseline = json.loads((ROOT / "translation-review/baseline.json").read_text())
    require(baseline["git_commit"] == COMMIT, "Unexpected baseline commit")
    raw = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{COMMIT}:{SOURCE}"])
    expected = baseline["files"][SOURCE]
    require(audit.digest(raw) == expected["sha256"], "Original SHA-256 mismatch")
    require(audit.protected(audit.parse_document(SOURCE, raw.decode())) == expected,
            "Parser output differs from the recorded baseline")
    return raw


def is_cjk(character):
    return bool(character) and (
        "\u3400" <= character <= "\u9fff"
        or "\u3000" <= character <= "\u303f"
        or "\uff00" <= character <= "\uffef"
        or character in "\u201c\u201d\u2018\u2019\u00b7\u2014\u2026"
    )


def normalize_punctuation(line):
    # Protect the English prefix of bilingual headings, including its punctuation.
    prefix = ""
    first_han = audit.HAN.search(line)
    if line.startswith("#") and first_han:
        prefix, line = line[:first_han.start()], line[first_han.start():]
    mapping = dict(zip(",;:?!()", "\uff0c\uff1b\uff1a\uff1f\uff01\uff08\uff09"))
    directions = {
        "\u300c": "\u201c", "\u300d": "\u201d",
        "\u300e": "\u2018", "\u300f": "\u2019",
    }
    characters = []
    opening = True
    for character in line:
        if character == '"':
            characters.append("\u201c" if opening else "\u201d")
            opening = not opening
        else:
            characters.append(directions.get(character, character))
    for i, character in enumerate(characters):
        previous = characters[i - 1] if i else ""
        following = characters[i + 1] if i + 1 < len(characters) else ""
        if character in mapping and (is_cjk(previous) or is_cjk(following)):
            characters[i] = mapping[character]
    return prefix + "".join(characters)


def token_shape(tokens):
    return [
        {
            "type": token.type, "tag": token.tag, "nesting": token.nesting,
            "level": token.level, "map": token.map, "markup": token.markup,
            "attrs": token.attrs, "hidden": token.hidden, "block": token.block,
            "children": token_shape(token.children or []),
        }
        for token in tokens
    ]


def validate(before, after, manifest):
    require(manifest["source"] == SOURCE, "Manifest source mismatch")
    require(manifest["baseline_sha256"] == audit.digest(before), "Manifest hash mismatch")
    old_lines = before.decode().splitlines(keepends=True)
    new_lines = after.decode().splitlines(keepends=True)
    require(len(old_lines) == len(new_lines), "Physical line count changed")
    chinese = {i for i, line in enumerate(old_lines, 1) if audit.HAN.search(line)}
    replacements = manifest["replacements"]
    changed = {int(i) for i in replacements}
    retained = set(manifest["reviewed_unchanged_lines"])
    held = {int(i) for i in manifest["held_lines"]}
    require(not (changed & retained or changed & held or retained & held),
            "Overlapping coverage categories")
    require(changed | retained | held == chinese, "Incomplete Chinese-line coverage")
    require(manifest["reviewed_unchanged_lines"] == RETAINED, "Retained review list changed")
    require(manifest["held_lines"] == HOLDS, "Hold decisions changed")
    observed_changes = set()
    for i, (old, new) in enumerate(zip(old_lines, new_lines), 1):
        old_body, new_body = old.rstrip("\r\n"), new.rstrip("\r\n")
        require(old[len(old_body):] == new[len(new_body):], f"Line ending changed: {i}")
        require(re.match(r"^[ \t\u200b]*", old_body)[0]
                == re.match(r"^[ \t\u200b]*", new_body)[0], f"Indentation changed: {i}")
        require(re.search(r"[ \t]*$", old_body)[0]
                == re.search(r"[ \t]*$", new_body)[0], f"Trailing whitespace changed: {i}")
        require(old_body.count("\u200b") == new_body.count("\u200b"),
                f"Zero-width layout character changed: {i}")
        if old_body.startswith("#") and audit.HAN.search(old_body):
            offset = audit.HAN.search(old_body).start()
            require(new_body[:offset] == old_body[:offset], f"Heading prefix changed: {i}")
        if old != new:
            require(i in chinese and audit.HAN.search(new_body), f"Non-Chinese edit: {i}")
            observed_changes.add(i)
        if i in changed:
            replacement = replacements[str(i)]
            require("\n" not in replacement and "\r" not in replacement,
                    f"Multiline replacement: {i}")
            require(new_body == replacement, f"Manifest does not reconstruct line: {i}")
            require(normalize_punctuation(new_body) == new_body,
                    f"Chinese punctuation needs normalization: {i}")
        else:
            require(old == new, f"Unrecorded change: {i}")
    require(observed_changes == changed, "Redundant or missing replacements")
    old_doc = audit.parse_document(SOURCE, before.decode())
    new_doc = audit.parse_document(SOURCE, after.decode())
    old_protected, new_protected = audit.protected(old_doc), audit.protected(new_doc)
    for key in old_protected:
        if key != "sha256":
            require(old_protected[key] == new_protected[key], f"Protected {key} changed")
    require(old_doc["codes"] == new_doc["codes"], "Code content or position changed")
    require(old_doc["footnotes"] == new_doc["footnotes"], "Footnote positions changed")
    require(token_shape(audit.MD.parse(before.decode()))
            == token_shape(audit.MD.parse(after.decode())), "Markdown token structure changed")
    # This chapter has no inline code, links or HTML requiring punctuation masking.
    require(not new_doc["links"] and not new_doc["html"], "Add punctuation protection first")
    require(all(item["kind"] == "code_block" for item in new_doc["codes"]),
            "Unexpected inline/fenced code")
    return {
        "status": "verified_with_holds",
        "source": SOURCE,
        "baseline_commit": COMMIT,
        "baseline_sha256": audit.digest(before),
        "after_sha256": audit.digest(after),
        "physical_lines": len(old_lines),
        "chinese_lines_inspected": len(chinese),
        "changed_chinese_lines": len(changed),
        "reviewed_unchanged_chinese_lines": len(retained),
        "completed_chinese_lines_excluding_holds": len(changed | retained),
        "held_chinese_lines": len(held),
        "held_lines": manifest["held_lines"],
        "unaccounted_chinese_lines": [],
        "protected_counts": {k: len(v) for k, v in old_protected.items() if k != "sha256"},
        "protection_mismatches": [],
        "protection_exceptions_used": [],
        "markdown_token_structure_unchanged": True,
        "line_endings_indentation_hard_breaks_unchanged": True,
        "punctuation_normalization_required_lines": [],
        "punctuation_scope": "All 65 changed Chinese lines; English heading prefixes protected. "
        "Protected code, including both held Chinese lines, excluded.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("record", "verify"))
    args = parser.parse_args()
    before, after = load_original(), (ROOT / SOURCE).read_bytes()
    manifest_path = DIRECTORY / "edits.json"
    if args.command == "record":
        require(not manifest_path.exists(), "Refusing to replace an existing manifest")
        old_lines, new_lines = before.decode().splitlines(), after.decode().splitlines()
        require(len(old_lines) == len(new_lines), "Line count changed")
        manifest = {
            "source": SOURCE,
            "baseline_sha256": audit.digest(before),
            "replacements": {
                str(i): new for i, (old, new) in enumerate(zip(old_lines, new_lines), 1)
                if old != new
            },
            "reviewed_unchanged_lines": RETAINED,
            "held_lines": HOLDS,
        }
        result = validate(before, after, manifest)
        audit.dump(manifest_path, manifest)
        audit.dump(DIRECTORY / "verification.json", result)
    else:
        manifest = json.loads(manifest_path.read_text())
        result = validate(before, after, manifest)
        require(result == json.loads((DIRECTORY / "verification.json").read_text()),
                "Stale verification artifact")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
