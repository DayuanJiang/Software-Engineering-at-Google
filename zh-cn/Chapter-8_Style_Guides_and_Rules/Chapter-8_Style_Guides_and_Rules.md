**CHAPTER 8**

# Style Guides and Rules

# 第八章 风格指南和规则

**Written by Shaindel Schwartz**

**Edited by Tom Manshreck**


Most engineering organizations have rules governing their codebases—rules about where source files are stored, rules about the formatting of the code, rules about naming and patterns and exceptions and threads. Most software engineers are working within the bounds of a set of policies that control how they operate. At Google, to manage our codebase, we maintain a set of style guides that define our rules.

大多数工程组织都有管理代码库的规则，涉及源文件的存放位置、代码格式、命名、模式、异常和线程等。大多数软件工程师都需要在一套规定工作方式的策略约束下开展工作。在谷歌，我们维护了一套风格指南，通过其中的规则来管理代码库。

Rules are laws. They are not just suggestions or recommendations, but strict, mandatory laws. As such, they are universally enforceable—rules may not be disregarded except as approved on a need-to-use basis. In contrast to rules, guidance provides recommendations and best practices. These bits are good to follow, even highly advisable to follow, but unlike rules, they usually have some room for variance.

规则就是法律。它们不只是建议，而是必须严格遵守的要求。因此，规则对所有人都适用；除非确有需要并获得批准，否则不得违背。相比之下，指导提供的是建议和最佳实践。这些做法值得遵循，有些甚至强烈建议遵循，但与规则不同，指导通常留有一定的变通空间。

We collect the rules that we define, the do’s and don’ts of writing code that must be followed, in our programming style guides, which are treated as canon. “Style” might be a bit of a misnomer here, implying a collection limited to formatting practices. Our style guides are more than that; they are the full set of conventions that govern our code. That’s not to say that our style guides are strictly prescriptive; style guide rules may call for judgement, such as the rule to use names that are “as descriptive as possible, within reason.” Rather, our style guides serve as the definitive source for the rules to which our engineers are held accountable.

我们把编写代码时必须遵守的规则，也就是哪些事必须做、哪些事不能做，汇集在编程风格指南中，并将其视为权威准则。这里的“风格”一词可能不太准确，容易让人以为指南只涉及代码格式。实际上，它涵盖了约束代码的全部约定。不过，这并不意味着指南把一切都规定得毫无余地；有些规则仍需运用判断力，例如要求命名“在合理范围内尽可能清楚地描述其含义”。风格指南的作用，是为工程师必须遵守的规则提供权威依据。

We maintain separate style guides for each of the programming languages used at Google [^1].At a high level, all of the guides have similar goals, aiming to steer code development with an eye to sustainability. At the same time, there is a lot of variation among them in scope, length, and content. Programming languages have different strengths, different features, different priorities, and different historical paths to adoption within Google’s ever-evolving repositories of code. It is far more practical, therefore, to independently tailor each language’s guidelines. Some of our style guides are concise, focusing on a few overarching principles like naming and formatting, as demonstrated in our Dart, R, and Shell guides. Other style guides include far more detail, delving into specific language features and stretching into far lengthier documents—notably, our C++, Python, and Java guides. Some style guides put a premium on typical non-Google use of the language—our Go style guide is very short, adding just a few rules to a summary directive to adhere to the practices outlined in the externally recognized conventions. Others include rules that fundamentally differ from external norms; our C++ rules disallow use of exceptions, a language feature widely used outside of Google code.

我们为谷歌使用的每门编程语言分别维护风格指南。总体而言，这些指南的目标相近，都着眼于可持续性来指导代码开发；但它们的范围、篇幅和内容又有很大差异。各门语言的优势、特性和侧重点不同，在谷歌不断演进的代码库中引入和使用的历程也不同。因此，分别为每门语言制定指南更切合实际。有些指南很简洁，只关注命名、格式等少数总体原则，Dart、R 和 Shell 指南便是如此。另一些则详细讨论具体语言特性，篇幅也长得多，尤其是 C++、Python 和 Java 指南。有些指南非常重视谷歌之外的常见用法。例如，Go 风格指南很短，除了要求遵循外部公认惯例这一总原则，只补充了几条规则。也有些规则与外部惯例截然不同：我们的 C++ 规则禁止使用异常，而这一语言特性在谷歌之外的代码中十分常见。

The wide variance among even our own style guides makes it difficult to pin down the precise description of what a style guide should cover. The decisions guiding the development of Google’s style guides stem from the need to keep our codebase sustainable. Other organizations’ codebases will inherently have different requirements for sustainability that necessitate a different set of tailored rules. This chapter discusses the principles and processes that steer the development of our rules and guidance, pulling examples primarily from Google’s C++, Python, and Java style guides.

即使是谷歌内部的风格指南，差异也如此之大，因此很难精确定义风格指南应该涵盖哪些内容。我们制定指南时的各项决策，都源于保持代码库可持续性的需要。其他组织的代码库在这方面自然会有不同要求，需要据此制定自己的规则。本章讨论我们制定规则和指导建议时遵循的原则与流程，主要以谷歌的 C++、Python 和 Java 风格指南为例。

> [^1]: Many of our style guides have external versions, which you can find at https://google.github.io/styleguide. We cite numerous examples from these guides within this chapter.
>
> 1 我们的许多风格指南都有对外公开的版本，可见 https://google.github.io/styleguide。我们在本章中引用了这些指南中的许多例子。

## Why Have Rules?  为什么需要规则？

So why do we have rules? The goal of having rules in place is to encourage “good” behavior and discourage “bad” behavior. The interpretation of “good” and “bad” varies by organization, depending on what the organization cares about. Such designations are not universal preferences; good versus bad is subjective, and tailored to needs. For some organizations, “good” might promote usage patterns that support a small memory footprint or prioritize potential runtime optimizations. In other organizations, “good” might promote choices that exercise new language features. Sometimes, an organization cares most deeply about consistency, so that anything inconsistent with existing patterns is “bad.” We must first recognize what a given organization values; we use rules and guidance to encourage and discourage behavior accordingly.

那么，为什么需要规则？制定规则是为了鼓励“好”的行为，抑制“坏”的行为。如何理解“好”与“坏”，取决于组织重视什么，因此各不相同。这种划分不是普遍适用的偏好，而是主观的、依需求而定的判断。有些组织可能认为，减少内存占用或优先考虑运行时优化潜力的用法才是“好”的；另一些组织则可能鼓励采用新的语言特性。有时，组织最重视一致性，那么一切与现有模式不一致的做法都算“坏”的。我们必须先弄清组织重视什么，再通过规则和指导来鼓励或抑制相应行为。

As an organization grows, the established rules and guidelines shape the common vocabulary of coding. A common vocabulary allows engineers to concentrate on what their code needs to say rather than how they’re saying it. By shaping this vocabulary, engineers will tend to do the “good” things by default, even subconsciously. Rules thus give us broad leverage to nudge common development patterns in desired directions.

随着组织壮大，既定的规则和指导会形成一套共同的编码表达方式，让工程师专注于代码要表达什么，而不是如何表达。建立了这套共同表达方式，工程师就更容易自然而然地、甚至下意识地采用“好”的做法。因此，规则能够在很大范围内发挥作用，引导常见的开发模式朝期望的方向发展。

## Creating the Rules  制定规则

When defining a set of rules, the key question is not, “What rules should we have?” The question to ask is, “What goal are we trying to advance?” When we focus on the goal that the rules will be serving, identifying which rules support this goal makes it easier to distill the set of useful rules. At Google, where the style guide serves as law for coding practices, we do not ask, “What goes into the style guide?” but rather, “Why does something go into the style guide?” What does our organization gain by having a set of rules to regulate writing code?

制定一套规则时，关键不是问“应该有哪些规则”，而是问“想要推进什么目标”。先明确规则服务的目标，再判断哪些规则有助于实现它，就更容易筛选出真正有用的规则。在谷歌，风格指南是编码实践必须遵守的准则，因此我们问的不是“指南里应该放什么”，而是“为什么要把这项内容写进指南”。制定一套规范代码编写的规则，究竟能给组织带来什么？

### Guiding Principles   指导原则

Let’s put things in context: Google’s engineering organization is composed of more than 30,000 engineers. That engineering population exhibits a wild variance in skill and background. About 60,000 submissions are made each day to a codebase of more than two billion lines of code that will likely exist for decades. We’re optimizing for a different set of values than most other organizations need, but to some degree, these concerns are ubiquitous——we need to sustain an engineering environment that is resilient to both scale and time.

先看背景：谷歌的工程组织有3万多名工程师，技能和背景差异很大。每天约有6万次提交进入一个超过20亿行、很可能要存在几十年的代码库。我们优化时看重的因素与大多数组织不同，但这些问题在一定程度上又是共通的：我们都需要维持一个能够适应规模增长、经受时间考验的工程环境。

In this context, the goal of our rules is to manage the complexity of our development environment, keeping the codebase manageable while still allowing engineers to work productively. We are making a trade-off here: the large body of rules that helps us toward this goal does mean we are restricting choice. We lose some flexibility and we might even offend some people, but the gains of consistency and reduced conflict furnished by an authoritative standard win out.

在这种背景下，规则的目标是控制开发环境的复杂性，让代码库保持可管理，同时让工程师能够高效工作。这里存在权衡：为实现目标制定的大量规则，确实限制了选择。我们失去了一些灵活性，甚至可能让一些人不满；但权威标准能带来一致性、减少冲突，这些收益超过了代价。

Given this view, we recognize a number of overarching principles that guide the development of our rules, which must:

- Pull their weight
- Optimize for the reader
- Be consistent
- Avoid error-prone and surprising constructs
- Concede to practicalities when necessary

基于这一认识，我们确立了几项制定规则的总体原则。规则必须：

- 收益抵得上成本
- 为读者优化
- 保持一致
- 避免容易出错或行为出人意料的语言结构
- 必要时为实际需要让步

#### Rules must pull their weight  规则的收益必须抵得上成本 

Not everything should go into a style guide. There is a nonzero cost in asking all of the engineers in an organization to learn and adapt to any new rule that is set. With too many rules [^2] ,not only will it become harder for engineers to remember all relevant rules as they write their code, but it also becomes harder for new engineers to learn their way. More rules also make it more challenging and more expensive to maintain the rule set.

并非所有内容都应该写进风格指南。每增加一条规则，要求组织内所有工程师学习并适应它，都有成本。规则过多，不仅会让工程师在编写代码时难以记住所有相关要求，也会增加新工程师的学习难度。规则越多，维护整套规则也越困难、成本越高。

To this end, we deliberately chose not to include rules expected to be self-evident. Google’s style guide is not intended to be interpreted in a lawyerly fashion; just because something isn’t explicitly outlawed does not imply that it is legal. For example, the C++ style guide has no rule against the use of goto. C++ programmers already tend to avoid it, so including an explicit rule forbidding it would introduce unnecessary overhead. If just one or two engineers are getting something wrong, adding to everyone’s mental load by creating new rules doesn’t scale.

