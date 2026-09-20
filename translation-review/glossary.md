# 核心术语表

这是基于自动候选和原文抽样审定的首批术语，不是全书完整词典。
首选译法适用于注明的语境，不授权全局替换。
英文频次为列出 keys 的合计；异译计数是候选对齐中文段内的精确字符串命中，不能视为逐词对齐后的译法频次。
未命中已列异译不等于漏译。全部定义、例外、证据和计数位置见 `glossary-statistics.json`。

| 英文术语 | 首选译法 | 英文次数 / 文档数 | 对齐中文中的已有异译命中 | 使用边界 |
| --- | --- | --- | --- | --- |
| software engineering | 软件工程 | 134 / 23 | 软件工程：132 | 学科及工程实践。 |
| codebase / code base | 代码库 | 313 / 26 | 代码库：300 | 代码整体及其维护。 |
| code review | 代码审查 | 244 / 17 | 代码审查：195；代码评审：32；代码审阅：2 | 代码变更的同行审查。 |
| Critique | Critique | 97 / 4 | Critique：75；体验：5；评论：34 | 工具名称，保留英文及大小写。 |
| test size | 测试规模 | 12 / 3 | 测试规模：11；规模：2；大小：2 | 测试分类中的 size 维度。 |
| test scope | 测试范围 | 4 / 2 | 测试范围：3；范围：7 | 测试分类中的 scope 维度。 |
| unit test | 单元测试 | 107 / 10 | 单元测试：107 | 测试类型。 |
| test double | 测试替身 | 92 / 4 | 测试替代：75；测试替换：2；测试替身：2 | 替代真实依赖的上位概念。 |
| brittle test | 脆弱测试 | 16 / 5 | 脆性测试：11；脆弱测试：2；脆弱的测试：1 | 对无害代码变动敏感。 |
| flaky test | 不稳定测试 | 17 / 6 | 松散测试：2；不稳定测试：7；不稳定的测试：4 | 测试结果非确定。 |
| technical debt | 技术债务 | 6 / 6 | 技术债务：5；技术债：1 | 工程维护语境。 |
| knowledge sharing | 知识共享 | 16 / 3 | 知识共享：15；知识分享：1 | 组织学习及知识传播。 |
| psychological safety | 心理安全感 | 13 / 3 | 心理上的安全感：1；心理安全：10；心理安全感：1 | 团队学习与协作。 |
| engineering productivity | 工程生产力 | 13 / 4 | 工程生产力：4；工程效率：2；工程生产效率：6 | 作为被衡量和改进的工程产出能力。 |
| version control | 版本控制 | 75 / 13 | 版本控制：76；版本管理：1 | 版本与变更管理。 |
| source control | 源代码版本控制 | 31 / 5 | 源代码控制：11；源码控制：13 | 需要明确管理对象为源代码时。 |
| monorepo | 单体代码仓库 | 53 / 8 | monorepo：20；语法库：2；单版本版本库：1；单一代码库：1；Monorepo：1；单版本库：18 | 代码仓库组织方式。 |
| source of truth | 权威来源 | 34 / 3 | 权威的标准来源：1；统一的信息来源：1；信息源：27；单信息源：4 | 版本控制、配置和数据的一致性依据。 |
| trunk-based development | 主干开发 | 16 / 3 | 基于主干的开发：14 | 分支与协作策略。 |
| build system | 构建系统 | 135 / 10 | 构建系统：127 | 自动化软件构建。 |
| dependency management | 依赖管理 | 41 / 5 | 依赖性管理：5；依赖管理：40；依赖关系管理：2 | 软件依赖及其版本、更新和兼容性。 |
| static analysis | 静态分析 | 78 / 10 | 静态分析：70 | 程序分析方法。 |
| false positive | 误报 | 10 / 3 | 误报：15；假阳性：2 | 静态分析和测试告警。 |
| false negative | 漏报 | 4 / 3 | 漏报：3 | 静态分析和测试告警。 |
| deprecation | 弃用 | 98 / 6 | 废弃：4；弃用：109 | API、组件和系统的退役过程。 |
| continuous integration | 持续集成 | 15 / 12 | 持续集成：13 | CI 的完整术语。 |
| continuous delivery | 持续交付 | 9 / 3 | 连续交付：2；持续交付：7 | CD 的完整术语。 |
| code coverage | 代码覆盖率 | 9 / 1 | 代码覆盖率：9 | 代码执行覆盖指标。 |

## 审定依据

### software engineering

本书强调软件随时间演进时的开发、修改与维护，以及规模和权衡；不能缩减为编程。

例外：programming 单独译为编程；不要把两者统一成同一个词。

- `zh-cn/Chapter-1_What_Is_Software_Engineering/Chapter-1_What_Is_Software_Engineering.md:19`：Software engineering isn’t programming.

### codebase / code base

某个项目或组织维护的代码整体。它与承载代码及其历史的版本控制仓库有关，但不是所有语境下都等同。

