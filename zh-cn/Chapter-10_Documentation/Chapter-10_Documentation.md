
**CHAPTER 10**

# Documentation

# 第十章 文档

**Written by Tom Manshreck**

**Edited by Riona MacNamara**

Of the complaints most engineers have about writing, using, and maintaining code, a singular common frustration is the lack of quality documentation. “What are the side effects of this method?” “I got an error after step 3.” “What does this acronym mean?” “Is this document up to date?” Every software engineer has voiced complaints about the quality, quantity, or sheer lack of documentation throughout their career, and the software engineers at Google are no different.

工程师在编写、使用和维护代码时，常有一个共同的困扰：缺少高质量的文档。“这个方法有什么副作用？”“我做到第3步之后出错了。”“这个缩写是什么意思？”“这份文档是最新的吗？”每位软件工程师在职业生涯中都抱怨过文档质量差、数量不足，甚至完全没有文档，谷歌的软件工程师也不例外。

Technical writers and project managers may help, but software engineers will always need to write most documentation themselves. Engineers, therefore, need the proper tools and incentives to do so effectively. The key to making it easier for them to write quality documentation is to introduce processes and tools that scale with the organization and that tie into their existing workflow.

技术撰稿人和项目经理可以提供帮助，但大部分文档始终需要软件工程师自己编写。因此，工程师需要合适的工具和激励，才能高效地完成这项工作。要让他们更容易写出高质量的文档，关键在于引入能够随组织规模扩展、融入现有工作流的流程和工具。

Overall, the state of engineering documentation in the late 2010s is similar to the state of software testing in the late 1980s. Everyone recognizes that more effort needs to be made to improve it, but there is not yet organizational recognition of its critical benefits. That is changing, if slowly. At Google, our most successful efforts have been when documentation is treated like code and incorporated into the traditional engineering workflow, making it easier for engineers to write and maintain simple documents.

总体而言，2010年代末的工程文档状况，与1980年代末的软件测试状况相似。人人都认识到需要投入更多精力来改进文档，但组织层面尚未充分认识到它的重要价值。这种情况正在改变，只是进展缓慢。在谷歌，最成功的做法是像对待代码一样对待文档，将其纳入常规工程工作流，让工程师更容易编写和维护简单的文档。

## What Qualifies as Documentation? 什么算是文档？

When we refer to “documentation,” we’re talking about every supplemental text that an engineer needs to write to do their job: not only standalone documents, but code comments as well. (In fact, most of the documentation an engineer at Google writes comes in the form of code comments.) We’ll discuss the various types of engineering documents further in this chapter.

这里所说的“文档”，是指工程师为完成工作而需要编写的所有辅助文字：不仅包括独立文档，也包括代码注释。（事实上，谷歌工程师编写的大部分文档都是代码注释。）本章后面会进一步讨论各类工程文档。

## Why Is Documentation Needed? 为什么需要文档？

Quality documentation has tremendous benefits for an engineering organization. Code and APIs become more comprehensible, reducing mistakes. Project teams are more focused when their design goals and team objectives are clearly stated. Manual processes are easier to follow when the steps are clearly outlined. Onboarding new members to a team or code base takes much less effort if the process is clearly documented.

高质量的文档能为工程组织带来巨大收益。代码和 API 更容易理解，错误就会减少。设计目标和团队目标写得清楚，项目团队就更能集中精力。手动操作的步骤列得明确，执行起来就更容易。入门流程有清楚的文档说明，让新成员融入团队或熟悉代码库所需的精力也会大幅减少。

But because documentation’s benefits are all necessarily downstream, they generally don’t reap immediate benefits to the author. Unlike testing, which (as we’ll see) quickly provides benefits to a programmer, documentation generally requires more effort up front and doesn’t provide clear benefits to an author until later. But, like investments in testing, the investment made in documentation will pay for itself over time. After all, you might write a document only once,[^1] but it will be read hundreds, perhaps thousands of times afterward; its initial cost is amortized across all the future readers. Not only does documentation scale over time, but it is critical for the rest of the organization to scale as well. It helps answer questions like these:

- Why were these design decisions made?
- Why did we implement this code in this manner?
- Why did I implement this code in this manner, if you’re looking at your own code two years later?

不过，文档的收益都体现在后续使用中，通常不会立即惠及作者。正如后文将讨论的，测试能很快为程序员带来收益；文档则通常需要先投入更多精力，之后作者才能明显受益。但与测试一样，对文档的投入也会随着时间推移获得回报。毕竟，一份文档可能只需编写一次，之后却会被阅读数百次，甚至数千次；最初的成本由未来的所有读者分摊。文档不仅能在长期使用中不断发挥价值，对组织其他部分的规模扩展也至关重要。它有助于回答以下问题：

- 为什么作出这些设计决策？
- 为什么我们要以这种方式实现这段代码？
- 如果两年后再看自己的代码：我当时为什么这样实现？

If documentation conveys all these benefits, why is it generally considered “poor” by engineers? One reason, as we’ve mentioned, is that the benefits aren’t immediate, especially to the writer. But there are several other reasons:

- Engineers often view writing as a separate skill than that of programming. (We’ll try to illustrate that this isn’t quite the case, and even where it is, it isn’t necessarily a separate skill from that of software engineering.)
- Some engineers don’t feel like they are capable writers. But you don’t need a robust command of English[^2] to produce workable documentation. You just need to step outside yourself a bit and see things from the audience’s perspective.
- Writing documentation is often more difficult because of limited tools support or integration into the developer workflow.
- Documentation is viewed as an extra burden—something else to maintain— rather than something that will make maintenance of their existing code easier.

既然文档有这么多好处，为什么工程师普遍认为文档“很差”？前面提到过，原因之一是收益不会立即显现，尤其对作者而言。此外，还有几个原因：

- 工程师往往把写作看作与编程不同的技能。（我们会尝试说明，两者并非截然不同；即使写作与编程不同，也未必是软件工程之外的技能。）
- 有些工程师觉得自己不擅长写作。但写出实用的文档并不需要精通英语，只需稍稍跳出自己的视角，站在读者的角度看问题。
- 工具支持有限，或文档工作未能充分融入开发者工作流，往往会增加编写文档的难度。
- 人们把文档视为额外负担，又多了一样需要维护的东西，而没有看到它能让现有代码更容易维护。

> [^1]: OK, you will need to maintain it and revise it occasionally.
>
> 1   当然，你还是需要维护文档，偶尔作些修订。
>
> [^2]: English is still the primary language for most programmers, and most technical documentation for programmers relies on an understanding of English.
>
> 2   英语仍然是大多数程序员使用的主要语言，阅读面向程序员的技术文档，大多也需要理解英语。

Not every engineering team needs a technical writer (and even if that were the case, there aren’t enough of them). This means that engineers will, by and large, write most of the documentation themselves. So, instead of forcing engineers to become technical writers, we should instead think about how to make writing documentation easier for engineers. Deciding how much effort to devote to documentation is a decision your organization will need to make at some point.

并非每个工程团队都需要技术撰稿人；即使都需要，也没有足够的人手。这意味着，大部分文档基本上还是要由工程师自己编写。因此，与其要求工程师成为技术撰稿人，不如考虑怎样让他们更容易编写文档。组织迟早需要决定，要在文档上投入多少精力。

Documentation benefits several different groups. Even to the writer, documentation provides the following benefits:

- It helps formulate an API. Writing documentation is one of the surest ways to figure out if your API makes sense. Often, the writing of the documentation itself leads engineers to reevaluate design decisions that otherwise wouldn’t be questioned. If you can’t explain it and can’t define it, you probably haven’t designed it well enough.
- It provides a road map for maintenance and a historical record. Tricks in code should be avoided, in any case, but good comments help out a great deal when you’re staring at code you wrote two years ago, trying to figure out what’s wrong.
- It makes your code look more professional and drive traffic. Developers will naturally assume that a well-documented API is a better-designed API. That’s not always the case, but they are often highly correlated. Although this benefit sounds cosmetic, it’s not quite so: whether a product has good documentation is usually a pretty good indicator of how well a product will be maintained.
- It will prompt fewer questions from other users. This is probably the biggest benefit over time to someone writing the documentation. If you have to explain something to someone more than once, it usually makes sense to document that process.

文档能让多个群体受益。即使对作者本人，也有以下好处：

- 帮助设计 API。编写文档是判断 API 是否合理的最可靠方法之一。写文档的过程，往往会促使工程师重新审视原本不会被质疑的设计决策。如果你无法解释它，也无法清楚地定义它，设计很可能还不够完善。
- 为维护工作提供指引，并留下历史记录。代码本就应避免取巧；不过，当你盯着两年前自己写的代码查找问题时，好的注释仍会大有帮助。
- 让代码显得更专业，吸引更多开发者使用。开发者自然会认为，文档完善的 API 设计也更好。事实未必总是如此，但两者往往高度相关。这听起来只是表面功夫，其实不然：产品是否有良好的文档，通常很能反映它今后会得到怎样的维护。
- 减少其他用户的提问。从长期看，这可能是文档作者最大的收益。如果一件事需要向别人解释不止一次，通常就值得把这个过程记录下来。

As great as these benefits are to the writer of documentation, the lion’s share of documentation’s benefits will naturally accrue to the reader. Google’s C++ Style Guide notes the maxim “optimize for the reader.” This maxim applies not just to code, but to the comments around code, or the documentation set attached to an API. Much like testing, the effort you put into writing good documents will reap benefits many times over its lifetime. Documentation is critical over time, and reaps tremendous benefits for especially critical code as an organization scales.

