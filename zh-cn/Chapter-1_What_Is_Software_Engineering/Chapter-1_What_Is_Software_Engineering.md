
**CHAPTER 1**

# What Is Software Engineering?

# 第一章 软件工程是什么？

**Written by Titus Winters**

**Edited by Tom Manshreck**

*Nothing is built on stone; all is built on sand, but we must build as if the sand were stone.*
																																		*--Jorge Luis Borges*

We see three critical differences between programming and software engineering: time, scale, and the trade-offs at play. On a software engineering project, engineers need to be more concerned with the passage of time and the eventual need for change. In a software engineering organization, we need to be more concerned about scale and efficiency, both for the software we produce as well as for the organization that is producing it. Finally, as software engineers, we are asked to make more complex decisions with higher-stakes outcomes, often based on imprecise estimates of time and growth.

我们认为，编程与软件工程有三个关键区别：时间、规模，以及其中的权衡取舍。在软件工程项目中，工程师需要更多地关注时间推移的影响，以及最终需要作出的变更。在软件工程组织中，无论是开发的软件，还是开发软件的组织本身，都需要更加关注规模和效率。最后，软件工程师需要作出更复杂、后果更重大的决策，而这些决策往往只能依据对时间和增长的不精确估计。

Within Google, we sometimes say, “Software engineering is programming integrated over time.” Programming is certainly a significant part of software engineering: after all, programming is how you generate new software in the first place. If you accept this distinction, it also becomes clear that we might need to delineate between programming tasks (development) and software engineering tasks (development, modification, maintenance). The addition of time adds an important new dimension to programming. Cubes aren’t squares, distance isn’t velocity. Software engineering isn’t programming.

在谷歌内部，我们有时会说：“软件工程是编程在时间上的积分。”编程当然是软件工程的重要组成部分：毕竟，新软件首先要靠编程来实现。如果接受这一区分，就不难理解，我们可能需要区分编程任务（开发）与软件工程任务（开发、修改、维护）。时间为编程引入了一个重要的新维度。立方体不是正方形，距离不是速度。同样，软件工程也不等于编程。

One way to see the impact of time on a program is to think about the question, “What is the expected life span[^1] of your code?” Reasonable answers to this question vary by roughly a factor of 100,000. It is just as reasonable to think of code that needs to last for a few minutes as it is to imagine code that will live for decades. Generally, code on the short end of that spectrum is unaffected by time. It is unlikely that you need to adapt to a new version of your underlying libraries, operating system (OS), hardware, or language version for a program whose utility spans only an hour. These short-lived systems are effectively “just” a programming problem, in the same way that a cube compressed far enough in one dimension is a square. As we expand that time to allow for longer life spans, change becomes more important. Over a span of a decade or more, most program dependencies, whether implicit or explicit, will likely change. This recognition is at the root of our distinction between software engineering and programming.

要理解时间对程序的影响，可以先问一个问题：“你的代码预计会使用多久？”这个问题的合理答案可以相差约100,000倍。代码只需使用几分钟，与代码需要使用几十年，都是合理的情况。通常，生命周期很短的代码不太受时间影响。对于只在一小时内有用的程序，你大概不必去适应底层库、操作系统（OS）、硬件或语言的新版本。这类短期系统实际上“只是”编程问题，就像把立方体沿一个维度充分压缩，就成了正方形。随着预期生命周期延长，变更也愈发重要。在十年甚至更长的时间里，程序的大多数依赖，无论显式还是隐式，都可能发生变化。这正是我们区分软件工程与编程的根本依据。

> [^1]: We don’t mean “execution lifetime,” we mean “maintenance lifetime”—how long will the code continue to be built, executed, and maintained? How long will this software provide value?
>
> [1] 这里指的不是“执行生命周期”，而是“维护生命周期”：代码还需要持续构建、执行和维护多久？软件还要提供多久的价值？

This distinction is at the core of what we call sustainability for software. Your project is sustainable if, for the expected life span of your software, you are capable of reacting to whatever valuable change comes along, for either technical or business reasons. Importantly, we are looking only for capability—you might choose not to perform a given upgrade, either for lack of value or other priorities.[^2] When you are fundamentally incapable of reacting to a change in underlying technology or product direction, you’re placing a high-risk bet on the hope that such a change never becomes critical. For short-term projects, that might be a safe bet. Over multiple decades, it probably isn’t.[^3]

这一区别也是我们所说的软件可持续性的核心。如果在软件的预期生命周期内，无论出于技术还是业务原因，你都有能力应对有价值的变更，那么项目就是可持续的。需要强调的是，我们关注的是这种能力：你仍然可以因为某次升级价值不足，或有其他更优先的事项，而选择不升级。如果你根本无法应对底层技术或产品方向的变化，就是在冒险押注：希望这种变化永远不会变得至关重要。对短期项目而言，这样的押注也许稳妥；但把时间拉长到几十年，恐怕就不是了。

Another way to look at software engineering is to consider scale. How many people are involved? What part do they play in the development and maintenance over time? A programming task is often an act of individual creation, but a software engineering task is a team effort. An early attempt to define software engineering produced a good definition for this viewpoint: “The multiperson development of multiversion programs.”[^4] This suggests the difference between software engineering and programming is one of both time and people. Team collaboration presents new problems, but also provides more potential to produce valuable systems than any single programmer could.

理解软件工程的另一个角度是规模。有多少人参与？在持续开发和维护的过程中，他们各自承担什么角色？编程任务往往是个人的创造活动，而软件工程任务需要团队协作。软件工程早期的一种定义很好地概括了这一点：“由多人开发多版本程序。”这说明，软件工程与编程的区别同时涉及时间和人员。团队协作会带来新问题，但与单个程序员相比，也更有潜力构建有价值的系统。

> [^2]: This is perhaps a reasonable hand-wavy definition of technical debt: things that “should” be done, but aren’t yet—the delta between our code and what we wish it was.
>
> 2 这也许可以作为技术债务的一个合理但粗略的定义：那些“应该做”却还没有做的事，也就是代码现状与我们期望状态之间的差距。
>
> [^3]: Also consider the issue of whether we know ahead of time that a project is going to be long lived.
>
> 3 还要考虑：我们是否能事先知道一个项目会长期存在。  
>
> [^4]: There is some question as to the original attribution of this quote; consensus seems to be that it was originally phrased by Brian Randell or Margaret Hamilton, but it might have been wholly made up by Dave Parnas. The common citation for it is “Software Engineering Techniques: Report of a conference sponsored by the NATO Science Committee,” Rome, Italy, 27–31 Oct. 1969, Brussels, Scientific Affairs Division, NATO.
>
> 4 这句话的最初出处尚有争议。一般认为，它最早由 Brian Randell 或 Margaret Hamilton 提出，但也可能完全出自 Dave Parnas。通常引用的来源是《软件工程技术：北约科学委员会主办会议的报告》，会议于1969年10月27日至31日在意大利罗马举行，报告由位于布鲁塞尔的北约科学事务司出版。

Team organization, project composition, and the policies and practices of a software project all dominate this aspect of software engineering complexity. These problems are inherent to scale: as the organization grows and its projects expand, does it become more efficient at producing software? Does our development workflow become more efficient as we grow, or do our version control policies and testing strategies cost us proportionally more? Scale issues around communication and human scaling have been discussed since the early days of software engineering, going all the way back to the Mythical Man Month. [^5] Such scale issues are often matters of policy and are fundamental to the question of software sustainability: how much will it cost to do the things that we need to do repeatedly?

在软件工程复杂性的这一方面，团队组织、项目构成，以及项目采用的策略和实践，都起着主导作用。这些问题与规模密不可分：组织增长、项目扩大后，软件开发是否会更高效？开发工作流的效率会随规模提升，还是版本控制和测试策略带来的成本也会按比例增加？从软件工程发展初期，人们就在讨论沟通和人员规模的问题，至少可以追溯到《人月神话》。这类规模问题往往取决于策略，也是软件可持续性的一个根本问题：那些必须反复完成的工作，究竟要付出多少成本？

We can also say that software engineering is different from programming in terms of the complexity of decisions that need to be made and their stakes. In software engineering, we are regularly forced to evaluate the trade-offs between several paths forward, sometimes with high stakes and often with imperfect value metrics. The job of a software engineer, or a software engineering leader, is to aim for sustainability and management of the scaling costs for the organization, the product, and the development workflow . With those inputs in mind, evaluate your trade-offs and make rational decisions. We might sometimes defer maintenance changes, or even embrace policies that don’t scale well, with the knowledge that we’ll need to revisit those decisions. Those choices should be explicit and clear about the deferred costs.

软件工程与编程的区别，还体现在决策的复杂程度及其后果上。在软件工程中，我们经常需要在几条可行路径之间作出权衡；有时后果重大，而衡量价值的指标又往往不够完善。软件工程师及其负责人的职责，是实现组织、产品和开发工作流的可持续性，并控制它们随规模扩大而增加的成本。应当根据这些因素评估取舍，作出理性决策。有时，我们会推迟维护性变更，甚至采用不利于规模扩展的策略，同时清楚地知道将来必须重新审视这些选择。这样的取舍应当明确作出，并清楚说明推迟到未来承担的成本。

Rarely is there a one-size-fits-all solution in software engineering, and the same applies to this book. Given a factor of 100,000 for reasonable answers on “How long will this software live,” a range of perhaps a factor of 10,000 for “How many engineers are in your organization,” and who-knows-how-much for “How many compute resources are available for your project,” Google’s experience will probably not match yours. In this book, we aim to present what we’ve found that works for us in the construction and maintenance of software that we expect to last for decades, with tens of thousands of engineers, and world-spanning compute resources. Most of the practices that we find are necessary at that scale will also work well for smaller endeavors: consider this a report on one engineering ecosystem that we think could be good as you scale up. In a few places, super-large scale comes with its own costs, and we’d be happier to not be paying extra overhead. We call those out as a warning. Hopefully if your organization grows large enough to be worried about those costs, you can find a better answer.

软件工程很少有放之四海而皆准的解决方案，本书也一样。“软件要使用多久”的合理答案可能相差100,000倍，“组织有多少工程师”的答案可能相差10,000倍，而“项目能使用多少计算资源”的差距更难估量。因此，谷歌的经验未必与你的情况吻合。本书介绍的是我们的实践：由数万名工程师，利用遍布全球的计算资源，构建并维护预计要使用几十年的软件。在这种规模下必不可少的许多做法，同样适用于规模较小的项目。你可以把本书看作一份工程生态系统的实践报告，我们认为其中的经验可能有助于你应对规模增长。不过，超大规模有时也会带来额外成本，而我们也宁愿不承担这些开销。对于这些情况，我们会特别指出，供读者警惕。希望当你的组织大到需要考虑这些成本时，能够找到更好的解决办法。

