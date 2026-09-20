
**CHAPTER 7**

# Measuring Engineering Productivity

# 第七章  度量工程生产力

**Written by  Ciera Jaspan**

**Edited by Riona Macnamara**

Google is a data-driven company. We back up most of our products and design decisions with hard data. The culture of data-driven decision making, using appropriate metrics, has some drawbacks, but overall, relying on data tends to make most decisions objective rather than subjective, which is often a good thing. Collecting and analyzing data on the human side of things, however, has its own challenges. Specifically, within software engineering, Google has found that having a team of specialists focus on engineering productivity itself to be very valuable and important as the company scales and can leverage insights from such a team.

谷歌是一家数据驱动型公司。我们的大多数产品和设计决策都有可靠的数据支持。采用恰当指标、以数据驱动决策的文化也有不足，但总体而言，依靠数据通常能让大多数决策更加客观，减少主观判断，这往往是件好事。不过，收集和分析与人的因素有关的数据，也有其独特的挑战。具体到软件工程，谷歌发现，随着公司规模扩大，设立一支专门研究工程生产力的专家团队非常重要，也很有价值，因为公司可以利用这支团队得出的见解。

## Why Should We Measure Engineering Productivity? 我们为什么要度量工程生产力？

Let’s presume that you have a thriving business (e.g., you run an online search engine), and you want to increase your business’s scope (enter into the enterprise application market, or the cloud market, or the mobile market). Presumably, to increase the scope of your business, you’ll need to also increase the size of your engineering organization. However, as organizations grow in size linearly, communication costs grow quadratically.[^1] Adding more people will be necessary to increase the scope of your business, but the communication overhead costs will not scale linearly as you add additional personnel. As a result, you won’t be able to scale the scope of your business linearly to the size of your engineering organization.

假设你的业务蓬勃发展，例如经营着一个在线搜索引擎，现在希望扩大业务范围，进入企业应用、云或移动市场。为此，你大概也需要扩大工程组织的规模。然而，组织规模线性增长时，沟通成本却按平方增长。扩大业务范围需要增加人员，但沟通开销并不会随人员增加而线性增长。因此，业务范围无法随着工程组织规模的增长而线性扩大。

There is another way to address our scaling problem, though: *we could make each individual more productive*. If we can increase the productivity of individual engineers in the organization, we can increase the scope of our business without the commensurate increase in communication overhead.

不过，解决规模扩展问题还有另一条路：*提高每个人的生产力*。如果能提高组织内每位工程师的生产力，就能扩大业务范围，而不必相应增加沟通开销。

Google has had to grow quickly into new businesses, which has meant learning how to make our engineers more productive. To do this, we needed to understand what makes them productive, identify inefficiencies in our engineering processes, and fix the identified problems. Then, we would repeat the cycle as needed in a continuous improvement loop. By doing this, we would be able to scale our engineering organization with the increased demand on it.

谷歌必须迅速拓展新业务，因此需要学会如何提高工程师的生产力。为此，我们需要了解哪些因素有助于工程师产出成果，找出工程流程中的低效环节，并解决发现的问题。随后，根据需要反复进行这些步骤，形成持续改进的循环。这样，工程组织就能随需求增长而扩大规模。

However, this improvement cycle *also* takes human resources. It would not be worthwhile to improve the productivity of your engineering organization by the equivalent of 10 engineers per year if it took 50 engineers per year to understand and fix productivity blockers. *Therefore, our goal is to not only improve software engineering productivity, but to do so efficiently.*

然而，这个改进循环*同样*需要人力。如果每年要投入50名工程师来查明并消除生产力障碍，换来的生产力提升却只相当于每年增加10名工程师的产出，就不值得。*因此，我们的目标不仅是提高软件工程生产力，还要以高效的方式实现这一提升。*

At Google, we addressed these trade-offs by creating a team of researchers dedicated to understanding engineering productivity. Our research team includes people from the software engineering research field and generalist software engineers, but we also include social scientists from a variety of fields, including cognitive psychology and behavioral economics. The addition of people from the social sciences allows us to not only study the software artifacts that engineers produce, but to also understand the human side of software development, including personal motivations, incentive structures, and strategies for managing complex tasks. The goal of the team is to take a data-driven approach to measuring and improving engineering productivity.

为处理这些权衡，谷歌成立了一支专门研究工程生产力的团队。团队成员既有软件工程研究人员和通才型软件工程师，也有来自认知心理学、行为经济学等不同领域的社会科学研究人员。社会科学研究人员的加入，让我们不仅能研究工程师产出的软件制品，还能理解软件开发中人的因素，包括个人动机、激励结构，以及管理复杂任务的策略。这支团队的目标是采用数据驱动的方法，度量并提高工程生产力。

In this chapter, we walk through how our research team achieves this goal. This begins with the triage process: there are many parts of software development that we *can* measure, but what *should* we measure? After a project is selected, we walk through how the research team identifies meaningful metrics that will identify the problematic parts of the process. Finally, we look at how Google uses these metrics to track improvements to productivity.

本章将介绍研究团队如何实现这一目标。首先是筛选项目：软件开发中有许多方面*可以*度量，但哪些才是应该度量的？选定项目后，我们会介绍研究团队如何确定有意义的指标，找出流程中存在问题的环节。最后，再看谷歌如何利用这些指标跟踪生产力的提升。