文档给作者带来的这些收益固然可观，但最大的受益者自然还是读者。谷歌的《C++ 风格指南》提出一条准则：“为读者优化。”它不仅适用于代码，也适用于代码中的注释和 API 的配套文档。与测试一样，编写好文档的投入会在文档的整个生命周期中带来数倍回报。文档对长期维护至关重要；组织规模越大，关键代码的文档就越能带来巨大收益。

## Documentation Is Like Code 把文档当作代码

Software engineers who write in a single, primary programming language still often reach for different languages to solve specific problems. An engineer might write shell scripts or Python to run command-line tasks, or they might write most of their backend code in C++ but write some middleware code in Java, and so on. Each language is a tool in the toolbox.

即使主要使用一种编程语言，软件工程师也常会借助其他语言来解决特定问题。例如，用 shell 脚本或 Python 执行命令行任务，或者用 C++ 编写大部分后端代码，同时用 Java 编写一些中间件代码。每种语言都是工具箱中的一种工具。

Documentation should be no different: it’s a tool, written in a different language (usually English) to accomplish a particular task. Writing documentation is not much different than writing code. Like a programming language, it has rules, a particular syntax, and style decisions, often to accomplish a similar purpose as that within code: enforce consistency, improve clarity, and avoid (comprehension) errors. Within technical documentation, grammar is important not because one needs rules, but to standardize the voice and avoid confusing or distracting the reader. Google requires a certain comment style for many of its languages for this reason.

文档也应如此：它是一种工具，用另一种语言（通常是英语）完成特定任务。写文档与写代码并没有太大区别。和编程语言一样，文档也有规则、特定语法和风格选择，目的往往与代码规范相近：保持一致、表达清楚、避免理解错误。技术文档重视语法，不是为了设立规则，而是为了统一行文语气，避免让读者困惑或分心。正因如此，谷歌对许多编程语言都规定了相应的注释风格。

Like code, documents should also have owners. Documents without owners become stale and difficult to maintain. Clear ownership also makes it easier to handle documentation through existing developer workflows: bug tracking systems, code review tooling, and so forth. Of course, documents with different owners can still conflict with one another. In those cases, it is important to designate canonical documentation: determine the primary source and consolidate other associated documents into that primary source (or deprecate the duplicates).

与代码一样，文档也应该有负责人。无人负责的文档会逐渐过时，也难以维护。明确归属后，就更容易通过现有的开发者工作流管理文档，例如使用缺陷跟踪系统和代码审查工具。当然，由不同人负责的文档仍可能相互矛盾。这时，重要的是指定权威文档：确定主要来源，再把其他相关文档合并进去，或者弃用重复文档。

The prevalent usage of “go/links” at Google (see Chapter 3) makes this process easier. Documents with straightforward go/ links often become the canonical source of truth. One other way to promote canonical documents is to associate them directly with the code they document by placing them directly under source control and alongside the source code itself.

谷歌广泛使用的“go/links”（见第3章）让这一过程更容易。拥有简明 go/links 的文档往往会成为权威来源。确立权威文档的另一种方法，是将文档与它所说明的代码直接关联：把文档纳入源代码版本控制，与源代码放在一起。

Documentation is often so tightly coupled to code that it should, as much as possible, be treated as code. That is, your documentation should:

- Have internal policies or rules to be followed
- Be placed under source control
- Have clear ownership responsible for maintaining the docs
- Undergo reviews for changes (and change with the code it documents)
- Have issues tracked, as bugs are tracked in code
- Be periodically evaluated (tested, in some respect)
- If possible, be measured for aspects such as accuracy, freshness, etc. (tools have still not caught up here)

文档通常与代码紧密耦合，因此应尽可能像代码一样管理。也就是说，文档应当：

- 遵循内部策略或规则
- 纳入源代码版本控制
- 有明确的负责人承担维护工作
- 变更经过审查，并随所说明的代码同步更新
- 像跟踪代码缺陷一样跟踪文档问题
- 定期接受评估，从某种意义上说就是测试
- 尽可能衡量准确性、时效性等方面的表现，目前工具在这方面还没有跟上

The more engineers treat documentation as “one of” the necessary tasks of software development, the less they will resent the upfront costs of writing, and the more they will reap the long-term benefits. In addition, making the task of documentation easier reduces those upfront costs.

工程师越是把文档视为软件开发的必要任务之一，就越能接受写作的前期投入，也越能享受到长期收益。此外，让文档工作更容易完成，本身也能降低这些前期成本。

------

 **Case Study: The Google Wiki** **案例研究：谷歌维基**

When Google was much smaller and leaner, it had few technical writers. The easiest way to share information was through our own internal wiki (GooWiki). At first, this seemed like a reasonable approach; all engineers shared a single documentation set and could update it as needed.

谷歌规模尚小、人员精简时，技术撰稿人很少。共享信息最简单的方式，是使用内部维基 GooWiki。起初，这种做法似乎很合理：所有工程师共用一套文档，并可按需更新。

But as Google scaled, problems with a wiki-style approach became apparent. Because there were no true owners for documents, many became obsolete.[^3] Because no process was put in place for adding new documents, duplicate documents and document sets began appearing. GooWiki had a flat namespace, and people were not good at applying any hierarchy to the documentation sets. At one point, there were 7 to 10 documents (depending on how you counted them) on setting up Borg, our production compute environment, only a few of which seemed to be maintained, and most were specific to certain teams with certain permissions and assumptions.

但随着谷歌规模扩大，维基式文档管理的问题逐渐显现。文档没有真正的负责人，许多内容因此过时。新增文档也没有相应流程，于是出现了重复的文档和文档集。GooWiki 使用扁平的命名空间，大家又不善于为文档集建立层次结构。曾有一段时间，仅介绍如何配置生产计算环境 Borg 的文档就有7到10份，具体数量取决于统计方式。其中似乎只有少数仍在维护，大多只适用于特定团队，并以特定权限和假设为前提。

Another problem with GooWiki became apparent over time: the people who could fix the documents were not the people who used them. New users discovering bad documents either couldn’t confirm that the documents were wrong or didn’t have an easy way to report errors. They knew something was wrong (because the document didn’t work), but they couldn’t “fix” it. Conversely, the people best able to fix the documents often didn’t need to consult them after they were written. The documentation became so poor as Google grew that the quality of documentation became Google’s number one developer complaint on our annual developer surveys.

随着时间推移，GooWiki 的另一个问题也显现出来：能修正文档的人，往往不是使用文档的人。新用户发现文档有问题后，要么无法确认究竟是不是文档错了，要么没有便捷的报错途径。他们知道有问题，因为照着文档做并不奏效，却无法“修复”文档。反过来，最有能力修正文档的人，往往在写完之后就不再需要查阅它。随着谷歌发展，文档质量不断恶化，最终成了年度开发者调查中，谷歌开发者抱怨最多的问题。

The way to improve the situation was to move important documentation under the same sort of source control that was being used to track code changes. Documents began to have their own owners, canonical locations within the source tree, and processes for identifying bugs and fixing them; the documentation began to dramatically improve. Additionally, the way documentation was written and maintained began to look the same as how code was written and maintained. Errors in the documents could be reported within our bug tracking software. Changes to the documents could be handled using the existing code review process. Eventually, engineers began to fix the documents themselves or send changes to technical writers (who were often the owners).

改善这一状况的办法，是把重要文档纳入与代码变更相同的源代码版本控制机制。文档开始有了自己的负责人、在源码树中的权威存放位置，以及发现和修复问题的流程，质量随之显著改善。文档的编写和维护方式，也开始与代码趋于一致。文档错误可以通过缺陷跟踪软件报告，文档修改可以沿用代码审查流程。最终，工程师开始自己修正文档，或把变更发给技术撰稿人，而后者往往正是文档的负责人。

Moving documentation to source control was initially met with a lot of controversy.
Many engineers were convinced that doing away with the GooWiki, that bastion of freedom of information, would lead to poor quality because the bar for documentation (requiring a review, requiring owners for documents, etc.) would be higher. But that wasn’t the case. The documents became better.

把文档纳入源代码版本控制，最初引发了不少争议。
许多工程师坚信，弃用 GooWiki 这座信息自由的堡垒会让文档质量下降，因为编写文档的门槛提高了：需要审查，需要指定负责人，等等。但事实并非如此，文档质量反而提高了。

The introduction of Markdown as a common documentation formatting language also helped because it made it easier for engineers to understand how to edit documents without needing specialized expertise in HTML or CSS. Google eventually introduced its own framework for embedding documentation within code: g3doc.With that framework, documentation improved further, as documents existed side by side with the source code within the engineer’s development environment. Now, engineers could update the code and its associated documentation in the same change (a practice for which we’re still trying to improve adoption).

引入 Markdown 作为通用的文档格式语言也起了作用：工程师无须掌握 HTML 或 CSS 的专门知识，就能轻松上手编辑文档。谷歌后来又引入了自有框架 g3doc，用于在代码中嵌入文档。文档与源代码并排出现在工程师的开发环境中，质量因此进一步提升。工程师现在可以在同一次变更中更新代码及相关文档；我们仍在努力推广这一做法。

The key difference was that maintaining documentation became a similar experience to maintaining code: engineers filed bugs, made changes to documents in changelists, sent changes to reviews by experts, and so on. Leveraging of existing developer  workflows, rather than creating new ones, was a key benefit.

