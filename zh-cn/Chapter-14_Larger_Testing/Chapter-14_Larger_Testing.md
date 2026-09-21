
**CHAPTER 14**

# Larger Testing

# 第十四章 较大规模测试

**Written by  Written by Joseph Graves**

**Edited by Lisa Carey**

In previous chapters, we have recounted how a testing culture was established at Google and how small unit tests became a fundamental part of the developer workflow. But what about other kinds of tests? It turns out that Google does indeed use many larger tests, and these comprise a significant part of the risk mitigation strategy necessary for healthy software engineering. But these tests present additional challenges to ensure that they are valuable assets and not resource sinks. In this chapter, we’ll discuss what we mean by “larger tests,” when we execute them, and best practices for keeping them effective.

前几章介绍了谷歌如何建立测试文化，以及小型单元测试如何成为开发者工作流的基本组成部分。那么，其他类型的测试呢？谷歌确实也使用了许多较大规模测试，它们是风险缓解策略的重要组成部分，而这类策略是软件工程健康发展的必要条件。不过，要让这些测试成为有价值的资产，而不是不断消耗资源的负担，还需要应对额外的挑战。本章将讨论什么是“较大规模测试”、何时执行这类测试，以及保持其有效性的最佳实践。

## What Are Larger Tests? 什么是较大规模测试？

As mentioned previously, Google has specific notions of test size. Small tests are restricted to one thread, one process, one machine. Larger tests do not have the same restrictions. But Google also has notions of test scope. A unit test necessarily is of smaller scope than an integration test. And the largest-scoped tests (sometimes called end-to-end or system tests) typically involve several real dependencies and fewer test doubles.