Before we get to specifics about teamwork, culture, policies, and tools, let’s first elaborate on these primary themes of time, scale, and trade-offs.

在讨论团队协作、文化、策略和工具的具体做法之前，我们先进一步说明时间、规模和权衡这三个核心主题。

> [^5]: Frederick P. Brooks Jr. The Mythical Man-Month: Essays on Software Engineering (Boston: Addison-Wesley, 1995)
>
> Frederick P. Brooks Jr.，《人月神话：软件工程随笔》（波士顿：Addison-Wesley，1995）。

## Time and Change 时间与变化
When a novice is learning to program, the life span of the resulting code is usually measured in hours or days. Programming assignments and exercises tend to be write- once, with little to no refactoring and certainly no long-term maintenance. These programs are often not rebuilt or executed ever again after their initial production. This isn’t surprising in a pedagogical setting. Perhaps in secondary or post-secondary education, we may find a team project course or hands-on thesis. If so, such projects are likely the only time student code will live longer than a month or so. Those developers might need to refactor some code, perhaps as a response to changing requirements, but it is unlikely they are being asked to deal with broader changes to their environment.

新手学习编程时，写出的代码通常只需要存在几小时或几天。编程作业和练习大多写完就结束，很少重构，更谈不上长期维护。这些程序最初完成后，往往再也不会被构建或执行。在教学环境中，这并不奇怪。中学或高等教育阶段也许会安排团队项目课程或实践型毕业课题，这可能是学生的代码唯一需要存续超过一个月左右的场合。学生可能会为了应对需求变化而重构部分代码，但通常不需要处理整个运行环境更广泛的变化。

We also find developers of short-lived code in common industry settings. Mobile apps often have a fairly short life span,[^6] and for better or worse, full rewrites are relatively common. Engineers at an early-stage startup might rightly choose to focus on immediate goals over long-term investments: the company might not live long enough to reap the benefits of an infrastructure investment that pays off slowly. A serial startup developer could very reasonably have 10 years of development experience and little or no experience maintaining any piece of software expected to exist for longer than a year or two.

在业界，开发短生命周期代码也很常见。移动应用的生命周期往往较短，不论利弊如何，彻底重写并不少见。处于早期阶段的初创公司，其工程师优先关注眼前目标而不是长期投入，可能完全合理：公司未必能存续到缓慢回报的基础设施投资开始见效的时候。因此，一个先后在多家初创公司工作的开发者，即使有10年开发经验，也可能几乎没有维护过预计要使用一两年以上的软件。

On the other end of the spectrum, some successful projects have an effectively unbounded life span: we can’t reasonably predict an endpoint for Google Search, the Linux kernel, or the Apache HTTP Server project. For most Google projects, we must assume that they will live indefinitely—we cannot predict when we won’t need to upgrade our dependencies, language versions, and so on. As their lifetimes grow, these long-lived projects *eventually* have a different feel to them than programming assignments or startup development.

在另一端，一些成功项目的生命周期实际上没有可预见的终点：我们很难合理预测谷歌搜索、Linux 内核或 Apache HTTP Server 项目会在何时结束。对于谷歌的大多数项目，我们必须假定它们会长期延续，因为无法预知何时才不再需要升级依赖、语言版本等。随着时间推移，这些长期项目最终会呈现出与编程作业或初创公司开发工作不同的特点。

Consider Figure 1-1, which demonstrates two software projects on opposite ends of this “expected life span” spectrum. For a programmer working on a task with an expected life span of hours, what types of maintenance are reasonable to expect? That is, if a new version of your OS comes out while you’re working on a Python script that will be executed one time, should you drop what you’re doing and upgrade? Of course not: the upgrade is not critical. But on the opposite end of the spectrum, Google Search being stuck on a version of our OS from the 1990s would be a clear problem.

图1-1展示了两个处于“预期生命周期”两端的软件项目。对于只需使用几小时的程序，合理的维护预期是什么？假设你正在编写一个只运行一次的 Python 脚本，此时操作系统发布了新版本，你应该放下手头工作去升级吗？当然不必，这次升级并不关键。反过来，如果谷歌搜索至今还停留在20世纪90年代的操作系统版本上，显然就有问题了。