关键变化在于，维护文档的体验与维护代码相似了：工程师提交缺陷报告，在变更列表中修改文档，将变更交给专家审查，等等。能够沿用现有开发者工作流，无须另建一套，是这一做法的重要优势。

------

> [^3]: When we deprecated GooWiki, we found that around 90% of the documents had no views or updates in the previous few months.
>
> 3   弃用 GooWiki 时，我们发现约90%的文档在此前几个月里既无人查看，也无人更新。

## Know Your Audience 了解你的受众

One of the most important mistakes that engineers make when writing documentation is to write only for themselves. It’s natural to do so, and writing for yourself is not without value: after all, you might need to look at this code in a few years and try to figure out what you once meant. You also might be of approximately the same skill set as someone reading your document. But if you write only for yourself, you are going to make certain assumptions, and given that your document might be read by a very wide audience (all of engineering, external developers), even a few lost readers is a large cost. As an organization grows, mistakes in documentation become more prominent, and your assumptions often do not apply.

工程师写文档时，一个主要错误是只为自己写。这样做很自然，也并非没有价值：毕竟，几年后你可能需要重新查看这段代码，弄清自己当时的意思。你的技能水平也可能与读者大致相同。但只为自己写，就容易默认某些前提。而文档可能面向很广的读者群，包括全体工程师和外部开发者，即使让少数读者看不懂，也会造成不小的代价。随着组织扩大，文档错误的影响会更突出，你默认的前提往往也不再适用。

Instead, before you begin writing, you should (formally or informally) identify the audience(s) your documents need to satisfy. A design document might need to persuade decision makers. A tutorial might need to provide very explicit instructions to someone utterly unfamiliar with your codebase. An API might need to provide complete and accurate reference information for any users of that API, be they experts or novices. Always try to identify a primary audience and write to that audience.

因此，动笔之前，应当先明确文档需要服务哪些受众，形式可以正式，也可以非正式。设计文档可能需要说服决策者；教程可能需要为完全不熟悉代码库的人提供十分明确的操作说明；API 文档则可能需要为所有用户，无论专家还是新手，提供完整、准确的参考信息。始终要尽量确定主要受众，并面向他们写作。

Good documentation need not be polished or “perfect.” One mistake engineers make when writing documentation is assuming they need to be much better writers. By that measure, few software engineers would write. Think about writing like you do about testing or any other process you need to do as an engineer. Write to your audience, in the voice and style that they expect. If you can read, you can write. Remember that  your audience is standing where you once stood, but without your new domain knowledge. So you don’t need to be a great writer; you just need to get someone like you as familiar with the domain as you now are. (And as long as you get a stake in the ground, you can improve this document over time.)

好的文档不必文笔精美，也不必“完美”。工程师写文档时，容易误以为自己必须先具备很高的写作水平；照这个标准，很少有人会动笔。应当像对待测试或其他工程职责一样对待写作，用受众期待的语气和风格表达。能读，就能写。记住，读者正处在你曾经的位置，只是还没有掌握你如今拥有的领域知识。你无须成为出色的作家，只需帮助一个和过去的你相似的人，达到你现在对这个领域的熟悉程度。（而且，只要先写出初稿，就可以在以后不断完善。）

### Types of Audiences 受众类型

We’ve pointed out that you should write at the skill level and domain knowledge appropriate for your audience. But who precisely is your audience? Chances are, you have multiple audiences based on one or more of the following criteria:

- Experience level (expert programmers, or junior engineers who might not even be familiar—gulp!—with the language).
- Domain knowledge (team members, or other engineers in your organization who are familiar only with API endpoints).
- Purpose (end users who might need your API to do a specific task and need to find that information quickly, or software gurus who are responsible for the guts of a particularly hairy implementation that you hope no one else needs to maintain).

前面提到，写作应适合受众的技能水平和领域知识。但受众究竟是谁？按以下一个或多个维度划分，你面对的很可能不止一类读者：

- 经验水平：可能是编程专家，也可能是初级工程师，甚至连所用的语言都不熟悉。
- 领域知识：可能是团队成员，也可能是组织中只熟悉 API 端点的其他工程师。
- 目的：可能是需要用 API 完成特定任务、希望快速找到相关信息的最终用户；也可能是负责某个极其复杂实现的内部细节的软件专家，而你但愿再没有别人需要维护那部分代码。

In some cases, different audiences require different writing styles, but in most cases, the trick is to write in a way that applies as broadly to your different audience groups as possible. Often, you will need to explain a complex topic to both an expert and a novice. Writing for the expert with domain knowledge may allow you to cut corners, but you’ll confuse the novice; conversely, explaining everything in detail to the novice will doubtless annoy the expert.

有些情况下，不同受众需要不同的写作风格；但大多数时候，关键是尽可能让同一种写法适合不同读者群。你往往需要同时向专家和新手解释一个复杂主题。面向熟悉领域的专家写作，可以省去一些说明，却会让新手困惑；反过来，为新手详尽解释一切，又难免让专家厌烦。

Obviously, writing such documents is a balancing act and there’s no silver bullet, but one thing we’ve found is that it helps to keep your documents short. Write descriptively enough to explain complex topics to people unfamiliar with the topic, but don’t lose or annoy experts. Writing a short document often requires you to write a longer one (getting all the information down) and then doing an edit pass, removing duplicate information where you can. This might sound tedious, but keep in mind that this expense is spread across all the readers of the documentation. As Blaise Pascal once said, “If I had more time, I would have written you a shorter letter.” By keeping a document short and clear, you will ensure that it will satisfy both an expert and a novice.

显然，写这样的文档需要权衡，没有万能办法。不过，我们发现，保持简短会有所帮助。描述要足以让不熟悉主题的人理解复杂内容，又不能让专家失去兴趣或感到厌烦。要写出简短的文档，往往得先写一份长稿，把信息记录完整，再通篇编辑，尽可能删去重复内容。这听起来也许繁琐，但这份投入会由文档的所有读者分摊。正如布莱斯·帕斯卡（Blaise Pascal）所说：“如果有更多时间，我会给你写一封更短的信。”文档简短而清楚，才能同时满足专家和新手的需要。

Another important audience distinction is based on how a user encounters a document:

- Seekers are engineers who know what they want and want to know if what they are looking at fits the bill. A key pedagogical device for this audience is consistency. If you are writing reference documentation for this group—within a code file, for example—you will want to have your comments follow a similar format so that readers can quickly scan a reference and see whether they find what they are looking for.
- Stumblers might not know exactly what they want. They might have only a vague idea of how to implement what they are working with. The key for this audience is clarity. Provide overviews or introductions (at the top of a file, for example) that explain the purpose of the code they are looking at. It’s also useful to identify when a doc is not appropriate for an audience. A lot of documents at Google begin with a “TL;DR statement” such as “TL;DR: if you are not interested in C++ compilers at Google, you can stop reading now.”

还可以根据用户如何接触到文档，区分两类重要受众：

- 查找者知道自己需要什么，想确认眼前的内容是否符合需求。帮助这类读者理解内容，关键在于一致性。例如，在代码文件中为他们编写参考文档时，注释应采用相近的格式，让读者能快速浏览，判断是否找到了所需信息。
- 浏览者未必清楚自己需要什么，对如何实现手头的任务可能只有模糊的想法。面向这类读者，关键是表达清楚。可以在文件开头等位置提供概述或介绍，说明当前代码的用途。明确说明文档不适合哪些读者，也很有帮助。谷歌的许多文档开头都有一段“TL;DR 声明”，例如：“TL;DR：如果你对谷歌的 C++ 编译器不感兴趣，就不必继续读了。”

Finally, one important audience distinction is between that of a customer (e.g., a user of an API) and that of a provider (e.g., a member of the project team). As much as possible, documents intended for one should be kept apart from documents intended for the other. Implementation details are important to a team member for maintenance purposes; end users should not need to read such information. Often, engineers denote design decisions within the reference API of a library they publish. Such reasonings belong more appropriately in specific documents (design documents) or, at best, within the implementation details of code hidden behind an interface.

最后，还要区分使用方与提供方：前者例如 API 用户，后者例如项目团队成员。面向这两类受众的文档，应尽可能分开。团队成员维护代码时需要了解实现细节，最终用户则不应被迫阅读这些信息。工程师常会把设计决策写进所发布库的 API 参考文档，但这些决策理由更适合放在专门的设计文档中；即使放在代码里，也应放在接口背后的实现部分。

## Documentation Types 文档类型

Engineers write various different types of documentation as part of their work: design documents, code comments, how-to documents, project pages, and more. These all count as “documentation.” But it is important to know the different types, and to not mix types. A document should have, in general, a singular purpose, and stick to it. Just as an API should do one thing and do it well, avoid trying to do several things within one document. Instead, break out those pieces more logically.

工程师的工作包括编写各类文档：设计文档、代码注释、操作指南、项目页面，等等。这些都属于“文档”，但应当区分类型，不要混杂在一起。一般来说，一份文档应只服务一个目的，并始终围绕它展开。正如一个 API 应当做好一件事一样，不要试图用一份文档完成多项任务，而应按逻辑把这些内容拆开。

There are several main types of documents that software engineers often need to write:

- Reference documentation, including code comments
- Design documents
- Tutorials
- Conceptual documentation
- Landing pages

软件工程师经常需要编写以下几类文档：

- 参考文档，包括代码注释
- 设计文档
- 教程
- 概念文档
- 入口页