如前所述，谷歌对测试规模有明确的定义。小型测试只能使用一个线程、一个进程和一台机器，较大规模测试则没有这些限制。不过，谷歌也区分测试范围。单元测试的范围必然小于集成测试；范围最广的测试有时称为端到端测试或系统测试，通常涉及多个真实依赖，使用的测试替身较少。（译者注：Martin Fowler 的文章[Test Double](https://martinfowler.com/bliki/TestDouble.html)介绍了 Gerard Meszaros 提出的`Test Double`概念。文章虽发表于2006年，其中的概念仍有参考价值。`Test Double`是一个统称，指为实现测试目的，用“替身”代替真实依赖对象，降低被测对象对真实组件的依赖，有助于提高测试速度和稳定性。本译文统一译为“测试替身”。）

Larger tests are many things that small tests are not. They are not bound by the same constraints; thus, they can exhibit the following characteristics:

- They may be slow. Our large tests have a default timeout of 15 minutes or 1 hour, but we also have tests that run for multiple hours or even days.
- They may be nonhermetic. Large tests may share resources with other tests and traffic.
- They may be nondeterministic. If a large test is nonhermetic, it is almost impossible to guarantee determinism: other tests or user state may interfere with it.

较大规模测试有许多小型测试不具备的特点。它们不受相同的约束，因此可能有以下特征：

- 运行可能很慢。我们的大型测试默认超时时间为15分钟或1小时，但也有一些测试要运行数小时，甚至数天。
- 可能不具备封闭性。大型测试可能与其他测试和流量共享资源。
- 结果可能不具有确定性。如果大型测试不具备封闭性，就几乎无法保证结果的确定性，因为其他测试或用户状态可能干扰它。

So why have larger tests? Reflect back on your coding process. How do you confirm that the programs you write actually work? You might be writing and running unit tests as you go, but do you find yourself running the actual binary and trying it out yourself? And when you share this code with others, how do they test it? By running your unit tests, or by trying it out themselves?

那么，为什么需要较大规模测试？回想一下编码过程：你如何确认自己写的程序确实能工作？你可能一边开发，一边编写和运行单元测试，但是否也会运行实际的二进制程序，亲自试用？把代码分享给别人后，他们又会如何测试？是运行你的单元测试，还是自己试用？

Also, how do you know that your code continues to work during upgrades? Suppose that you have a site that uses the Google Maps API and there’s a new API version. Your unit tests likely won’t help you to know whether there are any compatibility issues. You’d probably run it and try it out to see whether anything broke.

另外，你如何知道代码在升级后仍能正常工作？假设你的网站使用了谷歌地图 API，而这个 API 发布了新版本。单元测试很可能无法告诉你是否存在兼容性问题。你大概会运行网站，试用一下，看看有没有功能出错。

Unit tests can give you confidence about individual functions, objects, and modules, but large tests provide more confidence that the overall system works as intended. And having actual automated tests scales in ways that manual testing does not.

单元测试让你对单个函数、对象和模块有信心，大型测试则让你更有把握确认整个系统按预期工作。而且，真正实现自动化的测试具有手动测试无法比拟的可扩展性。

### Fidelity 仿真度

The primary reason larger tests exist is to address *fidelity*. Fidelity is the property by which a test is reflective of the real behavior of the system under test (SUT).

较大规模测试主要是为了解决仿真度问题。仿真度指测试能够在多大程度上反映被测系统（SUT）的真实行为。

One way of envisioning fidelity is in terms of the environment. As Figure 14-1 illustrates, unit tests bundle a test and a small portion of code together as a runnable unit, which ensures the code is tested but is very different from how production code runs. Production itself is, naturally, the environment of highest fidelity in testing. There is also a spectrum of interim options. A key for larger tests is to find the proper fit, because increasing fidelity also comes with increasing costs and (in the case of production) increasing risk of failure.

可以从环境的角度理解仿真度。如图14-1所示，单元测试把测试代码和一小部分被测代码打包成一个可运行单元。这能确保代码得到测试，却与生产代码的运行方式大不相同。生产环境本身自然是仿真度最高的测试环境，两者之间还有一系列选择。较大规模测试的关键之一，是找到合适的位置：仿真度越高，成本也越高；如果在生产环境中测试，故障风险也会随之增加。

![Figure 14-1](./images/Figure%2014-1.png)

*Figure 14-1. Scale of increasing fidelity* *图14-1 环境仿真度递增的尺度*

Tests can also be measured in terms of how faithful the test content is to reality. Many handcrafted, large tests are dismissed by engineers if the test data itself looks unrealistic. Test data copied from production is much more faithful to reality (having been captured that way), but a big challenge is how to create realistic test traffic *before* launching the new code. This is particularly a problem in artificial intelligence (AI), for which the “seed” data often suffers from intrinsic bias. And, because most data for unit tests is handcrafted, it covers a narrow range of cases and tends to conform to the biases of the author. The uncovered scenarios missed by the data represent a fidelity gap in the tests.

也可以根据测试内容与真实情况的接近程度来衡量测试。如果测试数据本身显得不真实，工程师就可能不认可许多手工编写的大型测试。从生产环境复制的数据更接近真实情况，因为它本来就采集自生产环境；但如何在*新代码上线之前*创建逼真的测试流量，是一大挑战。在人工智能（AI）领域，这个问题尤为突出，因为“种子”数据往往带有固有偏差。此外，大多数单元测试数据由人手工构造，覆盖的场景范围较窄，也容易反映编写者的偏见。数据未覆盖的场景，就是测试在仿真度上的缺口。

### Common Gaps in Unit Tests 单元测试常见的覆盖缺口

Larger tests might also be necessary where smaller tests fail. The subsections that follow present some particular areas where unit tests do not provide good risk mitigation coverage.

在较小规模测试无法胜任的地方，也可能需要较大规模测试。下面介绍一些具体领域，单元测试在这些领域的覆盖不足以有效缓解风险。

#### Unfaithful doubles 仿真度不足的测试替身

A single unit test typically covers one class or module. Test doubles (as discussed in Chapter 13) are frequently used to eliminate heavyweight or hard-to-test dependencies. But when those dependencies are replaced, it becomes possible that the replacement and the doubled thing do not agree.

一个单元测试通常覆盖一个类或模块。第13章讨论过，测试替身常用于替换开销大或难以测试的依赖。然而，替换之后，测试替身的行为可能与真实依赖不一致。

Almost all unit tests at Google are written by the same engineer who is writing the unit under test. When those unit tests need doubles and when the doubles used are mocks, it is the engineer writing the unit test defining the mock and its intended behavior. But that engineer usually did *not* write the thing being mocked and can be misinformed about its actual behavior. The relationship between the unit under test and a given peer is a behavioral contract, and if the engineer is mistaken about the actual behavior, the understanding of the contract is invalid.

在谷歌，几乎所有单元测试都由编写被测单元的工程师编写。如果测试需要替身，而且使用的是模拟对象（mock），那么模拟对象及其预期行为也由这位工程师定义。但这位工程师通常*并未*编写被模拟的组件，可能误解其实际行为。被测单元与协作组件之间存在行为契约；如果工程师误解了实际行为，对这份契约的理解也就有误。

Moreover, mocks become stale. If this mock-based unit test is not visible to the author of the real implementation and the real implementation changes, there is no signal that the test (and the code being tested) should be updated to keep up with the changes.

此外，模拟对象还会过时。如果真实实现的作者不知道这个使用模拟对象的单元测试，那么真实实现发生变化时，就不会有任何信号提醒人们：测试及被测代码也需要随之更新。

Note that, as mentioned in [Chapter 13], if teams provide fakes for their own services, this concern is mostly alleviated.

需要注意的是，正如第13章所述，如果团队为自己的服务提供伪实现（fake），就能在很大程度上缓解这一问题。

#### Configuration issues 配置问题

Unit tests cover code within a given binary. But that binary is typically not completely self-sufficient in terms of how it is executed. Usually a binary has some kind of deployment configuration or starter script. Additionally, real end-user-serving production instances have their own configuration files or configuration databases.

单元测试覆盖某个二进制程序中的代码，但这个程序通常无法完全独立运行，还需要部署配置或启动脚本。此外，真正为最终用户提供服务的生产实例，也有自己的配置文件或配置数据库。

If there are issues with these files or the compatibility between the state defined by these stores and the binary in question, these can lead to major user issues. Unit tests alone cannot verify this compatibility.[^1] Incidentally, this is a good reason to ensure that your configuration is in version control as well as your code, because then, changes to configuration can be identified as the source of bugs as opposed to introducing random external flakiness and can be built in to large tests.

如果这些文件有问题，或者其中存储的状态与目标二进制程序不兼容，就可能给用户造成严重问题。仅靠单元测试无法验证这种兼容性。这也说明，配置应当与代码一样纳入版本控制：这样既能确认缺陷是否源于配置变更，避免它表现为来自外部的随机不稳定性，也能将配置纳入大型测试。

At Google, configuration changes are the number one reason for our major outages. This is an area in which we have underperformed and has led to some of our most embarrassing bugs. For example, there was a global Google outage back in 2013 due to a bad network configuration push that was never tested. Configurations tend to be written in configuration languages, not production code languages. They also often have faster production rollout cycles than binaries, and they can be more difficult to test. All of these lead to a higher likelihood of failure. But at least in this case (and others), configuration was version controlled, and we could quickly identify the culprit and mitigate the issue.

在谷歌，配置变更是重大故障的首要原因。我们在这方面做得不够好，曾因此出现一些令人尴尬的缺陷。例如，2013年，一次未经测试的错误网络配置发布，导致谷歌发生全球性服务中断。配置通常用配置语言而非生产代码所用的语言编写，发布到生产环境的周期也往往比二进制程序更短，而且可能更难测试。这些因素都增加了故障的可能性。不过，至少在这次以及其他一些事件中，配置已经纳入版本控制，所以我们能迅速找到肇因，缓解问题。

> [^1]:	See “Continuous Delivery” on page 483 and Chapter 25 for more information.
>
> 1   更多信息参见第483页的“持续交付”及第25章。

#### Issues that arise under load 负载下出现的问题

At Google, unit tests are intended to be small and fast because they need to fit into our standard test execution infrastructure and also be run many times as part of a frictionless developer workflow. But performance, load, and stress testing often require sending large volumes of traffic to a given binary. These volumes become difficult to test in the model of a typical unit test. And our large volumes are big, often thousands or millions of queries per second (in the case of ads, [real-time bidding](https://oreil.ly/brV5-))!

在谷歌，单元测试要求规模小、运行快，既要适配标准测试执行基础设施，也要能在开发者工作流中反复运行，而不妨碍开发。但性能、负载和压力测试往往需要向某个二进制程序发送大量流量，典型的单元测试模型很难测试这种流量规模。我们的流量确实很大，往往达到每秒数千乃至数百万次查询，例如广告业务中的实时竞价！

#### Unanticipated behaviors, inputs, and side effects 未预料到的行为、输入和副作用

Unit tests are limited by the imagination of the engineer writing them. That is, they can only test for anticipated behaviors and inputs. However, issues that users find with a product are mostly unanticipated (otherwise it would be unlikely that they would make it to end users as issues). This fact suggests that different test techniques are needed to test for unanticipated behaviors.

单元测试受限于编写者的想象力，只能测试工程师预先想到的行为和输入。然而，用户在产品中发现的问题大多未被预料到，否则这些问题就不太可能一直留到最终用户使用时才暴露。这说明，测试未预料到的行为，需要采用不同的测试技术。

[Hyrum’s Law](http://hyrumslaw.com/)is an important consideration here: even if we could test 100% for conformance to a strict, specified contract, the effective user contract applies to all visible behaviors, not just a stated contract. It is unlikely that unit tests alone test for all visible behaviors that are not specified in the public API.

这里需要特别考虑海勒姆定律：即使能完整测试系统是否遵守严格、明确规定的契约，实际对用户生效的契约仍然涵盖所有可观察行为，而不只是明文规定的部分。仅靠单元测试，不太可能测到公共 API 中未规定的所有可观察行为。

#### Emergent behaviors and the “vacuum effect” 涌现行为与“真空效应”

Unit tests are limited to the scope that they cover (especially with the widespread use of test doubles), so if behavior changes in areas outside of this scope, it cannot be detected. And because unit tests are designed to be fast and reliable, they deliberately eliminate the chaos of real dependencies, network, and data. A unit test is like a problem in theoretical physics: ensconced in a vacuum, neatly hidden from the mess of the real world, which is great for speed and reliability but misses certain defect categories.

单元测试只能检查其覆盖范围内的行为，广泛使用测试替身时尤其如此，因此无法检测范围之外的行为变化。为了快速、可靠地运行，单元测试会刻意排除真实依赖、网络和数据带来的混乱。它就像理论物理中的一道题，被放在真空里，与现实世界的纷繁复杂隔绝。这有利于提高速度和可靠性，却也会漏掉某些类别的缺陷。

### Why Not Have Larger Tests? 为什么不采用较大规模测试？

In earlier chapters, we discussed many of the properties of a developer-friendly test. In particular, it needs to be as follows:

- *Reliable*  
	It must not be flaky and it must provide a useful pass/fail signal.
- *Fast*  
	It needs to be fast enough to not interrupt the developer workflow.
- *Scalable*  
	Google needs to be able to run all such useful affected tests efficiently for presubmits and for post-submits.

前几章讨论了对开发者友好的测试应具备的许多特性，尤其是以下几点：
- *可靠*  
	不能时而通过、时而失败，必须提供有用的通过或失败信号。
- *快速*  
	运行必须足够快，不打断开发者的工作流。
- *可扩展*  
	谷歌需要在提交前和提交后，高效运行所有受变更影响且有价值的测试。

Good unit tests exhibit all of these properties. Larger tests often violate all of these constraints. For example, larger tests are often flakier because they use more infrastructure than does a small unit test. They are also often much slower, both to set up as well as to run. And they have trouble scaling because of the resource and time requirements, but often also because they are not isolated—these tests can collide with one another.

良好的单元测试具备所有这些特性，较大规模测试却往往一项也不满足。例如，较大规模测试使用的基础设施比小型单元测试更多，因此结果往往更不稳定。它们的准备和运行通常也慢得多。资源和时间需求会限制它们的扩展能力，缺乏隔离也常常是原因之一，因为测试之间可能相互冲突。

Additionally, larger tests present two other challenges. First, there is a challenge of ownership. A unit test is clearly owned by the engineer (and team) who owns the unit. A larger test spans multiple units and thus can span multiple owners. This presents a long-term ownership challenge: who is responsible for maintaining the test and who is responsible for diagnosing issues when the test breaks? Without clear ownership, a test rots.

此外，较大规模测试还面临两个挑战。第一个是责任归属。单元测试自然由负责被测单元的工程师及其团队负责。较大规模测试跨越多个单元，也就可能涉及多个负责人。这带来了长期的责任归属问题：谁维护测试？测试失败时，谁诊断问题？没有明确的负责人，测试就会逐渐失去维护。

The second challenge for larger tests is one of standardization (or the lack thereof). Unlike unit tests, larger tests suffer a lack of standardization in terms of the infrastructure and process by which they are written, run, and debugged. The approach to larger tests is a product of a system’s architectural decisions, thus introducing variance in the type of tests required. For example, the way we build and run A-B diff regression tests in Google Ads is completely different from the way such tests are built and run in Search backends, which is different again from Drive. They use different platforms, different languages, different infrastructures, different libraries, and competing testing frameworks.

第二个挑战是缺乏标准化。与单元测试不同，较大规模测试在编写、运行和调试所需的基础设施与流程上，缺少统一标准。这类测试的做法取决于系统的架构决策，因此所需测试类型也各不相同。例如，谷歌广告构建和运行 A-B 差异回归测试的方式，与搜索后端完全不同，后者又与 Google Drive 不同。它们使用不同的平台、语言、基础设施、库，以及相互竞争的测试框架。

This lack of standardization has a significant impact. Because larger tests have so many ways of being run, they often are skipped during large-scale changes. (See Chapter 22.) The infrastructure does not have a standard way to run those tests, and asking the people executing LSCs to know the local particulars for testing on every team doesn’t scale. Because larger tests differ in implementation from team to team, tests that actually test the integration between those teams require unifying incompatible infrastructures. And because of this lack of standardization, we cannot teach a single approach to Nooglers (new Googlers) or even more experienced engineers, which both perpetuates the situation and also leads to a lack of understanding about the motivations of such tests.

缺乏标准化会产生显著影响。较大规模测试的运行方式五花八门，因此在大规模变更中经常被跳过，参见第22章。基础设施没有统一的方式来运行这些测试；要求执行大规模变更（LSC）的人员掌握每个团队特有的测试细节，也无法随规模扩展。各团队的实现不同，要真正测试团队之间的系统集成，就必须整合彼此不兼容的基础设施。此外，我们无法向 Noogler（谷歌新员工），甚至更有经验的工程师传授统一做法。这既让现状延续，也使人们难以理解为何需要这些测试。

## Larger Tests at Google 谷歌的较大规模测试

When we discussed the history of testing at Google earlier (see Chapter 11), we mentioned how Google Web Server (GWS) mandated automated tests in 2003 and how this was a watershed moment. However, we actually had automated tests in use before this point, but a common practice was using automated large and enormous tests. For example, AdWords created an end-to-end test back in 2001 to validate product scenarios. Similarly, in 2002, Search wrote a similar “regression test” for its indexing code, and AdSense (which had not even publicly launched yet) created its variation on the AdWords test.

前面讨论谷歌测试历史时，第11章提到 Google Web Server（GWS）在2003年强制要求自动化测试，并将其视为一个分水岭。不过，在此之前我们其实已经在使用自动化测试，只是当时通常采用大型甚至超大型测试。例如，AdWords 早在2001年就建立了端到端测试，用于验证产品场景。2002年，搜索团队也为索引代码编写了类似的“回归测试”；尚未公开推出的 AdSense 则在 AdWords 测试的基础上开发了自己的版本。

Other “larger” testing patterns also existed circa 2002. The Google search frontend relied heavily on manual QA—manual versions of end-to-end test scenarios. And Gmail got its version of a “local demo” environment—a script to bring up an end-to- end Gmail environment locally with some generated test users and mail data for local manual testing.

2002年前后，其他“较大规模”测试模式也已存在。谷歌搜索前端高度依赖人工质量保证，也就是手动执行端到端测试场景。Gmail 也有自己的“本地演示”环境：通过脚本在本地启动一个端到端的 Gmail 环境，生成一些测试用户和邮件数据，用于本地手动测试。

When C/J Build (our first continuous build framework) launched, it did not distinguish between unit tests and other tests, but there were two critical developments that led to a split. First, Google focused on unit tests because we wanted to encourage the testing pyramid and to ensure the vast majority of written tests were unit tests. Second, when TAP replaced C/J Build as our formal continuous build system, it was only able to do so for tests that met TAP’s eligibility requirements: hermetic tests buildable at a single change that could run on our build/test cluster within a maximum time limit. Although most unit tests satisfied this requirement, larger tests mostly did not. However, this did not stop the need for other kinds of tests, and they have continued to fill the coverage gaps. C/J Build even stuck around for years specifically to handle these kinds of tests until newer systems replaced it.

C/J Build 是我们的第一个持续构建框架，推出时并不区分单元测试和其他测试。后来，两个关键变化促成了这种区分。首先，谷歌把重点放在单元测试上，希望推广测试金字塔，确保绝大多数测试都是单元测试。其次，TAP 取代 C/J Build 成为正式持续构建系统时，只能接管符合其准入要求的测试：测试必须是封闭的，能基于某一次变更对应的代码状态构建，并能在构建与测试集群上于规定时限内运行完毕。大多数单元测试满足要求，较大规模测试则大多不满足。不过，对其他测试类型的需求并未因此消失，它们仍在填补覆盖缺口。C/J Build 甚至为专门处理这些测试而继续使用了多年，直到被更新的系统取代。

### Larger Tests and Time 较大规模测试与时间

Throughout this book, we have looked at the influence of time on software engineering, because Google has built software running for more than 20 years. How are larger tests influenced by the time dimension? We know that certain activities make more sense the longer the expected lifespan of code, and testing of various forms is an activity that makes sense at all levels, but the test types that are appropriate change over the expected lifetime of code.

本书始终关注时间对软件工程的影响，因为谷歌已经构建了持续运行20多年的软件。那么，时间维度如何影响较大规模测试？我们知道，代码的预期生命周期越长，某些活动就越值得做。测试在各种生命周期长度下都有价值，但适用的测试类型会随预期生命周期而变化。

As we pointed out before, unit tests begin to make sense for software with an expected lifespan from hours on up. At the minutes level (for small scripts), manual testing is most common, and the SUT usually runs locally, but the local demo likely *is* production, especially for one-off scripts, demos, or experiments. At longer lifespans, manual testing continues to exist, but the SUTs usually diverge because the production instance is often cloud hosted instead of locally hosted.

如前所述，当软件的预期生命周期达到数小时或更长时，单元测试就开始有价值。对于生命周期只有几分钟的小脚本，最常见的是手动测试，SUT 通常在本地运行；不过，这个本地演示环境很可能*就是*生产环境，尤其是一次性脚本、演示或实验。生命周期更长的软件仍然需要手动测试，但测试环境中的 SUT 与生产实例通常会分离，因为生产实例往往托管在云端，而不是本地。

The remaining larger tests all provide value for longer-lived software, but the main concern becomes the maintainability of such tests as time increases.

其余较大规模测试都能为长生命周期软件提供价值，但随着时间推移，这些测试的可维护性会成为主要问题。

Incidentally, this time impact might be one reason for the development of the “ice cream cone” testing antipattern, as mentioned in the Chapter 11 and shown again in Figure 14-2.

顺便说一句，时间的这种影响，可能正是“冰淇淋筒”测试反模式形成的原因之一。第11章已介绍过这一模式，图14-2再次给出示意。

![Figure 14-2](./images/Figure%2014-2.png)

*Figure 14-2. The ice cream cone testing antipattern*

When development starts with manual testing (when engineers think that code is meant to last only for minutes), those manual tests accumulate and dominate the initial overall testing portfolio. For example, it’s pretty typical to hack on a script or an app and test it out by running it, and then to continue to add features to it but continue to test it out by running it manually. This prototype eventually becomes functional and is shared with others, but no automated tests actually exist for it.

如果开发之初采用手动测试，因为工程师认为代码只会使用几分钟，那么手动测试就会不断积累，在最初的测试组合中占据主导。一个常见过程是：先动手写一个脚本或应用，运行一下来测试；随后不断添加功能，却仍然靠手动运行来测试。这个原型最终具备了实用功能，也分享给了别人，却始终没有自动化测试。

Even worse, if the code is difficult to unit test (because of the way it was implemented in the first place), the only automated tests that can be written are end-to-end ones, and we have inadvertently created “legacy code” within days.

更糟的是，如果最初的实现方式使代码难以进行单元测试，就只能编写端到端自动化测试。短短几天，我们便在无意中制造了“遗留代码”。

It is *critical* for longer-term health to move toward the test pyramid within the first few days of development by building out unit tests, and then to top it off after that point by introducing automated integration tests and moving away from manual end- to-end tests. We succeeded by making unit tests a requirement for submission, but covering the gap between unit tests and manual tests is necessary for long-term health.

要让软件长期健康发展，*至关重要*的是在开发的头几天就补齐单元测试，建立测试金字塔的基础；随后引入自动化集成测试，补上金字塔的上层，逐步摆脱手动端到端测试。我们通过要求提交代码时必须有单元测试，成功建立了这个基础；但要长期保持健康，还必须填补单元测试与手动测试之间的空白。

#### Larger Tests at Google Scale 谷歌规模下的较大规模测试

It would seem that larger tests should be more necessary and more appropriate at larger scales of software, but even though this is so, the complexity of authoring, running, maintaining, and debugging these tests increases with the growth in scale, even more so than with unit tests.

软件规模越大，较大规模测试似乎就越必要、越适用。事实确实如此，但编写、运行、维护和调试这些测试的复杂性，也会随规模增长而增加，而且增幅比单元测试更大。

In a system composed of microservices or separate servers, the pattern of interconnections looks like a graph: let the number of nodes in that graph be our *N*. Every time a new node is added to this graph, there is a multiplicative effect on the number of distinct execution paths through it.

由微服务或独立服务器组成的系统，其连接关系可以表示为一张图。设图中的节点数为 N，每增加一个节点，穿过这张图的不同执行路径数量就会受到乘法效应的影响。

[Figure 14-3 ](#_bookmark1226)depicts an imagined SUT: this system consists of a social network with users, a social graph, a stream of posts, and some ads mixed in. The ads are created by advertisers and served in the context of the social stream. This SUT alone consists of two groups of users, two UIs, three databases, an indexing pipeline, and six servers. There are 14 edges enumerated in the graph. Testing all of the end-to-end possibilities is already difficult. Imagine if we add more services, pipelines, and databases to this mix: photos and images, machine learning photo analysis, and so on?

图14-3展示了一个假想的 SUT：这是一个社交网络，包含用户、社交关系图、帖子信息流，以及混在信息流中的广告。广告由广告主创建，展示在社交信息流中。仅这个 SUT 就包含两组用户、两个 UI、三个数据库、一条索引流水线和六个服务器。图中列出了14条边，要测试所有可能的端到端路径已经很困难。试想，如果再加入更多服务、流水线和数据库，例如照片与图像、基于机器学习的照片分析，又会怎样？

![Figure 14-3](./images/Figure%2014-3.png)

*Figure 14-3. Example of a fairly small SUT: a social network with advertising*

The rate of distinct scenarios to test in an end-to-end way can grow exponentially or combinatorially depending on the structure of the system under test, and that growth does not scale. Therefore, as the system grows, we must find alternative larger testing strategies to keep things manageable.

需要端到端测试的不同场景数量，可能随被测系统的结构呈指数级或组合式增长，这样的增长无法持续应对。因此，随着系统扩大，必须寻找其他较大规模测试策略，让测试仍然可管理。

However, the value of such tests also increases because of the decisions that were necessary to achieve this scale. This is an impact of fidelity: as we move toward larger-*N* layers of software, if the service doubles are lower fidelity (1-epsilon), the chance of bugs when putting it all together is exponential in *N*. Looking at this example SUT again, if we replace the user server and ad server with doubles and those doubles are low fidelity (e.g., 10% accurate), the likelihood of a bug is 99% (1 – (0.1 ∗ 0.1)). And that’s just with two low-fidelity doubles.

然而，为达到这种规模而作出的架构决策，也会提高这类测试的价值。这与仿真度有关：当软件涉及更多节点，即 N 增大时，如果服务替身的仿真度较低，为 1−ε，把各部分组装起来后，出现缺陷的概率与 N 存在指数关系。再看前面的 SUT：如果用低仿真度的测试替身替换用户服务器和广告服务器，例如各自只有10%的准确度，那么出现缺陷的概率就是99%（1 −（0.1 ∗ 0.1））。而这还只是两个低仿真度替身。

Therefore, it becomes critical to implement larger tests in ways that work well at this scale but maintain reasonably high fidelity.

因此，较大规模测试必须既能适应该规模，又能保持足够高的仿真度，这一点至关重要。

------

Tip:"The Smallest Possible Test" 提示：“尽可能小的测试”
Even for integration tests,smaller is better-a handful of large tests is preferable to anenormous one.And,because the scope of a test is often coupled to the scope of theSUT,finding ways to make the SUT smaller help make the test smaller.

即使是集成测试，也是越小越好：几个大型测试优于一个超大型测试。而且，测试范围往往与 SUT 的范围相联系，因此设法缩小 SUT，也有助于缩小测试。

One way to achieve this test ratio when presented with a user journey that can requirecontributions from many internal systems is to "chain"tests,as illustrated inFigure 14-4,not specifically in their execution,but to create multiple smaller pairwiseintegration tests that represent the overall scenario.This is done by ensuring that theoutput of one test is used as the input to another test by persisting this output to adata repository.

对于需要多个内部系统共同完成的用户旅程，可以通过“串联”测试来实现这种划分，如图14-4所示。这里不是指把测试按顺序执行，而是创建多个较小的两两集成测试，共同代表整个场景。具体做法是将一个测试的输出持久化到数据存储中，供另一个测试作为输入使用。

![Figure 14-4](./images/Figure%2014-4.png)

Figure 14-4. Chained tests

## Structure of a Large Test 大型测试的结构

Although large tests are not bound by small test constraints and could conceivably consist of anything, most large tests exhibit common patterns. Large tests usually consist of a workflow with the following phases:

- Obtain a system under test
- Seed necessary test data
- Perform actions using the system under test
- Verify behaviors

大型测试不受小型测试的约束，理论上可以采用任意形式。不过，大多数大型测试仍有共同模式，通常包含以下几个阶段：

- 准备被测系统 
- 预置必要的测试数据
- 使用被测系统执行操作
- 验证行为

### The System Under Test 被测系统

One key component of large tests is the aforementioned SUT (see Figure 14-5). A typical unit test focuses its attention on one class or module. Moreover, the test code runs in the same process (or Java Virtual Machine [JVM], in the Java case) as the code being tested. For larger tests, the SUT is often very different; one or more separate processes with test code often (but not always) in its own process.

大型测试的关键组成部分之一，就是前面提到的 SUT，见图14-5。典型的单元测试关注一个类或模块，测试代码与被测代码在同一进程中运行；对于 Java，就是在同一个 Java 虚拟机（JVM）中运行。较大规模测试的 SUT 通常很不一样：它由一个或多个独立进程组成，而测试代码通常也在自己的进程中运行，但并非总是如此。

![Figure 14-5](./images/Figure%2014-5.png)

*Figure 14-5. An example system under test (SUT)*

At Google, we use many different forms of SUTs, and the scope of the SUT is one of the primary drivers of the scope of the large test itself (the larger the SUT, the larger the test). Each SUT form can be judged based on two primary factors:

- *Hermeticity*  
	This is the SUT’s isolation from usages and interactions from other components than the test in question. An SUT with high hermeticity will have the least exposure to sources of concurrency and infrastructure flakiness.
- *Fidelity*  
	The SUT’s accuracy in reflecting the production system being tested. An SUT with high fidelity will consist of binaries that resemble the production versions (rely on similar configurations, use similar infrastructures, and have a similar overall topology).

谷歌使用多种形式的 SUT。SUT 的范围是决定大型测试本身范围的主要因素之一：SUT 范围越广，测试范围也越广。每种形式都可以从两个主要维度来评价：
- *封闭性*  
	指 SUT 与当前测试之外的其他组件的使用和交互隔离的程度。封闭性越高，受到并发活动及基础设施不稳定因素影响的机会就越少。
- *仿真度*  
	指 SUT 反映被测生产系统的准确程度。高仿真度的 SUT 由接近生产版本的二进制程序组成，采用相似的配置、基础设施和整体拓扑。

Often these two factors are in direct conflict. Following are some examples of SUTs:

- *Single-process SUT*  
	The entire system under test is packaged into a single binary (even if in production these are multiple separate binaries). Additionally, the test code can be packaged into the same binary as the SUT. Such a test-SUT combination can be a “small” test if everything is single-threaded, but it is the least faithful to the production topology and configuration.
- *Single-machine SUT*  
	The system under test consists of one or more separate binaries (same as production) and the test is its own binary. But everything runs on one machine. This is used for “medium” tests. Ideally, we use the production launch configuration of each binary when running those binaries locally for increased fidelity.
- *Multimachine SUT*  
	The system under test is distributed across multiple machines (much like a production cloud deployment). This is even higher fidelity than the single-machine SUT, but its use makes tests “large” size and the combination is susceptible to increased network and machine flakiness.
- *Shared environments (staging and production)*  
	Instead of running a standalone SUT, the test just uses a shared environment. This has the lowest cost because these shared environments usually already exist, but the test might conflict with other simultaneous uses and one must wait for the code to be pushed to those environments. Production also increases the risk of end-user impact.
- *Hybrids*  
	Some SUTs represent a mix: it might be possible to run some of the SUT but have it interact with a shared environment. Usually the thing being tested is explicitly run but its backends are shared. For a company as expansive as Google, it is practically impossible to run multiple copies of all of Google’s interconnected services, so some hybridization is required.

这两个维度往往直接冲突。下面列举几种 SUT：

- *单进程 SUT*  
	整个被测系统打包成一个二进制文件，即使它在生产环境中由多个独立的二进制文件组成。测试代码也可以与 SUT 打包在一起。如果全部代码都在单线程中运行，这种测试与 SUT 的组合就可能属于“小型”测试，但它与生产环境的拓扑和配置最不相似。
- *单机 SUT*  
	被测系统与生产环境一样，由一个或多个独立的二进制程序组成，测试也是独立的二进制程序，但全部运行在一台机器上。这种形式用于“中型”测试。理想情况下，本地运行各程序时应使用其生产环境启动配置，以提高仿真度。
- *多机 SUT*  
	被测系统分布在多台机器上，类似于生产环境中的云部署。它的仿真度比单机 SUT 更高，但相应测试在规模分类上属于“大型”，而且更容易受网络和机器不稳定性的影响。
- *共享环境（预发和生产）*  
	测试直接使用共享环境，不单独运行 SUT。这种方式成本最低，因为共享环境通常已经存在，但测试可能与其他同时使用环境的活动冲突，而且必须等代码部署到这些环境后才能执行。在生产环境中测试，还会增加影响最终用户的风险。
- *混合模式*  
	有些 SUT 采用混合形式：单独运行系统的一部分，让它与共享环境交互。通常会专门启动被测组件，而后端仍然共享。对于谷歌这样规模庞大的公司，几乎不可能为所有相互连接的服务运行多套副本，因此需要采用一定程度的混合形式。

#### The benefits of hermetic SUTs 封闭式 SUT 的好处

The SUT in a large test can be a major source of both unreliability and long turnaround time. For example, an in-production test uses the actual production system deployment. As mentioned earlier, this is popular because there is no extra overhead cost for the environment, but production tests cannot be run until the code reaches that environment, which means those tests cannot themselves block the release of the code to that environment—the SUT is too late, essentially.

大型测试中的 SUT，可能是测试不可靠、反馈周期过长的主要来源。例如，在生产环境中测试会直接使用实际部署的生产系统。如前所述，这种做法很常见，因为无需额外承担环境成本。但只有代码进入生产环境后，测试才能运行，因此这些测试本身无法阻止代码发布到该环境。从这个意义上说，获得 SUT 的时机已经太晚了。

The most common first alternative is to create a giant shared staging environment and to run tests there. This is usually done as part of some release promotion process, but it again limits test execution to only when the code is available. As an alternative, some teams will allow engineers to “reserve” time in the staging environment and to use that time window to deploy pending code and to run tests, but this does not scale with a growing number of engineers or a growing number of services, because the environment, its number of users, and the likelihood of user conflicts all quickly grow.

最常见的初步替代方案，是建立一个庞大的共享预发环境，在其中运行测试。测试通常是逐步推进版本发布的流程的一部分，但仍然只能在代码部署到该环境后执行。另一种做法是允许工程师“预约”预发环境的时段，在这段时间内部署待发布代码并运行测试。不过，这种方式无法适应工程师或服务数量的增长，因为环境规模、使用人数以及使用冲突的可能性都会迅速增加。

The next step is to support cloud-isolated or machine-hermetic SUTs. Such an environment improves the situation by avoiding the conflicts and reservation requirements for code release.

下一步是支持云端隔离或机器级封闭的 SUT。这类环境不再需要为代码发布预约使用时段，也避免了相关冲突，从而改善了上述情况。

------

*Case Study:Risks of testing in production and Webdriver Torso*  
*案例研究：生产环境测试的风险与 Webdriver Torso*

We mentioned that testing in production can be risky.One humorous episode resulting from testing in production was known as the Webdriver Torso incident.Weneeded a way to verify that video rendering in You Tube production was workingproperly and so created automated scripts to generate test videos,upload them,andverify the quality of the upload.This was done in a Google-owned YouTube channelcalled Webdriver Torso.But this channel was public,as were most of the videos.

前面提到，在生产环境中测试有一定风险，Webdriver Torso 事件就是由此引发的一段趣事。为了验证 YouTube 生产环境中的视频渲染是否正常，我们编写了自动化脚本，生成并上传测试视频，再验证上传后的视频质量。这些操作在谷歌拥有的 YouTube 频道 Webdriver Torso 中进行。但这个频道是公开的，其中大多数视频也一样。

Subsequently,this channel was publicized in an article at Wired,which led to itsspread throughout the media and subsequent efforts to solve the mystery.Finally,ablogger tied everything back to Google.Eventually,we came clean by having a bit offun with it,including a Rickroll and an Easter Egg,so everything worked out well.Butwe do need to think about the possibility of end-user discovery of any test data weinclude in production and be prepared for it.

后来，《连线》的一篇文章报道了这个频道，其他媒体随之传播，人们开始尝试解开谜团。最终，一位博主发现这一切都与谷歌有关。我们最后用一种轻松的方式承认了此事，还加入了 Rickroll 恶作剧和一个彩蛋，结果也算圆满。不过，这件事提醒我们：放在生产环境中的任何测试数据，都可能被最终用户发现，我们必须考虑这种可能性并做好准备。

----------

#### Reducing the size of your SUT at problem boundaries 在难处理的边界处缩小 SUT

There are particularly painful testing boundaries that might be worth avoiding. Tests that involve both frontends and backends become painful because user interface (UI) tests are notoriously unreliable and costly:
- UIs often change in look-and-feel ways that make UI tests brittle but do not actually impact the underlying behavior.
- UIs often have asynchronous behaviors that are difficult to test.

有些边界会给测试带来很大困难，值得考虑避免跨越。同时涉及前端和后端的测试就很棘手，因为用户界面（UI）测试出了名地不可靠、成本高：
- UI 的外观和交互体验经常变化，虽然不影响底层行为，却会使 UI 测试变得脆弱。
- UI 往往有难以测试的异步行为。

Although it is useful to have end-to-end tests of a UI of a service all the way to its backend, these tests have a multiplicative maintenance cost for both the UI and the backends. Instead, if the backend provides a public API, it is often easier to split the tests into connected tests at the UI/API boundary and to use the public API to drive the end-to-end tests. This is true whether the UI is a browser, command-line interface (CLI), desktop app, or mobile app.

从服务的 UI 一直测到后端的端到端测试确实有用，但同时涉及两端会使维护成本成倍增加。如果后端提供公共 API，通常更容易在 UI 与 API 的边界处，把测试拆成相互衔接的几个测试，并通过公共 API 驱动端到端测试。无论 UI 是浏览器、命令行界面（CLI）、桌面应用还是移动应用，这一点都成立。

Another special boundary is for third-party dependencies. Third-party systems might not have a public shared environment for testing, and in some cases, there is a cost with sending traffic to a third party. Therefore, it is not recommended to have automated tests use a real third-party API, and that dependency is an important seam at which to split tests.

第三方依赖也是一种特殊边界。第三方系统可能不提供公共的共享测试环境，有时向它发送流量还会产生费用。因此，不建议自动化测试调用真实的第三方 API；这类依赖是拆分测试的重要位置。

To address this issue of size, we have made this SUT smaller by replacing its databases with in-memory databases and removing one of the servers outside the scope of the SUT that we actually care about, as shown in Figure 14-6. This SUT is more likely to fit on a single machine.

为解决规模问题，我们用内存数据库替换原有数据库，并移除一个不在实际关注范围内的服务器，从而缩小 SUT，如图14-6所示。这样的 SUT 更有可能在单台机器上运行。

![Figure 14-6](./images/Figure%2014-6.png)

*Figure 14-6. A reduced-size SUT*

The key is to identify trade-offs between fidelity and cost/reliability, and to identify reasonable boundaries. If we can run a handful of binaries and a test and pack it all into the same machines that do our regular compiles, links, and unit test executions, we have the easiest and most stable “integration” tests for our engineers.

关键是权衡仿真度与成本、可靠性，找到合理的边界。如果能把少量二进制程序和一个测试放到日常执行编译、链接和单元测试的机器上一起运行，就能为工程师提供最简单、最稳定的“集成”测试。

#### Record/replay proxies 录制/重放代理

In the previous chapter, we discussed test doubles and approaches that can be used to decouple the class under test from its difficult-to-test dependencies. We can also double entire servers and processes by using a mock, stub, or fake server or process with the equivalent API. However, there is no guarantee that the test double used actually conforms to the contract of the real thing that it is replacing.

上一章讨论了测试替身，以及如何将被测类与难以测试的依赖解耦。也可以用提供等效 API 的服务器或进程，按模拟对象、桩或伪实现的方式替换整个真实服务器或进程。但无法保证这些测试替身确实遵守了真实依赖的契约。

One way of dealing with an SUT’s dependent but subsidiary services is to use a test double, but how does one know that the double reflects the dependency’s actual behavior? A growing approach outside of Google is to use a framework for [consumer-driven contract](https://oreil.ly/RADVJ)tests. These are tests that define a contract for both the client and the provider of the service, and this contract can drive automated tests. That is, a client defines a mock of the service saying that, for these input arguments, I get a particular output. Then, the real service uses this input/output pair in a real test to ensure that it produces that output given those inputs. Two public tools for consumer-driven contract testing are [Pact Contract Testing](https://docs.pact.io/)and [Spring Cloud Contracts](https://oreil.ly/szQ4j). Google’s heavy dependency on protocol buffers means that we don’t use these internally.

对于 SUT 所依赖的辅助服务，一种处理方法是使用测试替身。但怎样确认替身反映了依赖的实际行为？在谷歌之外，使用消费者驱动契约测试框架的做法正逐渐普及。这类测试为服务的客户端和提供方定义共同契约，再用契约驱动自动化测试。具体来说，客户端定义服务的模拟对象，约定给定输入参数应得到什么输出；随后，真实服务用这组输入和输出进行测试，确认自己确实满足约定。两个公开可用的工具是[Pact Contract Testing](https://docs.pact.io/)和[Spring Cloud Contracts](https://oreil.ly/szQ4j)。谷歌高度依赖 protocol buffers，因此内部并未采用这些工具。

At Google, we do something a little bit different. [Our most popular approach](https://oreil.ly/-wvYi)(for which there is a public API) is to use a larger test to generate a smaller one by recording the traffic to those external services when running the larger test and replaying it when running smaller tests. The larger, or “Record Mode” test runs continuously on post-submit, but its primary purpose is to generate these traffic logs (it must pass, however, for the logs to be generated). The smaller, or “Replay Mode” test is used during development and presubmit testing.

谷歌的做法略有不同。我们最常用的方法提供了公共 API，它通过较大规模测试生成较小规模测试：运行前者时录制发往外部服务的流量，运行后者时再重放。较大的“录制模式”测试在提交后持续运行，主要目的是生成流量日志，但只有测试通过，才会生成日志。较小的“重放模式”测试则用于开发过程和提交前测试。

One of the interesting aspects of how record/replay works is that, because of nondeterminism, requests must be matched via a matcher to determine which response to replay. This makes them very similar to stubs and mocks in that argument matching is used to determine the resulting behavior.

录制/重放有一个有趣的特点：由于存在非确定性，必须通过匹配器匹配请求，才能确定重放哪个响应。这与桩和模拟对象很相似，都是通过参数匹配来决定相应行为。

What happens for new tests or tests where the client behavior changes significantly? In these cases, a request might no longer match what is in the recorded traffic file, so the test cannot pass in Replay mode. In that circumstance, the engineer must run the test in Record mode to generate new traffic, so it is important to make running Record tests easy, fast, and stable.

如果新增测试，或客户端行为发生显著变化，会怎样？此时，请求可能无法再与已录制流量文件中的内容匹配，因此测试无法在重放模式下通过。工程师必须改用录制模式运行测试，生成新的流量记录。因此，让录制模式测试易于运行、速度快且稳定，非常重要。

### Test Data 测试数据

A test needs data, and a large test needs two different kinds of data:

- *Seeded data*  
	Data preinitialized into the system under test reflecting the state of the SUT at the inception of the test
- *Test traffic*  
	Data sent to the system under test by the test itself during its execution

测试需要数据，而大型测试需要两类不同的数据：

- *预置数据*  
	预先写入被测系统的数据，反映测试开始时 SUT 的状态。
- *测试流量*  
	测试执行过程中，由测试本身发往被测系统的数据。

Because of the notion of the separate and larger SUT, the work to seed the SUT state is often orders of magnitude more complex than the setup work done in a unit test. For example:

- *Domain data*  
	Some databases contain data prepopulated into tables and used as configuration for the environment. Actual service binaries using such a database may fail on startup if domain data is not provided.
- *Realistic baseline*  
	For an SUT to be perceived as realistic, it might require a realistic set of base data at startup, both in terms of quality and quantity. For example, large tests of a social network likely need a realistic social graph as the base state for tests: enough test users with realistic profiles as well as enough interconnections between those users must exist for the testing to be accepted.
- *Seeding APIs*  
	The APIs by which data is seeded may be complex. It might be possible to directly write to a datastore, but doing so might bypass triggers and checks performed by the actual binaries that perform the writes.

由于 SUT 独立运行且规模更大，为它预置初始状态的工作，往往比单元测试的准备工作复杂几个数量级。例如：
- *领域数据*  
	某些数据库的表中预先填有数据，用作环境配置。如果缺少这些领域数据，使用数据库的实际服务程序可能启动失败。
- *贴近实际的基线*  
	要让人认可 SUT 足够贴近实际，启动时可能就需要一组在质量和数量上都符合实际情况的基础数据。例如，社交网络的大型测试可能需要逼真的社交关系图作为初始状态：既要有足够多的测试用户及其逼真的个人资料，用户之间也要有足够多的连接，这样的测试才具有说服力。
- *数据预置 API*  
	用于预置数据的 API 可能很复杂。也许可以直接写入数据存储，但这样可能绕过真实程序执行写入时会运行的触发器和检查。

Data can be generated in different ways, such as the following:

- *Handcrafted data*  
	Like for smaller tests, we can create test data for larger tests by hand. But it might require more work to set up data for multiple services in a large SUT, and we might need to create a lot of data for larger tests.
- *Copied data*  
	We can copy data, typically from production. For example, we might test a map of Earth by starting with a copy of our production map data to provide a baseline and then test our changes to it.
- *Sampled data*  
	Copying data can provide too much data to reasonably work with. Sampling data can reduce the volume, thus reducing test time and making it easier to reason about. “Smart sampling” consists of techniques to copy the minimum data necessary to achieve maximum coverage.

数据可以通过多种方式生成，例如：

- *手工构造的数据*  
	与较小规模测试一样，大型测试的数据也可以手工构造。但为大型 SUT 中的多个服务准备数据，可能需要更多工作，而且较大规模测试所需的数据量可能很大。
- *复制的数据*  
	可以复制数据，通常从生产环境复制。例如，测试地球地图时，可以先复制一份生产地图数据作为基线，再测试对它的变更。
- *抽样数据*  
	直接复制的数据可能多到难以处理。抽样可以减少数据量，缩短测试时间，也让数据更易于理解和分析。“智能抽样”则是用尽可能少的数据获得尽可能大覆盖范围的一类技术。

### Verification 验证

After an SUT is running and traffic is sent to it, we must still verify the behavior. There are a few different ways to do this:

- *Manual*  
	Much like when you try out your binary locally, manual verification uses humans to interact with an SUT to determine whether it functions correctly. This verification can consist of testing for regressions by performing actions as defined on a consistent test plan or it can be exploratory, working a way through different interaction paths to identify possible new failures.
	Note that manual regression testing does not scale sublinearly: the larger a system grows and the more journeys through it there are, the more human time is needed to manually test.
- *Assertions*  
	Much like with unit tests, these are explicit checks about the intended behavior of the system. For example, for an integration test of Google search of xyzzy, an assertion might be as follows:

```java 
assertThat(response.Contains("Colossal Cave"))
```

- *A/B comparison (differential)*  
	Instead of defining explicit assertions, A/B testing involves running two copies of the SUT, sending the same data, and comparing the output. The intended behavior is not explicitly defined: a human must manually go through the differences to ensure any changes are intended.

启动 SUT 并向它发送流量后，还必须验证其行为。常见方法有以下几种：

- *手动*  
	就像在本地试用二进制程序一样，手动验证由人来操作 SUT，判断其功能是否正确。可以按照固定测试计划中的操作检查回归缺陷，也可以探索不同的交互路径，寻找可能出现的新故障。
	需要注意，手动回归测试的成本无法实现次线性增长：系统越大、用户旅程越多，手动测试所需的人力时间就越多。
- *断言*  
	与单元测试一样，断言明确检查系统的预期行为。例如，针对在谷歌搜索中查询 xyzzy 的集成测试，可以使用如下断言：

```
assertThat(response.Contains("Colossal Cave"))
```

- *A/B 比较（差异比较）*  
	A/B 测试不显式定义断言，而是运行两套 SUT，发送相同数据，再比较输出。预期行为没有明确定义，因此必须由人逐一检查差异，确认所有变化都符合预期。

## Types of Larger Tests 较大规模测试的类型

We can now combine these different approaches to the SUT, data, and assertions to create different kinds of large tests. Each test then has different properties as to which risks it mitigates; how much toil is required to write, maintain, and debug it; and how much it costs in terms of resources to run.

现在可以把 SUT、数据和断言的不同选择组合起来，形成各种大型测试。每种测试各有特点：能缓解哪些风险，编写、维护和调试需要多少琐务，以及运行时要消耗多少资源。

What follows is a list of different kinds of large tests that we use at Google, how they are composed, what purpose they serve, and what their limitations are:

- Functional testing of one or more binaries
- Browser and device testing
- Performance, load, and stress testing
- Deployment configuration testing
- Exploratory testing
- A/B diff (regression) testing
- User acceptance testing (UAT)
- Probers and canary analysis
- Disaster recovery and chaos engineering
- User evaluation

下面列出谷歌使用的各种大型测试，并介绍其组成、用途和局限：

- 一个或多个二进制文件的功能测试
- 浏览器和设备测试
- 性能、负载和压力测试
- 部署配置测试
- 探索性测试
- A/B 差异（回归）测试
- 用户验收测试（UAT）
- 探针和金丝雀分析
- 灾难恢复和混沌工程
- 用户评估

Given such a wide number of combinations and thus a wide range of tests, how do we manage what to do and when? Part of designing software is drafting the test plan, and a key part of the test plan is a strategic outline of what types of testing are needed and how much of each. This test strategy identifies the primary risk vectors and the necessary testing approaches to mitigate those risk vectors.

组合和测试类型如此之多，该如何决定做哪些测试、何时做？制定测试计划是软件设计的一部分，而计划中的关键，是从策略层面明确需要哪些测试类型，以及每类需要多少。测试策略应识别主要风险及其来源，并确定缓解这些风险所需的测试方法。

At Google, we have a specialized engineering role of “Test Engineer,” and one of the things we look for in a good test engineer is the ability to outline a test strategy for our products.

谷歌设有专门的“测试工程师”岗位。我们判断一位测试工程师是否优秀的标准之一，就是能否为产品制定测试策略。

### Functional Testing of One or More Interacting Binaries 一个或多个相互协作的二进制程序的功能测试

Tests of these type have the following characteristics:

- SUT: single-machine hermetic or cloud-deployed isolated
- Data: handcrafted
- Verification: assertions

这类测试具有以下特点：

- SUT：单机封闭或云端部署的隔离环境
- 数据：手工构造
- 验证：断言

As we have seen so far, unit tests are not capable of testing a complex system with true fidelity, simply because they are packaged in a different way than the real code is packaged. Many functional testing scenarios interact with a given binary differently than with classes inside that binary, and these functional tests require separate SUTs and thus are canonical, larger tests.

前面已经看到，单元测试的打包方式与真实代码不同，因此无法以足够真实的方式测试复杂系统。许多功能测试场景需要与整个二进制程序交互，而不是与其中的类交互。这样的功能测试需要独立的 SUT，因此是典型的较大规模测试。

Testing the interactions of multiple binaries is, unsurprisingly, even more complicated than testing a single binary. A common use case is within microservices environments when services are deployed as many separate binaries. In this case, a functional test can cover the real interactions between the binaries by bringing up an SUT composed of all the relevant binaries and by interacting with it through a published API.

不难理解，测试多个二进制程序之间的交互，比测试单个程序更加复杂。微服务环境就是常见例子，服务会部署为许多独立的二进制程序。此时，功能测试可以启动一个由所有相关程序组成的 SUT，再通过对外公布的 API 与它交互，从而覆盖程序之间的真实交互。

### Browser and Device Testing 浏览器和设备测试

Testing web UIs and mobile applications is a special case of functional testing of one or more interacting binaries. It is possible to unit test the underlying code, but for the end users, the public API is the application itself. Having tests that interact with the application as a third party through its frontend provides an extra layer of coverage.

测试 Web UI 和移动应用，是对一个或多个相互协作的二进制程序进行功能测试的特殊情况。底层代码可以用单元测试验证，但对最终用户而言，公共 API 就是应用本身。让测试像第三方一样通过前端操作应用，可以增加一层测试覆盖。

### Performance, Load, and Stress testing 性能、负载和压力测试
Tests of these type have the following characteristics:

- SUT: cloud-deployed isolated
- Data: handcrafted or multiplexed from production
- Verification: diff (performance metrics)

这类测试具有以下特点：

- SUT：云端部署的隔离环境
- 数据：手工构造的数据，或复制分发的生产流量
- 验证：差异比较（性能指标）

Although it is possible to test a small unit in terms of performance, load, and stress, often such tests require sending simultaneous traffic to an external API. That definition implies that such tests are multithreaded tests that usually test at the scope of a binary under test. However, these tests are critical for ensuring that there is no degradation in performance between versions and that the system can handle expected spikes in traffic.

虽然可以对小范围的单元进行性能、负载和压力测试，但这类测试往往需要并发地向外部 API 发送流量，因此属于多线程测试，测试范围通常是整个被测二进制程序。这些测试至关重要，能确保新版本没有性能退化，并确认系统能够应对预期的流量峰值。

As the scale of the load test grows, the scope of the input data also grows, and it eventually becomes difficult to generate the scale of load required to trigger bugs under load. Load and stress handling are “highly emergent” properties of a system; that is, these complex behaviors belong to the overall system but not the individual members. Therefore, it is important to make these tests look as close to production as possible. Each SUT requires resources akin to what production requires, and it becomes difficult to mitigate noise from the production topology.

随着负载测试规模扩大，输入数据的范围也会扩大，最终可能很难生成足以触发负载相关缺陷的流量。处理负载和压力的能力，是系统“高度涌现”的属性：这些复杂行为属于整个系统，而不属于单个组件。因此，测试应尽可能接近生产环境。每套 SUT 都需要与生产环境相近的资源，而生产拓扑带来的噪声也很难消除。

One area of research for eliminating noise in performance tests is in modifying the deployment topology—how the various binaries are distributed across a network of machines. The machine running a binary can affect the performance characteristics; thus, if in a performance diff test, the base version runs on a fast machine (or one with a fast network) and the new version on a slow one, it can appear like a performance regression. This characteristic implies that the optimal deployment is to run both versions on the same machine. If a single machine cannot fit both versions of the binary, an alternative is to calibrate by performing multiple runs and removing peaks and valleys.

消除性能测试噪声的一个研究方向，是调整部署拓扑，即各个二进制程序在机器网络中的分布方式。运行程序的机器会影响性能。因此，在性能差异测试中，如果基准版本运行在较快的机器或网络较快的机器上，新版本却运行在较慢的机器上，就可能看起来出现了性能回归缺陷。这意味着，最佳部署方式是在同一台机器上运行两个版本。如果单台机器容纳不下两个版本，也可以多次运行，剔除峰值和谷值，以此校准结果。

### Deployment Configuration Testing 部署配置测试

Tests of these type have the following characteristics:

- SUT: single-machine hermetic or cloud-deployed isolated
- Data: none
- Verification: assertions (doesn’t crash)

这类测试具有以下特点：

- SUT：单机封闭或云端部署的隔离环境
- 数据：无
- 验证：断言（不会崩溃）

Many times, it is not the code that is the source of defects but instead configuration: data files, databases, option definitions, and so on. Larger tests can test the integration of the SUT with its configuration files because these configuration files are read during the launch of the given binary.

很多时候，缺陷不是源于代码，而是源于配置，例如数据文件、数据库、选项定义等。二进制程序在启动时会读取这些配置文件，因此较大规模测试可以验证 SUT 与配置文件能否正确配合。

Such a test is really a smoke test of the SUT without needing much in the way of additional data or verification. If the SUT starts successfully, the test passes. If not, the test fails.

这实际上是针对 SUT 的冒烟测试，不需要太多额外数据或验证。SUT 启动成功，测试就通过；否则，测试失败。

### Exploratory Testing 探索性测试

Tests of these type have the following characteristics:

- SUT: production or shared staging
- Data: production or a known test universe
- Verification: manual

这类测试具有以下特点：

- SUT：生产环境或共享预发环境
- 数据：生产数据或一套已知的测试数据
- 验证：手动

Exploratory testing[^2] is a form of manual testing that focuses not on looking for behavioral regressions by repeating known test flows, but on looking for questionable behavior by trying out new user scenarios. Trained users/testers interact with a product through its public APIs, looking for new paths through the system and for which behavior deviates from either expected or intuitive behavior, or if there are security vulnerabilities.

探索性测试是一种手动测试，重点不是重复已知流程来查找行为回归缺陷，而是尝试新的用户场景，寻找可疑行为。受过训练的用户或测试人员通过公共 API 操作产品，探索新的系统路径，检查行为是否偏离预期或直觉，以及是否存在安全漏洞。

Exploratory testing is useful for both new and launched systems to uncover unanticipated behaviors and side effects. By having testers follow different reachable paths through the system, we can increase the system coverage and, when these testers identify bugs, capture new automated functional tests. In a sense, this is a bit like a manual “fuzz testing” version of functional integration testing.

无论是新系统还是已上线系统，探索性测试都有助于发现未预料到的行为和副作用。测试人员探索系统中不同的可达路径，可以扩大测试覆盖范围；发现缺陷后，还可以据此增加自动化功能测试。从某种意义上说，这就像功能集成测试的手动“模糊测试”版本。

>[^2]: James A. Whittaker, Exploratory Software Testing: Tips, Tricks, Tours, and Techniques to Guide Test Design(New York: Addison-Wesley Professional, 2009).
>
> 2     James A. Whittaker，《探索性软件测试：指导测试设计的提示、诀窍、探索路线与技术》（纽约：Addison-Wesley Professional，2009年）。

#### Limitations 局限性

Manual testing does not scale sublinearly; that is, it requires human time to perform the manual tests. Any defects found by exploratory tests should be replicated with an automated test that can run much more frequently.

手动测试的成本无法实现次线性增长，因为每次执行都需要投入人力时间。探索性测试发现的任何缺陷，都应通过自动化测试复现，以便更频繁地检查。

#### Bug bashes 集中找缺陷

One common approach we use for manual exploratory testing is the [bug bash](https://oreil.ly/zRLyA). A team of engineers and related personnel (managers, product managers, test engineers, anyone with familiarity with the product) schedules a “meeting,” but at this session, everyone involved manually tests the product. There can be some published guidelines as to particular focus areas for the bug bash and/or starting points for using the system, but the goal is to provide enough interaction variety to document questionable product behaviors and outright bugs.

我们常用的一种手动探索性测试方式，是集中找缺陷（bug bash）。工程师与相关人员，例如经理、产品经理、测试工程师及其他熟悉产品的人，约好一次“会议”，但所有参与者都用这段时间手动测试产品。组织者可以事先说明重点检查哪些区域，或从哪里开始操作系统。目的在于让交互方式足够多样，从而记录可疑的产品行为和明确的缺陷。

### A/B Diff Regression Testing  A/B 差异回归测试

Tests of these type have the following characteristics:

- SUT: two cloud-deployed isolated environments
- Data: usually multiplexed from production or sampled
- Verification: A/B diff comparison

这类测试具有以下特点：

- SUT：两个云端部署的隔离环境
- 数据：通常是复制分发的生产流量，或抽样数据
- 验证：A/B 差异比较

Unit tests cover expected behavior paths for a small section of code. But it is impossible to predict many of the possible failure modes for a given publicly facing product. Additionally, as Hyrum’s Law states, the actual public API is not the declared one but all user-visible aspects of a product. Given those two properties, it is no surprise that A/B diff tests are possibly the most common form of larger testing at Google. This approach conceptually dates back to 1998. At Google, we have been running tests based on this model since 2001 for most of our products, starting with Ads, Search, and Maps.

单元测试覆盖一小部分代码中预期的行为路径，但面向公众的产品有许多可能的故障模式，无法事先预料。此外，正如海勒姆定律所说，实际的公共 API 并不只是声明的接口，而是产品所有对用户可见的行为。有了这两个原因，A/B 差异测试可能成为谷歌最常见的较大规模测试形式，也就不足为奇。这一思路可以追溯到1998年。谷歌自2001年起，从广告、搜索和地图开始，陆续在大多数产品中运行基于这一模式的测试。

A/B diff tests operate by sending traffic to a public API and comparing the responses between old and new versions (especially during migrations). Any deviations in behavior must be reconciled as either anticipated or unanticipated (regressions). In this case, the SUT is composed of two sets of real binaries: one running at the candidate version and the other running at the base version. A third binary sends traffic and compares the results.

A/B 差异测试向公共 API 发送流量，比较新旧版本的响应，尤其适用于迁移期间。任何行为差异都必须查明：是预期变化，还是未预料到的回归缺陷。此时，SUT 包含两组真实的二进制程序，一组运行候选版本，另一组运行基准版本。第三个二进制程序负责发送流量并比较结果。

There are other variants. We use A-A testing (comparing a system to itself) to identify nondeterministic behavior, noise, and flakiness, and to help remove those from A-B diffs. We also occasionally use A-B-C testing, comparing the last production version, the baseline build, and a pending change, to make it easy at one glance to see not only the impact of an immediate change, but also the accumulated impacts of what would be the next-to-release version.

这种方法还有其他变体。我们用 A-A 测试，也就是把系统与自身比较，识别非确定性行为、噪声和不稳定性，帮助从 A-B 差异中排除这些干扰。有时也会用 A-B-C 测试，比较最近的生产版本、基线构建和待提交的变更，让人一眼就能看出当前变更的影响，以及下一个待发布版本的累积影响。

A/B diff tests are a cheap but automatable way to detect unanticipated side effects for any launched system.

A/B 差异测试成本低且可以自动化，能检测任何已上线系统中未预料到的副作用。

#### Limitations  局限性

Diff testing does introduce a few challenges to solve:

- *Approval*  
	Someone must understand the results enough to know whether any differences are expected. Unlike a typical test, it is not clear whether diffs are a good or bad thing (or whether the baseline version is actually even valid), and so there is often a manual step in the process.
- *Noise*  
	For a diff test, anything that introduces unanticipated noise into the results leads to more manual investigation of the results. It becomes necessary to remediate noise, and this is a large source of complexity in building a good diff test.
- *Coverage*  
	Generating enough useful traffic for a diff test can be a challenging problem. The test data must cover enough scenarios to identify corner-case differences, but it is difficult to manually curate such data.
- *Setup*  
	Configuring and maintaining one SUT is fairly challenging. Creating two at a time can double the complexity, especially if these share interdependencies.

差异测试也有一些需要解决的挑战：

- *审批*  
	必须有人充分理解结果，才能判断差异是否符合预期。与典型测试不同，差异本身无法说明结果是好是坏，甚至基线版本是否有效也不明确，因此流程中通常需要人工确认。
- *噪声*  
	任何意料之外的噪声都会增加人工调查差异测试结果的工作量。因此必须消除噪声，而这也是构建良好差异测试的主要复杂性来源。
- *覆盖率*  
	为差异测试生成足够的有效流量并不容易。测试数据必须覆盖足够多的场景，才能发现边角情况中的差异，但这类数据很难靠人工挑选和维护。
- *配置*  
	配置和维护一套 SUT 已经很有挑战。同时创建两套可能使复杂性翻倍，尤其是在两套系统存在共享依赖或相互依赖时。

### UAT 用户验收测试

Tests of these type have the following characteristics:

- SUT: machine-hermetic or cloud-deployed isolated
- Data: handcrafted
- Verification: assertions

这类测试具有以下特点：

- SUT：机器级封闭或云端部署的隔离环境
- 数据：手工构造
- 验证：断言

A key aspect of unit tests is that they are written by the developer writing the code under test. But that makes it quite likely that misunderstandings about the *intended* behavior of a product are reflected not only in the code, but also the unit tests. Such unit tests verify that code is “Working as implemented” instead of “Working as intended.”

单元测试的一个重要特点，是由被测代码的开发者编写。但这也意味着，对产品*预期*行为的误解，很可能同时体现在代码和单元测试中。这样的测试验证的是代码“按实现方式运行”，而不是“按预期运行”。

For cases in which there is either a specific end customer or a customer proxy (a customer committee or even a product manager), UATs are automated tests that exercise the product through public APIs to ensure the overall behavior for specific [user jour‐](https://oreil.ly/lOaOq) [neys ](https://oreil.ly/lOaOq)is as intended. Multiple public frameworks exist (e.g., Cucumber and RSpec) to make such tests writable/readable in a user-friendly language, often in the context of “runnable specifications.”

如果存在明确的最终客户或客户代表，例如客户委员会，甚至产品经理，就可以使用用户验收测试（UAT）。这类自动化测试通过公共 API 操作产品，确保特定[用户旅程](https://oreil.ly/lOaOq)的整体行为符合预期。Cucumber、RSpec 等公开可用的框架，支持用对用户友好的语言编写和阅读这类测试，通常采用“可运行规范”的形式。

Google does not actually do a lot of automated UAT and does not use specification languages very much. Many of Google’s products historically have been created by the software engineers themselves. There has been little need for runnable specification languages because those defining the intended product behavior are often fluent in the actual coding languages themselves.

谷歌实际上很少进行自动化 UAT，也不常使用规范语言。过去，谷歌的许多产品都由软件工程师自己创建。定义产品预期行为的人，通常也熟练掌握实际使用的编程语言，因此不太需要可运行的规范语言。

### Probers and Canary Analysis 探针和金丝雀分析

Tests of these type have the following characteristics:

- SUT: production
- Data: production
- Verification: assertions and A/B diff (of metrics)

这类测试具有以下特点：

- SUT：生产环境
- 数据：生产数据
- 验证：断言和 A/B 差异比较（指标）

Probers and canary analysis are ways to ensure that the production environment itself is healthy. In these respects, they are a form of production monitoring, but they are structurally very similar to other large tests.

探针和金丝雀分析用于确保生产环境本身健康。因此，它们属于生产监控的一种形式，但结构与其他大型测试非常相似。

Probers are functional tests that run encoded assertions against the production environment. Usually these tests perform well-known and deterministic read-only actions so that the assertions hold even though the production data changes over time. For example, a prober might perform a Google search at [www.google.com ](http://www.google.com/)and verify that a result is returned, but not actually verify the contents of the result. In that respect, they are “smoke tests” of the production system, but they provide early detection of major issues.

探针是一类功能测试，用预先编写的断言检查生产环境。通常，它们执行行为明确、结果确定的只读操作，使断言在生产数据随时间变化时仍然成立。例如，探针可以在 [www.google.com](http://www.google.com/) 执行一次谷歌搜索，只验证是否返回结果，而不检查结果的具体内容。从这个角度看，探针是生产系统的“冒烟测试”，可以及早发现重大问题。

Canary analysis is similar, except that it focuses on when a release is being pushed to the production environment. If the release is staged over time, we can run both prober assertions targeting the upgraded (canary) services as well as compare health metrics of both the canary and baseline parts of production and make sure that they are not out of line.

金丝雀分析与此类似，但关注的是版本发布到生产环境的过程。如果发布分阶段进行，既可以用探针断言检查已升级的金丝雀服务，也可以比较生产环境中金丝雀部分与基线部分的健康指标，确保没有异常偏离。

Probers should be used in any live system. If the production rollout process includes a phase in which the binary is deployed to a limited subset of the production machines (a canary phase), canary analysis should be used during that procedure.

任何在线系统都应使用探针。如果生产发布流程包含金丝雀阶段，即先把二进制程序部署到少量生产机器上，就应在该阶段使用金丝雀分析。

#### Limitations 局限性

Any issues caught at this point in time (in production) are already affecting end users.

在生产环境这个阶段发现的问题，已经在影响最终用户。

If a prober performs a mutable (write) action, it will modify the state of production. This could lead to one of three outcomes: nondeterminism and failure of the assertions, failure of the ability to write in the future, or user-visible side effects.

如果探针执行会改变状态的写入操作，就会修改生产环境的状态。这可能导致三种后果之一：结果不确定并使断言失败、后续无法写入，或产生用户可见的副作用。

### Disaster Recovery and Chaos Engineering 灾难恢复与混沌工程

Tests of these type have the following characteristics:

- SUT: production
- Data: production and user-crafted (fault injection)
- Verification: manual and A/B diff (metrics)

这类测试具有以下特点：

- SUT：生产环境
- 数据：生产数据和人工构造的数据（故障注入）
- 验证：手动和 A/B 差异比较（指标）

These test how well your systems will react to unexpected changes or failures.

这类测试检查系统应对意外变化或故障的能力。

For years, Google has run an annual war game called [DiRT 
](https://oreil.ly/17ffL)(Disaster Recovery Testing) during which faults are injected into our infrastructure at a nearly planetary scale. We simulate everything from datacenter fires to malicious attacks. In one memorable case, we simulated an earthquake that completely isolated our headquarters in Mountain View, California, from the rest of the company. Doing so exposed not only technical shortcomings but also revealed the challenge of running a company when all the key decision makers were unreachable.[^3]

多年来，谷歌每年都会开展一次名为[DiRT](https://oreil.ly/17ffL)（Disaster Recovery Testing，灾难恢复测试）的演练，向几乎遍布全球的基础设施注入故障。模拟场景从数据中心火灾到恶意攻击，无所不包。有一次令人印象深刻的演练，我们模拟地震，让位于加利福尼亚州山景城的总部与公司其他部分完全隔绝。这不仅暴露了技术短板，也揭示了所有关键决策者都无法联系时，维持公司运转有多困难。

The impacts of DiRT tests require a lot of coordination across the company; by contrast, chaos engineering is more of a “continuous testing” for your technical infrastructure. [Made popular by Netflix](https://oreil.ly/BCwdM), chaos engineering involves writing programs that continuously introduce a background level of faults into your systems and seeing what happens. Some of the faults can be quite large, but in most cases, chaos testing tools are designed to restore functionality before things get out of hand. The goal of chaos engineering is to help teams break assumptions of stability and reliability and help them grapple with the challenges of building resiliency in. Today, teams at Google perform thousands of chaos tests each week using our own home-grown system called Catzilla.

DiRT 测试影响广泛，需要全公司大量协调。相比之下，混沌工程更像是对技术基础设施的“持续测试”。这种做法[由Netflix推广](https://oreil.ly/BCwdM)，通过编写程序，不断向系统注入作为背景干扰的故障，再观察结果。有些故障规模很大，但大多数混沌测试工具都会设法在局面失控前恢复功能。混沌工程旨在帮助团队打破系统必然稳定可靠的假设，应对为系统构建韧性的挑战。如今，谷歌团队每周都使用内部开发的 Catzilla 系统运行数千次混沌测试。

These kinds of fault and negative tests make sense for live production systems that have enough theoretical fault tolerance to support them and for which the costs and risks of the tests themselves are affordable.

如果在线生产系统在理论上具备足够的容错能力，能够承受这类故障测试和负向测试，而且测试本身的成本与风险也在可承受范围内，那么开展这些测试就有意义。

> [^3]:	During this test, almost no one could get anything done, so many people gave up on work and went to one of our many cafes, and in doing so, we ended up creating a DDoS attack on our cafe teams!
>
> 3   在这次测试中，几乎没人能推进工作，许多人索性放下工作，去了公司众多咖啡厅中的某一家。结果，我们对咖啡厅服务团队制造了一场 DDoS 攻击！

#### Limitations 局限性

Any issues caught at this point in time (in production) are already affecting end users.

在生产环境这个阶段发现的问题，已经在影响最终用户。

DiRT is quite expensive to run, and therefore we run a coordinated exercise on an infrequent scale. When we create this level of outage, we actually cause pain and negatively impact employee performance.

DiRT 的运行成本很高，因此这种需要统一协调的演练不会频繁开展。制造如此大规模的服务中断，确实会带来不便，影响员工的工作表现。

If a prober performs a mutable (write) action, it will modify the state of production. This could lead to either nondeterminism and failure of the assertions, failure of the ability to write in the future, or user-visible side effects.

如果探针执行会改变状态的写入操作，就会修改生产环境的状态。这可能导致结果不确定并使断言失败、后续无法写入，或产生用户可见的副作用。

### User Evaluation 用户评估

Tests of these type have the following characteristics:

- SUT: production
- Data: production
- Verification: manual and A/B diffs (of metrics)

这类测试具有以下特点：

- SUT：生产环境
- 数据：生产数据
- 验证：手动和 A/B 差异比较（指标）

Production-based testing makes it possible to collect a lot of data about user behavior. We have a few different ways to collect metrics about the popularity of and issues with upcoming features, which provides us with an alternative to UAT:

- *Dogfooding*  
	It’s possible using limited rollouts and experiments to make features in production available to a subset of users. We do this with our own staff sometimes (eat our own dogfood), and they give us valuable feedback in the real deployment environment.
- *Experimentation*  
	A new behavior is made available as an experiment to a subset of users without their knowing. Then, the experiment group is compared to the control group at an aggregate level in terms of some desired metric. For example, in YouTube, we had a limited experiment changing the way video upvotes worked (eliminating the downvote), and only a portion of the user base saw this change.
	This is a [massively important approach for Google](https://oreil.ly/OAvqF). One of the first stories a Noogler hears upon joining the company is about the time Google launched an experiment changing the background shading color for AdWords ads in Google Search and noticed a significant increase in ad clicks for users in the experimental group versus the control group.
- *Rater* *evaluation*  
	Human raters are presented with results for a given operation and choose which one is “better” and why. This feedback is then used to determine whether a given change is positive, neutral, or negative. For example, Google has historically used rater evaluation for search queries (we have published the guidelines we give our raters). In some cases, the feedback from this ratings data can help determine launch go/no-go for algorithm changes. Rater evaluation is critical for nondeterministic systems like machine learning systems for which there is no clear correct answer, only a notion of better or worse.
	

在生产环境中测试，可以收集大量用户行为数据。我们用几种不同方法收集指标，了解待推出功能的受欢迎程度及存在的问题，作为 UAT 的替代方案：

- *内部试用*  
	通过小范围发布和实验，可以让部分用户使用生产环境中的功能。我们有时会让员工来试用自己的产品，也就是所谓“吃自己的狗粮”，由他们在真实部署环境中提供宝贵反馈。
- *实验*  
	在部分用户不知情的情况下，让他们体验作为实验的新行为，再根据某个目标指标，从总体上比较实验组与对照组。例如，YouTube 曾小范围试验改变视频赞踩机制，取消点踩，只有部分用户看到了这项变化。
	这是一个[对谷歌来说非常重要的方法](https://oreil.ly/OAvqF)。谷歌新员工入职后最早听到的故事之一，是谷歌曾通过实验改变搜索页面中 AdWords 广告的背景颜色，结果发现实验组用户的广告点击量明显高于对照组。
- *评分员评估*  
	向人工评分员展示某项操作的结果，让他们选出哪个“更好”并说明原因，再根据反馈判断变更的影响是正面、中性还是负面。例如，谷歌过去一直用评分员评估搜索查询结果，也已公开评分员使用的指南。有时，这些评分数据的反馈有助于决定算法变更是否上线。对于机器学习等非确定性系统，评分员评估至关重要，因为它们没有明确的正确答案，只有更好或更差之分。

## Large Tests and the Developer Workflow  大型测试与开发者工作流

We’ve talked about what large tests are, why to have them, when to have them, and how much to have, but we have not said much about the who. Who writes the tests? Who runs the tests and investigates the failures? Who owns the tests? And how do we make this tolerable?

前面已经讨论了大型测试是什么、为什么需要、何时开展，以及需要多少，但还没有深入讨论由谁负责。谁编写测试？谁运行测试并调查失败原因？谁对测试负责？怎样才能让这些工作不至于难以承受？

Although standard unit test infrastructure might not apply, it is still critical to integrate larger tests into the developer workflow. One way of doing this is to ensure that automated mechanisms for presubmit and post-submit execution exist, even if these are different mechanisms than the unit test ones. At Google, many of these large tests do not belong in TAP. They are nonhermetic, too flaky, and/or too resource intensive. But we still need to keep them from breaking or else they provide no signal and become too difficult to triage. What we do, then, is to have a separate post-submit continuous build for these. We also encourage running these tests presubmit, because that provides feedback directly to the author.

即使标准单元测试基础设施不适用，把较大规模测试纳入开发者工作流仍然至关重要。一种做法是提供提交前、提交后自动执行的机制，即使它不同于单元测试的机制。谷歌的许多大型测试不适合在 TAP 中运行，因为它们不具备封闭性、结果太不稳定，或资源消耗过大。但仍须保证这些测试正常工作，否则它们既无法提供信号，失败原因也会越来越难排查。因此，我们为它们建立了独立的提交后持续构建机制，也鼓励提交前运行，以便直接向代码作者反馈结果。

A/B diff tests that require manual blessing of diffs can also be incorporated into such a workflow. For presubmit, it can be a code-review requirement to approve any diffs in the UI before approving the change. One such test we have files release-blocking bugs automatically if code is submitted with unresolved diffs.

需要人工确认差异的 A/B 差异测试，也可以纳入这样的工作流。提交前，可以把一项要求加入代码审查：批准变更之前，必须先在界面中确认所有差异。我们有一个这样的测试，如果代码提交时仍有未处理的差异，就会自动创建阻止发布的缺陷报告。

In some cases, tests are so large or painful that presubmit execution adds too much developer friction. These tests still run post-submit and are also run as part of the release process. The drawback to not running these presubmit is that the taint makes it into the monorepo and we need to identify the culprit change to roll it back. But we need to make the trade-off between developer pain and the incurred change latency and the reliability of the continuous build.

有些测试规模过大或运行起来过于麻烦，提交前执行会给开发者增加太多负担。这类测试仍会在提交后运行，也会纳入发布流程。缺点是问题代码可能进入单体代码仓库，之后需要找出引入问题的变更并回滚。因此，必须在开发者负担、由此带来的变更延迟，以及持续构建的可靠性之间作出权衡。

### Authoring Large Tests 编写大型测试

Although the structure of large tests is fairly standard, there is still a challenge with creating such a test, especially if it is the first time someone on the team has done so.

虽然大型测试的结构比较固定，编写起来仍有挑战，尤其是团队第一次编写这类测试时。

The best way to make it possible to write such tests is to have clear libraries, documentation, and examples. Unit tests are easy to write because of native language support (JUnit was once esoteric but is now mainstream). We reuse these assertion libraries for functional integration tests, but we also have created over time libraries for interacting with SUTs, for running A/B diffs, for seeding test data, and for orchestrating test workflows.

要让工程师能够编写这类测试，最好的办法是提供清晰易用的库、文档和示例。单元测试容易编写，是因为有相应编程语言的原生支持；JUnit 曾经鲜为人知，如今已是主流。功能集成测试可以复用这些断言库，同时，我们也逐步建立了用于与 SUT 交互、运行 A/B 差异测试、预置测试数据及编排测试工作流的库。

Larger tests are more expensive to maintain, in both resources and human time, but not all large tests are created equal. One reason that A/B diff tests are popular is that they have less human cost in maintaining the verification step. Similarly, production SUTs have less maintenance cost than isolated hermetic SUTs. And because all of this authored infrastructure and code must be maintained, the cost savings can compound.

较大规模测试的维护成本更高，既消耗资源，也占用人力时间，但不同测试的成本并不相同。A/B 差异测试受欢迎的原因之一，是维护验证步骤所需的人力较少。同样，直接使用生产环境中的 SUT，也比维护隔离、封闭的 SUT 成本低。所有自行编写的基础设施和代码都需要维护，因此这些成本节省还会累积放大。

However, this cost must be looked at holistically. If the cost of manually reconciling diffs or of supporting and safeguarding production testing outweighs the savings, it becomes ineffective.

不过，必须从整体上评估成本。如果人工核对差异，或支持生产环境测试并保障其安全所需的成本，超过了节省的成本，这些做法就不再划算。

### Running Large Tests 运行大型测试

We mentioned above how our larger tests don’t fit in TAP and so we have alternate continuous builds and presubmits for them. One of the initial challenges for our engineers is how to even run nonstandard tests and how to iterate on them.

前面提到，较大规模测试不适合在 TAP 中运行，因此我们为它们提供了其他持续构建和提交前测试机制。工程师最先遇到的挑战之一，就是如何运行这些非标准测试，以及如何反复修改、运行它们。

As much as possible, we have tried to make our larger tests run in ways familiar for our engineers. Our presubmit infrastructure puts a common API in front of running both these tests and running TAP tests, and our code review infrastructure shows both sets of results. But many large tests are bespoke and thus need specific documentation for how to run them on demand. This can be a source of frustration for unfamiliar engineers.

我们尽量让较大规模测试采用工程师熟悉的运行方式。提交前测试基础设施为这些测试和 TAP 测试提供统一的运行 API，代码审查基础设施则展示两组结果。但许多大型测试都是定制的，需要专门文档说明如何按需运行。不熟悉这些测试的工程师，可能因此感到困扰。

#### Speeding up tests  加快测试运行

Engineers don’t wait for slow tests. The slower a test is, the less frequently an engineer will run it, and the longer the wait after a failure until it is passing again.

工程师不愿等待慢测试。测试越慢，运行频率就越低；一旦失败，恢复到通过状态所需的时间也越长。

The best way to speed up a test is often to reduce its scope or to split a large test into two smaller tests that can run in parallel. But there are some other tricks that you can do to speed up larger tests.

加快测试的最佳方法，通常是缩小测试范围，或把一个大型测试拆成两个可并行运行的较小测试。此外，还有一些技巧可以加快较大规模测试。

Some naive tests will use time-based sleeps to wait for nondeterministic action to occur, and this is quite common in larger tests. However, these tests do not have thread limitations, and real production users want to wait as little as possible, so it is best for tests to react the way real production users would. Approaches include the following:

- Polling for a state transition repeatedly over a time window for an event to complete with a frequency closer to microseconds. You can combine this with a timeout value in case a test fails to reach a stable state.
- Implementing an event handler.
- Subscribing to a notification system for an event completion.

一些简单实现的测试会休眠固定时长，等待发生时间不确定的操作完成，这在较大规模测试中很常见。但这类测试没有线程限制，而真实用户希望等待越短越好，因此最好让测试也像真实用户一样及时响应。可采用以下方法：

- 在一个时间窗口内，以接近微秒级的间隔反复轮询状态变化，等待事件完成。还可以设置超时时间，防止测试始终无法达到稳定状态。
- 实现事件处理程序。
- 订阅事件完成的通知。

Note that tests that rely on sleeps and timeouts will all start failing when the fleet running those tests becomes overloaded, which spirals because those tests need to be rerun more often, increasing the load further.

需要注意，当运行测试的机器集群过载时，依赖休眠和超时的测试都会开始失败。随后，更频繁的重跑又会进一步加重负载，形成恶性循环。

*Lower internal system timeouts and delays*  
	A production system is usually configured assuming a distributed deployment topology, but an SUT might be deployed on a single machine (or at least a cluster of colocated machines). If there are hardcoded timeouts or (especially) sleep statements in the production code to account for production system delay, these should be made tunable and reduced when running tests.

*Optimize test build time*  
	One downside of our monorepo is that all of the dependencies for a large test are built and provided as inputs, but this might not be necessary for some larger tests. If the SUT is composed of a core part that is truly the focus of the test and some other necessary peer binary dependencies, it might be possible to use prebuilt versions of those other binaries at a known good version. Our build system (based on the monorepo) does not support this model easily, but the approach is actually more reflective of production in which different services release at different versions.

*缩短系统内部的超时和延迟*。  
	生产系统通常按分布式部署拓扑配置，但 SUT 可能只部署在单台机器上，或至少集中在位置相近的一组机器上。如果生产代码为了应对系统延迟而硬编码了超时时间，尤其是休眠语句，就应将这些时长改为可配置，并在测试时缩短。

*优化测试构建时间*。  
	单体代码仓库的一个缺点，是大型测试的所有依赖都会被构建并作为测试输入，但有些较大规模测试并不需要如此。如果 SUT 包含真正需要测试的核心部分，以及其他必要的协作程序依赖，就可能对后者使用已知正常版本的预构建二进制文件。基于单体代码仓库的构建系统不容易支持这种模式，但它其实更接近生产环境，因为不同服务会分别发布不同版本。

#### Driving out flakiness  消除测试不稳定性

Flakiness is bad enough for unit tests, but for larger tests, it can make them unusable. A team should view eliminating flakiness of such tests as a high priority. But how can flakiness be removed from such tests?

结果不稳定，对单元测试已经很不利，对较大规模测试甚至可能使其完全无法使用。团队应优先消除这类测试的不稳定性。那么，具体该怎么做？

Minimizing flakiness starts with reducing the scope of the test—a hermetic SUT will not be at risk of the kinds of multiuser and real-world flakiness of production or a shared staging environment, and a single-machine hermetic SUT will not have the network and deployment flakiness issues of a distributed SUT. But you can mitigate other flakiness issues through test design and implementation and other techniques. In some cases, you will need to balance these with test speed.

减少不稳定性，首先要缩小测试范围。封闭的 SUT 不会受到生产环境或共享预发环境中多用户活动及现实干扰的影响；单机封闭的 SUT，也不会有分布式 SUT 的网络和部署不稳定问题。其他不稳定因素则可以通过测试设计、实现及其他技术来缓解，有时还需要与测试速度作出权衡。

Just as making tests reactive or event driven can speed them up, it can also remove flakiness. Timed sleeps require timeout maintenance, and these timeouts can be embedded in the test code. Increasing internal system timeouts can reduce flakiness, whereas reducing internal timeouts can lead to flakiness if the system behaves in a nondeterministic way. The key here is to identify a trade-off that defines both a tolerable system behavior for end users (e.g., our maximum allowable timeout is *n* seconds) but handles flaky test execution behaviors well.

让测试及时响应状态变化或采用事件驱动，不仅能加快运行，也能消除不稳定性。固定时长的休眠要求维护相应的超时设置，而这些设置可能嵌在测试代码中。延长系统内部超时时间可以减少不稳定性；如果系统行为具有非确定性，缩短超时时间则可能增加不稳定性。关键是找到平衡：既保证系统行为在最终用户可接受的范围内，例如最大允许超时为*n*秒，也能妥善应对测试执行中的不稳定因素。

A bigger problem with internal system timeouts is that exceeding them can lead to difficult errors to triage. A production system will often try to limit end-user exposure to catastrophic failure by handling possible internal system issues gracefully. For example, if Google cannot serve an ad in a given time limit, we don’t return a 500, we just don’t serve an ad. But this looks to a test runner as if the ad-serving code might be broken when there is just a flaky timeout issue. It’s important to make the failure mode obvious in this case and to make it easy to tune such internal timeouts for test scenarios.

系统内部超时还有一个更大的问题：超时后产生的错误可能很难排查。生产系统往往会妥善处理内部问题，尽量避免让最终用户遭遇灾难性故障。例如，如果谷歌无法在规定时间内提供广告，不会返回500错误，而是不展示广告。但对运行测试的人来说，这看起来像是广告服务代码出了问题，实际上却只是偶发超时。因此，必须清楚地呈现这种失败原因，并让内部超时时间易于针对测试场景调整。

#### Making tests understandable  让测试变得易懂

A specific case for which it can be difficult to integrate tests into the developer workflow is when those tests produce results that are unintelligible to the engineer running the tests. Even unit tests can produce some confusion—if my change breaks your test, it can be difficult to understand why if I am generally unfamiliar with your code—but for larger tests, such confusion can be insurmountable. Tests that are assertive must provide a clear pass/fail signal and must provide meaningful error output to help triage the source of failure. Tests that require human investigation, like A/B diff tests, require special handling to be meaningful or else risk being skipped during presubmit.

如果测试结果让运行测试的工程师看不懂，就很难将测试纳入开发者工作流。即使是单元测试也可能令人困惑：我的变更让你的测试失败，但我不熟悉你的代码，便很难理解原因。对较大规模测试而言，这种困惑可能更加难以克服。使用断言的测试必须给出明确的通过或失败信号，以及有意义的错误输出，帮助排查失败来源。A/B 差异测试等需要人工调查的测试，则要经过专门处理，才能让结果具有实际意义，否则就可能在提交前被跳过。

How does this work in practice? A good large test that fails should do the following:

- *Have a message that clearly identifies what the failure is*  
	The worst-case scenario is to have an error that just says “Assertion failed” and a stack trace. A good error anticipates the test runner’s unfamiliarity with the code and provides a message that gives context: “In test_ReturnsOneFullPageOfSearchResultsForAPopularQuery, expected 10 search results but got 1.” For a performance or A/B diff test that fails, there should be a clear explanation in the output of what is being measured and why the behavior is considered suspect.
- *Minimize the effort necessary to identify the root cause of  the discrepancy*  
	A stack trace is not useful for larger tests because the call chain can span multiple process boundaries. Instead, it’s necessary to produce a trace across the call chain or to invest in automation that can narrow down the culprit. The test should produce some kind of artifact to this effect. For example, [Dapper](https://oreil.ly/FXzbv) is a framework used by Google to associate a single request ID with all the requests in an RPC call chain, and all of the associated logs for that request can be correlated by that ID to facilitate tracing.
- *Provide support and contact information.*  
	It should be easy for the test runner to get help by making the owners and supporters of the test easy to contact.

在实践中该怎么做？设计良好的大型测试，失败时应做到以下几点：

- *用消息明确说明哪里出了问题*  
	最糟的错误输出，只有一句“断言失败”和一份堆栈跟踪。好的错误消息会考虑到运行测试的人可能不熟悉代码，并补充背景，例如：“在 test_ReturnsOneFullPageOfSearchResultsForAPopularQuery 中，预期返回10条搜索结果，实际只有1条。”性能测试或 A/B 差异测试失败时，输出应清楚说明测量的对象，以及为什么认为相关行为可疑。
- *尽量降低查明差异根因的工作量*  
	较大规模测试的调用链可能跨越多个进程，因此堆栈跟踪并没有用。需要生成覆盖整条调用链的跟踪信息，或投入自动化手段缩小问题来源的范围。测试应生成相应的产物。例如，谷歌使用的[Dapper](https://oreil.ly/FXzbv)框架，会为 RPC 调用链中的所有请求关联同一个请求 ID，再通过这个 ID 关联所有相关日志，方便追踪。
- *提供支持和联系信息*  
	应让测试负责人和支持人员易于联系，使运行测试的人能够方便地获得帮助。

#### Owning Large Tests  大型测试的责任归属 

Larger tests must have documented owners—engineers who can adequately review changes to the test and who can be counted on to provide support in the case of test failures. Without proper ownership, a test can fall victim to the following:

- It becomes more difficult for contributors to modify and update the test
- It takes longer to resolve test failures

较大规模测试必须明确记录负责人。这些工程师应有能力审查测试变更，并在测试失败时可靠地提供支持。责任归属不清，可能带来以下问题：

- 贡献者更难修改和更新测试
- 解决测试失败问题所需的时间更长

And the test rots.

测试也会逐渐失去维护。

Integration tests of components within a particular project should be owned by the project lead. Feature-focused tests (tests that cover a particular business feature across a set of services) should be owned by a “feature owner”; in some cases, this owner might be a software engineer responsible for the feature implementation end to end; in other cases it might be a product manager or a “test engineer” who owns the description of the business scenario. Whoever owns the test must be empowered to ensure its overall health and must have both the ability to support its maintenance and the incentives to do so.

项目内部组件的集成测试，应由项目负责人负责。围绕特定功能的测试，即跨多个服务验证某项业务功能的测试，应由“功能负责人”负责。有时，这个人是负责端到端功能实现的软件工程师；有时则是负责描述业务场景的产品经理或测试工程师。无论由谁负责，都必须有权保障测试整体健康，也必须有能力、有动力支持测试维护。

It is possible to build automation around test owners if this information is recorded in a structured way. Some approaches that we use include the following:

- *Regular code ownership*  
	In many cases, a larger test is a standalone code artifact that lives in a particular location in our codebase. In that case, we can use the OWNERS ([Chapter 9](#_bookmark664)) information already present in the monorepo to hint to automation that the owner(s) of a particular test are the owners of the test code.
- *Per-test* *annotations*  
	In some cases, multiple test methods can be added to a single test class or module, and each of these test methods can have a different feature owner. We use  per-language structured annotations to document the test owner in each of these cases so that if a particular test method fails, we can identify the owner to contact.

如果以结构化形式记录负责人信息，就可以据此实现自动化。我们采用的方法包括：

- *常规代码责任归属*  
	大型测试常以独立代码的形式存放在代码库的特定位置。此时，可以使用单体代码仓库中已有的 OWNERS 信息，参见第9章，让自动化工具知道：测试代码的负责人，也是该测试的负责人。

- *逐测试标注*  
	同一个测试类或模块可以包含多个测试方法，而每个方法可能对应不同的功能负责人。我们用各语言提供的结构化标注记录这些负责人，以便某个测试方法失败时，能够确定该联系谁。

## Conclusion 总结

A comprehensive test suite requires larger tests, both to ensure that tests match the fidelity of the system under test and to address issues that unit tests cannot adequately cover. Because such tests are necessarily more complex and slower to run, care must be taken to ensure such larger tests are properly owned, well maintained, and run when necessary (such as before deployments to production). Overall, such larger tests must still be made as small as possible (while still retaining fidelity) to avoid developer friction. A comprehensive test strategy that identifies the risks of a system, and the larger tests that address them, is necessary for most software projects.

完整的测试套件需要较大规模测试，既要让测试如实反映被测系统，也要覆盖单元测试难以充分处理的问题。这类测试必然更复杂、运行更慢，因此必须明确负责人、妥善维护，并在必要时运行，例如部署到生产环境之前。总体而言，即使是较大规模测试，也应在保留仿真度的前提下尽可能缩小，避免妨碍开发者工作。大多数软件项目都需要全面的测试策略，明确系统风险，以及缓解这些风险所需的较大规模测试。

## TL;DRs  内容提要

- Larger tests cover things unit tests cannot.
- Large tests are composed of a System Under Test, Data, Action, and Verification.
- A good design includes a test strategy that identifies risks and larger tests that mitigate them.
- Extra effort must be made with larger tests to keep them from creating friction in the developer workflow.

- 较大规模测试能覆盖单元测试无法覆盖的内容。
- 大型测试由被测系统、数据、操作和验证组成。
- 良好的设计包含测试策略，明确风险及缓解风险所需的较大规模测试。
- 较大规模测试需要额外投入，才能避免妨碍开发者工作流。

