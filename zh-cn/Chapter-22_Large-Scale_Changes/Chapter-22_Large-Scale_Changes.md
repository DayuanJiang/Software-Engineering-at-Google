
**CHAPTER 22**

# Large-Scale Changes

# 第二十二章 大规模变更

**Written by Hyrum Wright**

**Edited by Lisa Carey**

Think for a moment about your own codebase. How many files can you reliably update in a single, simultaneous commit? What are the factors that constrain that number? Have you ever tried committing a change that large? Would you be able to do it in a reasonable amount of time in an emergency? How does your largest commit size compare to the actual size of your codebase? How would you test such a change? How many people would need to review the change before it is committed? Would you be able to roll back that change if it did get committed? The answers to these questions might surprise you (both what you *think* the answers are and what they actually turn out to be for your organization).

想一想你自己的代码库。一次提交同时更新多个文件时，你能可靠地更新多少个？哪些因素限制了这个数量？你尝试过提交这么大的变更吗？如果遇到紧急情况，能在合理的时间内完成吗？你做过的最大一次提交，与整个代码库的实际规模相比有多大？这样的变更该如何测试？提交之前需要多少人审查？提交之后还能回滚吗？这些问题的答案可能会让你意外，无论是你*认为*的答案，还是你的组织在实践中得出的答案。

At Google, we’ve long ago abandoned the idea of making sweeping changes across our codebase in these types of large atomic changes. Our observation has been that, as a codebase and the number of engineers working in it grows, the largest atomic change possible counterintuitively *decreases—*running all affected presubmit checks and tests becomes difficult, to say nothing of even ensuring that every file in the change is up to date before submission. As it has become more difficult to make sweeping changes to our codebase, given our general desire to be able to continually improve underlying infrastructure, we’ve had to develop new ways of reasoning about large-scale changes and how to implement them.

在谷歌，我们早已放弃通过这类大型原子变更来全面修改代码库的想法。我们观察到，随着代码库规模和参与开发的工程师数量增加，单次原子变更所能达到的最大规模反而会缩小。这有些违背直觉，但运行所有受影响的提交前检查和测试会变得困难，更不用说确保变更涉及的每个文件在提交前都已更新到最新版本。全面修改代码库越来越困难，而我们又希望持续改进底层基础设施，因此不得不探索新的思路，理解并实施大规模变更。

In this chapter, we’ll talk about the techniques, both social and technical, that enable us to keep the large Google codebase flexible and responsive to changes in underlying infrastructure. We’ll also provide some real-life examples of how and where we’ve used these approaches. Although your codebase might not look like Google’s, understanding these principles and adapting them locally will help your development organization scale while still being able to make broad changes across your codebase.

本章将介绍组织协作和技术两方面的方法，说明我们如何让谷歌庞大的代码库保持灵活，能够应对底层基础设施的变化。我们还会通过实际案例，展示这些方法的用法和适用场景。你的代码库可能与谷歌不同，但理解这些原则并结合自身情况调整，有助于开发组织在扩大规模的同时，继续具备全面修改代码库的能力。

## What Is a Large-Scale Change? 什么是大规模变更？

Before going much further, we should dig into what qualifies as a large-scale change (LSC). In our experience, an LSC is any set of changes that are logically related but cannot practically be submitted as a single atomic unit. This might be because it touches so many files that the underlying tooling can’t commit them all at once, or it might be because the change is so large that it would always have merge conflicts. In many cases, an LSC is dictated by your repository topology: if your organization uses a collection of distributed or federated repositories,[^1] making atomic changes across them might not even be technically possible.[^2] We’ll look at potential barriers to atomic changes in more detail later in this chapter.

在进一步讨论之前，先明确什么样的变更算是大规模变更（LSC）。根据我们的经验，只要一组变更在逻辑上相互关联，却无法在实际操作中作为一个原子单元提交，就属于大规模变更。原因可能是涉及的文件太多，底层工具无法一次性提交，也可能是变更规模太大，总会遇到合并冲突。在许多情况下，是否需要大规模变更取决于代码仓库的拓扑结构：如果组织使用一组分布式或联邦式代码仓库，跨仓库进行原子变更甚至可能在技术上都无法实现。本章后面会详细讨论原子变更可能遇到的障碍。

LSCs at Google are almost always generated using automated tooling. Reasons for making an LSC vary, but the changes themselves generally fall into a few basic categories:

- Cleaning up common antipatterns using codebase-wide analysis tooling
- Replacing uses of deprecated library features
- Enabling low-level infrastructure improvements, such as compiler upgrades
- Moving users from an old system to a newer one[^3]

谷歌的大规模变更几乎都由自动化工具生成。实施这些变更的原因各不相同，但变更本身通常可分为以下几类：

- 使用覆盖整个代码库的分析工具，清理常见的反模式
- 替换对已弃用库功能的使用
- 为编译器升级等底层基础设施改进创造条件
- 将用户从旧系统迁移到新系统

The number of engineers working on these specific tasks in a given organization might be low, but it is useful for their customers to have insight into the LSC tools and process. By their very nature, LSCs will affect a large number of customers, and the LSC tools easily scale down to teams making only a few dozen related changes.

一个组织中专门从事这些工作的工程师可能不多，但他们服务的用户了解大规模变更的工具和流程，也很有帮助。大规模变更本身就会影响大量用户，而相关工具也很容易用于较小规模的工作，适合只需进行几十项相关变更的团队。

There can be broader motivating causes behind specific LSCs. For example, a new language standard might introduce a more efficient idiom for accomplishing a given task, an internal library interface might change, or a new compiler release might require fixing existing problems that would be flagged as errors by the new release. The majority of LSCs across Google actually have near-zero functional impact: they tend to be widespread textual updates for clarity, optimization, or future compatibility. But LSCs are not theoretically limited to this behavior-preserving/refactoring class of change.

某项大规模变更背后可能有更广泛的动因。例如，新的语言标准可能引入更高效的惯用写法来完成某项任务，内部库的接口可能发生变化，或者新版本编译器会将代码中已有的问题报为错误，因而需要修复。谷歌的大多数大规模变更实际上几乎不影响功能，通常只是为了让代码更清晰、进行优化或保证未来的兼容性，而广泛修改代码文本。不过，从理论上说，大规模变更并不限于这类保持行为不变的重构。

In all of these cases, on a codebase the size of Google’s, infrastructure teams might routinely need to change hundreds of thousands of individual references to the old pattern or symbol. In the largest cases so far, we’ve touched millions of references, and we expect the process to continue to scale well. Generally, we’ve found it advantageous to invest early and often in tooling to enable LSCs for the many teams doing infrastructure work. We’ve also found that efficient tooling also helps engineers performing smaller changes. The same tools that make changing thousands of files efficient also scale down to tens of files reasonably well.

在上述各种情况下，面对谷歌这样规模的代码库，基础设施团队可能经常需要修改数十万处对旧模式或符号的引用。迄今为止，规模最大的变更已涉及数百万处引用，我们预计这套流程还能继续有效地扩展。我们发现，尽早并持续投入工具建设，让众多基础设施团队能够实施大规模变更，通常很有价值。高效的工具也能帮助工程师处理较小的变更：能够高效修改数千个文件的工具，用来修改几十个文件通常也同样合适。

> [^1]:  For some ideas about why, see Chapter 16.
>
> 1 关于其中的原因，参见第16章。
>
> [^2]:  It’s possible in this federated world to say “we’ll just commit to each repo as fast as possible to keep the duration of the build break small!” But that approach really doesn’t scale as the number of federated repositories grows.
>
> 2 在这种联邦式仓库环境中，有人可能会说：“我们尽快向每个代码仓库提交，把构建失败的时间压到最短就行了！”但随着联邦式仓库数量增加，这种方法实际上无法有效扩展。
>
> [^3]: For a further discussion about this practice, see Chapter 15.
>
> 3 关于这种做法的进一步讨论，见第15章。

## Who Deals with LSCs? 谁负责大规模变更？

As just indicated, the infrastructure teams that build and manage our systems are responsible for much of the work of performing LSCs, but the tools and resources are available across the company. If you skipped Chapter 1, you might wonder why infrastructure teams are the ones responsible for this work. Why can’t we just introduce a new class, function, or system and dictate that everybody who uses the old one move to the updated analogue? Although this might seem easier in practice, it turns out not to scale very well for several reasons.

如前所述，构建和管理系统的基础设施团队承担了大部分大规模变更工作，不过相关工具和资源向全公司开放。如果你跳过了第1章，可能会问：为什么要由基础设施团队负责？为什么不能只引入新的类、函数或系统，再要求所有旧版本的用户迁移到相应的新版本？这种做法看似更容易，但由于以下几个原因，实际上无法很好地适应规模增长。

First, the infrastructure teams that build and manage the underlying systems are also the ones with the domain knowledge required to fix the hundreds of thousands of references to them. Teams that consume the infrastructure are unlikely to have the context for handling many of these migrations, and it is globally inefficient to expect them to each relearn expertise that infrastructure teams already have. Centralization also allows for faster recovery when faced with errors because errors generally fall into a small set of categories, and the team running the migration can have a playbook—formal or informal—for addressing them.

首先，构建和管理底层系统的基础设施团队，也掌握了修改数十万处系统引用所需的领域知识。使用这些基础设施的团队通常缺少处理此类迁移所需的背景知识。要求每个团队重新学习基础设施团队已有的专业知识，从组织整体来看效率很低。集中处理还能在出错时更快恢复，因为错误通常集中在少数几类，负责迁移的团队可以准备正式或非正式的处理预案。