It was common in the early days of Google for teams to have monolithic wiki pages with bunches of links (many broken or obsolete), some conceptual information about how the system worked, an API reference, and so on, all sprinkled together. Such documents fail because they don’t serve a single purpose (and they also get so long that no one will read them; some notorious wiki pages scrolled through several dozens of screens). Instead, make sure your document has a singular purpose, and if adding something to that page doesn’t make sense, you probably want to find, or even create, another document for that purpose.

谷歌早期，团队常把所有内容塞进一张庞大的维基页面：大量链接，其中许多已失效或过时；一些系统工作原理的概念说明；API 参考资料，等等。这些内容杂陈在一起，文档因没有明确的单一用途而失去作用。页面还会长到无人愿意阅读，有些出了名的维基页面甚至要滚动几十屏。应当确保每份文档只服务一个目的；如果某项内容不适合加入当前页面，就应寻找甚至新建一份适合承载它的文档。

### Reference Documentation 参考文档

Reference documentation is the most common type that engineers need to write; indeed, they often need to write some form of reference documents every day. By reference documentation, we mean anything that documents the usage of code within the codebase. Code comments are the most common form of reference documentation that an engineer must maintain. Such comments can be divided into two basic camps: API comments versus implementation comments. Remember the audience differences between these two: API comments don’t need to discuss implementation details or design decisions and can’t assume a user is as versed in the API as the author. Implementation comments, on the other hand, can assume a lot more domain knowledge of the reader, though be careful in assuming too much: people leave projects, and sometimes it’s safer to be methodical about exactly why you wrote this code the way you did.

参考文档是工程师最常编写的文档类型，事实上，他们往往每天都需要编写某种形式的参考文档。这里指的是说明代码库中代码用法的各类资料。代码注释是工程师最常需要维护的参考文档，主要分为 API 注释和实现注释。要记住，两者面向不同受众：API 注释不必讨论实现细节或设计决策，也不能假定用户和作者一样熟悉 API；实现注释则可以假定读者拥有更多领域知识，但也不能假定过多。毕竟，人员会离开项目，有时还是把为什么这样写代码解释清楚更稳妥。

Most reference documentation, even when provided as separate documentation from the code, is generated from comments within the codebase itself. (As it should; reference documentation should be single-sourced as much as possible.) Some languages such as Java or Python have specific commenting frameworks (Javadoc, PyDoc, GoDoc) meant to make generation of this reference documentation easier. Other languages, such as C++, have no standard “reference documentation” implementation, but because C++ separates out its API surface (in header or .h files) from the implementation (.cc files), header files are often a natural place to document a C++ API.

大多数参考文档即使单独提供，也由代码库中的注释生成。本就应当如此：参考文档应尽可能从单一来源生成。Java、Python 等语言有专门的注释框架，例如 Javadoc、PyDoc、GoDoc，用来简化参考文档的生成。C++ 等语言没有标准的“参考文档”实现机制，但 C++ 把对外提供的 API 放在头文件，也就是 .h 文件中，与 .cc 文件中的实现分开，因此头文件自然适合承载 C++ API 的文档。

Google takes this approach: a C++ API deserves to have its reference documentation live within the header file. Other reference documentation is embedded directly in the Java, Python, and Go source code as well. Because Google’s Code Search browser (see Chapter 17) is so robust, we’ve found little benefit to providing separate generated reference documentation. Users in Code Search not only search code easily, they can usually find the original definition of that code as the top result. Having the documentation alongside the code’s definitions also makes the documentation easier to discover and maintain.

谷歌采用的就是这种方式：C++ API 的参考文档应放在头文件中。其他语言的参考文档也直接嵌入 Java、Python 和 Go 源代码。谷歌的 Code Search 代码浏览工具非常强大（见第17章），因此我们发现，另外生成一套参考文档的收益不大。用户不仅能轻松搜索代码，通常还能在搜索结果的首位找到它的原始定义。文档与代码定义放在一起，也更容易查找和维护。

We all know that code comments are essential to a well-documented API. But what precisely is a “good” comment? Earlier in this chapter, we identified two major audiences for reference documentation: seekers and stumblers. Seekers know what they want; stumblers don’t. The key win for seekers is a consistently commented codebase so that they can quickly scan an API and find what they are looking for. The key win for stumblers is clearly identifying the purpose of an API, often at the top of a file header. We’ll walk through some code comments in the subsections that follow. The code commenting guidelines that follow apply to C++, but similar rules are in place at Google for other languages.

我们都知道，API 要有完善的文档，代码注释必不可少。但怎样的注释才算“好”？前面区分了参考文档的两类主要读者：查找者和浏览者。前者知道自己需要什么，后者则不清楚。对查找者而言，最有帮助的是代码库中一致的注释格式，让他们能快速浏览 API，找到所需信息。对浏览者而言，最重要的是明确说明 API 的用途，通常应放在文件开头的注释中。下面几个小节会具体介绍代码注释。这里的指南针对 C++，谷歌对其他语言也有类似规则。

**File comments 文件注释**  
Almost all code files at Google must contain a file comment. (Some header files that contain only one utility function, etc., might deviate from this standard.) File comments should begin with a header of the following form:

谷歌几乎所有代码文件都必须包含文件注释；只含一个工具函数的头文件等情况可能例外。文件注释应以下列形式开头：

```C++
// -----------------------------------------------------------------------------
// str_cat.h
// -----------------------------------------------------------------------------
//
// This header file contains functions for efficiently concatenating and appending
// strings: StrCat() and StrAppend(). Most of the work within these routines is
// actually handled through use of a special AlphaNum type, which was designed
// to be used as a parameter type that efficiently manages conversion to
// strings and avoids copies in the above operations.
... ...
```

Generally, a file comment should begin with an outline of what’s contained in the code you are reading. It should identify the code’s main use cases and intended audience (in the preceding case, developers who want to concatenate strings). Any API that cannot be succinctly described in the first paragraph or two is usually the sign of an API that is not well thought out. Consider breaking the API into separate components in those cases.

文件注释通常应先概述当前代码的内容，说明主要用例和目标受众；上例面向的就是需要拼接字符串的开发者。如果一个 API 无法在开头一两段中简明地描述清楚，通常说明它的设计还不够周全。这时，应考虑把 API 拆成独立的组件。

#### Class comments 类注释

Most modern programming languages are object oriented. Class comments are therefore important for defining the API “objects” in use in a codebase. All public classes (and structs) at Google must contain a class comment describing the class/struct, important methods of that class, and the purpose of the class. Generally, class comments should be “nouned” with documentation emphasizing their object aspect. That is, say, “The Foo class contains x, y, z, allows you to do Bar, and has the following Baz aspects,” and so on.

大多数现代编程语言都是面向对象的，因此类注释对说明代码库中的 API“对象”很重要。谷歌所有公共类和结构体都必须包含类注释，描述该类或结构体、重要方法及其用途。类注释通常应以名词为中心，突出它所表示的对象。例如：“Foo 类包含 x、y、z，支持 Bar 操作，并具有以下 Baz 特性。”

Class comments should generally begin with a comment of the following form:

类注释通常应以下列形式开头：

```Java
// -----------------------------------------------------------------------------
// AlphaNum
// -----------------------------------------------------------------------------
//
// The AlphaNum class acts as the main parameter type for StrCat() and
// StrAppend(), providing efficient conversion of numeric, boolean, and
// hexadecimal values (through the Hex type) into strings.
```

#### Function comments 函数注释

All free functions, or public methods of a class, at Google must also contain a function comment describing what the function *does*. Function comments should stress the *active* nature of their use, beginning with an indicative verb describing what the function does and what is returned.

在谷歌，所有非成员函数以及类的公共方法，也都必须有函数注释，说明函数做什么。函数注释应突出它所执行的操作，以陈述动作的动词开头，描述函数的作用和返回值。

Function comments should generally begin with a comment of the following form:

函数注释通常应以下列形式开头：

```Java
// StrCat()
//
// Merges the given strings or numbers, using no delimiter(s),
// returning the merged result as a string.
... ...
```

Note that starting a function comment with a declarative verb introduces consistency across a header file. A seeker can quickly scan an API and read just the verb to get an idea of whether the function is appropriate: “Merges, Deletes, Creates,” and so on.

注意，以陈述动作的动词开头，可以让头文件中的函数注释保持一致。查找者快速浏览 API 时，只看“合并”“删除”“创建”等动词，就能大致判断函数是否适用。

Some documentation styles (and some documentation generators) require various forms of boilerplate on function comments, like “Returns:”, “Throws:”, and so forth, but at Google we haven’t found them to be necessary. It is often clearer to present such information in a single prose comment that’s not broken up into artificial section boundaries:

有些文档风格和文档生成器要求函数注释采用固定格式，例如“Returns:”“Throws:”等，但谷歌并未发现这些格式必不可少。把相关信息写成一段连贯的注释，往往比人为划分成几个小节更清楚：

```Java
// Creates a new record for a customer with the given name and address,
// and returns the record ID, or throws `DuplicateEntryError` if a
// record with that name already exists.
int AddCustomer(string name, string address);
```

Notice how the postcondition, parameters, return value, and exceptional cases are naturally documented together (in this case, in a single sentence), because they are not independent of one another. Adding explicit boilerplate sections would make the comment more verbose and repetitive, but no clearer (and arguably less clear).

