
**CHAPTER 19**

# Critique: Google’s Code Review Tool

# 第十九章 Critique：谷歌的代码审查工具

**Written by Caitlin Sadowski, Ilham Kurnia, and Ben Rohlfs**

**Edited by Lisa Carey**

As you saw in Chapter 9, code review is a vital part of software development, particularly when working at scale. The main goal of code review is to improve the readability and maintainability of the code base, and this is supported fundamentally by the review process. However, having a well-defined code review process in only one part of the code review story. Tooling that supports that process also plays an important part in its success.

正如第9章所述，代码审查是软件开发的重要组成部分，在大规模开发中尤其如此。代码审查的主要目标是提高代码库的可读性和可维护性，而审查流程是实现这一目标的根本保障。不过，明确的审查流程只是其中一部分，支持这一流程的工具同样关系到代码审查的成效。

In this chapter, we’ll look at what makes successful code review tooling via Google’s well-loved in-house system, Critique. Critique has explicit support for the primary motivations of code review, providing reviewers and authors with a view of the review and ability to comment on the change. Critique also has support for gatekeeping what code is checked into the codebase, discussed in the section on “scoring” changes. Code review information from Critique also can be useful when doing code archaeology, following some technical decisions that are explained in code review interactions (e.g., when inline comments are lacking). Although Critique is not the only code review tool used at Google, it is the most popular one by a large margin.

本章以谷歌内部广受欢迎的 Critique 为例，探讨代码审查工具成功的要素。Critique 针对代码审查的主要目的提供了相应支持，让审查者和作者能够查看审查情况，并对变更提出意见。它还支持对进入代码库的代码把关，后文“对变更进行评分”一节将介绍这一点。进行代码考古时，Critique 中的审查信息也有助于追溯审查讨论中解释过的技术决策，例如代码缺少行内注释时就可以借助这些信息。Critique 并非谷歌唯一的代码审查工具，但其受欢迎程度远超其他工具。

## Code Review Tooling Principles 代码审查工具的设计原则

We mentioned above that Critique provides functionality to support the goals of code review (we look at this functionality in more detail later in this chapter), but why is it so successful? Critique has been shaped by Google’s development culture, which includes code review as a core part of the workflow. This cultural influence translates into a set of guiding principles that Critique was designed to emphasize:

- *Simplicity*  
    Critique’s user interface (UI) is based around making it easy to do code review without a lot of unnecessary choices, and with a smooth interface. The UI loads fast, navigation is easy and hotkey supported, and there are clear visual markers for the overall state of whether a change has been reviewed.
- *Foundation of trust*  
    Code review is not for slowing others down; instead, it is for empowering others. Trusting colleagues as much as possible makes it work. This might mean, for example, trusting authors to make changes and not requiring an additional review phase to double check that minor comments are actually addressed. Trust also plays out by making changes openly accessible (for viewing and reviewing) across Google.
- *Generic communication*  
    Communication problems are rarely solved through tooling. Critique prioritizes generic ways for users to comment on the code changes, instead of complicated protocols. Critique encourages users to spell out what they want in their comments or even suggests some edits instead of making the data model and process more complex. Communication can go wrong even with the best code review tool because the users are humans.
- *Workflow integration*  
    Critique has a number of integration points with other core software development tools. Developers can easily navigate to view the code under review in our code search and browsing tool, edit code in our web-based code editing tool, or view test results associated with a code change.

前面提到，Critique 提供了支持代码审查目标的功能，本章后面会详细介绍。不过，它为什么如此成功？谷歌的开发文化将代码审查视为工作流的核心环节，也塑造了 Critique。这种文化影响体现在以下指导原则中，Critique 的设计着重遵循这些原则：

- *简洁性*  
    Critique 的用户界面（UI）旨在让代码审查更容易，减少不必要的选择，保证操作流畅。界面加载快，导航方便，支持快捷键，并以清晰的视觉标记显示变更是否已完成审查。
- *以信任为基础*  
    代码审查不是为了拖慢别人，而是为了帮助别人更好地完成工作。尽可能信任同事，审查才能发挥作用。例如，相信作者会作出相应修改，而不必再增加一轮审查，逐一确认细小的审查意见是否已经处理。信任还体现在变更对谷歌全公司开放，供大家查看和审查。
- *通用的沟通方式*  
    沟通问题很少能单靠工具解决。Critique 优先提供通用方式，让用户对代码变更提出意见，而不是引入复杂的沟通规则。它鼓励用户在审查意见中说清楚自己的要求，甚至直接提出修改建议，而不是让数据模型和流程变得更复杂。即使使用最好的代码审查工具，沟通仍可能出问题，因为使用工具的是人。
- *工作流集成*  
    Critique 与其他核心软件开发工具有多处集成。开发者可以方便地跳转到代码搜索和浏览工具，查看正在审查的代码；也可以在网页版代码编辑工具中修改代码，或查看与变更相关的测试结果。

Across these guiding principles, simplicity has probably had the most impact on the tool. There were many interesting features we considered adding, but we decided not to make the model more complicated to support a small set of users.

在这些指导原则中，简洁性可能对 Critique 的影响最大。我们考虑过添加许多有意思的功能，但最终决定，不为满足少数用户的需要而增加模型的复杂性。

Simplicity also has an interesting tension with workflow integration. We considered but ultimately decided against creating a “Code Central” tool with code editing, reviewing, and searching in one tool. Although Critique has many touchpoints with other tools, we consciously decided to keep code review as the primary focus. Features are linked from Critique but implemented in different subsystems.

简洁性与工作流集成之间也存在值得注意的矛盾。我们曾考虑创建一个集代码编辑、审查和搜索于一体的“代码中心”工具，但最终放弃了这个想法。尽管 Critique 与其他工具有多处衔接，我们仍明确决定让它专注于代码审查。其他功能可以从 Critique 通过链接访问，但由不同的子系统实现。

## Code Review Flow 代码审查流程

Code reviews can be executed at many stages of software development, as illustrated in Figure 19-1. Critique reviews typically take place before a change can be committed to the codebase, also known as precommit reviews. Although Chapter 9 contains a brief description of the code review flow, here we expand it to describe key aspects of Critique that help at each stage. We’ll look at each stage in more detail in the following sections.

