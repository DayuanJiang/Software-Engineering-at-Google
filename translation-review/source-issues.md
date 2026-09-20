# 既有问题与待核实项

这些问题来自修改前的书籍内容，不是统计工具新增的正文改动。不作无记录的自动修复；
全书处理状态见 `book-summary.md`，各章的保留事项见 `chapters/*/notes.md`。
第21章一处损坏链接的语法修复另存于 `link-syntax-exceptions.json`，其原可见目标地址未变。
机器可读的引用检查结果在 [existing-issues.json](existing-issues.json)。

## 英文缺损

- 位置：`zh-cn/Chapter-1_What_Is_Software_Engineering/Chapter-1_What_Is_Software_Engineering.md:136`。
- 本地英文：`Hyrum’s Law represents the practical knowledge that—even with the best of intentions, the best engineers, and solid practices for code review—.`
- 状态：2026-09-20 已与官方在线版核对，确认本地缺句。证据见 `chapter-01/README.md`。
- 理由：`that` 引出的内容在插入语后直接结束，没有完整展开。
- 处理：中文已根据官方原文校正，本地英文尚未补写；未根据旧中文反推英文。

## 引用及排版

自动检查结果按以下类型区分，不统一称为“已确认失效链接”：

| 类型 | 已确认的内容 | 仍需核实 |
| --- | --- | --- |
| `legacy_bookmark_without_explicit_id` | 本地引用 `_bookmark…`，目标文件没有同名显式 HTML ID | 站点渲染后的实际跳转 |
| `generated_anchor_not_verified` | 引用依赖标题自动生成的锚点 | Docsify 的实际锚点 |
| `footnote_parsed_as_relative_link` | Markdown 解析器把脚注内容解释成相对链接 | 站点的实际展示和跳转 |
| `footnote_reference_without_definition` | 原始标记存在 `[^n]` 引用，未找到同号 `[^n]:` 定义 | 是否改用了另一种脚注写法及实际渲染 |
| `missing_local_target` | 正常相对路径指向的文件不存在时才使用该分类 | 该缺失是否有意、应指向哪里 |

例如第三章里的 `> [^10]: Ibid.` 一类格式，会被所用 Markdown 解析器识别为指向 `Ibid.` 的链接定义。
第二十三章的脚注 URL 带反引号和尾部标点，也会被解释成相对路径。
这些是脚注或链接语法的既有疑点，不是通过网络确认的网页失效。

未探测外部网址，因此没有将超时、403、404 等 HTTP 状态作为本次判断依据。

## 人工对齐待办

`alignments.json` 保留准备阶段的 `ambiguous` 与 `unpaired` 组，不覆写为事后完美对齐。
各章已结合实际英文上下文审校；第一章另有逐组记录，其他章节的原有缺译或异常配对写入各章说明。

单段相邻和等长列表配对同样只是结构候选。尤其是中英表格、引文、长列表和脚注，
即便数量一致，也需要人工确认是否真的对应。

## 术语相关的明确误译样本

这些样本已根据同文件英文核对：

- 第一章脚注：`execution lifetime` 对应“开发生命周期”，混淆了执行与开发。已在第一章样稿中修正。
- 第十二章：`check in her change` 对应“检查她的改动”，已修正为提交代码变更。
- 第十九章标题：工具名 `Critique` 对应“体验”，已保留专名并同步目录。
- 第六章引文：英文 `twenty people` 对应“12名乘客”，已修正为20人。

以上均通过对照原文逐处修正，不靠词频或全局替换直接处理。

## 仍保留的内容边界

- 第18章原第337行、第23章原第673行的既有英文缺译，未通过新增段落补译。
- 第4章原第110行的逻辑关系、第25章原第447行的延迟方向与上下文存在张力，官方版亦如此；中文已明确标注处理依据，不声称英文已得到作者勘误。
- 原有代码错误、错别字、损坏书签、章号疑点、代码围栏标签及未译英文图注等，按各章说明保留。