注意，后置条件、参数、返回值和异常情况自然地写在了一起，本例甚至只用了一句话，因为这些信息并不彼此独立。加入固定格式的小节，只会让注释更冗长、更重复，并不会更清楚，甚至可能更难理解。

### Design Docs 设计文档

Most teams at Google require an approved design document before starting work on any major project. A software engineer typically writes the proposed design document using a specific design doc template approved by the team. Such documents are designed to be collaborative, so they are often shared in Google Docs, which has good collaboration tools. Some teams require such design documents to be discussed and debated at specific team meetings, where the finer points of the design can be discussed or critiqued by experts. In some respects, these design discussions act as a form of code review before any code is written.

谷歌大多数团队要求，重大项目开工前必须有一份获批的设计文档。软件工程师通常使用团队认可的模板，写出设计提案。设计文档需要协作完善，因此往往通过具备良好协作工具的 Google Docs 共享。有些团队还要求在专门的团队会议上讨论和辩论设计，让专家审视其中的细节。从某种意义上说，这些设计讨论相当于在动手写代码之前，先进行一轮代码审查。

Because the development of a design document is one of the first processes an engineer undertakes before deploying a new system, it is also a convenient place to ensure that various concerns are covered. The canonical design document templates at Google require engineers to consider aspects of their design such as security implications, internationalization, storage requirements and privacy concerns, and so on. In most cases, such parts of those design documents are reviewed by experts in those domains.

编写设计文档是工程师部署新系统前最早开展的工作之一，因此也是确保各类问题得到考虑的合适时机。谷歌的标准设计文档模板要求工程师考虑安全影响、国际化、存储需求、隐私等方面。通常，文档中的这些部分会由相应领域的专家审查。

A good design document should cover the goals of the design, its implementation strategy, and propose key design decisions with an emphasis on their individual trade-offs. The best design documents suggest design goals and cover alternative designs, denoting their strong and weak points.

好的设计文档应说明设计目标和实现策略，提出关键设计决策，并重点阐明每项决策的权衡。最好的设计文档还会提出设计目标，讨论备选方案，指出各自的优缺点。

A good design document, once approved, also acts not only as a historical record, but as a measure of whether the project successfully achieved its goals. Most teams archive their design documents in an appropriate location within their team documents so that they can review them at a later time. It’s often useful to review a design document before a product is launched to ensure that the stated goals when the design document was written remain the stated goals at launch (and if they do not, either the document or the product can be adjusted accordingly).

一份好的设计文档获批后，不仅能留下历史记录，还能作为衡量项目是否达成目标的依据。大多数团队会把设计文档归档到团队文档中的适当位置，以便日后回顾。产品发布前重新审视设计文档，往往很有帮助：这样可以确认，撰写文档时确立的目标，到发布时是否仍然一致；若不一致，就相应调整文档或产品。

### Tutorials 教程

Every software engineer, when they join a new team, will want to get up to speed as quickly as possible. Having a tutorial that walks someone through the setup of a new project is invaluable; “Hello World” has established itself is one of the best ways to ensure that all team members start off on the right foot. This goes for documents as well as code. Most projects deserve a “Hello World” document that assumes nothing and gets the engineer to make something “real” happen.

每位软件工程师加入新团队时，都希望尽快上手。一份带领新人完成新项目配置的教程非常宝贵。“Hello World”已被证明是让所有团队成员顺利起步的最佳方式之一，对代码如此，对文档也是如此。大多数项目都值得配上一份“Hello World”文档，不预设读者已经具备相关条件或知识，并让工程师真正做出一点东西。

Often, the best time to write a tutorial, if one does not yet exist, is when you first join a team. (It’s also the best time to find bugs in any existing tutorial you are following.) Get a notepad or other way to take notes, and write down everything you need to do along the way, assuming no domain knowledge or special setup constraints; after you’re done, you’ll likely know what mistakes you made during the process—and why —and can then edit down your steps to get a more streamlined tutorial. Importantly, write everything you need to do along the way; try not to assume any particular setup, permissions, or domain knowledge. If you do need to assume some other setup, state that clearly in the beginning of the tutorial as a set of prerequisites.

如果团队还没有教程，通常你刚加入时就是编写教程的最佳时机；这也是发现现有教程问题的最佳时机。拿个记事本，或用其他方式，记下沿途需要做的每件事，不预设读者已有领域知识或满足特定配置条件。全部完成后，你很可能已经知道自己哪里出过错、为什么出错，再据此精简步骤，整理出更流畅的教程。重要的是完整记录每一步，不要默认读者已经具备某种配置、权限或领域知识。如果确实依赖其他配置，就在教程开头将其明确列为前提条件。

Most tutorials require you to perform a number of steps, in order. In those cases, number those steps explicitly. If the focus of the tutorial is on the user (say, for external developer documentation), then number each action that a user needs to undertake. Don’t number actions that the system may take in response to such user actions. It is critical and important to number explicitly every step when doing this. Nothing is more annoying than an error on step 4 because you forget to tell someone to properly authorize their username, for example.

大多数教程需要读者按顺序完成多个步骤，这时应明确编号。如果教程以用户为中心，例如面向外部开发者的文档，就应给用户需要执行的每个操作编号，而不要给系统响应这些操作时自动执行的动作编号。每一步都明确列出、编上序号，这一点至关重要。例如，仅仅因为你漏写了应为用户的用户名授予适当权限，就让对方在第4步报错，实在令人恼火。

**Example: A bad tutorial**

1. Download the package from our server at <http://example.com>
2. Copy the shell script to your home directory
3. Execute the shell script
4. The foobar system will communicate with the authentication system
5. Once authenticated, foobar will bootstrap a new database named “baz”
6. Test “baz” by executing a SQL command on the command line
7. Type: CREATE DATABASE my_foobar_db;

**示例：糟糕的教程**

1. 从我们的服务器下载软件包，地址为<http://example.com>
2. 将 shell 脚本复制到主目录
3. 执行 shell 脚本
4. foobar 系统将与身份验证系统通信
5. 身份验证通过后，foobar 将初始化一个名为“baz”的新数据库
6. 在命令行执行 SQL 命令，测试“baz”
7. 输入：CREATE DATABASE my_foobar_db;

In the preceding procedure, steps 4 and 5 happen on the server end. It’s unclear whether the user needs to do anything, but they don’t, so those side effects can be mentioned as part of step 3. As well, it’s unclear whether step 6 and step 7 are different. (They aren’t.) Combine all atomic user operations into single steps so that the user knows they need to do something at each step in the process. Also, if your tutorial has user-visible input or output, denote that on separate lines (often using the convention of a monospaced bold font).

在上述流程中，第4步和第5步都在服务器端执行。文档没有说清用户是否需要操作，但其实不需要，所以可以把这些附带动作并入第3步说明。第6步和第7步是否为不同操作也不清楚，实际上它们是同一个操作。应把每个完整、不可再分的用户操作合并为一个步骤，让读者知道每一步都需要自己动手。此外，如果教程包含用户可见的输入或输出，应单独列行，通常使用等宽粗体。

**Example: A bad tutorial made better**

1. Download the package from our server at <http://example.com>:

```bash
curl -I http://example.com
```

2. Copy the shell script to your home directory:

```bash
cp foobar.sh ~
```

3. Execute the shell script in your home directory:

```bash
cd ~; foobar.sh
```

The foobar system will first communicate with the authentication system. Once authenticated, foobar will bootstrap a new database named “baz” and open an input shell.
4. Test “baz” by executing a SQL command on the command line:

```bash
baz:$ CREATE DATABASE my_foobar_db;
```

示例：改进后的教程

1. 从我们的服务器下载软件包，地址为<http://example.com>：

```bash
$curl -I http://example.com
```

2. 将 shell 脚本复制到主目录：

```bash
$cp foobar.sh ~
```

3. 在主目录中执行 shell 脚本：

```bash
$cd ~; foobar.sh
```

foobar 系统会先与身份验证系统通信。验证通过后，foobar 将初始化一个名为“baz”的新数据库，并打开一个可输入命令的 shell。

4. 在命令行执行 SQL 命令，测试“baz”：

```bash
baz:$CREATE DATABASE my_foobar_db;
```

Note how each step requires specific user intervention. If, instead, the tutorial had a focus on some other aspect (e.g., a document about the “life of a server”), number those steps from the perspective of that focus (what the server does).

注意，每一步都要求用户执行一项具体操作。如果教程侧重其他对象，例如介绍“服务器生命周期”，则应从该对象的角度组织并编号步骤，也就是列出服务器执行的动作。

### Conceptual Documentation 概念文档

Some code requires deeper explanations or insights than can be obtained simply by reading the reference documentation. In those cases, we need conceptual documentation to provide overviews of the APIs or systems. Some examples of conceptual documentation might be a library overview for a popular API, a document describing the life cycle of data within a server, and so on. In almost all cases, a conceptual document is meant to augment, not replace, a reference documentation set. Often this leads to duplication of some information, but with a purpose: to promote clarity. In those cases, it is not necessary for a conceptual document to cover all edge cases (though a reference should cover those cases religiously). In this case, sacrificing some accuracy is acceptable for clarity. The main point of a conceptual document is to impart understanding.

有些代码需要更深入的解释，仅阅读参考文档还不足以理解。这时，就需要概念文档来概述 API 或系统，例如介绍某个常用 API 所属库的概览，或说明数据在服务器中生命周期的文档。概念文档几乎总是对参考文档的补充，而非替代。两者往往会重复一些信息，但这是为了讲得更清楚。概念文档不必涵盖所有边界情况，参考文档则应严格覆盖。在这里，为了清晰易懂而适当牺牲准确性是可以接受的，因为概念文档的首要目的是帮助读者理解。