如图19-1所示，代码审查可以在软件开发的多个阶段进行。Critique 中的审查通常发生在变更提交到代码库之前，也称为提交前审查。第9章已简要介绍代码审查流程，这里将进一步说明 Critique 在各阶段提供的关键支持。后续各节会详细介绍这些阶段。

![Figure 19-1](./images/Figure%2019-1.png)

*Figure 19-1. The code review flow*

Typical review steps go as follows:

1. **Create a change.** A user authors a change to the codebase in their workspace. This *author* then uploads a *snapshot* (showing a patch at a particular point in time) to Critique, which triggers the run of automatic code analyzers (see Chapter 20).
2. **Request** **review.** After the author is satisfied with the diff of the change and the result of the analyzers shown in Critique, they mail the change to one or more reviewers.
3. **Comment.** *Reviewers* open the change in Critique and draft comments on the diff. Comments are by default marked as *unresolved,* meaning they are crucial for the author to address. Additionally, reviewers can add *resolved* comments that are optional or informational. Results from automatic code analyzers, if present, are also visible to reviewers. Once a reviewer has drafted a set of comments, they need to *publish* them in order for the author to see them; this has the advantage of allowing a reviewer to provide a complete thought on a change atomically, after having reviewed the entire change. Anyone can comment on changes, providing a “drive-by review” as they see it necessary.
4. **Modify change and reply to comments.** The author modifies the change, uploads new snapshots based on the feedback, and replies back to the reviewers. The author addresses (at least) all unresolved comments, either by changing the code or just replying to the comment and changing the comment type to be *resolved*. The author and reviewers can look at diffs between any pairs of snapshots to see what changed. Steps 3 and 4 might be repeated multiple times.
5. **Change approval.** When the reviewers are happy with the latest state of the change, they approve the change and mark it as “looks good to me” (LGTM). They can optionally include comments to address. After a change is deemed good for submission, it is clearly marked green in the UI to show this state.
6. **Commit a change.** Provided the change is approved (which we’ll discuss shortly), the author can trigger the commit process of the change. If automatic analyzers and other precommit hooks (called “presubmits”) don’t find any problems, the change is committed to the codebase.

典型的审查步骤如下：

1. **创建变更。** 用户在自己的工作区中修改代码库。这位*作者*随后向 Critique 上传一个*快照*，呈现某个时间点的补丁，并触发自动代码分析器运行（见第20章）。
2. **请求审查。** 作者确认变更的差异以及 Critique 中显示的分析结果符合预期后，通过邮件将变更发送给一位或多位审查者。
3. **提出审查意见。** 审查者在 Critique 中打开变更，针对 diff 起草审查意见。意见默认标记为*未解决*，表示作者必须认真处理。审查者也可以添加标记为*已解决*的意见，供作者参考或选择是否采纳。如果有自动代码分析结果，审查者也能看到。起草完一组意见后，审查者需要将其*发布*，作者才能看到。这样，审查者可以先看完整项变更，再一次性给出完整意见。任何人都可以对变更提出意见，在认为有必要时进行“顺路审查”。
4. **修改变更并回复审查意见。** 作者根据反馈修改变更、上传新快照，并回复审查者。作者至少要处理所有未解决的意见：可以修改代码，也可以直接回复意见，并将其状态改为*已解决*。作者和审查者可以比较任意两个快照，查看其中的差异。步骤3和4可能重复多次。
5. **批准变更。** 审查者对变更的最新状态满意后，就会批准变更，标记为“看起来没问题”（LGTM）。此时仍可以附上需要作者处理的审查意见。当变更满足提交条件时，UI 会用醒目的绿色标明这一状态。
6. **提交变更。** 变更获得批准后，作者便可以启动提交流程，具体批准条件稍后介绍。如果自动分析器和其他提交前钩子（称为“presubmits”）都未发现问题，变更就会提交到代码库。

Even after the review process is started, the entire system provides significant flexibility to deviate from the regular review flow. For example, reviewers can un-assign themselves from the change or explicitly assign it to someone else, and the author can postpone the review altogether. In emergency cases, the author can forcefully commit their change and have it reviewed after commit.

即使审查已经开始，系统仍允许灵活调整，不必拘泥于常规流程。例如，审查者可以退出某项变更的审查，也可以明确将审查任务转交给其他人；作者则可以推迟整个审查。在紧急情况下，作者可以强制提交变更，再进行提交后审查。

### Notifications 通知

As a change moves through the stages outlined earlier, Critique publishes event notifications that might be used by other supporting tools. This notification model allows Critique to focus on being a primary code review tool instead of a general purpose tool, while still being integrated into the developer workflow. Notifications enable a separation of concerns such that Critique can just emit events and other systems build off of those events.

随着变更依次进入前述各阶段，Critique 会发布事件通知，供其他辅助工具使用。这种通知模型让 Critique 在融入开发者工作流的同时，仍以代码审查为核心，而不必成为通用工具。通知实现了关注点分离：Critique 只需发出事件，其他系统则基于这些事件提供各自的功能。

For example, users can install a Chrome extension that consumes these event notifications. When a change needs the user’s attention—for example, because it is their turn to review the change or some presubmit fails—the extension displays a Chrome notification with a button to go directly to the change or silence the notification. We have found that some developers really like immediate notification of change updates, but others choose not to use this extension because they find it is too disruptive to their flow.

例如，用户可以安装一个接收这些事件通知的 Chrome 扩展。当某项变更需要用户关注时，比如轮到用户审查，或某项提交前检查失败，扩展就会显示 Chrome 通知，并提供按钮，让用户直接转到该变更或将通知静音。我们发现，一些开发者很喜欢即时收到变更更新通知，另一些人则觉得这会过多打断工作，因此选择不使用这个扩展。

Critique also manages emails related to a change; important Critique events trigger email notifications. In addition to being displayed in the Critique UI, some analyzer findings are configured to also send the results out by email. Critique also processes email replies and translates them to comments, supporting users who prefer an email-based flow. Note that for many users, emails are not a key feature of code review; they use Critique’s dashboard view (discussed later) to manage reviews.

Critique 也管理与变更有关的电子邮件，重要事件会触发邮件通知。部分分析结果除了显示在 Critique UI 中，还会按配置通过邮件发送。Critique 还会处理邮件回复，将其转换为审查意见，以支持偏好邮件工作流的用户。不过，对许多用户而言，邮件并不是代码审查的关键功能，他们通过 Critique 的仪表板视图管理审查，后文会介绍这一视图。

