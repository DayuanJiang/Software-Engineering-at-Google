
**CHAPTER 24**

# Continuous Delivery

# 第二十四章 持续交付

**Written by adha Narayan, Bobbi Jones, Sheri Shipe, and David Owens**

**Edited by Lisa Carey**

Given how quickly and unpredictably the technology landscape shifts, the competitive advantage for any product lies in its ability to quickly go to market. An organization’s velocity is a critical factor in its ability to compete with other players, maintain product and service quality, or adapt to new regulation. This velocity is bottlenecked by the time to deployment. Deployment doesn’t just happen once at initial launch. There is a saying among educators that no lesson plan survives its first contact with the student body. In much the same way, no software is perfect at first launch, and the only guarantee is that you’ll have to update it. Quickly.

技术格局变化迅速，而且难以预测，因此，任何产品的竞争优势都在于迅速推向市场的能力。组织的行动速度，是其能否参与竞争、保持产品和服务质量、适应新法规的关键因素，而完成部署所需的时间就是速度的瓶颈。部署并不是首次上线时做一次就够了。教育工作者有句话：任何教案第一次用到学生身上后，都免不了要调整。软件也是如此：没有软件在首次上线时就完美无缺，唯一可以确定的是，你必须更新它，而且要快。

The long-term life cycle of a software product involves rapid exploration of new ideas, rapid responses to landscape shifts or user issues, and enabling developer velocity at scale. From Eric Raymond’s The Cathedral and the Bazaar to Eric Reis’ The Lean Startup, the key to any organization’s long-term success has always been in its ability to get ideas executed and into users’ hands as quickly as possible and reacting quickly to their feedback. Martin Fowler, in his book Continuous Delivery (aka CD), points out that “The biggest risk to any software effort is that you end up building something that isn’t useful. The earlier and more frequently you get working software in front of real users, the quicker you get feedback to find out how valuable it really is.”

在软件产品漫长的生命周期中，需要迅速探索新想法、响应行业格局变化或用户问题，并在规模扩大时仍能保持开发速度。从埃里克·雷蒙德（Eric Raymond）的《大教堂与集市》（The Cathedral and The Bazaar）到埃里克·赖斯（Eric Reis）的《精益创业》（The Lean Startup），组织长期成功的关键始终在于：尽快把想法付诸实现，交到用户手中，并迅速响应用户反馈。马丁·福勒（Martin Fowler）在其著作《持续交付》（Continuous Delivery，简称 CD）中指出：“软件开发最大的风险，是最终做出的东西没有用。越早、越频繁地把能用的软件交到真实用户手中，就能越快获得反馈，了解它究竟有多大价值。”

Work that stays in progress for a long time before delivering user value is high risk and high cost, and can even be a drain on morale. At Google, we strive to release early and often, or “launch and iterate,” to enable teams to see the impact of their work quickly and to adapt faster to a shifting market. The value of code is not realized at the time of submission but when features are available to your users. Reducing the time between “code complete” and user feedback minimizes the cost of work that is in progress.

工作长期处于进行中，却迟迟不能为用户带来价值，风险和成本都会很高，甚至会打击士气。在谷歌，我们力求尽早发布、频繁发布，也就是“上线并迭代”，让团队迅速看到工作成效，更快地适应市场变化。代码的价值并非在提交时实现，而是在用户能够使用相应功能时才得以实现。缩短“代码完成”到获得用户反馈之间的时间，可以尽量降低未交付工作的成本。

    You get extraordinary outcomes by realizing that the launch *never lands* but that it begins a learning cycle where you then fix the next most important thing, measure how it went, fix the next thing, etc.—and it is *never complete*.
    —David Weekly, Former Google product manager

    要取得非凡成果，就要认识到：上线从来不是终点，而是学习循环的开始。你接着解决下一个最重要的问题，衡量效果，再解决下一个问题，如此反复，这个过程永远不会结束。
    -David Weekly，前谷歌产品经理

At Google, the practices we describe in this book allow hundreds (or in some cases thousands) of engineers to quickly troubleshoot problems, to independently work on new features without worrying about the release, and to understand the effectiveness of new features through A/B experimentation. This chapter focuses on the key levers of rapid innovation, including managing risk, enabling developer velocity at scale, and understanding the cost and value trade-off of each feature you launch.

在谷歌，本书介绍的实践让数百名，有时甚至数千名工程师能够迅速排查问题，独立开发新功能而不必担心发布，并通过 A/B 实验了解新功能的效果。本章重点介绍推动快速创新的关键措施，包括管理风险、在规模扩大时保持开发速度，以及理解每项新功能在成本与价值之间的权衡。

## Idioms of Continuous Delivery at Google 谷歌持续交付的常用实践

A core tenet of Continuous Delivery (CD) as well as of Agile methodology is that over time, smaller batches of changes result in higher quality; in other words, *faster is safer*. This can seem deeply controversial to teams at first glance, especially if the prerequisites for setting up CD—for example, Continuous Integration (CI) and testing— are not yet in place. Because it might take a while for all teams to realize the ideal of CD, we focus on developing various aspects that deliver value independently en route to the end goal. Here are some of these:

- *Agility*  
    Release frequently and in small batches