“Concept” documents are the most difficult forms of documentation to write. As a result, they are often the most neglected type of document within a software engineer’s toolbox. One problem engineers face when writing conceptual documentation is that it often cannot be embedded directly within the source code because there isn’t a canonical location to place it. Some APIs have a relatively broad API surface area, in which case, a file comment might be an appropriate place for a “conceptual” explanation of the API. But often, an API works in conjunction with other APIs and/or modules. The only logical place to document such complex behavior is through a separate conceptual document. If comments are the unit tests of documentation, conceptual documents are the integration tests.

概念文档最难写，因此往往也是软件工程师最容易忽视的文档类型。一个难点是，它通常没有明确的权威存放位置，因而难以直接嵌入源代码。有些 API 对外提供的接口范围较广，这时可以在文件注释中作概念性说明。但 API 往往会与其他 API、模块或两者共同工作，要说明这种复杂行为，唯一合理的方式就是另写一份概念文档。如果把代码注释比作文档中的单元测试，那么概念文档就是集成测试。

Even when an API is appropriately scoped, it often makes sense to provide a separate conceptual document. For example, Abseil’s StrFormat library covers a variety of concepts that accomplished users of the API should understand. In those cases, both internally and externally, we provide a format concepts document.

即使 API 的范围划分合理，单独提供概念文档通常仍然值得。例如，Abseil 的 StrFormat 库涉及多个概念，熟练使用这个 API 的用户应当理解它们。因此，我们面向内部和外部用户都提供了格式化概念文档。

A concept document needs to be useful to a broad audience: both experts and novices alike. Moreover, it needs to emphasize clarity, so it often needs to sacrifice completeness (something best reserved for a reference) and (sometimes) strict accuracy. That’s not to say a conceptual document should intentionally be inaccurate; it just means that it should focus on common usage and leave rare usages or side effects for reference documentation.

概念文档需要同时帮助专家和新手等广泛受众，并以清晰易懂为重。因此，往往需要放弃面面俱到，把完整性留给参考文档；有时也需要在严格的准确性上作些取舍。这并不是说要故意写得不准确，而是应侧重常见用法，把少见用法和副作用留给参考文档。

### Landing Pages 入口页

Most engineers are members of a team, and most teams have a “team page” somewhere on their company’s intranet. Often, these sites are a bit of a mess: a typical landing page might contain some interesting links, sometimes several documents titled “read this first!”, and some information both for the team and for its customers. Such documents start out useful but rapidly turn into disasters; because they become so cumbersome to maintain, they will eventually get so obsolete that they will be fixed by only the brave or the desperate.

大多数工程师都属于某个团队，而大多数团队都会在公司内网上设置“团队页面”。这些站点往往有些混乱：典型的入口页可能放着一些有趣的链接、几份标题为“请先读这里！”的文档，以及面向团队和客户的各种信息。这类文档起初很有用，却很快会变得一团糟。由于维护过于繁琐，内容最终严重过时，只有格外勇敢或实在别无选择的人才会去修整。

Luckily, such documents look intimidating, but are actually straightforward to fix: ensure that a landing page clearly identifies its purpose, and then include only links to other pages for more information. If something on a landing page is doing more than being a traffic cop, it is not doing its job. If you have a separate setup document, link to that from the landing page as a separate document. If you have too many links on the landing page (your page should not scroll multiple screens), consider breaking up the pages by taxonomy, under different sections.

好在这类文档虽然看起来棘手，修整方法却很直接：让入口页明确说明自身用途，其余详细信息只通过链接引向其他页面。入口页的职责就是引导读者，承担更多工作反而偏离了本职。如果已有独立的配置文档，就从入口页链接过去。如果链接过多，页面长到需要滚动好几屏，就应考虑按类别分组，把相关页面放在不同小节下。

Most poorly configured landing pages serve two different purposes: they are the “goto” page for someone who is a user of your product or API, or they are the home page for a team. Don’t have the page serve both masters—it will become confusing. Create a separate “team page” as an internal page apart from the main landing page. What the team needs to know is often quite different than what a customer of your API needs to know.

大多数组织不当的入口页混合了两种用途：既是产品或 API 用户查找信息的首选页面，又是团队主页。不要让同一页面兼顾这两种用途，否则容易混乱。应当在主入口页之外，另设一个面向内部的“团队页面”。团队需要了解的内容，往往与 API 客户的需求大不相同。

## Documentation Reviews 文档评审

At Google, all code needs to be reviewed, and our code review process is well understood and accepted. In general, documentation also needs review (though this is less universally accepted). If you want to “test” whether your documentation works, you should generally have someone else review it.

在谷歌，所有代码都需要审查，代码审查流程也已得到充分理解和普遍接受。一般来说，文档同样需要评审，只是这一点还没有得到同样广泛的认可。想“测试”文档是否有用，通常就应请别人来评审。

A technical document benefits from three different types of reviews, each emphasizing different aspects:

- A technical review, for accuracy. This review is usually done by a subject matter expert, often another member of your team. Often, this is part of a code review itself.
- An audience review, for clarity. This is usually someone unfamiliar with the domain. This might be someone new to your team or a customer of your API.
- A writing review, for consistency. This is often a technical writer or volunteer.

技术文档可以从以下三类评审中受益，各自侧重不同方面：

- 技术评审侧重准确性，通常由领域专家完成，往往就是团队中的另一位成员。这类评审常常也是代码审查的一部分。
- 受众评审侧重是否清晰易懂，通常由不熟悉该领域的人完成，例如团队新人或 API 客户。
- 写作评审侧重一致性，通常由技术撰稿人或志愿者完成。

Of course, some of these lines are sometimes blurred, but if your document is high profile or might end up being externally published, you probably want to ensure that it receives more types of reviews. (We’ve used a similar review process for this book.) Any document tends to benefit from the aforementioned reviews, even if some of those reviews are ad hoc. That said, even getting one reviewer to review your text is preferable to having no one review it.

这些评审之间的界限有时并不清晰。不过，如果文档受到广泛关注，或最终可能对外发布，就应尽量让它接受更多类型的评审；本书也采用了类似流程。任何文档通常都能从上述评审中受益，即使有些评审只是临时安排的。当然，哪怕只请一位评审者看过，也比完全无人评审好。

Importantly, if documentation is tied into the engineering workflow, it will often improve over time. Most documents at Google now implicitly go through an audience review because at some point, their audience will be using them, and hopefully letting you know when they aren’t working (via bugs or other forms of feedback).

重要的是，文档一旦融入工程工作流，往往就会随着时间推移不断改进。谷歌现在的大多数文档实际上都会经历受众评审：读者迟早会使用文档，而我们希望，他们发现文档不管用时，会通过缺陷报告或其他反馈途径告诉作者。

---
**Case Study: The Developer Guide Library 案例研究：开发者指南库**  
As mentioned earlier, there were problems associated with having most (almost all) engineering documentation contained within a shared wiki: little ownership of important documentation, competing documentation, obsolete information, and difficulty in filing bugs or issues with documentation. But this problem was not seen in some documents: the Google C++ style guide was owned by a select group of senior engineers (style arbiters) who managed it. The document was kept in good shape because certain people cared about it. They implicitly owned that document. The document was also canonical: there was only one C++ style guide.

前面提到，把大多数乃至几乎所有工程文档都放在共享维基中，会带来一些问题：重要文档缺乏负责人，同一主题存在相互竞争的文档，信息过时，文档错误或问题也难以报告。但有些文档没有这些问题。例如，谷歌的 C++ 风格指南由一组选定的资深工程师，也就是风格仲裁者负责管理。有人关心这份文档，它就一直保持着良好状态。这些人实际上承担了负责人的职责。它也具有权威性，因为 C++ 风格指南只有一份。

As previously mentioned, documentation that sits directly within source code is one way to promote the establishment of canonical documents; if the documentation sits alongside the source code, it should usually be the most applicable (hopefully). At Google, each API usually has a separate g3doc directory where such documents live (written as Markdown files and readable within our Code Search browser). Having the documentation exist alongside the source code not only establishes de facto ownership, it makes the documentation seem more wholly “part” of the code.

如前所述，把文档直接放进源代码，是确立权威文档的一种方式。与源码放在一起的文档，通常应当最适用，至少我们希望如此。在谷歌，每个 API 通常都有独立的 g3doc 目录，用来存放 Markdown 文档，并可在 Code Search 代码浏览工具中阅读。文档与源码并置，不仅确立了实际的责任归属，也更让人觉得文档就是代码的一部分。

Some documentation sets, however, cannot exist very logically within source code. A “C++ developer guide” for Googlers, for example, has no obvious place to sit within the source code. There is no master “C++” directory where people will look for such information. In this case (and others that crossed API boundaries), it became useful to create standalone documentation sets in their own depot. Many of these culled together associated existing documents into a common set, with common navigation and look-and-feel. Such documents were noted as “Developer Guides” and, like the code in the codebase, were under source control in a specific documentation depot, with this depot organized by topic rather than API. Often, technical writers managed these developer guides, because they were better at explaining topics across API boundaries.