## Stage 1: Create a Change 阶段1：创建变更

A code review tool should provide support at all stages of the review process and should not be the bottleneck for committing changes. In the prereview step, making it easier for change authors to polish a change before sending it out for review helps reduce the time taken by the reviewers to inspect the change. Critique displays change diffs with knobs to ignore whitespace changes and highlight move-only changes. Critique also surfaces the results from builds, tests, and static analyzers, including style checks (as discussed in Chapter 9).

代码审查工具应支持审查流程的各个阶段，而不应成为提交变更的瓶颈。在送审前，让作者更方便地完善变更，有助于缩短审查者检查变更的时间。Critique 提供变更差异视图，并允许用户忽略空白字符的变化，突出显示仅移动代码的变更。它还展示构建、测试和静态分析器的结果，包括第9章讨论的代码风格检查。

Showing an author the diff of a change gives them the opportunity to wear a different hat: that of a code reviewer. Critique lets a change author see the diff of their changes as their reviewer will, and also see the automatic analysis results. Critique also supports making lightweight modifications to the change from within the review tool and suggests appropriate reviewers. When sending out the request, the author can also include preliminary comments on the change, providing the opportunity to ask reviewers directly about any open questions. Giving authors the chance to see a change just as their reviewers do prevents misunderstanding.

向作者展示变更差异，让他们有机会换到代码审查者的视角。Critique 为作者提供与审查者相同的差异视图，也展示自动分析结果。作者还可以直接在审查工具中作小幅修改，并获得合适的审查者推荐。发送审查请求时，作者可以附上初步意见，就尚未解决的问题直接向审查者提问。让作者从审查者的视角查看变更，有助于避免误解。

To provide further context for the reviewers, the author can also link the change to a specific bug. Critique uses an autocomplete service to show relevant bugs, prioritizing bugs that are assigned to the author.

为了给审查者提供更多上下文，作者还可以将变更关联到具体的缺陷记录。Critique 通过自动补全服务显示相关缺陷，并优先列出分配给作者的缺陷。

### Diffing 差异比较

The core of the code review process is understanding the code change itself. Larger changes are typically more difficult to understand than smaller ones. Optimizing the diff of a change is thus a core requirement for a good code review tool.

代码审查的核心是理解代码变更本身。大变更通常比小变更更难理解，因此，优化差异展示是优秀代码审查工具的一项核心要求。

In Critique, this principle translates onto multiple layers (see Figure 19-2). The diffing component, starting from an optimized longest common subsequence algorithm, is enhanced with the following:

- Syntax highlighting
- Cross-references (powered by Kythe; see Chapter 17)
- Intraline diffing that shows the difference on character-level factoring in the word boundaries (Figure 19-2)
- An option to ignore whitespace differences to a varying degree
- Move detection, in which chunks of code that are moved from one place to another are marked as being moved (as opposed to being marked as removed here and added there, as a naive diff algorithm would)

在 Critique 中，这一原则体现在多个层面（见图19-2）。差异比较组件以经过优化的最长公共子序列算法为基础，并增加了以下功能：

- 语法高亮
- 交叉引用（由 Kythe 提供，见第17章）
- 行内差异比较，在考虑单词边界的同时显示字符级差异（图19-2）
- 可选择在不同程度上忽略空白字符差异
- 移动检测，将从一处移到另一处的代码块标记为已移动，而不是像朴素的 diff 算法那样，标记为在原处删除、在新位置添加

![Figure 19-2](./images/Figure%2019-2.png)

*Figure 19-2. Intraline diffing showing character-level differences*

Users can also view the diff in various different modes, such as overlay and side by side. When developing Critique, we decided that it was important to have side-by- side diffs to make the review process easier. Side-by-side diffs take a lot of space: to make them a reality, we had to simplify the diff view structure, so there is no border, no padding—just the diff and line numbers. We also had to play around with a variety of fonts and sizes until we had a diff view that accommodates even for Java’s 100- character line limit for the typical screen-width resolution when Critique launched (1,440 pixels).

用户还可以用叠加、并排等不同模式查看 diff。开发 Critique 时，我们认为并排差异视图对简化审查很重要。不过，并排展示占用的空间很大。为此，我们简化了 diff 视图的结构，去掉边框和内边距，只保留差异内容和行号。我们还反复尝试不同字体和字号，最终让视图在 Critique 推出时常见的1440像素屏幕宽度下，也能容纳 Java 每行最多100个字符的代码。

Critique further supports a variety of custom tools that provide diffs of artifacts produced by a change, such as a screenshot diff of the UI modified by a change or configuration files generated by a change.

Critique 还支持多种定制工具，用来展示变更所产生制品的 diff，例如变更前后 UI 的截图差异，或变更生成的配置文件差异。

To make the process of navigating diffs smooth, we were careful not to waste space and spent significant effort ensuring that diffs load quickly, even for images and large files and/or changes. We also provide keyboard shortcuts to quickly navigate through files while visiting only modified sections.

为了让 diff 浏览流畅，我们尽量避免浪费空间，并投入大量精力确保差异视图快速加载，即使涉及图片、大文件或大变更也是如此。我们还提供快捷键，让用户在文件间快速跳转，并只浏览修改过的部分。

When users drill down to the file level, Critique provides a UI widget with a compact display of the chain of snapshot versions of a file; users can drag and drop to select which versions to compare. This widget automatically collapses similar snapshots, drawing focus to important snapshots. It helps the user understand the evolution of a file within a change; for example, which snapshots have test coverage, have already been reviewed, or have comments. To address concerns of scale, Critique prefetches everything, so loading different snapshots is very quick.

进入单个文件后，Critique 会用一个紧凑的 UI 组件展示该文件的一系列快照版本，用户可以通过拖放选择要比较的版本。组件会自动折叠相似快照，让重要快照更醒目，帮助用户理解文件在一项变更中的演进，例如哪些快照有测试覆盖信息、已经过审查，或附有审查意见。为应对规模问题，Critique 会预取所有内容，因此加载不同快照非常快。

### Analysis Results 分析结果

Uploading a snapshot of the change triggers code analyzers (see Chapter 20). Critique displays the analysis results on the change page, summarized by analyzer status chips shown below the change description, as depicted in Figure 19-3, and detailed in the Analysis tab, as illustrated in Figure 19-4.

