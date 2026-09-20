
**CHAPTER 16**

# Version Control and Branch Management

# 第十六章 版本控制和分支管理

**Written by Titus Winters**

**Edited by Lisa Carey**

Perhaps no software engineering tool is quite as universally adopted throughout the industry as version control. One can hardly imagine any software organization larger than a few people that doesn’t rely on a formal Version Control System (VCS) to manage its source code and coordinate activities between engineers.

在软件工程工具中，版本控制或许是全行业采用最广泛的一种。很难想象，一个不止几个人的软件组织，会不依靠正式的版本控制系统（VCS）来管理源代码、协调工程师的工作。

In this chapter, we’re going to look at why the use of version control has become such an unambiguous norm in software engineering, and we describe the various possible approaches to version control and branch management, including how we do it at scale across all of Google. We’ll also examine the pros and cons of various approaches; although we believe everyone should use version control, some version control policies and processes might work better for your organization (or in general) than others. In particular, we find “trunk-based development” as popularized by DevOps[^1] (one repository, no dev branches) to be a particularly scalable policy approach, and we’ll provide some suggestions as to why that is.

本章将讨论为什么使用版本控制已成为软件工程中如此明确的规范，并介绍版本控制和分支管理的各种做法，包括谷歌如何在全公司范围内大规模应用这些做法。我们还会分析各种方法的利弊。虽然我们认为人人都应使用版本控制，但无论是针对你的组织，还是从一般情况来看，不同策略和流程的效果都可能有所不同。尤其是，我们发现 DevOps 推广的“主干开发”（一个代码仓库，没有开发分支）特别有利于规模扩展，后文将解释其中的原因。

> [^1]: The DevOps Research Association, which was acquired by Google between the first draft of this chapter and publication, has published extensively on this in the annual “State of DevOps Report” and the book Accelerate. As near as we can tell, it popularized the terminology trunk-based development.
>
> 1 DevOps 研究协会在年度《DevOps 状况报告》和《加速》一书中，对此作了大量论述。从本章初稿完成到出版之间，该协会被谷歌收购。据我们所知，“主干开发”这一术语正是由它推广开来的。

## What Is Version Control?  什么是版本控制？

A VCS is a system that tracks revisions (versions) of files over time. A VCS maintains some metadata about the set of files being managed, and collectively a copy of the files and metadata is called a repository[^2] (repo for short). A VCS helps coordinate the activities of teams by allowing multiple developers to work on the same set of files simultaneously. Early VCSs did this by granting one person at a time the right to edit a file—that style of locking is enough to establish sequencing (an agreed-upon “which is newer,” an important feature of VCS). More advanced systems ensure that changes to a *collection* of files submitted at once are treated as a single unit (*atomicity* when a logical change touches multiple files). Systems like CVS (a popular VCS from the 90s) that didn’t have this atomicity for a commit were subject to corruption and lost changes. Ensuring atomicity removes the chance of previous changes being overwritten unintentionally, but requires tracking which version was last synced to—at commit time, the commit is rejected if any file in the commit has been modified at head since the last time the local developer synced. Especially in such a change-tracking VCS, a developer’s working copy of the managed files will therefore need metadata of its own. Depending on the design of the VCS, this copy of the repository can be a repository itself, or might contain a reduced amount of metadata—such a reduced copy is usually a “client” or “workspace.”

VCS 是跟踪文件历次修订（版本）的系统。它维护所管理文件集的元数据；一份文件副本连同这些元数据，统称为代码仓库（简称 repo）。VCS 允许多个开发者同时处理同一组文件，从而协调团队的工作。早期 VCS 每次只允许一个人编辑某个文件，这种锁定方式足以确定先后顺序，也就是对“哪个更新”达成一致，这是 VCS 的一项重要功能。更先进的系统会把一次提交中对*文件集合*的修改视为一个整体，也就是在一次逻辑变更涉及多个文件时保证原子性。CVS 等系统（CVS 是20世纪90年代流行的 VCS）不具备这种提交原子性，因而可能出现数据损坏和变更丢失。保证原子性可以避免先前的变更被无意覆盖，但也需要跟踪上次同步到了哪个版本：提交时，只要本次提交中的任何文件在开发者上次同步后又在主干最新版本中被修改过，提交就会遭到拒绝。因此，尤其是在这种跟踪变更的 VCS 中，开发者持有的受管理文件的工作副本也需要自己的元数据。具体取决于 VCS 的设计，这份仓库副本本身可以是完整的代码仓库，也可以只包含精简后的元数据；后一种副本通常称为“客户端”或“工作区”。

This seems like a lot of complexity: why is a VCS necessary? What is it about this sort of tool that has allowed it to become one of the few nearly universal tools for software development and software engineering?

这似乎引入了不少复杂性：为什么需要 VCS？是什么让它成为软件开发和软件工程中少数几种几乎普遍采用的工具之一？

Imagine for a moment working without a VCS. For a (very) small group of distributed developers working on a project of limited scope without any understanding of version control, the simplest and lowest-infrastructure solution is to just pass copies of the project back and forth. This works best when edits are nonsimultaneous (people are working in different time zones, or at least with different working hours). If there’s any chance for people to not know which version is the most current, we immediately have an annoying problem: tracking which version is the most up to date. Anyone who has attempted to collaborate in a non-networked environment will likely recall the horrors of copying back-and-forth files named *Presentation v5 - final - redlines - Josh’s version v2*. And as we shall see, when there isn’t a single agreed-upon source of truth, collaboration becomes high friction and error prone.

设想一下没有 VCS 时如何工作。一小群分散各地的开发者，如果对版本控制一无所知，又只在开发一个范围有限的项目，最简单、对基础设施要求最低的办法，就是来回传递项目副本。在大家不同时编辑的情况下，这种办法效果最好，比如大家身处不同时区，或至少工作时间不同。可一旦有人无法确定哪个版本最新，就会立刻遇到一个烦人的问题：如何识别最新版本。凡是尝试过在没有网络的环境中协作的人，大概都记得来回复制名为 *Presentation v5 - final - redlines - Josh's version v2* 的文件有多痛苦。正如后文所述，没有一个大家认可的唯一权威来源，协作就会阻力重重，而且容易出错。

Introducing shared storage requires slightly more infrastructure (getting access to shared storage), but provides an easy and obvious solution. Coordinating work in a shared drive might suffice for a while with a small enough number of people but still requires out-of-band collaboration to avoid overwriting one another’s work. Further, working directly in that shared storage means that any development task that doesn’t keep the build working continuously will begin to impede everyone on the team—if I’m making a change to some part of this system at the same time that you kick off a build, your build won’t work. Obviously, this doesn’t scale well.

引入共享存储需要多一点基础设施，也就是获得共享存储的访问权限，但它提供了一个简单直观的解决方案。人数足够少时，借助共享磁盘协调工作或许能应付一阵子，不过大家仍需在系统之外相互协调，避免覆盖彼此的工作。此外，如果直接在共享存储中开发，任何不能始终保持构建正常的任务，都会妨碍整个团队：你启动构建时，如果我正在修改系统的某个部分，你的构建就会失败。显然，这种方式不利于规模扩展。

In practice, lack of file locking and lack of merge tracking will inevitably lead to collisions and work being overwritten. Such a system is very likely to introduce out-of-band coordination to decide who is working on any given file. If that file-locking is encoded in software, we’ve begun reinventing an early-generation version control like RCS (among others). After you realize that granting write permissions a file at a time is too coarse grained and you begin wanting line-level tracking—we’re definitely reinventing version control. It seems nearly inevitable that we’ll want some structured mechanism to govern these collaborations. Because we seem to just be reinventing the wheel in this hypothetical, we might as well use an off-the-shelf tool.

实践中，缺少文件锁和合并跟踪，必然会导致冲突和工作成果被覆盖。使用这样的系统，大家很可能需要在系统之外协调，决定每个文件由谁修改。如果用软件来实现文件锁，就已经开始重新发明 RCS 之类的早期版本控制系统了。等到你发现以整个文件为单位授予写权限粒度太粗，开始需要逐行跟踪时，就更是在重新发明版本控制。看来，我们几乎必然需要某种结构化机制来管理这些协作。既然这个假设推演最终还是在重复造轮子，不如直接使用现成工具。

> [^2]: Although the formal idea of what is and is not a repository changes a bit depending on your choice of VCS, and the terminology will vary.
>
> 2 不过，具体什么算作代码仓库，会随所选 VCS 略有不同，相关术语也不尽相同。

### Why Is Version Control Important?  为什么版本控制很重要？