不过，有些文档集很难在源码中找到合理的位置。例如，面向谷歌员工的“C++ 开发者指南”就没有明显适合存放的地方：源码中没有一个供大家查找这类信息的总“C++”目录。对于这种跨越 API 边界的文档，建立独立文档集并放入专门仓库就很有用。许多文档集会选取现有的相关文档，整合为一套具有统一导航和外观的资料，称为“开发者指南”。它们与代码一样纳入源代码版本控制，但存放在专门的文档仓库中，按主题而非 API 组织。这些指南通常由技术撰稿人管理，因为他们更善于解释跨 API 的主题。

Over time, these developer guides became canonical. Users who wrote competing or supplementary documents became amenable to adding their documents to the canonical document set after it was established, and then deprecating their competing documents. Eventually, the C++ style guide became part of a larger “C++ Developer Guide.” As the documentation set became more comprehensive and more authoritative, its quality also improved. Engineers began logging bugs because they knew someone was maintaining these documents. Because the documents were locked down under source control, with proper owners, engineers also began sending changelists directly to the technical writers.

随着时间推移，这些开发者指南逐渐成为权威文档。权威文档集建立后，原先另写同类或补充文档的用户，也愿意把内容纳入其中，再弃用原来的重复文档。最终，C++ 风格指南成为更完整的“C++ 开发者指南”的一部分。文档集越全面、越权威，质量也随之提升。工程师知道有人维护，便开始提交缺陷报告。由于文档已统一纳入源代码版本控制，并有明确的负责人，工程师也开始直接向技术撰稿人发送变更列表。

The introduction of go/links (see Chapter 3) allowed most documents to, in effect,more easily establish themselves as canonical on any given topic. Our C++ Developer Guide became established at “go/cpp,” for example. With better internal search, go/links, and the integration of multiple documents into a common documentation set,such canonical documentation sets became more authoritative and robust over time.

引入 go/links（见第3章）后，大多数文档更容易成为相应主题的权威来源。例如，“go/cpp”成为 C++ 开发者指南的固定入口。借助更好的内部搜索、go/links，以及多份文档的统一整合，这些文档集逐渐变得更权威、更完善。

---

## Documentation Philosophy 文档写作理念

Caveat: the following section is more of a treatise on technical writing best practices (and personal opinion) than of “how Google does it.” Consider it optional for software engineers to fully grasp, though understanding these concepts will likely allow you to more easily write technical information.

需要说明的是，下面主要讨论技术写作的最佳实践，也包含个人看法，并非介绍“谷歌是怎么做的”。软件工程师不必强求完全掌握这一部分，但理解这些概念，可能会让技术内容更容易写清楚。

### WHO, WHAT, WHEN, WHERE, and WHY 谁、什么、何时、何地、为什么

Most technical documentation answers a “HOW” question. How does this work? How do I program to this API? How do I set up this server? As a result, there’s a tendency for software engineers to jump straight into the “HOW” on any given document and ignore the other questions associated with it: the WHO, WHAT, WHEN, WHERE, and WHY. It’s true that none of those are generally as important as the HOW—a design document is an exception because an equivalent aspect is often the WHY—but without a proper framing of technical documentation, documents end up confusing. Try to address the other questions in the first two paragraphs of any document:

- WHO was discussed previously: that’s the audience. But sometimes you also need to explicitly call out and address the audience in a document. Example: “This document is for new engineers on the Secret Wizard project.”
- WHAT identifies the purpose of this document: “This document is a tutorial designed to start a Frobber server in a test environment.” Sometimes, merely writing the WHAT helps you frame the document appropriately. If you start adding information that isn’t applicable to the WHAT, you might want to move that information into a separate document.
- WHEN identifies when this document was created, reviewed, or updated. Documents in source code have this date noted implicitly, and some other publishing schemes automate this as well. But, if not, make sure to note the date on which the document was written (or last revised) on the document itself.
- WHERE is often implicit as well, but decide where the document should live. Usually, the preference should be under some sort of version control, ideally with the source code it documents. But other formats work for different purposes as well. At Google, we often use Google Docs for easy collaboration, particularly on design issues. At some point, however, any shared document becomes less of a discussion and more of a stable historical record. At that point, move it to someplace more permanent, with clear ownership, version control, and responsibility.
- WHY sets up the purpose for the document. Summarize what you expect someone to take away from the document after reading it. A good rule of thumb is to establish the WHY in the introduction to a document. When you write the summary, verify whether you’ve met your original expectations (and revise accordingly).

大多数技术文档回答的是“如何”：系统如何工作？如何使用这个 API 编程？如何配置这台服务器？因此，软件工程师写文档时，容易直接进入“如何”，忽略相关的其他问题：谁、什么、何时、何地、为什么。通常，这些问题确实不如“如何”重要，设计文档是个例外，其中“为什么”往往同样重要。但如果没有先交代清楚背景，技术文档就容易令人困惑。应尽量在每份文档的前两段回答其他几个问题：

- WHO 指受众，前面已经讨论过。有时还应在文档中直接点明它写给谁。例如：“本文档面向刚加入秘密向导项目的工程师。”
- WHAT 说明文档的用途，例如：“本教程介绍如何在测试环境中启动 Frobber 服务器。”有时，只要把“写什么”说清楚，就能帮助你确定文档范围。如果后来加入的信息超出了这个范围，就应考虑移到另一份文档中。
- WHEN 说明文档的创建、评审或更新时间。存放在源代码中的文档已经隐含记录了这些日期，有些其他发布机制也会自动记录。否则，就务必在文档中注明编写日期或最近一次修订日期。
- WHERE 往往也隐含在文档中，但仍需决定文档应放在哪里。通常应优先纳入某种版本控制，最好与所说明的源代码放在一起；其他形式也各有用途。在谷歌，我们经常使用 Google Docs 方便协作，尤其是讨论设计问题。不过，共享文档到了某个阶段，会从讨论载体变为相对稳定的历史记录。这时，就应把它移到更适合长期保存的位置，明确归属和维护责任，并纳入版本控制。
- WHY 交代写作目的。概括说明希望读者读完后获得什么。一个实用做法是，在引言中明确“为什么”，写总结时再检查是否达到了最初的预期，并据此修订。

### The Beginning, Middle, and End 开头、中间和结尾

All documents—indeed, all parts of documents—have a beginning, middle, and end. Although it sounds amazingly silly, most documents should often have, at a minimum, those three sections. A document with only one section has only one thing to say, and very few documents have only one thing to say. Don’t be afraid to add sections to your document; they break up the flow into logical pieces and provide readers with a roadmap of what the document covers.

所有文档，乃至文档中的每个部分，都有开头、中间和结尾。这听起来似乎是句废话，但大多数文档至少应有这三个部分。只有一个部分的文档只能围绕一件事展开，而很少有文档只需要说一件事。不要怕给文档划分小节；小节能按逻辑组织行文，也让读者看清文档涵盖哪些内容。

Even the simplest document usually has more than one thing to say. Our popular “C++ Tips of the Week” have traditionally been very short, focusing on one small piece of advice. However, even here, having sections helps. Traditionally, the first section denotes the problem, the middle section goes through the recommended solutions, and the conclusion summarizes the takeaways. Had the document consisted of only one section, some readers would doubtless have difficulty teasing out the important points.

即使最简单的文档，通常也不只需要说一件事。广受欢迎的“每周 C++ 提示”一向很短，每篇聚焦一条小建议，但即便如此，划分小节仍然有帮助。通常，开头说明问题，中间介绍推荐方案，结尾归纳要点。如果整篇只有一个部分，有些读者就难以提炼出重点。

Most engineers loathe redundancy, and with good reason. But in documentation, redundancy is often useful. An important point buried within a wall of text can be difficult to remember or tease out. On the other hand, placing that point at a more prominent location early can lose context provided later on. Usually, the solution is to introduce and summarize the point within an introductory paragraph, and then use the rest of the section to make your case in a more detailed fashion. In this case, redundancy helps the reader understand the importance of what is being stated.

大多数工程师不喜欢冗余，这不无道理。但在文档中，适当重复往往有益。要点埋在大段文字中，读者可能难以发现或记住；若直接移到开头的醒目位置，又可能缺少后文提供的背景。通常的办法是，先在引入段落中概述要点，再用本节其余篇幅详细说明。这样的重复有助于读者理解所述内容的重要性。

### The Parameters of Good Documentation 良好文档的衡量标准

There are usually three aspects of good documentation: completeness, accuracy, and clarity. You rarely get all three within the same document; as you try to make a document more “complete,” for example, clarity can begin to suffer. If you try to document every possible use case of an API, you might end up with an incomprehensible mess. For programming languages, being completely accurate in all cases (and documenting all possible side effects) can also affect clarity. For other documents, trying to be clear about a complicated topic can subtly affect the accuracy of the document; you might decide to ignore some rare side effects in a conceptual document, for example,because the point of the document is to familiarize someone with the usage of an API, not provide a dogmatic overview of all intended behavior.

好文档通常有三个衡量维度：完整性、准确性和清晰性。一份文档很难三者兼得。例如，越追求“完整”，清晰性就越可能受损；试图列出 API 的所有可能用例，最终可能把文档写得杂乱难懂。介绍编程语言时，追求所有情况下都完全准确，并记录一切可能的副作用，也会影响清晰性。反过来，其他类型的文档为了把复杂主题讲清楚，又可能在细节上影响准确性。例如，概念文档可能省略一些少见的副作用，因为它旨在帮助读者熟悉 API 的用法，而非刻板地罗列所有预期行为。