上传变更快照会触发代码分析器运行（见第20章）。Critique 在变更页面展示分析结果：变更描述下方的分析器状态标签汇总结果，如图19-3所示；Analysis 选项卡则提供详细信息，如图19-4所示。

Analyzers can mark specific findings to highlight in red for increased visibility. Analyzers that are still in progress are represented by yellow chips, and gray chips are displayed otherwise. For the sake of simplicity, Critique offers no other options to mark or highlight findings—actionability is a binary option. If an analyzer produces some results (“findings”), clicking the chip opens up the findings. Like comments, findings can be displayed inside the diff but styled differently to make them easily distinguishable. Sometimes, the findings also include fix suggestions, which the author can preview and choose to apply from Critique.

分析器可以将特定检查结果标为红色，使其更醒目。仍在运行的分析器用黄色状态标签表示，其余则显示灰色。为保持简洁，Critique 不提供其他标记或突出显示检查结果的选项，只区分结果是否需要采取行动。如果分析器产生了检查结果，点击状态标签即可查看。这些结果与审查意见一样，可以显示在 diff 中，但采用不同样式，便于区分。有些检查结果还附带修复建议，作者可以在 Critique 中预览，并选择是否应用。

![Figure 19-3](./images/Figure%2019-3.png)

*Figure* *19-3.* *Change* *summary* *and* *diff*  view

![Figure 19-4](./images/Figure%2019-4.png)

*Figure* *19-4.* *Analysis* *results*

For example, suppose that a linter finds a style violation of extra spaces at the end of the line. The change page will display a chip for that linter. From the chip, the author can quickly go to the diff showing the offending code to understand the style violation with two clicks. Most linter violations also include fix suggestions. With a click, the author can preview the fix suggestion (for example, remove the extra spaces), and with another click, apply the fix on the change.

例如，假设代码风格检查工具（linter）发现某行末尾有多余空格，违反了风格规范。变更页面就会显示该 linter 的状态标签。作者从标签出发，只需点击两次，就能转到包含违规代码的 diff，了解问题所在。linter 报告的大多数违规项还附带修复建议。作者点击一次即可预览建议，例如删除多余空格，再点击一次便可将修复应用到变更中。

### Tight Tool Integration 紧密的工具集成