- *Automation*  
​    Reduce or remove repetitive overhead of frequent releases

- *Isolation*  
​    Strive for modular architecture to isolate changes and make troubleshooting easier

- *Reliability*  
​    Measure key health indicators like crashes or latency and keep improving them

- *Data-driven* *decision* *making*  
​    Use A/B testing on health metrics to ensure quality

- *Phased* *rollout*  
​    Roll out changes to a few users before shipping to everyone

持续交付（CD）和敏捷方法论都有一个核心原则：从长期来看，每批变更越小，质量就越高。换句话说，越快越安全。团队初听这一观点，可能会觉得很有争议，尤其是在持续集成（CI）和测试等 CD 前提条件尚未具备时。让所有团队达到理想的 CD 状态可能需要时间，因此，我们着重推进一些本身就能带来价值的实践，逐步走向最终目标。其中包括：

- *敏捷性*  
​    小批量、频繁地发布。

- *自动化*  
​    减少或消除频繁发布的重复性开销。

- *隔离性*  
​    力求采用模块化架构，隔离变更，简化故障排查。

- *可靠性*  
​    衡量崩溃、延迟等关键健康指标，并持续改善。

- *数据驱动的决策*  
​    通过 A/B 测试比较健康指标，确保质量。

- *分阶段发布*  
​    先向少量用户发布变更，再推向所有用户。

At first, releasing new versions of software frequently might seem risky. As your userbase grows, you might fear the backlash from angry users if there are any bugs that you didn’t catch in testing, and you might quite simply have too much new code in your product to test exhaustively. But this is precisely where CD can help. Ideally, there are so few changes between one release and the next that troubleshooting issues is trivial. In the limit, with CD, every change goes through the QA pipeline and is automatically deployed into production. This is often not a practical reality for many teams, and so there is often work of culture change toward CD as an intermediate step, during which teams can build their readiness to deploy at any time without actually doing so, building up their confidence to release more frequently in the future.

 起初，频繁发布软件新版本似乎很冒险。随着用户群扩大，你可能会担心：一旦有缺陷未在测试中发现，就会招致用户的不满；产品中的新代码也可能多到根本无法穷尽测试。但这恰恰是 CD 能发挥作用的地方。理想情况下，相邻版本之间的变更很少，排查问题也就很简单。将 CD 做到极致，每项变更都会经过 QA 流水线，自动部署到生产环境。不过，许多团队实际上还做不到这一点，因此往往需要先推动面向 CD 的文化转变。在这个过渡阶段，团队可以先具备随时部署的能力，而不必真的随时部署，逐步建立信心，为今后更频繁地发布作准备。

## Velocity Is a Team Sport: How to Break Up a Deployment into Manageable Pieces   提速需要团队协作：如何将部署拆分成易于管理的部分

When a team is small, changes come into a codebase at a certain rate. We’ve seen an antipattern emerge as a team grows over time or splits into subteams: a subteam branches off its code to avoid stepping on anyone’s feet, but then struggles, later, with integration and culprit finding. At Google, we prefer that teams continue to develop at head in the shared codebase and set up CI testing, automatic rollbacks, and culprit finding to identify issues quickly. This is discussed at length in Chapter 23.

团队规模较小时，变更以一定的速率进入代码库。我们观察到，随着团队逐渐壮大或拆分为多个子团队，一种反模式会随之出现：子团队为了避免相互干扰，单独建立代码分支，随后却在集成和定位致错变更时遇到困难。在谷歌，我们更倾向于让团队继续基于共享代码库的最新版本开发，并建立 CI 测试、自动回滚和致错变更定位机制，以便迅速发现问题。第23章对此有详细讨论。

One of our codebases, YouTube, is a large, monolithic Python application. The release process is laborious, with Build Cops, release managers, and other volunteers. Almost every release has multiple cherry-picked changes and respins. There is also a 50-hour manual regression testing cycle run by a remote QA team on every release. When the operational cost of a release is this high, a cycle begins to develop in which you wait to push out your release until you’re able to test it a bit more. Meanwhile, someone wants to add just one more feature that’s almost ready, and pretty soon you have yourself a release process that’s laborious, error prone, and slow. Worst of all, the experts who did the release last time are burned out and have left the team, and now nobody even knows how to troubleshoot those strange crashes that happen when you try to release an update, leaving you panicky at the very thought of pushing that button.

我们的一个代码库 YouTube，是大型单体 Python 应用。它的发布过程十分繁重，需要构建值守人员（Build Cops）、发布经理和其他志愿者参与。几乎每次发布都要选择性合并（cherry-pick）多项变更，并反复重新构建。每个版本还要由远程 QA 团队执行一轮耗时50小时的手工回归测试。发布的操作成本高到这种程度，就容易陷入一个循环：总想再多做些测试，才肯发布。与此同时，又有人想再加一个即将完成的功能。很快，发布流程就变得费力、易错又缓慢。最糟糕的是，上次负责发布的专家已经耗尽精力、离开团队，而如今甚至没人知道该如何排查发布更新时那些奇怪的崩溃，一想到要按下发布按钮就让人恐慌。