例外：repository 涉及具体版本控制存储或仓库时，优先译为代码仓库。

- `zh-cn/Chapter-1_What_Is_Software_Engineering/Chapter-1_What_Is_Software_Engineering.md:224`：Your organization’s codebase is sustainable when you are able to change all of the things that you ought to change, safely, and can do so for the life of your codebase.

### code review

由代码作者以外的人审查代码的过程，通常发生在代码进入代码库之前。

例外：review 用于文档或绩效时按上下文翻译；不要全局替换为代码审查。

- `zh-cn/Chapter-9_Code_Review/Chapter-9_Code_Review.md:12`：Code review is a process in which code is reviewed by someone other than the author, often before the introduction of that code into a codebase.

### Critique

Google 内部代码审查工具的专名。

例外：同段中的普通 comment 仍可译为评论或审查意见；因此本条的评论命中数不等于专名误译次数。

- `zh-cn/Chapter-9_Code_Review/Chapter-9_Code_Review.md:16`：At Google, we use a custom code review tool, Critique, to support our process.

### test size

测试消耗的资源及允许执行的操作，属于运行约束维度。

例外：不是测试用例数量，也不是被验证代码的范围。small/medium/large 按这一维度译为小型/中型/大型测试。

- `zh-cn/Chapter-12_Unit_Testing/Chapter-12_Unit_Testing.md:12`：size refers to the resources consumed by a test and what it is allowed to do

### test scope

测试打算验证多少代码，是与资源消耗不同的分类维度。

例外：不能因为单元测试通常是小型测试，就把范围和规模混为一谈；代码中的词法 scope 可译为作用域。

- `zh-cn/Chapter-12_Unit_Testing/Chapter-12_Unit_Testing.md:12`：scope refers to how much code a test is intended to validate.

### unit test

验证范围较窄的测试，例如针对单个类或方法；不以运行资源规模作为定义。

例外：不要直接改成小型测试，原文明确两者并不总是相同。

- `zh-cn/Chapter-12_Unit_Testing/Chapter-12_Unit_Testing.md:12`：Unit tests are usually small in size, but this isn’t always the case.

### test double

测试中代替真实实现的对象或函数，原文以电影中的替身作类比。

例外：不统一改为 mock；fake、stub 和 mock 的具体区别需要在各自语境下保留。

- `zh-cn/Chapter-13_Test_Doubles/Chapter-13_Test_Doubles.md:20`：A test double is an object or function that can stand in for a real implementation in a test

### brittle test

生产代码发生无关且没有引入实际缺陷的变动时，也会失败的测试。

例外：与 flaky test 区分，不笼统合并为不稳定测试。

- `zh-cn/Chapter-12_Unit_Testing/Chapter-12_Unit_Testing.md:56`：a brittle test is one that fails in the face of an unrelated change to production code that does not introduce any real bugs.

### flaky test

生产代码没有变化，仍会非确定性地失败的测试。

例外：不是对代码变更脆弱，也不是测试组织松散；首次出现可保留 flaky 英文。

- `zh-cn/Chapter-12_Unit_Testing/Chapter-12_Unit_Testing.md:64`：a flaky test, which fails nondeterministically without any change to production code.

### technical debt

本书用尚未完成但应该完成的事项，以及代码现状与期望状态之间的差距来概括这一概念。

例外：原文将这一解释称为粗略定义，不把它润色成唯一或严格定义。

- `zh-cn/Chapter-1_What_Is_Software_Engineering/Chapter-1_What_Is_Software_Engineering.md:39`：This is perhaps a reasonable hand-wavy definition of technical debt

### knowledge sharing

通过提问、记录、教程和课程等机制在组织内传播知识。

例外：普通动词 share 可以按句意使用分享，不机械替换。

- `zh-cn/Chapter-3_Knowledge_Sharing/Chapter-3_Knowledge_Sharing.md:12`：you need both experts who know the answers to those questions and mechanisms to distribute their knowledge

### psychological safety

团队成员能够坦然提问、承认不知道、尝试和犯错的环境感受。

例外：不是信息安全，也不是避免一切困难或批评。

- `zh-cn/Chapter-3_Knowledge_Sharing/Chapter-3_Knowledge_Sharing.md:111`：In a healthy environment, people feel comfortable asking questions, being wrong, and learning new things.

### engineering productivity

工程组织和工程师取得产出的能力；原文另外讨论如何高效地改善这种能力。

例外：普通行文可按上下文使用工作效率；遇到 productivity 与 efficiency 对比时，保留生产力与效率的区别。

- `zh-cn/Chapter-7_Measuring_Engineering_Productivity/Chapter-7_Measuring_Engineering_Productivity.md:30`：Therefore, our goal is to not only improve software engineering productivity, but to do so efficiently.

### version control

跟踪版本及变更历史、支持协作的机制，系统缩写为 VCS。

例外：dependency management 不并入版本控制；VCS 保留原缩写。