Google has tools built on top of Piper, its monolithic source code repository (see [Chapter 16](#_bookmark1364)), such as the following:

- Cider, an online IDE for editing source code stored in the cloud
- Code Search, a tool for searching code in the codebase
- Tricorder, a tool for displaying static analysis results (mentioned earlier)
- Rapid, a release tool that packages and deploys binaries containing a series of changes
- Zapfhahn, a test coverage calculation tool

谷歌在单体源代码仓库 Piper（见第16章）之上构建了一系列工具，例如：

- Cider：在线 IDE，用于编辑存储在云端的源代码
- Code Search：在代码库中搜索代码的工具
- Tricorder：前面提到的静态分析结果展示工具
- Rapid：发布工具，用于打包和部署包含一系列变更的二进制文件
- Zapfhahn：测试覆盖率计算工具

Additionally, there are services that provide context on change metadata (for example, about users involved in a change or linked bugs). Critique is a natural melting pot for a quick one-click/hover access or even embedded UI support to these systems, although we need to be careful not to sacrifice simplicity. For example, from a change page in Critique, the author needs to click only once to start editing the change further in Cider. There is support to navigate between cross-references using Kythe or view the mainline state of the code in Code Search (see Chapter 17). Critique links out to the release tool so that users can see whether a submitted change is in a specific release. For these tools, Critique favors links rather than embedding so as not to distract from the core review experience. One exception here is test coverage: the information of whether a line of code is covered by a test is shown by different background colors on the line gutter in the file’s diff view (not all projects use this coverage tool).

此外，还有服务为变更元数据提供上下文，例如参与变更的用户或关联的缺陷记录。Critique 很适合汇集这些系统的入口，让用户点击一次或悬停鼠标即可快速访问，甚至可以直接嵌入它们的 UI，但集成时必须注意保持简洁。例如，作者在 Critique 的变更页面只需点击一次，就能转到 Cider 继续编辑。用户也可以通过 Kythe 在交叉引用之间跳转，或在 Code Search 中查看代码主干的状态（见第17章）。Critique 还提供发布工具的链接，方便用户确认某项已提交的变更是否包含在特定发布版本中。对于这些工具，Critique 优先使用链接而非嵌入式界面，以免分散用户对代码审查这一核心任务的注意力。测试覆盖率是一个例外：文件的 diff 视图会在行号栏用不同背景色表示各行是否被测试覆盖，但并非所有项目都使用这一覆盖率工具。

Note that tight integration between Critique and a developer’s workspace is possible because of the fact that workspaces are stored in a FUSE-based filesystem, accessible beyond a particular developer’s computer. The Source of Truth is hosted in the cloud and accessible to all of these tools.

Critique 之所以能与开发者工作区紧密集成，是因为工作区存储在基于 FUSE 的文件系统中，不仅可以从该开发者的计算机访问，也可以从其他地方访问。作为权威来源的数据托管在云端，所有这些工具都能访问。

## Stage 2: Request Review 阶段2：请求审查

After the author is happy with the state of the change, they can send it for review, as depicted in Figure 19-5. This requires the author to pick the reviewers. Within a small team, finding a reviewer might seem simple, but even there it is useful to distribute reviews evenly across team members and consider situations like who is on vacation. To address this, teams can provide an email alias for incoming code reviews. The alias is used by a tool called *GwsQ* (named after the initial team that used this technique:  
(Google Web Server) that assigns specific reviewers based on the configuration linked to the alias. For example, a change author can assign a review to some-team-list-alias, and GwsQ will pick a specific member of some-team-list-alias to perform the review.

作者对变更的状态满意后，就可以将其送审，如图19-5所示。这需要作者选择审查者。在小团队中，找到审查者似乎很容易，但即便如此，均衡分配审查任务、考虑成员休假等情况仍然很有必要。为此，团队可以提供一个接收代码审查请求的邮件别名，由名为 *GwsQ* 的工具使用。工具名称来自最先采用这一做法的团队：
谷歌 Web 服务器团队（Google Web Server）。GwsQ 根据与别名关联的配置指派具体审查者。例如，作者可以把审查任务分配给某个团队邮件列表的别名，GwsQ 随后会从该列表中选择一位成员负责审查。

![Figure 19-5](./images/Figure%2019-5.png)

Figure 19-5. Requesting reviewers

Given the size of Google’s codebase and the number of people modifying it, it can be difficult to find out who is best qualified to review a change outside your own project. Finding reviewers is a problem to consider when reaching a certain scale. Critique must deal with scale. Critique offers the functionality to propose sets of reviewers that are sufficient to approve the change. The reviewer selection utility takes into account the following factors:

- Who owns the code that is being changed (see the next section)
- Who is most familiar with the code (i.e., who recently changed it)
- Who is available for review (i.e., not out of office and preferably in the same time zone)
- The GwsQ team alias setup

谷歌的代码库庞大，修改代码的人也很多，因此，为自己项目之外的变更找到最合适的审查者并不容易。达到一定规模后，如何寻找审查者就成了必须考虑的问题，Critique 也不例外。它可以推荐能满足变更批准要求的审查者组合。审查者选择工具会考虑以下因素：

- 谁是被修改代码的所有者（见下一节）
- 谁最熟悉这些代码，即谁最近修改过它们
- 谁能参与审查，即没有休假或离岗，最好还在同一时区
- GwsQ 的团队别名配置

Assigning a reviewer to a change triggers a review request. This request runs “presubmits” or precommit hooks applicable to the change; teams can configure the presubmits related to their projects in many ways. The most common hooks include the following:

- Automatically adding email lists to changes to raise awareness and transparency
- Running automated test suites for the project
- Enforcing project-specific invariants on both code (to enforce local code style restrictions) and change descriptions (to allow generation of release notes or other forms of tracking)

为变更指派审查者会触发审查请求，进而运行适用于该变更的提交前钩子，也称为“presubmits”。团队可以按多种方式配置项目的提交前检查。常见的钩子包括：

- 自动将邮件列表加入变更的通知范围，让更多人了解变更，提高透明度
- 为项目运行自动化测试套件
- 检查代码和变更描述是否始终满足项目特定的约束：前者用于强制执行项目的代码风格要求，后者便于生成发布说明或以其他方式跟踪变更

As running tests is resource intensive, at Google they are part of presubmits (run when requesting review and when committing changes) rather than for every snapshot like Tricorder checks. Critique surfaces the result of running the hooks in a similar way to how analyzer results are displayed, with an extra distinction to highlight the fact that a failed result blocks the change from being sent for review or committed. Critique notifies the author via email if presubmits fail.

运行测试消耗的资源较多，因此在谷歌，测试属于提交前检查，在请求审查和提交变更时运行，而不像 Tricorder 检查那样对每个快照运行。Critique 展示钩子执行结果的方式与分析结果相似，但会额外标明：检查失败会阻止变更送审或提交。提交前检查失败时，Critique 会通过邮件通知作者。

## Stages 3 and 4: Understanding and Commenting on a Change 阶段3和4：理解变更并提出审查意见

After the review process starts, the author and the reviewers work in tandem to reach the goal of committing changes of high quality.

审查开始后，作者与审查者共同协作，目标是提交高质量的变更。

### Commenting 提出审查意见

Making comments is the second most common action that users make in Critique after viewing changes (Figure 19-6). Commenting in Critique is free for all. Anyone—not only the change author and the assigned reviewers—can comment on a change.

在 Critique 中，用户最常进行的操作是查看变更，其次就是提出审查意见（图19-6）。这项功能向所有人开放，任何人都可以对变更提出意见，不限于变更作者和指定的审查者。

Critique also offers the ability to track review progress via per-person state. Reviewers have checkboxes to mark individual files at the latest snapshot as reviewed, helping the reviewer keep track of what they have already looked at. When the author modifies a file, the “reviewed” checkbox for that file is cleared for all reviewers because the latest snapshot has been updated.

Critique 还会为每位审查者分别记录状态，方便跟踪审查进度。审查者可以通过复选框，将最新快照中的各个文件标记为已审查，以便知道自己已经看过哪些内容。当作者修改文件、更新最新快照后，系统会清除所有审查者对该文件的“已审查”勾选。

![Figure 19-6](./images/Figure%2019-6.png)

*Figure 19-6. Commenting on the diff view*

When a reviewer sees a relevant analyzer finding, they can click a “Please fix” button to create an unresolved comment asking the author to address the finding. Reviewers can also suggest a fix to a change by inline editing the latest version of the file. Critique transforms this suggestion into a comment with a fix attached that can be applied by the author.

审查者看到相关的分析器检查结果时，可以点击“Please fix”按钮，创建一条未解决的审查意见，请作者处理该问题。审查者还可以直接在页面中编辑文件的最新版本，提出修复建议。Critique 会将建议转换为一条审查意见，并附上作者可以应用的修复。

Critique does not dictate what comments users should create, but for some common comments, Critique provides quick shortcuts. The change author can click the “Done” button on the comment panel to indicate when a reviewer’s comment has been addressed, or the “Ack” button to acknowledge that the comment has been read, typically used for informational or optional comments. Both have the effect of resolving the comment thread if it is unresolved. These shortcuts simplify the workflow and reduce the time needed to respond to review comments.

Critique 不规定用户应提出什么意见，但为常见回复提供了快捷操作。变更作者可以点击审查意见面板上的“Done”按钮，表示已处理该意见；也可以点击“Ack”按钮，确认已经阅读，这通常用于供参考或可选择采纳的意见。如果这条意见所在的讨论串尚未解决，两种操作都会将其标记为已解决。这些快捷操作简化了工作流，缩短了回复审查意见所需的时间。

As mentioned earlier, comments are drafted as-you-go, but then “published” atomically, as shown in Figure 19-7. This allows authors and reviewers to ensure that they are happy with their comments before sending them out.

如前所述，审查意见可以边看边写，但会在完成后一次性整体“发布”，如图19-7所示。这样，作者和审查者都可以先确认意见表达妥当，再将其发送出去。

![Figure 19-7](./images/Figure%2019-7.png)

*Figure 19-7. Preparing comments to the author*

### Understanding the State of a Change 了解变更状态

Critique provides a number of mechanisms to make it clear where in the comment- and-iterate phase a change is currently located. These include a feature for determining who needs to take action next, and a dashboard view of review/author status for all of the changes with which a particular developer is involved.

Critique 提供了多种机制，让用户清楚了解变更在意见交流和迭代过程中进展到哪一步。这些机制包括确定下一步由谁处理的功能，以及汇总开发者所参与全部变更的仪表板，展示其作为审查者或作者时的相关状态。

#### “Whose turn” feature “轮到谁”功能

One important factor in accelerating the review process is understanding when it’s your turn to act, especially when there are multiple reviewers assigned to a change. This might be the case if the author wants to have their change reviewed by a software engineer and the user-experience person responsible for the feature, or the SRE carrying the pager for the service. Critique helps define who is expected to look at the change next by managing an *attention set* for each change.

要加快审查，一个重要因素是清楚何时轮到自己处理，尤其是在一项变更有多位审查者时。例如，作者可能希望软件工程师与负责该功能的用户体验人员共同审查，或请负责该服务值班的 SRE 参与审查。Critique 为每项变更管理一个关注集，帮助明确接下来应由谁查看变更。

The attention set comprises the set of people on which a change is currently blocked. When a reviewer or author is in the attention set, they are expected to respond in a timely manner. Critique tries to be smart about updating the attention set when a user publishes their comments, but users can also manage the attention set themselves. Its usefulness increases even more when there are more reviewers in the change. The attention set is surfaced in Critique by rendering the relevant usernames in bold.

关注集包含当前需要作出回应、变更才能继续推进的人员。审查者或作者进入关注集后，就应及时回应。用户发布审查意见时，Critique 会尝试智能更新关注集，用户也可以自行管理。参与一项变更的审查者越多，关注集的作用就越大。Critique 通过加粗相关用户名来标示关注集成员。

After we implemented this feature, our users had a difficult time imagining the previous state. The prevailing opinion is: how did we get along without this? The alternative before we implemented this feature was chatting between reviewers and authors to understand who was dealing with a change. This feature also emphasizes the turn- based nature of code review; it is always at least one person’s turn to take action.

推出这项功能后，用户很难想象再回到从前的状态。大家普遍的反应是：“以前没有它，我们是怎么做的？”此前，审查者和作者需要通过聊天确认谁正在处理变更。这项功能也突出了代码审查轮流推进的特点：任何时候，都至少有一个人需要采取行动。

#### Dashboard and search system 仪表板和搜索系统

Critique’s landing page is the user’s dashboard page, as depicted in Figure 19-8. The dashboard page is divided into user-customizable sections, each of them containing a list of change summaries.

Critique 的首页就是用户的仪表板，如图19-8所示。仪表板分成多个可由用户自定义的区域，每个区域都包含一份变更摘要列表。

![Figure 19-8](./images/Figure%2019-8.png)

*Figure* *19-8. Dashboard view*

The dashboard page is powered by a search system called *Changelist Search*. Changelist Search indexes the latest state of all available changes (both pre- and post-submit) across all users at Google and allows its users to look up relevant changes by regular expression–based queries. Each dashboard section is defined by a query to Changelist Search. We have spent time ensuring Changelist Search is fast enough for interactive use; everything is indexed quickly so that authors and reviewers are not slowed down, despite the fact that we have an extremely large number of concurrent changes happening simultaneously at Google.

仪表板由名为 *Changelist Search* 的搜索系统支撑。该系统为谷歌所有用户的全部可用变更建立索引，记录其最新状态，包括提交前和提交后的状态，并支持用正则表达式查询相关变更。仪表板的每个区域都由一条 Changelist Search 查询定义。我们投入了时间，确保搜索速度能满足交互使用的需要。尽管谷歌有大量变更同时进行，所有内容仍能迅速建立索引，不会拖慢作者和审查者的工作。

To optimize the user experience (UX), Critique’s default dashboard setting is to have the first section display the changes that need a user’s attention, although this is customizable. There is also a search bar for making custom queries over all changes and browsing the results. As a reviewer, you mostly just need the attention set. As an author, you mostly just need to take a look at what is still waiting for review to see if you need to ping any changes. Although we have shied away from customizability in some other parts of the Critique UI, we found that users like to set up their dashboards differently without detracting from the fundamental experience, similar to the way everyone organizes their emails differently.[^1]

为改善用户体验（UX），Critique 的仪表板默认在第一个区域显示需要用户关注的变更，用户也可以调整这一设置。页面还提供搜索栏，用于对全部变更执行自定义查询并浏览结果。作为审查者，你通常只需关注将你列入关注集的变更；作为作者，你通常只需查看哪些变更仍在等待审查，判断是否需要催促。虽然我们在 Critique UI 的其他一些部分避免提供自定义选项，但在仪表板上，用户喜欢按各自习惯设置，又不会影响核心体验，就像每个人整理邮件的方式各不相同。

> [^1]: Centralized “global” reviewers for large-scale changes (LSCs) are particularly prone to customizing this dashboard to avoid flooding it during an LSC (see Chapter 22).
>
> 1 集中负责大规模变更（LSCs）的“全局”审查者尤其倾向于自定义仪表板，以免在进行大规模变更时，仪表板被相关变更淹没（见第22章）。

## Stage 5: Change Approvals (Scoring a Change) 阶段5：变更批准（对变更进行评分）

Showing whether a reviewer thinks a change is good boils down to providing concerns and suggestions via comments. There also needs to be some mechanism for providing a high-level “OK” on a change. At Google, the scoring for a change is divided into three parts:

- LGTM (“looks good to me”)
- Approval
- The number of unresolved comments

审查者是否认可一项变更，最终会体现在审查意见中提出的问题和建议上。此外，还需要一种机制，表示对变更的整体认可。在谷歌，变更评分分为三个部分：

- LGTM（“看起来没问题”）
- 批准
- 未解决的审查意见数量

An LGTM stamp from a reviewer means that “I have reviewed this change, believe that it meets our standards, and I think it is okay to commit it after addressing unresolved comments.” An Approval stamp from a reviewer means that “as a gatekeeper, I allow this change to be committed to the codebase.” A reviewer can mark comments as unresolved, meaning that the author will need to act upon them. When the change has at least one LGTM, sufficient approvals and no unresolved comments, the author can then commit the change. Note that every change requires an LGTM regardless of approval status, ensuring that at least two pairs of eyes viewed the change. This simple scoring rule allows Critique to inform the author when a change is ready to commit (shown prominently as a green page header).

审查者给出 LGTM，表示：“我已经审查过这项变更，相信它符合我们的标准，并认为在处理完未解决的意见后就可以提交。”给出批准则表示：“作为把关人，我允许这项变更提交到代码库。”审查者可以将意见标记为未解决，表示作者需要处理。变更至少获得一个 LGTM、取得所需的全部批准，且没有未解决的意见时，作者才能提交。无论批准状态如何，每项变更都需要一个 LGTM，确保至少有两个人看过变更。借助这条简单的评分规则，Critique 能明确告知作者何时可以提交，并用绿色页眉醒目标示。

We made a conscious decision in the process of building Critique to simplify this rating scheme. Initially, Critique had a “Needs More Work” rating and also a “LGTM++”. The model we have moved to is to make LGTM/Approval always positive. If a change definitely needs a second review, primary reviewers can add comments but without LGTM/Approval. After a change transitions into a mostly-good state, reviewers will typically trust authors to take care of small edits—the tooling does not require repeated LGTMs regardless of change size.

开发 Critique 时，我们明确决定简化评分方案。最初，Critique 既有“还需修改”评级，也有“LGTM++”。后来采用的模型让 `LGTM/批准` 始终表示肯定。如果变更确实需要再次审查，主要审查者可以提出意见，但暂不给出 LGTM 或批准。变更基本达到要求后，审查者通常会信任作者自行完成小幅修改；无论变更大小如何，工具都不要求反复给出 LGTM。

This rating scheme has also had a positive influence on code review culture. Reviewers cannot just thumbs-down a change with no useful feedback; all negative feedback from reviewers must be tied to something specific to be fixed (for example, an unresolved comment). The phrasing “unresolved comment” was also chosen to sound relatively nice.

这套评分方案也对代码审查文化产生了积极影响。审查者不能只否定变更，却不给出有用的反馈；所有负面反馈都必须指向需要修复的具体问题，例如一条未解决的审查意见。选择“未解决的审查意见”这一措辞，也是为了让表达相对温和。

Critique includes a scoring panel, next to the analysis chips, with the following information:

- Who has LGTM’ed the change
- What approvals are still required and why
- How many unresolved comments are still open

Critique 在分析器状态标签旁提供了一个评分面板，展示以下信息：

- 谁已对变更给出 LGTM
- 还需要哪些批准，以及为什么需要
- 还有多少审查意见尚未解决

Presenting the scoring information this way helps the author quickly understand what they still need to do to get the change committed.

这样展示评分信息，能帮助作者迅速了解提交变更前还需要完成哪些工作。

LGTM and Approval are *hard* requirements and can be granted only by reviewers. Reviewers can also revoke their LGTM and Approval at any time before the change is committed. Unresolved comments are *soft* requirements; the author can mark a comment “resolved” as they reply. This distinction promotes and relies on trust and communication between the author and the reviewers. For example, a reviewer can LGTM the change accompanied with unresolved comments without later on checking precisely whether the comments are truly addressed, highlighting the trust the reviewer places on the author. This trust is particularly important for saving time when there is a significant difference in time zones between the author and the reviewer. Exhibiting trust is also a good way to build trust and strengthen teams.

LGTM 和批准是*硬性*要求，只能由审查者给出；在变更提交之前，审查者可以随时撤销。未解决的审查意见则是*软性*要求，作者可以在回复时自行将其标记为“已解决”。这种区分既促进了作者与审查者之间的信任和沟通，也以此为基础。例如，审查者可以在给出 LGTM 的同时留下未解决的意见，之后不再逐项核查作者是否确实处理，体现对作者的信任。作者与审查者的时区相差较大时，这種信任尤其有助于节省时间。主动信任他人，也有助于建立信任、增强团队凝聚力。

## Stage 6: Commiting a Change 阶段6：提交变更

Last but not least, Critique has a button for committing the change after the review to avoid context-switching to a command-line interface.

最后一个同样重要的功能是：Critique 提供了审查后直接提交变更的按钮，用户不必再切换到命令行界面。

### After Commit: Tracking History 提交后：跟踪历史记录

In addition to the core use of Critique as a tool for reviewing source code changes before they are committed to the repository, Critique is also used as a tool for change archaeology. For most files, developers can view a list of the past history of changes that modified a particular file in the Code Search system (see Chapter 17), or navigate directly to a change. Anyone at Google can browse the history of a change to generally viewable files, including the comments on and evolution of the change. This enables future auditing and is used to understand more details about why changes were made or how bugs were introduced. Developers can also use this feature to learn how changes were engineered, and code review data in aggregate is used to produce trainings.

Critique 的核心用途是在源代码变更提交到仓库之前进行审查，此外也用于变更考古。对于大多数文件，开发者可以在 Code Search 中查看修改过该文件的历史变更列表（见第17章），或直接跳转到某项变更。只要文件向全公司开放，谷歌任何人都可以浏览其变更历史，包括审查意见和变更的演进过程。这些记录可供日后审计，也能帮助开发者进一步理解为何作出某项变更，或缺陷是如何引入的。开发者还可以借此学习变更的设计与实现方法，汇总后的代码审查数据也会用来制作培训材料。

Critique also supports the ability to comment after a change is committed; for example, when a problem is discovered later or additional context might be useful for someone investigating the change at another time. Critique also supports the ability to roll back changes and see whether a particular change has already been rolled back.

Critique 也允许在变更提交后继续添加审查意见，例如后来发现了问题，或需要补充上下文，方便其他人日后追查这项变更。它还支持回滚变更，并查看某项变更是否已经回滚。

------

Case Study: Gerrit 案例研究：Gerrit

Although Critique is the most commonly used review tool at Google, it is not the only one. Critique is not externally available due to its tight interdependencies with our large monolithic repository and other internal tools. Because of this, teams at Google that work on open source projects (including Chrome and Android) or internal projects that can’t or don’t want to be hosted in the monolithic repository use a different code review tool: Gerrit.

Critique 是谷歌最常用的代码审查工具，但并非唯一选择。它与谷歌的大型单体代码仓库及其他内部工具存在紧密的相互依赖关系，因此不对外提供。谷歌负责开源项目的团队，包括 Chrome 和 Android 团队，以及内部项目无法或不愿托管在单体代码仓库中的团队，因而使用另一种代码审查工具：Gerrit。

Gerrit is a standalone, open source code review tool that is tightly integrated with the Git version control system. As such, it offers a web UI to many Git features including code browsing, merging branches, cherry-picking commits, and, of course, code review. In addition, Gerrit has a fine-grained permission model that we can use to restrict access to repositories and branches.

Gerrit 是一款独立的开源代码审查工具，与 Git 版本控制系统紧密集成。它为许多 Git 功能提供了 Web UI，包括浏览代码、合并分支、拣选提交，当然还有代码审查。此外，Gerrit 提供细粒度权限模型，可以限制对代码仓库和分支的访问。

Both Critique and Gerrit have the same model for code reviews in that each commit is reviewed separately. Gerrit supports stacking commits and uploading them for individual review. It also allows the chain to be committed atomically after it’s reviewed.

Critique 和 Gerrit 采用相同的代码审查模型：每个提交都单独审查。Gerrit 支持将多个提交堆叠成链，上传后逐个审查；整条提交链通过审查后，还可以作为一个原子操作整体提交。

Being open source, Gerrit accommodates more variants and a wider range of use cases; Gerrit’s rich plug-in system enables a tight integration into custom environments. To support these use cases, Gerrit also supports a more sophisticated scoring system. A reviewer can veto a change by placing a –2 score, and the scoring system is highly configurable.

作为开源工具，Gerrit 支持更多样的使用方式和更广泛的使用场景，丰富的插件系统让它能与定制环境紧密集成。为支持这些场景，Gerrit 还提供了更复杂的评分系统：审查者可以给出 -2 分来否决变更，评分规则也支持高度自定义。

You can learn more about Gerrit and see it in action at [*https://www.gerritcodereview.com*](https://www.gerritcodereview.com/).

你可以在[*https://www.gerritcodereview.com*](https://www.gerritcodereview.com/)进一步了解 Gerrit，并查看它的实际使用情况。

------

## Conclusion 总结

There are a number of implicit trade-offs when using a code review tool. Critique builds in a number of features and integrates with other tools to make the review process more seamless for its users. Time spent in code reviews is time not spent coding, so any optimization of the review process can be a productivity gain for the company. Having only two people in most cases (author and reviewer) agree on the change before it can be committed keeps velocity high. Google greatly values the educational aspects of code review, even though they are more difficult to quantify.

使用代码审查工具时，需要作出一些隐含的权衡。Critique 内置多项功能，并与其他工具集成，让用户的审查流程更加顺畅。花在代码审查上的时间就不能再用来写代码，因此，审查流程的任何优化都可能提高公司的生产力。在大多数情况下，变更只需作者和审查者两个人达成一致即可提交，有助于保持较快的开发速度。谷歌也十分重视代码审查的教育价值，尽管这种价值更难量化。

To minimize the time it takes for a change to be reviewed, the code review process should flow seamlessly, informing users succinctly of the changes that need their attention and identifying potential issues before human reviewers come in (issues are caught by analyzers and Continuous Integration). When possible, quick analysis results are presented before the longer-running analyses can finish.

要尽量缩短变更的审查时间，代码审查流程就应顺畅衔接，简明地告知用户哪些变更需要关注，并在人工审查开始前，由分析器和持续集成发现潜在问题。在条件允许时，应先展示快速分析的结果，不必等耗时更长的分析完成。

There are several ways in which Critique needs to support questions of scale. The Critique tool must scale to the large quantity of review requests produced without suffering a degradation in performance. Because Critique is on the critical path to getting changes committed, it must load efficiently and be usable for special situations such as unusually large changes.[^2] The interface must support managing user activities (such as finding relevant changes) over the large codebase and help reviewers and authors navigate the codebase. For example, Critique helps with finding appropriate reviewers for a change without having to figure out the ownership/maintainer landscape (a feature that is particularly important for large-scale changes such as API migrations that can affect many files).

Critique 需要从几个方面应对规模问题。它必须承载大量审查请求，而不降低性能。由于处在变更提交的关键路径上，Critique 必须快速加载，并能处理异常庞大的变更等特殊情况。界面还必须支持用户在大型代码库中开展工作，例如查找相关变更，并帮助审查者和作者浏览代码库。比如，Critique 可以为变更寻找合适的审查者，用户不必先弄清相关代码归谁所有、由谁维护。这对大规模变更尤其重要，例如可能影响许多文件的 API 迁移。

Critique favors an opinionated process and a simple interface to improve the general review workflow. However, Critique does allow some customizability: custom analyzers and presubmits provide specific context on changes, and some team-specific policies (such as requiring LGTM from multiple reviewers) can be enforced.

Critique 倾向于采用有明确设计取向的流程和简洁的界面，改善日常审查工作流。不过，它也允许一定程度的自定义：定制分析器和提交前检查可以提供与变更相关的特定上下文，也可以强制执行团队特有的策略，例如要求多位审查者给出 LGTM。

> [^2]: Although most changes are small (fewer than 100 lines), Critique is sometimes used to review large refactoring changes that can touch hundreds or thousands of files, especially for LSCs that must be executed atomically (see Chapter 22).
>
> 2 大多数变更都很小，不到100行，但 Critique 有时也用于审查涉及数百甚至数千个文件的大型重构变更，尤其是必须以原子方式执行的大规模变更（LSCs，见第22章）。

Trust and communication are core to the code review process. A tool can enhance the experience, but can’t replace them. Tight integration with other tools has also been a key factor in Critique’s success.

信任和沟通是代码审查流程的核心。工具可以改善体验，却无法取代它们。与其他工具紧密集成，也是 Critique 成功的关键因素。

## TL;DRs  内容提要

- Trust and communication are core to the code review process. A tool can enhance the experience, but it can’t replace them.
- Tight integration with other tools is key to great code review experience.
- Small workflow optimizations, like the addition of an explicit “attention set,” can increase clarity and reduce friction substantially.

- 信任和沟通是代码审查流程的核心。工具可以改善体验，却无法取代它们。
- 与其他工具紧密集成，是获得良好代码审查体验的关键。
- 工作流中的小幅优化，例如引入明确的“关注集”，就能让流程更清晰，大幅减少协作阻力。