In each case, a “good document” is defined as the document that is doing its intended job. As a result, you rarely want a document doing more than one job. For each document (and for each document type), decide on its focus and adjust the writing appropriately. Writing a conceptual document? You probably don’t need to cover every part of the API. Writing a reference? You probably want this complete, but perhaps must sacrifice some clarity. Writing a landing page? Focus on organization and keep discussion to a minimum. All of this adds up to quality, which, admittedly, is stubbornly difficult to accurately measure.

无论哪种情况，“好文档”都是能完成预定任务的文档，因此通常不应让一份文档承担多项任务。要为每份文档及每类文档确定重点，相应调整写法。写概念文档，可能不必覆盖 API 的每个部分；写参考文档，通常应追求完整，为此也许不得不牺牲一些清晰性；写入口页，则应着重组织信息，尽量少作展开讨论。这些因素共同决定文档质量，而质量确实很难准确衡量。

How can you quickly improve the quality of a document? Focus on the needs of the audience. Often, less is more. For example, one mistake engineers often make is adding design decisions or implementation details to an API document. Much like you should ideally separate the interface from an implementation within a welldesigned API, you should avoid discussing design decisions in an API document. Users don’t need to know this information. Instead, put those decisions in a specialized document for that purpose (usually a design doc).

怎样快速提高文档质量？关注受众需求，往往少即是多。例如，工程师常犯的错误，是在 API 文档中加入设计决策或实现细节。正如设计良好的 API 应尽量将接口与实现分离，API 文档也应避免讨论设计决策。用户不需要了解这些信息，应把它们放在专门的文档中，通常就是设计文档。

### Deprecating Documents 弃用文档

Just like old code can cause problems, so can old documents. Over time, documents become stale, obsolete, or (often) abandoned. Try as much as possible to avoid abandoned documents, but when a document no longer serves any purpose, either remove it or identify it as obsolete (and, if available, indicate where to go for new information). Even for unowned documents, someone adding a note that “This no longer works!” is more helpful than saying nothing and leaving something that seems authoritative but no longer works.

旧代码会带来问题，旧文档也一样。随着时间推移，文档可能陈旧、失效，或者更常见地，无人再维护。应尽量避免让文档处于无人维护的状态；如果一份文档已经毫无用途，就将其删除或标明已过时，并在有新信息来源时给出指引。即使文档没有负责人，补上一句“这些内容已经不适用了！”，也比一言不发、留下看似权威却已失效的内容更有帮助。

At Google, we often attach “freshness dates” to documentation. Such documents note the last time a document was reviewed, and metadata in the documentation set will send email reminders when the document hasn’t been touched in, for example, three months. Such freshness dates, as shown in the following example—and tracking your documents as bugs—can help make a documentation set easier to maintain over time, which is the main concern for a document:

在谷歌，我们常给文档附上“时效检查日期”，记录最近一次审阅的时间。借助文档集中的元数据，如果文档已有一段时间未改动，例如三个月，系统就会发送邮件提醒。下例所示的时效检查日期，再加上像跟踪缺陷一样跟踪文档，有助于降低长期维护的难度；这正是文档需要重点解决的问题：

```Java
<!--*
# Document freshness: For more information, see go/fresh-source. freshness: { owner: `username` reviewed: '2019-02-27' }

# 文档的新鲜度：更多信息，请看 go/fresh-source。 freshness: { owner: `username` reviewed: '2019-02-27' }
*-->
```

Users who own such a document have an incentive to keep that freshness date current (and if the document is under source control, that requires a code review). As a result, it’s a low-cost means to ensure that a document is looked over from time to time. At Google, we found that including the owner of a document in this freshness date within the document itself with a byline of “Last reviewed by...” led to increased adoption as well.

文档负责人有动力及时更新时效检查日期；如果文档已纳入源代码版本控制，这项修改还需要经过代码审查。因此，这是一种成本很低的办法，能促使人们定期检查文档。谷歌还发现，在文档的时效检查信息中加上负责人，以“Last Review by…”署名，也能提高这项做法的采用率。

## When Do You Need Technical Writers? 何时需要技术撰稿人？

When Google was young and growing, there weren’t enough technical writers in software engineering. (That’s still the case.) Those projects deemed important tended to receive a technical writer, regardless of whether that team really needed one. The idea was that the writer could relieve the team of some of the burden of writing and maintaining documents and (theoretically) allow the important project to achieve greater velocity. This turned out to be a bad assumption.

谷歌早期不断发展时，软件工程领域的技术撰稿人并不充足，现在仍然如此。当时，只要项目被认为重要，通常就会配备一位技术撰稿人，而不论团队是否真的需要。设想是由技术撰稿人分担文档编写和维护工作，理论上让重要项目推进得更快。事实证明，这个假设并不成立。

We learned that most engineering teams can write documentation for themselves (their team) perfectly fine; it’s only when they are writing documents for another audience that they tend to need help because it’s difficult to write to another audience. The feedback loop within your team regarding documents is more immediate, the domain knowledge and assumptions are clearer, and the perceived needs are more obvious. Of course, a technical writer can often do a better job with grammar and organization, but supporting a single team isn’t the best use of a limited and specialized resource; it doesn’t scale. It introduced a perverse incentive: become an important project and your software engineers won’t need to write documents. Discouraging engineers from writing documents turns out to be the opposite of what you want to do.

我们发现，大多数工程团队完全能为本团队写好文档，往往只有面向其他受众时才需要帮助，因为为其他人写作更困难。团队内部的文档反馈更及时，领域知识和默认前提更清楚，需求也更容易看见。技术撰稿人当然通常能把语法和结构处理得更好，但让这种稀缺的专业资源只服务一个团队，并不是最佳用法，也难以随组织规模扩展。这种安排还产生了反向激励：只要项目变得重要，软件工程师就不必写文档了。然而，削弱工程师写文档的意愿，恰恰与我们的目标背道而驰。

Because they are a limited resource, technical writers should generally focus on tasks that software engineers don’t need to do as part of their normal duties. Usually, this involves writing documents that cross API boundaries. Project Foo might clearly know what documentation Project Foo needs, but it probably has a less clear idea what Project Bar needs. A technical writer is better able to stand in as a person unfamiliar with the domain. In fact, it’s one of their critical roles: to challenge the assumptions your team makes about the utility of your project. It’s one of the reasons why many, if not most, software engineering technical writers tend to focus on this specific type of API documentation.

技术撰稿人是稀缺资源，通常应专注于不属于软件工程师日常职责的工作，往往就是编写跨 API 边界的文档。Foo 项目团队可能很清楚自己需要什么文档，却未必清楚 Bar 项目的需求。技术撰稿人更能站在不熟悉该领域的人的立场上。事实上，他们的重要职责之一，就是质疑团队对项目用途所作的假设。这也是许多乃至大多数软件工程技术撰稿人专注于这类 API 文档的原因之一。

## Conclusion 总结

Google has made good strides in addressing documentation quality over the past decade, but to be frank, documentation at Google is not yet a first-class citizen. For comparison, engineers have gradually accepted that testing is necessary for any code change, no matter how small. As well, testing tooling is robust, varied and plugged into an engineering workflow at various points. Documentation is not ingrained at nearly the same level.

过去十年间，谷歌在改善文档质量方面进步很大。但坦率地说，文档在谷歌还没有获得应有的重要地位。相比之下，工程师已逐渐接受：任何代码变更，无论多小，都需要测试。测试工具也已成熟、多样，并融入工程工作流的各个环节。文档远未达到同样深入的程度。

To be fair, there’s not necessarily the same need to address documentation as with testing. Tests can be made atomic (unit tests) and can follow prescribed form and function. Documents, for the most part, cannot. Tests can be automated, and schemes to automate documentation are often lacking. Documents are necessarily subjective; the quality of the document is measured not by the writer, but by the reader, and often quite asynchronously. That said, there is a recognition that documentation is important, and processes around document development are improving. In this author’s opinion, the quality of documentation at Google is better than in most software engineering shops.

不过，文档未必需要按测试的方式来处理。测试可以拆成单元测试这样的基本单元，遵循规定的形式和功能，文档大多做不到。测试可以自动化，文档却往往缺少相应的自动化方案。文档难免带有主观性：质量由读者而非作者评判，而且评价通常要在写作完成一段时间后才会出现。尽管如此，文档的重要性已经得到认可，编写文档的流程也在不断改进。在本章作者看来，谷歌的文档质量优于大多数软件工程组织。

To change the quality of engineering documentation, engineers—and the entire engineering organization—need to accept that they are both the problem and the solution. Rather than throw up their hands at the state of documentation, they need to realize that producing quality documentation is part of their job and saves them time and effort in the long run. For any piece of code that you expect to live more than a few months, the extra cycles you put in documenting that code will not only help others, it will help you maintain that code as well.

要改善工程文档质量，工程师乃至整个工程组织都需要承认：问题与自己有关，解决问题也要靠自己。与其面对文档现状无奈摊手，不如认识到，编写高质量文档本就是工作的一部分，长期来看还能节省时间和精力。对于预计使用超过几个月的代码，额外投入精力编写文档，不仅能帮助他人，也能帮助你自己维护代码。

## TL;DRs  内容提要

- Documentation is hugely important over time and scale.
- Documentation changes should leverage the existing developer workflow.
- Keep documents focused on one purpose.
- Write for your audience, not yourself.

- 从时间推移和规模扩展来看，文档至关重要。
- 文档变更应沿用现有的开发者工作流。
- 每份文档只服务一个目的。
- 为受众写作，而不是为自己写。