If your releases are costly and sometimes risky, the *instinct* is to slow down your release cadence and increase your stability period. However, this only provides short- term stability gains, and over time it slows velocity and frustrates teams and users. The *answer* is to reduce cost, increase discipline, and make the risks more incremental, but it is critical to resist the obvious operational fixes and invest in long-term architectural changes. The obvious operational fixes to this problem lead to a few traditional approaches: reverting to a traditional planning model that leaves little room for learning or iteration, adding more governance and oversight to the development process, and implementing risk reviews or rewarding low-risk (and often low-value) features.

如果发布成本高，有时还伴随风险，*本能*的反应是放慢发布节奏，延长稳定化阶段。然而，这只能暂时提高稳定性，长此以往，会拖慢进度，让团队和用户失望。解决办法是降低成本、严格遵守流程，将风险分散到一次次小幅变更中。关键在于克制仅从操作层面修补的冲动，转而投资于长期的架构改进。那些看似直接的操作层面修补，往往会引向几种传统做法：退回几乎不给学习和迭代留余地的传统规划模式；加强对开发流程的治理和监督；开展风险审查，或奖励低风险、往往也低价值的功能。

The investment with the best return, though, is migrating to a microservice architecture, which can empower a large product team with the ability to remain scrappy and innovative while simultaneously reducing risk. In some cases, at Google, the answer has been to rewrite an application from scratch rather than simply migrating it, establishing the desired modularity into the new architecture. Although either of these options can take months and is likely painful in the short term, the value gained in terms of operational cost and cognitive simplicity will pay off over an application’s lifespan of years.

不过，回报最高的投资是迁移到微服务架构：它既能降低风险，又能让大型产品团队保持灵活和创新能力。在谷歌，有时我们会选择从头重写应用，而不只是迁移，在新架构中实现所需的模块化。无论采用哪一种方式，都可能需要数月，短期内也很可能令人痛苦。但在应用长达多年的生命周期中，降低运营成本、减轻理解负担所带来的收益，足以让这项投入获得回报。

## Evaluating Changes in Isolation: Flag-Guarding Features 单独评估变更：用标志保护功能

A key to reliable continuous releases is to make sure engineers “flag guard” *all changes*. As a product grows, there will be multiple features under various stages of development coexisting in a binary. Flag guarding can be used to control the inclusion or expression of feature code in the product on a feature-by-feature basis and can be expressed differently for release and development builds. A feature flag disabled for a build should allow build tools to strip the feature from the build if the language permits it. For instance, a stable feature that has already shipped to customers might be enabled for both development and release builds. A feature under development might be enabled only for development, protecting users from an unfinished feature. New feature code lives in the binary alongside the old codepath—both can run, but the new code is guarded by a flag. If the new code works, you can remove the old codepath and launch the feature fully in a subsequent release. If there’s a problem, the flag value can be updated independently from the binary release via a dynamic config update.

要可靠地持续发布，关键之一是确保工程师用标志保护所有变更。随着产品发展，同一个二进制文件中会共存多个处于不同开发阶段的功能。通过标志，可以逐项控制功能代码是否包含在产品中，以及是否启用；发布构建和开发构建也可以采用不同的设置。如果某项功能的标志在一次构建中被禁用，那么只要编程语言支持，构建工具就应能从构建产物中剔除该功能。例如，已经交付给客户的稳定功能，可以在开发构建和发布构建中都启用；仍在开发的功能则可以只在开发构建中启用，避免用户受到未完成功能的影响。新功能代码与旧代码路径共存于二进制文件中，两者都能运行，但新代码受标志控制。如果新代码运行正常，就可以在后续版本中移除旧代码路径，全面启用新功能。如果出现问题，则可以通过动态配置更新来修改标志值，无须另行发布二进制包。

In the old world of binary releases, we had to time press releases closely with our binary rollouts. We had to have a successful rollout before a press release about new functionality or a new feature could be issued. This meant that the feature would be out in the wild before it was announced, and the risk of it being discovered ahead of time was very real.

过去按二进制包发布功能时，新闻稿的发布时间必须与二进制包的部署进度紧密配合。只有部署成功后，才能发布介绍新功能的新闻稿。这意味着在正式宣布之前，功能就已经进入实际使用环境，确实存在提前被发现的风险。

This is where the beauty of the flag guard comes to play. If the new code has a flag, the flag can be updated to turn your feature on immediately before the press release, thus minimizing the risk of leaking a feature. Note that flag-guarded code is not a *perfect* safety net for truly sensitive features. Code can still be scraped and analyzed if it’s not well obfuscated, and not all features can be hidden behind flags without adding a lot of complexity. Moreover, even flag configuration changes must be rolled out with care. Turning on a flag for 100% of your users all at once is not a great idea, so a configuration service that manages safe configuration rollouts is a good investment. Nevertheless, the level of control and the ability to decouple the destiny of a particular feature from the overall product release are powerful levers for long-term sustainability of the application.

这正是标志保护的优势。如果新代码受标志控制，就可以在新闻稿发布前一刻更新标志，启用功能，尽量降低功能提前泄露的风险。不过，对于真正敏感的功能，标志保护并不能提供完美的保障。代码如果没有充分混淆，仍可能被提取和分析；也并非所有功能都能在不大幅增加复杂性的前提下，通过标志隐藏。此外，即使只是修改标志配置，也必须谨慎发布。一次性为100%的用户启用某个标志并不明智，因此，值得投入资源建设配置服务，管理配置的安全发布。尽管如此，这种控制能力，以及让单项功能不再受整体产品发布牵制的能力，仍是实现应用长期可持续性的重要手段。

