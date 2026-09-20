# Reader Dependencies

- Docsify 4.13.1 and its search plugin, MIT license. The existing v4 architecture is retained.
- Docsify Vue base CSS: its remote Google Fonts import is removed; the reader uses system fonts.
- `../reader-icons.svg` is generated from Lucide Static 0.468.0 icons. See the included license.

Reproduce with `uv run --project tools python tools/fetch_reader_assets.py`.
The reading surface uses local dependencies. The existing Gitalk discussion integration loads only on request.
