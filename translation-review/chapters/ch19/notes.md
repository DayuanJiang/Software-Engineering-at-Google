# 第19章中文润色记录

## 范围与覆盖

- 按已批准的第1章风格处理：信息型、偏硬技术书籍，润色自由度约 3/10；准确优先，不概括、不补写历史事实。
- 完整通读并二次对照本章双语内容，包括标题、正文、列表、脚注、英文图注及行内代码；另查看图19-3、图19-5以核对界面语境。
- 全章444个物理行不变。全部126个含中文的原始行已复核：修改109行，确认保留17行，暂缓0行，覆盖率100%。物理行数不等于段落数。
- 17个保留行：35、52、71、84、128、154、176、237、286、300、322、333、368、374、386、410、436；逐项记录于 `edits.json`。
- 本次人工修改仅涉及指定章节与本目录；不修改共享工具、术语表、导航或其他章节。不使用子代理、外部模型 API，不提交或推送。

## 依据

已读 `translation-review/subagent-brief.md`、`translation-review/glossary.md`、`translation-review/chapter-01/terminology.md`、第1章样稿 README 及修改对照样例。
已完整阅读 `en-zh-translation-polish/SKILL.md` 及其三份参考材料：`text-analysis-and-qa.md`、`translationese-symptoms.md`、`techniques.md`。
为区分批准与 Readability 资格，额外只读核对第9章第88至118行、第244至250行的相关英中内容；未修改第9章。

## 术语与主要修正

- **Critique**：始终保留产品名；第6行标题改为“第十九章 Critique：谷歌的代码审查工具”。纠正正文中的“评论”“批评”等专名误译；普通“体验”仍用于 user experience。
- **code review / author / reviewer / comment**：分别为“代码审查”“作者／变更作者”“审查者”“审查意见”。不把审查意见当成代码注释，也不把 review 译成“评论”。第18行 inline comments 指代码中的行内注释。
- **LGTM / Approval**：前者表示审查认可，后者表示把关者准许提交。第338行保留三项提交条件：至少一个 LGTM、取得所需批准、没有未解决意见。第366行保留硬性要求与作者可自行标记解决的软性要求之别。
- **Readability**：资格语境应称“Readability 资格（语言规范审查资格）”，不等于代码容易阅读。第19章本地正文只有第12行普通意义的 readability，对应第14行“可读性”；没有资格说明段落，因此未擅自把资格说明加入正文。第9章明确区分 LGTM、代码所有者批准和 Readability 批准，可作为跨章语义依据。
- **unresolved / resolved**：保留“未解决／已解决”状态；第77行纠正为 LGTM 后仍可附上需要处理的意见，而非“已解决的评论”。第270行区分 Done 的“已处理”与 Ack 的“已阅读”，两者均可将讨论串标记为已解决。
- **presubmits / analyzer / linter / finding / chip**：分别按语境处理为“提交前检查／提交前钩子”“分析器”“代码风格检查工具”“检查结果”“状态标签”。第174、418行纠正把工具误译成人员的问题。
- **diffing / intraline diffing / longest common subsequence**：采用“差异比较”“行内差异比较”“最长公共子序列”；第132行是代码已移动，而非正在移动。第140行保留推出时1440像素屏宽和 Java 每行100字符的历史语境。
- **attention set**：沿用“关注集”，明确其中是当前需要回应、变更才能推进的人，而非有意阻碍变更的人。第290行将携带值班呼叫器的 SRE 译为负责服务值班的 SRE；第316行将 ping 译为催促审查，而非修正代码。
- **source of truth / monolithic repository**：分别为“权威来源”“单体代码仓库”；Code Search、Cider、Tricorder、Rapid、Zapfhahn、GwsQ 等工具名保持可辨识。
- 第346行修正 thumbs-down 的否定方向。第394行恢复 cherry-picking commits 的“拣选提交”；第398行区分“逐个审查”与“个人审阅”，保留整条提交链的原子提交语义。
- 第414行恢复“花在审查上的时间就不能用来写代码”的机会成本含义。第426行 opinionated process 是有明确设计取向的流程，不是意见一致。

## 原文与保护边界

- 第12行英文 `process in only one part` 存在语法疑点；按上下文翻译为“只是其中一部分”，英文原样保留。
- 第204至205行 GwsQ 英文括号不配对，并跨物理行；中文第207至208行在原行位内理顺语句，英文和既有硬换行均未改动。
- 第216行 `see the next section` 的所有权交叉指引在本地章节中不够明确；第223行仍按原文保留“见下一节”，不推测并改写目标。
- 第368行英文标题拼写 `Commiting` 原样保留。第342行唯一受保护行内代码 `LGTM/批准` 原样保留。
- 原有 `#_bookmark1364` 目标、中文脚注的数字形式及英文正文中的脚注引用均保留，未新增或重排标记。8条英文图注没有擅自增译。
- 无围栏代码块或缩进代码块，无 HTML 项，无待审的“被识别为代码块的中文”。没有新增译注或把译注并入作者正文。
- 未查询官方在线原文，以上为本地源文观察，不声称已经校勘上游版本。这些保护边界不计为未完成的中文行。

## 校验

- 使用 `uv run --offline --locked --project tools --cache-dir .cache/uv python -B ...`，仅验证本章；直接使用现有 `translation_audit.py` 和 `book_review.py` 的解析、保护、重建与覆盖检查，未放宽断言或添加代码例外。
- 基准提交：`110720f031b43e18708fdc38af03269b65b3cc41`。
- 基准 SHA-256：`8c5d62997bf278ad197f7117d5a806a445a56bfcc3dbd43c0725319469dd601a`，与 `translation-review/baseline.json` 一致。
- 结果：126个英文源行哈希、131个英文片段、1项行内代码、13个链接记录、111个结构项、4个脚注标记均一致；HTML 项为0。13个链接记录包括8条图片引用、3条 Markdown 链接和2条解析出的裸 URL，不代表13个独立目标。
- 318个不含中文的行逐字节不变；逐行核验缩进、行尾空白、换行形式、脚注位置和英文标题前缀。完整 Markdown token 结构、强调、列表、软换行及硬换行均一致。
- 本章8张截图同时与 Git 原始内容及基线 SHA-256 比对，全部一致。
- 对126个中文行机械执行标点归一检查，先保护行内代码、链接及英文标题前缀；结果已符合规则，需要归一的行0个，引号残留0个。
- 清单可逐字节重建当前章节，修改行、保留行与暂缓行完整且互不重叠。详细结果见 `verification.json`。
- 本章专用 `git -c core.whitespace=-blank-at-eol diff --check` 通过；关闭该项检查仅为保留原有 Markdown 行尾硬换行空格。
- 未运行全仓库断言、站点浏览器检查或外链可达性检查；结构校验不等于自动证明译文语义正确，语义已人工逐段复核。

核心保护与清单检查可只针对本章重跑：

```bash
uv run --offline --locked --project tools --cache-dir .cache/uv python -B - <<'PY'
import json, sys
sys.path.insert(0, "tools")
import book_review as review
import translation_audit as audit
manifest = json.loads((review.DIRECTORY / "ch19/edits.json").read_text())
baseline = json.loads((audit.DEFAULT_OUT / "baseline.json").read_text())
source = manifest["source"]
before = review.original(source, baseline)
assert manifest["baseline_sha256"] == audit.digest(before)
print(review.validate(source, before, (audit.ROOT / source).read_bytes(), manifest))
PY
```