## Striving for Agility: Setting Up a Release Train 追求敏捷：建立发布列车机制

Google’s Search binary is its first and oldest. Large and complicated, its codebase can be tied back to Google’s origin—a search through our codebase can still find code written at least as far back as 2003, often earlier. When smartphones began to take off, feature after mobile feature was shoehorned into a hairball of code written primarily for server deployment. Even though the Search experience was becoming more vibrant and interactive, deploying a viable build became more and more difficult. At one point, we were releasing the Search binary into production only once per week, and even hitting that target was rare and often based on luck.

搜索是谷歌最早的二进制程序。它的代码库庞大而复杂，历史可以追溯到谷歌创立之初。如今在代码库中搜索，仍能找到写于2003年的代码，往往还能找到更早的代码。智能手机开始兴起时，一个接一个的移动端功能被硬塞进一团盘根错节、主要为服务器部署而编写的代码中。搜索体验虽然变得更加丰富、更具交互性，但部署一个可用构建却越来越困难。曾有一段时间，我们每周只向生产环境发布一次搜索二进制包，即使这个目标也很少达成，而且往往要靠运气。

When one of our contributing authors, Sheri Shipe, took on the project of increasing our release velocity in Search, each release cycle was taking a group of engineers days to complete. They built the binary, integrated data, and then began testing. Each bug had to be manually triaged to make sure it wouldn’t impact Search quality, the user experience (UX), and/or revenue. This process was grueling and time consuming and did not scale to the volume or rate of change. As a result, a developer could never know when their feature was going to be released into production. This made timing press releases and public launches challenging.

本章作者之一 Sheri Shipe 接手提高搜索发布速度的项目时，每轮发布都需要一组工程师花上数天才能完成。他们先构建二进制包、集成数据，再开始测试。每个缺陷都必须人工研判，以确认它不会影响搜索质量、用户体验（UX）或收入。这个过程费力又耗时，无法应对不断增加的变更数量和变更速度。因此，开发者根本无法确定自己的功能何时会发布到生产环境，新闻稿和产品公开上线的时间也就难以安排。

Releases don’t happen in a vacuum, and having reliable releases makes the dependent factors easier to synchronize. Over the course of several years, a dedicated group of engineers implemented a continuous release process, which streamlined everything about sending a Search binary into the world. We automated what we could, set deadlines for submitting features, and simplified the integration of plug-ins and data into the binary. We could now consistently release a new Search binary into production every other day.

发布不是孤立的活动。发布过程可靠，与之相关的各项工作就更容易协调。在数年间，一个专门的工程师团队建立了持续发布流程，简化了搜索二进制包从内部走向用户的各个环节。我们尽可能实现自动化，为功能提交设定截止时间，并简化了将插件和数据集成到二进制包中的过程。现在，我们能够稳定地每隔一天向生产环境发布一个新的搜索二进制包。

What were the trade-offs we made to get predictability in our release cycle? They narrow down to two main ideas we baked into the system.

为了让发布周期变得可预测，我们作了哪些权衡？归结起来，就是融入系统的两个主要理念。

### No Binary Is Perfect 没有完美的二进制包

The first is that *no binary is perfect*, especially for builds that are incorporating the work of tens or hundreds of developers independently developing dozens of major features. Even though it’s impossible to fix every bug, we constantly need to weigh questions such as: If a line has been moved two pixels to the left, will it affect an ad display and potential revenue? What if the shade of a box has been altered slightly? Will it make it difficult for visually impaired users to read the text? The rest of this book is arguably about minimizing the set of unintended outcomes for a release, but in the end we must admit that software is fundamentally complex. There is no perfect binary—decisions and trade-offs have to be made every time a new change is released into production. Key performance indicator metrics with clear thresholds allow features to launch even if they aren’t perfect[^1] and can also create clarity in otherwise contentious launch decisions.

首先，*没有一个二进制包是完美的*。尤其是那些汇集了数十乃至数百名开发者成果的构建：这些开发者正分别开发数十项重要功能。虽然不可能修复所有缺陷，我们仍要不断权衡这样的问题：一条线向左移动两个像素，会不会影响广告展示和潜在收入？一个方框的色调略有变化，会不会让视障用户难以阅读其中的文字？本书的其他内容可以说都是在探讨如何尽量减少发布带来的意外后果，但最终，我们必须承认软件本身就是复杂的。没有完美的二进制包，每次将新变更发布到生产环境，都必须作出决策和权衡。为关键绩效指标设定明确的阈值，既能让尚不完美的功能获得发布机会，也能为原本容易引发争议的发布决策提供清晰依据。

One bug involved a rare dialect spoken on only one island in the Philippines. If a user asked a search question in this dialect, instead of an answer to their question, they would get a blank web page. We had to determine whether the cost of fixing this bug was worth delaying the release of a major new feature.

