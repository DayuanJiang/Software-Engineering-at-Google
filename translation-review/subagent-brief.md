# Chapter Editing Brief

The user approved Chapter 1's Chinese polishing style and requested all remaining chapters.
The parent will assign exactly one chapter and an output directory to each worker.

## Scope

- Edit only the assigned chapter Markdown and its assigned review directory.
- Do not edit Chapter 1, other chapters, shared tools, the glossary, root navigation, or global reports.
- Do not spawn agents, call external model APIs, commit, push, or deploy.
- Other workers may modify disjoint files. Do not revert their work or run all-repo assertions expecting those files unchanged.

## Required Reading

Read `/Users/jiangdayuan/.agents/skills/en-zh-translation-polish/SKILL.md` and its three `reference/` files.
Use `translation-review/glossary.md`, `translation-review/chapter-01/terminology.md`,
and the Chapter 1 sample/README to match the approved style.
Read the entire assigned bilingual chapter, including notes, lists, tables and code context.

## Editorial Standard

Informative technical prose, freedom about 3/10: accuracy first, natural readable Chinese second.
Correct mistranslations, lost negation/conditions/quantifiers, unclear referents, units and technical terminology.
Do not summarize, omit details, add unsupported propositions, modernize historical claims or overdecorate prose.
Preserve English source text exactly. Only Chinese lines are editable.
Preserve line count/order, heading levels and English heading prefixes, Markdown links/targets, images,
inline code, HTML, footnote markers, code blocks and original hard line breaks.
Read code for context but do not change executable code or comments inside code blocks.
If Chinese prose is misclassified as an indented code block, preserve it and report the hold explicitly.
Retain existing translator notes as notes, not author text.
Record source gaps/ambiguities instead of inventing missing English. Official Abseil book pages may be checked
when necessary, but do not alter the local English without parent review.

Important conventions: code review = 代码审查; test double = 测试替身; infrastructure = 基础设施;
regression = 回归缺陷, not rollback; fork = 分叉, branch = 分支;
SemVer = 语义化版本管理; Critique is a proper name, not 体验/评论.
Distinguish test size/scope, brittle/flaky, continuous delivery/deployment.
Google's Readability certification/process is not merely abstract code readability.
Correct chapter titles when needed, but parent handles navigation labels.

## Deliverables

1. Actually edit the assigned chapter in your workspace using `apply_patch`.
2. In the assigned directory create `edits.json`:
   - `source`: repository-relative chapter path
   - `baseline_sha256`: the original chapter SHA-256 from `translation-review/baseline.json`
   - `replacements`: map of original 1-based line numbers to complete replacement lines (without newline)
   - `reviewed_unchanged_lines`: all other original lines containing Chinese that you reviewed and retained
   - `held_lines`: any Chinese lines deliberately left pending, with reasons (do not call them completed)
3. Add concise `notes.md`: terminology choices, material fixes, source issues and any held content.
4. Validate only this chapter against the original Git snapshot
   `110720f031b43e18708fdc38af03269b65b3cc41`.
   Use `tools/translation_audit.py` parsing/protection helpers if useful; do not weaken their assertions.
   English, code, links, structures and footnote markers must match. Report any mismatches honestly.
5. Final response: changed file paths, Chinese line review/edit counts, validation result and holds.

Use `uv run --offline --locked --project tools --cache-dir .cache/uv python ...` for Python work.
Avoid broad replacement rules. A finished chapter needs a complete contextual edit, not keyword cleanup.