For this chapter, we follow one concrete example posed by the C++ and Java language teams at Google: readability. For most of Google’s existence, these teams have managed the readability process at Google. (For more on readability, see Chapter 3.) The readability process was put in place in the early days of Google, before automatic formatters (Chapter 8 and linters that block submission were commonplace (Chapter 9). The process itself is expensive to run because it requires hundreds of engineers performing readability reviews for other engineers in order to grant readability to them. Some engineers viewed it as an archaic hazing process that no longer held utility, and it was a favorite topic to argue about around the lunch table. The concrete question from the language teams was this: is the time spent on the readability process worthwhile?

本章将贯穿一个具体案例：谷歌 C++ 和 Java 语言团队提出的 Readability 资格认证问题。谷歌成立以来的大部分时间里，这些团队一直负责管理 Readability 流程。（有关 Readability 的更多内容，参见第3章。）这套流程在谷歌早期就已建立，当时自动格式化工具（第8章）和能阻止代码提交的 lint 检查工具（第9章）还不普及。流程本身的运行成本很高，需要数百名工程师为其他工程师进行 Readability 审查，以授予他们相应资格。一些工程师认为，这是一套过时的、刻意刁难新人的入门仪式，已经没有实用价值，也因此常在午餐桌上引发争论。语言团队提出的具体问题是：花在 Readability 流程上的时间值得吗？

> [^1]: Frederick P. Brooks, The Mythical Man-Month: Essays on Software Engineering (New York: Addison-Wesley, 1995).
>
> 1   Frederick P. Brooks，《人月神话：软件工程随笔》（纽约：Addison-Wesley，1995）。

## Triage: Is It Even Worth Measuring? 项目筛选：究竟是否值得度量？

Before we decide how to measure the productivity of engineers, we need to know when a metric is even worth measuring. The measurement itself is expensive: it takes people to measure the process, analyze the results, and disseminate them to the rest of the company. Furthermore, the measurement process itself might be onerous and slow down the rest of the engineering organization. Even if it is not slow, tracking progress might change engineers’ behavior, possibly in ways that mask the underlying issues. We need to measure and estimate smartly; although we don’t want to guess, we shouldn’t waste time and resources measuring unnecessarily.

在决定如何度量工程师的生产力之前，首先需要判断某个指标是否值得度量。度量本身成本不低：需要投入人力，测量流程、分析结果，再把结果传达给公司其他人。此外，度量过程本身可能十分繁琐，拖慢工程组织其他部分的工作。即使不会拖慢工作，跟踪进展也可能改变工程师的行为，甚至掩盖根本问题。我们需要审慎地度量和估计：既不能凭空猜测，也不该把时间和资源浪费在不必要的度量上。

At Google, we’ve come up with a series of questions to help teams determine whether it’s even worth measuring productivity in the first place. We first ask people to describe what they want to measure in the form of a concrete question; we find that the more concrete people can make this question, the more likely they are to derive benefit from the process. When the readability team approached us, its question was simple: are the costs of an engineer going through the readability process worth the benefits they might be deriving for the company?

在谷歌，我们整理了一系列问题，帮助团队先判断是否值得度量生产力。首先，请他们把想要度量的内容表述成一个具体问题。我们发现，问题越具体，团队就越可能从度量过程中获益。Readability 团队找到我们时，问题很简单：工程师完成 Readability 流程可能为公司带来的收益，是否值得付出相应成本？

We then ask them to consider the following aspects of their question:

*What result are you expecting, and why?*  
    Even though we might like to pretend that we are neutral investigators, we are not. We do have preconceived notions about what ought to happen. By acknowledging this at the outset, we can try to address these biases and prevent post hoc explanations of the results.  
    When this question was posed to the readability team, it noted that it was not sure. People were certain the costs had been worth the benefits at one point in time, but with the advent of autoformatters and static analysis tools, no one was entirely certain. There was a growing belief that the process now served as a hazing ritual. Although it might still provide engineers with benefits (and they had survey data showing that people did claim these benefits), it was not clear whether it was worth the time commitment of the authors or the reviewers of the code.

*If the data supports your expected result, what action will be taken?*  
    We ask this because if no action will be taken, there is no point in measuring. Notice that an action might in fact be “maintain the status quo” if there is a planned change that will occur if we didn’t have this result.  
    When asked about this, the answer from the readability team was straightforward: if the benefit was enough to justify the costs of the process, they would link to the research and the data on the FAQ about readability and advertise it to set expectations.

*If we get a negative result, will appropriate action be taken?*  
    We ask this question because in many cases, we find that a negative result will not change a decision. There might be other inputs into a decision that would override any negative result. If that is the case, it might not be worth measuring in the first place. This is the question that stops most of the projects that our research team takes on; we learn that the decision makers were interested in knowing the results, but for other reasons, they will not choose to change course.  
    In the case of readability, however, we had a strong statement of action from the team. It committed that, if our analysis showed that the costs either outweighed the benefit or the benefits were negligible, the team would kill the process. As different programming languages have different levels of maturity in formatters and static analyses, this evaluation would happen on a per-language basis.

*Who is going to decide to take action on the result, and when would they do it?*  
    We ask this to ensure that the person requesting the measurement is the one who is empowered to take action (or is doing so directly on their behalf). Ultimately, the goal of measuring our software process is to help people make business decisions. It’s important to understand who that individual is, including what form of data convinces them. Although the best research includes a variety of approaches (everything from structured interviews to statistical analyses of logs), there might be limited time in which to provide decision makers with the data they need. In those cases, it might be best to cater to the decision maker. Do they tend to make decisions by empathizing through the stories that can be retrieved from interviews?[^2] Do they trust survey results or logs data? Do they feel comfortable with complex statistical analyses? If the decider doesn’t believe the form of the result in principle, there is again no point in measuring the process.  
    In the case of readability, we had a clear decision maker for each programming language. Two language teams, Java and C++, actively reached out to us for assistance, and the others were waiting to see what happened with those languages first.[^3] The decision makers trusted engineers’ self-reported experiences for understanding happiness and learning, but the decision makers wanted to see “hard numbers” based on logs data for velocity and code quality. This meant that we needed to include both qualitative and quantitative analysis for these metrics. There was not a hard deadline for this work, but there was an internal conference that would make for a useful time for an announcement if there was going to be a change. That deadline gave us several months in which to complete the work.

接着，我们请他们从以下几个方面考虑这个问题：

*你预期会得到什么结果？为什么？*
    我们也许愿意把自己看作中立的研究者，但事实并非如此。对于应该出现什么结果，我们确实有先入为主的想法。一开始就承认这一点，才能设法处理这些偏见，避免事后为结果寻找解释。
    面对这个问题，Readability 团队表示并不确定。大家确信，这套流程曾经确实值得投入，但随着自动格式化和静态分析工具的出现，谁也不再完全确定。越来越多的人认为，它如今成了一种刁难新人的入门仪式。虽然这套流程可能仍能让工程师受益，而且调查数据也表明工程师确实报告了这些收益，但它是否值得代码作者和审查者投入时间，仍不清楚。

*如果数据支持你的预期结果，会采取什么行动？*
    之所以这样问，是因为如果不采取任何行动，度量就没有意义。注意，如果没有这一结果就会按计划作出变更，那么“维持现状”本身也可以是一项行动。
    Readability 团队的回答很明确：如果收益足以抵偿流程的成本，就会在 Readability 常见问题页面中附上研究和数据的链接，并加以宣传，帮助大家形成合理预期。

*如果得到负面结果，会采取适当的行动吗？*
    提出这个问题，是因为我们发现，在许多情况下，负面结果并不会改变决策。决策中的其他考量可能会压过任何负面结果。如果是这样，一开始就可能不值得度量。我们研究团队经手的大多数项目，都是在这个问题上被叫停的：决策者虽然想知道结果，却会因为其他原因而坚持原有方向。
    不过，在 Readability 案例中，团队作出了明确的行动承诺：如果分析表明成本超过收益，或收益可以忽略不计，就取消这套流程。由于不同编程语言的格式化和静态分析工具成熟度不同，评估会按语言分别进行。

*谁会决定根据结果采取行动？何时行动？*
    这样问，是为了确保提出度量请求的人有权采取行动，或直接代表有权行动的人提出请求。归根结底，度量软件流程是为了帮助人们作出业务决策。因此，要了解决策者是谁，以及什么形式的数据能说服他们。最好的研究会综合多种方法，从结构化访谈到日志统计分析，但我们可能只有有限的时间来提供决策者所需的数据。在这种情况下，最好考虑决策者接受数据的方式：他们是否倾向于从访谈故事中产生共鸣，并据此决策？他们信任调查结果还是日志数据？他们能否接受复杂的统计分析？如果决策者根本不认可呈现结果所用的方法，度量流程也就没有意义。
    在 Readability 项目中，每种编程语言都有明确的决策者。Java 和 C++ 两个语言团队主动寻求我们的帮助，其他团队则想先看看这两种语言的研究结果。对于满意度和学习情况，决策者信任工程师自述的体验；但对于工作速度和代码质量，他们希望看到基于日志数据的“硬数字”。这意味着，我们需要对这些指标同时进行定性和定量分析。这项工作没有硬性截止日期，不过，如果要作出变更，即将举行的一次内部会议会是合适的宣布时机。以此为期限，我们有几个月的时间完成研究。

By asking these questions, we find that in many cases, measurement is simply not worthwhile…and that’s OK! There are many good reasons to not measure the impact of a tool or process on productivity. Here are some examples that we’ve seen:

*You can’t afford to change the process/tools right now*  
    There might be time constraints or financial constraints that prevent this. For example, you might determine that if only you switched to a faster build tool, it would save hours of time every week. However, the switchover will mean pausing development while everyone converts over, and there’s a major funding deadline approaching such that you cannot afford the interruption. Engineering trade-offs are not evaluated in a vacuum—in a case like this, it’s important to realize that the broader context completely justifies delaying action on a result.

*Any results will soon be invalidated by other factors*  
    Examples here might include measuring the software process of an organization just before a planned reorganization. Or measuring the amount of technical debt for a deprecated system.  
    The decision maker has strong opinions, and you are unlikely to be able to provide a large enough body of evidence, of the right type, to change their beliefs.  
    This comes down to knowing your audience. Even at Google, we sometimes find people who have unwavering beliefs on a topic due to their past experiences. We have found stakeholders who never trust survey data because they do not believe self-reports. We’ve also found stakeholders who are swayed best by a compelling narrative that was informed by a small number of interviews. And, of course, there are stakeholders who are swayed only by logs analysis. In all cases, we attempt to triangulate on the truth using mixed methods, but if a stakeholder is limited to believing only in methods that are not appropriate for the problem, there is no point in doing the work.

*The results will be used only as vanity metrics to support something you were going to do anyway*  
    This is perhaps the most common reason we tell people at Google not to measure a software process. Many times, people have planned a decision for multiple reasons, and improving the software development process is only one benefit of several. For example, the release tool team at Google once requested a measurement to a planned change to the release workflow system. Due to the nature of the change, it was obvious that the change would not be worse than the current state, but they didn’t know if it was a minor improvement or a large one. We asked the team: if it turns out to only be a minor improvement, would you spend the resources to implement the feature anyway, even if it didn’t look to be worth the investment? The answer was yes! The feature happened to improve productivity, but this was a side effect: it was also more performant and lowered the release tool team’s maintenance burden.  

*The only metrics available are not precise enough to measure the problem and can be confounded by other factors*  
    In some cases, the metrics needed (see the upcoming section on how to identify metrics) are simply unavailable. In these cases, it can be tempting to measure using other metrics that are less precise (lines of code written, for example). However, any results from these metrics will be uninterpretable. If the metric confirms the stakeholders’ preexisting beliefs, they might end up proceeding with their plan without consideration that the metric is not an accurate measure. If it does not confirm their beliefs, the imprecision of the metric itself provides an easy explanation, and the stakeholder might, again, proceed with their plan.

问过这些问题后，我们发现，许多情况下根本不值得度量。这没有关系！不去度量某个工具或流程对生产力的影响，也有很多充分的理由。下面是我们遇到的一些例子：

*目前无法承担改变流程或工具的成本*  
    时间或资金限制可能让变更无法进行。例如，你可能已经确定，改用更快的构建工具每周能节省数小时。然而，在所有人完成切换之前，开发工作必须暂停；此时，一个重要的资金期限又即将到来，你无法承受这样的中断。工程权衡不能脱离实际环境。在这种情况下，要认识到，考虑整体情况后，推迟根据结果采取行动完全合理。

*任何结果很快就会因其他因素而失效*  
    例如，在组织即将按计划重组之前度量其软件流程，或者度量一个已弃用系统的技术债务量。  
    决策者有根深蒂固的看法，而你不太可能提供足够多、类型又恰当的证据来改变他们的想法。  
    这归根结底取决于你是否了解受众。即使在谷歌，也有人因过去的经历而对某个问题深信不疑。有些利益相关者从不相信调查数据，因为他们不信任自述信息；另一些人则最容易被基于少量访谈、令人信服的叙述打动；当然，也有人只接受日志分析。无论哪种情况，我们都会尝试混合使用多种方法，相互印证以了解实情。但如果利益相关者只相信不适合该问题的方法，这项工作就没有意义。

*结果只会被当作虚荣指标，为无论如何都会做的事情提供支持*  
    这也许是我们在谷歌劝大家不要度量软件流程的最常见原因。很多时候，人们已经出于多种原因计划作出某项决策，改进软件开发流程只是它的若干收益之一。例如，谷歌的发布工具团队曾请我们度量发布工作流系统中一项计划变更的效果。从变更的性质来看，显然不会比现状更差，只是不知道改进幅度有多大。我们问：如果最终只有小幅改进，即使看起来不值得投入，你们仍会花资源实现这个功能吗？答案是肯定的！这个功能确实能提高生产力，但这只是附带效果；它的性能也更好，还能减轻发布工具团队的维护负担。

*现有指标不够精确，无法度量所研究的问题，还可能受到其他因素的干扰*  
    有时，所需的指标根本无法获得，如何确定指标将在后文讨论。这时，人们很容易转而使用不够精确的指标，例如编写的代码行数。然而，这些指标得出的结果都无法作出有意义的解释。如果结果印证了利益相关者原有的看法，他们可能就会继续执行计划，忽略指标并不准确这一事实；如果结果没有印证原有看法，又很容易归因于指标本身不够精确，利益相关者仍可能照原计划行事。

When you are successful at measuring your software process, you aren’t setting out to prove a hypothesis correct or incorrect; *success means giving a stakeholder the data they need to make a decision*. If that stakeholder won’t use the data, the project is always a failure. We should only measure a software process when a concrete decision will be made based on the outcome. For the readability team, there was a clear decision to be made. If the metrics showed the process to be beneficial, they would publicize the result. If not, the process would be abolished. Most important, the readability team had the authority to make this decision.

度量软件流程的目的，不是证明某个假设正确或错误；*成功意味着为利益相关者提供决策所需的数据*。如果利益相关者不会使用这些数据，项目就一定是失败的。只有在会根据结果作出具体决策时，才应该度量软件流程。Readability 团队面临的决策很明确：如果指标表明流程有益，就公布研究结果；否则，就取消这套流程。最重要的是，Readability 团队有权作出这个决定。

> [^2]: It’s worth pointing out here that our industry currently disparages “anecdata,” and everyone has a goal of being “data driven.” Yet anecdotes continue to exist because they are powerful. An anecdote can provide context and narrative that raw numbers cannot; it can provide a deep explanation that resonates with others because it mirrors personal experience. Although our researchers do not make decisions on anecdotes, we do use and encourage techniques such as structured interviews and case studies to deeply understand phenomena and provide context to quantitative data.
>
> 2 值得指出的是，业界目前往往轻视“轶事数据”，人人都以“数据驱动”为目标。然而，轶事仍有其地位，因为它们很有说服力。轶事能够提供原始数字无法呈现的背景和叙事，也能给出深入的解释，因贴近个人经历而引发共鸣。我们的研究人员虽然不依据轶事作出决策，但确实使用并鼓励结构化访谈、案例研究等方法，以深入理解现象，为定量数据提供背景。 
>
> [^3]: Java and C++ have the greatest amount of tooling support. Both have mature formatters and static analysis tools that catch common mistakes. Both are also heavily funded internally. Even though other language teams, like Python, were interested in the results, clearly there was not going to be a benefit for Python to remove readability if we couldn’t even show the same benefit for Java or C++.
>
> 3 Java 和 C++ 获得的工具支持最多，两者都有成熟的格式化和静态分析工具，能发现常见错误，也都获得了大量内部资金支持。Python 等其他语言团队虽然也对结果感兴趣，但很显然，如果连 Java 或 C++ 都无法证明取消 Readability 流程有益，Python 就更不会从中受益。

## Selecting Meaningful Metrics with Goals and Signals  根据目标和信号选择有意义的指标

After we decide to measure a software process, we need to determine what metrics to use. Clearly, lines of code (LOC) won’t do,[^4] but how do we actually measure engineering productivity?

决定度量某个软件流程后，就需要确定使用哪些指标。显然，代码行数（LOC）不合适，但究竟该如何度量工程生产力呢？

At Google, we use the Goals/Signals/Metrics (GSM) framework to guide metrics creation.

在谷歌，我们用目标/信号/指标（GSM）框架来指导指标的制定。

- A *goal* is a desired end result. It’s phrased in terms of what you want to understand at a high level and should not contain references to specific ways to measure it.
- A signal is how you might know that you’ve achieved the end result. Signals are things we would *like* to measure, but they might not be measurable themselves.
- A *metric* is proxy for a signal. It is the thing we actually can measure. It might not be the ideal measurement, but it is something that we believe is close enough.

- *目标* 是期望达到的最终结果。它从整体层面表述你希望了解什么，不应涉及具体的度量方法。
- *信号* 是判断是否达到最终结果的依据。信号是我们*想要*度量的事物，但其本身未必能够度量。
- *指标* 是信号的代理，是我们实际上能够度量的事物。它可能不是理想的度量，但我们认为它已足够接近所要反映的信号。

The GSM framework encourages several desirable properties when creating metrics. First, by creating goals first, then signals, and finally metrics, it prevents the *streetlight* *effect*. The term comes from the full phrase “looking for your keys under the streetlight”: if you look only where you can see, you might not be looking in the right place. With metrics, this occurs when we use the metrics that we have easily accessible and that are easy to measure, regardless of whether those metrics suit our needs. Instead, GSM forces us to think about which metrics will actually help us achieve our goals, rather than simply what we have readily available.

GSM 框架有助于在制定指标时形成几个良好特性。首先，先确定目标，再确定信号，最后确定指标，可以避免*路灯*效应。这个说法来自“在路灯下找钥匙”：如果只在看得见的地方找，可能根本就找错了地方。在度量中，如果只使用容易获得、容易测量的指标，不管它们是否符合需求，就会出现同样的问题。GSM 则要求我们思考，哪些指标真正有助于实现目标，而不只是看看手头有哪些现成指标。

Second, GSM helps prevent both metrics creep and metrics bias by encouraging us to come up with the appropriate set of metrics, using a principled approach, *in advance* of actually measuring the result. Consider the case in which we select metrics without a principled approach and then the results do not meet our stakeholders’ expectations. At that point, we run the risk that stakeholders will propose that we use different metrics that they believe will produce the desired result. And because we didn’t select based on a principled approach at the start, there’s no reason to say that they’re wrong! Instead, GSM encourages us to select metrics based on their ability to measure the original goals. Stakeholders can easily see that these metrics map to their original goals and agree, in advance, that this is the best set of metrics for measuring the outcomes.

其次，GSM 鼓励我们在实际度量结果之前，按明确的原则选定一组合适的指标，从而避免指标不断扩张，以及指标选择上的偏见。假设最初选指标时没有明确原则，测出的结果又不符合利益相关者的预期，他们就可能提议改用另一组指标，认为这样能得出想要的结果。而我们既然一开始就没有依循原则，也就没有理由说他们错了！GSM 则鼓励我们根据指标能否度量最初的目标来作选择。利益相关者很容易看清指标与原始目标的对应关系，并提前同意，这是度量结果最合适的一组指标。

Finally, GSM can show us where we have measurement coverage and where we do not. When we run through the GSM process, we list all our goals and create signals for each one. As we will see in the examples, not all signals are going to be measurable and that’s OK! With GSM, at least we have identified what is not measurable. By identifying these missing metrics, we can assess whether it is worth creating new metrics or even worth measuring at all.

最后，GSM 能让我们看清哪些方面已被度量覆盖，哪些还没有。在 GSM 流程中，我们列出所有目标，并为每个目标确定信号。后面的例子会说明，并非所有信号都能度量，这没有关系！借助 GSM，我们至少能明确哪些信号无法度量。找出这些缺失的指标后，就能评估是否值得制定新指标，甚至判断整个问题是否值得度量。

The important thing is to maintain *traceability*. For each metric, we should be able to trace back to the signal that it is meant to be a proxy for and to the goal it is trying to measure. This ensures that we know which metrics we are measuring and why we are measuring them.

关键是保持*可追溯性*。每个指标都应能追溯到它所代表的信号，以及它试图度量的目标。这样，我们才能清楚自己在度量哪些指标，以及为什么要度量它们。

> [^4]: “From there it is only a small step to measuring ‘programmer productivity’ in terms of ‘number of lines of code produced per month.’ This is a very costly measuring unit because it encourages the writing of insipid code, but today I am less interested in how foolish a unit it is from even a pure business point of view. My point today is that, if we wish to count lines of code, we should not regard them as ‘lines produced’ but as ‘lines spent’: the current conventional wisdom is so foolish as to book that count on the wrong side of the ledger.” Edsger Dijkstra, on the cruelty of really teaching computing science, EWD Manuscript 1036.
>
> 4  “由此再往前走一小步，就会用‘每月产出的代码行数’来度量‘程序员生产力’。这种度量单位代价高昂，因为它鼓励人们编写乏善可陈的代码。不过，今天我不想着重讨论，即使仅从商业角度看，这种单位也有多么愚蠢。我今天要说的是，如果要统计代码行数，就不应把它们视为‘产出的行数’，而应视为‘耗费的行数’：当下通行的观念竟愚蠢到把这个数字记在了账本错误的一侧。”Edsger Dijkstra，《论真正教授计算机科学的残酷性》，EWD 手稿1036。

## Goals  目标

A goal should be written in terms of a desired property, without reference to any metric. By themselves, these goals are not measurable, but a good set of goals is something that everyone can agree on before proceeding onto signals and then metrics.

目标应描述期望具备的特性，不涉及任何指标。这些目标本身无法度量，但一组合适的目标，应当能让大家先达成共识，再继续确定信号和指标。

To make this work, we need to have identified the correct set of goals to measure in the first place. This would seem straightforward: surely the team knows the goals of their work! However, our research team has found that in many cases, people forget to include all the possible *trade-offs within productivity*, which could lead to mismeasurement.

要让这种方法奏效，首先需要选对要度量的目标。这似乎很简单：团队当然知道自己的工作目标！但研究团队发现，人们常常没有考虑到*生产力各方面之间所有可能的权衡*，从而导致度量失当。

Taking the readability example, let’s assume that the team was so focused on making the readability process fast and easy that it had forgotten the goal about code quality. The team set up tracking measurements for how long it takes to get through the review process and how happy engineers are with the process. One of our teammates proposes the following:  

> I can make your review velocity very fast: just remove code reviews entirely.

以 Readability 为例，假设团队一心想让流程更快、更轻松，却忘了代码质量这一目标。团队设置了指标，跟踪完成审查所需的时间，以及工程师对流程的满意程度。这时，我们的一位团队成员提出：  

> 我可以让你们的审查速度大幅提高：直接取消代码审查就行。

Although this is obviously an extreme example, teams forget core trade-offs all the time when measuring: they become so focused on improving velocity that they forget to measure quality (or vice versa). To combat this, our research team divides productivity into five core components. These five components are in trade-off with one another, and we encourage teams to consider goals in each of these components to ensure that they are not inadvertently improving one while driving others downward. To help people remember all five components, we use the mnemonic “QUANTS”:

***Quality** of the code*  
    What is the quality of the code produced? Are the test cases good enough to prevent regressions? How good is an architecture at mitigating risk and changes?

***Attention** from engineers*  
    How frequently do engineers reach a state of flow? How much are they distracted by notifications? Does a tool encourage engineers to context switch?

*Intellectual complexity*  
    How much cognitive load is required to complete a task? What is the inherent complexity of the problem being solved? Do engineers need to deal with unnecessary complexity?

*Tempo and velocity*  
    How quickly can engineers accomplish their tasks? How fast can they push their releases out? How many tasks do they complete in a given timeframe?

*Satisfaction*  
    How happy are engineers with their tools? How well does a tool meet engineers’ needs? How satisfied are they with their work and their end product? Are engineers feeling burned out?

这个例子显然很极端，但团队在度量时经常会忽略关键的权衡：一心提高速度，却忘了度量质量，或者反过来。为避免这种情况，我们的研究团队把生产力分为五个核心方面。这五个方面之间存在权衡，因此我们鼓励团队考虑每个方面的目标，确保不会在无意中改善一项，却让其他项变差。为了方便记住这五个方面，我们使用助记词“QUANTS”：

代码的***质量***  
    产出的代码质量如何？测试用例是否足以防止回归缺陷？架构能在多大程度上降低风险、减轻变更带来的影响？

工程师的***注意力***  
    工程师多常能进入心流状态？通知会在多大程度上分散他们的注意力？工具是否会促使工程师切换上下文？

*认知复杂度*  
    完成任务需要多大的认知负荷？待解决的问题本身有多复杂？工程师是否需要应对不必要的复杂性？

*节奏和速度*  
    工程师能多快完成任务？能多快发布版本？在给定时间内能完成多少任务？

*满意度*  
    工程师对工具有多满意？工具能在多大程度上满足需求？他们对自己的工作和最终产品有多满意？是否感到职业倦怠？

Going back to the readability example, our research team worked with the readability team to identify several productivity goals of the readability process:

*Quality of the code*  
    Engineers write higher-quality code as a result of the readability process; they write more consistent code as a result of the readability process; and they contribute to a culture of code health as a result of the readability process.

*Attention from engineers*  
    We did not have any attention goal for readability. This is OK! Not all questions about engineering productivity involve trade-offs in all five areas.

*Intellectual complexity*  
    Engineers learn about the Google codebase and best coding practices as a result of the readability process, and they receive mentoring during the readability process.

*Tempo and velocity*  
    Engineers complete work tasks faster and more efficiently as a result of the readability process.

*Satisfaction*  
    Engineers see the benefit of the readability process and have positive feelings about participating in it.

回到 Readability 的例子，研究团队与 Readability 团队合作，为这套流程确定了几个生产力目标：

*代码的质量*  
    Readability 流程让工程师写出质量更高、一致性更好的代码，并为重视代码健康的文化作出贡献。

*工程师的注意力*  
    我们没有为 Readability 设定注意力方面的目标。这没有关系！并非每个工程生产力问题都涉及全部五个方面的权衡。

*认知复杂度*  
    工程师通过 Readability 流程了解谷歌代码库和最佳编码实践，并在这一过程中接受指导。

*节奏和速度*  
    Readability 流程让工程师更快、更高效地完成工作任务。

*满意度*  
    工程师认可 Readability 流程的益处，并对参与这一流程有积极感受。

## Signals  信号

A signal is the way in which we will know we’ve achieved our goal. Not all signals are measurable, but that’s acceptable at this stage. There is not a 1:1 relationship between signals and goals. Every goal should have at least one signal, but they might have more. Some goals might also share a signal. Table 7-1 shows some example signals for the goals of the readability process measurement.

信号是判断目标是否实现的依据。并非所有信号都能度量，但在这一阶段可以接受。信号与目标并非一一对应：每个目标至少应有一个信号，也可以有多个；不同目标还可以共用一个信号。表7-1列出了度量 Readability 流程时，部分目标及其对应信号的示例。

*Table 7-1. Signals and goals*  *表7-1：信号与目标 *

| Goals                                                        | Signals                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Engineers write higher-quality code as a result of the readability process. | Engineers who have been granted readability judge their code to be of higher quality than engineers who have not been granted readability. The readability process has a positive impact on code quality. |
| Engineers learn about the Google codebase and best coding practices as a result of the readability process. | Engineers report learning from the readability process.      |
| Engineers receive mentoring during the readability process.  | Engineers report positive interactions with experienced Google engineers who serve as reviewers during the readability process. |
| Engineers receive mentoring during the readability process.<br/>Engineers complete work tasks faster and more efficiently as a result of the readability process.<br/><br/><br/>Engineers see the benefit of the readability process and have positive feelings about participating in it. | Engineers who have been granted readability judge themselves to be more productive than engineers who have not been granted readability. Changes written by engineers who have been granted readability are faster to review than changes written by engineers who have not been granted readability.<br/>Engineers view the readability process as being worthwhile. |

| 目标                                                         | 信号                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Readability 流程让工程师写出质量更高的代码。               | 取得 Readability 资格的工程师，对自身代码质量的评价高于未取得资格的工程师。Readability 流程对代码质量有积极影响。 |
| 工程师通过 Readability 流程了解谷歌代码库和最佳编码实践。       | 工程师表示自己在 Readability 流程中学到了东西。                     |
| 工程师在 Readability 流程中接受指导。                               | 工程师表示，在 Readability 流程中，他们与担任审查者的资深谷歌工程师有良好的互动。 |
| 工程师在 Readability 流程中接受指导。<br/><br/>Readability 流程让工程师更快、更高效地完成工作任务。<br/><br/>工程师认可 Readability 流程的益处，并对参与这一流程有积极感受。 | 取得 Readability 资格的工程师，对自身生产力的评价高于未取得资格的工程师。取得资格的工程师所写的变更，比未取得资格的工程师所写的变更审查得更快。<br/><br/>工程师认为 Readability 流程值得投入。 |


## Metrics  指标

Metrics are where we finally determine how we will measure the signal. Metrics are not the signal themselves; they are the measurable proxy of the signal. Because they are a proxy, they might not be a perfect measurement. For this reason, some signals might have multiple metrics as we try to triangulate on the underlying signal.

到了指标这一步，我们才最终确定如何度量信号。指标不是信号本身，而是信号的可度量代理。既然只是代理，就未必能完美反映信号。因此，有些信号可能对应多个指标，以便相互印证，更准确地把握信号所反映的情况。

For example, to measure whether engineers’ code is reviewed faster after readability, we might use a combination of both survey data and logs data. Neither of these metrics really provide the underlying truth. (Human perceptions are fallible, and logs metrics might not be measuring the entire picture of the time an engineer spends reviewing a piece of code or can be confounded by factors unknown at the time, like the size or difficulty of a code change.) However, if these metrics show different results, it signals that possibly one of them is incorrect and we need to explore further. If they are the same, we have more confidence that we have reached some kind of truth.

例如，要度量工程师取得 Readability 资格后，其代码是否审查得更快，可以结合调查数据和日志数据。这两类指标都不能直接揭示真实情况：人的感知可能出错，日志指标也未必能完整反映工程师审查代码所花的时间，还可能受到当时未知因素的干扰，例如代码变更的规模或难度。如果两类指标得出的结果不同，就说明其中一类可能有误，需要进一步调查；如果结果一致，我们就更有把握，认为结果反映了某种真实情况。

Additionally, some signals might not have any associated metric because the signal might simply be unmeasurable at this time. Consider, for example, measuring code quality. Although academic literature has proposed many proxies for code quality, none of them have truly captured it. For readability, we had a decision of either using a poor proxy and possibly making a decision based on it, or simply acknowledging that this is a point that cannot currently be measured. Ultimately, we decided not to capture this as a quantitative measure, though we did ask engineers to self-rate their code quality.

此外，有些信号可能暂时根本无法度量，因此没有对应指标。例如，学术文献虽然提出过许多代码质量的代理指标，却没有一个能真正反映代码质量。在 Readability 研究中，我们面临一个选择：使用不理想的代理指标，并可能据此作出决策；或者直接承认，这一点目前无法度量。最终，我们决定不将代码质量纳入定量度量，不过仍请工程师对自己的代码质量作了评价。

Following the GSM framework is a great way to clarify the goals for why you are measuring your software process and how it will actually be measured. However, it’s still possible that the metrics selected are not telling the complete story because they are not capturing the desired signal. At Google, we use qualitative data to validate our metrics and ensure that they are capturing the intended signal.

GSM 框架有助于明确度量软件流程的目的，以及具体如何度量。不过，选出的指标仍可能没有捕捉到想要的信号，因而无法反映全貌。在谷歌，我们用定性数据验证指标，确保它们确实反映了预期的信号。

## Using Data to Validate Metrics  使用数据验证指标

As an example, we once created a metric for measuring each engineer’s median build latency; the goal was to capture the “typical experience” of engineers’ build latencies. We then ran an *experience sampling study*. In this style of study, engineers are interrupted in context of doing a task of interest to answer a few questions. After an engineer started a build, we automatically sent them a small survey about their experiences and expectations of build latency. However, in a few cases, the engineers responded that they had not started a build! It turned out that automated tools were starting up builds, but the engineers were not blocked on these results and so it didn’t “count” toward their “typical experience.” We then adjusted the metric to exclude such builds.[^5]

例如，我们曾制定一个指标，测量每位工程师的构建延迟中位数，以反映他们对构建延迟的“典型体验”。随后，我们开展了一项*体验抽样研究*：在工程师执行研究所关注的任务时打断他们，请他们回答几个问题。工程师启动构建后，我们会自动发送一份简短问卷，询问他们对构建延迟的体验和预期。然而，少数工程师回答说，他们根本没有启动构建！原来，是自动化工具发起了构建，而工程师并不需要等待这些构建结果，因此不应将其“计入”工程师的“典型体验”。于是，我们调整指标，排除了这类构建。

Quantitative metrics are useful because they give you power and scale. You can measure the experience of engineers across the entire company over a large period of time and have confidence in the results. However, they don’t provide any context or narrative. Quantitative metrics don’t explain why an engineer chose to use an antiquated tool to accomplish their task, or why they took an unusual workflow, or why they circumvented a standard process. Only qualitative studies can provide this information, and only qualitative studies can then provide insight on the next steps to improve a process.

定量指标的价值在于，它们能有力地支持大规模度量：你可以在较长时间内度量全公司工程师的体验，并对结果有信心。但它们无法提供背景或叙事。定量指标不能解释，为什么工程师会选择过时的工具来完成任务，为什么采用不常见的工作流，或为什么绕过标准流程。只有定性研究才能提供这些信息，并据此帮助我们判断下一步该如何改进流程。

> [^5]:	It has routinely been our experience at Google that when the quantitative and qualitative metrics disagree, it was because the quantitative metrics were not capturing the expected result.
>
> 5 在谷歌，我们经常遇到这样的情况：定量指标与定性指标不一致，是因为定量指标没有捕捉到预期要反映的结果。

Consider now the signals presented in Table 7-2. What metrics might you create to measure each of those? Some of these signals might be measurable by analyzing tool and code logs. Others are measurable only by directly asking engineers. Still others might not be perfectly measurable—how do we truly measure code quality, for example?

现在看看表7-2中的信号。可以为每个信号制定什么指标？有些信号可以通过分析工具日志和代码日志来度量，有些只能直接询问工程师，还有些可能无法得到完整的度量。例如，究竟该如何真正度量代码质量？

Ultimately, when evaluating the impact of readability on productivity, we ended up with a combination of metrics from three sources. First, we had a survey that was specifically about the readability process. This survey was given to people after they completed the process; this allowed us to get their immediate feedback about the process. This hopefully avoids recall bias,[^6] but it does introduce both recency bias[^7] and sampling bias.[^8] Second, we used a large-scale quarterly survey to track items that were not specifically about readability; instead, they were purely about metrics that we expected readability should affect. Finally, we used fine-grained logs metrics from our developer tools to determine how much time the logs claimed it took engineers to complete specific tasks.[^9] Table 7-2 presents the complete list of metrics with their corresponding signals and goals.

评估 Readability 对生产力的影响时，我们最终结合了三个来源的指标。首先是专门针对 Readability 流程的调查，在工程师完成流程后进行，以获取即时反馈。这样有望避免回忆偏差，却也引入了近因偏差和抽样偏差。其次，我们通过大规模季度调查跟踪一些并不专门针对 Readability 的项目；这些项目只关注我们预期会受 Readability 影响的指标。最后，我们使用开发者工具中细粒度的日志指标，了解日志所记录的工程师完成特定任务的耗时。表7-2列出了全部指标，以及对应的信号和目标。

*Table 7-2. Goals, signals, and metrics*  *表7-2：目标、信号和指标*

| QUANTS                       | Goal                                                         | Signal                                                       | Metric                                                       |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Qu**ality of the code      | Engineers write higherquality code as a result of the readability process. | Engineers who have been granted readability judge their code to be of higher quality than engineers who have not been granted readability.<br/>The readability process has a positive impact on code quality. | Quarterly Survey: Proportion ofengineers who report being satisfied with the quality of their own code<br/><br/>Readability Survey: Proportion of engineers reporting that readability reviews have no impact or negative impact on code quality |
|                              |                                                              |                                                              | Readability Survey: Proportionof engineers reporting thatparticipating in the readability process has improved codequality for their team |
|                              | Engineers write more consistent code as a result of the readability process. | Engineers are given consistent feedback and direction in code reviews by readability reviewers as a part of the readability process. | Readability Survey: Proportion of engineers reporting inconsistency in readability reviewers’ comments and readability criteria. |
|                              | Engineers contribute to a culture of code health as a result of the readability process. | Engineers who have been granted readability regularly comment on style and/or readability issues in code reviews. | Readability Survey: Proportion of engineers reporting that they regularly comment on style and/or readability issues in code reviews |
| **A**ttention from engineers | n/a                                                          | n/a                                                          | n/a                                                          |
| I**n**tellectual             | Engineers learn about the Google codebase and best coding practices as a result of the readability process. | Engineers report learning from the readability process.      | Readability Survey: Proportion of engineers reporting that they learned about four relevant topics |
|                              |                                                              |                                                              | Readability Survey: Proportion of engineers reporting that learning or gaining expertise was a strength of the readability process |
|                              | Engineers receive mentoring during the readability process.  | Engineers report positive interactions with experienced Google engineers who serve as reviewers during the readability process. | Readability Survey: Proportion of engineers reporting that working with readability reviewers was a strength of the readability process |
| **T**empo/velocity           | Engineers are more productive as a result of the readability process. | Engineers who have been granted readability judge themselves to be more productive than engineers who have not been granted readability. | Quarterly Survey: Proportion of engineers reporting that they’re highly productive |
|                              |                                                              | Engineers report that completing the readability process positively affects their engineering velocity. | Readability Survey: Proportion of engineers reporting that not having readability reduces team engineering velocity |
|                              |                                                              | Changelists (CLs) written by engineers who have been granted readability are faster to review than CLs written by engineers who have not been granted readability. | Logs data: Median review time for CLs from authors with readability and without readability |
|                              |                                                              | CLs written by engineers who have been granted readability are easier to shepherd through code review than CLs written by engineers who have not been granted readability. | Logs data: Median shepherding time for CLs from authors with readability and without readability |
|                              |                                                              | CLs written by engineers who have been granted readability are faster to get through code review than CLs written by engineers who have not been granted readability. | Logs data: Median time to submit for CLs from authors with readability and without readability |
|                              |                                                              | The readability process does not have a negative impact on engineering velocity. | Readability Survey: Proportion of engineers reporting that the readability process negatively impacts their velocity |
|                              |                                                              |                                                              | Readability Survey: Proportion of engineers reporting that readability reviewers responded promptly |
|                              |                                                              |                                                              | Readability Survey: Proportion of engineers reporting that timeliness of reviews was a strength of the readability process |
| **S**atisfaction             | Engineers see the benefit of the readability process and have positive feelings about participating in it. | Engineers view the readability process as being an overall positive experience. | Readability Survey: Proportion of engineers reporting that their experience with the readability process was positive overall |
|                              |                                                              | Engineers view the readability process as being worthwhile   | Readability Survey: Proportion of engineers reporting that the readability process is worthwhile |
|                              |                                                              |                                                              | Readability Survey: Proportion of engineers reporting that the quality of readability reviews is a strength of the process |
|                              |                                                              |                                                              | Readability Survey: Proportion of engineers reporting that thoroughness is a strength of the process |
|                              |                                                              | Engineers do not view the readability process as frustrating. | Readability Survey: Proportion of engineers reporting that the readability process is uncertain, unclear, slow, or frustrating |
|                              |                                                              |                                                              | Quarterly Survey: Proportion of engineers reporting that they’re satisfied with their own engineering velocity |



| QUANTS         | 目标                                                         | 信号                                                         | 指标                                                         |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **代码**的质量 | Readability 流程让工程师写出质量更高的代码。               | 取得 Readability 资格的工程师，对自身代码质量的评价高于未取得资格的工程师。<br/><br/>Readability 流程对代码质量有积极影响。 | 季度调查：对自身代码质量表示满意的工程师比例<br/><br/>Readability 调查：认为 Readability 审查对代码质量没有影响或有负面影响的工程师比例 |
|                |                                                              |                                                              | Readability 调查：认为参与 Readability 流程提高了团队代码质量的工程师比例 |
|                | Readability 流程让工程师写出一致性更好的代码。           | 在 Readability 流程的代码审查中，工程师从 Readability 审查者那里获得一致的反馈和指导。 | Readability 调查：反映 Readability 审查意见和资格评定标准缺乏一致性的工程师比例。 |
|                | Readability 流程促使工程师为重视代码健康的文化作出贡献。               | 取得 Readability 资格的工程师经常在代码审查中就风格和/或可读性问题提出意见。 | Readability 调查：表示自己经常在代码审查中就风格和/或可读性问题提出意见的工程师比例 |
| 工程师的注意力   | 不适用                                                       | 不适用                                                       | 不适用                                                       |
| 认知复杂度           | 工程师通过 Readability 流程了解谷歌代码库和最佳编码实践。       | 工程师表示自己在 Readability 流程中学到了东西。                     | Readability 调查：表示自己学习了四个相关主题的工程师比例         |
|                |                                                              |                                                              | Readability 调查：认为能够学习或获得专业知识是 Readability 流程优势的工程师比例 |
|                | 工程师在 Readability 流程中接受指导。                               | 工程师表示，在 Readability 流程中，他们与担任审查者的资深谷歌工程师有良好的互动。 | Readability 调查：认为与 Readability 审查者合作是 Readability 流程优势的工程师比例 |
| 节奏/速度      | Readability 流程提高了工程师的生产力。                     | 取得 Readability 资格的工程师，对自身生产力的评价高于未取得资格的工程师。 | 季度调查：认为自己生产力很高的工程师比例                 |
|                |                                                              | 工程师表示，完成 Readability 流程能提高他们的工程工作速度。 | Readability 调查：认为没有取得 Readability 资格会降低团队工程工作速度的工程师比例   |
|                |                                                              | 取得 Readability 资格的工程师所写的变更列表（CLs），比未取得资格的工程师所写的变更列表审查得更快。 | 日志数据：已取得和未取得 Readability 资格的作者所写 CL 的审查耗时中位数   |
|                |                                                              | 相比未取得 Readability 资格的工程师所写的 CL，取得资格的工程师所写的 CL 在推进代码审查时更省力。 | 日志数据：已取得和未取得 Readability 资格的作者所写 CL，推进审查所需时间的中位数 |
|                |                                                              | 取得 Readability 资格的工程师所写的 CL，比未取得资格的工程师所写的 CL 更快完成代码审查。 | 日志数据：已取得和未取得 Readability 资格的作者所写 CL，到提交为止的耗时中位数 |
|                |                                                              | Readability 流程不会对工程工作速度产生负面影响。                       | Readability 调查：认为 Readability 流程降低了自己工作速度的工程师比例     |
|                |                                                              |                                                              | Readability 调查：表示 Readability 审查者回复及时的工程师比例             |
|                |                                                              |                                                              | Readability 调查：认为审查及时是 Readability 流程优势的工程师比例 |
| 满意度         | 工程师认可 Readability 流程的益处，并对参与这一流程有积极感受。 | 工程师认为 Readability 流程的整体体验是积极的。               | Readability 调查：认为自己参与 Readability 流程的整体体验积极的工程师比例 |
|                |                                                              | 工程师认为 Readability 流程值得投入。                                 | Readability 调查：认为 Readability 流程值得投入的工程师比例               |
|                |                                                              |                                                              | Readability 调查：认为 Readability 审查的质量是流程优势的工程师比例       |
|                |                                                              |                                                              | Readability 调查：认为审查全面细致是流程优势的工程师比例             |
|                |                                                              | 工程师不认为 Readability 流程令人沮丧。                         | Readability 调查：认为 Readability 流程充满不确定性、含糊不清、缓慢或令人沮丧的工程师比例 |
|                |                                                              |                                                              | 季度调查：对自身工程工作速度表示满意的工程师比例     |



> [^6]:	Recall bias is the bias from memory. People are more likely to recall events that are particularly interesting or frustrating.
>
> 6 回忆偏差是由记忆造成的偏差。人们更容易想起那些特别有趣或令人沮丧的事件。
>
> [^7]:	Recency bias is another form of bias from memory in which people are biased toward their most recent experience. In this case, as they just successfully completed the process, they might be feeling particularly good about it.
>
> 7 近因偏差是另一种由记忆造成的偏差，人们会更看重最近的经历。在这个案例中，工程师刚刚顺利完成流程，因此可能对它感觉格外良好。
>
> [^8]:	Because we asked only those people who completed the process, we aren’t capturing the opinions of those who did not complete the process.
>
> 8 由于我们只询问了完成流程的人，因此没有收集到未完成流程者的意见。
>
> [^9]:	There is a temptation to use such metrics to evaluate individual engineers, or perhaps even to identify high and low performers. Doing so would be counterproductive, though. If productivity metrics are used for performance reviews, engineers will be quick to game the metrics, and they will no longer be useful for measuring and improving productivity across the organization. The only way to make these measurements work is to let go of the idea of measuring individuals and embrace measuring the aggregate effect.
>
> 9 人们很容易想用这些指标评价单个工程师，甚至区分高绩效和低绩效人员，但这样做会适得其反。如果把生产力指标用于绩效评估，工程师很快就会学会操弄指标，使其不再能用于度量和提高整个组织的生产力。要让这些度量发挥作用，唯一的办法是放弃度量个人的想法，转而度量总体效果。

## Taking Action and Tracking Results  采取行动并跟踪结果

Recall our original goal in this chapter: we want to take action and improve productivity. After performing research on a topic, the team at Google always prepares a list of recommendations for how we can continue to improve. We might suggest new features to a tool, improving latency of a tool, improving documentation, removing obsolete processes, or even changing the incentive structures for the engineers. Ideally, these recommendations are “tool driven”: it does no good to tell engineers to change their process or way of thinking if the tools do not support them in doing so. We instead always assume that engineers will make the appropriate trade-offs if they have the proper data available and the suitable tools at their disposal.

回顾本章最初的目标：采取行动，提高生产力。研究完某个问题后，谷歌的研究团队总会列出进一步改进的建议，例如为工具增加功能、降低工具延迟、改进文档、取消过时流程，甚至改变工程师的激励结构。理想情况下，这些建议应由工具来推动落实：如果工具不提供支持，光要求工程师改变流程或思维方式并没有用。我们的出发点始终是，只要工程师掌握了恰当的数据，并有合适的工具可用，就会作出合理的权衡。

For readability, our study showed that it was overall worthwhile: engineers who had achieved readability were satisfied with the process and felt they learned from it. Our logs showed that they also had their code reviewed faster and submitted it faster, even accounting for no longer needing as many reviewers. Our study also showed places for improvement with the process: engineers identified pain points that would have made the process faster or more pleasant. The language teams took these recommendations and improved the tooling and process to make it faster and to be more transparent so that engineers would have a more pleasant experience.

对于 Readability，研究表明这套流程总体上值得投入：取得资格的工程师对流程满意，并认为自己从中有所收获。日志显示，他们的代码审查和提交也更快；即使考虑到取得资格后所需审查者减少这一因素，结论仍然成立。研究也找出了可改进之处：工程师指出了一些痛点，解决后能让流程更快、体验更好。语言团队采纳了这些建议，改进工具和流程，提高速度和透明度，让工程师获得更好的体验。

## Conclusion  总结

At Google, we’ve found that staffing a team of engineering productivity specialists has widespread benefits to software engineering; rather than relying on each team to chart its own course to increase productivity, a centralized team can focus on broad- based solutions to complex problems. Such “human-based” factors are notoriously difficult to measure, and it is important for experts to understand the data being analyzed given that many of the trade-offs involved in changing engineering processes are difficult to measure accurately and often have unintended consequences. Such a team must remain data driven and aim to eliminate subjective bias.

谷歌的经验表明，设立工程生产力专家团队，能为软件工程带来广泛收益。与其让各团队自行摸索提高生产力的方法，不如由专门团队集中研究复杂问题，寻找能广泛适用的解决方案。与人有关的因素一向难以度量，而改变工程流程涉及的许多权衡，也难以准确衡量，还常常带来意想不到的后果。因此，专家必须理解所分析的数据。这样的团队必须坚持以数据为依据，努力消除主观偏见。

## TL;DRs  内容提要

- Before measuring productivity, ask whether the result is actionable, regardless of whether the result is positive or negative. If you can’t do anything with the result, it is likely not worth measuring.
- Select meaningful metrics using the GSM framework. A good metric is a reasonable proxy to the signal you’re trying to measure, and it is traceable back to your original goals.
- Select metrics that cover all parts of productivity (QUANTS). By doing this, you ensure that you aren’t improving one aspect of productivity (like developer velocity) at the cost of another (like code quality).
- Qualitative metrics are metrics, too! Consider having a survey mechanism for tracking longitudinal metrics about engineers’ beliefs. Qualitative metrics should also align with the quantitative metrics; if they do not, it is likely the quantitative metrics that are incorrect.
- Aim to create recommendations that are built into the developer workflow and incentive structures. Even though it is sometimes necessary to recommend additional training or documentation, change is more likely to occur if it is built into the developer’s daily habits.

- 度量生产力之前，先问清楚：无论结果正面还是负面，能否据此采取行动？如果不能，很可能就不值得度量。
- 使用 GSM 框架选择有意义的指标。好的指标应能合理代表所要度量的信号，并可追溯到最初的目标。
- 选择覆盖生产力各个方面（QUANTS）的指标，确保不会为了改善一个方面，例如开发者的工作速度，而牺牲另一个方面，例如代码质量。
- 定性指标也是指标！可以考虑建立调查机制，长期跟踪工程师看法的变化。定性指标应与定量指标相互印证；如果不一致，很可能是定量指标有误。
- 尽量让改进建议融入开发者的工作流和激励结构。虽然有时确实需要增加培训或文档，但把改进融入开发者的日常习惯，更容易促成改变。