有一个缺陷涉及一种罕见方言，只有菲律宾某个岛屿上的居民使用。用户用这种方言搜索问题时，得不到答案，只会看到空白网页。我们必须判断，是否值得为了修复这个缺陷，付出推迟发布一项重要新功能的代价。

We ran from office to office trying to determine how many people actually spoke this language, if it happened every time a user searched in this language, and whether these folks even used Google on a regular basis. Every quality engineer we spoke with deferred us to a more senior person. Finally, data in hand, we put the question to Search’s senior vice president. Should we delay a critical release to fix a bug that affected only a very small Philippine island? It turns out that no matter how small your island, you should get reliable and accurate search results: we delayed the release and fixed the bug.

我们奔走于各个办公室，想弄清究竟有多少人使用这种语言、每次用这种语言搜索是否都会出现问题，以及这些人平时是否经常使用谷歌。每位与我们交谈的质量工程师都请我们去问更资深的人。最后，我们带着收集到的数据，请搜索业务的高级副总裁定夺：是否应该推迟一次关键发布，去修复一个只影响菲律宾某个小岛的缺陷？最终的结论是，无论居住的岛屿多小，用户都应该得到可靠、准确的搜索结果。于是，我们推迟了发布，修复了这个缺陷。

> [^1]:  Remember the SRE “error-budget” formulation: perfection is rarely the best goal. Understand how much room for error is acceptable and how much of that budget has been spent recently and use that to adjust the trade-off between velocity and stability.
>
> 1 记住 SRE 的“错误预算”理念：完美很少是最佳目标。先明确可以容忍多少错误，以及近期已经消耗了多少预算，再据此调整速度与稳定性之间的权衡。

### Meet Your Release Deadline 遵守发布截止时间

The second idea is that *if you’re late for the release train, it will leave without you*. There’s something to be said for the adage, “deadlines are certain, life is not.” At some point in the release timeline, you must put a stake in the ground and turn away developers and their new features. Generally speaking, no amount of pleading or begging will get a feature into today’s release after the deadline has passed.

第二个理念是，*如果你赶不上发布列车，它也会照常发车*。有句话说得有道理：“截止时间是确定的，生活却充满变数。”发布流程必须设定一个明确的截止点，到了这个时间，就不再接受开发者提交的新功能。一般来说，错过截止时间后，无论开发者怎样恳求，也不能把功能加进当天的版本。

There is the *rare* exception. The situation usually goes like this. It’s late Friday evening and six software engineers come storming into the release manager’s cube in a panic. They have a contract with the NBA and finished the feature moments ago. But it must go live before the big game tomorrow. The release must stop and we must cherry- pick the feature into the binary or we’ll be in breach of contract! A bleary-eyed release engineer shakes their head and says it will take four hours to cut and test a new binary. It’s their kid’s birthday and they still need to pick up the balloons.

也有*极少数例外*，通常是这样的场景：周五深夜，六名软件工程师慌慌张张地冲进发布经理的隔间。他们与 NBA 签了合同，功能刚刚完成，却必须在明天的重要比赛前上线。“必须暂停发布，把这项功能选择性合并进二进制包，否则我们就违约了！”一位睡眼惺忪的发布工程师摇摇头，说重新生成并测试一个二进制包需要四个小时。今天是这位工程师孩子的生日，还得去取气球。

A world of regular releases means that if a developer misses the release train, they’ll be able to catch the next train in a matter of hours rather than days. This limits developer panic and greatly improves work–life balance for release engineers.

有了定期发布机制，开发者即使错过一班发布列车，只需再等几个小时，而不是几天，就能赶上下一班。这能减轻开发者的焦虑，也能大大改善发布工程师的工作与生活平衡。

## Quality and User-Focus: Ship Only What Gets Used 关注质量与用户：只交付会被使用的功能

Bloat is an unfortunate side effect of most software development life cycles, and the more successful a product becomes, the more bloated its code base typically becomes. One downside of a speedy, efficient release train is that this bloat is often magnified and can manifest in challenges to the product team and even to the users. Especially if the software is delivered to the client, as in the case of mobile apps, this can mean the user’s device pays the cost in terms of space, download, and data costs, even for features they never use, whereas developers pay the cost of slower builds, complex deployments, and rare bugs. In this section, we’ll talk about how dynamic deployments allow you to ship only what is used, forcing necessary trade-offs between user value and feature cost. At Google, this often means staffing dedicated teams to improve the efficiency of the product on an ongoing basis.

代码膨胀是大多数软件在开发生命周期中一个令人遗憾的副作用。产品越成功，代码库通常也越臃肿。快速、高效的发布列车机制有一个缺点：它往往会加剧这种膨胀，给产品团队甚至用户带来困难。尤其是移动应用这类交付到客户端的软件，即使用户从不使用某些功能，这些功能仍可能占用设备存储空间，增加下载负担和流量费用；开发者则要承担构建变慢、部署复杂和罕见缺陷带来的成本。本节讨论如何通过动态部署，只交付实际会被使用的内容，从而促使团队在用户价值与功能成本之间作出必要的权衡。在谷歌，这往往意味着组建专门团队，持续提高产品的运行效率。

