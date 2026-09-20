<div align="center">

# Software Engineering at Google 中文版

**《谷歌的软件工程》中英对照阅读版，附带一个为这本书专门打造的网页阅读器。**

*Lessons Learned from Programming Over Time*
<br>
Titus Winters、Tom Manshreck、Hyrum Wright 著

[![在线阅读](https://img.shields.io/badge/在线阅读-GitHub%20Pages-b4423a?style=for-the-badge)](https://dayuanjiang.github.io/Software-Engineering-at-Google/)
[![章节进度](https://img.shields.io/badge/章节-25%20%2F%2025%20全部完成-2e7d32?style=for-the-badge)](#目录)
[![内容许可](https://img.shields.io/badge/内容许可-CC%20BY--SA%203.0-555?style=for-the-badge)](#授权许可)

<br>

<a href="https://dayuanjiang.github.io/Software-Engineering-at-Google/">
  <img src="assets/images/reader-light.png" alt="阅读器截图：第一章，中英对照模式，本章图解已展开" width="920">
</a>

</div>

<br>

## 这本书讲什么

Google 用了二十多年时间，把成千上万名工程师和几十亿行代码组织成一个能持续演进的整体。这本书讲的就是他们在这个过程中学到的东西：为什么“软件工程是编程在时间上的积分”，代码审查为什么必须强制执行，测试为什么要分大小，依赖管理为什么比想象中难得多，以及大规模变更、持续集成、持续交付在 Google 内部到底是怎么运转的。

全书分五个部分：理论、文化、流程、工具、总结。它讨论的是团队和组织层面的工程实践，而不限于某一种语言或框架，因此对任何规模的团队都有参考价值。

## 这个仓库有什么

- **全书中英对照。** 每一段英文原文下面紧跟中文译文，可以对照着读，也可以只读中文。
- **全书中文润色。** 在 [qiangmzsx](https://github.com/qiangmzsx/Software-Engineering-at-Google) 的翻译基础上，逐章审校了 25 章正文及序言、前言、后记的中文表达。核心术语统一了译法，审校过程和术语表都保留在 `translation-review/` 目录里。
- **一个专门的网页阅读器。** 中英对照或纯中文切换、浅色深色主题、字号调节、章节内目录、阅读进度、译者注弹窗，还有为每一章绘制的图解。
- **134 张章节图解。** 25 章各有一张总览图，另有 109 张小节细节图，把书中的关键概念画成 SVG。每张图都有桌面和移动端两种版式，可以放大查看和下载。
- **可复现的审校工具链。** `tools/` 目录下的脚本负责术语抽取、译文校验、阅读器清单生成，全部有测试覆盖。

## 开始阅读

**在线阅读**：<https://dayuanjiang.github.io/Software-Engineering-at-Google/>

**本地阅读**：仓库本身就是一个静态站点，任何静态文件服务器都能直接运行。

```bash
git clone https://github.com/DayuanJiang/Software-Engineering-at-Google.git
cd Software-Engineering-at-Google
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

**直接读 Markdown**：所有章节都在 [`zh-cn/`](zh-cn/) 目录下，按章节分文件夹存放，在 GitHub 上点开就能读。

## 阅读器

<div align="center">
  <img src="assets/images/reader-dark.png" alt="阅读器截图：深色主题，正文中内嵌的章节图解和译者补充" width="920">
</div>

<br>

阅读器基于 Docsify 构建，所有依赖都已本地化，可以离线使用。你的阅读偏好会保存在浏览器里，下次打开自动恢复。

| 功能 | 说明 |
| --- | --- |
| 中英 / 中文 | 顶栏一键切换。中英模式下英文原文和中文译文逐段对照，中文模式下只显示译文。 |
| 主题与字号 | 浅色和深色两套主题，正文字号 16 至 22 像素可调。 |
| 本章目录 | 右侧固定显示当前章节的小节目录，滚动时自动高亮所在位置。 |
| 章节图解 | 每章开头有一张总览图，正文中关键小节配有细节图。支持放大、适应窗口、下载 SVG。 |
| 译者注 | 译者补充的说明以弹窗形式呈现，点击即看，关闭后回到原处。 |
| 查看源文 | 章末可以跳转到这一章的 Markdown 源文件。译者注中引用的资料会附上原始来源链接。 |
| 搜索 | 在全部章节里检索关键词。 |
| 讨论 | 章末的讨论区按需加载，沿用了原仓库的 Gitalk 配置。 |

## 目录

| 部分 | 章节 | 原文标题 | 译者 |
| --- | --- | --- | --- |
| | [序言](zh-cn/Foreword.md) | Foreword | @qiangmzsx |
| | [前言](zh-cn/Preface.md) | Preface | @qiangmzsx |
| **第一部分 理论** | [第一章 软件工程是什么？](zh-cn/Chapter-1_What_Is_Software_Engineering/Chapter-1_What_Is_Software_Engineering.md) | What Is Software Engineering? | @qiangmzsx |
| **第二部分 文化** | [第二章 如何在团队中有效协作](zh-cn/Chapter-2_How_to_Work_Well_on_Teams/Chapter-2_How_to_Work_Well_on_Teams.md) | How to Work Well on Teams | @qiangmzsx |
| | [第三章 知识共享](zh-cn/Chapter-3_Knowledge_Sharing/Chapter-3_Knowledge_Sharing.md) | Knowledge Sharing | @qiangmzsx |
| | [第四章 面向公平的工程实践](zh-cn/Chapter-4_Engineering_for_Equity/Chapter-4_Engineering_for_Equity.md) | Engineering for Equity | @qiangmzsx |
| | [第五章 如何领导团队](zh-cn/Chapter-5_How_to_Lead_a_Team/Chapter-5_How_to_Lead_a_Team.md) | How to Lead a Team | @qiangmzsx |
| | [第六章 领导大规模团队](zh-cn/Chapter-6_Leading_at_Scale/Chapter-6_Leading_at_Scale.md) | Leading at Scale | @FingerLiu |
| | [第七章 度量工程生产力](zh-cn/Chapter-7_Measuring_Engineering_Productivity/Chapter-7_Measuring_Engineering_Productivity.md) | Measuring Engineering Productivity | @qiangmzsx |
| **第三部分 流程** | [第八章 风格指南和规则](zh-cn/Chapter-8_Style_Guides_and_Rules/Chapter-8_Style_Guides_and_Rules.md) | Style Guides and Rules | @ll13 |
| | [第九章 代码审查](zh-cn/Chapter-9_Code_Review/Chapter-9_Code_Review.md) | Code Review | @qiangmzsx |
| | [第十章 文档](zh-cn/Chapter-10_Documentation/Chapter-10_Documentatio.md) | Documentation | @qiangmzsx |
| | [第十一章 测试概述](zh-cn/Chapter-11_Testing_Overview/Chapter-11_Testing_Overview.md) | Testing Overview | @qiangmzsx |
| | [第十二章 单元测试](zh-cn/Chapter-12_Unit_Testing/Chapter-12_Unit_Testing.md) | Unit Testing | @qiangmzsx |
| | [第十三章 测试替身](zh-cn/Chapter-13_Test_Doubles/Chapter-13_Test_Doubles.md) | Test Doubles | @qiangmzsx |
| | [第十四章 较大规模测试](zh-cn/Chapter-14_Larger_Testing/Chapter-14_Larger_Testing.md) | Larger Testing | @qiangmzsx |
| | [第十五章 弃用](zh-cn/Chapter-15_Deprecation/Chapter-15_Deprecation.md) | Deprecation | [@jixiuf](https://github.com/jixiuf) |
| **第四部分 工具** | [第十六章 版本控制和分支管理](zh-cn/Chapter-16_Version_Control_and_Branch_Management/Chapter-16_Version_Control_and_Branch_Management.md) | Version Control and Branch Management | @qiangmzsx |
| | [第十七章 代码搜索](zh-cn/Chapter-17_Code_Search/Chapter-17_Code_Search.md) | Code Search | [@transfercai](https://github.com/transfercai) |
| | [第十八章 构建系统与构建理念](zh-cn/Chapter-18_Build_Systems_and_Build_Philosophy/Chapter-18_Build_Systems_and_Build_Philosophy.md) | Build Systems and Build Philosophy | @qiangmzsx |
| | [第十九章 Critique：谷歌的代码审查工具](zh-cn/Chapter-19_Critique_Googles_Code_Review_Tool/Chapter-19_Critique_Googles_Code_Review_Tool.md) | Critique: Google's Code Review Tool | @qiangmzsx |
| | [第二十章 静态分析](zh-cn/Chapter-20_Static_Analysis/Chapter-20_Static_Analysis.md) | Static Analysis | @yangjun |
| | [第二十一章 依赖管理](zh-cn/Chapter-21_Dependency_Management/Chapter-21_Dependency_Management.md) | Dependency Management | @qiangmzsx |
| | [第二十二章 大规模变更](zh-cn/Chapter-22_Large-Scale_Changes/Chapter-22_Large-Scale_Changes.md) | Large-Scale Changes | @qiangmzsx |
| | [第二十三章 持续集成](zh-cn/Chapter-23_Continuous_Integration/Chapter-23_Continuous_Integration.md) | Continuous Integration | @qiangmzsx |
| | [第二十四章 持续交付](zh-cn/Chapter-24_Continuous_Delivery/Chapter-24_Continuous_Delivery.md) | Continuous Delivery | @qiangmzsx |
| | [第二十五章 计算即服务](zh-cn/Chapter-25_Compute_as_a_Service/Chapter-25_Compute_as_a_Service.md) | Compute as a Service | @qiangmzsx |
| **第五部分 总结** | [后记](zh-cn/Afterword.md) | Afterword | @qiangmzsx |

## 翻译是怎么审校的

这是一本偏硬的技术书，润色时以准确为先，改动幅度控制得很小。审校的每一步都留有记录，方便任何人复核：

- [`translation-review/glossary.md`](translation-review/glossary.md)：人工审定的核心术语表，包含每个术语的译法、适用范围、例外和原文依据。
- [`translation-review/book-summary.md`](translation-review/book-summary.md)：全书 28 篇文档的逐章审校入口和保护边界。
- [`translation-review/cross-review.md`](translation-review/cross-review.md)：第十一至十四章的独立语义交叉复核。
- [`translation-review/final-verification.md`](translation-review/final-verification.md)：最终验收记录、测试结果和未覆盖事项。

术语抽取用 spaCy 处理英文、jieba 处理中文，再按段落配对计算中英共现，最后由人工在候选里挑选并确认译法。频次最高的译法不一定是对的，所以自动结果一律标为待审定。完整方法见 [`translation-review/README.md`](translation-review/README.md)。

## 工具链

`tools/` 目录下是支撑上面这些工作的脚本，用 [uv](https://docs.astral.sh/uv/) 管理依赖。

| 脚本 | 作用 |
| --- | --- |
| `translation_audit.py` | 解析全部 Markdown，抽取中英语料并统计术语候选。只读，不改书稿。 |
| `book_review.py` | 离线校验各章清单和全书进度。 |
| `chapter_pilot.py` | 把审定后的中文行级修改应用到章节，并与原始快照比对。 |
| `reader_content.py` | 把审校记录编译成阅读器用的展示层内容，例如译者注弹窗。 |
| `build_reader_manifest.py` | 生成并校验阅读器的章节和图解清单。 |
| `fetch_reader_assets.py` | 拉取固定版本的前端依赖，生成 Lucide 图标精灵。 |

```bash
cd tools
uv sync                                  # 安装依赖
uv run python translation_audit.py --help
uv run --with pytest pytest -q           # 运行全部测试
```

## 参与贡献

发现译文有误，或者有更好的表达，欢迎直接提 Pull Request。

1. 章节文件在 `zh-cn/` 下，修改中文段落即可，英文原文请保持原样。
2. 术语请先查 [`translation-review/glossary.md`](translation-review/glossary.md)，与已审定译法保持一致。
3. 提交前在 `tools/` 目录运行一遍测试。

## 致谢

- 本仓库源自 [qiangmzsx/Software-Engineering-at-Google](https://github.com/qiangmzsx/Software-Engineering-at-Google)。感谢 @qiangmzsx 发起并完成大部分章节的翻译，也感谢 @FingerLiu、@ll13、@jixiuf、@transfercai、@yangjun 等所有贡献者。
- 感谢三位作者和 O'Reilly 在 [abseil.io](https://abseil.io/resources/swe-book) 免费公开英文原版。
- 阅读器使用了 [Docsify](https://docsify.js.org/) 和 [Lucide](https://lucide.dev/) 图标，许可信息见 [`assets/vendor/`](assets/vendor/)。

国内已有正式出版的中文版《Google 软件工程》。如果你希望获得更权威的译文，推荐购买纸质书支持作者与译者。

## 授权许可

除特别声明外，本书内容采用 [CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/)（署名、相同方式共享）授权，代码采用 [BSD 3-Clause](https://opensource.org/licenses/BSD-3-Clause) 许可。