Consider the amount of time it takes to do the first of a series of semi-mechanical changes that you don’t understand. You probably spend some time reading about the motivation and nature of the change, find an easy example, try to follow the provided suggestions, and then try to apply that to your local code. Repeating this for every team in an organization greatly increases the overall cost of execution. By making only a few centralized teams responsible for LSCs, Google both internalizes those costs and drives them down by making it possible for the change to happen more efficiently.

设想你要完成一系列半机械式的变更，却还不理解这些变更，第一次操作会花多长时间？你可能需要先阅读资料，了解变更的动机和性质，找一个简单示例，尝试按照建议操作，再将其应用到自己负责的代码中。如果组织中的每个团队都重复这个过程，总体执行成本就会大幅增加。谷歌让少数几个团队集中负责大规模变更，既将这些成本内部化，也通过提高执行效率降低了成本。

Second, nobody likes unfunded mandates.[^4] Even though a new system might be categorically better than the one it replaces, those benefits are often diffused across an organization and thus unlikely to matter enough for individual teams to want to update on their own initiative. If the new system is important enough to migrate to, the costs of migration will be borne somewhere in the organization. Centralizing the migration and accounting for its costs is almost always faster and cheaper than depending on individual teams to organically migrate.

第二，没有人喜欢只下达任务却不给相应资源的要求。即使新系统明显优于旧系统，收益也往往分散在整个组织中，落到单个团队头上，通常不足以促使他们主动更新。如果新系统重要到值得迁移，组织中总得有人承担迁移成本。集中开展迁移并核算成本，几乎总是比依赖各团队自发迁移更快、更便宜。

Additionally, having teams that own the systems requiring LSCs helps align incentives to ensure the change gets done. In our experience, organic migrations are unlikely to fully succeed, in part because engineers tend to use existing code as examples when writing new code. Having a team that has a vested interest in removing the old system responsible for the migration effort helps ensure that it actually gets done. Although funding and staffing a team to run these kinds of migrations can seem like an additional cost, it is actually just internalizing the externalities that an unfunded mandate creates, with the additional benefits of economies of scale.

此外，让负责相关系统的团队承担大规模变更，也有助于使激励与目标一致，确保变更完成。根据我们的经验，自发迁移很难彻底完成，部分原因是工程师编写新代码时往往会参考已有代码。让一个能从移除旧系统中直接受益的团队负责迁移，有助于确保工作真正完成。为此类迁移安排专门团队并投入资金和人员，看似增加了成本，实际上只是把下达任务却不给资源所产生的外部成本内部化，还能额外获得规模经济的收益。

> [^4]:  By “unfunded mandate,” we mean “additional requirements imposed by an external entity without balancing compensation.” Sort of like when the CEO says that everybody must wear an evening gown for “formal Fridays” but doesn’t give you a corresponding raise to pay for your formal wear.
>
> 4  这里所说的“只下达任务却不给相应资源”，是指“外部主体提出额外要求，却不提供相应补偿”。这有点像 CEO 要求每个人在“正装星期五”穿晚礼服，却不给你相应加薪来支付礼服费用。

-----

##### Case Study: Filling Potholes 案例研究：填补坑洞

Although the LSC systems at Google are used for high-priority migrations, we’ve also discovered that just having them available opens up opportunities for various small fixes across our codebase, which just wouldn’t have been possible without them. Much like transportation infrastructure tasks consist of building new roads as well as repairing old ones, infrastructure groups at Google spend a lot of time fixing existing code, in addition to developing new systems and moving users to them.

谷歌的大规模变更系统用于高优先级的迁移，但我们也发现，有了这些系统，就能在整个代码库中进行各种小修小补，而这些工作原本无法开展。交通基础设施建设既包括修建新路，也包括修补旧路；同样，谷歌的基础设施团队除了开发新系统并迁移用户，还会花大量时间修复现有代码。

For example, early in our history, a template library emerged to supplement the C++ Standard Template Library. Aptly named the Google Template Library, this library consisted of several header files’ worth of implementation. For reasons lost in the mists of time, one of these header files was named *stl_util.h* and another was named *map-util.h* (note the different separators in the file names). In addition to driving the consistency purists nuts, this difference also led to reduced productivity, and engineers had to remember which file used which separator, and only discovered when they got it wrong after a potentially lengthy compile cycle.

例如，谷歌早期曾出现一个模板库，用来补充 C++ 标准模板库。它被恰如其分地命名为 Google Template Library，实现在几个头文件中。其中一个头文件叫作*stl_util.h*，另一个却叫作*map-util.h*，命名原因早已无从考证（注意两个文件名使用了不同的分隔符）。这不仅让追求一致性的人难以忍受，也降低了工作效率。工程师必须记住各文件使用哪种分隔符；一旦记错，往往要等一轮可能相当漫长的编译结束后才能发现。

Although fixing this single-character change might seem pointless, particularly across a codebase the size of Google’s, the maturity of our LSC tooling and process enabled us to do it with just a couple weeks’ worth of background-task effort. Library authors could find and apply this change en masse without having to bother end users of these files, and we were able to quantitatively reduce the number of build failures caused by this specific issue. The resulting increases in productivity (and happiness) more than paid for the time to make the change.

只改一个字符看似不值得，尤其是在谷歌这样规模的代码库中。不过，凭借成熟的大规模变更工具和流程，我们把它作为次要任务处理，只投入约两周的工作量就完成了。库的作者可以批量找出并修改所有相关位置，不必打扰这些文件的使用者。我们也确实测到了这一问题所致构建失败次数的下降。工作效率和愉悦感提升带来的收益，超过了实施变更的时间成本。

As the ability to make changes across our entire codebase has improved, the diversity of changes has also expanded, and we can make some engineering decisions knowing that they aren’t immutable in the future. Sometimes, it’s worth the effort to fill a few potholes.

随着全面修改代码库的能力增强，我们能做的变更也更加多样。作出某些工程决策时，我们知道它们将来仍可调整。有时，花些力气填补几处坑洞是值得的。

-----

## Barriers to Atomic Changes  原子变更的障碍

Before we discuss the process that Google uses to actually effect LSCs, we should talk about why many kinds of changes can’t be committed atomically. In an ideal world, all logical changes could be packaged into a single atomic commit that could be tested, reviewed, and committed independent of other changes. Unfortunately, as a repository—and the number of engineers working in it—grows, that ideal becomes less feasible. It can be completely infeasible even at small scale when using a set of distributed or federated repositories.

在讨论谷歌实施大规模变更的具体流程之前，先来看看为什么许多变更无法以原子方式提交。理想情况下，每项逻辑变更都可以打包为一次原子提交，独立于其他变更进行测试、审查和提交。然而，随着代码仓库规模和参与开发的工程师数量增加，这种理想越来越难以实现。如果使用一组分布式或联邦式代码仓库，即使规模很小，也可能完全无法做到。

### Technical Limitations  技术限制

To begin with, most Version Control Systems (VCSs) have operations that scale linearly with the size of a change. Your system might be able to handle small commits (e.g., on the order of tens of files) just fine, but might not have sufficient memory or processing power to atomically commit thousands of files at once. In centralized VCSs, commits can block other writers (and in older systems, readers) from using the system as they process, meaning that large commits stall other users of the system.

首先，大多数版本控制系统（VCS）都有一些操作，其开销会随变更规模线性增长。系统可能轻松处理小型提交，例如涉及几十个文件的提交，却没有足够的内存或处理能力，一次性以原子方式提交数千个文件。在集中式 VCS 中，提交处理期间可能阻塞其他写入者，较老的系统甚至还会阻塞读取者。这意味着大型提交会让系统的其他用户无法继续工作。

In short, it might not be just “difficult” or “unwise” to make a large change atomically: it might simply be impossible with a given infrastructure. Splitting the large change into smaller, independent chunks gets around these limitations, although it makes the execution of the change more complex.[^5]

简言之，以原子方式提交大型变更，可能不只是“困难”或“不明智”，而是在现有基础设施上根本无法实现。将大型变更拆成较小且相互独立的部分，可以绕过这些限制，但也会让执行过程更复杂。