Whereas some products are web-based and run on the cloud, many are client applications that use shared resources on a user’s device—a phone or tablet. This choice in itself showcases a trade-off between native apps that can be more performant and resilient to spotty connectivity, but also more difficult to update and more susceptible to platform-level issues. A common argument against frequent, continuous deployment for native apps is that users dislike frequent updates and must pay for the data cost and the disruption. There might be other limiting factors such as access to a network or a limit to the reboots required to percolate an update.

有些产品基于 Web，在云端运行；许多产品则是客户端应用，需要共享用户手机或平板电脑上的资源。选择哪种形式，本身就涉及权衡：原生应用可能性能更好，也更能应对时断时续的网络连接，但更新更困难，也更容易受到平台层面问题的影响。反对原生应用频繁、持续部署的一个常见理由是，用户不喜欢频繁更新，还要承担流量费用和使用中断的代价。此外，也可能存在其他限制，例如能否连接网络，以及为使更新生效而重启设备的次数限制。

Even though there is a trade-off to be made in terms of how frequently to update a product, the goal is to *have these choices be intentional*. With a smooth, well-running CD process, how often a viable release is *created* can be separated from how often a user *receives* it. You might achieve the goal of being able to deploy weekly, daily, or hourly, without actually doing so, and you should intentionally choose release processes in the context of your users’ specific needs and the larger organizational goals, and determine the staffing and tooling model that will best support the long-term sustainability of your product.

产品更新频率固然需要权衡，但目标是*有意识地作出这些选择*。有了顺畅、运行良好的 CD 流程，生成可发布版本的频率就能与用户实际收到版本的频率分开。你可以具备每周、每天甚至每小时部署一次的能力，而不必真的按这个频率部署。应当结合用户的具体需求和组织的整体目标，有意识地选择发布流程，并确定最有利于产品长期可持续性的人员配置与工具方案。

Earlier in the chapter, we talked about keeping your code modular. This allows for dynamic, configurable deployments that allow better utilization of constrained resources, such as the space on a user’s device. In the absence of this practice, every user must receive code they will never use to support translations they don’t need or architectures that were meant for other kinds of devices. Dynamic deployments allow apps to maintain small sizes while only shipping code to a device that brings its users value, and A/B experiments allow for intentional trade-offs between a feature’s cost and its value to users and your business.

本章前面讨论过代码模块化。它能支持动态、可配置的部署，更有效地利用用户设备存储空间等有限资源。没有这种做法，每个用户都得接收一些永远不会用到的代码，例如支持自己不需要的语言译文，或支持其他类型设备架构的代码。动态部署只向设备交付能为其用户带来价值的代码，让应用保持较小的体积；A/B 实验则帮助团队有意识地权衡功能成本，以及功能对用户和业务的价值。

There is an upfront cost to setting up these processes, and identifying and removing frictions that keep the frequency of releases lower than is desirable is a painstaking process. But the long-term wins in terms of risk management, developer velocity, and enabling rapid innovation are so high that these initial costs become worthwhile.

建立这些流程需要前期投入，找出并消除妨碍发布频率达到理想水平的阻力，也是一项艰苦的工作。但从长期来看，风险管理、开发速度和快速创新能力方面的收益，足以让这些初期投入物有所值。

## Shifting Left: Making Data-Driven Decisions Earlier 左移：提前做出数据驱动的决策

If you’re building for all users, you might have clients on smart screens, speakers, or Android and iOS phones and tablets, and your software may be flexible enough to allow users to customize their experience. Even if you’re building for only Android devices, the sheer diversity of the more than two billion Android devices can make the prospect of qualifying a release overwhelming. And with the pace of innovation, by the time someone reads this chapter, whole new categories of devices might have bloomed.

如果软件面向所有用户，你可能需要提供运行在智能屏幕、音箱，以及 Android 和 iOS 手机、平板电脑上的客户端，软件也可能足够灵活，允许用户定制自己的使用体验。即使只面向 Android 设备，超过20亿台设备的多样性，也足以让版本的发布验证工作令人望而生畏。创新还在持续，等读者看到本章时，或许已经涌现出全新的设备类别。

One of our release managers shared a piece of wisdom that turned the situation around when he said that the diversity of our client market was not a *problem*, but a *fact*. After we accepted that, we could switch our release qualification model in the following ways:

- If *comprehensive* testing is practically infeasible, aim for *representative* testing instead.
- Staged rollouts to slowly increasing percentages of the userbase allow for fast fixes.
- Automated A/B releases allow for statistically significant results proving a release’s quality, without tired humans needing to look at dashboards and make decisions.

一位发布经理的一句话改变了我们的思路：客户端市场的多样性不是一个问题，而是一个事实。接受这一点之后，我们就能从以下几个方面调整发布验证方式：

- 如果实际上无法进行*全面*测试，就以*代表性*测试为目标。
- 分阶段发布，逐步增加覆盖的用户比例，便于迅速修复问题。
- 自动化 A/B 发布可以用具有统计显著性的结果证明版本质量，无须让疲惫的人员盯着仪表盘作决策。

When it comes to developing for Android clients, Google apps use specialized testing tracks and staged rollouts to an increasing percentage of user traffic, carefully monitoring for issues in these channels. Because the Play Store offers unlimited testing tracks, we can also set up a QA team in each country in which we plan to launch, allowing for a global overnight turnaround in testing key features.