为此，我们有意不写入那些本应不言自明的规则。谷歌的风格指南不应被当作可以逐字钻研、寻找漏洞的法律条文；没有明令禁止，并不意味着允许。例如，C++ 风格指南没有禁止使用 goto 的规则，因为 C++ 程序员通常已经会避免使用它，再明文禁止只会增加不必要的负担。如果只有一两个工程师犯错，却要为此制定新规则、增加所有人的记忆负担，这种做法就无法随组织规模扩展。

> [^2]: Tooling matters here. The measure for “too many” is not the raw number of rules in play, but how many an engineer needs to remember. For example, in the bad-old-days pre-clang-format, we needed to remember a ton of formatting rules. Those rules haven’t gone away, but with our current tooling, the cost of adherence has fallen dramatically. We’ve reached a point at which somebody could add an arbitrary number of formatting rules and nobody would care, because the tool just does it for you.
>
> 2  工具在这里很重要。“规则太多”不是指规则总数太多，而是指工程师需要记住的规则太多。例如，在还没有 clang-format 的日子里，我们得记住大量格式规则。如今这些规则依然存在，但工具已大幅降低了遵守它们的成本。现在，即使再增加任意数量的格式规则，也不会有人在意，因为工具会自动处理。

#### Optimize for the reader   为读者优化

Another principle of our rules is to optimize for the reader of the code rather than the author. Given the passage of time, our code will be read far more frequently than it is written. We’d rather the code be tedious to type than difficult to read. In our Python style guide, when discussing conditional expressions, we recognize that they are shorter than if statements and therefore more convenient for code authors. However, because they tend to be more difficult for readers to understand than the more verbose if statements, we restrict their usage. We value “simple to read” over “simple to write.” We’re making a trade-off here: it can cost more upfront when engineers must repeatedly type potentially longer, descriptive names for variables and types. We choose to pay this cost for the readability it provides for all future readers.

另一项原则是优先考虑代码读者，而不是作者。随着时间推移，代码被阅读的次数会远多于被编写的次数。我们宁愿多敲一些字，也不愿让代码难以阅读。Python 风格指南在讨论条件表达式时承认，它们比 if 语句简短，写起来更方便。但它们往往比篇幅更长的 if 语句更难理解，因此我们限制了其使用。我们更看重“容易读”，而不是“容易写”。这也是一种权衡：工程师需要反复输入更长、更具描述性的变量名和类型名，前期成本可能更高。我们愿意承担这个成本，换取所有未来读者都能受益的可读性。

As part of this prioritization, we also require that engineers leave explicit evidence of intended behavior in their code. We want readers to clearly understand what the code is doing as they read it. For example, our Java, JavaScript, and C++ style guides mandate use of the override annotation or keyword whenever a method overrides a superclass method. Without the explicit in-place evidence of design, readers can likely figure out this intent, though it would take a bit more digging on the part of each reader working through the code.

出于同样的考虑，我们还要求工程师在代码中明确体现预期行为，让读者能够直接看懂代码在做什么。例如，Java、JavaScript 和 C++ 风格指南要求：只要方法重写了超类方法，就必须使用 override 注解或关键字。没有这些就地说明设计意图的标记，读者大概也能推断出来，但每个人都要多花一些时间查证。

Evidence of intended behavior becomes even more important when it might be surprising. In C++, it is sometimes difficult to track the ownership of a pointer just by reading a snippet of code. If a pointer is passed to a function, without being familiar with the behavior of the function, we can’t be sure what to expect. Does the caller still own the pointer? Did the function take ownership? Can I continue using the pointer after the function returns or might it have been deleted? To avoid this problem, our C++ style guide prefers the use of std::unique_ptr when ownership transfer is intended. unique_ptr is a construct that manages pointer ownership, ensuring that only one copy of the pointer ever exists. When a function takes a unique_ptr as an argument and intends to take ownership of the pointer, callers must explicitly invoke move semantics:

如果预期行为可能出人意料，明确体现这种行为就更重要。在 C++ 中，仅凭一段代码，有时很难追踪指针的所有权。把指针传给一个函数时，如果不熟悉函数的行为，就无法确定接下来会怎样：调用方是否仍拥有这个指针？函数是否接管了所有权？函数返回后还能继续使用指针吗，还是它指向的对象可能已经被删除？为避免这类问题，C++ 风格指南建议在需要转移所有权时优先使用 std::unique_ptr。unique_ptr 用于管理指针所有权，确保拥有该所有权的指针只有一个副本。当函数以 unique_ptr 为参数并打算接管所有权时，调用方必须显式使用移动语义：

```C++
// Function that takes a Foo* and may or may not assume ownership of 
// the passed pointer.
void TakeFoo(Foo* arg);
// Calls to the function don’t tell the reader anything about what to 
// expect with regard to ownership after the function returns.
Foo* my_foo(NewFoo());
TakeFoo(my_foo);
```

Compare this to the following:
再与下面的代码比较：

```C++
// Function that takes a std::unique_ptr<Foo>.
void TakeFoo(std::unique_ptr<Foo> arg);
// Any call to the function explicitly shows that ownership is 
// yielded and the unique_ptr cannot be used after the function 
// returns.
std::unique_ptr<Foo> my_foo(FooFactory()); TakeFoo(std::move(my_foo));
```

Given the style guide rule, we guarantee that all call sites will include clear evidence of ownership transfer whenever it applies. With this signal in place, readers of the code don’t need to understand the behavior of every function call. We provide enough information in the API to reason about its interactions. This clear documentation of behavior at the call sites ensures that code snippets remain readable and understandable. We aim for local reasoning, where the goal is clear understanding of what’s happening at the call site without needing to find and reference other code, including the function’s implementation.

有了这条风格指南规则，我们就能保证：凡是涉及所有权转移的调用，都会在调用处明确体现这一点。有了这种标记，读者不必逐一深入了解每个函数的行为，就能凭 API 提供的信息推断交互方式。在调用处清楚地说明行为，可以让代码片段保持易读、易懂。我们的目标是支持局部推理：不必查找函数实现等其他代码，就能清楚地理解调用处发生了什么。

Most style guide rules covering comments are also designed to support this goal of in-place evidence for readers. Documentation comments (the block comments prepended to a given file, class, or function) describe the design or intent of the code that follows. Implementation comments (the comments interspersed throughout the code itself) justify or highlight non-obvious choices, explain tricky bits, and underscore important parts of the code. We have style guide rules covering both types of comments, requiring engineers to provide the explanations another engineer might be looking for when reading through the code.

风格指南中关于注释的大多数规则，也旨在让读者就地获得所需信息。文档注释，也就是文件、类或函数前面的块注释，用来描述后续代码的设计或意图；实现注释则穿插在代码中，说明不直观的选择及其理由，解释难懂的部分，突出重要之处。两类注释都有相应规则，要求工程师写出其他人在阅读代码时可能需要的解释。

#### Be consistent   保持一致性

Our view on consistency within our codebase is similar to the philosophy we apply to our Google offices. With a large, distributed engineering population, teams are frequently split among offices, and Googlers often find themselves traveling to other sites. Although each office maintains its unique personality, embracing local flavor and style, for anything necessary to get work done, things are deliberately kept the same. A visiting Googler’s badge will work with all local badge readers; any Google devices will always get WiFi; the video conferencing setup in any conference room will have the same interface. A Googler doesn’t need to spend time learning how to get this all set up; they know that it will be the same no matter where they are. It’s easy to move between offices and still get work done.

我们对代码库一致性的看法，与管理谷歌办公室的理念相似。工程师人数众多、分布广泛，同一团队经常分散在多个办公地点，员工也常到其他地点出差。每处办公室都保留着自己的个性和当地风格，但完成工作所必需的设施则刻意保持一致：来访员工的工牌可以用于当地所有读卡器，谷歌设备都能接入 WiFi，各会议室的视频会议系统也采用相同界面。员工不必花时间重新学习如何配置这些设施，因为他们知道，无论身在何处，用法都一样。因此，即使换了办公地点，也能轻松继续工作。

That’s what we strive for with our source code. Consistency is what enables any engineer to jump into an unfamiliar part of the codebase and get to work fairly quickly. A local project can have its unique personality, but its tools are the same, its techniques are the same, its libraries are the same, and it all Just Works.

这也是我们在源代码中追求的体验。一致性能让任何工程师进入代码库中不熟悉的部分后，都能较快地开始工作。单个项目可以有自己的个性，但使用的工具、技术和库都相同，一切都能照常运作。

##### Advantages of consistency    一致性的优点

Even though it might feel restrictive for an office to be disallowed from customizing a badge reader or video conferencing interface, the consistency benefits far outweigh the creative freedom we lose. It’s the same with code: being consistent may feel constraining at times, but it means more engineers get more work done with less effort:[^3]

- When a codebase is internally consistent in its style and norms, engineers writing code and others reading it can focus on what’s getting done rather than how it is presented. To a large degree, this consistency allows for expert chunking. [^4]When we solve our problems with the same interfaces and format the code in a consistent way, it’s easier for experts to glance at some code, zero in on what’s important, and understand what it’s doing. It also makes it easier to modularize code and spot duplication. For these reasons, we focus a lot of attention on consistent naming conventions, consistent use of common patterns, and consistent formatting and structure. There are also many rules that put forth a decision on a seemingly small issue solely to guarantee that things are done in only one way.For example, take the choice of the number of spaces to use for indentation or the limit set on line length .[^5] It’s the consistency of having one answer rather than the answer itself that is the valuable part here.
- Consistency enables scaling. Tooling is key for an organization to scale, and consistent code makes it easier to build tools that can understand, edit, and generate code. The full benefits of the tools that depend on uniformity can’t be applied if everyone has little pockets of code that differ—if a tool can keep source files updated by adding missing imports or removing unused includes, if different projects are choosing different sorting strategies for their import lists, the tool might not be able to work everywhere. When everyone is using the same components and when everyone’s code follows the same rules for structure and organization, we can invest in tooling that works everywhere, building in automation for many of our maintenance tasks. If each team needed to separately invest in a bespoke version of the same tool, tailored for their unique environment, we would lose that advantage.
- Consistency helps when scaling the human part of an organization, too. As an organization grows, the number of engineers working on the codebase increases. Keeping the code that everyone is working on as consistent as possible enables better mobility across projects, minimizing the ramp-up time for an engineer switching teams and building in the ability for the organization to flex and adapt as headcount needs fluctuate. A growing organization also means that people in other roles interact with the code—SREs, library engineers, and code janitors, for example. At Google, these roles often span multiple projects, which means engineers unfamiliar with a given team’s project might jump in to work on that project’s code. A consistent experience across the codebase makes this efficient.
- Consistency also ensures resilience to time. As time passes, engineers leave projects, new people join, ownership shifts, and projects merge or split. Striving for a consistent codebase ensures that these transitions are low cost and allows us nearly unconstrained fluidity for both the code and the engineers working on it, simplifying the processes necessary for long-term maintenance.