> [^6]: Appcelerator, “[Nothing is Certain Except Death, Taxes and a Short Mobile App Lifespan](https://oreil.ly/pnT2_),” Axway Developer blog, December 6, 2012.
>
> 除了死亡、税收和移动应用短暂的生命周期，没有什么是确定的。

![Figure 1-1. Life span and the importance of upgrades](./images/figure%201-1.png)

The low and high points on the expected life span spectrum suggest that there’s a transition somewhere. Somewhere along the line between a one-off program and a project that lasts for decades, a transition happens: a project must begin to react to changing externalities.[^7] For any project that didn’t plan for upgrades from the start, that transition is likely very painful for three reasons, each of which compounds the others:

- You’re performing a task that hasn’t yet been done for this project; more hidden assumptions have been baked-in.
- The engineers trying to do the upgrade are less likely to have experience in this sort of task.
- The size of the upgrade is often larger than usual, doing several years’ worth of upgrades at once instead of a more incremental upgrade.

预期生命周期的两个极端表明，中间必然存在某个转折点。从一次性程序到持续几十年的项目，到了某个阶段，项目就必须开始应对外部环境的变化。如果项目从一开始就没有为升级作准备，跨过这个转折点往往会非常痛苦，原因有三，而且它们还会相互加剧：

- 这项工作在项目中从未做过，代码已经积累了更多隐含假设。
- 负责升级的工程师很可能缺乏此类工作经验。
- 升级范围往往比平时大，需要一次补上几年的升级，而不是逐步推进。

And thus, after actually going through such an upgrade once (or giving up part way through), it’s pretty reasonable to overestimate the cost of doing a subsequent upgrade and decide “Never again.” Companies that come to this conclusion end up committing to just throwing things out and rewriting their code, or deciding to never upgrade again. Rather than take the natural approach by avoiding a painful task, sometimes the more responsible answer is to invest in making it less painful. It all depends on the cost of your upgrade, the value it provides, and the expected life span of the project in question.

因此，在经历一次这样的升级，甚至中途放弃之后，人们很容易高估下一次升级的成本，并下决心“再也不升级了”。得出这一结论的公司，最终要么选择把旧代码全部丢掉重写，要么决定永远不再升级。回避痛苦的工作是很自然的反应，但有时更负责任的选择，是投入资源，让这项工作不再那么痛苦。如何取舍，取决于升级的成本、它带来的价值，以及项目的预期生命周期。

> [^7]: Your own priorities and tastes will inform where exactly that transition happens. We’ve found that most projects seem to be willing to upgrade within five years. Somewhere between 5 and 10 years seems like a conservative estimate for this transition in general.
>
> 7 具体的转折点取决于你的优先事项和偏好。我们发现，大多数项目似乎愿意在五年内升级。总体而言，把这个转折点估计在5到10年之间，似乎是一个保守判断。

Getting through not only that first big upgrade, but getting to the point at which you can reliably stay current going forward, is the essence of long-term sustainability for your project. Sustainability requires planning and managing the impact of required change. For many projects at Google, we believe we have achieved this sort of sustainability, largely through trial and error.

项目的长期可持续性，不只是熬过第一次大规模升级，还要做到此后能够持续、可靠地跟进更新。要实现这一点，就必须规划并管理必要变更带来的影响。我们认为，谷歌的许多项目已经具备这种可持续性，而这很大程度上是反复试错的结果。

So, concretely, how does short-term programming differ from producing code with a much longer expected life span? Over time, we need to be much more aware of the difference between “happens to work” and “is maintainable.” There is no perfect solution for identifying these issues. That is unfortunate, because keeping software maintainable for the long-term is a constant battle.

具体来说，短期编程与开发预期要使用很久的代码，到底有什么不同？时间越长，我们越需要分清“碰巧能用”和“可以维护”。遗憾的是，识别这些问题没有完美的方法，而让软件长期保持可维护性是一场持久战。

### Hyrum’s  Law 海勒姆定律

If you are maintaining a project that is used by other engineers, the most important lesson about “it works” versus “it is maintainable” is what we’ve come to call *Hyrum’s* *Law*:

    *With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody.*

如果你维护的项目会被其他工程师使用，那么，要理解“能用”与“可维护”的区别，最重要的一课就是我们所说的海勒姆定律：

    *只要 API 的用户足够多，不论你在契约中作了什么承诺，系统的每一种可观察行为都会被某些用户依赖。*

In our experience, this axiom is a dominant factor in any discussion of changing software over time. It is conceptually akin to entropy: discussions of change and maintenance over time must be aware of Hyrum’s Law[^8] just as discussions of efficiency or thermodynamics must be mindful of entropy. Just because entropy never decreases doesn’t mean we shouldn’t try to be efficient. Just because Hyrum’s Law will apply when maintaining software doesn’t mean we can’t plan for it or try to better understand it. We can mitigate it, but we know that it can never be eradicated.

根据我们的经验，只要讨论软件随时间发生的变化，这条定律就是绕不开的因素。它在概念上类似于熵：讨论长期变更和维护时必须考虑海勒姆定律，就像讨论效率或热力学时必须考虑熵一样。熵不会减少，并不意味着我们不该努力提高效率；维护软件时海勒姆定律会发挥作用，也不意味着我们无法提前规划或加深理解。我们可以减轻它的影响，但也知道无法彻底消除它。

Hyrum’s Law represents the practical knowledge that—even with the best of intentions, the best engineers, and solid practices for code review—. As an API owner, you will gain some flexibility and freedom by being clear about interface promises, but in practice, the complexity and difficulty of a given change also depends on how useful a user finds some observable behavior of your API. If users cannot depend on such things, your API will be easy to change. Given enough time and enough users, even the most innocuous change will break something;[^9] your analysis of the value of that change must incorporate the difficulty in investigating, identifying, and resolving those breakages.

海勒姆定律概括了一条实践经验：即使初衷良好、工程师优秀、代码审查实践扎实，我们也不能假定用户会完全遵守已公布的契约或最佳实践。作为 API 的维护者，明确接口承诺可以为你保留一定的灵活性和自由度。但在实践中，一次变更有多复杂、多困难，也取决于用户有多看重 API 的某些可观察行为。如果用户无法依赖这些行为，API 就容易修改。只要时间足够长、用户足够多，即使看似最无害的变更，也会破坏某些使用方式。因此，评估变更价值时，还必须考虑调查、定位和解决这些问题的难度。

> [^8]:	To his credit, Hyrum tried really hard to humbly call this “The Law of Implicit Dependencies,” but “Hyrum’s Law” is the shorthand that most people at Google have settled on.
>
> 值得一提的是，海勒姆出于谦逊，曾极力主张称它为“隐式依赖定律”，但谷歌的大多数人最终还是采用了“海勒姆定律”这个简称。
>
> [^9]:	See “Workflow,” an xkcd comic.
>
> 参见 xkcd 漫画《工作流》（Workflow）。

### Example: Hash Ordering 哈希遍历顺序

Consider the example of hash iteration ordering. If we insert five elements into a hash-based set, in what order do we get them out?

以哈希容器的遍历顺序为例：向一个基于哈希的集合插入五个元素后，会按什么顺序取出它们？

```python
>>> for i in {"apple", "banana", "carrot", "durian", "eggplant"}: print(i)
...
durian 
carrot 
apple 
eggplant 
banana
```

Most programmers know that hash tables are non-obviously ordered. Few know the specifics of whether the particular hash table they are using is intending to provide that particular ordering forever. This might seem unremarkable, but over the past decade or two, the computing industry’s experience using such types has evolved:

- Hash flooding[^10] attacks provide an increased incentive for nondeterministic hash iteration.
- Potential efficiency gains from research into improved hash algorithms or hash containers require changes to hash iteration order.
- Per Hyrum’s Law, programmers will write programs that depend on the order in which a hash table is traversed, if they have the ability to do so.

大多数程序员都知道，哈希表中的元素顺序并不直观。但很少有人清楚，自己使用的哈希表是否打算永久保证这个顺序。这似乎无关紧要，但在过去的一二十年里，业界对这类数据结构的认识已经发生了变化：

- 哈希洪水攻击使人们更有理由采用非确定性的哈希遍历顺序。
- 改进哈希算法或哈希容器可能带来效率提升，但往往需要改变遍历顺序。
- 根据海勒姆定律，只要有机会，程序员就会写出依赖哈希表遍历顺序的程序。

As a result, if you ask any expert “Can I assume a particular output sequence for my hash container?” that expert will presumably say “No.” By and large that is correct, but perhaps simplistic. A more nuanced answer is, “If your code is short-lived, with no changes to your hardware, language runtime, or choice of data structure, such an assumption is fine. If you don’t know how long your code will live, or you cannot promise that nothing you depend upon will ever change, such an assumption is incorrect.” Moreover, even if your own implementation does not depend on hash container order, it might be used by other code that implicitly creates such a dependency. For example, if your library serializes values into a Remote Procedure Call (RPC) response, the RPC caller might wind up depending on the order of those values.

因此，如果你问专家：“我能假定哈希容器按某个特定顺序输出吗？”得到的回答大概是“不能”。这基本正确，却可能过于简单。更细致的回答是：“如果代码只会短期使用，其间硬件、语言运行时和数据结构都不会变化，这样假定没有问题。但如果你不知道代码会使用多久，或者无法保证它依赖的一切都不会变化，这样假定就不成立。”此外，即使你的实现不依赖哈希容器的顺序，使用它的其他代码也可能隐式建立这种依赖。例如，如果库把一组值序列化到远程过程调用（RPC）的响应中，调用方最终可能就会依赖这些值的排列顺序。

This is a very basic example of the difference between “it works” and “it is correct.” For a short-lived program, depending on the iteration order of your containers will not cause any technical problems. For a software engineering project, on the other hand, such reliance on a defined order is a risk—given enough time, something will make it valuable to change that iteration order. That value can manifest in a number of ways, be it efficiency, security, or merely future-proofing the data structure to allow for future changes. When that value becomes clear, you will need to weigh the trade- offs between that value and the pain of breaking your developers or customers.

这是区分“能用”和“正确”的一个简单例子。对短期程序而言，依赖容器的遍历顺序不会带来技术问题。但对软件工程项目而言，依赖某个固定顺序就是一种风险：只要时间足够长，总会出现让改变遍历顺序变得有价值的理由。这种价值可能体现为效率、安全性，也可能只是让数据结构更容易适应未来的变化。一旦这种价值显现，就需要权衡它与破坏开发者或客户现有使用方式所带来的代价。

> [^10]: A type of Denial-of-Service (DoS) attack in which an untrusted user knows the structure of a hash table and the hash function and provides data in such a way as to degrade the algorithmic performance of operations on the table.
>
> 一种拒绝服务（DoS）攻击：不受信任的用户了解哈希表的结构和哈希函数，并据此构造输入，使表上操作的算法性能恶化。

Some languages specifically randomize hash ordering between library versions or even between execution of the same program in an attempt to prevent dependencies. But even this still allows for some Hyrum’s Law surprises: there is code that uses hash iteration ordering as an inefficient random-number generator. Removing such randomness now would break those users. Just as entropy increases in every thermodynamic system, Hyrum’s Law applies to every observable behavior.  

为了避免用户依赖遍历顺序，有些语言会特意让不同库版本，甚至同一程序的不同次运行，采用随机化的哈希遍历顺序。然而，这仍可能带来海勒姆定律式的意外：有些代码竟把哈希遍历顺序当作低效的随机数生成器。此时，如果去掉这种随机性，反而会破坏这些用户的代码。正如每个热力学系统中的熵都会增加一样，海勒姆定律适用于每一种可观察行为。

Thinking over the differences between code written with a “works now” and a “works indefinitely” mentality, we can extract some clear relationships. Looking at code as an artifact with a (highly) variable lifetime requirement, we can begin to categorize programming styles: code that depends on brittle and unpublished features of its dependencies is likely to be described as “hacky” or “clever,” whereas code that follows best practices and has planned for the future is more likely to be described as “clean” and “maintainable.” Both have their purposes, but which one you select depends crucially on the expected life span of the code in question. We’ve taken to saying, “It’s programming if ‘clever’ is a compliment, but it’s software engineering if ‘clever’ is an accusation.” 

比较“现在能用”与“长期都能用”这两种心态下写出的代码，可以看出一些清晰的关系。把代码视为使用寿命要求差异极大的产物，就能进一步区分编程风格：依赖底层组件中脆弱、未公开特性的代码，常被称为“取巧”或“聪明”；遵循最佳实践、为未来作好准备的代码，则更可能被称为“整洁”或“可维护”。两者各有用途，如何选择，关键取决于代码的预期生命周期。我们常说：“如果‘聪明’是赞美，那是在谈编程；如果‘聪明’是批评，那是在谈软件工程。”  

### Why Not Just Aim for “Nothing Changes”? 为什么不追求“一切不变”？

Implicit in all of this discussion of time and the need to react to change is the assumption that change might be necessary. Is it?

前面关于时间和应对变化的讨论，都隐含着一个假设：变更可能是必要的。真是这样吗？

As with effectively everything else in this book, it depends. We’ll readily commit to “For most projects, over a long enough time period, everything underneath them might need to be changed.” If you have a project written in pure C with no external dependencies (or only external dependencies that promise great long-term stability, like POSIX), you might well be able to avoid any form of refactoring or difficult upgrade. C does a great job of providing stability—in many respects, that is its primary purpose.

和本书中几乎所有其他问题一样，答案取决于具体情况。我们可以明确地说：“对大多数项目而言，只要时间足够长，其底层的一切都可能需要改变。”如果项目完全用 C 编写，没有外部依赖，或者只依赖 POSIX 这类承诺长期稳定的接口，你确实可能不必进行任何重构或棘手的升级。C 在保持稳定性方面做得很好；从许多方面看，这正是它的主要目标。

Most projects have far more exposure to shifting underlying technology. Most programming languages and runtimes change much more than C does. Even libraries implemented in pure C might change to support new features, which can affect downstream users. Security problems are disclosed in all manner of technology, from processors to networking libraries to application code. Every piece of technology upon which your project depends has some (hopefully small) risk of containing critical bugs and security vulnerabilities that might come to light only after you’ve started relying on it. If you are incapable of deploying a patch for Heartbleed or mitigating speculative execution problems like Meltdown and Spectre because you’ve assumed (or promised) that nothing will ever change, that is a significant gamble.

但大多数项目面对的底层技术，变化远比这频繁。大多数编程语言和运行时都比 C 变化得多；即使完全用 C 实现的库，也可能为了支持新功能而变更，从而影响下游用户。从处理器、网络库到应用代码，各类技术都可能被发现存在安全问题。项目依赖的每一项技术，都可能包含严重缺陷或安全漏洞（希望这种风险很小），而这些问题可能在你开始依赖它之后才暴露出来。如果因为假定或承诺“一切都不会变”，就无法部署 Heartbleed（心脏出血）的补丁，或缓解 Meltdown（熔毁）、Spectre（幽灵）这类推测执行漏洞，那就是在冒很大的风险。

Efficiency improvements further complicate the picture. We want to outfit our datacenters with cost-effective computing equipment, especially enhancing CPU efficiency. However, algorithms and data structures from early-day Google are simply less efficient on modern equipment: a linked-list or a binary search tree will still work fine, but the ever-widening gap between CPU cycles versus memory latency impacts what “efficient” code looks like. Over time, the value in upgrading to newer hardware can be diminished without accompanying design changes to the software. Backward compatibility ensures that older systems still function, but that is no guarantee that old optimizations are still helpful. Being unwilling or unable to take advantage of such opportunities risks incurring large costs. Efficiency concerns like this are particularly subtle: the original design might have been perfectly logical and following reasonable best practices. It’s only after an evolution of backward-compatible changes that a new, more efficient option becomes important. No mistakes were made, but the passage of time still made change valuable.

效率提升又让问题更复杂。我们希望为数据中心配置性价比更高的计算设备，尤其是提高 CPU 效率。然而，谷歌早期采用的算法和数据结构，在现代硬件上未必高效：链表和二叉搜索树仍然能正常工作，但 CPU 周期与内存访问延迟之间不断扩大的差距，已经改变了“高效代码”的标准。随着时间推移，如果不相应调整软件设计，升级硬件的收益就可能打折。向后兼容只能保证旧系统仍能运行，不能保证旧的优化仍然有效。不愿或不能利用这些机会，可能造成高昂成本。这类效率问题尤其微妙：最初的设计可能完全合理，也遵循了当时的最佳实践；只是经历一系列向后兼容的变化后，新的高效方案才变得重要。没有人犯错，时间本身却让变更产生了价值。

Concerns like those just mentioned are why there are large risks for long-term projects that haven’t invested in sustainability. We must be capable of responding to these sorts of issues and taking advantage of these opportunities, regardless of whether they directly affect us or manifest in only the transitive closure of technology we build upon. Change is not inherently good. We shouldn’t change just for the sake of change. But we do need to be capable of change. If we allow for that eventual necessity, we should also consider whether to invest in making that capability cheap. As every system administrator knows, it’s one thing to know in theory that you can recover from tape, and another to know in practice exactly how to do it and how much it will cost when it becomes necessary. Practice and expertise are great drivers of efficiency and reliability.

这些问题说明，长期项目如果没有为可持续性投入资源，就会面临很大风险。无论问题直接影响我们，还是只出现在所依赖技术的传递闭包中，我们都必须有能力应对，并利用其中的机会。**变更本身并不意味着好处**。我们不该为了改变而改变，但必须具备改变的能力。既然最终可能需要这种能力，就还应考虑是否投入资源，降低使用它的成本。系统管理员都知道：理论上知道可以从磁带恢复数据，与实际掌握恢复步骤、清楚必要时要付出多少成本，是两回事。实践和专业知识能显著提高效率与可靠性。

## Scale and Efficiency  规模和效率

As noted in the Site Reliability Engineering (SRE) book,[^11] Google’s production system as a whole is among the most complex machines created by humankind. The complexity involved in building such a machine and keeping it running smoothly has required countless hours of thought, discussion, and redesign from experts across our organization and around the globe. So, we have already written a book about the complexity of keeping that machine running at that scale.

正如《Site Reliability Engineering》（SRE，站点可靠性工程）一书所述，谷歌的整个生产系统，是人类创造的最复杂的机器之一。要构建这样一台机器并让它平稳运行，需要组织内部及世界各地的专家投入无数小时，反复思考、讨论和重新设计。关于如何在这种规模下维持系统运行，以及其中的复杂性，我们已经写过一本书。

Much of this book focuses on the complexity of scale of the organization that produces such a machine, and the processes that we use to keep that machine running over time. Consider again the concept of codebase sustainability: “Your organization’s codebase is sustainable when you are able to change all of the things that you ought to change, safely, and can do so for the life of your codebase.” Hidden in the discussion of capability is also one of costs: if changing something comes at inordinate cost, it will likely be deferred. If costs grow superlinearly over time, the operation clearly is not scalable.[^12] Eventually, time will take hold and something unexpected will arise that you absolutely must change. When your project doubles in scope and you need to perform that task again, will it be twice as labor intensive? Will you even have the human resources required to address the issue next time?

本书则更多地关注另一种复杂性：构建这样一台机器的组织，其规模如何增长，以及我们采用什么流程让机器长期运行。再看代码库可持续性的定义：“如果组织能够在代码库的整个生命周期内，安全地完成所有应当完成的变更，代码库就是可持续的。”能力问题背后还有成本问题：如果变更的代价过高，人们很可能会推迟它。如果成本随时间呈超线性增长，这项工作显然就不具备可扩展性。随着时间推移，终究会出现意想不到、又不得不处理的变更。当项目范围变为原来的两倍，再做同一项工作时，人力投入也要翻倍吗？下一次，你是否还能找到足够的人手？

Human costs are not the only finite resource that needs to scale. Just as software itself needs to scale well with traditional resources such as compute, memory, storage, and bandwidth, the development of that software also needs to scale, both in terms of human time involvement and the compute resources that power your development workflow. If the compute cost for your test cluster grows superlinearly, consuming more compute resources per person each quarter, you’re on an unsustainable path and need to make changes soon.

需要随规模增长而妥善管理的有限资源，不只有人力。软件本身要在计算、内存、存储和带宽等传统资源上具备良好的可扩展性；软件开发过程也一样，既要考虑工程师投入的时间，也要考虑支撑开发工作流的计算资源。如果测试集群的计算成本呈超线性增长，人均资源消耗每个季度都在增加，那么这种发展方式就是不可持续的，需要尽快调整。

Finally, the most precious asset of a software organization—the codebase itself—also needs to scale. If your build system or version control system scales superlinearly over time, perhaps as a result of growth and increasing changelog history, a point might come at which you simply cannot proceed. Many questions, such as “How long does it take to do a full build?”, “How long does it take to pull a fresh copy of the repository?”, or “How much will it cost to upgrade to a new language version?” aren’t actively monitored and change at a slow pace. They can easily become like the metaphorical boiled frog; it is far too easy for problems to worsen slowly and never manifest as a singular moment of crisis. Only with an organization-wide awareness and commitment to scaling are you likely to keep on top of these issues.

最后，软件组织最宝贵的资产，也就是*代码库*本身，同样需要具备可扩展性。如果随着代码增长和变更历史积累，构建系统或版本控制系统的开销呈超线性增长，最终可能会让工作无法继续。“完整构建需要多久？”“获取一份新的代码仓库副本需要多久？”“升级到新的语言版本要付出多少成本？”这些指标往往没有受到持续监测，而且变化缓慢。它们很容易变成“温水煮青蛙”式的问题：状况不断恶化，却从未出现一个明显的危机时刻。只有整个组织都认识到可扩展性的重要性，并持续投入，才可能控制住这些问题。

Everything your organization relies upon to produce and maintain code should be scalable in terms of overall cost and resource consumption. In particular, everything your organization must do repeatedly should be scalable in terms of human effort. Many common policies don’t seem to be scalable in this sense.

组织用于开发和维护代码的一切，都应当在总成本和资源消耗上具备可扩展性。尤其是必须反复完成的工作，其人力投入更应如此。按这个标准看，许多常见策略并不具备可扩展性。

> [^11]: Beyer, B. et al. Site Reliability Engineering: How Google Runs Production Systems. (Boston: O’Reilly Media,2016).
>
> Beyer, B. 等，《站点可靠性工程：谷歌如何运行生产系统》（波士顿：O'Reilly Media，2016）。
>
> [^12]: Whenever we use “scalable” in an informal context in this chapter, we mean “sublinear scaling with regard to human interactions.”
>
> 本章在非正式语境中使用“可扩展”时，指的是“所需的人际交互量随规模呈次线性增长”。

### Policies That Don’t Scale 难以随规模扩展的策略

With a little practice, it becomes easier to spot policies with bad scaling properties. Most commonly, these can be identified by considering the work imposed on a single engineer and imagining the organization scaling up by 10 or 100 times. When we are 10 times larger, will we add 10 times more work with which our sample engineer needs to keep up? Does the amount of work our engineer must perform grow as a function of the size of the organization? Does the work scale up with the size of the codebase? If either of these are true, do we have any mechanisms in place to automate or optimize that work? If not, we have scaling problems.

稍加练习，就能更容易地识别难以随规模扩展的策略。一个常用方法是：先看它给一名工程师带来了多少工作，再设想组织规模变为原来的10倍或100倍。当组织达到原来的10倍时，这名工程师需要应付的工作也会变成10倍吗？他的工作量是否取决于组织规模，或随着代码库增大而增加？只要其中一项成立，就应该继续问：有没有机制可以自动化或优化这些工作？如果没有，就存在规模扩展问题。

Consider a traditional approach to deprecation. We discuss deprecation much more in Chapter 15, but the common approach to deprecation serves as a great example of scaling problems. A new Widget has been developed. The decision is made that everyone should use the new one and stop using the old one. To motivate this, project leads say “We’ll delete the old Widget on August 15th; make sure you’ve converted to the new Widget.”

传统的弃用方式就是一个例子。第15章会详细讨论弃用，这里先用常见做法说明规模问题。假设团队开发了一个新的组件，并决定所有人都应停用旧组件、改用新的。为了推动迁移，项目负责人宣布：“我们将在8月15日删除旧组件，请务必在此之前完成迁移。”

This type of approach might work in a small software setting but quickly fails as both the depth and breadth of the dependency graph increases. Teams depend on an ever- increasing number of Widgets, and a single build break can affect a growing percentage of the company. Solving these problems in a scalable way means changing the way we do deprecation: instead of pushing migration work to customers, teams can internalize it themselves, with all the economies of scale that provides.

这种做法在小规模软件环境中或许可行，但随着依赖图的深度和广度增加，很快就会失效。团队依赖的组件越来越多，一次构建失败就可能波及公司更大比例的团队。要以可扩展的方式解决问题，就需要改变弃用流程：由组件维护团队自行承担迁移工作，而不是把它推给使用方，从而获得规模经济带来的收益。

In 2012, we tried to put a stop to this with rules mitigating churn: infrastructure teams must do the work to move their internal users to new versions themselves or do the update in place, in backward-compatible fashion. This policy, which we’ve called the “Churn Rule,” scales better: dependent projects are no longer spending progressively greater effort just to keep up. We’ve also learned that having a dedicated group of experts execute the change scales better than asking for more maintenance effort from every user: experts spend some time learning the whole problem in depth and then apply that expertise to every subproblem. Forcing users to respond to churn means that every affected team does a worse job ramping up, solves their immediate problem, and then throws away that now-useless knowledge. Expertise scales better.   

2012年，我们尝试通过一项减少变更适配负担的规则来扭转这种局面：**基础设施团队必须自行将内部用户迁移到新版本，或以向后兼容的方式原地更新**。我们将它称为“变更适配规则”（Churn Rule）。这一策略更具可扩展性，因为依赖这些组件的项目不必为了跟上更新而不断增加投入。我们也发现，让一组专门的专家执行变更，比要求每个用户额外投入维护工作更容易随规模扩展。专家先花时间深入理解整个问题，再把这些知识用于各个子问题。反之，迫使用户自行适配变更，会让每个受影响的团队都低效地重新学习一遍，解决眼前问题后，又把短期内用不上的知识抛在一边。专业知识更能发挥规模效益。  

The traditional use of development branches is another example of policy that has built-in scaling problems. An organization might identify that merging large features into trunk has destabilized the product and conclude, “We need tighter controls on when things merge. We should merge less frequently.” This leads quickly to every team or every feature having separate dev branches. Whenever any branch is decided to be “complete,” it is tested and merged into trunk, triggering some potentially expensive work for other engineers still working on their dev branch, in the form of resyncing and testing. Such branch management can be made to work for a small organization juggling 5 to 10 such branches. As the size of an organization (and the number of branches) increases, it quickly becomes apparent that we’re paying an ever-increasing amount of overhead to do the same task. We’ll need a different approach as we scale up, and we discuss that in Chapter 16.

传统的开发分支管理，也内含规模扩展问题。组织可能发现，大功能合入主干后影响了产品稳定性，于是得出结论：“必须更严格地控制合并时机，降低合并频率。”很快，每个团队或每项功能都有了独立的开发分支。某个分支一旦被认为已经“完成”，就会经过测试后合入主干；仍在其他分支上工作的工程师，则可能需要付出很大代价来重新同步和测试。对只需同时管理5到10个分支的小型组织而言，这种方式也许可行。但随着组织和分支数量增加，完成同样的工作所需的额外开销也会不断上升。规模扩大后，需要换一种方法，第16章将详细讨论。

### Policies That Scale Well 适于规模扩展的策略

What sorts of policies result in better costs as the organization grows? Or, better still, what sorts of policies can we put in place that provide superlinear value as the organization grows?

那么，什么样的策略能让成本在组织增长时保持合理？更进一步，有没有策略能让价值随着组织增长而呈超线性提升？

One of our favorite internal policies is a great enabler of infrastructure teams, protecting their ability to make infrastructure changes safely. “If a product experiences outages or other problems as a result of infrastructure changes, but the issue wasn’t surfaced by tests in our Continuous Integration (CI) system, it is not the fault of the infrastructure change.” More colloquially, this is phrased as “If you liked it, you should have put a CI test on it,” which we call “The Beyoncé Rule.”[^13] From a scaling perspective, the Beyoncé Rule implies that complicated, one-off bespoke tests that aren’t triggered by our common CI system do not count. Without this, an engineer on an infrastructure team could conceivably need to track down every team with any affected code and ask them how to run their tests. We could do that when there were a hundred engineers. We definitely cannot afford to do that anymore.

我们很看重的一项内部策略，为基础设施团队安全实施变更提供了有力保障：“如果基础设施变更导致产品停机或出现其他问题，但问题没有被持续集成（CI）系统中的测试发现，就不能把责任归咎于这次基础设施变更。”通俗的说法是：“既然你在意它，就应该给它写一个 CI 测试。”我们称之为“碧昂斯规则”。从可扩展性的角度看，那些复杂、临时定制、不会由统一 CI 系统触发的测试，不能算作这里要求的测试。否则，基础设施工程师可能需要逐一找到所有代码受影响的团队，询问各自的测试如何运行。只有一百名工程师时，我们还做得到；如今已承担不起这样的成本。

We’ve found that expertise and shared communication forums offer great value as an organization scales. As engineers discuss and answer questions in shared forums, knowledge tends to spread. New experts grow. If you have a hundred engineers writing Java, a single friendly and helpful Java expert willing to answer questions will soon produce a hundred engineers writing better Java code. Knowledge is viral, experts are carriers, and there’s a lot to be said for the value of clearing away the common stumbling blocks for your engineers. We cover this in greater detail in Chapter 3.

我们发现，专业知识和公共交流平台能在组织扩大时带来巨大价值。工程师在共同的论坛中讨论、答疑，知识便随之传播，新的专家也逐渐成长。如果有100名工程师在写 Java，一位友善、乐于答疑的 Java 专家，很快就能帮助这100人写出更好的 Java 代码。知识能够像病毒一样传播，专家就是传播者。为工程师清除共同的障碍，价值不容小觑。第3章将更详细地讨论这一点。

> [^13]: This is a reference to the popular song “Single Ladies,” which includes the refrain “If you liked it then you shoulda put a ring on it.”
>
> 这里借用了流行歌曲《Single Ladies》（单身女士）的副歌：“如果你喜欢她，就该为她戴上戒指。”

### Example: Compiler Upgrade 示例：编译器升级

Consider the daunting task of upgrading your compiler. Theoretically, a compiler upgrade should be cheap given how much effort languages take to be backward compatible, but how cheap of an operation is it in practice? If you’ve never done such an upgrade before, how would you evaluate whether your codebase is compatible with that change?

再看升级编译器这项艰巨的工作。编程语言为了保持向后兼容投入了大量努力，按理说，升级编译器的成本应该很低。但在实践中，究竟有多低？如果从未做过这样的升级，你会如何判断代码库能否兼容这次变更？

In our experience, language and compiler upgrades are subtle and difficult tasks even when they are broadly expected to be backward compatible. A compiler upgrade will almost always result in minor changes to behavior: fixing miscompilations, tweaking optimizations, or potentially changing the results of anything that was previously undefined. How would you evaluate the correctness of your entire codebase against all of these potential outcomes?

根据我们的经验，即使普遍预期语言和编译器升级能够向后兼容，这项工作仍然细节繁多、困难重重。编译器升级几乎总会带来细微的行为变化，例如修复错误编译、调整优化，或改变原本行为未定义的代码所产生的结果。面对所有这些可能性，你该如何评估整个代码库是否仍然正确？

The most storied compiler upgrade in Google’s history took place all the way back in 2006. At that point, we had been operating for a few years and had several thousand engineers on staff. We hadn’t updated compilers in about five years. Most of our engineers had no experience with a compiler change. Most of our code had been exposed to only a single compiler version. It was a difficult and painful task for a team of (mostly) volunteers, which eventually became a matter of finding shortcuts and simplifications in order to work around upstream compiler and language changes that we didn’t know how to adopt.[^14] In the end, the 2006 compiler upgrade was extremely painful. Many Hyrum’s Law problems, big and small, had crept into the codebase and served to deepen our dependency on a particular compiler version. Breaking those implicit dependencies was painful. The engineers in question were taking a risk: we didn’t have the Beyoncé Rule yet, nor did we have a pervasive CI system, so it was difficult to know the impact of the change ahead of time or be sure they wouldn’t be blamed for regressions.

谷歌历史上最为人津津乐道的一次编译器升级，可以追溯到2006年。当时，公司已运营数年，有数千名工程师，而编译器大约五年没有更新过。多数工程师没有经历过编译器变更，多数代码也只用一个编译器版本构建过。对于主要由志愿者组成的团队，这是一项艰难而痛苦的任务。到后来，团队只能寻找捷径和简化办法，绕过那些不知道如何适应的上游编译器及语言变化。总之，2006年的升级异常痛苦。大大小小的海勒姆定律问题早已渗入代码库，加深了代码对特定编译器版本的依赖，而打破这些隐式依赖并不容易。参与的工程师还承担着风险：那时没有碧昂斯规则，也没有覆盖广泛的 CI 系统，很难事先掌握变更影响，更无法保证自己不会因回归缺陷受到指责。

This story isn’t at all unusual. Engineers at many companies can tell a similar story about a painful upgrade. What is unusual is that we recognized after the fact that the task had been painful and began focusing on technology and organizational changes to overcome the scaling problems and turn scale to our advantage: automation (so that a single human can do more), consolidation/consistency (so that low-level changes have a limited problem scope), and expertise (so that a few humans can do more).

这样的经历并不罕见，许多公司的工程师都能讲出类似的痛苦升级故事。不同之处在于，我们事后认识到了问题，开始从技术和组织两方面着手，克服规模带来的困难，并把规模转化为优势：通过自动化让一个人完成更多工作；通过整合与一致性，限制底层变更涉及的问题范围；通过专业知识，让少数人完成更多工作。

The more frequently you change your infrastructure, the easier it becomes to do so. We have found that most of the time, when code is updated as part of something like a compiler upgrade, it becomes less brittle and easier to upgrade in the future. In an ecosystem in which most code has gone through several upgrades, it stops depending on the nuances of the underlying implementation; instead, it depends on the actual abstraction guaranteed by the language or OS. Regardless of what exactly you are upgrading, expect the first upgrade for a codebase to be significantly more expensive than later upgrades, even controlling for other factors.

基础设施变更做得越频繁，后续变更就越容易。我们发现，代码在编译器升级等工作中得到更新后，大多会变得不那么脆弱，也更容易再次升级。当一个生态系统中的多数代码已经经历过多次升级，它们就不再依赖底层实现的细枝末节，而是依赖语言或操作系统真正保证的抽象。无论升级什么，即使排除其他因素的影响，代码库的首次升级也往往比后续升级昂贵得多。

> [^14]: Specifically, interfaces from the C++ standard library needed to be referred to in namespace std, and an optimization change for std::string turned out to be a significant pessimization for our usage, thus requiring some additional workarounds.
>
> 具体来说，C++ 标准库接口需要通过 std 命名空间引用；对 std::string 的一项优化，在我们的使用场景下反而显著降低了性能，因此还需要额外的变通处理。

Through this and other experiences, we’ve discovered many factors that affect the flexibility of a codebase:

- *Expertise*  
    We know how to do this; for some languages, we’ve now done hundreds of compiler upgrades across many platforms.
- *Stability*  
    There is less change between releases because we adopt releases more regularly; for some languages, we’re now deploying compiler upgrades every week or two.
- *Conformity*  
    There is less code that hasn’t been through an upgrade already, again because we are upgrading regularly.
- *Familiarity*  
    Because we do this regularly enough, we can spot redundancies in the process of performing an upgrade and attempt to automate. This overlaps significantly with SRE views on toil.[^15]
- *Policy*  
    We have processes and policies like the Beyoncé Rule. The net effect of these processes is that upgrades remain feasible because infrastructure teams do not need to worry about every unknown usage, only the ones that are visible in our CI systems.

这些经历让我们认识到，代码库的灵活性受许多因素影响：

- *专业知识*
    我们已经掌握了方法。对于某些语言，我们在多个平台上累计完成了数百次编译器升级。
- *稳定性*  
    升级更规律，相邻两次升级之间的变化就更少。对于某些语言，我们现在每隔一两周就部署一次编译器升级。
- *一致性*  
    由于定期升级，从未经历过升级的代码越来越少。
- *熟悉程度*  
    经常执行升级，让我们能识别流程中的重复劳动，并尝试将其自动化。这与 SRE 对 toil（琐务）的看法有很大共通之处。
- *策略*  
    我们建立了碧昂斯规则等流程和策略。它们共同保证了升级仍然可行：基础设施团队只需关注 CI 系统中可见的使用方式，不必为每一种未知用法负责。

The underlying lesson is not about the frequency or difficulty of compiler upgrades, but that as soon as we became aware that compiler upgrade tasks were necessary, we found ways to make sure to perform those tasks with a constant number of engineers, even as the codebase grew.[^16] If we had instead decided that the task was too expensive and should be avoided in the future, we might still be using a decade-old compiler version. We would be paying perhaps 25% extra for computational resources as a result of missed optimization opportunities. Our central infrastructure could be vulnerable to significant security risks given that a 2006-era compiler is certainly not helping to mitigate speculative execution vulnerabilities. Stagnation is an option, but often not a wise one.

这里真正的启示，不是编译器升级应该多频繁或有多困难，而是：一旦确认升级不可避免，我们就找到了办法，即使代码库不断增长，也能由固定数量的工程师完成升级。如果当初认为这项工作太昂贵、今后应该避免，我们可能至今还在使用十年前的编译器，并因错过优化机会而多付约25%的计算资源成本。核心基础设施也可能面临严重的安全风险，毕竟2006年前后的编译器显然无法帮助缓解推测执行漏洞。停滞不前也是一种选择，但往往并不明智。

> [^15]: Beyer et al. Site Reliability Engineering: How Google Runs Production Systems, Chapter 5, “Eliminating Toil.”
>
> Beyer 等，《站点可靠性工程：谷歌如何运行生产系统》，第5章“消除琐务”。
>
> [^16]: In our experience, an average software engineer (SWE) produces a pretty constant number of lines of code per unit time. For a fixed SWE population, a codebase grows linearly—proportional to the count of SWE- months over time. If your tasks require effort that scales with lines of code, that’s concerning.
>
> 根据我们的经验，一名软件工程师（SWE）在单位时间内产出的代码行数大致稳定。如果工程师人数固定，代码库就会随时间线性增长，与累计投入的工程师人月数成正比。如果某项任务所需的工作量也随代码行数增长，就值得警惕。

### Shifting Left  左移

One of the broad truths we’ve seen to be true is the idea that finding problems earlier in the developer workflow usually reduces costs. Consider a timeline of the developer workflow for a feature that progresses from left to right, starting from conception and design, progressing through implementation, review, testing, commit, canary, and eventual production deployment. Shifting problem detection to the “left” earlier on this timeline makes it cheaper to fix than waiting longer, as shown in Figure 1-2.

我们反复观察到一条普遍规律：在开发工作流中越早发现问题，通常成本越低。设想一条从左到右的功能开发时间线：从构思、设计开始，依次经过实现、审查、测试、提交、金丝雀发布，最终部署到生产环境。如图1-2所示，把问题发现的时点向“左”移，也就是更早发现问题，修复成本通常比拖到后面更低。

This term seems to have originated from arguments that security mustn’t be deferred until the end of the development process, with requisite calls to “shift left on security.” The argument in this case is relatively simple: if a security problem is discovered only after your product has gone to production, you have a very expensive problem. If it is caught before deploying to production, it may still take a lot of work to identify and remedy the problem, but it’s cheaper. If you can catch it before the original developer commits the flaw to version control, it’s even cheaper: they already have an understanding of the feature; revising according to new security constraints is cheaper than committing and forcing someone else to triage it and fix it.

“左移”这个术语似乎源于一种主张：安全不能等到开发过程结束后才考虑，因此需要“安全左移”。道理很简单：产品上线后才发现安全问题，处理成本会非常高。上线前发现问题，即使定位和修复仍需大量工作，也会便宜一些。如果在原开发者把缺陷提交到版本控制系统之前就发现，成本会更低：开发者此时仍熟悉该功能，按新的安全约束修改代码，比提交后再让别人排查和修复容易得多。

![*Figure 1-2. Timeline of* *the developer* *workflow*](./images/figure%201-2.png)

The same basic pattern emerges many times in this book. Bugs that are caught by static analysis and code review before they are committed are much cheaper than bugs that make it to production. Providing tools and practices that highlight quality, reliability, and security early in the development process is a common goal for many of our infrastructure teams. No single process or tool needs to be perfect, so we can assume a defense-in-depth approach, hopefully catching as many defects on the left side of the graph as possible.

本书会反复出现同样的模式：在提交前通过静态分析和代码审查发现的缺陷，修复成本远低于流入生产环境的缺陷。许多基础设施团队的共同目标，就是提供工具和实践，在开发早期提醒工程师关注质量、可靠性和安全。任何单一流程或工具都不必完美无缺；我们可以采用纵深防御，争取在时间线左侧尽可能多地发现缺陷。

## Trade-offs and Costs 权衡和成本

If we understand how to program, understand the lifetime of the software we’re maintaining, and understand how to maintain it as we scale up with more engineers producing and maintaining new features, all that is left is to make good decisions. This seems obvious: in software engineering, as in life, good choices lead to good outcomes. However, the ramifications of this observation are easily overlooked. Within Google, there is a strong distaste for “because I said so.” It is important for there to be a decider for any topic and clear escalation paths when decisions seem to be wrong, but the goal is consensus, not unanimity. It’s fine and expected to see some instances of “I don’t agree with your metrics/valuation, but I see how you can come to that conclusion.” Inherent in all of this is the idea that there needs to be a reason for everything; “just because,” “because I said so,” or “because everyone else does it this way” are places where bad decisions lurk. Whenever it is efficient to do so, we should be able to explain our work when deciding between the general costs for two engineering options.

如果我们懂得编程，了解所维护软件的生命周期，也知道当更多工程师加入、不断开发和维护新功能时，该如何在规模增长中持续维护软件，那么剩下的就是作出好的决策。这似乎理所当然：无论软件工程还是生活，好的选择都会带来好的结果。但这句话的含义常被忽略。在谷歌，人们很反感“因为我说了算”。每个议题都应有决策者；如果决策看起来有问题，也应有明确的升级处理渠道。不过，目标是形成共识，而不是要求所有人意见完全一致。“我不同意你的衡量标准或价值判断，但理解你为什么得出这个结论”，这样的情况正常，也在预期之内。核心原则是：做事必须有理由。“反正就这样”“因为我说了算”“别人都这么做”，往往会掩藏糟糕的决策。在比较两种工程方案的各类成本并作出选择时，只要解释过程的成本合理，我们就应当能说明自己的判断依据。

What do we mean by cost? We are not only talking about dollars here. “Cost” roughly translates to effort and can involve any or all of these factors:

- Financial costs (e.g., money)
- Resource costs (e.g., CPU time)
- Personnel costs (e.g., engineering effort)
- Transaction costs (e.g., what does it cost to take action?)
- Opportunity costs (e.g., what does it cost to not take action?)
- Societal costs (e.g., what impact will this choice have on society at large?)

这里的“成本”是什么意思？它不只指金钱，大致可以理解为需要付出的代价，可能涉及以下一项或多项因素：

- 财务成本（如金钱）
- 资源成本（如 CPU 时间）
- 人力成本（如工程师投入的工作量）
- 交易成本（例如，采取行动的成本是多少？）
- 机会成本（例如，不采取行动的成本是多少？）
- 社会成本（例如，这个选择将对整个社会产生什么影响？）

Historically, it’s been particularly easy to ignore the question of societal costs. However, Google and other large tech companies can now credibly deploy products with billions of users. In many cases, these products are a clear net benefit, but when we’re operating at such a scale, even small discrepancies in usability, accessibility, fairness, or potential for abuse are magnified, often to the detriment of groups that are already marginalized. Software pervades so many aspects of society and culture; therefore, it is wise for us to be aware of both the good and the bad that we enable when making product and technical decisions. We discuss this much more in Chapter 4.

过去，人们尤其容易忽略社会成本。但如今，谷歌和其他大型科技公司确实有能力推出服务数十亿用户的产品。很多时候，这些产品总体上利大于弊；然而，在如此大的规模下，可用性、无障碍性、公平性或被滥用的可能性方面，即使只有细微差异，也会被放大，往往进一步损害已经处于边缘地位的群体。软件已渗透社会和文化的许多方面，因此，作出产品和技术决策时，我们应当同时考虑它可能带来的好处与坏处。第4章将详细讨论。

In addition to the aforementioned costs (or our estimate of them), there are biases: status quo bias, loss aversion, and others. When we evaluate cost, we need to keep all of the previously listed costs in mind: the health of an organization isn’t just whether there is money in the bank, it’s also whether its members are feeling valued and productive. In highly creative and lucrative fields like software engineering, financial cost is usually not the limiting factor—personnel cost usually is. Efficiency gains from keeping engineers happy, focused, and engaged can easily dominate other factors, simply because focus and productivity are so variable, and a 10-to-20% difference is easy to imagine.

除了上述成本及其估计，还需要考虑现状偏见、损失厌恶等认知偏差。评估成本时，应把前面列出的各项因素都纳入考虑：组织是否健康，不只看银行账户上有多少钱，还要看成员是否觉得受到重视、能够有效开展工作。在软件工程这样高度依赖创造力、回报又高的领域，限制因素通常不是财务成本，而是人力成本。让工程师保持愉快、专注和投入，所带来的效率收益很容易超过其他因素，因为专注程度和生产力的差异很大，出现10%到20%的差距并不难想象。

### Example: Markers 示例：记号笔

In many organizations, whiteboard markers are treated as precious goods. They are tightly controlled and always in short supply. Invariably, half of the markers at any given whiteboard are dry and unusable. How often have you been in a meeting that was disrupted by lack of a working marker? How often have you had your train of thought derailed by a marker running out? How often have all the markers just gone missing, presumably because some other team ran out of markers and had to abscond with yours? All for a product that costs less than a dollar.

在许多组织里，白板笔被当作贵重物品，管理严格，却总是缺货。随便走到一块白板前，往往就有一半的笔已经干了，无法使用。你有多少次因为找不到能写的白板笔而中断会议？多少次因为笔没墨了而打断思路？又有多少次，所有笔都不见了，大概是别的团队用完了，只好顺走你们的？而这一切，不过是为了一件价格不到一美元的东西。

Google tends to have unlocked closets full of office supplies, including whiteboard markers, in most work areas. With a moment’s notice it is easy to grab dozens of markers in a variety of colors. Somewhere along the line we made an explicit trade- off: it is far more important to optimize for obstacle-free brainstorming than to protect against someone wandering off with a bunch of markers.

谷歌的大多数工作区通常都有不锁门的办公用品柜，里面也包括白板笔。需要时，随手就能拿到几十支不同颜色的笔。我们曾明确作出这样一个取舍：让头脑风暴不受阻碍，远比防止有人拿走一把白板笔重要。

We aim to have the same level of eyes-open and explicit weighing of the cost/benefit trade-offs involved for everything we do, from office supplies and employee perks through day-to-day experience for developers to how to provision and run global- scale services. We often say, “Google is a data-driven culture.” In fact, that’s a simplification: even when there isn’t *data*, there might still be *evidence*, *precedent*, and *argument*. Making good engineering decisions is all about weighing all of the available inputs and making informed decisions about the trade-offs. Sometimes, those decisions are based on instinct or accepted best practice, but only after we have exhausted approaches that try to measure or estimate the true underlying costs.

我们希望对每一件事，都同样清醒、明确地权衡成本与收益：从办公用品、员工福利，到开发者的日常体验，再到全球服务的资源配置和运行。我们常说：“谷歌拥有数据驱动的文化。”其实，这是一种简化说法：即使没有*数据*，也可能有*证据*、*先例*和*论据*。好的工程决策，要综合考虑所有可获得的信息，在充分了解情况后作出取舍。有时，最终仍要依靠直觉或公认的最佳实践，但前提是，我们已经尽力尝试衡量或估计真正的底层成本。

In the end, decisions in an engineering group should come down to very few things:

- We are doing this because we must (legal requirements, customer requirements).
- We are doing this because it is the best option (as determined by some appropriate decider) we can see at the time, based on current evidence.

归根结底，工程团队作出决策的理由应当很简单：

- 我们这样做是因为我们必须这么做（法律要求、客户要求）。
- 我们这样做，是因为根据现有证据，这是当时能找到的最佳方案，并由合适的决策者作出了判断。

Decisions should not be “We are doing this because I said so.”[^17]

决策理由不应是“我们这么做，因为我说了算”。[^17]

> [^17]: This is not to say that decisions need to be made unanimously, or even with broad consensus; in the end, someone must be the decider. This is primarily a statement of how the decision-making process should flow for whoever is actually responsible for the decision.
>
> 这并不意味着决策必须获得一致赞同，甚至不一定需要广泛共识；最终仍须有人拍板。这里主要是在说明，实际负责决策的人应遵循怎样的决策过程。

### Inputs to Decision Making 决策依据

When we are weighing data, we find two common scenarios:

- All of the quantities involved are measurable or can at least be estimated. This usually means that we’re evaluating trade-offs between CPU and network, or dollars and RAM, or considering whether to spend two weeks of engineer-time in order to save N CPUs across our datacenters.
- Some of the quantities are subtle, or we don’t know how to measure them. Sometimes this manifests as “We don’t know how much engineer-time this will take.” Sometimes it is even more nebulous: how do you measure the engineering cost of a poorly designed API? Or the societal impact of a product choice?

权衡数据时，通常会遇到两种情况：

- 涉及的各项数量都能测量，或至少可以估计。例如，在 CPU 和网络、资金和 RAM 之间权衡，或考虑是否值得投入两周的工程师时间，以节省数据中心里的 N 个 CPU。
- 有些因素难以量化，或者我们不知道该如何衡量。有时只是“不知道要投入多少工程师时间”，有时则更难捉摸：设计拙劣的 API 会带来多少工程成本？某项产品选择又会产生怎样的社会影响？

There is little reason to be deficient on the first type of decision. Any software engineering organization can and should track the current cost for compute resources, engineer-hours, and other quantities you interact with regularly. Even if you don’t want to publicize to your organization the exact dollar amounts, you can still produce a conversion table: this many CPUs cost the same as this much RAM or this much network bandwidth.

对于第一类决策，我们没有太多理由做不好。任何软件工程组织，都能够也应当持续掌握计算资源、工程师工时及其他常用资源的当前成本。即使不愿在组织内公开具体金额，也可以提供一张成本换算表：多少 CPU 的成本，相当于多少 RAM 或多少网络带宽。

With an agreed-upon conversion table in hand, every engineer can do their own analysis. “If I spend two weeks changing this linked-list into a higher-performance structure, I’m going to use five gibibytes more production RAM but save two thousand CPUs. Should I do it?” Not only does this question depend upon the relative cost of RAM and CPUs, but also on personnel costs (two weeks of support for a software engineer) and opportunity costs (what else could that engineer produce in two weeks?).

有了共同认可的成本换算表，每位工程师都可以自行分析：“如果我花两周，把这个链表改成性能更高的数据结构，生产环境会多占用5 GiB 的 RAM，但能节省两千个 CPU。我该做吗？”答案不只取决于 RAM 与 CPU 的相对成本，还取决于人力成本（一名软件工程师两周的投入）和机会成本（他用这两周还能完成什么）。

For the second type of decision, there is no easy answer. We rely on experience, leadership, and precedent to negotiate these issues. We’re investing in research to help us quantify the hard-to-quantify (see Chapter 7). However, the best broad suggestion that we have is to be aware that not everything is measurable or predictable and to attempt to treat such decisions with the same priority and greater care. They are often just as important, but more difficult to manage.

第二类决策则没有简单答案。我们需要借助经验、领导者的判断和先例来处理这些问题，也在投入研究，尝试量化那些难以量化的因素（见第7章）。但总体上，最重要的建议是：认识到并非一切都能测量或预测，给予这类决策同等重视，并更加审慎地处理。它们往往同样重要，只是更难把握。

### Example: Distributed Builds 示例：分布式构建

Consider your build. According to completely unscientific Twitter polling, something like 60 to 70% of developers build locally, even with today’s large, complicated builds. This leads directly to nonjokes as illustrated by this “Compiling” comic—how much productive time in your organization is lost waiting for a build? Compare that to the cost to run something like distcc for a small group. Or, how much does it cost to run a small build farm for a large group? How many weeks/months does it take for those costs to be a net win?

看看你的构建流程。一项完全不具科学性的 Twitter 投票显示，即使面对如今大型而复杂的构建，仍有约60%到70%的开发者在本地完成。这让《Compiling》（编译）漫画里的情景，成了不折不扣的现实：组织中究竟有多少本可用于产出的时间，浪费在等待构建上？把这笔成本与为小团队运行 distcc 之类工具的成本比较一下。对于大团队，运行一个小型构建集群又要多少钱？过多少周或多少个月，这笔投入就能带来净收益？

Back in the mid-2000s, Google relied purely on a local build system: you checked out code and you compiled it locally. We had massive local machines in some cases (you could build Maps on your desktop!), but compilation times became longer and longer as the codebase grew. Unsurprisingly, we incurred increasing overhead in personnel costs due to lost time, as well as increased resource costs for larger and more powerful local machines, and so on. These resource costs were particularly troublesome: of course we want people to have as fast a build as possible, but most of the time, a high- performance desktop development machine will sit idle. This doesn’t feel like the proper way to invest those resources.

在2000年代中期，谷歌完全依赖本地构建：检出代码，再在本机编译。有些开发者配备了性能很强的本地机器，甚至能在桌面机上构建 Maps！但随着代码库增长，编译时间越来越长。结果不难预料：等待浪费的时间推高了人力成本，更强大的本地机器也增加了资源成本。后者尤其让人头疼：我们当然希望构建越快越好，但高性能桌面开发机在大部分时间里都处于闲置状态。这显然不像合理的资源投入方式。

Eventually, Google developed its own distributed build system. Development of this system incurred a cost, of course: it took engineers time to develop, it took more engineer time to change everyone’s habits and workflow and learn the new system, and of course it cost additional computational resources. But the overall savings were clearly worth it: builds became faster, engineer-time was recouped, and hardware investment could focus on managed shared infrastructure (in actuality, a subset of our production fleet) rather than ever-more-powerful desktop machines. Chapter 18 goes into more of the details on our approach to distributed builds and the relevant trade-offs.

最终，谷歌开发了自己的分布式构建系统。当然，这也有成本：工程师需要花时间开发，还要花更多时间改变大家的习惯和工作流、学习新系统，此外也需要额外的计算资源。但总体收益显然值得这些投入：构建更快，工程师节省了时间，硬件投资也能转向统一管理的共享基础设施，实际上是生产机群中的一部分，而不必不断购置更强大的桌面机。第18章将详细介绍我们的分布式构建方式及相关权衡。

So, we built a new system, deployed it to production, and sped up everyone’s build. Is that the happy ending to the story? Not quite: providing a distributed build system made massive improvements to engineer productivity, but as time went on, the distributed builds themselves became bloated. What was constrained in the previous case by individual engineers (because they had a vested interest in keeping their local builds as fast as possible) was unconstrained within a distributed build system. Bloated or unnecessary dependencies in the build graph became all too common. When everyone directly felt the pain of a nonoptimal build and was incentivized to be vigilant, incentives were better aligned. By removing those incentives and hiding bloated dependencies in a parallel distributed build, we created a situation in which consumption could run rampant, and almost nobody was incentivized to keep an eye on build bloat. This is reminiscent of Jevons Paradox: consumption of a resource may increase as a response to greater efficiency in its use.

于是，新系统建成、投入生产，所有人的构建都加快了。故事就这样圆满结束了吗？并没有。分布式构建大幅提高了工程师的生产力，但随着时间推移，构建本身又开始膨胀。在本地构建时，工程师有切身动力把构建保持得尽可能快，因此会主动控制其规模；到了分布式系统里，这种约束消失了。构建图中臃肿或不必要的依赖变得十分常见。过去，每个人都直接承受低效构建的代价，也就有动力保持警惕，个人与整体利益较为一致。去掉这种动力，又用并行分布式构建掩盖依赖膨胀后，资源消耗就可能失去控制，却几乎没有人有动力关注它。这让人想起杰文斯悖论（Jevons Paradox）：资源利用效率提高，反而可能导致资源消耗增加。

Overall, the saved costs associated with adding a distributed build system far, far outweighed the negative costs associated with its construction and maintenance. But, as we saw with increased consumption, we did not foresee all of these costs. Having blazed ahead, we found ourselves in a situation in which we needed to reconceptualize the goals and constraints of the system and our usage, identify best practices (small dependencies, machine-management of dependencies), and fund the tooling and maintenance for the new ecosystem. Even a relatively simple trade-off of the form “We’ll spend $$$s for compute resources to recoup engineer time” had unforeseen downstream effects.

总体而言，引入分布式构建系统节省的成本，远远超过了开发和维护它的成本。但资源消耗的增长也说明，我们并未预见所有代价。向前推进后，我们发现必须重新思考系统和使用方式的目标与约束，明确最佳实践，例如控制依赖规模、自动管理依赖，并为这个新生态系统的工具和维护投入资金。即使“花钱购买计算资源，以节省工程师时间”这样看似简单的权衡，也会产生未曾预料的后续影响。

### Example: Deciding Between Time and Scale 示例：在时间与规模之间取舍

Much of the time, our major themes of time and scale overlap and work in conjunction. A policy like the Beyoncé Rule scales well and helps us maintain things over time. A change to an OS interface might require many small refactorings to adapt to, but most of those changes will scale well because they are of a similar form: the OS change doesn’t manifest differently for every caller and every project.

很多时候，时间与规模这两个主题相互交织、共同发挥作用。碧昂斯规则既适于规模扩展，也有助于长期维护。操作系统接口的一次变化，可能需要许多小规模重构来适应，但多数变更都能有效地批量处理，因为它们的形式相近：同一项系统变化，不会对每个调用方、每个项目都呈现出完全不同的影响。

Occasionally time and scale come into conflict, and nowhere so clearly as in the basic question: should we add a dependency or fork/reimplement it to better suit our local needs?

但时间和规模有时也会冲突，最明显的例子就是：应该直接引入一个依赖，还是创建它的分叉或重新实现，以更好地满足自身需求？

This question can arise at many levels of the software stack because it is regularly the case that a bespoke solution customized for your narrow problem space may outperform the general utility solution that needs to handle all possibilities. By forking or reimplementing utility code and customizing it for your narrow domain, you can add new features with greater ease, or optimize with greater certainty, regardless of whether we are talking about a microservice, an in-memory cache, a compression routine, or anything else in our software ecosystem. Perhaps more important, the control you gain from such a fork isolates you from changes in your underlying dependencies: those changes aren’t dictated by another team or third-party provider. You are in control of how and when to react to the passage of time and necessity to change.

软件栈的许多层面都会遇到这个问题。针对特定小范围问题定制的方案，往往可能优于需要兼顾各种情况的通用方案。无论对象是微服务、内存缓存、压缩例程，还是生态系统中的其他部分，通过创建通用代码的分叉或重新实现，再针对自身领域定制，都可以更容易地添加功能，也更有把握地优化。也许更重要的是，分叉带来的控制权，能让你不必被动跟随底层依赖的变更：不再由其他团队或第三方供应商决定如何变化，而是由你自行决定，何时、以何种方式应对时间推移带来的变更需求。

```txt
[一条微博引发的思考——再谈“Software Stack”之“软件栈”译法！](https://www.ituring.com.cn/article/1144)
软件栈（Software Stack），是指为了实现某种完整功能解决方案（例如某款产品或服务）所需的一套软件子系统或组件。
```

On the other hand, if every developer forks everything used in their software project instead of reusing what exists, scalability suffers alongside sustainability. Reacting to a security issue in an underlying library is no longer a matter of updating a single dependency and its users: it is now a matter of identifying every vulnerable fork of that dependency and the users of those forks.

另一方面，如果每个开发者都为项目用到的一切创建分叉，而不是复用现有实现，可扩展性和可持续性都会受损。底层库出现安全问题时，就不再只是更新一个依赖及其使用方，而必须找出这个依赖所有存在漏洞的分叉，以及每个分叉的使用方。

As with most software engineering decisions, there isn’t a one-size-fits-all answer to this situation. If your project life span is short, forks are less risky. If the fork in question is provably limited in scope, that helps, as well—avoid forks for interfaces that could operate across time or project-time boundaries (data structures, serialization formats, networking protocols). Consistency has great value, but generality comes with its own costs, and you can often win by doing your own thing—if you do it carefully.

和大多数软件工程决策一样，这个问题没有通用答案。如果项目生命周期很短，分叉的风险就较小；如果能够证明分叉的影响范围有限，风险也会降低。对于可能跨越时间或项目时间边界的接口，例如数据结构、序列化格式和网络协议，应避免创建分叉。一致性很有价值，但通用性也有成本。只要足够审慎，自行实现往往也能获得收益。

## Revisiting Decisions, Making Mistakes 重审决策与犯错

One of the unsung benefits of committing to a data-driven culture is the combined ability and necessity of admitting to mistakes. A decision will be made at some point, based on the available data—hopefully based on good data and only a few assumptions, but implicitly based on currently available data. As new data comes in, contexts change, or assumptions are dispelled, it might become clear that a decision was in error or that it made sense at the time but no longer does. This is particularly critical for a long-lived organization: time doesn’t only trigger changes in technical dependencies and software systems, but in data used to drive decisions.

坚持数据驱动文化，有一个常被忽视的好处：组织既有能力，也有必要承认错误。每项决策都基于作出决策时可获得的数据；我们希望数据可靠、假设尽量少，但归根结底，用的仍然只是当时的数据。随着新数据出现、情境改变或假设被推翻，我们可能发现原决策有误，或者它当时合理，如今却已不再适用。对于长期存在的组织，这一点尤为重要：时间不只会改变技术依赖和软件系统，也会改变决策所依据的数据。

We believe strongly in data informing decisions, but we recognize that the data will change over time, and new data may present itself. This means, inherently, that decisions will need to be revisited from time to time over the life span of the system in question. For long-lived projects, it’s often critical to have the ability to change directions after an initial decision is made. And, importantly, it means that the deciders need to have the right to admit mistakes. Contrary to some people’s instincts, leaders who admit mistakes are more respected, not less.

我们坚信应当用数据辅助决策，也承认数据会随时间改变，还可能出现新的数据。这意味着，在系统的生命周期内，必须不时重新审视决策。对长期项目而言，初始决策之后仍有能力改变方向，往往至关重要。更重要的是，决策者必须有承认错误的权利。与一些人的直觉相反，承认错误的领导者会赢得更多尊重，而不是更少。

Be evidence driven, but also realize that things that can’t be measured may still have value. If you’re a leader, that’s what you’ve been asked to do: exercise judgement, assert that things are important. We’ll speak more on leadership in Chapters 5 and 6.

要以证据为依据，也要认识到，无法衡量的东西仍可能有价值。如果你是领导者，运用判断力、指出哪些事重要，正是你的职责。第5章和第6章会进一步讨论领导力。

## Software Engineering Versus Programming 软件工程与编程

When presented with our distinction between software engineering and programming, you might ask whether there is an inherent value judgement in play. Is programming somehow worse than software engineering? Is a project that is expected to last a decade with a team of hundreds inherently more valuable than one that is useful for only a month and built by two people?

看到我们对软件工程和编程的区分，你可能会问：这是否隐含了价值判断？编程就比软件工程差吗？一个由数百人开发、预计要使用十年的项目，难道天然比两个人开发、只需使用一个月的项目更有价值？

Of course not. Our point is not that software engineering is superior, merely that these represent two different problem domains with distinct constraints, values, and best practices. Rather, the value in pointing out this difference comes from recognizing that some tools are great in one domain but not in the other. You probably don’t need to rely on integration tests (see Chapter 14) and Continuous Deployment (CD) practices (see Chapter 24) for a project that will last only a few days. Similarly, all of our long-term concerns about semantic versioning (SemVer) and dependency management in software engineering projects (see Chapter 21) don’t really apply for short-term programming projects: use whatever is available to solve the task at hand.

当然不是。我们不是说软件工程更优越，而是说它们属于两个不同的问题领域，各有约束、价值和最佳实践。指出区别的意义，在于认识到：某些工具适合一个领域，却未必适合另一个。只需存在几天的项目，大概不必依靠集成测试（见第14章）和持续部署（CD）实践（见第24章）。同样，软件工程项目中有关语义化版本管理（SemVer）和依赖管理的长期考量（见第21章），对短期编程项目并不真正适用：使用现有可用的手段，解决眼前任务即可。

We believe it is important to differentiate between the related-but-distinct terms “programming” and “software engineering.” Much of that difference stems from the management of code over time, the impact of time on scale, and decision making in the face of those ideas. Programming is the immediate act of producing code. Software engineering is the set of policies, practices, and tools that are necessary to make that code useful for as long as it needs to be used and allowing collaboration across a team.

我们认为，有必要区分“编程”与“软件工程”这两个相关但不同的概念。差异很大程度上来自长期代码管理、时间对规模的影响，以及面对这些因素时如何决策。编程是直接编写代码的活动；软件工程则是一整套策略、实践和工具，既让代码在需要它的整个期间持续发挥作用，也支持团队协作。

## Conclusion 总结

This book discusses all of these topics: policies for an organization and for a single programmer, how to evaluate and refine your best practices, and the tools and technologies that go into maintainable software. Google has worked hard to have a sustainable codebase and culture. We don’t necessarily think that our approach is the one true way to do things, but it does provide proof by example that it can be done. We hope it will provide a useful framework for thinking about the general problem: how do you maintain your code for as long as it needs to keep working?

本书将讨论这些主题：适用于组织和单个程序员的策略，评估并改进最佳实践的方法，以及构建可维护软件所需的工具和技术。谷歌一直努力建立可持续的代码库与文化。我们并不认为自己的方法是唯一正确的道路，但它至少提供了一个实例，证明这些目标能够实现。希望本书能提供一个有用的思考框架，帮助你回答这个普遍问题：如何维护代码，让它在需要运行的整个期间都能持续工作？

## TL;DRs  内容提要

- Software engineering” differs from “programming” in dimensionality: programming is about producing code. Software engineering extends that to include the maintenance of that code for its useful life span.
- There is a factor of at least 100,000 times between the life spans of short-lived code and long-lived code. It is silly to assume that the same best practices apply universally on both ends of that spectrum.
- Software is sustainable when, for the expected life span of the code, we are capable of responding to changes in dependencies, technology, or product requirements. We may choose to not change things, but we need to be capable.
- Hyrum’s Law: with a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody.
- Every task your organization has to do repeatedly should be scalable (linear or better) in terms of human input. Policies are a wonderful tool for making process scalable.
- Process inefficiencies and other software-development tasks tend to scale up slowly. Be careful about boiled-frog problems.
- Expertise pays off particularly well when combined with economies of scale.
- "Because I said so"” is a terrible reason to do things.
- Being data driven is a good start, but in reality, most decisions are based on a mix of data, assumption, precedent, and argument. It’s best when objective data makes up the majority of those inputs, but it can rarely be all of them.
- Being data driven over time implies the need to change directions when the data changes (or when assumptions are dispelled). Mistakes or revised plans are inevitable.

- “软件工程”与“编程”处在不同的维度：编程关注编写代码，软件工程则进一步关注代码在整个有效使用期内的维护。
- 短生命周期代码与长生命周期代码的使用寿命，至少可以相差100,000倍。假定同一套最佳实践适用于这两个极端，并不明智。
- 如果在代码的预期生命周期内，我们有能力应对依赖、技术或产品需求的变化，软件就是可持续的。可以选择不变，但不能没有改变的能力。
- 海勒姆定律：只要 API 的用户足够多，不论你在契约中作了什么承诺，系统的每一种可观察行为都会被某些用户依赖。
- 组织必须反复执行的每项任务，其人力投入都应具备可扩展性，即随规模线性增长或更慢。策略是让流程具备可扩展性的有力工具。
- 流程低效问题和其他软件开发任务的规模，往往会缓慢增长。要警惕“温水煮青蛙”式的问题。
- 当专业知识与规模经济相结合时，回报尤其丰厚。
- “因为我说了算”是个糟糕的做事理由。
- 数据驱动是好的起点，但实际决策通常还需要结合假设、先例和论据。客观数据最好占主要部分，却很少能成为全部依据。
- 长期坚持数据驱动，就意味着数据变化或假设被推翻时，需要调整方向。犯错和修订计划都不可避免。