在开发 Android 客户端时，谷歌应用会使用专门的测试通道，分阶段发布到越来越大比例的用户流量，并密切监控这些通道中出现的问题。由于 Play Store 提供不限数量的测试通道，我们还可以在每个计划上线的国家设立 QA 团队，一夜之间完成全球范围内的关键功能测试。

One issue we noticed when doing deployments to Android was that we could expect a statistically significant change in user metrics *simply from pushing an update*. This meant that even if we made no changes to our product, pushing an update could affect device and user behavior in ways that were difficult to predict. As a result, although canarying the update to a small percentage of user traffic could give us good information about crashes or stability problems, it told us very little about whether the newer version of our app was in fact better than the older one.

向 Android 设备部署时，我们注意到一个问题：单是推送一次更新，就能预期用户指标会发生具有统计显著性的变化。这意味着，即使产品本身毫无改动，推送更新也可能以难以预测的方式影响设备和用户行为。因此，虽然向一小部分用户流量进行金丝雀发布，能提供有关崩溃或稳定性问题的有用信息，却几乎无法说明新版应用是否真的比旧版更好。

Dan Siroker and Pete Koomen have already discussed the value of A/B testing[^2] your features, but at Google, some of our larger apps also A/B test their *deployments*. This means sending out two versions of the product: one that is the desired update, with the baseline being a placebo (your old version just gets shipped again). As the two versions roll out simultaneously to a large enough base of similar users, you can compare one release against the other to see whether the latest version of your software is in fact an improvement over the previous one. With a large enough userbase, you should be able to get statistically significant results within days, or even hours. An automated metrics pipeline can enable the fastest possible release by pushing forward a release to more traffic as soon as there is enough data to know that the guardrail metrics will not be affected.

Dan Siroker 和 Pete Koomen 已经讨论过对功能进行 A/B 测试的价值，而在谷歌，一些较大型的应用还会对*部署*本身进行 A/B 测试。具体做法是发布两个版本：一个是计划推出的更新，另一个则是作为基线的“安慰剂”，也就是把旧版重新发布一次。把这两个版本同时推向足够多、特征相似的用户，就可以比较它们，判断最新版软件是否确实比旧版有所改进。用户群足够大时，应该在几天甚至几小时内就能得到具有统计显著性的结果。自动化指标流水线一旦收集到足够的数据，确认护栏指标不会受到影响，就能立即将该版本推广到更多流量，尽可能加快发布。

Obviously, this method does not apply to every app and can be a lot of overhead when you don’t have a large enough userbase. In these cases, the recommended best practice is to aim for change-neutral releases. All new features are flag guarded so that the only change being tested during a rollout is the stability of the deployment itself.

显然，这种方法并非适用于所有应用，用户群不够大时，还可能带来很高的开销。在这种情况下，推荐的做法是尽量让发布不改变功能行为。所有新功能都用标志保护，这样在逐步发布时，需要检验的就只有部署本身的稳定性。

> [^2]:  Dan Siroker and Pete Koomen, *A/B Testing: The Most Powerful Way to Turn Clicks Into Customers* (Hoboken: Wiley, 2013).
>
> 2   Dan Siroker 和 Pete Koomen，《A/B 测试：将点击转化为客户的最有力方法》（Hoboken: Wiley，2013）。

## Changing Team Culture: Building Discipline into Deployment 改变团队文化：严格遵守部署流程

Although “Always Be Deploying” helps address several issues affecting developer velocity, there are also certain practices that address issues of scale. The initial team launching a product can be fewer than 10 people, each taking turns at deployment and production-monitoring responsibilities. Over time, your team might grow to hundreds of people, with subteams responsible for specific features. As this happens and the organization scales up, the number of changes in each deployment and the amount of risk in each release attempt is increasing superlinearly. Each release contains months of sweat and tears. Making the release successful becomes a high-touch and labor-intensive effort. Developers can often be caught trying to decide which is worse: abandoning a release that contains a quarter’s worth of new features and bug fixes, or pushing out a release without confidence in its quality.

“始终保持部署”有助于解决一些影响开发速度的问题，此外还有一些实践专门应对规模问题。产品最初上线时，团队可能不到10人，大家轮流负责部署和生产环境监控。随着时间推移，团队可能发展到数百人，由不同子团队负责特定功能。组织规模扩大后，每次部署的变更数量、每次尝试发布所承担的风险，都呈超线性增长。每次发布都凝聚着数月的心血，要成功发布，就得投入大量协调工作和人力。开发者常常陷入两难：是放弃一个包含整整一季度新功能和缺陷修复的版本，还是在对质量没有把握的情况下将它发布出去？

At scale, increased complexity usually manifests as increased release latency. Even if you release every day, a release can take a week or longer to fully roll out safely, leaving you a week behind when trying to debug any issues. This is where “Always Be Deploying” can return a development project to effective form. Frequent release trains allow for minimal divergence from a known good position, with the recency of changes aiding in resolving issues. But how can a team ensure that the complexity inherent with a large and quickly expanding codebase doesn’t weigh down progress?