不允许各办公室自行定制读卡器或视频会议界面，可能让人觉得受限，但一致性带来的好处远远超过失去的创作自由。代码也是如此：保持一致有时会让人感到束缚，却能让更多工程师以更少的投入完成更多工作：  
- 当代码库内部的风格和规范保持一致时，代码作者和读者就能专注于代码的功能，而不是呈现方式。这种一致性在很大程度上有助于专家进行“组块”识别。采用相同接口解决问题，并以一致的方式格式化代码，专家就更容易扫一眼代码、抓住重点，理解它的作用，也更容易将代码模块化并发现重复。因此，我们非常重视命名约定、常见模式用法，以及格式和结构的一致性。还有许多规则，只是对看似微小的问题作出统一规定，确保大家采用同一种做法，例如缩进用几个空格、每行最多多少字符。这里真正有价值的是答案统一，而不是选了哪个答案。
- 一致性有助于规模扩展。工具是组织扩大规模的关键，而代码保持一致，就更容易开发能够理解、编辑和生成代码的工具。如果每个人的代码中都有一些与众不同的部分，依赖一致性的工具就无法充分发挥作用。例如，某个工具能自动补上缺失的导入、移除未使用的包含，但如果各项目对导入列表采用不同的排序方式，它就未必能适用于所有项目。当大家使用相同组件，代码遵循相同的结构和组织规则时，我们就能投入资源开发通用工具，将许多维护任务自动化。如果每个团队都要为自己的特殊环境单独定制同一种工具，这种优势就不存在了。
- 一致性也有助于组织在人员方面扩展。组织壮大后，参与代码库工作的工程师会更多。尽可能保持代码一致，有助于工程师在项目之间流动，缩短转组后的上手时间，也让组织能够随着人员需求变化灵活调整。组织增长还意味着更多不同角色会接触代码，例如 SRE、库工程师和代码清理人员。在谷歌，这些角色的职责常常横跨多个项目，因此不熟悉某个团队项目的工程师，也可能需要修改它的代码。整个代码库提供一致的体验，能让这类工作更高效。
- 一致性也有助于应对时间带来的变化。随着时间推移，工程师会离开项目，新人会加入，负责人会更换，项目也会合并或拆分。努力保持代码库一致，能降低这些转变的成本，让代码和工程师都能较为自由地在项目间流动，从而简化长期维护所需的流程。