While version control is practically ubiquitous now, this was not always the case. The very first VCSs date back to the 1970s (SCCS) and 1980s (RCS)—many years later than the first references to software engineering as a distinct discipline. Teams participated in “the [multiperson development of multiversion software](https://arxiv.org/pdf/1805.02742.pdf)” before the industry had any formal notion of version control. Version control evolved as a response to the novel challenges of digital collaboration. It took decades of evolution and dissemination for reliable, consistent use of version control to evolve into the norm that it is today.[^3] So how did it become so important, and, given that it seems like a self-evident solution, why might anyone resist the idea of VCS?

版本控制如今几乎无处不在，但过去并非如此。最早的 VCS 出现在20世纪70年代（SCCS）和80年代（RCS），比软件工程首次被视为独立学科晚了许多年。在业界正式形成版本控制的概念之前，团队就已经在开展“[多版本软件的多人开发](https://arxiv.org/pdf/1805.02742.pdf)”。版本控制的发展，是为了应对数字化协作带来的新挑战。经过几十年的演进和普及，可靠、持续地使用版本控制才成为今天的规范。那么，它为什么变得如此重要？既然这套解决方案看起来理所当然，又为什么会有人抵触 VCS？

Recall that software engineering is programming integrated over time; we’re drawing a distinction (in dimensionality) between the instantaneous production of source code and the act of maintaining that product over time. That basic distinction goes a long way to explaining the importance of, and hesitation toward, VCS: at the most fundamental level, version control is the engineer’s primary tool for managing the interplay between raw source and time. We can conceptualize VCS as a way to extend a standard filesystem. A filesystem is a mapping from filename to contents. A VCS extends that to provide a mapping from (filename, time) to contents, along with the metadata necessary to track last sync points and audit history. Version control makes the consideration of time an explicit part of the operation: unnecessary in a program‐ming task, critical in a software engineering task. In most cases, a VCS also allows for an extra input to that mapping (a branch name) to allow for parallel mappings; thus:

回想一下，软件工程是编程在时间上的积分。我们从维度上区分了某一时刻写出源代码，与此后持续维护这些代码。这一根本区别，很大程度上既解释了 VCS 为什么重要，也解释了人们为什么对它有所迟疑：版本控制最基本的作用，是帮助工程师管理源代码与时间之间的相互影响。可以把 VCS 看作对标准文件系统的扩展。文件系统把文件名映射到文件内容；VCS 则把（文件名，时间）映射到文件内容，并提供跟踪上次同步点和审计历史所需的元数据。版本控制把时间因素明确纳入操作之中：这对编程任务并非必需，对软件工程任务却至关重要。大多数 VCS 还允许为映射增加一个输入，也就是分支名，从而支持并行的映射关系：

```txt
VCS(filename, time, branch) => file contents
```

In the default usage, that branch input will have a commonly understood default: we call that “head,” “default,” or “trunk” to denote main branch.

通常，分支这一输入有一个大家公认的默认值，称为“head”“default”或“trunk”，表示主分支。

The (minor) remaining hesitation toward consistent use of version control comes almost directly from conflating programming and software engineering—we teach programming, we train programmers, we interview for jobs based on programming problems and techniques. It’s perfectly reasonable for a new hire, even at a place like Google, to have little or no experience with code that is worked on by more than one person or for more than a couple weeks. Given that experience and understanding of the problem, version control seems like an alien solution. Version control is solving a problem that our new hire hasn’t necessarily experienced: an “undo,” not for a single file but for an entire project, adding a lot of complexity for sometimes nonobvious benefits.

人们对持续使用版本控制仍有的那一点迟疑，几乎都直接源于把编程与软件工程混为一谈：我们教的是编程，培养的是程序员，招聘面试也围绕编程问题和技巧展开。即使在谷歌，新员工几乎没有接触过多人共同维护、或持续开发超过几周的代码，也完全可以理解。以这样的经验和对问题的认识来看，版本控制难免显得陌生。它解决的问题，新员工未必经历过：不是撤销单个文件的修改，而是对整个项目执行“撤销”。为此引入的复杂性不少，好处却未必一眼可见。

In some software groups, the same result plays out when management views the job of the techies as “software development” (sit down and write code) rather than “software engineering” (produce code, keep it working and useful for some extended period). With a mental model of programming as the primary task and little understanding of the interplay between code and the passage of time, it’s easy to see something described as “go back to a previous version to undo a mistake” as a weird, high- overhead luxury.

一些软件团队也会遇到同样的情况：管理层把技术人员的工作看作“软件开发”，也就是坐下来写代码，而不是“软件工程”，也就是写出代码，并让它在较长时间内持续正常运行、提供价值。如果认为主要任务就是编程，又不太理解代码与时间推移之间的关系，就很容易把“回到先前的版本来撤销错误”看成一种奇怪而昂贵的奢侈做法。

In addition to allowing separate storage and reference to versions over time, version control helps us bridge the gap between single-developer and multideveloper processes. In practical terms, this is why version control is so critical to software engineering, because it allows us to scale up teams and organizations, even though we use it only infrequently as an “undo” button. Development is inherently a branch-and- merge process, both when coordinating between multiple developers or a single developer at different points in time. A VCS removes the question of “which is more recent?” Use of modern version control automates error-prone operations like tracking which set of changes have been applied. Version control is how we coordinate between multiple developers and/or multiple points in time.

版本控制不仅能分别存储和引用不同时期的版本，还能帮助我们从单人开发过渡到多人协作。这正是它对软件工程至关重要的实际原因：即使很少把它当作“撤销”按钮，它仍能支持团队和组织扩大规模。**开发本质上是一个创建分支再合并的过程，无论要协调的是多个开发者，还是同一开发者在不同时间所做的工作。**VCS 让我们不必再争论“哪个版本更新”。现代版本控制可以自动完成跟踪已应用变更等容易出错的操作，帮助我们协调多人之间、不同时点之间，或兼具这两个维度的工作。

Because VCS has become so thoroughly embedded in the process of software engineering, even legal and regulatory practices have caught up. VCS allows a formal record of every change to every line of code, which is increasingly necessary for satisfying audit requirements. When mixing between in-house development and appropriate use of third-party sources, VCS helps track provenance and origination for every line of code.

VCS 已经深深融入软件工程流程，法律和监管实践也随之调整。它能正式记录每一行代码的每一次变更，而满足审计要求也越来越离不开这样的记录。在结合内部开发与适当使用第三方源代码时，VCS 还能帮助追踪每行代码的来源和流转历史。

In addition to the technical and regulatory aspects of tracking source over time and handling sync/branch/merge operations, version control triggers some nontechnical changes in behavior. The ritual of committing to version control and producing a commit log is a trigger for a moment of reflection: what have you accomplished since your last commit? Is the source in a state that you’re happy with? The moment of introspection associated with committing, writing up a summary, and marking a task complete might have value on its own for many people. The start of the commit process is a perfect time to run through a checklist, run static analyses (see Chapter 20), check test coverage, run tests and dynamic analysis, and so on.

除了在技术和监管层面支持源代码历史跟踪，以及同步、分支和合并操作，版本控制还会带来一些非技术性的行为变化。提交代码并撰写提交日志，是一个促使人停下来反思的过程：上次提交之后完成了什么？代码现在的状态是否令人满意？对许多人来说，提交、撰写摘要和标记任务完成时的这片刻反思，本身就可能有价值。开始提交时，也正适合逐项核对检查清单、运行静态分析（见第20章）、检查测试覆盖率，以及运行测试和动态分析等。

Like any process, version control comes with some overhead: someone must configure and manage your version control system, and individual developers must use it. But make no mistake about it: these can almost always be pretty cheap. Anecdotally, most experienced software engineers will instinctively use version control for any project that lasts more than a day or two, even for a single-developer project. The consistency of that result argues that the trade-off in terms of value (including risk reduction) versus overhead must be a pretty easy one. But we’ve promised to acknowledge that context matters and to encourage engineering leaders to think for themselves. It is always worth considering alternatives, even on something as fundamental as version control.

与任何流程一样，版本控制也有开销：需要有人配置和管理系统，每位开发者也都要使用它。不过要明确，这些成本几乎总是很低。从经验来看，大多数资深软件工程师都会本能地为持续超过一两天的项目使用版本控制，即使项目只有自己一个开发者。大家如此一致的选择表明，要在其价值（包括降低风险）和开销之间作出取舍，并不困难。但我们也承诺过，要承认具体情境的重要性，并鼓励工程负责人独立思考。即使是版本控制这样基础的做法，也值得考虑替代方案。

In truth, it’s difficult to envision any task that can be considered modern software engineering that doesn’t immediately adopt a VCS. Given that you understand the value and need for version control, you are likely now asking what type of version control you need.

事实上，很难想象有什么称得上现代软件工程的任务，不会一开始就采用 VCS。理解了版本控制的价值和必要性后，你大概会问：应该使用哪一类版本控制系统？

> [^3]: Indeed, I’ve given several public talks that use “adoption of version control” as the canonical example of how the norms of software engineering can and do evolve over time. In my experience, in the 1990s, version control was pretty well understood as a best practice but not universally followed. In the early 2000s, it was still common to encounter professional groups that didn’t use it. Today, the use of tools like Git seems ubiquitous even among college students working on personal projects. Some of this rise in adoption is likely due to better user experience in the tools (nobody wants to go back to RCS), but the role of experience and changing norms is significant.
>
> 3 我在几次公开演讲中，都把“采用版本控制”作为典型例子，说明软件工程规范不仅能够、而且确实会随时间演变。根据我的经验，20世纪90年代，大家已经普遍知道版本控制是最佳实践，却没有普遍采用。到了21世纪初，不使用版本控制的专业团队仍很常见。如今，即使是做个人项目的大学生，似乎也普遍使用 Git 之类的工具。采用率提高，可能部分归功于工具用户体验的改善，毕竟没人想回到 RCS；但经验积累和规范变化也发挥了重要作用。

### Centralized VCS Versus Distributed VCS  集中式 VCS 与分布式 VCS

At the most simplistic level, all modern VCSs are equivalent to one another: so long as your system has a notion of atomically committing changes to a batch of files, everything else is just UI. You could build the same general semantics (not workflow) of any modern VCS out of another one and a pile of simple shell scripts. Thus, arguing about which VCS is “better” is primarily a matter of user experience—the core functionality is the same, the differences come in user experience, naming, edge-case features, and performance. Choosing a VCS is like choosing a filesystem format: when choosing among a modern-enough format, the differences are fairly minor, and the more important question by far is the content you fill that system with and the way you *use* it. However, major architectural differences in VCSs can make configuration, policy, and scaling decisions easier or more difficult, so it’s important to be aware of the big architectural differences, chiefly the decision between centralized or decentralized.

从最简单的层面看，所有现代 VCS 都是等价的：只要系统支持以原子方式提交一批文件的变更，其余差别就只是用户界面（UI）。借助另一种 VCS 和一组简单的 shell 脚本，就可以实现任何现代 VCS 的基本语义，但不一定能复现其工作流。因此，争论哪种 VCS“更好”，主要是在讨论用户体验：核心功能相同，区别在于用户体验、命名、边界情况的功能和性能。选择 VCS 就像选择文件系统格式：只要候选格式足够现代，差别通常不大，远为重要的是存入什么内容，以及如何使用它。不过，VCS 的主要架构差异确实会影响配置、策略和规模扩展方面的决策难度，因此需要了解这些差异，尤其是集中式与去中心化之间的选择。

#### Centralized VCS  集中式 VCS

In centralized VCS implementations, the model is one of a single central repository (likely stored on some shared compute resource for your organization). Although a developer can have files checked out and accessible on their local workstation, operations that interact on the version control status of those files need to be communicated to the central server (adding files, syncing, updating existing files, etc.). Any code that is committed by a developer is committed into that central repository. The first VCS implementations were all centralized VCSs.

集中式 VCS 采用单一中央代码仓库的模型，仓库通常存放在组织的某种共享计算资源上。开发者可以把文件检出到本地工作站并访问它们，但涉及文件版本控制状态的操作，例如添加文件、同步和更新现有文件，都需要与中央服务器通信。开发者提交的所有代码都会进入中央仓库。最早的 VCS 实现都是集中式的。

Going back to the 1970s and early 1980s, we see that the earliest of these VCSs, such as RCS, focused on locking and preventing multiple simultaneous edits. You could copy the contents of a repository, but if you wanted to edit a file, you might need to acquire a lock, enforced by the VCS, to ensure that only you are making edits. When you’ve completed an edit, you release the lock. The model worked fine when any given change was a quick thing, or if there was rarely more than one person that wanted the lock for a file at any given time. Small edits like tweaking config files worked OK, as did working on a small team that either kept disjointed working hours or that rarely worked on overlapping files for extended periods. This sort of simplistic locking has inherent problems with scale: it can work fine for a few people, but has the potential to fall apart with larger groups if any of those locks become contended.[^4]

回到20世纪70年代和80年代初，RCS 等早期 VCS 主要依靠锁定，防止多人同时编辑。你可以复制仓库内容，但编辑某个文件前，可能必须先取得由 VCS 强制执行的锁，以确保只有你能修改它；编辑完成后再释放锁。如果每次变更都能很快完成，或者很少有多人同时需要同一个文件的锁，这种模型就运行良好。微调配置文件之类的小修改没有问题；小团队如果工作时间互不重叠，或者很少长时间修改相同文件，也能顺利使用。这种简单的锁定机制有固有的规模限制：几个人使用时可以运行良好，但团队变大后，一旦发生锁竞争，就可能难以为继。

As a response to this scaling problem, the VCSs that were popular through the 90s and early 2000s operated at a higher level. These more modern centralized VCSs avoid the exclusive locking but track which changes you’ve synced, requiring your edit to be based on the most-current version of every file in your commit. CVS wrapped and refined RCS by (mostly) operating on batches of files at a time and allowing multiple developers to check out a file at the same time: so long as your base version contained all of the changes in the repository, you’re allowed to commit. Subversion advanced further by providing true atomicity for commits, version tracking, and better tracking for unusual operations (renames, use of symbolic links, etc.). The centralized repository/checked-out client model continues today within Subversion as well as most commercial VCSs.

为应对这一规模问题，20世纪90年代至21世纪初流行的 VCS 转向了更高层次的处理方式。这些较新的集中式 VCS 不再使用排他锁，而是跟踪你同步过哪些变更，并要求本次提交中的每个文件都基于其最新版本修改。CVS 在 RCS 外增加封装并加以改进，主要以一批文件为单位操作，允许多个开发者同时检出同一个文件：只要你的基础版本包含仓库中已有的全部变更，就可以提交。Subversion 又向前迈了一步，提供真正的提交原子性、版本跟踪，以及对重命名、符号链接等不常见操作的更完善跟踪。中央仓库配合检出客户端的模式，至今仍用于 Subversion 和大多数商业 VCS。

> [^4]: Anecdote: To illustrate this, I looked for information on what pending/unsubmitted edits Googlers had outstanding for a semipopular file in my most recent project. At the time of this writing, 27 changes are pending, 12 from people on my team, 5 from people on related teams, and 10 from engineers I’ve never met. This is basically working as expected. Technical systems or policies that require out-of-band coordination certainly don’t scale to 24/7 software engineering in distributed locations.
>
> 4   举个例子：为说明这一点，我查看了最近一个项目中某个使用较多的文件，看看谷歌工程师还有哪些待提交的修改。撰写本章时，共有27项变更尚未提交，其中12项来自我的团队，5项来自相关团队，10项来自我从未见过的工程师。这基本上就是预期的工作状态。需要在系统之外另行协调的技术系统或策略，显然无法支持分散各地、全天候开展的软件工程工作。

#### Distributed VCS 分布式 VCS

Starting in the mid-2000s, many popular VCSs followed the Distributed Version Control System (DVCS) paradigm, seen in systems like Git and Mercurial. The primary conceptual difference between DVCS and more traditional centralized VCS (Subversion, CVS) is the question: “Where can you commit?” or perhaps, “Which copies of these files count as a repository?”

从21世纪第一个十年的中期开始，许多流行的版本控制系统（VCS）采用了分布式版本控制系统（DVCS）范式，Git 和 Mercurial 就是例子。DVCS 与 Subversion、CVS 等传统集中式 VCS 的主要概念区别，在于如何回答“可以在哪里提交”，或者说，“这些文件的哪些副本算作代码仓库”。

A DVCS world does not enforce the constraint of a central repository: if you have a copy (clone, fork) of the repository, you have a repository that you can commit to as well as all of the metadata necessary to query for information about things like revision history. A standard workflow is to clone some existing repository, make some edits, commit them locally, and then push some set of commits to another repository, which may or may not be the original source of the clone. Any notion of centrality is purely conceptual, a matter of policy, not fundamental to the technology or the underlying protocols.

DVCS 不强制要求存在中央代码仓库：只要拥有仓库的副本，无论是克隆还是分叉，就拥有一个可以提交的仓库，以及查询修订历史等信息所需的全部元数据。典型工作流是克隆现有仓库，修改后在本地提交，再把一组提交推送到另一个仓库；后者可以是最初克隆的来源，也可以不是。所谓“中心”，纯粹是概念上的约定和策略选择，并非技术或底层协议的固有要求。

The DVCS model allows for better offline operation and collaboration without inherently declaring one particular repository to be the source of truth. One repository isn’t necessary “ahead” or “behind” because changes aren’t inherently projected into a linear timeline. However, considering common *usage*, both the centralized and DVCS models are largely interchangeable: whereas a centralized VCS provides a clearly defined central repository through technology, most DVCS ecosystems define a central repository for a project as a matter of policy. That is, most DVCS projects are built around one conceptual source of truth (a particular repository on GitHub, for instance). DVCS models tend to assume a more distributed use case and have found particularly strong adoption in the open source world.

DVCS 模型更便于离线操作和协作，也不要求从一开始就指定某个仓库为权威来源。仓库之间未必能简单判定谁“领先”、谁“落后”，因为变更并不天然排列在线性的时间轴上。不过，从常见用法来看，集中式与 DVCS 模型在很大程度上可以互换：集中式 VCS 通过技术确定中央仓库，而大多数 DVCS 生态系统通过策略为项目指定中央仓库。也就是说，大多数 DVCS 项目仍围绕一个概念上的权威来源运作，例如 GitHub 上的某个仓库。DVCS 通常面向更分散的使用场景，在开源领域尤其普及。

Generally speaking, the dominant source control system today is Git, which implements DVCS.[^5] When in doubt, use that—there’s some value in doing what everyone else does. If your use cases are expected to be unusual, gather some data and evaluate the trade-offs.

总体而言，如今占主导地位的源代码版本控制系统是 Git，它采用 DVCS 模型。拿不准时，就用它：采用大家普遍使用的工具，本身就有价值。如果预计自己的使用场景比较特殊，再收集数据、评估取舍。

Google has a complex relationship with DVCS: our main repository is based on a (massive) custom in-house centralized VCS. There are periodic attempts to integrate more standard external options and to match the workflow that our engineers (especially Nooglers) have come to expect from external development. Unfortunately, those attempts to move toward more common tools like Git have been stymied by the sheer size of the codebase and userbase, to say nothing of Hyrum’s Law effects tying us to a particular VCS and interface for that VCS.[^6] This is perhaps not surprising: most existing tools don’t scale well with 50,000 engineers and tens of millions of commits.[^7] The DVCS model, which often (but not always) includes transmission of history and metadata, requires a lot of data to spin up a repository to work out of.

谷歌与 DVCS 的关系比较复杂：我们的主仓库建立在内部定制的集中式 VCS 之上，规模非常庞大。我们不时尝试接入更通用的外部工具，让工作流符合工程师，尤其是 Nooglers 在外部开发中形成的习惯和预期。遗憾的是，转向 Git 等通用工具的尝试，一直受到庞大代码库和用户规模的阻碍；海勒姆定律带来的影响，又让我们难以摆脱特定 VCS 及其接口。这或许并不意外：大多数现有工具都难以扩展到支持50,000名工程师和数千万次提交的规模。DVCS 通常需要传输历史记录和元数据，虽然也有例外，因此要准备一个可供开发使用的仓库，就需要大量数据。

In our workflow, centrality and in-the-cloud storage for the codebase seem to be critical to scaling. The DVCS model is built around the idea of downloading the entire codebase and having access to it locally. In practice, over time and as your organization scales up, any given developer is going to operate on a relatively smaller percentage of the files in a repository, and a small fraction of the versions of those files. As we grow (in file count and engineer count), that transmission becomes almost entirely waste. The only need for locality for most files occurs when building, but distributed (and reproducible) build systems seem to scale better for that task as well (see Chapter 18).

在我们的工作流中，集中管理代码库并将其存储在云端，似乎是实现规模扩展的关键。DVCS 模型围绕下载整个代码库、在本地访问代码这一思路建立。但实际上，随着时间推移和组织扩大，每位开发者处理的文件占仓库全部文件的比例会越来越小，所需版本也只占这些文件全部版本的一小部分。文件和工程师的数量越多，传输的数据就越接近纯粹的浪费。大多数文件只有在构建时才需要放在本地，而分布式且可复现的构建系统，似乎也能更好地支持这项工作的规模扩展（见第18章）。

> [^5]: Stack Overflow Developer Survey Results, 2018.
>
> 5 Stack Overflow 开发者调查结果，2018年。
>
> [^6]: Monotonically increasing version numbers, rather than commit hashes, are particularly troublesome. Many systems and scripts have grown up in the Google developer ecosystem that assume that the numeric ordering of commits is the same as the temporal order—undoing those hidden dependencies is difficult.
>
> 6 使用单调递增的版本号而非提交哈希，尤其让迁移棘手。谷歌开发者生态系统中的许多系统和脚本，都假定提交编号的大小顺序与提交时间顺序一致。要消除这些隐含依赖并不容易。
>
> [^7]: For that matter, as of the publication of the Monorepo paper, the repository itself had something like 86 TB of data and metadata, ignoring release branches. Fitting that onto a developer workstation directly would be… challenging.
>
> 7 而且，在 Monorepo 论文发表时，即使不计发布分支，仓库也已有约86 TB 的数据和元数据。要把这些内容直接放进开发者的工作站，恐怕……颇有挑战。

### Source of Truth 权威来源

Centralized VCSs (Subversion, CVS, Perforce, etc.) bake the source-of-truth notion into the very design of the system: whatever is most recently committed at trunk is the current version. When a developer goes to check out the project, by default that trunk version is what they will be presented with. Your changes are “done” when they have been recommitted on top of that version.

集中式 VCS（Subversion、CVS、Perforce 等）把权威来源直接纳入系统设计：主干上最近提交的内容就是当前版本。开发者检出项目时，默认得到的就是这个主干版本。修改在该版本之上重新提交后，才算“完成”。

However, unlike centralized VCS, there is no *inherent* notion of which copy of the distributed repository is the single source of truth in DVCS systems. In theory, it’s possible to pass around commit tags and PRs with no centralization or coordination, allowing disparate branches of development to propagate unchecked, and thus risking a conceptual return to the world of *Presentation v5 - final - redlines - Josh’s version* *v2*. Because of this, DVCS requires more explicit policy and norms than a centralized VCS does.

然而，与集中式 VCS 不同，DVCS 并不*固有地规定*分布式仓库的哪个副本是唯一权威来源。理论上，人们可以不经集中管理或协调，就相互传递提交标签和 PR，让各条开发分支不受约束地传播。这样就有可能在概念上重回 *Presentation v5 - final - redlines - Josh's version v2* 的世界。因此，DVCS 比集中式 VCS 更需要明确的策略和规范。

Well-managed projects using DVCS declare one specific branch in one specific repository to be the source of truth and thus avoid the more chaotic possibilities. We see this in practice with the spread of hosted DVCS solutions like GitHub or GitLab— users can clone and fork the repository for a project, but there is still a single primary repository: things are “done” when they are in the trunk branch on that repository.

管理良好的 DVCS 项目，会明确指定某个仓库中的某个分支作为权威来源，从而避免混乱。GitHub、GitLab 等托管 DVCS 平台的普及，正体现了这种做法：用户可以克隆、分叉项目仓库，但仍只有一个主仓库；工作进入该仓库的主干分支，才算“完成”。

It isn’t an accident that centralization and Source of Truth has crept back into the usage even in a DVCS world. To help illustrate just how important this Source of Truth idea is, let’s imagine what happens when we don’t have a clear source of truth.

即使采用 DVCS，集中管理和权威来源的概念也重新回到了实际使用中，这并非偶然。为了说明权威来源有多重要，不妨设想一下：没有明确的权威来源，会发生什么？

#### Scenario: no clear source of truth  场景：没有明确的权威来源

Imagine that your team adheres to the DVCS philosophy enough to avoid defining a specific branch+repository as the ultimate source of truth.

设想你的团队十分坚持 DVCS 理念，以至于不愿将某个仓库中的特定分支指定为最终的权威来源。

In some respects, this is reminiscent of the *Presentation v5 - final - redlines - Josh’s version v2* model—after you pull from a teammate’s repository, it isn’t necessarily clear which changes are present and which are not. In some respects, it’s better than that because the DVCS model tracks the merging of individual patches at a much finer granularity than those ad hoc naming schemes, but there’s a difference between the DVCS knowing *which* changes are incorporated and every engineer being sure they have *all* the past/relevant changes represented.

这在某种程度上又回到了 *Presentation v5 - final - redlines - Josh's version v2* 的模式：从队友的仓库拉取代码后，你未必清楚其中包含哪些变更，又缺少哪些。当然，情况也有所改善，因为 DVCS 跟踪单个补丁合并情况的粒度，比这种临时命名方案细得多。不过，DVCS 知道合入了哪些变更，与每位工程师都确信自己拥有过去全部相关变更，并不是一回事。

Consider what it takes to ensure that a release build includes all of the features that have been developed by each developer for the past few weeks. What (noncentralized, scalable) mechanisms are there to do that? Can we design policies that are fundamentally better than having everyone sign off? Are there any that require only sublinear human effort as the team scales up? Is that going to continue working as the number of developers on the team scales up? As far as we can see: probably not. Without a central Source of Truth, someone is going to keep a list of which features are potentially ready to be included in the next release. Eventually that bookkeeping is reproducing the model of having a centralized Source of Truth.

想一想，要确保发布构建包含每位开发者在过去几周完成的全部功能，需要做些什么？有没有去中心化、又能随规模扩展的机制？能否设计出比逐人确认从根本上更好的策略？有没有办法让所需人力随团队规模仅呈次线性增长？开发者继续增加后，这种办法还能奏效吗？据我们判断，恐怕没有。如果没有集中的权威来源，就会有人维护一份清单，记录哪些功能可能已经可以纳入下一次发布。到头来，这种记录方式又重现了集中式权威来源的模型。

Further imagine: when a new developer joins the team, where do they get a fresh, known-good copy of the code?

再想一步：新开发者加入团队时，应该到哪里获取一份最新且已知可用的代码副本？

DVCS enables a lot of great workflows and interesting usage models. But if you’re concerned with finding a system that requires sublinear human effort to manage as the team grows, it’s pretty important to have one repository (and one branch) actually defined to be the ultimate source of truth.

DVCS 支持许多出色的工作流和有趣的使用模式。但如果希望随着团队扩大，系统管理所需的人力仅呈次线性增长，那么，明确指定一个仓库中的一个分支作为最终的权威来源，就十分重要。

There is some relativity in that Source of Truth. That is, for a given project, that Source of Truth might be different for a different organization. This caveat is important: it’s reasonable for engineers at Google or RedHat to have different Sources of Truth for Linux Kernel patches, still different than Linus (the Linux Kernel maintainer) himself would. DVCS works fine when organizations and their Sources of Truth are hierarchical (and invisible to those outside the organization)—that is perhaps the most practically useful effect of the DVCS model. A RedHat engineer can commit to the local Source of Truth repository, and changes can be pushed from there upstream periodically, while Linus has a completely different notion of what is the Source of Truth. So long as there is no choice or uncertainty as to where a change should be pushed, we can avoid a large class of chaotic scaling problems in the DVCS model.

权威来源也有相对性：对于同一个项目，不同组织可以认定不同的权威来源。这个限定很重要。谷歌和 RedHat 的工程师可以为 Linux 内核补丁采用不同的权威来源，也可以与内核维护者 Linus 本人采用的来源不同。当组织及其权威来源形成层级，而且内部细节对组织外部不可见时，DVCS 就能很好地运作。这或许是 DVCS 模型最有实际价值的作用。RedHat 工程师可以向本组织的权威仓库提交，再由该仓库定期向上游推送变更；Linus 则可以采用完全不同的权威来源。只要变更应推送到哪里是唯一且明确的，就能避免 DVCS 模型中一大类会随规模增长而加剧的混乱。

In all of this thinking, we’re assigning special significance to the trunk branch. But of course, “trunk” in your VCS is only the technology default, and an organization can choose different policies on top of that. Perhaps the default branch has been abandoned and all work actually happens on some custom development branch—other than needing to provide a branch name in more operations, there’s nothing inherently broken in that approach; it’s just nonstandard. There’s an (oft-unspoken) truth when discussing version control: the technology is only one part of it for any given organization; there is almost always an equal amount of policy and usage convention on top of that.

上述讨论都赋予了主干分支特殊地位。不过，VCS 中的“主干”只是技术上的默认设置，组织可以在其上采用不同策略。也许默认分支早已弃用，所有工作实际都在某个自定义开发分支上进行。除了更多操作需要明确填写分支名，这种做法本身没有问题，只是不常见。讨论版本控制时，有一个往往没有明说的事实：对任何组织而言，技术都只是其中一部分，建立在技术之上的策略和使用惯例，几乎总有同等重要的分量。

No topic in version control has more policy and convention than the discussion of how to use and manage branches. We look at branch management in more detail in the next section.

在版本控制的各种议题中，分支的使用和管理最离不开策略与惯例。下一节将详细讨论分支管理。

### Version Control Versus Dependency Management 版本控制与依赖管理

There’s a lot of conceptual similarity between discussions of version control policies and dependency management (see [Chapter 21](#_bookmark1845)). The differences are primarily in two forms: VCS policies are largely about how you manage your own code, and are usually much finer grained. Dependency management is more challenging because we primarily focus on projects managed and controlled by other organizations, at a higher granularity, and these situations mean that you don’t have perfect control. We’ll discuss a lot more of these high-level issues later in the book.

版本控制策略与依赖管理在概念上有许多相似之处（见第21章），主要区别有两点：VCS 策略关注如何管理自己的代码，粒度通常也细得多。依赖管理则主要涉及由其他组织管理和控制的项目，粒度更粗，而且你无法完全掌控，因此更具挑战性。本书后面会进一步讨论这些较高层次的问题。

## Branch Management  分支管理

Being able to track different revisions in version control opens up a variety of different approaches for how to manage those different versions. Collectively, these different approaches fall under the term *branch management*, in contrast to a single “trunk.”

版本控制能够跟踪不同修订版，因此也就有了多种管理这些版本的方法。与只使用一条“主干”相对，这些方法统称为*分支管理*。

### Work in Progress Is Akin to a Branch  正在进行的工作类似于一个分支

Any discussion that an organization has about branch management policies ought to at least acknowledge that every piece of work-in-progress in the organization is equivalent to a branch. This is more explicitly the case with a DVCS in which developers are more likely to make numerous local staging commits before pushing back to the upstream Source of Truth. This is still true of centralized VCSs: uncommitted local changes aren’t conceptually different than committed changes on a branch, other than potentially being more difficult to find and diff against. Some centralized systems even make this explicit. For example, when using Perforce, every change is given two revision numbers: one indicating the implicit branch point where the change was created, and one indicating where it was recommitted, as illustrated in [Figure 16-1](#_bookmark1418). Perforce users can query to see who has outstanding changes to a given file, inspect the pending changes in other users’ uncommitted changes, and more.

组织讨论分支管理策略时，至少应承认：组织内每一项尚在进行的工作，都相当于一个分支。DVCS 更明显地体现了这一点，因为开发者往往会先在本地作出多次阶段性提交，再推送回上游权威来源。集中式 VCS 也是如此：未提交的本地变更，与已经提交到分支上的变更，在概念上没有区别，只是可能更难找到并进行差异比较。有些集中式系统甚至直接体现了这一点。例如，Perforce 会为每项变更赋予两个修订号：一个表示创建变更时的隐含分支点，另一个表示重新提交变更的位置，如图16-1所示。Perforce 用户可以查询谁对某个文件还有待提交变更，也可以查看其他用户尚未提交的具体修改等。

![Figure 16-1. Two revision numbers in Perforce](./images/Figure%2016-1.png)

*Figure 16-1. Two revision numbers in Perforce*  *图 16-1. Perforce 中的两个修订号*

This “uncommitted work is akin to a branch” idea is particularly relevant when thinking about refactoring tasks. Imagine a developer being told, “Go rename Widget to OldWidget.” Depending on an organization’s branch management policies and understanding, what counts as a branch, and which branches matter, this could have several interpretations:

- Rename Widget on the trunk branch in the Source of Truth repository
- Rename Widget on all branches in the Source of Truth repository
- Rename Widget on all branches in the Source of Truth repository, and find all devs with outstanding changes to files that reference Widget

考虑重构任务时，“未提交的工作类似于分支”这一认识尤其重要。假设一位开发者接到任务：“把 Widget 重命名为 OldWidget。”组织采用什么分支管理策略、如何认定分支、哪些分支需要关注，都会影响这项任务的含义。它可能有以下几种解释：

- 在权威仓库的主干分支上重命名 Widget
- 在权威仓库的所有分支上重命名 Widget
- 在权威仓库的所有分支上重命名 Widget，并找出所有正在修改引用 Widget 的文件、且尚未提交变更的开发者。

If we were to speculate, attempting to support that “rename this everywhere, even in outstanding changes” use case is part of why commercial centralized VCSs tend to track things like “which engineers have this file open for editing?” (We don’t think this is a scalable way to *perform* a refactoring task, but we understand the point of view.)

我们推测，商业集中式 VCS 往往会跟踪“哪些工程师正在编辑这个文件”，部分原因就是为了支持“在所有地方重命名，连待提交变更也不例外”这样的需求。（我们不认为这种重构方式有利于规模扩展，但理解其中的考虑。）

### Dev Branches  开发分支

In the age before consistent unit testing (see Chapter 11), when the introduction of any given change had a high risk of regressing functionality elsewhere in the system, it made sense to treat *trunk* specially. “We don’t commit to trunk,” your Tech Lead might say, “until new changes have gone through a full round of testing. Our team uses feature-specific development branches instead.”

在尚未持续采用单元测试的年代（见第11章），任何变更都很可能导致系统其他部分的功能出现回归缺陷，因此特别对待 *trunk*（主干）是合理的。技术负责人可能会说：“新变更通过一轮完整测试之前，我们不会向主干提交。我们的团队会先使用针对具体功能的开发分支。”

A development branch (usually “dev branch”) is a halfway point between “this is done but not committed” and “this is what new work is based on.” The problem that these are attempting to solve (instability of the product) is a legitimate one—but one that we have found to be solved far better with more extensive use of tests, Continuous Integration (CI) (see Chapter 23), and quality enforcement practices like thorough code review.

开发分支（通常称为“dev branch”）是介于“工作已完成但尚未提交”和“可供新工作作为基础”之间的中间状态。它试图解决的产品不稳定问题确实存在，但我们发现，更广泛地使用测试、持续集成（CI，见第23章），再配合充分的代码审查等质量保障措施，效果要好得多。

We believe that a version control policy that makes extensive use of dev branches as a means toward product stability is inherently misguided. The same set of commits are going to be merged to trunk eventually. Small merges are easier than big ones. Merges done by the engineer who authored those changes are easier than batching unrelated changes and merging later (which will happen eventually if a team is sharing a dev branch). If presubmit testing on the merge reveals any new problems, the same argument applies: it’s easier to determine whose changes are responsible for a regression if there is only one engineer involved. Merging a large dev branch implies that more changes are happening in that test run, making failures more difficult to isolate. Triaging and root-causing the problem is difficult; fixing it is even worse.

我们认为，依靠大量开发分支来保证产品稳定的版本控制策略，从根本上就走错了方向。同一组提交最终还是要合入主干。小规模合并比大规模合并容易；由变更作者亲自合并，也比把互不相关的变更积攒起来日后统一合并容易，而团队共享开发分支最终就会出现后一种情况。如果合并的提交前测试发现新问题，道理同样适用：只涉及一位工程师时，更容易确定是谁的变更导致了回归缺陷。合并大型开发分支，意味着一次测试要面对更多变更，更难定位失败原因。问题分诊和根因分析已经很难，修复就更难了。

Beyond the lack of expertise and inherent problems in merging a single branch, there are significant scaling risks when relying on dev branches. This is a very common productivity drain for a software organization. When there are multiple branches being developed in isolation for long periods, coordinating merge operations becomes significantly more expensive (and possibly riskier) than they would be with trunk-based development.

除了合并单个分支时可能缺少必要知识、以及合并本身的固有问题，依赖开发分支还会带来显著的规模扩展风险。这是软件组织中很常见的生产力损耗。多个分支长期各自独立开发时，协调合并的成本会远高于主干开发，风险也可能更大。

#### How did we become addicted to dev branches?  我们是如何沉迷于开发分支的？

It’s easy to see how organizations fall into this trap: they see, “Merging this long-lived development branch reduced stability” and conclude, “Branch merges are risky.” Rather than solve that with “Better testing” and “Don’t use branch-based development strategies,” they focus on slowing down and coordinating the symptom: the branch merges. Teams begin developing new branches based on other in-flight branches. Teams working on a long-lived dev branch might or might not regularly have that branch synched with the main development branch. As the organization scales up, the number of development branches grows as well, and the more effort is placed on coordinating that branch merge strategy. Increasing effort is thrown at coordination of branch merges—a task that inherently doesn’t scale. Some unlucky engineer becomes the Build Master/Merge Coordinator/Content Management Engineer, focused on acting as the single point coordinator to merge all the disparate branches in the organization. Regularly scheduled meetings attempt to ensure that the organization has “worked out the merge strategy for the week.”[^8] The teams that aren’t chosen to merge often need to re-sync and retest after each of these large merges.

组织如何陷入这个困境并不难理解：看到“合并长期存在的开发分支降低了稳定性”，便得出“分支合并有风险”的结论。他们没有通过改进测试、放弃基于分支的开发策略来解决问题，而是着眼于放慢并协调分支合并这个表面症状。团队开始基于其他尚未完成的分支创建新分支。长期在某个开发分支上工作的团队，有的会定期与主开发分支同步，有的不会。组织越大，开发分支越多，协调合并策略所花的精力也越多。越来越多的投入流向分支合并协调，而这项工作本身就难以随规模扩展。某个不走运的工程师成为构建负责人、合并协调员或内容管理工程师，充当唯一的协调者，负责合并组织内各处分支。大家定期开会，确保“本周的合并策略已经确定”。那些没轮到合并的团队，往往需要在每次大规模合并后重新同步和测试。

All of that effort in merging and retesting is *pure overhead*. The alternative requires a different paradigm: trunk-based development, rely heavily on testing and CI, keep the build green, and disable incomplete/untested features at runtime. Everyone is responsible to sync to trunk and commit; no “merge strategy” meetings, no large/expensive merges. And, no heated discussions about which version of a library should be used—there can be only one. There must be a single Source of Truth. In the end, there will be a single revision used for a release: narrowing down to a single source of truth is just the “shift left” approach for identifying what is and is not being included.

这些合并和重复测试的工作，都是*纯粹的开销*。另一条路需要采用不同范式：主干开发，充分依靠测试和 CI，始终保持构建通过，并在运行时禁用尚未完成或未经测试的功能。每个人都负责同步主干并提交，不再需要“合并策略”会议，也没有庞大而昂贵的合并。大家也不必为使用库的哪个版本争论不休，因为只能有一个版本。必须有唯一权威来源。最终，发布时总要选定一个修订版；提前统一权威来源，只不过是把“包含什么、不包含什么”的判断左移了。

> [^8]: Recent informal Twitter polling suggests about 25% of software engineers have been subjected to “regularly scheduled” merge strategy meetings.
>
> 8   最近一次非正式推特调查显示，约25%的软件工程师经历过“定期召开”的合并策略会议。

### Release Branches  发布分支

If the period between releases (or the release lifetime) for a product is longer than a few hours, it may be sensible to create a release branch that represents the exact code that went into the release build for your product. If any critical flaws are discovered between the actual release of that product into the wild and the next release cycle, fixes can be cherry-picked (a minimal, targeted merge) from trunk to your release branch.

如果产品的发布间隔，或某个发布版本的生命周期，超过几个小时，那么创建一个发布分支、准确记录该版本构建所用的代码，可能是合理的。产品正式发布后，到下一轮发布之前，如果发现严重缺陷，就可以从主干选择性合并修复到发布分支，也就是只做最小范围、有针对性的合并。

By comparison to dev branches, release branches are generally benign: it isn’t the technology of branches that is troublesome, it’s the usage. The primary difference between a dev branch and a release branch is the expected end state: a dev branch is expected to merge back to trunk, and could even be further branched by another team. A release branch is expected to be abandoned eventually.

与开发分支相比，发布分支通常无害：问题不在分支技术本身，而在使用方式。二者的主要区别是预期归宿不同。开发分支最终要合回主干，期间甚至可能被另一个团队用来创建新分支；发布分支最终则会弃用。

In the highest-functioning technical organizations that Google’s DevOps Research and Assessment (DORA) organization has identified, release branches are practically nonexistent. Organizations that have achieved Continuous Deployment (CD)—the ability to release from trunk many times a day—likely tend to skip release branches: it’s much easier to simply add the fix and redeploy. Thus, cherry-picks and branches seem like unnecessary overhead. Obviously, this is more applicable to organizations that deploy digitally (such as web services and apps) than those that push any form of tangible release to customers; it is generally valuable to know exactly what has been pushed to customers.

在谷歌 DevOps 研究与评估团队（DORA）识别出的表现最好的技术组织中，发布分支几乎不存在。能够持续部署（CD），也就是每天多次从主干发布的组织，往往倾向于省去发布分支：直接加入修复再重新部署，要容易得多。因此，选择性合并（cherry-picks）和发布分支似乎成了不必要的开销。显然，这更适合通过数字渠道部署网络服务、应用等产品的组织，而不太适合向客户交付实体产品的组织；对于后者，准确知道已经交付给客户的版本，通常很有价值。

That same DORA research also suggests a strong positive correlation between “trunk- based development,” “no long-lived dev branches,” and good technical outcomes. The underlying idea in both of those ideas seems clear: branches are a drag on productivity. In many cases we think complex branch and merge strategies are a perceived safety crutch—an attempt to keep trunk stable. As we see throughout this book, there are other ways to achieve that outcome.

同一项 DORA 研究还表明，“主干开发”“没有长期存在的开发分支”都与良好的技术成果有很强的正相关关系。这两种做法背后的思路很清楚：分支会拖累生产力。我们认为，很多时候，人们只是觉得复杂的分支和合并策略能提供安全保障，试图借此保持主干稳定。正如本书各处所示，实现这一目标还有其他方法。

## Version Control at Google  谷歌的版本控制

At Google, the vast majority of our source is managed in a single repository (monorepo) shared among roughly 50,000 engineers. Almost all projects that are owned by Google live there, except large open source projects like Chromium and Android. This includes public-facing products like Search, Gmail, our advertising products, our Google Cloud Platform offerings, as well as the internal infrastructure necessary to support and develop all of those products.

谷歌的绝大多数源代码，都在约50,000名工程师共享的单体代码仓库（monorepo）中管理。除 Chromium、Android 等大型开源项目外，几乎所有归谷歌所有的项目都在这里，包括搜索、Gmail、广告产品、谷歌云平台等面向公众的产品，以及开发和支持这些产品所需的内部基础设施。

We rely on an in-house-developed centralized VCS called Piper, built to run as a distributed microservice in our production environment. This has allowed us to use Google-standard storage, communication, and Compute as a Service technology to provide a globally available VCS storing more than 80 TB of content and metadata. The Piper monorepo is then simultaneously edited and committed to by many thousands of engineers every day. Between humans and semiautomated processes that make use of version control (or improve things checked into VCS), we’ll regularly handle 60,000 to 70,000 commits to the repository per work day. Binary artifacts are fairly common because the full repository isn’t transmitted and thus the normal costs of binary artifacts don’t really apply. Because of the focus on Google-scale from the earliest conception, operations in this VCS ecosystem are still cheap at human scale: it takes perhaps 15 seconds total to create a new client at trunk, add a file, and commit an (unreviewed) change to Piper. This low-latency interaction and well-understood/ well-designed scaling simplifies a lot of the developer experience.

我们使用内部开发的集中式 VCS，名为 Piper，它以分布式微服务的形式运行在生产环境中。因此，我们可以利用谷歌标准的存储、通信和计算即服务技术，提供全球可用的版本控制服务，存储超过80 TB 的内容和元数据。每天都有数千名工程师同时编辑 Piper 单体代码仓库并向其提交。工程师和使用版本控制、或改进仓库中内容的半自动化流程，通常每个工作日合计产生60,000到70,000次提交。二进制构件在仓库中相当常见，因为不需要传输整个仓库，存放二进制构件通常带来的成本也就不太适用。Piper 从设计之初就面向谷歌的规模，因此对单个开发者而言，操作成本仍然很低：从主干创建新客户端、添加文件，再向 Piper 提交一项未经审查的变更，总共可能只需15秒。低延迟的交互，加上经过充分理解和设计的扩展能力，大幅简化了开发者的使用体验。

By virtue of Piper being an in-house product, we have the ability to customize it and enforce whatever source control policies we choose. For instance, we have a notion of granular ownership in the monorepo: at every level of the file hierarchy, we can find OWNERS files that list the usernames of engineers that are allowed to approve commits within that subtree of the repository (in addition to the OWNERS that are listed at higher levels in the tree). In an environment with many repositories, this might have been achieved by having separate repositories with filesystem permissions enforcement controlling commit access or via a Git “commit hook” (action triggered at commit time) to do a separate permissions check. By controlling the VCS, we can make the concept of ownership and approval more explicit and enforced by the VCS during an attempted commit operation. The model is also flexible: ownership is just a text file, not tied to a physical separation of repositories, so it is trivial to update as the result of a team transfer or organization restructuring.

Piper 是内部产品，因此我们可以按需定制，并强制执行选定的源代码版本控制策略。例如，单体代码仓库支持细粒度的所有权：文件目录树的每一层都可以有 OWNERS 文件，列出有权批准该子树内提交的工程师用户名；上层目录 OWNERS 文件列出的人也拥有这一权限。在多仓库环境中，可以通过划分仓库并使用文件系统权限控制提交访问，或利用 Git 的“提交钩子”，也就是提交时触发的操作，单独检查权限。由于掌控 VCS，我们可以明确表达所有权与审批规则，并在提交时由 VCS 强制执行。这种模型也很灵活：所有权只记录在文本文件中，不受仓库物理划分的约束，因此团队移交或组织重组时很容易调整。

### One Version  单版本

The incredible scaling powers of Piper alone wouldn’t allow the sort of collaboration that we rely upon. As we said earlier: version control is also about policy. In addition to our VCS, one key feature of Google’s version control policy is what we’ve come to refer to as “One Version.” This extends the “Single Source of Truth” concept we looked at earlier—ensuring that a developer knows which branch and repository is their source of truth—to something like “For every dependency in our repository, there must be only one version of that dependency to choose.”[^9] For third-party packages, this means that there can be only a single version of that package checked into our repository, in the steady state.[^10] For internal packages, this means no forking without repackaging/renaming: it must be technologically safe to mix both the original and the fork into the same project with no special effort. This is a powerful feature for our ecosystem: there are very few packages with restrictions like “If you include this package (A), you cannot include other package (B).”

仅凭 Piper 强大的扩展能力，还无法实现我们所依赖的协作方式。正如前文所说，版本控制也离不开策略。除了 VCS 本身，谷歌版本控制策略还有一个关键特征，我们称为“单版本”。它把前文的“唯一权威来源”概念进一步扩展：不仅要让开发者知道以哪个仓库的哪个分支为准，还要求“仓库中的每项依赖，都只能有一个可供选择的版本”。对第三方软件包而言，这意味着在稳定状态下，仓库中只能检入该包的一个版本。对内部软件包而言，这意味着分叉时必须重新打包或重命名，让原版和分叉版能够在技术上安全地共存于同一个项目，无须额外处理。这给我们的生态系统带来了很大便利：极少有软件包需要规定“引入软件包 A，就不能引入软件包 B”。

This notion of having a single copy on a single branch in a single repository as our Source of Truth is intuitive but also has some subtle depth in application. Let’s investigate a scenario in which we have a monorepo (and thus arguably have fulfilled the letter of the law on Single Source of Truth), but have allowed forks of our libraries to propagate on trunk.

以单个仓库、单个分支中的一份副本作为权威来源，这个概念很直观，但实践中的含义更为微妙。不妨考察这样一种情况：我们采用了单体代码仓库，表面上已经满足唯一权威来源的要求，却允许库的分叉在主干上不断增多。

> [^9]: For example, during an upgrade operation, there might be two versions checked in, but if a developer is adding a new dependency on an existing package, there should be no choice in which version to depend upon.
>
> 9  例如，升级期间可能同时检入两个版本，但开发者新添对现有软件包的依赖时，应该只有一个版本可选。
>
> [^10]: That said, we fail at this in many cases because external packages sometimes have pinned copies of their own dependencies bundled in their source release. You can read more on how all of this goes wrong in Chapter 21.
>
> 10 不过，我们在不少情况下也未能做到，因为外部软件包有时会在发布的源码中捆绑自身依赖的固定版本副本。第21章会进一步讨论由此引发的问题。

### Scenario: Multiple Available Versions  场景：多个可用版本

Imagine the following scenario: some team discovers a bug in common infrastructure code (in our case, Abseil or Guava or the like). Rather than fix it in place, the team decides to fork that infrastructure and tweak it to work around the bug—without renaming the library or the symbols. It informs other teams near them, “Hey, we have an improved version of Abseil checked in over here: check it out.” A few other teams build libraries that themselves rely on this new fork.

设想某个团队发现公共基础设施代码中有一个 bug，比如谷歌使用的 Abseil 或 Guava。团队没有直接修复原版，而是分叉这份基础设施代码，稍作修改以绕过缺陷，却没有重命名库或其中的符号。他们告诉周边团队：“我们在这里检入了一个改进版 Abseil，来看看。”随后，其他几个团队编写的库也依赖了这个新分叉。

As we’ll see in Chapter 21, we’re now in a dangerous situation. If any project in the codebase comes to depend on both the original and the forked versions of Abseil simultaneously, in the best case, the build fails. In the worst case, we’ll be subjected to difficult-to-understand runtime bugs stemming from linking in two mismatched versions of the same library. The “fork” has effectively added a coloring/partitioning property to the codebase: the transitive dependency set for any given target must include exactly one copy of this library. Any link added from the “original flavor” partition of the codebase to the “new fork” partition will likely break things. This means that in the end that something as simple as “adding a new dependency” becomes an operation that might require running all tests for the entire codebase, to ensure that we haven’t violated one of these partitioning requirements. That’s expensive, unfortunate, and doesn’t scale well.

正如第21章将要讨论的，此时我们已处于危险境地。如果代码库中的任何项目同时依赖 Abseil 原版和分叉版，最好的结果也是构建失败；最坏的情况是，同一个库的两个不匹配版本被链接到一起，产生难以理解的运行时缺陷。这个“fork”实际上给代码库加上了着色或分区的约束：任一构建目标的传递依赖集合，都必须恰好包含该库的一份副本。从使用“原版”的分区向使用“新分叉”的分区新增任何依赖关系，都可能造成故障。到头来，就连“添加一项新依赖”这样简单的操作，也可能需要运行整个代码库的全部测试，才能确认没有违反这些分区约束。这既昂贵又令人遗憾，也不利于规模扩展。

In some cases, we might be able to hack things together in a way to allow a resulting executable to function correctly. Java, for instance, has a relatively standard practice called [*shading*](https://oreil.ly/RuWX3), which tweaks the names of the internal dependencies of a library to hide those dependencies from the rest of the application. When dealing with functions, this is technically sound, even if it is theoretically a bit of a hack. When dealing with types that can be passed from one package to another, shading solutions work neither in theory nor in practice. As far as we know, any technological trickery that allows multiple isolated versions of a library to function in the same binary share this limitation: that approach will work for functions, but there is no good (efficient) solution to shading types—multiple versions for any library that provides a vocabulary type (or any higher-level construct) will fail. Shading and related approaches are patching over the underlying issue: multiple versions of the same dependency are needed. (We’ll discuss how to minimize that in general in Chapter 21.)

有时，可以通过一些变通手段让最终的可执行文件正常运行。例如，Java 有一种较为标准的做法，叫作 [*shading*](https://oreil.ly/RuWX3)：修改库内部依赖的名称，让应用程序的其他部分看不到这些依赖。对于函数，这在技术上可行，虽然从理论上看有些取巧；但对于需要在软件包之间传递的类型，shading 无论在理论上还是实践中都行不通。据我们所知，任何让同一个库的多个隔离版本在同一二进制文件中运行的技术手段，都有这一限制：函数可以这样处理，类型却没有理想且高效的 shading 方案。只要库提供词汇类型或更高层次的结构，多版本共存就会失败。Shading 及类似方法只是暂时掩盖了根本问题：系统需要同一依赖的多个版本。（第21章将讨论一般如何尽量减少这种情况。）

Any policy system that allows for multiple versions in the same codebase is allowing for the possibility of these costly incompatibilities. It’s possible that you’ll get away with it for a while (we certainly have a number of small violations of this policy), but in general, any multiple-version situation has a very real possibility of leading to big problems.

任何允许同一代码库中存在多个版本的策略，都容许了这些代价高昂的不兼容问题。你也许能暂时相安无事，我们自己也确实有少量违反这项策略的情况，但总体而言，多版本共存确实可能引发严重问题。

### The “One-Version” Rule  “单版本”规则

With that example in mind, on top of the Single Source of Truth model, we can hopefully understand the depth of this seemingly simple rule for source control and branch management:

结合这个例子，再回到唯一权威来源模型，就更容易理解下面这条看似简单的源代码版本控制与分支管理规则的深意：

    Developers must never have a choice of “What version of this component should I depend upon?”
    绝不能让开发者面对“我应该依赖这个组件的哪个版本？”这样的选择。

Colloquially, this becomes something like a “One-Version Rule.” In practice, “One- Version” is not hard and fast,[^11] but phrasing this around limiting the versions that can be *chosen* when adding a new dependency conveys a very powerful understanding.

通俗地说，这就是“单版本规则”。实践中，“单版本”并非绝对不能变通，但把要求表述为“添加新依赖时限制可选版本”，能够更准确地传达这条规则的重要含义。

For an individual developer, lack of choice can seem like an arbitrary impediment. Yet we see again and again that for an organization, it’s a critical component in efficient scaling. Consistency has a profound importance at all levels in an organization. From one perspective, this is a direct side effect of discussions about consistency and ensuring the ability to leverage consistent “choke points.”

对单个开发者而言，不给选择可能像是人为设置的无理障碍。但我们反复看到，对整个组织而言，这却是高效扩大规模的关键。一致性在组织各个层面都至关重要。从某个角度说，这正是强调一致性、确保能够利用统一“控制点”所直接带来的结果。

> [^11]: For instance, if there are external/third-party libraries that are periodically updated, it might be infeasible to update that library and update all use of it in a single atomic change. As such, it is often necessary to add a new version of that library, prevent new users from adding dependencies on the old one, and incrementally switch usage from old to new.
>
> 11 例如，外部或第三方库定期更新时，可能无法在一次原子变更中同时升级库及其所有使用方。因此，往往需要先加入新版本，禁止新使用方依赖旧版本，再逐步把现有使用方迁移到新版本。

### (Nearly) No Long-Lived Branches  (几乎)没有长期存在的分支

There are several deeper ideas and policies implicit in our One-Version Rule; foremost among them: development branches should be minimal, or at best be very short lived. This follows from a lot of published work over the past 20 years, from Agile processes to DORA research results on trunk-based development and even Phoenix Project[^12] lessons on “reducing work-in-progress.” When we include the idea of pending work as akin to a dev branch, this further reinforces that work should be done in small increments against trunk, committed regularly.

单版本规则隐含着几项更深层次的理念和策略，最重要的是：尽量少用开发分支，使用时也应让它们的存续时间尽可能短。过去20年间的大量成果都支持这一点，从敏捷流程、DORA 关于主干开发的研究，到《凤凰城项目》中“减少尚未完成的工作”的经验，都有体现。如果再把待完成的工作也看作开发分支，就更能理解：工作应基于主干，以小步增量推进，并定期提交。

As a counterexample: in a development community that depends heavily on long- lived development branches, it isn’t difficult to imagine opportunity for choice creeping back in.

反过来看，如果一个开发社区高度依赖长期存在的开发分支，就不难想象，版本选择的问题会重新出现。

Imagine this scenario: some infrastructure team is working on a new Widget, better than the old one. Excitement grows. Other newly started projects ask, “Can we depend on your new Widget?” Obviously, this can be handled if you’ve invested in codebase visibility policies, but the deep problem happens when the new Widget is “allowed” but only exists in a parallel branch. Remember: new development must not have a choice when adding a dependency. That new Widget should be committed to trunk, disabled from the runtime until it’s ready, and hidden from other developers by visibility if possible—or the two Widget options should be designed such that they can coexist, linked into the same programs.

设想某个基础设施团队正在开发新的 Widget，比旧版更好，大家越来越期待。其他新启动的项目问：“我们能依赖你们的新 Widget 吗？”如果事先建立了代码库可见性策略，当然可以处理这种请求。真正的问题在于：新 Widget 已“获准”使用，却只存在于一条并行分支中。不要忘记，新的开发工作在添加依赖时，不应面临版本选择。新 Widget 应提交到主干，准备好之前在运行时禁用，并尽可能通过可见性限制对其他开发者隐藏。另一种办法是将两个 Widget 设计成可以共存，能够链接进同一个程序。

Interestingly, there is already evidence of this being important in the industry. In Accelerate and the most recent State of DevOps reports, DORA points out that there is a predictive relationship between trunk-based development and high-performing software organizations. Google is not the only organization to have discovered this— nor did we necessarily have expected outcomes in mind when these policies evolved —--—it just seemed like nothing else worked. DORA’s result certainly matches our experience.

值得注意的是，业界已有证据表明这件事很重要。在《加速》和最新的《DevOps 状况报告》中，DORA 指出，主干开发可以用于预测软件组织的高绩效。发现这一点的并不只有谷歌；这些策略形成时，我们也未必事先预见了结果，只是觉得其他办法似乎都行不通。DORA 的研究结果确实与我们的经验一致。

Our policies and tools for large-scale changes (LSCs; see [Chapter 22](#_bookmark1935)) put additional weight on the importance of trunk-based development: broad/shallow changes that are applied across the codebase are already a massive (often tedious) undertaking when modifying everything checked in to the trunk branch. Having an unbounded number of additional dev branches that might need to be refactored at the same time would be an awfully large tax on executing those types of changes, finding an ever- expanding set of hidden branches. In a DVCS model, it might not even be possible to identify all of those branches.

我们针对大规模变更（LSCs，见第22章）的策略和工具，进一步凸显了主干开发的重要性。这类变更涉及整个代码库，范围广、单处改动浅；即使只修改已经检入主干的代码，也是庞大而往往繁琐的工作。如果还要同时重构数量没有上限的开发分支，就得不断寻找越来越多的隐藏分支，执行成本会大幅增加。在 DVCS 模型中，甚至未必能找出所有这些分支。

Of course, our experience is not universal. You might find yourself in unusual situations that require longer-lived dev branches in parallel to (and regularly merged with) trunk.

当然，我们的经验并非适用于所有情况。有些特殊场景可能确实需要让开发分支与主干长期并行，并定期与主干合并。

Those scenarios should be rare, and should be understood to be expensive. Across the roughly 1,000 teams that work in the Google monorepo, there are only a couple that have such a dev branch.[^13] Usually these exist for a very specific (and very unusual) reason. Most of those reasons boil down to some variation of “We have an unusual requirement for compatibility over time.” Oftentimes this is a matter of ensuring compatibility for data at rest across versions: readers and writers of some file format need to agree on that format over time even if the reader or writer implementations are modified. Other times, long-lived dev branches might come from promising API compatibility over time—when One Version isn’t enough and we need to promise that an older version of a microservice client still works with a newer server (or vice versa). That can be a very challenging requirement, something that you should not promise lightly for an actively evolving API, and something you should treat carefully to ensure that period of time doesn’t accidentally begin to grow. Dependency across time in any form is far more costly and complicated than code that is time invariant. Internally, Google production services make relatively few promises of that form.[^14] We also benefit greatly from a cap on potential version skew imposed by our “build horizon”: every job in production needs to be rebuilt and redeployed every six months, maximum. (Usually it is far more frequent than that.)

这种场景应当很少，而且必须认识到它的成本很高。在使用谷歌单体代码仓库的约1,000个团队中，只有两三个团队维护这样的开发分支，通常都有非常具体、非常特殊的原因。多数原因可以归结为：“我们有特殊的跨时间兼容性要求。”常见情况是必须保证已存储数据在不同版本间兼容：即使某种文件格式的读写实现发生变化，双方对格式的理解也必须始终一致。另一些长期开发分支则源于 API 的长期兼容性承诺：仅靠单版本已不够，必须保证旧版微服务客户端仍能与新版服务端配合，或反过来，保证新版客户端仍能与旧版服务端配合。这可能是极具挑战性的要求。对于仍在积极演进的 API，不应轻易作出这种承诺；还应谨慎控制兼容期限，避免它不知不觉延长。任何形式的跨时间依赖，都比不涉及时间变化的代码昂贵、复杂得多。谷歌内部的生产服务较少作出此类承诺。我们的“构建时限”还为潜在的版本偏差设置了上限，从中受益很大：每项生产作业都必须重新构建并部署，两次之间最长不得超过六个月。（通常要频繁得多。）

We’re sure there are other situations that might necessitate long-lived dev branches. Just make sure to keep them rare. If you adopt other tools and practices discussed in this book, many will tend to exert pressure against long-lived dev branches. Automation and tooling that works great at trunk and fails (or takes more effort) for a dev branch can help encourage developers to stay current.

当然，还可能有其他情况需要长期开发分支，但务必让它们保持少量。如果采用本书介绍的其他工具和实践，其中许多都会促使团队减少长期开发分支。自动化和工具在主干上运行良好，在开发分支上却可能失败，或需要额外投入，这会鼓励开发者持续跟进主干。

> [^12]: Kevin Behr, Gene Kim, and George Spafford, The Phoenix Project (Portland: IT Revolution Press, 2018).
> 12  Kevin Behr、Gene Kim 和 George Spafford，《凤凰城项目》（波特兰：IT 革命出版社，2018年）。
>
> [^13]: It’s difficult to get a precise count, but the number of such teams is almost certainly fewer than 10./
>
> 13  很难准确统计，但这样的团队几乎肯定不到10个。
>
> [^14]: Cloud interfaces are a different story.
> 14  云接口是另一回事。

#### What About Release Branches?  发布分支呢？

Many Google teams use release branches, with limited cherry picks. If you’re going to put out a monthly release and continue working toward the next release, it’s perfectly reasonable to make a release branch. Similarly, if you’re going to ship devices to customers, it’s valuable to know exactly what version is out “in the field.” Use caution and reason, keep cherry picks to a minimum, and don’t plan to remerge with trunk. Our various teams have all sorts of policies about release branches given that relatively few teams have arrived at the sort of rapid release cadence promised by CD (see Chapter 24) that obviates the need or desire for a release branch. Generally speaking,release branches don’t cause any widespread cost in our experience. Or, at least, no noticeable cost above and beyond the additional inherent cost to the VCS.

谷歌许多团队都会使用发布分支，只进行少量选择性合并。如果计划每月发布一次，同时继续开发下一个版本，创建发布分支完全合理。向客户交付设备时，准确知道客户实际使用的是哪个版本，也很有价值。应谨慎、理性地使用发布分支，尽量减少选择性合并（cherry picks），不要计划再合回主干。达到 CD 所追求的快速发布节奏（见第24章）、因而不再需要或希望使用发布分支的团队，还相对较少，所以各团队采用了不同的发布分支策略。总体而言，根据我们的经验，发布分支不会造成广泛的成本，至少除了 VCS 本身固有的额外开销，没有其他明显成本。

## Monorepos    单体代码仓库

In 2016, we published a (highly cited, much discussed) paper on Google’s monorepo approach.[^15] The monorepo approach has some inherent benefits, and chief among them is that adhering to One Version is trivial: it’s usually more difficult to violate One Version than it would be to do the right thing. There’s no process of deciding which versions of anything are official, or discovering which repositories are important. Building tools to understand the state of the build (see Chapter 23) doesn’t also require discovering where important repositories exist. Consistency helps scale up the impact of introducing new tools and optimizations. By and large, engineers can see what everyone else is doing and use that to inform their own choices in code and system design. These are all very good things.

2016年，我们发表了一篇介绍 Google 单体代码仓库实践的论文，后来被广泛引用和讨论。monorepo 有一些天然优势，最重要的是遵守单版本规则很容易：违反规则往往比遵守规则还难。不必再判断哪个版本才是正式版本，也不必寻找哪些仓库才重要。开发用于了解构建状态的工具（见第23章）时，同样无须先找出重要仓库的位置。一致性有助于扩大新工具和优化措施的成效。总体而言，工程师能看到其他人在做什么，并以此为自己的代码和系统设计提供参考。这些都是实实在在的好处。

Given all of that and our belief in the merits of the One-Version Rule, it is reasonable to ask whether a monorepo is the One True Way. By comparison, the open source community seems to work just fine with a “manyrepo” approach built on a seemingly infinite number of noncoordinating and nonsynchronized project repositories.

考虑到这些优势，以及我们对单版本规则的认可，自然会问：单体代码仓库是否是唯一正确的做法？相比之下，开源社区采用多仓库方式，建立在几乎数不清、彼此不协调也不同步的项目仓库之上，似乎同样运行良好。

In short: no, we don’t think the monorepo approach as we’ve described it is the perfect answer for everyone. Continuing the parallel between filesystem format and VCS, it’s easy to imagine deciding between using 10 drives to provide one very large logical filesystem or 10 smaller filesystems accessed separately. In a filesystem world, there are pros and cons to both. Technical issues when evaluating filesystem choice would range from outage resilience, size constraints, performance characteristics, and so on. Usability issues would likely focus more on the ability to reference files across filesystem boundaries, add symlinks, and synchronize files.

简而言之，不是。我们并不认为上述单体代码仓库方式对所有人都是完美答案。继续沿用文件系统格式与 VCS 的类比：可以把10块磁盘组成一个很大的逻辑文件系统，也可以组成10个分别访问的小文件系统。两种方式各有利弊。选择时，技术上要考虑故障应对能力、容量限制、性能特征等；使用体验上则更关注能否跨文件系统引用文件、添加符号链接和同步文件。

A very similar set of issues governs whether to prefer a monorepo or a collection of finer-grained repositories. The specific decisions of how to store your source code (or store your files, for that matter) are easily debatable, and in some cases, the particulars of your organization and your workflow are going to matter more than others. These are decisions you’ll need to make yourself.

选择单体代码仓库，还是一组粒度更细的仓库，也取决于一组类似问题。源代码该如何存储，乃至文件该如何存储，都很容易引起争论。在某些情境下，组织和工作流的具体特点会格外重要。这些决策需要你自己作出。

What is important is not whether we focus on monorepo; it’s to adhere to the One- Version principle to the greatest extent possible: developers must not have a *choice* when adding a dependency onto some library that is already in use in the organization. Choice violations of the One-Version Rule lead to merge strategy discussions, diamond dependencies, lost work, and wasted effort.

关键不在于是否采用单体代码仓库，而在于尽可能遵守单版本原则：开发者添加对组织已经使用的某个库的依赖时，不能有版本*选择*。允许违反这条规则的选择，就会带来合并策略讨论、菱形依赖、工作成果丢失和精力浪费。

Software engineering tools including both VCS and build systems are increasingly providing mechanisms to smartly blend between fine-grained repositories and monorepos to provide an experience akin to the monorepo—an agreed-upon ordering of commits and understanding of the dependency graph. Git submodules, Bazel with external dependencies, and CMake subprojects all allow modern developers to synthesize something weakly approximating monorepo behavior without the costs and downsides of a monorepo.[^16] For instance, fine-grained repositories are easier to deal with in terms of scale (Git often has performance issues after a few million commits and tends to be slow to clone when repositories include large binary artifacts) and storage (VCS metadata can add up, especially if you have binary artifacts in your version control system). Fine-grained repositories in a federated/virtual-monorepo (VMR)–style repository can make it easier to isolate experimental or top-secret projects while still holding to One Version and allowing access to common utilities.

VCS、构建系统等软件工程工具，正越来越多地提供机制，将细粒度仓库与单体代码仓库的特点结合起来，形成类似单体代码仓库的体验：对提交顺序达成一致，并能掌握依赖关系图。Git 子模块、Bazel 的外部依赖支持和 CMake 子项目，都能让开发者在一定程度上模拟单体代码仓库的行为，又不必承担其成本和弊端。例如，细粒度仓库在规模和存储方面更容易管理：Git 的提交量达到几百万后往往会出现性能问题，仓库包含大型二进制构件时，克隆也通常较慢；VCS 元数据同样会不断累积，尤其是仓库包含二进制构件时。采用联合式或虚拟单体代码仓库（VMR）模式来组织细粒度仓库，更便于隔离实验性或绝密项目，同时仍能遵守单版本规则，并访问通用工具。

To put it another way: if every project in your organization has the same secrecy, legal, privacy, and security requirements,[^17] a true monorepo is a fine way to go. Otherwise, *aim* for the functionality of a monorepo, but allow yourself the flexibility of implementing that experience in a different fashion. If you can manage with disjoint repositories and adhere to One Version or your workload is all disconnected enough to allow truly separate repositories, great. Otherwise, synthesizing something like a VMR in some fashion may represent the best of both worlds.

换句话说，如果组织中所有项目的保密、法律、隐私和安全要求都相同，真正的单体代码仓库是不错的选择。否则，应以获得单体代码仓库的功能为目标，同时保留用其他方式实现这种体验的灵活性。如果使用分离的仓库也能遵守单版本规则，或者各项工作本就足够独立，可以采用真正互不相干的仓库，那很好。否则，以某种方式构建类似 VMR 的体系，可能更能兼得两者之长。

After all, your choice of filesystem format really doesn’t matter as much as what you write to it.

毕竟，与你所写入的内容相比，文件系统格式的选择并不是那么重要。

> [^15]: Rachel Potvin and Josh Levenberg, “Why Google stores billions of lines of code in a single repository,” Communications of the ACM, 59 No. 7 (2016): 78-87.
>
> 15 Rachel Potvin 和 Josh Levenberg，《为什么谷歌将数十亿行代码存储在一个代码仓库中》，《ACM 通讯》，第59卷第7期（2016）：78-87。
>
> [^16]: We don’t think we’ve seen anything do this particularly smoothly, but the interrepository dependencies/virtual monorepo idea is clearly in the air.
>
> 16 据我们所见，还没有哪套系统能特别顺畅地做到这一点，但仓库间依赖和虚拟单体代码仓库的想法，显然已在酝酿之中。
>
> [^17]: Or you have the willingness and capability to customize your VCS—and maintain that customization for the lifetime of your codebase/organization. Then again, maybe don’t plan on that as an option; that is a lot of overhead.
>
> 17 或者，你愿意且有能力定制 VCS，并在代码库或组织的整个生命周期内维护这些定制。不过，也许最好别把它列为选项，毕竟开销很大。

## Future of Version Control  版本控制的未来

Google isn’t the only organization to publicly discuss the benefits of a monorepo approach. Microsoft, Facebook, Netflix, and Uber have also publicly mentioned their reliance on the approach. DORA has published about it extensively. It’s vaguely possible that all of these successful, long-lived companies are misguided, or at least that their situations are sufficiently different as to be inapplicable to the average smaller organization. Although it’s possible, we think it is unlikely.

公开讨论单体代码仓库优势的组织并不只有谷歌。微软、Facebook、Netflix 和 Uber 也公开提到采用这种方式，DORA 更对此作了大量论述。这些成功且长期经营的公司，也许全都判断失误；又或者，它们的情况确实与一般较小组织差异太大，经验无法适用。这种可能性虽不能排除，但我们认为不大。

Most arguments against monorepos focus on the technical limitations of having a single large repository. If cloning a repository from upstream is quick and cheap, developers are more likely to keep changes small and isolated (and to avoid making mistakes with committing to the wrong work-in-progress branch). If cloning a repository (or doing some other common VCS operation) takes hours of wasted developer time, you can easily see why an organization would shy away from reliance on such a large repository/operation. We luckily avoided this pitfall by focusing on providing a VCS that scales massively.

反对单体代码仓库的理由，大多集中在单个大型仓库的技术限制上。如果从上游克隆仓库既快又便宜，开发者就更容易把变更保持在小范围内并相互隔离，也更不容易误提交到另一个尚在开发的分支。如果克隆仓库或执行其他常见 VCS 操作，要白白耗去开发者几个小时，组织不愿依赖这种大型仓库和操作，也就不难理解。我们一直着力提供能支持超大规模的 VCS，因而有幸避开了这个问题。

Looking at the past few years of major improvements to Git, there’s clearly a lot of work being done to support larger repositories: shallow clones, sparse branches, better optimization, and more. We expect this to continue and the importance of “but we need to keep the repository small” to diminish.

回顾过去几年 Git 的重大改进，可以看到大量工作都在支持更大的仓库，例如浅克隆、稀疏分支和进一步优化等。我们预计这一趋势会持续下去，“必须让仓库保持小规模”这一顾虑的重要性也会下降。

The other major argument against monorepos is that it doesn’t match how development happens in the Open Source Software (OSS) world. Although true, many of the practices in the OSS world come (rightly) from prioritizing freedom, lack of coordination, and lack of computing resources. Separate projects in the OSS world are effectively separate organizations that happen to be able to see one another’s code. Within the boundaries of an organization, we can make more assumptions: we can assume the availability of compute resources, we can assume coordination, and we can assume that there is some amount of centralized authority.

另一个反对单体代码仓库的主要理由，是它不符合开源软件（OSS）领域的开发方式。这一点没错，但开源领域的许多实践，源于对自由的优先考虑，以及缺乏协调和计算资源的现实，这些选择自有其合理性。开源领域的各个项目，实际上是碰巧能够查看彼此代码的独立组织。而在一个组织内部，可以作出更多假设：有可用的计算资源，能够协调，也存在一定程度的集中决策权。

A less common but perhaps more legitimate concern with the monorepo approach is that as your organization scales up, it is less and less likely that every piece of code is subject to exactly the same legal, compliance, regulatory, secrecy, and privacy requirements. One native advantage of a manyrepo approach is that separate repositories are obviously capable of having different sets of authorized developers, visibility, permissions, and so on. Stitching that feature into a monorepo can be done but implies some ongoing carrying costs in terms of customization and maintenance.

对单体代码仓库还有一种较少提及、却可能更合理的担忧：组织越大，所有代码受同一套法律、合规、监管、保密和隐私要求约束的可能性就越小。多仓库方式有一个天然优势：各仓库可以分别设置获授权的开发者、可见范围和权限。单体代码仓库也能加入这些功能，但需要持续承担定制和维护成本。

At the same time, the industry seems to be inventing lightweight interrepository linkage over and over again. Sometimes, this is in the VCS (Git submodules) or the build system. So long as a collection of repositories have a consistent understanding of “what is trunk,” “which change happened first,” and mechanisms to describe dependencies, we can easily imagine stitching together a disparate collection of physical repositories into one larger VMR. Even though Piper has done very well for us, investing in a highly scaling VMR and tools to manage it and relying on off-the-shelf customization for per-repository policy requirements could have been a better investment.

与此同时，业界似乎在反复设计轻量级的仓库间关联机制，有的放在 VCS 中，例如 Git 子模块，有的放在构建系统中。只要一组仓库对“什么是主干”“哪项变更先发生”有一致认识，并有机制描述依赖关系，就不难设想把这些分散的物理仓库连接成更大的 VMR。Piper 虽然很好地满足了我们的需求，但如果当初投入一个高度可扩展的 VMR 及其管理工具，并利用现成工具的定制能力满足各仓库的策略要求，也许会是更好的投资。

As soon as someone builds a sufficiently large nugget of compatible and interdependent projects in the OSS community and publishes a VMR view of those packages, we suspect that OSS developer practices will begin to change. We see glimpses of this in the tools that *could* synthesize a virtual monorepo as well as in the work done by (for instance) large Linux distributions discovering and publishing mutually compatible revisions of thousands of packages. With unit tests, CI, and automatic version bumping for new submissions to one of those revisions, enabling a package owner to update trunk for their package (in nonbreaking fashion, of course), we think that model will catch on in the open source world. It is just a matter of efficiency, after all: a (virtual) monorepo approach with a One-Version Rule cuts down the complexity of software development by a whole (difficult) dimension: time.

我们推测，一旦有人在 OSS 社区中聚合起一组足够庞大、彼此兼容且相互依赖的项目，并发布这些软件包的 VMR 视图，开源开发者的实践就会开始改变。能够构建虚拟单体代码仓库的工具，以及大型 Linux 发行版等所做的工作，已经显露出这种趋势：后者会找出并发布数千个软件包彼此兼容的修订版。如果再配合单元测试、CI，以及其中某个修订版收到新提交时自动递增版本号的机制，让软件包维护者能够在不破坏兼容性的前提下更新自己的主干，我们认为这种模式会在开源领域普及。归根结底，这是效率问题：采用单体代码仓库，即使只是虚拟的，再加上单版本规则，可以从软件开发的复杂性中减少整整一个难以处理的维度，也就是时间。

We expect version control and dependency management to evolve in this direction in the next 10 to 20 years: VCSs will focus on *allowing* larger repositories with better performance scaling, but also removing the need for larger repositories by providing better mechanisms to stitch them together across project and organizational boundaries. Someone, perhaps the existing package management groups or Linux distributors, will catalyze a de facto standard virtual monorepo. Depending on the utilities in that monorepo will provide easy access to a compatible set of dependencies as one unit. We’ll more generally recognize that version numbers are timestamps, and that allowing version skew adds a dimensionality complexity (time) that costs a lot—and that we can learn to avoid. It starts with something logically like a monorepo.

我们预计，未来10到20年，版本控制和依赖管理会朝这个方向演进：VCS 一方面支持*更大的代码仓库*，让性能更好地随规模扩展；另一方面，提供更好的机制，跨越项目和组织边界连接仓库，从而不再需要物理上的大型仓库。某个组织，也许是现有的软件包管理团队或 Linux 发行版提供方，会推动形成一个事实上的标准虚拟单体代码仓库。依赖其中的通用工具，就能方便地获得一整组相互兼容的依赖。人们会更普遍地认识到，版本号就是时间戳；允许版本偏差，就增加了时间这一维度的复杂性，代价高昂，却是可以学会避免的。起点，就是在逻辑上形成类似单体代码仓库的体系。

## Conclusion  总结

Version control systems are a natural extension of the collaboration challenges and opportunities provided by technology, especially shared compute resources and computer networks. They have historically evolved in lockstep with the norms of software engineering as we understand them at the time.

技术，尤其是共享计算资源和计算机网络，带来了协作的机遇与挑战，版本控制系统正是在此基础上自然发展而来的。纵观其历史，版本控制始终与各个时期人们对软件工程规范的认识同步演进。

Early systems provided simplistic file-granularity locking. As typical software engineering projects and teams grew larger, the scaling problems with that approach became apparent, and our understanding of version control changed to match those challenges. Then, as development increasingly moved toward an OSS model with distributed contributors, VCSs became more decentralized. We expect a shift in VCS technology that assumes constant network availability, focusing more on storage and build in the cloud to avoid transmitting unnecessary files and artifacts. This is increasingly critical for large, long-lived software engineering projects, even if it means a change in approach compared to simple single-dev/single-machine programming projects. This shift to cloud will make concrete what has emerged with DVCS approaches: even if we allow distributed development, something must still be centrally recognized as the Source of Truth.

早期系统只提供简单的文件粒度锁定。软件工程项目和团队的典型规模扩大后，这种方式的扩展问题逐渐显现，我们对版本控制的认识也随之改变。后来，开发越来越多地采用贡献者分散各地的开源模式，VCS 也变得更加去中心化。我们预计，VCS 技术会转向以网络持续可用为前提，更重视云端存储和构建，避免传输不必要的文件和构件。对大型、长期的软件工程项目而言，这一点愈发重要，尽管它意味着不能继续沿用简单的单人、单机编程项目的做法。转向云端，会让 DVCS 实践中已显现的认识更加具体：即使允许分布式开发，也必须共同认定一个权威来源。

The current DVCS decentralization is a sensible reaction of the technology to the needs of the industry (especially the open source community). However, DVCS configuration needs to be tightly controlled and coupled with branch management policies that make sense for your organization. It also can often introduce unexpected scaling problems: perfect fidelity offline operation requires a lot more local data. Failure to rein in the potential complexity of a branching free-for-all can lead to a potentially unbounded amount of overhead between developers and deployment of that code. However, complex technology doesn’t need to be used in a complex fashion: as we see in monorepo and trunk-based development models, keeping branch policies simple generally leads to better engineering outcomes.

当前 DVCS 的去中心化，是技术对行业需求，尤其是开源社区需求的合理回应。但 DVCS 配置需要严格控制，并配合适合本组织的分支管理策略。它也常会引入意想不到的规模问题：要在离线时完整保留原有操作能力，就需要更多本地数据。如果放任分支自由增生，不约束由此产生的复杂性，从开发到部署之间的开销就可能没有上限。不过，技术复杂，不等于使用方式也必须复杂。单体代码仓库和主干开发的实践表明，保持分支策略简单，通常能取得更好的工程成果。

Choice leads to costs here. We highly endorse the One-Version Rule presented here: developers within an organization must not have a choice where to commit, or which version of an existing component to depend upon. There are few policies we’re aware of that can have such an impact on the organization: although it might be annoying for individual developers, in the aggregate, the end result is far better.

在这里，选择会带来成本。我们强烈支持本章提出的单版本规则：组织内的开发者向哪里提交、依赖现有组件的哪个版本，都不应存在选择。据我们所知，很少有策略能对组织产生如此大的影响。它可能让个别开发者觉得烦恼，但整体结果要好得多。

## TL;DRs  内容提要

- Use version control for any software development project larger than “toy project with only one developer that will never be updated.”
- There’s an inherent scaling problem when there are choices in “which version of this should I depend upon?”
- One-Version Rules are surprisingly important for organizational efficiency. Removing choices in where to commit or what to depend upon can result in significant simplification.
- In some languages, you might be able to spend some effort to dodge this with technical approaches like shading, separate compilation, linker hiding, and so on. The work to get those approaches working is entirely lost labor—your software engineers aren’t producing anything, they’re just working around technical debts.
- Previous research (DORA/State of DevOps/Accelerate) has shown that trunk- based development is a predictive factor in high-performing development organizations. Long-lived dev branches are not a good default plan.
- Use whatever version control system makes sense for you. If your organization wants to prioritize separate repositories for separate projects, it’s still probably wise for interrepository dependencies to be unpinned/“at head”/“trunk based.” There are an increasing number of VCS and build system facilities that allow you to have both small, fine-grained repositories as well as a consistent “virtual” head/trunk notion for the whole organization.

- 只要软件开发项目超出了“仅由一人开发、永不更新的玩具项目”的范围，就应使用版本控制。
- 一旦需要选择“应该依赖它的哪个版本”，就存在固有的规模扩展问题。
- 单版本规则对组织效率的重要性超乎想象。消除提交位置和依赖版本的选择，可以显著简化工作。
- 在某些语言中，或许可以花些精力用 shading、分别编译、链接器隐藏等技术绕过这类问题。但让这些方法运转起来，完全是在白费力气：工程师没有产出新东西，只是在绕开技术债务。
- 既有研究（DORA/State of DevOps/Accelerate）表明，主干开发是预测开发组织高绩效的因素之一。长期存在的开发分支不宜作为默认方案。
- 选择适合自己的版本控制系统。如果组织优先考虑为不同项目设置独立仓库，让仓库间的依赖不固定在某个版本，而是跟随最新版本或主干，可能仍是明智的选择。越来越多的 VCS 和构建系统功能，既支持小型、细粒度的仓库，也支持整个组织一致的“虚拟”最新版本或主干概念。
