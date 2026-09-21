"""Build the reader's Chinese body face: Noto Serif SC, subset to the characters the book uses.

Run with: uv run --project tools --with fonttools --with brotli python tools/build_fonts.py
"""

import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "fonts"
FONTS = ROOT / "assets" / "fonts"
SOURCE = "https://github.com/notofonts/noto-cjk/raw/main/Serif/"
FACES = ["NotoSerifSC-Regular", "NotoSerifSC-SemiBold"]


def fetch(url, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["curl", "-fsSL", "--retry", "2", url, "-o", str(target)], check=True)


def book_characters():
    """Every printable character in the book text, plus ASCII and the CJK punctuation blocks."""
    chars = {chr(c) for c in range(0x20, 0x7F)}
    chars |= {chr(c) for c in range(0x3000, 0x3040)}  # CJK symbols and punctuation
    chars |= {chr(c) for c in range(0xFF01, 0xFF5F)}  # fullwidth ASCII variants
    for path in (ROOT / "zh-cn").rglob("*.md"):
        chars |= set(path.read_text())
    for folder in ("reader-content", "reader-review"):
        for path in (ROOT / "assets" / folder).glob("*.json"):
            chars |= set(json.dumps(json.loads(path.read_text()), ensure_ascii=False))
    return "".join(sorted(c for c in chars if c.isprintable()))


def main():
    FONTS.mkdir(parents=True, exist_ok=True)
    charset = FONTS / "charset.txt"
    charset.write_text(book_characters() + "\n")
    for name in FACES:
        source = CACHE / f"{name}.otf"
        if not source.exists():
            fetch(SOURCE + f"SubsetOTF/SC/{name}.otf", source)
        subprocess.run([
            sys.executable, "-m", "fontTools.subset", str(source),
            f"--text-file={charset}", "--flavor=woff2", "--desubroutinize",
            "--name-IDs=0,1,2,3,4,5,6,13,14",
            f"--output-file={FONTS / (name + '.woff2')}",
        ], check=True)
    license_path = CACHE / "LICENSE"
    if not license_path.exists():
        fetch(SOURCE + "LICENSE", license_path)
    shutil.copyfile(license_path, FONTS / "LICENSE.txt")
    sizes = ", ".join(f"{name}.woff2 {(FONTS / (name + '.woff2')).stat().st_size // 1024} KB" for name in FACES)
    print(f"Subset {len(charset.read_text().rstrip(chr(10)))} characters: {sizes}.")


if __name__ == "__main__":
    main()