规模扩大时，复杂性增加通常会表现为发布耗时变长。即使每天都有版本发布，一个版本也可能需要一周甚至更久，才能安全地完成全面发布；等到排查问题时，你已经落后了一周。此时，“始终保持部署”可以让开发项目重新高效运转。频繁的发布列车让每次发布与已知良好状态之间的差异尽可能小，而变更刚发生不久，也有助于排查问题。不过，面对庞大且快速增长的代码库，团队怎样才能避免其固有的复杂性拖慢进度？

On Google Maps, we take the perspective that features are very important, but only very seldom is any feature so important that a release should be held for it. If releases are frequent, the pain a feature feels for missing a release is small in comparison to the pain all the new features in a release feel for a delay, and especially the pain users can feel if a not-quite-ready feature is rushed to be included.

谷歌地图团队的观点是：功能很重要，但极少有功能重要到值得为它推迟整个版本的发布。发布足够频繁时，一项功能错过当前版本所付出的代价，远小于整个版本延期给所有新功能带来的代价，更不用说匆忙加入尚未准备好的功能，可能给用户造成的损害。

One release responsibility is to protect the product from the developers.

发布工作的一项职责，就是保护产品，避免它因开发者的行为而受损。

When making trade-offs, the passion and urgency a developer feels about launching a new feature can never trump the user experience with an existing product. This means that new features must be isolated from other components via interfaces with strong contracts, separation of concerns, rigorous testing, communication early and often, and conventions for new feature acceptance.

作权衡时，开发者上线新功能的热情和紧迫感，绝不能凌驾于现有产品的用户体验之上。因此，必须通过契约严格的接口、关注点分离、严格测试、尽早且频繁的沟通，以及新功能验收规范，将新功能与其他组件隔离。

## Conclusion 总结

Over the years and across all of our software products, we’ve found that, counterintuitively, faster is safer. The health of your product and the speed of development are not actually in opposition to each other, and products that release more frequently and in small batches have better quality outcomes. They adapt faster to bugs encountered in the wild and to unexpected market shifts. Not only that, faster is *cheaper*, because having a predictable, frequent release train forces you to drive down the cost of each release and makes the cost of any abandoned release very low.

多年来，我们在所有软件产品中都发现了一个看似违反直觉的事实：越快越安全。产品健康状况与开发速度并不矛盾，小批量、频繁发布的产品质量更好，也能更快地应对实际使用中暴露的缺陷和意料之外的市场变化。不仅如此，更快也*更省钱*：可预测、频繁发车的发布列车会促使你降低每次发布的成本，即使放弃某次发布，代价也很小。

Simply having the structures in place that *enable* continuous deployment generates the majority of the value, *even if you don’t actually push those releases out to users*. What do we mean? We don’t actually release a wildly different version of Search, Maps, or YouTube every day, but to be able to do so requires a robust, well- documented continuous deployment process, accurate and real-time metrics on user satisfaction and product health, and a coordinated team with clear policies on what makes it in or out and why. In practice, getting this right often also requires binaries that can be configured in production, configuration managed like code (in version control), and a toolchain that allows safety measures like dry-run verification, rollback/rollforward mechanisms, and reliable patching.

只要建立起*能够*支持持续部署的机制，就能获得其中大部分价值，*即使你并未真的把这些版本推送给用户*。这是什么意思？我们并不是每天都发布一个变化巨大的搜索、地图或 YouTube 版本。但要具备这样的能力，就必须有稳健且文档完备的持续部署流程、反映用户满意度和产品健康状况的准确实时指标，以及协作有序的团队。团队还要有明确规则，决定哪些变更可以纳入发布、哪些不能，以及原因何在。在实践中，往往还需要能在生产环境中调整配置的二进制包、像代码一样纳入版本控制的配置，以及支持试运行验证、回滚与前滚机制、可靠补丁更新等安全措施的工具链。

## TL;DRs  内容提要

- *Velocity is a team sport*: The optimal workflow for a large team that develops code collaboratively requires modularity of architecture and near-continuous integration.
- Evaluate changes in isolation: Flag guard any features to be able to isolate prob‐ lems early.
- Make reality your benchmark: Use a staged rollout to address device diversity and the breadth of the userbase. Release qualification in a synthetic environment that isn’t similar to the production environment can lead to late surprises.
- Ship only what gets used: Monitor the cost and value of any feature in the wild to know whether it’s still relevant and delivering sufficient user value.
- Shift left: Enable faster, more data-driven decision making earlier on all changes through CI and continuous deployment.
- Faster is safer: Ship early and often and in small batches to reduce the risk of each release and to minimize time to market.

- *提速需要团队协作*：对协作开发代码的大型团队而言，最佳工作流需要模块化架构和近乎持续的集成。
- 单独评估变更：用标志保护各项功能，以便尽早隔离问题。
- 以实际情况为基准：通过分阶段发布，应对设备的多样性和广泛的用户群。如果在与生产环境相差较大的模拟环境中验证版本是否可以发布，就可能到后期才发现意外问题。
- 只交付会被使用的功能：监控每项功能在实际使用中的成本与价值，判断它是否仍有用，是否仍能为用户提供足够的价值。
- 左移：借助 CI 和持续部署，对所有变更更早、更快地作出更有数据依据的决策。
- 越快越安全：尽早、小批量、频繁地发布，降低每次发布的风险，尽量缩短产品推向市场的时间。
