"""Fetch version-pinned public reader dependencies and build a Lucide icon sprite."""

from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "assets" / "vendor"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def fetch(url, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["curl", "-fsSL", "--retry", "2", url, "-o", str(target)], check=True)


def strip_remote_font_import():
    path = VENDOR / "docsify-vue.css"
    text = path.read_text()
    if text.startswith('@import url("https://fonts.googleapis.com/'):
        path.write_text(text.partition(";")[2])


def main():
    sources = {
        "docsify.min.js": "https://cdn.jsdelivr.net/npm/docsify@4.13.1/lib/docsify.min.js",
        "docsify-zoom-image.min.js": "https://cdn.jsdelivr.net/npm/docsify@4.13.1/lib/plugins/zoom-image.min.js",
        "docsify-vue.css": "https://cdn.jsdelivr.net/npm/docsify@4.13.1/lib/themes/vue.css",
        "docsify.LICENSE.txt": "https://cdn.jsdelivr.net/npm/docsify@4.13.1/LICENSE",
        # Prism language components register with the Prism instance bundled in Docsify.
        "prism-python.min.js": "https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-python.min.js",
        "prism-java.min.js": "https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-java.min.js",
        "prism-c.min.js": "https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-c.min.js",
        "prism-cpp.min.js": "https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-cpp.min.js",
        "prism-go.min.js": "https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-go.min.js",
        "prism.LICENSE.txt": "https://cdn.jsdelivr.net/npm/prismjs@1.29.0/LICENSE",
        "lucide.LICENSE.txt": "https://cdn.jsdelivr.net/npm/lucide-static@0.468.0/LICENSE",
    }
    for name, url in sources.items():
        fetch(url, VENDOR / name)
    strip_remote_font_import()
    sprite = ET.Element(f"{{{NS}}}svg")
    names = ["menu", "sun", "moon", "minus", "plus", "maximize-2", "minimize-2",
             "download", "x", "list", "book-open", "github", "chevron-left", "chevron-right",
             "type", "chevron-down"]
    temporary = ROOT / ".cache" / "reader-icons"
    for name in names:
        path = temporary / f"{name}.svg"
        fetch(f"https://cdn.jsdelivr.net/npm/lucide-static@0.468.0/icons/{name}.svg", path)
        source = ET.parse(path).getroot()
        symbol = ET.SubElement(sprite, f"{{{NS}}}symbol", {
            "id": "icon-" + name, "viewBox": source.get("viewBox", "0 0 24 24"),
            "fill": "none", "stroke": "currentColor", "stroke-width": "2",
            "stroke-linecap": "round", "stroke-linejoin": "round",
        })
        for child in source:
            symbol.append(child)
    ET.ElementTree(sprite).write(ROOT / "assets" / "reader-icons.svg", encoding="utf-8", xml_declaration=True)
    print(f"Fetched Docsify 4.13.1, Prism 1.29.0 language components, and {len(names)} Lucide 0.468.0 symbols.")


if __name__ == "__main__":
    main()