- `zh-cn/Chapter-16_Version_Control_and_Branch_Management/Chapter-16_Version_Control_and_Branch_Management.md:34`：without any understanding of version control

### source control

源代码的版本及变更管理。第二十一章将它与跨组织的依赖管理加以区分。

例外：上下文已明确时可简称版本控制；不把 source 译成来源。

- `zh-cn/Chapter-21_Dependency_Management/Chapter-21_Dependency_Management.md:28`：Source control and dependency management are related issues separated by the question:

### monorepo

以单一仓库组织多个项目的代码；原文也讨论虚拟的单一仓库。

例外：不等于单版本规则，也不意味着代码没有历史版本。

- `zh-cn/Chapter-21_Dependency_Management/Chapter-21_Dependency_Management.md:28`：a large organization with a (virtual?) single repository (monorepo)

### source of truth

协作各方认可并据以确定当前状态的来源。

例外：single source of truth 译为唯一权威来源；不是字面意义的真理。

- `zh-cn/Chapter-16_Version_Control_and_Branch_Management/Chapter-16_Version_Control_and_Branch_Management.md:34`：when there isn’t a single agreed-upon source of truth, collaboration becomes high friction and error prone.

### trunk-based development

围绕共同主干同步并提交变更，依靠测试和持续集成保持主干可用的开发方式。

例外：不把所有 trunk 单独出现的位置替换成主干开发。

- `zh-cn/Chapter-16_Version_Control_and_Branch_Management/Chapter-16_Version_Control_and_Branch_Management.md:276`：The alternative requires a different paradigm: trunk-based development, rely heavily on testing and CI, keep the build green

### build system

将工程师编写的源代码转化为机器可执行二进制文件的系统。

例外：build 作动词时译为构建；作为一次运行或产物时需要按上下文区分，不全部译成构建系统。

- `zh-cn/Chapter-18_Build_Systems_and_Build_Philosophy/Chapter-18_Build_Systems_and_Build_Philosophy.md:26`：they transform the source code written by engineers into executable binaries that can be read by machines.

### dependency management

管理项目所依赖的其他代码或子项目及其演进，尤其涉及本组织不能直接控制的开发与更新。

例外：不把 dependency 的所有出现一概替换为依赖项；关系和具体对象要区分。

- `zh-cn/Chapter-21_Dependency_Management/Chapter-21_Dependency_Management.md:28`：interdependencies between unknown and not-necessarily-collaborating projects are a dependency management problem.

### static analysis

不运行被分析程序，而通过分析源代码发现问题的方法。

例外：具体 analysis check 可以译为分析检查项；与 dynamic analysis 区分。

- `zh-cn/Chapter-20_Static_Analysis/Chapter-20_Static_Analysis.md:11`：The “static” part specifically refers to analyzing the source code instead of a running program

### false positive

工具把实际上没有目标问题的代码错误地标记为有问题。

例外：effective false positive 是另有定义的用户感知指标，不直接等同于技术上的误报。

- `zh-cn/Chapter-20_Static_Analysis/Chapter-20_Static_Analysis.md:73`：A “false positive” occurs when a tool incorrectly flags code as having the issue.

### false negative

代码确实存在分析工具旨在发现的问题，但工具没有发现。

例外：不能与 false positive 的误报方向颠倒。

- `zh-cn/Chapter-20_Static_Analysis/Chapter-20_Static_Analysis.md:73`：a “false negative” is when a piece of code contains an issue that the analysis tool was designed to find, but the tool misses it.

### deprecation

本章指有序地从过时系统迁出，并最终移除这些系统的过程。

例外：已标记 deprecated 不一定已经被删除；标记弃用、迁移和移除是不同阶段。

- `zh-cn/Chapter-15_Deprecation/Chapter-15_Deprecation.md:17`：We refer to the process of orderly migration away from and eventual removal of obsolete systems as deprecation.

### continuous integration

频繁集成变更并通过自动构建和测试尽早发现集成问题；本章还讨论更广的系统集成。

例外：本条英文计数不包含缩写 CI，避免全称加缩写重复计数；不与持续交付混同。

- `zh-cn/Chapter-23_Continuous_Integration/Chapter-23_Continuous_Integration.md:10`：the fundamental goal of CI is to automatically catch problematic changes as early as possible.

### continuous delivery

围绕持续向用户交付可用软件、尽早获得反馈的工程实践。

例外：不自动改为持续部署；本条计数不包含缩写 CD。

- `zh-cn/Chapter-24_Continuous_Delivery/Chapter-24_Continuous_Delivery.md:16`：The earlier and more frequently you get working software in front of real users, the quicker you get feedback to find out how valuable it really is.

### code coverage

代码被测试执行的覆盖程度。本书示例以行覆盖率说明，同时提醒还有路径和分支等覆盖维度。

例外：不是测试质量的充分证明；不要把执行过改写成验证正确。

- `zh-cn/Chapter-11_Testing_Overview/Chapter-11_Testing_Overview.md:406`：Code coverage is a measure of which lines of feature code are exercised by which tests.