> [^3]:  Credit to H. Wright for the real-world comparison, made at the point of having visited around 15 different Google offices.
>
> 3 感谢 H. Wright 提供这个现实类比；他是在走访了约15处谷歌办公室后提出的。
>
> [^4]:  “Chunking” is a cognitive process that groups pieces of information together into meaningful “chunks” rather than keeping note of them individually. Expert chess players, for example, think about configurations of  pieces rather than the positions of the individuals.
>
> 4  “组块”是一种认知过程：把零散信息组合成有意义的整体，而不是逐项记忆。例如，国际象棋高手考虑的是棋子的布局，而不是每个棋子的位置。
>
> [^5]:  See [4.2 Block indentation: +2 spaces, Spaces vs. Tabs, 4.4 Column limit:100 and Line Length](https://oreil.ly/WhufW)
>
> 5 查阅  [4.2 Block indentation: +2 spaces, Spaces vs. Tabs, 4.4 Column limit:100 and Line Length](https://oreil.ly/WhufW)

-----

##### At Scale   规模效应

A few years ago, our C++ style guide promised to almost never change style guide rules that would make old code inconsistent: “In some cases, there might be good arguments for changing certain style rules, but we nonetheless keep things as they are in order to preserve consistency.”

几年前，C++ 风格指南曾承诺，几乎不会修改那些一旦改变就会让旧代码不再符合要求的规则：“有时，修改某些风格规则或许有充分理由，但为了保持一致性，我们仍会维持现状。”

When the codebase was smaller and there were fewer old, dusty corners, that made sense.

当代码库还比较小、鲜少维护的陈旧代码也不多时，这样做是合理的。

When the codebase grew bigger and older, that stopped being a thing to prioritize. This was (for the arbiters behind our C++ style guide, at least) a conscious change: when striking this bit, we were explicitly stating that the C++ codebase would never again be completely consistent, nor were we even aiming for that.

但当代码库越来越大、存在的时间越来越长时，这就不再是优先目标。至少对 C++ 风格指南的裁定者而言，这是一次有意识的转变：删去这条表述时，我们明确表示，C++ 代码库今后不会再完全一致，甚至不再以此为目标。

It would simply be too much of a burden to not only update the rules to current best practices, but to also require that we apply those rules to everything that’s ever been written. Our Large Scale Change tooling and processes allow us to update almost all of our code to follow nearly every new pattern or syntax so that most old code exhibits the most recent approved style (see Chapter 22). Such mechanisms aren’t perfect, however; when the codebase gets as large as it is, we can’t be sure every bit of old code can conform to the new best practices. Requiring perfect consistency has reached the point where there’s too much cost for the value.

如果不仅要让规则跟上当前的最佳实践，还要求所有既有代码都遵守新规则，负担就太重了。借助大规模变更工具和流程，我们可以把几乎所有代码更新为新的模式或语法，让大多数旧代码也采用最新认可的风格（见第22章）。但这些机制并不完美：代码库达到这样的规模，就无法保证每一处旧代码都符合新的最佳实践。追求完全一致的成本，已经超过了它能带来的价值。

-----

**Setting the standard.** When we advocate for consistency, we tend to focus on internal consistency. Sometimes, local conventions spring up before global ones are adopted, and it isn’t reasonable to adjust everything to match. In that case, we advocate a hierarchy of consistency: “Be consistent” starts locally, where the norms within a given file precede those of a given team, which precede those of the larger project, which precede those of the overall codebase. In fact, the style guides contain a number of rules that explicitly defer to local conventions[^6], valuing this local consistency over a scientific technical choice.

**确立标准。** 提倡一致性时，我们通常首先关注内部一致性。有时，在全局约定采用之前，局部约定就已经形成，让所有代码都改为遵循全局约定并不合理。因此，我们提倡按层级保持一致：“保持一致”先从局部开始，文件内的规范优先于团队规范，团队规范优先于项目规范，项目规范又优先于整个代码库的规范。风格指南中有多条规则明确要求遵循局部约定，认为局部一致性比从技术角度选出一个最合理的方案更重要。

However, it is not always enough for an organization to create and stick to a set of internal conventions. Sometimes, the standards adopted by the external community should be taken into account.

不过，仅仅制定并遵守一套内部约定，并不总是足够。有时，组织还需要考虑外部社区采用的标准。

> [^6]: Use of const, for example.
>
> 6 例如，[使用const](https://google.github.io/styleguide/cppguide.html#Use_of_const)的规则。

-----

##### Counting Spaces  缩进用几个空格

The Python style guide at Google initially mandated two-space indents for all of our Python code. The standard Python style guide, used by the external Python community, uses four-space indents. Most of our early Python development was in direct support of our C++ projects, not for actual Python applications. We therefore chose to use two-space indentation to be consistent with our C++ code, which was already formatted in that manner. As time went by, we saw that this rationale didn’t really hold up. Engineers who write Python code read and write other Python code much more often than they read and write C++ code. We were costing our engineers extra effort every time they needed to look something up or reference external code snippets. We were also going through a lot of pain each time we tried to export pieces of our code into open source, spending time reconciling the differences between our internal code and the external world we wanted to join.

谷歌的 Python 风格指南最初要求所有 Python 代码都用两个空格缩进，而外部 Python 社区遵循的标准风格指南采用四个空格。早期，我们的 Python 开发主要是为 C++ 项目提供支持，而不是开发独立的 Python 应用。因此，我们选择两个空格，与已有的 C++ 代码格式保持一致。但随着时间推移，我们发现这个理由站不住脚：编写 Python 的工程师读写其他 Python 代码的频率，远高于读写 C++ 代码。每次查阅资料或参考外部代码片段，他们都得额外花精力适应。每次打算开源部分代码，我们也要费很大力气，处理内部代码与外部社区惯例之间的差异。

When the time came for Starlark (a Python-based language designed at Google to serve as the build description language) to have its own style guide, we chose to change to using four-space indents to be consistent with the outside world.[^7]

后来，需要为 Starlark 制定风格指南时，我们改为采用四个空格缩进，以便与外部社区保持一致。Starlark 是谷歌设计的一种基于 Python 的语言，用作构建描述语言。

-----

If conventions already exist, it is usually a good idea for an organization to be consistent with the outside world. For small, self-contained, and short-lived efforts, it likely won’t make a difference; internal consistency matters more than anything happening outside the project’s limited scope. Once the passage of time and potential scaling become factors, the likelihood of your code interacting with outside projects or even ending up in the outside world increase. Looking long-term, adhering to the widely accepted standard will likely pay off.

如果外部已有通行惯例，组织通常最好与之保持一致。对于规模小、自成一体、生命周期短的项目，这可能无关紧要；内部一致性比项目有限范围之外的事情更重要。但一旦需要考虑时间推移和未来的规模增长，代码就更可能与外部项目交互，甚至最终对外发布。从长远看，遵循广泛接受的标准，很可能值得。

> [^7]: Style formatting for BUILD files implemented with Starlark is applied by buildifier. See https://github.com/ bazelbuild/buildtools.
>
> 7 使用 Starlark 编写的 BUILD 文件由 buildifier 统一格式。参见 https://github.com/ bazelbuild/buildtools。

#### Avoid error-prone and surprising constructs  避免容易出错或行为出人意料的语言结构

Our style guides restrict the use of some of the more surprising, unusual, or tricky constructs in the languages that we use. Complex features often have subtle pitfalls not obvious at first glance. Using these features without thoroughly understanding their complexities makes it easy to misuse them and introduce bugs. Even if a construct is well understood by a project’s engineers, future project members and maintainers are not guaranteed to have the same understanding.

我们的风格指南限制使用一些行为出人意料、不常见或难以掌握的语言结构。复杂特性往往隐藏着不易察觉的陷阱；没有充分理解其复杂之处就使用，很容易因误用而引入缺陷。即使当前项目的工程师很熟悉某种结构，也不能保证未来的成员和维护者同样了解它。

This reasoning is behind our Python style guide ruling to avoid using power features such as reflection. The reflective Python functions hasattr() and getattr() allow a user to access attributes of objects using strings:

这正是 Python 风格指南要求避免使用反射等高级特性的原因。Python 的反射函数 hasattr() 和 getattr() 允许通过字符串访问对象属性：

```python
if hasattr(my_object, 'foo'): 
some_var = getattr(my_object, 'foo')
```

Now, with that example, everything might seem fine. But consider this: some_file.py:

这个例子看上去或许没有问题。但再看看下面的代码：

some_file.py:

```python
A_CONSTANT = [
    'foo',
    'bar',
    'baz',
]
```

other_file.py:

```python
values = []
for field in some_file.A_CONSTANT: 
values.append(getattr(my_object, field))
```

When searching through code, how do you know that the fields foo, bar, and baz are being accessed here? There’s no clear evidence left for the reader. You don’t easily see and therefore can’t easily validate which strings are used to access attributes of your object. What if, instead of reading those values from A_CONSTANT, we read them from a Remote Procedure Call (RPC) request message or from a data store? Such obfuscated code could cause a major security flaw, one that would be very difficult to notice, simply by validating the message incorrectly. It’s also difficult to test and verify such code.

搜索代码时，怎么知道这里访问了 foo、bar 和 baz 字段？代码没有为读者留下明确线索。很难看出哪些字符串被用来访问对象属性，也就很难验证这些访问。如果这些值不是来自 A_CONSTANT，而是来自远程过程调用（Remote Procedure Call, RPC）的请求消息或数据存储，又会怎样？这种含义不明的代码，只要消息校验有误，就可能造成严重且难以察觉的安全漏洞。测试和验证这类代码也很困难。

Python’s dynamic nature allows such behavior, and in very limited circumstances, using hasattr() and getattr() is valid. In most cases, however, they just cause obfuscation and introduce bugs.

Python 的动态特性允许这种行为，在极少数情况下，使用 hasattr() 和 getattr() 也确实合理。但在大多数情况下，它们只会让代码含义更不清楚，并引入缺陷。

Although these advanced language features might perfectly solve a problem for an expert who knows how to leverage them, power features are often more difficult to understand and are not very widely used. We need all of our engineers able to operate in the codebase, not just the experts. It’s not just support for the novice software engineer, but it’s also a better environment for SREs—if an SRE is debugging a production outage, they will jump into any bit of suspect code, even code written in a language in which they are not fluent. We place higher value on simplified, straightforward code that is easier to understand and maintain.

对于懂得如何运用这些高级语言特性的专家，它们也许能完美解决某个问题；但这些特性往往更难理解，使用也不广泛。我们需要所有工程师都能在代码库中工作，而不只是专家。这样不仅有助于新手，也能改善 SRE 的工作环境：排查生产故障时，SRE 可能需要检查任何可疑代码，即使它是用自己不熟悉的语言编写的。我们更看重简单直接、容易理解和维护的代码。

#### Concede to practicalities  为实际需要让步

In the words of Ralph Waldo Emerson: “A foolish consistency is the hobgoblin of little minds.” In our quest for a consistent, simplified codebase, we do not want to blindly ignore all else. We know that some of the rules in our style guides will encounter cases that warrant exceptions, and that’s OK. When necessary, we permit concessions to optimizations and practicalities that might otherwise conflict with our rules.

用拉尔夫·沃尔多·爱默生的话说：“愚蠢地追求一致，是心胸狭隘者的执念。”（原译补充：为渺小的政治家、哲学家和神学家所崇拜。一个伟大的灵魂与一致性毫无关系。）追求一致、简单的代码库，并不意味着忽略其他一切。我们知道，有些规则会遇到需要例外处理的情况，这没有问题。必要时，即使优化或实际需要与规则冲突，我们也允许让步。

Performance matters. Sometimes, even if it means sacrificing consistency or readability, it just makes sense to accommodate performance optimizations. For example, although our C++ style guide prohibits use of exceptions, it includes a rule that allows the use of noexcept, an exception-related language specifier that can trigger compiler optimizations.

性能很重要。有时，为性能优化作出让步是合理的，即使这意味着牺牲一致性或可读性。例如，C++ 风格指南虽然禁止使用异常，却允许使用 noexcept；这是一个与异常相关的语言说明符，能够触发编译器优化。

Interoperability also matters. Code that is designed to work with specific non-Google pieces might do better if tailored for its target. For example, our C++ style guide includes an exception to the general CamelCase naming guideline that permits use of the standard library’s snake_case style for entities that mimic standard library features.[^8] The C++ style guide also allows exemptions for Windows programming, where compatibility with platform features requires multiple inheritance, something explicitly forbidden for all other C++ code. Both our Java and JavaScript style guides explicitly state that generated code, which frequently interfaces with or depends on components outside of a project’s ownership, is out of scope for the guide’s rules.[^9] Consistency is vital; adaptation is key.

互操作性同样重要。如果代码要与谷歌之外的特定组件配合，针对这些组件作适当调整，效果可能更好。例如，C++ 风格指南为通常采用的 CamelCase 命名规则留了一个例外：模仿标准库功能的实体，可以采用标准库的 snake_case 风格。Windows 编程也有豁免，因为兼容平台特性需要使用多重继承，而其他 C++ 代码都被明确禁止这样做。Java 和 JavaScript 风格指南还明确规定，自动生成的代码不受指南规则约束；这类代码经常需要与项目控制范围之外的组件交互，或依赖这些组件。一致性很重要，适应实际情况也很关键。

> [^8]: See [Exceptions to Naming Rules](https://google.github.io/styleguide/cppguide.html#Exceptions_to_Naming_Rules). As an example, our open sourced Abseil libraries use snake_case naming for types intended to be replacements for standard types. See the types defined in https://github.com/abseil/abseilcpp/blob/master/absl/utility/utility.h. These are C++11 implementation of C++14 standard types and therefore use the standard’s favored snake_case style instead of Google’s preferred CamelCase form.
>
> 8 参见命名规则的例外。例如，开源 Abseil 库中用于替代标准类型的类型采用 snake_case 命名，可见 https://github.com/abseil/abseilcpp/blob/master/absl/utility/utility.h 中的定义。这些类型用 C++11 实现了 C++14 的标准类型，因此沿用标准偏好的 snake_case 风格，而不是谷歌偏好的 CamelCase。
>
> [^9};  See [Generated code: mostly exempt](https://google.github.io/styleguide/jsguide.html#policies-generated-code-mostly-exempt).
>
> 9 参见[生成的代码：大多豁免](https://google.github.io/styleguide/jsguide.html#policies-generated-code-mostly-exempt)。

### The Style Guide  风格指南

So, what does go into a language style guide? There are roughly three categories into which all style guide rules fall:

- Rules to avoid dangers
- Rules to enforce best practices
- Rules to ensure consistency

那么，语言风格指南究竟包含哪些内容？所有规则大致可以分为三类：

- 规避危险的规则
- 要求遵循最佳实践的规则
- 确保一致性的规则

#### Avoiding danger  规避危险

First and foremost, our style guides include rules about language features that either must or must not be done for technical reasons. We have rules about how to use static members and variables; rules about using lambda expressions; rules about handling exceptions; rules about building for threading, access control, and class inheritance. We cover which language features to use and which constructs to avoid. We call out standard vocabulary types that may be used and for what purposes. We specifically include rulings on the hard-to-use and the hard-to-use-correctly—some language features have nuanced usage patterns that might not be intuitive or easy to apply properly, causing subtle bugs to creep in. For each ruling in the guide, we aim to include the pros and cons that were weighed with an explanation of the decision that was reached. Most of these decisions are based on the need for resilience to time, supporting and encouraging maintainable language usage.

首先，风格指南会从技术角度规定，使用语言特性时哪些事必须做、哪些事禁止做。这些规则涉及静态成员和变量、lambda 表达式、异常处理，以及线程、访问控制和类继承等。我们说明应该使用哪些特性、避免哪些语言结构，也列出允许使用的标准词汇类型及其用途。对于难用、尤其是难以正确使用的特性，我们会专门作出规定：有些特性的用法细节复杂，不够直观，难以正确运用，容易悄悄引入缺陷。我们希望每条规则都能说明曾权衡过的利弊，以及最终决策的理由。大多数决策都着眼于长期维护，支持和鼓励采用可维护的语言用法。

#### Enforcing best practices 要求遵循最佳实践

Our style guides also include rules enforcing some best practices of writing source code. These rules help keep the codebase healthy and maintainable. For example, we specify where and how code authors must include comments.[^10] Our rules for comments cover general conventions for commenting and extend to include specific cases that must include in-code documentation—cases in which intent is not always obvious, such as fall-through in switch statements, empty exception catch blocks, and template metaprogramming. We also have rules detailing the structuring of source files, outlining the organization of expected content. We have rules about naming: naming of packages, of classes, of functions, of variables. All of these rules are intended to guide engineers to practices that support healthier, more sustainable code.

风格指南还通过规则要求遵循一些源代码编写的最佳实践，以保持代码库的健康和可维护性。例如，我们规定代码作者必须在什么地方、以什么方式添加注释。除了注释的一般约定，规则还列出了必须在代码中加以说明的情况，尤其是意图不够明显的地方，例如 switch 语句中的贯穿执行、空的异常捕获块，以及模板元编程。我们也详细规定源文件的结构，说明各项内容应如何组织，并规定包、类、函数和变量的命名方式。这些规则都是为了引导工程师采用有助于代码健康和可持续维护的实践。

Some of the best practices enforced by our style guides are designed to make source code more readable. Many formatting rules fall under this category. Our style guides specify when and how to use vertical and horizontal whitespace in order to improve readability. They also cover line length limits and brace alignment. For some languages, we cover formatting requirements by deferring to autoformatting tools— gofmt for Go, dartfmt for Dart. Itemizing a detailed list of formatting requirements or naming a tool that must be applied, the goal is the same: we have a consistent set of formatting rules designed to improve readability that we apply to all of our code.

风格指南要求遵循的某些最佳实践，旨在提高源代码的可读性，许多格式规则就属于这一类。指南规定了何时以及如何使用空行和水平空白，也规定了行长限制和大括号对齐方式。对于某些语言，我们把格式要求交给自动格式化工具处理，例如 Go 的 gofmt 和 Dart 的 dartfmt。无论逐项列出格式要求，还是指定必须使用的工具，目标都相同：把一套有助于阅读的统一格式规则应用于所有代码。

Our style guides also include limitations on new and not-yet-well-understood language features. The goal is to preemptively install safety fences around a feature’s potential pitfalls while we all go through the learning process. At the same time, before everyone takes off running, limiting use gives us a chance to watch the usage patterns that develop and extract best practices from the examples we observe. For these new features, at the outset, we are sometimes not sure of the proper guidance to give. As adoption spreads, engineers wanting to use the new features in different ways discuss their examples with the style guide owners, asking for allowances to permit additional use cases beyond those covered by the initial restrictions. Watching the waiver requests that come in, we get a sense of how the feature is getting used and eventually collect enough examples to generalize good practice from bad. After we have that information, we can circle back to the restrictive ruling and amend it to allow wider use.

风格指南也会限制使用新出现、尚未被充分理解的语言特性。在大家仍在学习时，先为潜在陷阱设置防护，可以降低风险。同时，在全面采用之前限制使用，也让我们有机会观察逐渐形成的使用模式，并从实际案例中提炼最佳实践。对于新特性，我们起初有时也不确定该给出什么指导。随着使用范围扩大，工程师若想尝试最初限制之外的用法，就会带着实例与指南负责人讨论，申请豁免。观察这些请求，能帮助我们了解特性的实际用法，逐渐积累足够的案例，区分好的实践与不好的实践。有了这些信息，就能重新审视原先的限制，修改规则，允许更广泛的使用。

> [^10]: See `https://google.github.io/styleguide/cppguide.html#Comments`, `http://google.github.io/styleguide/pyguide#38-comments-and-docstrings`, and `https://google.github.io/styleguide/javaguide.html#s7-javadoc`, where multiple languages define general comment rules.
>
> 10 参见 `https://google.github.io/styleguide/cppguide.html#Comments`、`http://google.github.io/styleguide/pyguide#38-comments-and-docstrings`，以及 `https://google.github.io/styleguide/javaguide.html#s7-javadoc`, where multiple languages define general comment rules. 这些指南分别规定了多种语言的通用注释规则。

---

#### Case Study: Introducing std::unique_ptr  案例分析：引入 std::unique_ptr

When C++11 introduced std::unique_ptr, a smart pointer type that expresses exclusive ownership of a dynamically allocated object and deletes the object when the unique_ptr goes out of scope, our style guide initially disallowed usage. The behavior of the unique_ptr was unfamiliar to most engineers, and the related move semantics that the language introduced were very new and, to most engineers, very confusing. Preventing the introduction of std::unique_ptr in the codebase seemed the safer choice. We updated our tooling to catch references to the disallowed type and kept our existing guidance recommending other types of existing smart pointers.

C++11 引入了 std::unique_ptr。这种智能指针表示对动态分配对象的独占所有权，并在 unique_ptr 离开作用域时删除对象。我们的风格指南最初禁止使用它：大多数工程师不熟悉它的行为，而语言同时引入的相关移动语义也很新，令许多人困惑。因此，先不让 std::unique_ptr 进入代码库，似乎是更安全的选择。我们更新了工具，以检测对这一禁用类型的引用，同时继续建议使用已有的其他智能指针类型。

Time passed. Engineers had a chance to adjust to the implications of move semantics and we became increasingly convinced that using std::unique_ptr was directly in line with the goals of our style guidance. The information regarding object ownership that a std::unique_ptr facilitates at a function call site makes it far easier for a reader to understand that code. The added complexity of introducing this new type, and the novel move semantics that come with it, was still a strong concern, but the significant improvement in the long-term overall state of the codebase made the adoption of std::unique_ptr a worthwhile trade-off.

随着时间推移，工程师逐渐有机会理解并适应移动语义的影响，我们也越来越确信，使用 std::unique_ptr 符合风格指南的目标。它在函数调用处提供的对象所有权信息，能大幅降低读者理解代码的难度。引入这种新类型及其附带的移动语义所增加的复杂性，仍是重要顾虑；但从长期看，它能显著改善代码库的整体状况，因此采用 std::unique_ptr 是值得的取舍。

---

#### Building in consistency  确保一致性

Our style guides also contain rules that cover a lot of the smaller stuff. For these rules, we make and document a decision primarily to make and document a decision. Many rules in this category don’t have significant technical impact. Things like naming conventions, indentation spacing, import ordering: there is usually no clear, measurable, technical benefit for one form over another, which might be why the technical community tends to keep debating them.[^11] By choosing one, we’ve dropped out of the endless debate cycle and can just move on. Our engineers no longer spend time discussing two spaces versus four. The important bit for this category of rules is not what we’ve chosen for a given rule so much as the fact that we have chosen.

风格指南中还有许多处理细节的规则。制定这些规则，主要就是为了作出决定，并把决定记录下来。其中很多选择并没有显著的技术影响，例如命名约定、缩进空格数、导入顺序：某种形式通常并不比另一种形式具有明确、可衡量的技术优势，也许正因如此，技术社区才会争论不休。一旦选定一种做法，我们就能结束无休止的争论，继续工作。工程师不再需要花时间讨论缩进该用两个还是四个空格。对这类规则而言，重要的不是选了什么，而是已经作出了选择。

> 11 Such discussions are really just bikeshedding, an illustration of Parkinson’s law of triviality.
>
> 11 这类讨论其实只是围绕琐事争论不休，也就是“自行车棚效应”，体现了帕金森琐碎定律。

#### And for everything else...   至于其他的一切……

With all that, there’s a lot that’s not in our style guides. We try to focus on the things that have the greatest impact on the health of our codebase. There are absolutely best practices left unspecified by these documents, including many fundamental pieces of good engineering advice: don’t be clever, don’t fork the codebase, don’t reinvent the wheel, and so on. Documents like our style guides can’t serve to take a complete novice all the way to a master-level understanding of software engineering—there are some things we assume, and this is intentional.

即便如此，风格指南仍有很多内容未作规定。我们尽量把注意力放在对代码库健康影响最大的事项上，因此必然会有一些最佳实践未被写入，包括许多基本的工程建议：不要自作聪明，不要创建代码库的分叉，不要重复造轮子，等等。风格指南这样的文档，无法让一个完全的新手一路成长为精通软件工程的大师。有些知识，我们有意假定读者已经掌握。

## Changing the Rules  修改规则

Our style guides aren’t static. As with most things, given the passage of time, the landscape within which a style guide decision was made and the factors that guided a given ruling are likely to change. Sometimes, conditions change enough to warrant reevaluation. If a new language version is released, we might want to update our rules to allow or exclude new features and idioms. If a rule is causing engineers to invest effort to circumvent it, we might need to reexamine the benefits the rule was supposed to provide. If the tools that we use to enforce a rule become overly complex and burdensome to maintain, the rule itself might have decayed and need to be revisited. Noticing when a rule is ready for another look is an important part of the process that keeps our rule set relevant and up to date.

风格指南并非一成不变。随着时间推移，当初制定规则的环境和依据都可能改变；有时，变化大到足以让我们重新评估规则。语言发布新版本时，可能需要更新规则，明确允许或禁止哪些新特性和惯用法。如果工程师为了绕过某条规则付出很多精力，就可能需要重新审视它本应带来的收益。如果执行规则的工具变得过于复杂、难以维护，也可能说明规则本身已经过时，需要重审。及时发现哪些规则值得重新评估，是让整套规则始终切合实际、跟上变化的重要环节。

The decisions behind rules captured in our style guides are backed by evidence. When adding a rule, we spend time discussing and analyzing the relevant pros and cons as well as the potential consequences, trying to verify that a given change is appropriate for the scale at which Google operates. Most entries in Google’s style guides include these considerations, laying out the pros and cons that were weighed during the process and giving the reasoning for the final ruling. Ideally, we prioritize this detailed reasoning and include it with every rule.

风格指南中的规则都有证据作为决策依据。增加规则时，我们会讨论、分析利弊和潜在后果，尽量确认这项变更是否适合谷歌的运作规模。指南的大多数条目都记录了这些考量，列出权衡过的利弊，并说明最终决定的理由。理想情况下，我们应优先保证每条规则都附有这样的详细论证。

Documenting the reasoning behind a given decision gives us the advantage of being able to recognize when things need to change. Given the passage of time and changing conditions, a good decision made previously might not be the best current one. With influencing factors clearly noted, we are able to identify when changes related to one or more of these factors warrant reevaluating the rule.

记录决策理由，有助于判断何时需要改变。随着时间推移、条件变化，过去的好决定未必仍是现在的最佳选择。明确记录影响决策的因素，就能在其中一个或多个因素发生变化时，判断是否需要重新评估规则。

---

#### Case Study:CamelCase Naming 案例分析：驼峰命名法

At Google, when we defined our initial style guidance for Python code, we chose to use CamelCase naming style instead of snake_case naming style for method names. Although the public Python style guide (PEP 8) and most of the Python community used snake_case naming, most of Google’s Python usage at the time was for C++ developers using Python as a scripting layer on top of a C++ codebase. Many of the defined Python types were wrappers for corresponding C++ types, and because Google’s C++ naming conventions follow CamelCase style, the cross-language consistency was seen as key.

最初为 Python 代码制定风格指南时，谷歌选择用 CamelCase 而不是 snake_case 为方法命名。公开的 Python 风格指南（PEP 8）和 Python 社区的大多数开发者都采用 snake_case，但当时谷歌主要由 C++ 开发者使用 Python，为 C++ 代码库编写上层脚本。许多 Python 类型都是对应 C++ 类型的封装，而谷歌的 C++ 命名约定采用 CamelCase，因此跨语言的一致性被视为关键。

Later, we reached a point at which we were building and supporting independent Python applications. The engineers most frequently using Python were Python engineers developing Python projects, not C++ engineers pulling together a quick script. We were causing a degree of awkwardness and readability problems for our Python engineers, requiring them to maintain one standard for our internal code but constantly adjust for another standard every time they referenced external code. We were also making it more difficult for new hires who came in with Python experience to adapt to our codebase norms.

后来，我们开始开发和维护独立的 Python 应用。最常使用 Python 的，变成了开发 Python 项目的 Python 工程师，而不是临时写个脚本的 C++ 工程师。原有规则给他们带来了不便和阅读障碍：内部代码要遵循一套标准，每次参考外部代码又得适应另一套标准。已有 Python 经验的新员工，也因此更难适应代码库的规范。

As our Python projects grew, our code more frequently interacted with external Python projects. We were incorporating third-party Python libraries for some of our projects, leading to a mix within our codebase of our own CamelCase format with the externally preferred snake_case style. As we started to open source some of our Python projects, maintaining them in an external world where our conventions were nonconformist added both complexity on our part and wariness from a community that found our style surprising and somewhat weird.

随着 Python 项目增长，我们的代码与外部 Python 项目的交互越来越频繁。一些项目引入第三方 Python 库后，代码库中便混用了内部的 CamelCase 和外部惯用的 snake_case。后来，我们开始开源部分 Python 项目，而自己的约定与外部惯例格格不入。这不仅增加了我们在外部维护项目的复杂性，也让社区有所顾虑，因为他们觉得这种风格出人意料，甚至有些古怪。

Presented with these arguments, after discussing both the costs (losing consistency with other Google code, reeducation for Googlers used to our Python style) and benefits (gaining consistency with most other Python code, allowing what was already leaking in with third-party libraries), the style arbiters for the Python style guide decided to change the rule. With the restriction that it be applied as a file-wide choice, an exemption for existing code, and the latitude for projects to decide what is best for them, the Google Python style guide was updated to permit snake_case naming.

面对这些理由，Python 风格指南的仲裁者讨论了改变规则的成本与收益。成本包括失去与谷歌其他代码的一致性，以及让习惯了原有风格的员工重新学习；收益则包括与大多数外部 Python 代码保持一致，并正式允许那些已随第三方库进入代码库的用法。最终，仲裁者决定修改规则，允许使用 snake_case，但要求同一文件内采用统一的命名风格，既有代码可以豁免，各项目也可自行判断怎样选择最合适。

---

### The Process  流程

Recognizing that things will need to change, given the long lifetime and ability to scale that we are aiming for, we created a process for updating our rules. The process for changing our style guide is solution based. Proposals for style guide updates are framed with this view, identifying an existing problem and presenting the proposed change as a way to fix it. “Problems,” in this process, are not hypothetical examples of things that could go wrong; problems are proven with patterns found in existing Google code. Given a demonstrated problem, because we have the detailed reasoning behind the existing style guide decision, we can reevaluate, checking whether a different conclusion now makes more sense.

我们追求长期存续和可扩展性，也认识到规则终究需要改变，因此建立了更新规则的流程。这套流程以解决问题为出发点：更新提案需要指出现有问题，并说明建议的变更如何解决它。这里的“问题”不是假想中可能出错的例子，而是谷歌现有代码中反复出现、有据可查的情况。问题得到证实后，我们就能依据原有决策的详细理由重新评估，判断现在是否应得出不同结论。

The community of engineers writing code governed by the style guide are often best positioned to notice when a rule might need to be changed. Indeed, here at Google, most changes to our style guides begin with community discussion. Any engineer can ask questions or propose a change, usually by starting with the language-specific mailing lists dedicated to style guide discussions.

按风格指南编写代码的工程师，往往最容易发现哪些规则可能需要修改。事实上，谷歌的大多数风格指南变更都始于社区讨论。任何工程师都可以提问或提出修改建议，通常会先在相应语言专门讨论风格指南的邮件列表中发起讨论。

Proposals for style guide changes might come fully-formed, with specific, updated wording suggested, or might start as vague questions about the applicability of a given rule. Incoming ideas are discussed by the community, receiving feedback from other language users. Some proposals are rejected by community consensus, gauged to be unnecessary, too ambiguous, or not beneficial. Others receive positive feedback, gauged to have merit either as-is or with some suggested refinement. These proposals, the ones that make it through community review, are subject to final decision- making approval.

修改建议可能已经很完整，连新的具体措辞都已拟好；也可能只是一个尚不明确的问题，询问某条规则是否适用。社区会讨论这些想法，由同样使用该语言的其他工程师提供反馈。对于有些提案，社区形成共识，认为没有必要、过于含糊或没有益处，因此予以否决；另一些则获得积极反馈，被认为可以直接采用，或稍作完善后采用。通过社区审查的提案，还需要交由最终决策者批准。

### The Style Arbiters  风格仲裁者

At Google, for each language’s style guide, final decisions and approvals are made by the style guide’s owners—our style arbiters. For each programming language, a group of long-time language experts are the owners of the style guide and the designated decision makers. The style arbiters for a given language are often senior members of the language’s library team and other long-time Googlers with relevant language experience.

在谷歌，每门语言的风格指南都由其负责人，也就是风格仲裁者，作出最终决定并批准变更。每门语言都有一组长期研究和使用该语言的专家，负责指南并承担决策职责。他们通常包括该语言库团队的资深成员，以及其他在谷歌工作多年、具有相关语言经验的工程师。

The actual decision making for any style guide change is a discussion of the engineering trade-offs for the proposed modification. The arbiters make decisions within the context of the agreed-upon goals for which the style guide optimizes. Changes are not made according to personal preference; they’re trade-off judgments. In fact, the C++ style arbiter group currently consists of four members. This might seem strange: having an odd number of committee members would prevent tied votes in case of a split decision. However, because of the nature of the decision making approach, where nothing is “because I think it should be this way” and everything is an evaluation of trade-off, decisions are made by consensus rather than by voting. The four-member group is happily functional as-is.

任何风格指南变更的决策，实质上都是讨论提案涉及的工程权衡。仲裁者以共同认可的指南目标为依据，而不是按个人偏好作决定。事实上，C++ 风格仲裁组目前有四名成员。这似乎有些奇怪：成员人数为奇数，才能避免意见分歧时票数打平。但我们的决策不是“因为我觉得应该这样”，而是对利弊的评估，所以靠共识而不是投票作决定。四人小组照样运作良好。

### Exceptions   例外

Yes, our rules are law, but yes, some rules warrant exceptions. Our rules are typically designed for the greater, general case. Sometimes, specific situations would benefit from an exemption to a particular rule. When such a scenario arises, the style arbiters are consulted to determine whether there is a valid case for granting a waiver to a particular rule.

没错，规则就是法律，但有些规则确实需要例外。规则通常面向广泛的一般情况，而某些特殊场景下，豁免某条规则可能更有益。这时，需要请风格仲裁者判断理由是否充分，能否批准豁免。

Waivers are not granted lightly. In C++ code, if a macro API is introduced, the style guide mandates that it be named using a project-specific prefix. Because of the way C++ handles macros, treating them as members of the global namespace, all macros that are exported from header files must have globally unique names to prevent collisions. The style guide rule regarding macro naming does allow for arbiter-granted exemptions for some utility macros that are genuinely global. However, when the reason behind a waiver request asking to exclude a project-specific prefix comes down to preferences due to macro name length or project consistency, the waiver is rejected. The integrity of the codebase outweighs the consistency of the project here.

豁免不会轻易获批。C++ 风格指南规定，引入宏 API 时，名称必须带有项目专属前缀。C++ 中的宏在全局范围内起作用，因此从头文件导出的所有宏都必须全局唯一，以免发生命名冲突。宏命名规则允许仲裁者为某些真正具有全局用途的实用宏批准豁免。但如果申请省略项目前缀，只是嫌宏名太长，或希望与项目内部命名保持一致，就会被拒绝。在这里，代码库整体不受破坏，比单个项目保持一致更重要。

Exceptions are allowed for cases in which it is gauged to be more beneficial to permit the rule-breaking than to avoid it. The C++ style guide disallows implicit type conversions, including single-argument constructors. However, for types that are designed to transparently wrap other types, where the underlying data is still accurately and precisely represented, it’s perfectly reasonable to allow implicit conversion. In such cases, waivers to the no-implicit-conversion rule are granted. Having such a clear case for valid exemptions might indicate that the rule in question needs to be clarified or amended. However, for this specific rule, enough waiver requests are received that appear to fit the valid case for exemption but in fact do not—either because the specific type in question is not actually a transparent wrapper type or because the type is a wrapper but is not actually needed—that keeping the rule in place as-is is still worthwhile.

如果判断打破规则比遵守规则更有益，就可以允许例外。C++ 风格指南禁止隐式类型转换，也包括通过单参数构造函数进行的隐式转换。但如果某个类型只是对其他类型作透明封装，底层数据仍能得到准确、精确的表示，允许隐式转换就完全合理。这类情况可以获得豁免。存在如此明确的合理例外，也许说明规则需要澄清或修改。不过，对这条规则而言，我们收到过足够多看似符合条件、实际并不符合的申请：有些类型并非透明封装，有些虽是封装，却根本没有必要。因此，保留原规则仍然值得。

## Guidance  指导

In addition to rules, we curate programming guidance in various forms, ranging from long, in-depth discussion of complex topics to short, pointed advice on best practices that we endorse.

除了规则，我们还整理了多种形式的编程指导，既有对复杂主题的长篇深入讨论，也有针对所认可最佳实践的简短建议。

Guidance represents the collected wisdom of our engineering experience, documenting the best practices that we’ve extracted from the lessons learned along the way. Guidance tends to focus on things that we’ve observed people frequently getting wrong or new things that are unfamiliar and therefore subject to confusion. If the rules are the “musts,” our guidance is the “shoulds.”

指导汇集了工程经验中积累的智慧，记录了从实践教训中提炼的最佳实践。它通常关注人们经常犯错的地方，或尚不熟悉、容易产生困惑的新事物。如果说规则规定的是“必须”，那么指导说明的就是“应该”。

One example of a pool of guidance that we cultivate is a set of primers for some of the predominant languages that we use. While our style guides are prescriptive, ruling on which language features are allowed and which are disallowed, the primers are descriptive, explaining the features that the guides endorse. They are quite broad in their coverage, touching on nearly every topic that an engineer new to the language’s use at Google would need to reference. They do not delve into every detail of a given topic, but they provide explanations and recommended use. When an engineer needs to figure out how to apply a feature that they want to use, the primers aim to serve as the go-to guiding reference.

我们为一些主要语言编写的入门指南，就是这类指导资料的例子。风格指南具有规范性，规定哪些特性允许使用、哪些不允许；入门指南则重在解释，说明那些受到认可的特性。它们覆盖面很广，几乎涉及初次在谷歌使用这门语言的工程师可能需要查阅的所有主题。虽然不会深究每个细节，但会解释相关特性，并推荐用法。工程师想弄清某项特性该如何使用时，可以优先查阅这些入门指南。

A few years ago, we began publishing a series of C++ tips that offered a mix of general language advice and Google-specific tips. We cover hard things—object lifetime, copy and move semantics, argument-dependent lookup; new things—C++ 11 features as they were adopted in the codebase, preadopted C++17 types like string_view, optional, and variant; and things that needed a gentle nudge of correction—reminders not to use using directives, warnings to remember to look out for implicit bool conversions. The tips grow out of actual problems encountered, addressing real programming issues that are not covered by the style guides. Their advice, unlike the rules in the style guide, are not true canon; they are still in the category of advice rather than rule. However, given the way they grow from observed patterns rather than abstract ideals, their broad and direct applicability set them apart from most other advice as a sort of “canon of the common.” Tips are narrowly focused and relatively short, each one no more than a few minutes’ read. This “Tip of the Week” series has been extremely successful internally, with frequent citations during code reviews and technical discussions.[^12]

几年前，我们开始发布一系列 C++ 技巧，既有通用的语言建议，也有谷歌特有的做法。内容包括难点，如对象生命周期、复制与移动语义、实参依赖查找；新特性，如逐步引入代码库的 C++11 特性，以及提前采用的 string_view、optional、variant 等 C++17 类型；还有需要适时提醒的事项，例如不要使用 using 指令，留意隐式 bool 转换。这些技巧来自实际遇到的问题，处理的是风格指南未涵盖的编程问题。它们与指南中的规则不同，不是必须遵守的权威准则，仍属于建议。不过，由于源于观察到的实际模式，而不是抽象理想，它们具有广泛、直接的适用性，因此又有别于大多数建议，可以说是“常见实践的准则”。每篇技巧都聚焦一个小主题，篇幅较短，几分钟便能读完。这个“每周技巧”系列在内部非常成功，代码审查和技术讨论中经常引用。

Software engineers come in to a new project or codebase with knowledge of the programming language they are going to be using, but lacking the knowledge of how the programming language is used within Google. To bridge this gap, we maintain a series of “<Language>@Google 101” courses for each of the primary programming languages in use. These full-day courses focus on what makes development with that language different in our codebase. They cover the most frequently used libraries and idioms, in-house preferences, and custom tool usage. For a C++ engineer who has just become a Google C++ engineer, the course fills in the missing pieces that make them not just a good engineer, but a good Google codebase engineer.

软件工程师加入新项目或代码库时，已经熟悉将使用的编程语言，却不了解它在谷歌内部的用法。为弥补这一差距，我们为每门主要语言开设了“<语言>@Google 101”系列课程。课程为期一天，重点介绍在谷歌代码库中使用这门语言开发时有哪些不同，涵盖最常用的库和惯用法、内部偏好的做法，以及定制工具的使用。对于刚加入谷歌的 C++ 工程师，这门课可以补齐相关知识，让他不仅是优秀的工程师，也能在谷歌代码库中出色地工作。

In addition to teaching courses that aim to get someone completely unfamiliar with our setup up and running quickly, we also cultivate ready references for engineers deep in the codebase to find the information that could help them on the go. These references vary in form and span the languages that we use. Some of the useful references that we maintain internally include the following:

- Language-specific advice for the areas that are generally more difficult to get correct (such as concurrency and hashing).
- Detailed breakdowns of new features that are introduced with a language update and advice on how to use them within the codebase.
- Listings of key abstractions and data structures provided by our libraries. This keeps us from reinventing structures that already exist and provides a response to, “I need a thing, but I don’t know what it’s called in our libraries.”

除了通过课程帮助不熟悉谷歌开发环境的工程师快速上手，我们也整理了便于随时查阅的参考资料，供已经深入代码库工作的工程师按需使用。这些资料形式多样，涵盖我们使用的各门语言。内部维护的实用参考资料包括：

- 针对并发、哈希等通常难以正确处理的领域，提供各门语言的具体建议。
- 详细介绍语言更新带来的新特性，并建议如何在代码库中使用。
- 列出内部库提供的关键抽象和数据结构，避免重复实现已有结构，也帮助工程师回答：“我需要这样一个东西，却不知道它在我们的库里叫什么。”

> 12 https://abseil.io/tips has a selection of some of our most popular tips.
>
> 12 https://abseil.io/tips 收录了部分最受欢迎的技巧。

## Applying the Rules  应用规则

Rules, by their nature, lend greater value when they are enforceable. Rules can be enforced socially, through teaching and training, or technically, with tooling. We have various formal training courses at Google that cover many of the best practices that our rules require. We also invest resources in keeping our documentation up to date to ensure that reference material remains accurate and current. A key part of our overall training approach when it comes to awareness and understanding of our rules is the role that code reviews play. The readability process that we run here at Google —where engineers new to Google’s development environment for a given language are mentored through code reviews—is, to a great extent, about cultivating the habits and patterns required by our style guides (see details on the readability process in
Chapter 3). The process is an important piece of how we ensure that these practices are learned and applied across project boundaries.

规则能够得到切实执行，才更有价值。执行既可以依靠教学、培训等人员层面的措施，也可以依靠工具等技术手段。谷歌有多种正式培训课程，涵盖规则要求的许多最佳实践；我们也投入资源持续更新文档，确保参考资料准确、不过时。要让工程师认识并理解规则，代码审查是整体培训方式中的关键一环。谷歌的 Readability（可读性认证）流程通过代码审查，为初次接触谷歌某门语言开发环境的工程师提供指导，很大程度上就是在培养风格指南要求的习惯和模式（详见第3章）。这一流程是确保这些实践跨越项目边界、得到学习和应用的重要机制。

Although some level of training is always necessary—engineers must, after all, learn the rules so that they can write code that follows them—when it comes to checking for compliance, rather than exclusively depending on engineer-based verification, we strongly prefer to automate enforcement with tooling.

一定程度的培训始终必不可少，毕竟工程师要先学会规则，才能写出符合规则的代码。但在检查是否遵守规则时，我们更倾向于用工具自动执行，而不是完全依赖工程师人工检查。

Automated rule enforcement ensures that rules are not dropped or forgotten as time passes or as an organization scales up. New people join; they might not yet know all the rules. Rules change over time; even with good communication, not everyone will remember the current state of everything. Projects grow and add new features; rules that had previously not been relevant are suddenly applicable. An engineer checking for rule compliance depends on either memory or documentation, both of which can fail. As long as our tooling stays up to date, in sync with our rule changes, we know that our rules are being applied by all our engineers for all our projects.

自动化执行能确保规则不会随着时间推移或组织扩大而被遗漏、遗忘。新人可能还不了解全部规则；规则会变化，即使沟通充分，也不是所有人都能记住每项最新要求；项目增长、功能增加后，原本无关的规则也可能突然适用。人工检查依靠记忆或文档，两者都可能出错。而只要工具及时更新、与规则变化同步，我们就能确保所有工程师在所有项目中都遵守规则。

Another advantage to automated enforcement is minimization of the variance in how a rule is interpreted and applied. When we write a script or use a tool to check for compliance, we validate all inputs against a single, unchanging definition of the rule. We aren’t leaving interpretation up to each individual engineer. Human engineers view everything with a perspective colored by their biases. Unconscious or not, potentially subtle, and even possibly harmless, biases still change the way people view things. Leaving enforcement up to engineers is likely to see inconsistent interpretation and application of the rules, potentially with inconsistent expectations of accountability. The more that we delegate to the tools, the fewer entry points we leave for human biases to enter.

自动化执行还能尽量减少规则解释和应用上的差异。脚本或工具依据同一个固定的规则定义检查所有输入，不把解释权留给每位工程师。人的看法总会受到自身偏见影响；这些偏见可能无意识、很细微，甚至无害，但仍会改变看待事物的方式。让工程师自行执行规则，可能导致解释和应用不一致，甚至对责任的要求也不一致。交给工具处理的部分越多，人为偏见介入的机会就越少。

Tooling also makes enforcement scalable. As an organization grows, a single team of experts can write tools that the rest of the company can use. If the company doubles in size, the effort to enforce all rules across the entire organization doesn’t double, it costs about the same as it did before.

工具也让规则执行具备可扩展性。组织扩大时，一个专家团队就能开发出供全公司使用的工具。即使公司规模翻倍，在整个组织中执行所有规则所需的投入也不会翻倍，而是与原来大致相同。

Even with the advantages we get by incorporating tooling, it might not be possible to automate enforcement for all rules. Some technical rules explicitly call for human judgment. In the C++ style guide, for example: “Avoid complicated template metaprogramming.” “Use auto to avoid type names that are noisy, obvious, or unimportant—cases where the type doesn’t aid in clarity for the reader.” “Composition is often more appropriate than inheritance.” In the Java style guide: “There’s no single correct recipe for how to [order the members and initializers of your class]; different classes may order their contents in different ways.” “It is very rarely correct to do nothing in response to a caught exception.” “It is extremely rare to override Object.finalize.” For all of these rules, judgment is required and tooling can’t (yet!) take that place.

工具虽然有这些优势，却未必能自动执行所有规则。有些技术规则明确需要人工判断。例如，C++ 风格指南规定：“避免复杂的模板元编程。”“使用 auto，避免写出冗长、显而易见或无关紧要的类型名，也就是那些无助于读者理解代码的类型名。”“组合往往比继承更合适。”Java 风格指南则规定：“如何[排列类成员和初始化器]，没有唯一正确的方法；不同的类可以采用不同顺序。”“捕获异常后什么都不做，极少是正确的处理方式。”“重写 Object.finalize 的情况极为罕见。”这些规则都需要判断力，工具目前还无法替代。

Other rules are social rather than technical, and it is often unwise to solve social problems with a technical solution. For many of the rules that fall under this category, the details tend to be a bit less well defined and tooling would become complex and expensive. It’s often better to leave enforcement of those rules to humans. For example, when it comes to the size of a given code change (i.e., the number of files affected and lines modified) we recommend that engineers favor smaller changes. Small changes are easier for engineers to review, so reviews tend to be faster and more thorough. They’re also less likely to introduce bugs because it’s easier to reason about the potential impact and effects of a smaller change. The definition of small, however, is somewhat nebulous. A change that propagates the identical one-line update across hundreds of files might actually be easy to review. By contrast, a smaller, 20-line change might introduce complex logic with side effects that are difficult to evaluate. We recognize that there are many different measurements of size, some of which may be subjective—particularly when taking the complexity of a change into account. This is why we do not have any tooling to autoreject a proposed change that exceeds an arbitrary line limit. Reviewers can (and do) push back if they judge a change to be too large. For this and similar rules, enforcement is up to the discretion of the engineers authoring and reviewing the code. When it comes to technical rules, however, whenever it is feasible, we favor technical enforcement.

还有些规则涉及人员协作，而不是技术；用技术方案解决人员协作问题，往往并不明智。这类规则的细节通常不够明确，若交给工具执行，工具可能变得复杂且成本高昂，因此由人判断往往更好。例如，我们建议工程师尽量缩小单次代码变更的规模，也就是受影响的文件数和修改行数。小变更更容易审查，审查通常也更快、更彻底；它们的潜在影响更容易推断，因此引入缺陷的可能性也更低。不过，“小”并没有清晰的定义。在数百个文件中重复同一项单行修改，可能很容易审查；反过来，只改20行，也可能引入复杂逻辑和难以评估的副作用。衡量规模有多种方式，有些难免带有主观性，尤其是考虑变更复杂度时。因此，我们没有用工具按某个任意设定的行数上限自动拒绝变更。如果审查者认为变更过大，可以要求调整，实践中也确实会这样做。这类规则由代码作者和审查者酌情执行；而对于技术规则，只要可行，我们仍倾向于通过技术手段执行。

### Error Checkers  错误检查工具

Many rules covering language usage can be enforced with static analysis tools. In fact, an informal survey of the C++ style guide by some of our C++ librarians in mid-2018 estimated that roughly 90% of its rules could be automatically verified. Error- checking tools take a set of rules or patterns and verify that a given code sample fully complies. Automated verification removes the burden of remembering all applicable rules from the code author. If an engineer only needs to look for violation warnings— many of which come with suggested fixes—surfaced during code review by an analyzer that has been tightly integrated into the development workflow, we minimize the effort that it takes to comply with the rules. When we began using tools to flag deprecated functions based on source tagging, surfacing both the warning and the suggested fix in-place, the problem of having new usages of deprecated APIs disappeared almost overnight. Keeping the cost of compliance down makes it more likely for engineers to happily follow through.

许多语言使用规则可以通过静态分析工具执行。2018年年中，一些 C++ 库工程师曾对 C++ 风格指南作过非正式调查，估计约90%的规则可以自动检查。错误检查工具依据一组规则或模式，验证代码是否完全符合要求，从而免去作者记住所有适用规则的负担。如果分析工具紧密集成到开发工作流中，在代码审查时直接显示违规警告，并且许多警告还附有修复建议，工程师只需关注这些提示，就能大幅减少遵守规则所需的精力。我们开始依据源代码中的标记检测已弃用函数，并在相应位置同时显示警告和修复建议后，新增代码继续使用已弃用 API 的问题几乎一夜之间就消失了。降低遵守规则的成本，更能让工程师乐于执行。

We use tools like clang-tidy (for C++) and Error Prone (for Java) to automate the process of enforcing rules. See Chapter 20 for an in-depth discussion of our approach.

我们使用 clang-tidy（用于 C++）和 Error Prone（用于 Java）等工具自动执行规则。第20章会深入讨论这些做法。

The tools we use are designed and tailored to support the rules that we define. Most tools in support of rules are absolutes; everybody must comply with the rules, so everybody uses the tools that check them. Sometimes, when tools support best practi‐ces where there’s a bit more flexibility in conforming to the conventions, there are opt-out mechanisms to allow projects to adjust for their needs.

这些工具都针对我们制定的规则设计和定制。大多数规则检查工具都必须使用：既然人人都要遵守规则，也就人人都要用工具检查。但有些工具支持的是留有变通空间的最佳实践，因此提供退出机制，让项目可以按自身需要调整。

### Code Formatters  代码格式化工具

At Google, we generally use automated style checkers and formatters to enforce consistent formatting within our code. The question of line lengths has stopped being interesting.[^13]Engineers just run the style checkers and keep moving forward. When formatting is done the same way every time, it becomes a non-issue during code review, eliminating the review cycles that are otherwise spent finding, flagging, and fixing minor style nits.

在谷歌，我们通常用自动风格检查工具和格式化工具来统一代码格式。行长已不再是值得讨论的问题；工程师运行检查工具后，就可以继续工作。每次都以相同方式格式化代码，格式就不会再成为代码审查的议题，也省去了为发现、指出和修正细小风格问题而反复审查的时间。

In managing the largest codebase ever, we’ve had the opportunity to observe the results of formatting done by humans versus formatting done by automated tooling. The robots are better on average than the humans by a significant amount. There are some places where domain expertise matters—formatting a matrix, for example, is something a human can usually do better than a general-purpose formatter. Failing that, formatting code with an automated style checker rarely goes wrong.

管理有史以来最大的代码库，让我们有机会比较人工与自动工具的格式化效果。平均而言，工具明显优于人工。某些场景确实需要领域知识，例如矩阵的排版，人工通常比通用格式化工具做得更好。除此之外，交给自动风格检查工具格式化代码，很少会出问题。

We enforce use of these formatters with presubmit checks: before code can be submitted, a service checks whether running the formatter on the code produces any diffs. If it does, the submit is rejected with instructions on how to run the formatter to fix the code. Most code at Google is subject to such a presubmit check. For our code, we use clang-format for C++; an in-house wrapper around yapf for Python; gofmt for Go; dartfmt for Dart; and buildifier for our BUILD files.

我们通过提交前检查强制使用这些格式化工具：代码提交之前，服务会检查运行格式化工具后是否产生差异。如果有差异，就拒绝提交，并说明如何运行工具修正代码。谷歌的大多数代码都接受这类检查。C++ 使用 clang-format，Python 使用内部封装的 yapf，Go 使用 gofmt，Dart 使用 dartfmt，BUILD 文件则使用 buildifier。

> 13 When you consider that it takes at least two engineers to have the discussion and multiply that by the number of times this conversation is likely to happen within a collection of more than 30,000 engineers, it turns out that “how many characters” can become a very expensive question.
>
> 13 每次讨论至少涉及两名工程师，再乘以这种讨论在3万多名工程师中可能发生的次数，就会发现：“一行多少个字符”也可能是个代价高昂的问题。

---

#### Case Study: gofmt  案例分析：gofmt

Sameer Ajmani

萨米尔·阿吉马尼

Google released the Go programming language as open source on November 10, 2009. Since then, Go has grown as a language for developing services, tools, cloud infrastructure, and open source software.[^14]

谷歌于2009年11月10日开源发布了 Go 编程语言。此后，Go 逐渐发展成为开发服务、工具、云基础设施和开源软件所使用的语言。

We knew that we needed a standard format for Go code from day one. We also knew that it would be nearly impossible to retrofit a standard format after the open source release. So the initial Go release included gofmt, the standard formatting tool for Go.

从第一天起，我们就知道 Go 代码需要统一的标准格式，也知道等到开源发布后再补推这种标准，几乎不可能。因此，Go 的首个版本就附带了标准格式化工具 gofmt。

**Motivations 动机**

Code reviews are a software engineering best practice, yet too much time was spent in review arguing over formatting. Although a standard format wouldn’t be everyone’s favorite, it would be good enough to eliminate this wasted time.[^15]

代码审查是软件工程的最佳实践，但审查时有太多时间花在了格式争论上。标准格式未必合每个人的心意，却足以避免这种时间浪费。

By standardizing the format, we laid the foundation for tools that could automatically update Go code without creating spurious diffs: machine-edited code would be indistinguishable from human-edited code.[^16]

统一格式也为自动更新 Go 代码的工具奠定了基础：工具修改不会产生无意义的格式差异，因为机器编辑和人工编辑的代码在格式上没有区别。

For example, in the months leading up to Go 1.0 in 2012, the Go team used a tool called gofix to automatically update pre-1.0 Go code to the stable version of the language and libraries. Thanks to gofmt, the diffs gofix produced included only the important bits: changes to uses of the language and APIs. This allowed programmers to more easily review the changes and learn from the changes the tool made.

例如，2012年 Go 1.0 发布前的几个月，Go 团队用 gofix 工具自动更新早于 1.0 的 Go 代码，使之适配语言和库的稳定版本。有了 gofmt，gofix 产生的差异就只包含重要内容，也就是语言和 API 用法的变化。程序员因此更容易审查变更，也能从工具所作的修改中学习。

**Impact 影响**

Go programmers expect that all Go code is formatted with gofmt. gofmt has no configuration knobs, and its behavior rarely changes. All major editors and IDEs use gofmt or emulate its behavior, so nearly all Go code in existence is formatted identically. At first, Go users complained about the enforced standard; now, users often cite gofmt as one of the many reasons they like Go. Even when reading unfamiliar Go code, the format is familiar.

Go 程序员默认所有 Go 代码都经过 gofmt 格式化。gofmt 没有可调的配置项，行为也很少改变。主流编辑器和 IDE 都使用 gofmt，或实现相同的行为，因此几乎所有 Go 代码都采用同一种格式。起初，用户曾抱怨这项强制标准；如今，gofmt 却常被列为他们喜欢 Go 的原因之一。即使代码陌生，格式也很熟悉。

Thousands of open source packages read and write Go code.[^17] Because all editors and IDEs agree on the Go format, Go tools are portable and easily integrated into new developer environments and workflows via the command line.

有数千个开源包会读取和生成 Go 代码。由于所有编辑器和 IDE 都遵循同一种 Go 格式，Go 工具便于移植，也容易通过命令行集成到新的开发环境和工作流中。

 **Retrofitting 为既有代码统一格式**

In 2012, we decided to automatically format all BUILD files at Google using a new standard formatter: buildifier. BUILD files contain the rules for building Google’s software with Blaze, Google’s build system. A standard BUILD format would enable us to create tools that automatically edit BUILD files without disrupting their format, just as Go tools do with Go files.

2012年，我们决定使用新的标准格式化工具 buildifier，自动格式化谷歌的所有 BUILD 文件。BUILD 文件包含通过谷歌构建系统 Blaze 构建软件的规则。统一 BUILD 格式后，就能开发自动编辑这些文件而不扰乱格式的工具，就像 Go 工具处理 Go 文件一样。

It took six weeks for one engineer to get the reformatting of Google’s 200,000 BUILD files accepted by the various code owners, during which more than a thousand new BUILD files were added each week. Google’s nascent infrastructure for making large- scale changes greatly accelerated this effort. (See Chapter 22.)

一位工程师花了六周时间，才让各代码负责人接受了对谷歌20万个 BUILD 文件重新格式化的变更；其间，每周还会新增一千多个 BUILD 文件。谷歌当时初步建立的大规模变更基础设施，大大加快了这项工作（见第22章）。

-----

> [^14]:  In December 2018, Go was the #4 language on GitHub as measured by pull requests.
>
> 14 2018年12月，按拉取请求数量衡量，Go 在 GitHub 的编程语言中排名第四。
>
> [^15]:  Robert Griesemer’s 2015 talk, “The Cultural Evolution of gofmt,” provides details on the motivation, design,and impact of gofmt on Go and other languages.
>
> 15 Robert Griesemer 在2015年的演讲《gofmt 的文化演变》中详细介绍了 gofmt 的动机、设计，
> 以及 gofmt 对 Go 和其他语言的影响。
>
> [^16]:  Russ Cox explained in 2009 that gofmt was about automated changes: “So we have all the hard parts of a program manipulation tool just sitting waiting to be used. Agreeing to accept ‘gofmt style’ is the piece that makes it doable in a finite amount of code.”
>
> 16 Russ Cox 在2009年解释说，gofmt 的目的在于支持自动化修改：“这样一来，开发程序修改工具所需的那些困难部分，我们都已经具备，只等投入使用。只要大家同意接受‘gofmt 风格’，就能用有限的代码量实现这样的工具。”
>
> [^17]:  The Go AST and format packages each have thousands of importers.
>
> 17 Go 的 AST 包和 format 包，分别被数千个包导入使用。

## Conclusion  总结

For any organization, but especially for an organization as large as Google’s engineering force, rules help us to manage complexity and build a maintainable codebase. A shared set of rules frames the engineering processes so that they can scale up and keep growing, keeping both the codebase and the organization sustainable for the long term.

对任何组织，尤其是谷歌这样规模庞大的工程组织，规则都有助于管理复杂性、建立可维护的代码库。一套共同遵守的规则为工程流程提供了框架，使其能够随规模扩展、持续发展，从而让代码库和组织都保持长期可持续性。

## TL;DRs  内容提要

- Rules and guidance should aim to support resilience to time and scaling.
- Know the data so that rules can be adjusted.
- Not everything should be a rule.
- Consistency is key.
- Automate enforcement when possible.

- 规则和指导应有助于应对时间推移和规模增长。
- 了解数据，以便调整规则。
- 并非所有做法都应写成规则。
- 一致性是关键。
- 只要可行，就用自动化手段执行规则。