> [^5]:  See [*https://ieeexplore.ieee.org/abstract/document/8443579*](https://ieeexplore.ieee.org/abstract/document/8443579).
>
> 5  查阅 [*https://ieeexplore.ieee.org/abstract/document/8443579*](https://ieeexplore.ieee.org/abstract/document/8443579)。

### Merge Conflicts 合并冲突

As the size of a change grows, the potential for merge conflicts also increases. Every version control system we know of requires updating and merging, potentially with manual resolution, if a newer version of a file exists in the central repository. As the number of files in a change increases, the probability of encountering a merge conflict also grows and is compounded by the number of engineers working in the repository.

变更规模越大，越容易出现合并冲突。据我们所知，所有版本控制系统在中央代码仓库中出现文件的新版本时，都要求更新并合并，有时还需要手动解决冲突。变更涉及的文件越多，发生合并冲突的概率就越高；同时在仓库中工作的工程师越多，这个问题也越严重。

If your company is small, you might be able to sneak in a change that touches every file in the repository on a weekend when nobody is doing development. Or you might have an informal system of grabbing the global repository lock by passing a virtual (or even physical!) token around your development team. At a large, global company like Google, these approaches are just not feasible: somebody is always making changes to the repository.

如果公司很小，你或许可以趁周末没人开发时，提交一项涉及仓库中所有文件的变更。也可以采用非正式的约定，在开发团队中传递一个虚拟令牌，甚至是实物令牌，借此获取仓库的全局锁。但在谷歌这样业务遍布全球的大公司，这些办法都不可行，因为始终有人在修改代码仓库。

With few files in a change, the probability of merge conflicts shrinks, so they are more likely to be committed without problems. This property also holds for the following areas as well.

一项变更涉及的文件越少，发生合并冲突的概率就越低，也就越容易顺利提交。下面几个方面同样体现了小型变更的优势。

### No Haunted Graveyards  不留闹鬼的墓地

The SREs who run Google’s production services have a mantra: “No Haunted Graveyards.” A haunted graveyard in this sense is a system that is so ancient, obtuse, or complex that no one dares enter it. Haunted graveyards are often business-critical systems that are frozen in time because any attempt to change them could cause the system to fail in incomprehensible ways, costing the business real money. They pose a real existential risk and can consume an inordinate amount of resources.

负责谷歌生产服务的 SRE 有一句格言：“不留闹鬼的墓地。”这里的“闹鬼的墓地”，指的是过于老旧、晦涩或复杂，以至于无人敢碰的系统。这些系统往往对业务至关重要，却长期停滞不变，因为任何修改都可能让系统以难以理解的方式发生故障，给企业造成实际损失。它们确实可能危及企业生存，也可能消耗大量不成比例的资源。

Haunted graveyards don’t just exist in production systems, however; they can be found in codebases. Many organizations have bits of software that are old and unmaintained, written by someone long off the team, and on the critical path of some important revenue-generating functionality. These systems are also frozen in time, with layers of bureaucracy built up to prevent changes that might cause instability. Nobody wants to be the network support engineer II who flipped the wrong bit!

不过，“闹鬼的墓地”不仅存在于生产系统中，也存在于代码库里。许多组织都有一些老旧且无人维护的软件，作者早已离开团队，而软件仍处在某些重要创收功能的关键路径上。这些系统同样长期停滞不变，周围设置了层层审批手续，以阻止可能引发不稳定的变更。谁也不想成为那个改错一个比特的二级网络支持工程师！

These parts of a codebase are anathema to the LSC process because they prevent the completion of large migrations, the decommissioning of other systems upon which they rely, or the upgrade of compilers or libraries that they use. From an LSC perspective, haunted graveyards prevent all kinds of meaningful progress.

代码库中的这些部分，是大规模变更流程的重大障碍：它们使大型迁移无法完成，让其所依赖的其他系统无法退役，也妨碍所用编译器或库的升级。从大规模变更的角度看，“闹鬼的墓地”阻碍了各种有意义的改进。

At Google, we’ve found the counter to this to be good, old-fashioned  testing. When software is thoroughly tested, we can make arbitrary changes to it and know with confidence whether those changes are breaking, no matter the age or complexity of the system. Writing those tests takes a lot of effort, but it allows a codebase like Google’s to evolve over long periods of time, consigning the notion of haunted software graveyards to a graveyard of its own.

在谷歌，我们发现，应对这个问题靠的还是行之有效的老办法：测试。只要软件经过充分测试，无论系统多老、多复杂，我们都可以对其进行各种修改，并有把握地判断变更是否破坏了现有功能。编写这些测试需要投入大量精力，但也正因如此，谷歌这样的代码库才能长期演进，让“闹鬼的软件墓地”这一概念本身成为历史。

### Heterogeneity  异质性

LSCs really work only when the bulk of the effort for them can be done by computers, not humans. As good as humans can be with ambiguity, computers rely upon consistent environments to apply the proper code transformations to the correct places. If your organization has many different VCSs, Continuous Integration (CI) systems, project-specific tooling, or formatting guidelines, it is difficult to make sweeping changes across your entire codebase. Simplifying the environment to add more consistency will help both the humans who need to move around in it and the robots making automated transformations.

只有将大部分工作交给计算机，而不是人工完成，大规模变更才能真正发挥作用。人善于处理模糊情形，计算机却需要一致的环境，才能在正确的位置应用正确的代码转换。如果组织内并存多种 VCS、持续集成（CI）系统、项目专用工具或格式规范，就很难全面修改代码库。简化环境、提高一致性，既有助于需要在不同项目间工作的人，也有助于执行自动转换的程序。

For example, many projects at Google have presubmit tests configured to run before changes are made to their codebase. Those checks can be very complex, ranging from checking new dependencies against a whitelist, to running tests, to ensuring that the change has an associated bug. Many of these checks are relevant for teams writing new features, but for LSCs, they just add additional irrelevant complexity.

例如，谷歌的许多项目配置了提交前测试，在变更进入代码库之前运行。检查内容可能相当复杂，包括对照白名单核查新增依赖、运行测试，以及确认变更关联了缺陷记录等。其中许多检查对开发新功能的团队有用，但对大规模变更而言，只会增加与任务无关的复杂性。

We’ve decided to embrace some of this complexity, such as running presubmit tests, by making it standard across our codebase. For other inconsistencies, we advise teams to omit their special checks when parts of LSCs touch their project code. Most teams are happy to help given the benefit these kinds of changes are to their projects.

我们选择接受其中一部分复杂性，例如运行提交前测试，并将其纳入整个代码库的标准流程。对于其他不一致之处，我们建议团队在大规模变更涉及其项目代码时，跳过各自的特殊检查。考虑到这类变更对项目的益处，大多数团队都乐于配合。

### Testing  测试

Every change should be tested (a process we’ll talk about more in just a moment), but the larger the change, the more difficult it is to actually test it appropriately. Google’s CI system will run not only the tests immediately impacted by a change, but also any tests that transitively depend on the changed files.[^6] This means a change gets broad coverage, but we’ve also observed that the farther away in the dependency graph a test is from the impacted files, the more unlikely a failure is to have been caused by the change itself.

每项变更都应该经过测试，稍后我们会详细讨论这个过程。不过，变更越大，就越难进行恰当的测试。谷歌的 CI 系统不仅运行直接受变更影响的测试，还会运行所有通过传递依赖关联到修改文件的测试。这让变更获得了广泛的测试覆盖。但我们也观察到，在依赖图中，测试距离修改文件越远，其失败就越不可能由这次变更本身引起。

Small, independent changes are easier to validate, because each of them affects a smaller set of tests, but also because test failures are easier to diagnose and fix. Finding the root cause of a test failure in a change of 25 files is pretty straightforward; finding 1 in a 10,000-file change is like the proverbial needle in a haystack.

小而独立的变更更容易验证，不仅因为每项变更影响的测试较少，也因为测试失败后更容易诊断和修复。在涉及25个文件的变更中查找测试失败的根因，通常相当直接；换成涉及10,000个文件的变更，就如同大海捞针。

The trade-off in this decision is that smaller changes will cause the same tests to be run multiple times, particularly tests that depend on large parts of the codebase. Because engineer time spent tracking down test failures is much more expensive than the compute time required to run these extra tests, we’ve made the conscious decision that this is a trade-off we’re willing to make. That same trade-off might not hold for all organizations, but it is worth examining what the proper balance is for yours.

这样做的代价是，同一项测试会随着多项小型变更反复运行，尤其是那些依赖代码库中大量代码的测试。不过，工程师排查测试失败所花的时间，远比额外运行这些测试所需的计算时间昂贵，因此我们明确选择了这一取舍。它未必适合所有组织，但值得思考你的组织应当如何平衡这两类成本。

> [^6]:  This probably sounds like overkill, and it likely is. We’re doing active research on the best way to determine the “right” set of tests for a given change, balancing the cost of compute time to run the tests, and the human cost of making the wrong choice.
>
> 6 这听起来可能有些过度，而且很可能确实如此。我们正在积极研究如何为给定变更确定“恰当”的测试集，在运行测试所需的计算时间成本与选错测试集带来的人力成本之间取得平衡。

-----

##### Case Study: Testing LSCs  案例研究：测试大规模变更

***Adam Bender***

Today it is common for a double-digit percentage (10% to 20%) of the changes in a project to be the result of LSCs, meaning a substantial amount of code is changed in projects by people whose full-time job is unrelated to those projects. Without good tests, such work would be impossible, and Google’s codebase would quickly atrophy under its own weight. LSCs enable us to systematically migrate our entire codebase to newer APIs, deprecate older APIs, change language versions, and remove popular but dangerous practices.

如今，一个项目中有两位数百分比的变更，通常为10%到20%，来自大规模变更，已是常见现象。这意味着项目中的大量代码由本职工作与该项目无关的人修改。没有良好的测试，这项工作就无法开展，谷歌的代码库也会因规模带来的负担而迅速退化。大规模变更让我们能够有系统地将整个代码库迁移到新 API、弃用旧 API、更换语言版本，并消除常见却危险的做法。

Even a simple one-line signature change becomes complicated when made in a thousand different places across hundreds of different products and services.[^7] After the change is written, you need to coordinate code reviews across dozens of teams. Lastly, after reviews are approved, you need to run as many tests as you can to be sure the change is safe.[^8] We say “as many as you can,” because a good-sized LSC could trigger a rerun of every single test at Google, and that can take a while. In fact, many LSCs have to plan time to catch downstream clients whose code backslides while the LSC makes its way through the process.

即使只是修改一行函数签名，一旦涉及数百个产品和服务中的上千处位置，也会变得复杂。完成代码修改后，需要协调数十个团队进行代码审查。审查通过后，还要运行尽可能多的测试，确保变更安全。之所以说“尽可能多”，是因为一次规模较大的大规模变更可能触发谷歌所有测试重新运行，而这需要不少时间。实际上，许多大规模变更还必须预留时间，处理迁移推进期间下游用户重新引入旧用法的代码。

Testing an LSC can be a slow and frustrating process. When a change is sufficiently large, your local environment is almost guaranteed to be permanently out of sync with head as the codebase shifts like sand around your work. In such circumstances, it is easy to find yourself running and rerunning tests just to ensure your changes continue to be valid. When a project has flaky tests or is missing unit test coverage, it can require a lot of manual intervention and slow down the entire process. To help speed things up, we use a strategy called the TAP (Test Automation Platform) train.

测试大规模变更可能既缓慢又令人沮丧。当变更足够大时，周围的代码库不断变化，本地环境几乎注定会一直落后于最新版本 head。在这种情况下，你很容易陷入反复运行测试的循环，只为确认自己的变更仍然有效。如果项目存在不稳定测试，或缺少单元测试覆盖，就可能需要大量人工干预，拖慢整个流程。为加快进度，我们采用了一种称为“TAP（测试自动化平台）列车”的策略。

**Riding the TAP Train**  **搭乘TAP列车**

The core insight to LSCs is that they rarely interact with one another, and most affected tests are going to pass for most LSCs. As a result, we can test more than one change at a time and reduce the total number of tests executed. The train model has proven to be very effective for testing LSCs.

关于大规模变更，一个关键认识是：不同变更很少相互影响，而且对于大多数变更，大多数受影响的测试都会通过。因此，可以同时测试多项变更，减少测试执行总次数。实践证明，列车模型对测试大规模变更非常有效。

The TAP train takes advantage of two facts:

- LSCs tend to be pure refactorings and therefore very narrow in scope, preserving local semantics.
- Individual changes are often simpler and highly scrutinized, so they are correct  more often than not.

TAP列车利用了两个事实：

- 大规模变更往往是纯粹的重构，因此改动范围很窄，并保持局部语义不变。
- 单项变更通常较简单，而且经过严格审查，因此大多是正确的。

The train model also has the advantage that it works for multiple changes at the same time and doesn’t require that each individual change ride in isolation.[^9]

列车模型还有一个优点：可以同时处理多项变更，不必让每项变更单独“乘车”。

The train has five steps and is started fresh every three hours:

1. For each change on the train, run a sample of 1,000 randomly-selected tests.
2. Gather up all the changes that passed their 1,000 tests and create one uberchange from all of them: “the train.”
3. Run the union of all tests directly affected by the group of changes. Given a large enough (or low-level enough) LSC, this can mean running every single test in Google’s repository. This process can take more than six hours to complete.
4. For each nonflaky test that fails, rerun it individually against each change that made it into the train to determine which changes caused it to fail.
5. TAP generates a report for each change that boarded the train. The report describes all passing and failing targets and can be used as evidence that an LSC is safe to submit.

列车流程包含五个步骤，每三小时启动一趟新列车：

1. 对列车上的每项变更，随机抽取1000个测试运行。
2. 汇集所有通过各自1000个测试的变更，将它们组合成一项超级变更，也就是“列车”。
3. 运行直接受这组变更影响的所有测试的并集。如果大规模变更涉及的范围够广，或足够底层，就可能需要运行谷歌代码仓库中的每一项测试。这一步可能需要六个多小时才能完成。
4. 对于每个失败且不属于不稳定测试的测试，分别针对列车中的每项变更重新运行，以确定哪些变更导致了失败。
5. TAP 为每项“上车”的变更生成一份报告，列出所有通过和失败的测试目标，作为大规模变更可以安全提交的证据。

-----

> [^7]: The largest series of LSCs ever executed removed more than one billion lines of code from the repository over the course of three days. This was largely to remove an obsolete part of the repository that had been migrated to a new home; but still, how confident do you have to be to delete one billion lines of code?
>
> 7 迄今实施过的最大一组大规模变更，在三天内从代码仓库中删除了超过10亿行代码。这主要是清除已迁往新位置的过时部分；即便如此，要删除10亿行代码，也得有多大的把握才行？
>  
> [^8]: LSCs are usually supported by tools that make finding, making, and reviewing changes relatively straightforward.
>
> 8 大规模变更通常有工具支持，使查找修改位置、生成变更和审查变更都相对直接。
>
> [^9]: It is possible to ask TAP for single change “isolated” run, but these are very expensive and are performed only during off-peak hours.
>
> 9 可以要求 TAP 针对单项变更进行“隔离”运行，但成本很高，因此只在非高峰时段执行。

### Code Review 代码审查

Finally, as we mentioned in Chapter 9, all changes need to be reviewed before submission, and this policy applies even for LSCs. Reviewing large commits can be tedious, onerous, and even error prone, particularly if the changes are generated by hand (a process you want to avoid, as we’ll discuss shortly). In just a moment, we’ll look at how tooling can often help in this space, but for some classes of changes, we still want humans to explicitly verify they are correct. Breaking an LSC into separate shards makes this much easier.

最后，正如第9章所述，所有变更都需要在提交前经过审查，大规模变更也不例外。审查大型提交可能枯燥、繁重，还容易出错，尤其是变更由人工生成时。稍后会说明为什么应尽量避免手工生成变更，以及工具如何帮助审查。不过，对于某些类型的变更，我们仍然需要人工明确确认其正确性。将大规模变更拆成独立分片，会让这项工作容易得多。

-----

##### Case Study: scoped_ptr to std::unique_ptr  案例研究：从 scoped_ptr 到 std::unique_ptr

Since its earliest days, Google’s C++ codebase has had a self-destructing smart pointer for wrapping heap-allocated C++ objects and ensuring that they are destroyed when the smart pointer goes out of scope. This type was called scoped_ptr and was used extensively throughout Google’s codebase to ensure that object lifetimes were appropriately managed. It wasn’t perfect, but given the limitations of the then-current C++ standard (C++98) when the type was first introduced, it made for safer programs.

谷歌的 C++ 代码库很早就有一种会自动析构的智能指针，用来包装在堆上分配的 C++ 对象，并确保智能指针离开作用域时销毁这些对象。这种类型叫作 scoped_ptr，在谷歌代码库中广泛使用，用于正确管理对象的生命周期。它并不完美，但考虑到最初引入时 C++98 标准的限制，已经能让程序更加安全。

In C++11, the language introduced a new type: std::unique_ptr. It fulfilled the same function as scoped_ptr, but also prevented other classes of bugs that the language now could detect. std::unique_ptr was strictly better than scoped_ptr, yet Google’s codebase had more than 500,000 references to scoped_ptr scattered among millions of source files. Moving to the more modern type required the largest LSC attempted to that point within Google.

C++11 引入了新类型 std::unique_ptr。它实现了与 scoped_ptr 相同的功能，还能防止此时语言已能检测到的其他类别的缺陷。std::unique_ptr 明确优于 scoped_ptr，但谷歌代码库中有超过50万处对 scoped_ptr 的引用，散布在数百万个源文件中。迁移到这个更现代的类型，需要开展谷歌当时尝试过的最大规模变更。

Over the course of several months, several engineers attacked the problem in parallel. Using Google’s large-scale migration infrastructure, we were able to change references to scoped_ptr into references to std::unique_ptr as well as slowly adapt scoped_ptr to behave more closely to std::unique_ptr. At the height of the migration process, we were consistently generating, testing and committing more than 700 independent changes, touching more than 15,000 files *per day*. Today, we sometimes manage 10 times that throughput, having refined our practices and improved our tooling.

几位工程师并行投入这项工作，持续了数月。借助谷歌的大规模迁移基础设施，我们将 scoped_ptr 的引用改为 std::unique_ptr，同时逐步调整 scoped_ptr，使其行为更接近 std::unique_ptr。在迁移高峰期，我们持续以*每天*超过700项独立变更的速度生成、测试并提交修改，涉及超过15,000个文件。如今，随着实践完善、工具改进，我们有时能达到当时10倍的吞吐量。

Like almost all LSCs, this one had a very long tail of tracking down various nuanced behavior dependencies (another manifestation of Hyrum’s Law), fighting race conditions with other engineers, and uses in generated code that weren’t detectable by our automated tooling. We continued to work on these manually as they were discovered by the testing infrastructure.

和几乎所有大规模变更一样，这次迁移也有漫长的收尾工作：追查对各种细微行为的依赖，这是海勒姆定律的又一体现；处理与其他工程师并行修改引发的竞态；以及查找生成代码中自动化工具无法检测到的用法。随着测试基础设施陆续发现这些问题，我们继续手动处理。

scoped_ptr was also used as a parameter type in some widely used APIs, which made small independent changes difficult. We contemplated writing a call-graph analysis system that could change an API and its callers, transitively, in one commit, but were concerned that the resulting changes would themselves be too large to commit atomically.

一些广泛使用的 API 还将 scoped_ptr 用作参数类型，这使小而独立的变更难以实施。我们考虑过编写调用图分析系统，在一次提交中修改 API，并沿调用关系递归修改所有调用方，但担心由此产生的变更本身太大，无法以原子方式提交。

In the end, we were able to finally remove scoped_ptr by first making it a type alias of std::unique_ptr and then performing the textual substitution between the old alias and the new, before eventually just removing the old scoped_ptr alias. Today, Google’s codebase benefits from using the same standard type as the rest of the C++ ecosystem, which was possible only because of our technology and tooling for LSCs.

最终，我们先将 scoped_ptr 改为 std::unique_ptr 的类型别名，再通过文本替换将旧名称改为新名称，最后删除旧的 scoped_ptr 别名，完成了迁移。如今，谷歌代码库得以使用与 C++ 生态系统其他项目相同的标准类型，并从中受益。这离不开我们的大规模变更技术和工具。

-----

## LSC Infrastructure  LSC基础设施

Google has invested in a significant amount of infrastructure to make LSCs possible. This infrastructure includes tooling for change creation, change management, change review, and testing. However, perhaps the most important support for LSCs has been the evolution of cultural norms around large-scale changes and the oversight given to them. Although the sets of technical and social tools might differ for your organization, the general principles should be the same.

谷歌投入了大量资源建设基础设施，使大规模变更成为可能，其中包括创建、管理、审查和测试变更的工具。不过，最重要的支撑或许是与大规模变更相关的文化规范逐渐演变，以及对这些变更的监督。你的组织所用的技术工具和协作机制可能不同，但基本原则应当相通。

### Policies and Culture  策略和文化

As we’ve described in Chapter 16, Google stores the bulk of its source code in a single monolithic repository (monorepo), and every engineer has visibility into almost all of this code. This high degree of openness means that any engineer can edit any file and send those edits for review to those who can approve them. However, each of those edits has costs, both to generate as well as review.[^10]

如第16章所述，谷歌将大部分源代码存储在一个单体代码仓库（monorepo）中，每位工程师几乎都能查看其中的全部代码。这种高度开放意味着，任何工程师都可以修改任何文件，再将变更交给有批准权限的人审查。不过，每次修改都有成本，生成和审查变更都需要投入。

Historically, these costs have been somewhat symmetric, which limited the scope of changes a single engineer or team could generate. As Google’s LSC tooling improved, it became easier to generate a large number of changes very cheaply, and it became equally easy for a single engineer to impose a burden on a large number of reviewers across the company. Even though we want to encourage widespread improvements to our codebase, we want to make sure there is some oversight and thoughtfulness behind them, rather than indiscriminate tweaking.[^11]

过去，生成与审查变更的成本大致相当，这限制了单个工程师或团队能够生成的变更范围。随着谷歌的大规模变更工具不断改进，以极低成本生成大量变更越来越容易，一个工程师也就很容易给全公司的大量审查者带来负担。我们希望鼓励对代码库进行广泛改进，但也希望这些工作经过监督和审慎考虑，而不是随意修改。

The end result is a lightweight approval process for teams and individuals seeking to make LSCs across Google. This process is overseen by a group of experienced engineers who are familiar with the nuances of various languages, as well as invited domain experts for the particular change in question. The goal of this process is not to prohibit LSCs, but to help change authors produce the best possible changes, which make the most use of Google’s technical and human capital. Occasionally, this group might suggest that a cleanup just isn’t worth it: for example, cleaning up a common typo without any way of preventing recurrence.

因此，我们为计划在谷歌开展大规模变更的团队和个人建立了轻量级审批流程。流程由一组熟悉各种语言细节的资深工程师，以及针对具体变更邀请的领域专家共同监督。目的不是阻止大规模变更，而是帮助作者尽可能提高变更质量，充分利用谷歌的技术和人力资源。有时，这个小组也会指出某项清理不值得做，例如修正常见的拼写错误，却没有办法防止它再次出现。

Related to these policies was a shift in cultural norms surrounding LSCs. Although it is important for code owners to have a sense of responsibility for their software, they also needed to learn that LSCs were an important part of Google’s effort to scale our software engineering practices. Just as product teams are the most familiar with their own software, library infrastructure teams know the nuances of the infrastructure, and getting product teams to trust that domain expertise is an important step toward social acceptance of LSCs. As a result of this culture shift, local product teams have grown to trust LSC authors to make changes relevant to those authors’ domains.

伴随这些策略的，是围绕大规模变更的文化规范转变。代码所有者应对自己的软件负责，但也需要认识到，大规模变更是谷歌推动软件工程实践适应规模增长的重要手段。产品团队最熟悉自己的软件，基础库团队则最了解基础设施的细节。让产品团队信任这些专业知识，是大规模变更获得组织认可的重要一步。随着文化转变，各产品团队逐渐愿意信任大规模变更的作者，让他们在各自的专业领域内修改代码。

Occasionally, local owners question the purpose of a specific commit being made as part of a broader LSC, and change authors respond to these comments just as they would other review comments. Socially, it’s important that code owners understand the changes happening to their software, but they also have come to realize that they don’t hold a veto over the broader LSC. Over time, we’ve found that a good FAQ and a solid historic track record of improvements have generated widespread endorsement of LSCs throughout Google.

有时，项目的代码所有者会质疑大规模变更中某次具体提交的目的，变更作者会像回应其他代码审查意见一样作出解释。从协作角度看，代码所有者需要了解自己的软件正在发生哪些变化，但也逐渐认识到，自己并不拥有对整个大规模变更的否决权。我们发现，完善的常见问题解答（FAQ），加上长期积累的可靠改进记录，让大规模变更逐渐在谷歌获得了广泛支持。

> [^10]:  There are obvious technical costs here in terms of compute and storage, but the human costs in time to review a change far outweigh the technical ones.
>
> 10  这里显然涉及计算和存储方面的技术成本，但审查变更所花时间对应的人力成本，远高于这些技术成本。
>
> [^11]:   For example, we do not want the resulting tools to be used as a mechanism to fight over the proper spelling of “gray” or “grey” in comments.
>
> 11  例如，我们不希望这些工具被用来争论注释中应该写“gray”还是“grey”。

### Codebase Insight  深入了解代码库

To do LSCs, we’ve found it invaluable to be able to do large-scale analysis of our codebase, both on a textual level using traditional tools, as well as on a semantic level. For example, Google’s use of the semantic indexing tool [Kythe](https://kythe.io/)provides a complete map of the links between parts of our codebase, allowing us to ask questions such as “Where are the callers of this function?” or “Which classes derive from this one?” Kythe and similar tools also provide programmatic access to their data so that they can be incorporated into refactoring tools. (For further examples, see Chapters 17 and 20.)

我们发现，实施大规模变更时，对代码库进行大范围分析的能力至关重要，既包括使用传统工具进行文本分析，也包括语义分析。例如，谷歌使用的语义索引工具 Kythe 能完整呈现代码库各部分之间的关联，从而回答“这个函数的调用方在哪里？”或“哪些类派生自这个类？”等问题。Kythe 及类似工具还允许通过程序访问其数据，便于集成到重构工具中。（更多示例参见第17章和第20章。）

We also use compiler-based indices to run abstract syntax tree-based analysis and transformations over our codebase. Tools such as [ClangMR](https://oreil.ly/c6xvO), JavacFlume, or [Refaster](https://oreil.ly/Er03J), which can perform transformations in a highly parallelizable way, depend on these insights as part of their function. For smaller changes, authors can use specialized, custom tools, perl or sed, regular expression matching, or even a simple shell script.

我们还使用基于编译器的索引，对代码库执行基于抽象语法树的分析和转换。[ClangMR](https://oreil.ly/c6xvO)、JavacFlume 或 [Refaster](https://oreil.ly/Er03J) 等工具能够高度并行地执行转换，其部分功能就依赖于这些分析信息。对于较小的变更，作者可以使用专门定制的工具、perl 或 sed、正则表达式匹配，甚至简单的 shell 脚本。

Whatever tool your organization uses for change creation, it’s important that its human effort scale sublinearly with the codebase; in other words, it should take roughly the same amount of human time to generate the collection of all required changes, no matter the size of the repository. The change creation tooling should also be comprehensive across the codebase, so that an author can be assured that their change covers all of the cases they’re trying to fix.

无论组织使用什么工具生成变更，关键是所需的人力投入应随代码库规模呈次线性增长。换句话说，无论仓库有多大，生成全部所需变更花费的人力时间都应大致相同。变更生成工具还应覆盖整个代码库，让作者能够确信，变更已包含所有需要修复的情况。

As with other areas in this book, an early investment in tooling usually pays off in the short to medium term. As a rule of thumb, we’ve long held that if a change requires more than 500 edits, it’s usually more efficient for an engineer to learn and execute our change-generation tools rather than manually execute that edit. For experienced “code janitors,” that number is often much smaller.

与本书讨论的其他领域一样，尽早投入工具建设，通常在中短期内就能获得回报。我们一直采用一条经验准则：如果一项变更需要修改500处以上，工程师学习并使用变更生成工具，通常比手工修改更高效。对于有经验的“代码清洁工”，这个门槛往往低得多。

### Change Management  变更管理

Arguably the most important piece of large-scale change infrastructure is the set of tooling that shards a master change into smaller pieces and manages the process of testing, mailing, reviewing, and committing them independently. At Google, this tool is called Rosie, and we discuss its use more completely in a few moments when we examine our LSC process. In many respects, Rosie is not just a tool, but an entire platform for making LSCs at Google scale. It provides the ability to split the large sets of comprehensive changes produced by tooling into smaller shards, which can be tested, reviewed, and submitted independently.

大规模变更基础设施中最重要的部分，可以说是这样一套工具：它将总变更拆成较小的分片，并分别管理各分片的测试、邮件送审、审查和提交。在谷歌，这个工具叫作 Rosie；稍后介绍大规模变更流程时，会更详细地讨论它的用法。从许多方面看，Rosie 不只是工具，而是支持谷歌这种规模的大规模变更平台。它将工具生成的完整大型变更集拆成小分片，让每个分片都能独立测试、审查和提交。

### Testing  测试

Testing is another important piece of large-scale-change–enabling infrastructure. As discussed in Chapter 11, tests are one of the important ways that we validate our software will behave as expected. This is particularly important when applying changes that are not authored by humans. A robust testing culture and infrastructure means that other tooling can be confident that these changes don’t have unintended effects.

测试是支撑大规模变更的另一项重要基础设施。如第11章所述，测试是验证软件行为符合预期的重要方式之一，对非人工编写的变更尤其如此。健全的测试文化和基础设施，能为其他工具提供依据，确认这些变更不会带来意外影响。

Google’s testing strategy for LSCs differs slightly from that of normal changes while still using the same underlying CI infrastructure. Testing LSCs means not just ensuring the large master change doesn’t cause failures, but that each shard can be submitted safely and independently. Because each shard can contain arbitrary files, we don’t use the standard project-based presubmit tests. Instead, we run each shard over the transitive closure of every test it might affect, which we discussed earlier.

谷歌对大规模变更采用的测试策略与普通变更略有不同，但底层使用同一套 CI 基础设施。测试不仅要确保总变更不会导致失败，还要确保每个分片都能安全、独立地提交。每个分片可能包含任意文件，因此我们不使用标准的按项目组织的提交前测试，而是像前面所述，针对每个分片运行其可能影响的测试的传递闭包。

### Language Support  编程语言支持

LSCs at Google are typically done on a per-language basis, and some languages support them much more easily than others. We’ve found that language features such as type aliasing and forwarding functions are invaluable for allowing existing users to continue to function while we introduce new systems and migrate users to them nonatomically. For languages that lack these features, it is often difficult to migrate systems incrementally.[^12]

谷歌的大规模变更通常按编程语言分别开展，有些语言比其他语言更容易支持这类工作。我们发现，类型别名和转发函数等语言特性十分重要：它们让我们能在引入新系统、以非原子方式迁移用户的同时，保证现有用户的代码继续正常工作。缺少这些特性的语言，通常很难支持系统的增量迁移。

We’ve also found that statically typed languages are much easier to perform large automated changes in than dynamically typed languages. Compiler-based tools along with strong static analysis provide a significant amount of information that we can use to build tools to affect LSCs and reject invalid transformations before they even get to the testing phase. The unfortunate result of this is that languages like Python, Ruby, and JavaScript that are dynamically typed are extra difficult for maintainers. Language choice is, in many respects, intimately tied to the question of code lifespan: languages that tend to be viewed as more focused on developer productivity tend to be more difficult to maintain. Although this isn’t an intrinsic design requirement, it is where the current state of the art happens to be.

我们还发现，在静态类型语言中实施大规模自动变更，远比动态类型语言容易。基于编译器的工具和强大的静态分析能提供大量信息，我们据此构建大规模变更工具，在无效转换进入测试阶段之前就将其排除。遗憾的是，这意味着 Python、Ruby 和 JavaScript 等动态类型语言会给维护者带来额外困难。语言选择与代码的预期使用寿命密切相关：通常被认为更注重开发者生产力的语言，往往更难维护。这并非语言设计必然如此，而是目前技术发展所处的状态。

Finally, it’s worth pointing out that automatic language formatters are a crucial part of the LSC infrastructure. Because we work toward optimizing our code for readability, we want to make sure that any changes produced by automated tooling are intelligible to both immediate reviewers and future readers of the code. All of the LSCgeneration tools run the automated formatter appropriate to the language being changed as a separate pass so that the change-specific tooling does not need to concern itself with formatting specifics. Applying automated formatting, such as [google-java-format](https://github.com/google/google-java-format)or [clang-format](https://clang.llvm.org/docs/ClangFormat.html), to our codebase means that automatically produced changes will “fit in” with code written by a human, reducing future development friction. Without automated formatting, large-scale automated changes would never have become the accepted status quo at Google.

最后，自动代码格式化工具也是大规模变更基础设施的关键组成部分。我们重视代码的可读性，希望自动生成的变更既便于当前的审查者理解，也便于未来的代码读者阅读。所有大规模变更生成工具都会在单独的处理步骤中，运行相应语言的自动格式化工具，让负责具体变更的工具不必处理格式细节。对代码库使用 [google-java-format](https://github.com/google/google-java-format) 或 [clang-format](https://clang.llvm.org/docs/ClangFormat.html) 等自动格式化工具，可以让自动生成的变更与人工编写的代码风格一致，减少今后开发中的阻力。没有自动格式化，大规模自动变更就不可能成为谷歌广泛接受的常规做法。

> [^12]:   In fact, Go recently introduced these kinds of language features specifically to support large-scale refactorings （ see [https://talks.golang.org/2016/refactor.article](https://talks.golang.org/2016/refactor.article) ）.
>
> 12  事实上，Go 最近就专门引入了这类语言特性，以支持大规模重构（参见`https://talks.golang.org/2016/refactor.article`）。

-----

##### Case Study: Operation RoseHub  案例研究： Operation RoseHub 

LSCs have become a large part of Google’s internal culture, but they are starting to have implications in the broader world. Perhaps the best known case so far was “[Operation RoseHub](https://oreil.ly/txtDj).”

大规模变更已成为谷歌内部文化的重要组成部分，也开始对外部世界产生影响。迄今最知名的案例，或许就是“Operation RoseHub”。

In early 2017, a vulnerability in the Apache Commons library allowed any Java application with a vulnerable version of the library in its transitive classpath to become susceptible to remote execution. This bug became known as the Mad Gadget. Among other things, it allowed an avaricious hacker to encrypt the San Francisco Municipal Transportation Agency’s systems and shut down its operations. Because the only requirement for the vulnerability was having the wrong library somewhere in its classpath, anything that depended on even one of many open source projects on GitHub was vulnerable.

2017年初，Apache Commons 库中的一个漏洞，使任何在传递依赖的类路径中包含该库受影响版本的 Java 应用程序，都可能遭到远程代码执行攻击。这个漏洞被称为 Mad Gadget。它造成的后果之一，是一名贪图钱财的黑客得以加密旧金山市交通局的系统，导致其停止运作。只要类路径中的某处包含有漏洞的库，就满足了受影响的条件。因此，GitHub 上许多开源项目都可能成为风险来源，应用程序哪怕只依赖其中一个，也会受到威胁。

To solve this problem, some enterprising Googlers launched their own version of the LSC process. By using tools such as [BigQuery](https://cloud.google.com/bigquery), volunteers identified affected projects and sent more than 2,600 patches to upgrade their versions of the Commons library to one that addressed Mad Gadget. Instead of automated tools managing the process, more than 50 humans made this LSC work.

为解决这个问题，一些积极行动的谷歌员工开展了他们自己的大规模变更流程。志愿者使用 [BigQuery](https://cloud.google.com/bigquery) 等工具找出受影响的项目，提交了2600多个补丁，将这些项目使用的 Commons 库升级到修复了 Mad Gadget 的版本。这次流程没有由自动化工具管理，而是靠50多名志愿者完成了大规模变更。

-----

## The LSC Process  LSC过程

With these pieces of infrastructure in place, we can now talk about the process for actually making an LSC. This roughly breaks down into four phases (with very nebulous boundaries between them):

1. Authorization
2. Change creation
3. Shard management
4. Cleanup

有了这些基础设施，就可以进一步讨论实施大规模变更的具体流程。整个流程大致分为四个阶段，各阶段之间并没有严格界限：

1. 授权
2. 变更创建
3. 分片管理
4. 清理

Typically, these steps happen after a new system, class, or function has been written, but it’s important to keep them in mind during the design of the new system. At Google, we aim to design successor systems with a migration path from older systems in mind, so that system maintainers can move their users to the new system automatically.

这些步骤通常在新系统、类或函数编写完成后才开始，但设计新系统时就应将它们纳入考虑。在谷歌，我们力求在设计替代系统时就规划好从旧系统迁移的路径，让系统维护者能够自动将用户迁移到新系统。

### Authorization  授权

We ask potential authors to fill out a brief document explaining the reason for a proposed change, its estimated impact across the codebase (i.e., how many smaller shards the large change would generate), and answers to any questions potential reviewers might have. This process also forces authors to think about how they will describe the change to an engineer unfamiliar with it in the form of an FAQ and proposed change description. Authors also get “domain review” from the owners of the API being refactored.

我们要求计划实施变更的作者填写一份简短文档，说明变更原因、预计对整个代码库的影响，也就是会拆出多少个小分片，并回答审查者可能提出的问题。这也促使作者思考，如何通过常见问题解答和拟定的变更描述，向不了解这项工作的工程师解释变更。此外，作者还要请待重构 API 的所有者进行“领域审查”。

This proposal is then forwarded to an email list with about a dozen people who have oversight over the entire process. After discussion, the committee gives feedback on how to move forward. For example, one of the most common changes made by the committee is to direct all of the code reviews for an LSC to go to a single “global approver.” Many first-time LSC authors tend to assume that local project owners should review everything, but for most mechanical LSCs, it’s cheaper to have a single expert understand the nature of the change and build automation around reviewing it properly.

接着，提案会转发到一个约有十几名成员的邮件列表，这些成员负责监督整个流程。委员会讨论后，就后续推进方式给出反馈。例如，常见的调整之一，是让同一位“全局审批人”负责某项大规模变更的全部代码审查。许多初次实施大规模变更的作者以为，所有修改都应交给各项目的代码所有者审查。但对于大多数机械式的大规模变更，让一位专家理解变更性质，再建立相应的自动化审查手段，成本更低。

After the change is approved, the author can move forward in getting their change submitted. Historically, the committee has been very liberal with their approval,[^13] and often gives approval not just for a specific change, but also for a broad set of related changes. Committee members can, at their discretion, fast-track obvious changes without the need for full deliberation.

变更获批后，作者就可以继续推进提交工作。过去，委员会的审批一直较为宽松，而且往往不只批准某一项变更，还会一并批准一大类相关变更。对于显然可行的变更，委员会成员可以酌情快速批准，不必经过完整审议。

The intent of this process is to provide oversight and an escalation path, without being too onerous for the LSC authors. The committee is also empowered as the escalation body for concerns or conflicts about an LSC: local owners who disagree with the change can appeal to this group who can then arbitrate any conflicts. In practice, this has rarely been needed.

这一流程旨在提供监督和升级处理渠道，同时避免给大规模变更的作者带来过重负担。委员会也有权处理与大规模变更相关的疑虑或冲突：项目的代码所有者若不同意某项变更，可以向委员会申诉，由其裁决争议。实践中，很少需要走到这一步。

> [^13]:  The only kinds of changes that the committee has outright rejected have been those that are deemed dangerous, such as converting all NULL instances to nullptr, or extremely low-value, such as changing spelling from British English to American English, or vice versa. As our experience with such changes has increased and the cost of LSCs has dropped, the threshold for approval has as well.
>
> 13  委员会直接否决过的，只有被认为危险或价值极低的变更。前者例如将所有 NULL 替换为 nullptr，后者例如将英式拼写改为美式拼写，或反过来。随着相关经验积累、大规模变更成本下降，审批门槛也在降低。

### Change Creation 变更创建

After getting the required approval, an LSC author will begin to produce the actual code edits. Sometimes, these can be generated comprehensively into a single large global change that will be subsequently sharded into many smaller independent pieces. Usually, the size of the change is too large to fit in a single global change, due to technical limitations of the underlying version control system.

获得必要批准后，大规模变更的作者就开始生成实际的代码修改。有时，可以先将全部修改生成为一项大型全局变更，再拆成许多小而独立的部分。不过，由于底层版本控制系统的技术限制，修改规模通常大到无法容纳在单项全局变更中。

The change generation process should be as automated as possible so that the parent change can be updated as users backslide into old uses[^14] or textual merge conflicts occur in the changed code. Occasionally, for the rare case in which technical tools aren’t able to generate the global change, we have sharded change generation across humans (see “Case Study: Operation RoseHub” on page 472). Although much more labor intensive than automatically generating changes, this allows global changes to happen much more quickly for time-sensitive applications.

变更生成过程应尽可能自动化，以便在用户重新引入旧用法，或修改的代码发生文本合并冲突时，及时更新总变更。在极少数工具无法生成全局变更的情况下，我们也会把生成工作分配给多个人完成，参见第472页的“案例研究：Operation RoseHub”。虽然这比自动生成变更耗费更多人力，但对于时效性要求高的场景，仍能大幅加快全局变更的推进。

Keep in mind that we optimize for human readability of our codebase, so whatever tool generates changes, we want the resulting changes to look as much like humangenerated changes as possible. This requirement leads to the necessity of style guides and automatic formatting tools (see Chapter 8).[^15]

请记住，我们优先考虑代码库对人的可读性。因此，无论使用什么工具生成变更，都希望结果尽可能接近人工编写的代码。这也是为什么需要风格指南和自动格式化工具，参见第8章。

> [^14]:   This happens for many reasons: copy-and-paste from existing examples, committing changes that have been in development for some time, or simply reliance on old habits.
>
> 14  原因有很多：复制粘贴现有示例，提交已开发了一段时间的变更，或者仅仅沿用旧习惯。
>
> [^15]:   In actuality, this is the reasoning behind the original work on clang-format for C++.
>
> 15  实际上，这正是最初为 C++ 开发 clang-format 的出发点。

### Sharding and Submitting  分片与提交

After a global change has been generated, the author then starts running Rosie. Rosie takes a large change and shards it based upon project boundaries and ownership rules into changes that *can* be submitted atomically. It then puts each individually sharded change through an independent test-mail-submit pipeline. Rosie can be a heavy user of other pieces of Google’s developer infrastructure, so it caps the number of outstanding shards for any given LSC, runs at lower priority, and communicates with the rest of the infrastructure about how much load it is acceptable to generate on our shared testing infrastructure.

生成全局变更后，作者便开始运行 Rosie。Rosie 根据项目边界和代码所有权规则，将大型变更拆成可以原子提交的分片，再让各分片独立经过测试、邮件送审和提交的流水线。Rosie 可能大量使用谷歌开发基础设施中的其他服务，因此会限制每项大规模变更尚未完成的分片数量，以较低优先级运行，并与其他基础设施协调，确定共享测试基础设施能够承受多少负载。

We talk more about the specific test-mail-submit process for each shard below.

下面会进一步介绍每个分片所经历的测试、邮件送审和提交过程。

-----

##### Cattle Versus Pets  牛与宠物

We often use the “cattle and pets” analogy when referring to individual machines in a distributed computing environment, but the same principles can apply to changes within a codebase.

谈到分布式计算环境中的单台机器时，我们常用“牛与宠物”作比喻。同样的道理也适用于代码库中的变更。

At Google, as at most organizations, typical changes to the codebase are handcrafted by individual engineers working on specific features or bug fixes. Engineers might spend days or weeks working through the creation, testing, and review of a single change. They come to know the change intimately, and are proud when it is finally committed to the main repository. The creation of such a change is akin to owning and raising a favorite pet.

和大多数组织一样，谷歌代码库中的普通变更通常由工程师为某个功能或缺陷修复手工编写。工程师可能花几天甚至几周，完成一项变更的创建、测试和审查。他们对这项变更十分熟悉，等到它最终提交到主代码仓库时，也会感到自豪。创建这样的变更，就像养育一只心爱的宠物。

In contrast, effective handling of LSCs requires a high degree of automation and produces an enormous number of individual changes. In this environment, we’ve found it useful to treat specific changes as cattle: nameless and faceless commits that might be rolled back or otherwise rejected at any given time with little cost unless the entire herd is affected. Often this happens because of an unforeseen problem not caught by tests, or even something as simple as a merge conflict.

相比之下，有效处理大规模变更需要高度自动化，也会生成大量独立变更。这时，把具体变更当作牛群中的一头牛会很有帮助：这些提交并无特殊身份，随时可能被回滚或拒绝，只要不影响整个牛群，代价就很小。原因通常是测试未发现的意外问题，甚至只是一次合并冲突。

With a “pet” commit, it can be difficult to not take rejection personally, but when working with many changes as part of a large-scale change, it’s just the nature of the job. Having automation means that tooling can be updated and new changes generated at very low cost, so losing a few cattle now and then isn’t a problem.

如果把一次提交当作“宠物”，遭到拒绝时很难不往心里去。但在大规模变更中处理众多变更时，这只是工作的常态。有了自动化，就能更新工具并以很低的成本重新生成变更，因此偶尔损失几头牛并不成问题。

-----

#### Testing 测试

Each independent shard is tested by running it through TAP, Google’s CI framework. We run every test that depends on the files in a given change transitively, which often creates high load on our CI system.

每个独立分片都通过谷歌的 CI 框架 TAP 进行测试。我们会运行所有通过传递依赖关联到该变更所含文件的测试，这常常给 CI 系统带来很高的负载。

This might sound computationally expensive, but in practice, the vast majority of shards affect fewer than one thousand tests, out of the millions across our codebase. For those that affect more, we can group them together: first running the union of all affected tests for all shards, and then for each individual shard running just the intersection of its affected tests with those that failed the first run. Most of these unions cause almost every test in the codebase to be run, so adding additional changes to that batch of shards is nearly free.

这听起来可能需要大量计算资源，但实际上，代码库虽有数百万个测试，绝大多数分片影响的测试不到1000个。对于影响更多测试的分片，可以合并处理：先运行这些分片所影响的全部测试的并集，再针对每个分片，只重跑其受影响测试与首轮失败测试的交集。这些并集大多已涵盖代码库中几乎全部测试，因此再向这批分片加入变更，几乎不会增加成本。

One of the drawbacks of running such a large number of tests is that independent low-probability events are almost certainties at large enough scale. Flaky and brittle tests, such as those discussed in Chapter 11, which often don’t harm the teams that write and maintain them, are particularly difficult for LSC authors. Although fairly low impact for individual teams, flaky tests can seriously affect the throughput of an LSC system. Automatic flake detection and elimination systems help with this issue, but it can be a constant effort to ensure that teams that write flaky tests are the ones that bear their costs.

运行海量测试有一个缺点：彼此独立的低概率事件，在规模足够大时几乎必然出现。第11章讨论过的不稳定测试和脆弱测试，通常不会给编写、维护它们的团队造成太大影响，却会让大规模变更的作者十分棘手。不稳定测试对单个团队影响较小，却可能严重降低大规模变更系统的吞吐量。自动检测和消除测试不稳定性的系统有助于缓解问题，但要让编写不稳定测试的团队承担相应成本，可能需要持续努力。

In our experience with LSCs as semantic-preserving, machine-generated changes, we are now much more confident in the correctness of a single change than a test with any recent history of flakiness—so much so that recently flaky tests are now ignored when submitting via our automated tooling. In theory, this means that a single shard can cause a regression that is detected only by a flaky test going from flaky to failing. In practice, we see this so rarely that it’s easier to deal with it via human communication rather than automation.

根据我们处理保持语义不变、由机器生成的大规模变更的经验，我们现在对单项变更正确性的信心，远高于对近期曾出现不稳定现象的测试的信心。因此，通过自动化工具提交时，我们会忽略近期不稳定的测试。理论上，这意味着某个分片可能引入回归缺陷，而只有一个从偶发失败变成持续失败的不稳定测试能够发现它。实际中，这种情况极少发生，通过人工沟通处理比实现自动化更容易。

For any LSC process, individual shards should be committable independently. This means that they don’t have any interdependence or that the sharding mechanism can group dependent changes (such as to a header file and its implementation) together. Just like any other change, large-scale change shards must also pass project-specific checks before being reviewed and committed.

无论采用什么大规模变更流程，各分片都应能够独立提交。这意味着分片之间没有依赖，或者分片机制能够把存在依赖的修改归到同一分片，例如对头文件及其实现的修改。与其他变更一样，大规模变更的分片在审查和提交前，也必须通过项目专用检查。

#### Mailing reviewers  邮件送审

After Rosie has validated that a change is safe through testing, it mails the change to an appropriate reviewer. In a company as large as Google, with thousands of engineers, reviewer discovery itself is a challenging problem. Recall from Chapter 9 that code in the repository is organized with OWNERS files, which list users with approval privileges for a specific subtree in the repository. Rosie uses an owners detection service that understands these OWNERS files and weights each owner based upon their expected ability to review the specific shard in question. If a particular owner proves to be unresponsive, Rosie adds additional reviewers automatically in an effort to get a change reviewed in a timely manner.

Rosie 通过测试确认变更安全后，就会将变更以邮件形式发给合适的审查者。在谷歌这样拥有数千名工程师的公司，找到审查者本身就是一个难题。如第9章所述，代码仓库使用 OWNERS 文件组织代码所有权，列出有权批准特定子树中变更的用户。Rosie 使用能够解析这些文件的所有者识别服务，并根据各所有者审查具体分片的预期能力分配权重。如果某位所有者迟迟没有响应，Rosie 会自动增加审查者，争取让变更及时得到审查。

As part of the mailing process, Rosie also runs the per-project precommit tools, which might perform additional checks. For LSCs, we selectively disable certain checks such as those for nonstandard change description formatting. Although useful for individual changes on specific projects, such checks are a source of heterogeneity across the codebase and can add significant friction to the LSC process. This heterogeneity is a barrier to scaling our processes and systems, and LSC tools and authors can’t be expected to understand special policies for each team.

邮件送审时，Rosie 还会运行各项目的提交前工具，其中可能包含额外检查。对于大规模变更，我们会选择性地禁用某些检查，例如对项目自定义变更描述格式的检查。这些检查虽然对具体项目的单项变更有用，却增加了整个代码库的异质性，给大规模变更流程带来明显阻力。这种异质性妨碍流程和系统随规模扩展，不能要求大规模变更工具及其使用者了解每个团队的特殊规定。

We also aggressively ignore presubmit check failures that preexist the change in question. When working on an individual project, it’s easy for an engineer to fix those and continue with their original work, but that technique doesn’t scale when making LSCs across Google’s codebase. Local code owners are responsible for having no preexisting failures in their codebase as part of the social contract between them and infrastructure teams.

对于变更之前就已存在的提交前检查失败，我们也会尽可能忽略。在单个项目中，工程师顺手修复这些问题后继续工作并不难；但对整个谷歌代码库实施大规模变更时，这种做法无法有效扩展。各项目的代码所有者有责任保证代码库中没有这类既有失败，这是他们与基础设施团队之间协作约定的一部分。

#### Reviewing 审查

As with other changes, changes generated by Rosie are expected to go through the standard code review process. In practice, we’ve found that local owners don’t often treat LSCs with the same rigor as regular changes—they trust the engineers generating LSCs too much. Ideally these changes would be reviewed as any other, but in practice, local project owners have come to trust infrastructure teams to the point where these changes are often given only cursory review. We’ve come to only send changes to local owners for which their review is required for context, not just approval permissions. All other changes can go to a “global approver”: someone who has ownership rights to approve *any* change throughout the repository.

和其他变更一样，Rosie 生成的变更也应经过标准代码审查流程。但实践中，我们发现各项目的代码所有者往往不会像审查普通变更那样严格审查大规模变更，因为他们过于信任生成变更的工程师。理想情况下，这些变更应得到同等审查；实际上，项目所有者对基础设施团队的信任，常常使审查流于粗略。因此，我们后来只在审查确实需要项目背景知识时，才将变更交给项目所有者，而不只是为了取得批准权限。其余变更都可以交给“全局审批人”，也就是拥有整个代码仓库所有权权限、能够批准任何变更的人。

When using a global approver, all of the individual shards are assigned to that person, rather than to individual owners of different projects. Global approvers generally have specific knowledge of the language and/or libraries they are reviewing and work with the large-scale change author to know what kinds of changes to expect. They know what the details of the change are and what potential failure modes for it might exist and can customize their workflow accordingly.

采用全局审批人时，所有分片都交给同一个人，而不是分给不同项目的代码所有者。全局审批人通常熟悉相关语言或库，有时两者都熟悉，并与大规模变更的作者合作，了解预期会出现哪些修改。他们掌握变更细节和潜在的失败模式，因此可以相应调整审查流程。

Instead of reviewing each change individually, global reviewers use a separate set of pattern-based tooling to review each of the changes and automatically approve ones that meet their expectations. Thus, they need to manually examine only a small subset that are anomalous because of merge conflicts or tooling malfunctions, which allows the process to scale very well.

全局审批人不会逐项手工审查变更，而是使用另一套基于模式的工具检查各项变更，自动批准符合预期的部分。这样，只需手动检查因合并冲突或工具故障而出现异常的少量变更，审查流程也就能够有效地随规模扩展。

#### Submitting 提交

Finally, individual changes are committed. As with the mailing step, we ensure that the change passes the various project precommit checks before actually finally being committed to the repository.

最后，各项变更分别提交。与邮件送审阶段一样，在变更最终进入代码仓库之前，我们会确保它通过各项项目提交前检查。

With Rosie, we are able to effectively create, test, review, and submit thousands of changes per day across all of Google’s codebase and have given teams the ability to effectively migrate their users. Technical decisions that used to be final, such as the name of a widely used symbol or the location of a popular class within a codebase, no longer need to be final.

借助 Rosie，我们每天都能在谷歌整个代码库中高效地创建、测试、审查并提交数千项变更，让各团队能够高效地迁移用户。过去一旦作出就难以改变的技术决策，例如常用符号的名称或常用类在代码库中的位置，如今都不必再是定局。

### Cleanup  清理

Different LSCs have different definitions of “done,” which can vary from completely removing an old system to migrating only high-value references and leaving old ones to organically disappear.[^16] In almost all cases, it’s important to have a system that prevents additional introductions of the symbol or system that the large-scale change worked hard to remove. At Google, we use the Tricorder framework mentioned in Chapters 20 and 19 to flag at review time when an engineer introduces a new use of a deprecated object, and this has proven an effective method to prevent backsliding. We talk more about the entire deprecation process in Chapter 15.

不同的大规模变更对“完成”的定义不同：有的要求彻底移除旧系统，有的只迁移高价值的引用，让其余旧引用自然消失。几乎所有情况下，都需要一种机制，防止开发者重新引入那些费力移除的符号或系统。谷歌使用第20章和第19章介绍的 Tricorder 框架，在代码审查时标记对已弃用对象的新增使用。实践证明，这能有效防止旧用法再次出现。第15章会进一步讨论完整的弃用流程。

> [^16]: Sadly, the systems we most want to organically decompose are those that are the most resilient to doing so. They are the plastic six-pack rings of the code ecosystem.
>
> 16 遗憾的是，我们最希望自然分解的系统，往往恰恰最难分解。它们就像代码生态系统中捆扎六罐装饮料的塑料环。

## Conclusion  总结

LSCs form an important part of Google’s software engineering ecosystem. At design time, they open up more possibilities, knowing that some design decisions don’t need to be as fixed as they once were. The LSC process also allows maintainers of core infrastructure the ability to migrate large swaths of Google’s codebase from old systems, language versions, and library idioms to new ones, keeping the codebase consistent, spatially and temporally. And all of this happens with only a few dozen engineers supporting tens of thousands of others.

大规模变更是谷歌软件工程生态系统的重要组成部分。知道某些设计决策不再像过去那样难以更改，设计时就有了更多选择。大规模变更流程也让核心基础设施的维护者能够将代码库中的大量代码，从旧系统、旧语言版本和旧的库惯用写法迁移到相应的新版本，使代码库在不同部分之间、在长期演进过程中都能保持一致。完成这一切，只需几十名工程师为数万名工程师提供支持。

No matter the size of your organization, it’s reasonable to think about how you would make these kinds of sweeping changes across your collection of source code. Whether by choice or by necessity, having this ability will allow greater flexibility as your organization scales while keeping your source code malleable over time.

无论组织规模多大，都值得考虑如何对全部源代码实施这类全面变更。不管是主动选择还是迫于需要，具备这种能力，都能让组织在扩大规模时保持更大的灵活性，也让源代码在长期演进中仍然易于修改。

## TL;DRs  内容提要

- An LSC process makes it possible to rethink the immutability of certain technical decisions.
- Traditional models of refactoring break at large scales.
- Making LSCs means making a habit of making LSCs.

- 大规模变更流程让我们能够重新思考：某些技术决策是否真的不可更改。
- 传统重构模式到了大规模场景下就难以奏效。
- 要做好大规模变更，就要养成经常进行大规模变更的习惯。
