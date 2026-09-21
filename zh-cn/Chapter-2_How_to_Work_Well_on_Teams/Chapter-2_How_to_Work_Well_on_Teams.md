
**CHAPTER 2**

# How to Work Well on Teams

# 第二章 如何在团队中有效协作

**Written by Brian Fitzpatrick**

**Edited by Riona MacNamara**

Because this chapter is about the cultural and social aspects of software engineering at Google, it makes sense to begin by focusing on the one variable over which you definitely have control: you.

本章讨论谷歌软件工程中的文化和人际互动，因此不妨先关注一个你肯定能掌控的变量：你自己。

People are inherently imperfect—we like to say that humans are mostly a collection of intermittent bugs. But before you can understand the bugs in your coworkers, you need to understand the bugs in yourself. We’re going to ask you to think about your own reactions, behaviors, and attitudes—and in return, we hope you gain some real insight into how to become a more efficient and successful software engineer who spends less energy dealing with people-related problems and more time writing great code.

人天生就不完美。我们常说，人基本上就是一堆时不时发作的缺陷。但要理解同事身上的缺陷，先得了解自己的。接下来，我们会请你反思自己的反应、行为和态度，希望这能让你真正看清如何成为更高效、更成功的软件工程师：少花些精力处理人际问题，多花些时间编写出色的代码。

The critical idea in this chapter is that software development is a team endeavor. And to succeed on an engineering team—or in any other creative collaboration—you need to reorganize your behaviors around the core principles of humility, respect, and trust.

本章的核心观点是：软件开发需要团队协作。要在工程团队中，或在其他创造性协作中取得成功，你需要以谦逊、尊重和信任为核心原则，调整自己的行为。

Before we get ahead of ourselves, let’s begin by observing how software engineers tend to behave in general.

先别急着往下谈，我们先看看软件工程师通常会怎样行事。

## Help Me Hide My Code  帮我隐藏我的代码

For the past 20 years, my colleague Ben[^1] and I have spoken at many programming conferences. In 2006, we launched Google’s (now deprecated) open source Project Hosting service, and at first, we used to get lots of questions and requests about the product. But around mid-2008, we began to notice a trend in the sort of requests we were getting:
    “Can you please give Subversion on Google Code the ability to hide specific branches?”
    “Can you make it possible to create open source projects that start out hidden to the world and then are revealed when they’re ready?”
    “Hi, I want to rewrite all my code from scratch, can you please wipe all the history?”
Can you spot a common theme to these requests?

过去20年里，我和同事 Ben 在许多编程会议上做过演讲。2006年，我们推出了谷歌的开源项目托管服务（现已弃用）。起初，我们经常收到关于这个产品的问题和请求。但到了2008年年中左右，我们发现这些请求呈现出一种趋势：

​    “能不能让 Google Code 上的 Subversion 支持隐藏特定分支？” 

​    “能不能让开源项目创建后先不对外公开，等准备好了再公开？” 

​    “你好，我想从头重写全部代码，能不能把所有历史记录都删掉？”

你能看出这些请求的共同点吗？

The answer is insecurity. People are afraid of others seeing and judging their work in progress. In one sense, insecurity is just a part of human nature—nobody likes to be criticized, especially for things that aren’t finished. Recognizing this theme tipped us off to a more general trend within software development: insecurity is actually a symptom of a larger problem.

答案是缺乏安全感。人们害怕别人看到并评价自己尚未完成的工作。从某种意义上说，缺乏安全感是人性的一部分：谁也不喜欢受到批评，尤其不喜欢因为尚未完成的工作受批评。发现这个共同点，让我们注意到软件开发中一个更普遍的现象：缺乏安全感其实是某个更大问题的表征。

> [^1]: Ben Collins-Sussman, also an author within this book.  
        Ben Collins-Sussman，也是本书的作者之一。

## The Genius Myth  天才神话

Many humans have the instinct to find and worship idols. For software engineers, those might be Linus Torvalds, Guido Van Rossum, Bill Gates—all heroes who changed the world with heroic feats. Linus wrote Linux by himself, right?

许多人天生就会寻找并崇拜偶像。对软件工程师来说，偶像可能是 Linus Torvalds、Guido Van Rossum 或 Bill Gates，这些人都凭借非凡的成就改变了世界。Linux 不就是 Linus 一个人写出来的吗？

Actually, what Linus did was write just the beginnings of a proof-of-concept Unix- like kernel and show it to an email list. That was no small accomplishment, and it was definitely an impressive achievement, but it was just the tip of the iceberg. Linux is hundreds of times bigger than that initial kernel and was developed by thousands of smart people. Linus’ real achievement was to lead these people and coordinate their work; Linux is the shining result not of his original idea, but of the collective labor of the community. (And Unix itself was not entirely written by Ken Thompson and Dennis Ritchie, but by a group of smart people at Bell Labs.)

实际上，Linus 只是写出了一个用于概念验证的类 Unix 内核的初步版本，并在邮件列表中展示出来。这当然是不小的成就，也确实令人赞叹，但它只是冰山一角。Linux 的规模比最初的内核大了几百倍，凝聚了数千名聪明开发者的工作。Linus 真正的成就在于领导这些人、协调他们的工作；Linux 这一耀眼成果并不归功于他最初的想法，而是来自社区的集体劳动。（Unix 本身也并非完全由肯·汤普森和丹尼斯·里奇编写，而是贝尔实验室一群聪明人的共同成果。）

On that same note, did Guido Van Rossum personally write all of Python? Certainly, he wrote the first version. But hundreds of others were responsible for contributing to subsequent versions, including ideas, features, and bug fixes. Steve Jobs led an entire team that built the Macintosh, and although Bill Gates is known for writing a BASIC interpreter for early home computers, his bigger achievement was building a successful company around MS-DOS. Yet they all became leaders and symbols of the collective achievements of their communities. The Genius Myth is the tendency that we as humans need to ascribe the success of a team to a single person/leader.

同样，Python 的全部代码都是 Guido Van Rossum 亲自写的吗？他确实编写了第一个版本，但后续版本的想法、功能和缺陷修复，都有数百名其他开发者的贡献。史蒂夫·乔布斯领导的是整个开发麦金塔电脑的团队。比尔·盖茨虽然以为早期家用电脑编写 BASIC 解释器而闻名，但他更大的成就是围绕 MS-DOS 建立了一家成功的公司。然而，他们都成为各自群体的领导者，以及集体成就的象征。所谓“天才神话”，就是我们总倾向于把团队的成功归功于某一个人或领导者。

And what about Michael Jordan?

那么 Michael Jordan 呢？

It’s the same story. We idolized him, but the fact is that he didn’t win every basketball game by himself. His true genius was in the way he worked with his team. The team’s coach, Phil Jackson, was extremely clever, and his coaching techniques are legendary.

道理也一样。我们崇拜他，但他并不是靠一己之力赢下每一场篮球比赛的。他真正的天赋体现在与球队协作的方式上。球队教练 Phil Jackson 极其聪明，执教方法堪称传奇。

He recognized that one player alone never wins a championship, and so he assembled an entire “dream team” around MJ. This team was a well-oiled machine—at least as impressive as Michael himself.

他明白，单靠一名球员永远赢不了冠军，因此围绕 Michael Jordan 组建了一整支“梦之队”。这支球队如同一台运转顺畅的机器，至少与迈克尔本人一样令人赞叹。

So, why do we repeatedly idolize the individual in these stories? Why do people buy products endorsed by celebrities? Why do we want to buy Michelle Obama’s dress or Michael Jordan’s shoes?

那么，为什么我们听到这些故事时，总是会崇拜其中的个人？为什么人们会购买名人代言的产品？为什么我们会想买米歇尔·奥巴马穿的裙子或 Michael Jordan 穿的鞋子？

Celebrity is a big part of it. Humans have a natural instinct to find leaders and role models, idolize them, and attempt to imitate them. We all need heroes for inspiration, and the programming world has its heroes, too. The phenomenon of “techie- celebrity” has almost spilled over into mythology. We all want to write something world-changing like Linux or design the next brilliant programming language.

名人效应是很大一部分原因。人类天生就会寻找领导者和榜样，崇拜他们，并试图模仿他们。我们都需要英雄来激励自己，编程领域也有自己的英雄。“技术名人”现象几乎已演变为神话。我们都想写出像 Linux 那样改变世界的软件，或设计出下一门出色的编程语言。

Deep down, many engineers secretly wish to be seen as geniuses. This fantasy goes something like this:

- You are struck by an awesome new concept.
- You vanish into your cave for weeks or months, slaving away at a perfect implementation of your idea.
- You then “unleash” your software on the world, shocking everyone with your genius.
- Your peers are astonished by your cleverness.
- People line up to use your software.
- Fame and fortune follow naturally.

许多工程师内心深处都暗自希望被人视为天才。他们的幻想大致是这样的：

- 你突然想到一个绝妙的新点子。
- 你躲进自己的洞穴，一连消失数周乃至数月，埋头苦干，力求把想法实现得尽善尽美。
- 随后，你向全世界“发布”这款软件，以自己的天才震撼所有人。
- 同行们惊叹于你的聪明才智。
- 人们排队使用你的软件。
- 名利自然随之而来。

But hold on: time for a reality check. You’re probably not a genius.

是时候回归现实了。你很可能不是天才。

No offense, of course—we’re sure that you’re a very intelligent person. But do you realize how rare actual geniuses really are? Sure, you write code, and that’s a tricky skill. But even if you are a genius, it turns out that that’s not enough. Geniuses still make mistakes, and having brilliant ideas and elite programming skills doesn’t guarantee that your software will be a hit. Worse, you might find yourself solving only analytical problems and not human problems. Being a genius is most definitely not an excuse for being a jerk: anyone—genius or not—with poor social skills tends to be a poor teammate. The vast majority of the work at Google (and at most companies!) doesn’t require genius-level intellect, but 100% of the work requires a minimal level of social skills. What will make or break your career, especially at a company like Google, is how well you collaborate with others.

这当然无意冒犯，我们相信你非常聪明。但你知道真正的天才有多罕见吗？你会编程，这的确是一项难以掌握的技能。可即使你是天才，光有这一点也不够。天才也会犯错，绝妙的想法和顶尖的编程能力并不能保证软件大获成功。更糟的是，你可能只会解决需要分析的问题，却解决不了人的问题。天才身份绝不是待人恶劣的借口：无论是不是天才，社交能力差的人往往都不是好队友。谷歌以及大多数公司的绝大部分工作并不需要天才般的智力，但100%的工作都需要最基本的社交能力。决定你职业生涯成败的，是你与他人协作的能力，在谷歌这样的公司尤其如此。

It turns out that this Genius Myth is just another manifestation of our insecurity. Many programmers are afraid to share work they’ve only just started because it means peers will see their mistakes and know the author of the code is not a genius.

说到底，天才神话只是我们缺乏安全感的另一种表现。许多程序员害怕分享刚起步的工作，因为这样一来，同行就会看到他们的错误，知道代码的作者并不是天才。

To quote a friend:
> I know I get SERIOUSLY insecure about people looking before something is done. Like they are going to seriously judge me and think I’m an idiot.

引用一位朋友的话：  
> 我知道，东西还没做完就让人来看，会让我特别没有安全感。总觉得他们会严厉地评判我，认定我是个白痴。

This is an extremely common feeling among programmers, and the natural reaction is to hide in a cave, work, work, work, and then polish, polish, polish, sure that no one will see your goof-ups and that you’ll still have a chance to unveil your masterpiece when you’re done. Hide away until your code is perfect.

这种感觉在程序员中极为普遍，自然而然的反应就是躲进洞穴，不停地干活，再反复打磨。这样就能确保没人看到自己的失误，等完成后，仍有机会向大家展示自己的杰作。先躲起来，直到代码完美无缺。

Another common motivation for hiding your work is the fear that another programmer might take your idea and run with it before you get around to working on it. By keeping it secret, you control the idea.

不公开工作的另一个常见原因，是担心其他程序员拿到你的想法，抢在你动手之前就将它付诸实现。只要保密，你就能掌控这个想法。

We know what you’re probably thinking now: so what? Shouldn’t people be allowed to work however they want?
Actually, no. In this case, we assert that you’re doing it wrong, and it is a big deal. Here’s why.

我们知道你现在可能在想：那又怎样？难道不该允许大家按自己喜欢的方式工作吗？

其实不该如此。对于这种情况，我们的看法很明确：你的做法不对，而且问题不小。原因如下。

## Hiding Considered Harmful 隐藏工作的危害

If you spend all of your time working alone, you’re increasing the risk of unnecessary failure and cheating your potential for growth. Even though software development is deeply intellectual work that can require deep concentration and alone time, you must play that off against the value (and need!) for collaboration and review.

如果你始终独自工作，就会增加本可避免的失败风险，也会限制自己的成长。软件开发确实是高度依赖思考的工作，可能需要专注和独处，但你必须在这些需求与协作、审查的价值和必要性之间作出权衡。

First of all, how do you even know whether you’re on the right track?

首先，你怎么知道自己的方向对不对？

Imagine you’re a bicycledesign enthusiast, and one day you get a brilliant idea for a completely new way to design a gear shifter. You order parts and proceed to spend weeks holed up in your garage trying to build a prototype. When your neighbor— also a bike advocate—asks you what’s up, you decide not to talk about it. You don’t want anyone to know about your project until it’s absolutely perfect. Another few months go by and you’re having trouble making your prototype work correctly. But because you’re working in secrecy, it’s impossible to solicit advice from your mechanically inclined friends.

假设你是一名自行车设计爱好者，有一天突发奇想，要用一种全新的方式设计变速器。你订购了零件，随后在车库里埋头干了几个星期，尝试做出原型。邻居也是自行车爱好者，问起你在忙什么，你却决定保密，非要等项目完美无缺才肯告诉别人。又过了几个月，你还是没法让原型正常运转。但既然一直秘密进行，就无法向那些擅长机械的朋友请教。

Then, one day your neighbor pulls his bike out of his garage with a radical new gear- shifting mechanism. Turns out he’s been building something very similar to your invention, but with the help of some friends down at the bike shop. At this point, you’re exasperated. You show him your work. He points out that your design had some simple flaws—ones that might have been fixed in the first week if you had shown him. There are a number of lessons to learn here.

后来有一天，邻居从车库里推出自行车，上面装着一种全新的变速装置。原来，他也一直在做与你的发明十分相似的东西，只是有自行车店的几位朋友帮忙。你又气又恼，把自己的成果拿给他看。他指出，你的设计中有几个简单的缺陷；如果早些拿给他看，也许第一周就能解决。这个故事值得吸取不少教训。

### Early Detection 及早发现

If you keep your great idea hidden from the world and refuse to show anyone anything until the implementation is polished, you’re taking a huge gamble. It’s easy to make fundamental design mistakes early on. You risk reinventing wheels.2 And you forfeit the benefits of collaboration, too: notice how much faster your neighbor moved by working with others? This is why people dip their toes in the water before jumping in the deep end: you need to make sure that you’re working on the right thing, you’re doing it correctly, and it hasn’t been done before. The chances of an early misstep are high. The more feedback you solicit early on, the more you lower this risk.3 Remember the tried-and-true mantra of “Fail early, fail fast, fail often.”

把好点子藏起来，非等到实现得尽善尽美才肯让别人看，就是在冒很大的风险。早期很容易犯根本性的设计错误，也可能重复造轮子。[^2]你还会失去协作的好处：注意到邻居与他人合作后，进展快了多少吗？这就是人们跳入深水区前要先试试水的原因：你得确认自己做的是正确的事，方法也正确，而且这件事还没有人做过。早期走错路的可能性很高；在早期征求的反馈越多，这种风险就越低。[^3]记住那句久经检验的箴言：“尽早失败，快速失败，经常失败。”

Early sharing isn’t just about preventing personal missteps and getting your ideas vetted. It’s also important to strengthen what we call the bus factor of your project.

尽早分享不只是为了避免个人失误、让别人检验你的想法，也有助于提高项目的“巴士因子”。

> [^2]: Literally, if you are, in fact, a bike designer.  
        如果你真的是自行车设计师，这里的“造轮子”就不是比喻了。

> [^3]: I should note that sometimes it’s dangerous to get too much feedback too early in the process if you’re still unsure of your general direction or goal.  
        这里要提醒一句：如果你还不确定总体方向或目标，过早获得太多反馈有时也会带来风险。

### The Bus Factor 巴士因子

Bus factor (noun): the number of people that need to get hit by a bus before your project is completely doomed.

巴士因子（名词）：有多少人被巴士撞倒后，项目就会彻底陷入绝境。

How dispersed is the knowledge and know-how in your project? If you’re the only person who understands how the prototype code works, you might enjoy good job security—but if you get hit by a bus, the project is toast. If you’re working with a colleague, however, you’ve doubled the bus factor. And if you have a small team designing and prototyping together, things are even better—the project won’t be marooned when a team member disappears. Remember: team members might not literally be hit by buses, but other unpredictable life events still happen. Someone might get married, move away, leave the company, or take leave to care for a sick relative. Ensuring that there is at least good documentation in addition to a primary and a secondary owner for each area of responsibility helps future-proof your project’s success and increases your project’s bus factor. Hopefully most engineers recognize that it is better to be one part of a successful project than the critical part of a failed project.

项目的知识和实践经验分散在多少人手中？如果只有你了解原型代码如何工作，你的职位也许很稳固，但万一你被巴士撞倒，项目就完了。如果有一位同事与你合作，巴士因子就翻了一番。若有一个小团队共同设计和制作原型，情况就更好：即使一名成员不在了，项目也不至于陷入困境。记住，团队成员未必真的会被巴士撞倒，但生活中总有其他意外。有人可能结婚、搬家、离职，或请假照顾生病的亲属。确保每个职责领域都有主要负责人和后备负责人，并且至少有完善的文档，有助于保障项目未来的成功，提高巴士因子。希望大多数工程师都能明白：做成功项目中的一员，总比做失败项目中不可或缺的那个人更好。

Beyond the bus factor, there’s the issue of overall pace of progress. It’s easy to forget that working alone is often a tough slog, much slower than people want to admit. How much do you learn when working alone? How fast do you move? Google and Stack Overflow are great sources of opinions and information, but they’re no substitute for actual human experience. Working with other people directly increases the collective wisdom behind the effort. When you become stuck on something absurd, how much time do you waste pulling yourself out of the hole? Think about how different the experience would be if you had a couple of peers to look over your shoulder and tell you—instantly—how you goofed and how to get past the problem. This is exactly why teams sit together (or do pair programming) in software engineering companies. Programming is hard. Software engineering is even harder. You need that second pair of eyes.

除了巴士因子，还要考虑整体进展速度。人们很容易忘记，独自工作往往十分艰难，进展也比自己愿意承认的慢得多。一个人做事能学到多少？又能推进多快？Google 和 Stack Overflow 能提供丰富的观点与信息，却无法替代他人的实际经验。与人合作，可以直接汇集更多人的智慧。如果你被一个荒唐的小问题卡住，要浪费多少时间才能脱困？试想，若有几位同行在旁边看看，立刻指出哪里出了错、该如何解决，体验会有多大不同。这正是软件工程公司让团队坐在一起工作或进行结对编程的原因。编程很难，软件工程更难。你需要另一双眼睛帮你检查。

### Pace of Progress 进展速度

Here’s another analogy. Think about how you work with your compiler. When you sit down to write a large piece of software, do you spend days writing 10,000 lines of code, and then, after writing that final, perfect line, press the “compile” button for the very first time? Of course you don’t. Can you imagine what sort of disaster would result? Programmers work best in tight feedback loops: write a new function, compile. Add a test, compile. Refactor some code, compile. This way, we discover and fix typos and bugs as soon as possible after generating code. We want the compiler at our side for every little step; some environments can even compile our code as we type. This is how we keep code quality high and make sure our software is evolving correctly, bit by bit. The current DevOps philosophy toward tech productivity is explicit about these sorts of goals: get feedback as early as possible, test as early as possible, and think about security and production environments as early as possible. This is all bundled into the idea of “shifting left” in the developer workflow; the earlier we find a problem, the cheaper it is to fix it.

再打个比方，想想你是怎样使用编译器的。编写大型软件时，你会花几天时间写完10,000行代码，等最后一行也完美无缺，才第一次按下“编译”按钮吗？当然不会。你能想象那会造成怎样的灾难吗？程序员在短周期反馈循环中工作最有效：写一个新函数，编译；加一个测试，编译；重构一些代码，再编译。这样，代码写出来后，拼写错误和缺陷就能尽快被发现并修复。我们希望每一小步都有编译器相伴，有些环境甚至会在输入代码时实时编译。正是这样，我们才能保持代码质量，确保软件一点点朝正确的方向演进。当前 DevOps 关于技术生产力的理念明确强调这些目标：尽早获得反馈，尽早测试，尽早考虑安全问题和生产环境。这些做法都体现了开发工作流中的“左移”思想：越早发现问题，修复成本就越低。

The same sort of rapid feedback loop is needed not just at the code level, but at the whole-project level, too. Ambitious projects evolve quickly and must adapt to changing environments as they go. Projects run into unpredictable design obstacles or political hazards, or we simply discover that things aren’t working as planned. Requirements morph unexpectedly. How do you get that feedback loop so that you know the instant your plans or designs need to change? Answer: by working in a team. Most engineers know the quote, “Many eyes make all bugs shallow,” but a better version might be, “Many eyes make sure your project stays relevant and on track.” People working in caves awaken to discover that while their original vision might be complete, the world has changed and their project has become irrelevant.

这种快速反馈循环不仅适用于代码，也适用于整个项目。目标远大的项目演进很快，推进过程中必须适应不断变化的环境。项目可能遇到意想不到的设计障碍或组织内部的政治风险，也可能只是没有按计划发展。需求也会出乎意料地变化。怎样建立反馈循环，才能在计划或设计需要调整时立刻察觉？答案是团队协作。大多数工程师都听过“只要有足够多的人检查，所有缺陷都容易解决”，但更贴切的说法或许是：“更多人的关注能确保项目仍有价值，且方向正确。”躲在洞穴里工作的人回过神来时才发现，即使最初的愿景已经实现，世界也已改变，项目不再切合需要。

------

**Case Study: Engineers and Offices**

**案例研究：工程师与办公环境**

Twenty-five years ago, conventional wisdom stated that for an engineer to be productive, they needed to have their own office with a door that closed. This was supposedly the only way they could have big, uninterrupted slabs of time to deeply concentrate on writing reams of code.

25年前，人们普遍认为，工程师要高效工作，就需要一间能够关上门的独立办公室。大家以为，只有这样，他们才能拥有大段不受打扰的时间，专心编写大量代码。

I think that it’s not only unnecessary for most engineers[^4] to be in a private office, it’s downright dangerous. Software today is written by teams, not individuals, and a high- bandwidth, readily available connection to the rest of your team is even more valuable than your internet connection. You can have all the uninterrupted time in the world, but if you’re using it to work on the wrong thing, you’re wasting your time.

我认为，对大多数工程师而言，独立办公室不仅没有必要，甚至相当危险。如今的软件由团队而非个人编写，随时都能与队友充分沟通，比接入互联网更有价值。你可以拥有再多不受打扰的时间，但如果方向错了，这些时间就都浪费了。

Unfortunately, it seems that modern-day tech companies (including Google, in some cases) have swung the pendulum to the exact opposite extreme. Walk into their offices and you’ll often find engineers clustered together in massive rooms—a hundred or more people together—with no walls whatsoever. This “open floor plan” is now a topic of huge debate and, as a result, hostility toward open offices is on the rise. The tiniest conversation becomes public, and people end up not talking for risk of annoying dozens of neighbors. This is just as bad as private offices!

遗憾的是，如今的科技公司似乎又走向了另一个极端，谷歌有时也不例外。走进它们的办公室，常能看到一百人甚至更多工程师挤在一个大房间里，没有任何墙壁隔断。这种“开放式布局”如今引发了激烈争论，人们对开放式办公室也越来越反感。再小的交谈都会被周围人听见，结果大家怕打扰附近几十位同事，索性不再说话。这与独立办公室一样糟糕！

We think the middle ground is really the best solution. Group teams of four to eight people together in small rooms (or large offices) to make it easy (and non- embarrassing) for spontaneous conversation to happen.

我们认为，折中才是最好的办法：让四到八人的团队共用一个小房间或大办公室，方便大家自然地交谈，也不必感到尴尬。

Of course, in any situation, individual engineers still need a way to filter out noise and interruptions, which is why most teams I’ve seen have developed a way to communicate that they’re currently busy and that you should limit interruptions. Some of us used to work on a team with a vocal interrupt protocol: if you wanted to talk, you would say “Breakpoint Mary,” where Mary was the name of the person you wanted to talk to. If Mary was at a point where she could stop, she would swing her chair around and listen. If Mary was too busy, she’d just say “ack,” and you’d go on with other things until she finished with her current head state.

当然，无论采用哪种安排，工程师个人仍需要办法屏蔽噪声、减少打扰。因此，我见过的大多数团队都会约定一种信号，表示自己正忙，请尽量不要打断。我们中有些人曾在一个团队里使用口头中断协议：想与人交谈时，就说“Breakpoint Mary”，其中 Mary 是对方的名字。如果 Mary 恰好可以停下来，就会转过椅子听你说；如果正忙，就只回答“收到”，你便先去做别的事，等她把当前的思路处理完。

Other teams have tokens or stuffed animals that team members put on their monitor to signify that they should be interrupted only in case of emergency. Still other teams give out noise-canceling headphones to engineers to make it easier to deal with background noise—in fact, in many companies, the very act of wearing headphones is a common signal that means “don’t disturb me unless it’s really important.” Many engineers tend to go into headphones-only mode when coding, which may be useful for short spurts but, if used all the time, can be just as bad for collaboration as walling yourself off in an office.

有的团队用小物件或毛绒玩具作为标记，放在显示器上，表示只有紧急情况才能打扰。还有些团队为工程师配备降噪耳机，帮助隔绝背景噪声。事实上，在许多公司，戴上耳机本身就是常见的信号，意思是“除非事情真的很重要，否则请勿打扰”。许多工程师写代码时喜欢戴着耳机、与外界隔开，短时间内这样做或许有用，但如果一直如此，对协作的妨碍就与把自己关在办公室里一样大。

Don’t misunderstand us—we still think engineers need uninterrupted time to focus on writing code, but we think they need a high-bandwidth, low-friction connection to their team just as much. If less-knowledgeable people on your team feel that there’s a barrier to asking you a question, it’s a problem: finding the right balance is an art.

别误会，我们仍然认为工程师需要不受打扰的时间，专心编写代码；但与团队充分、顺畅地沟通也同样重要。如果团队中知识不如你丰富的人觉得向你提问有障碍，那就有问题了。如何取得恰当的平衡，是一门艺术。

------

> [^4]:  I do, however, acknowledge that serious introverts likely need more peace, quiet, and alone time than most people and might benefit from a quieter environment, if not their own office.  
         不过，我也承认，性格非常内向的人可能比大多数人更需要安宁、静谧和独处的时间。即使没有独立办公室，更安静的环境也可能对他们有益。

### In Short, Don’t Hide 总之，不要躲起来

So, what “hiding” boils down to is this: working alone is inherently riskier than working with others. Even though you might be afraid of someone stealing your idea or thinking you’re not intelligent, you should be much more concerned about wasting huge swaths of your time toiling away on the wrong thing.

Don’t become another statistic.

所以，关于“躲起来工作”，归根结底就是：独自工作的风险本就高于与人合作。你也许担心别人窃取想法，或觉得你不够聪明，但更该担心的是，把大量时间耗费在错误的方向上。

不要再添一个这样的失败案例。

## It’s All About the Team 关键在于团队

So, let’s back up now and put all of these ideas together.

现在，让我们回过头来，把这些观点串起来。

The point we’ve been hammering away at is that, in the realm of programming, lone craftspeople are extremely rare—and even when they do exist, they don’t perform superhuman achievements in a vacuum; their world-changing accomplishment is almost always the result of a spark of inspiration followed by a heroic team effort.

我们反复强调的是：在编程领域，单打独斗的高手极为罕见。即使有，他们也不是在与世隔绝的情况下取得非凡成就的。那些改变世界的成果，几乎总是始于灵感，再由团队付出巨大努力才得以实现。

A great team makes brilliant use of its superstars, but the whole is always greater than the sum of its parts. But creating a superstar team is fiendishly difficult.

优秀的团队能充分发挥明星成员的才华，而团队整体的力量总是大于成员力量之和。不过，打造一支明星团队极其困难。

Let’s put this idea into simpler words: software engineering is a team endeavor.

说得更简单些：软件工程需要团队协作。

This concept directly contradicts the inner Genius Programmer fantasy so many of us hold, but it’s not enough to be brilliant when you’re alone in your hacker’s lair. You’re not going to change the world or delight millions of computer users by hiding and preparing your secret invention. You need to work with other people. Share your vision. Divide the labor. Learn from others. Create a brilliant team.

这个观念与许多人心中的“天才程序员”幻想直接冲突，但独自躲在黑客的藏身处，再聪明也不够。你无法靠躲起来秘密准备一项发明，就改变世界或让数百万计算机用户满意。你需要与人协作，分享愿景，分担工作，向别人学习，打造出色的团队。

Consider this: how many pieces of widely used, successful software can you name that were truly written by a single person? (Some people might say “LaTeX,” but it’s hardly “widely used,” unless you consider the number of people writing scientific papers to be a statistically significant portion of all computer users!)

想一想：在那些广泛使用、取得成功的软件中，你能说出几款真正由一个人编写的软件？（有人可能会说“LaTeX”，但它很难算得上“广泛使用”，除非你认为撰写科学论文的人在所有计算机用户中占了统计意义上足够大的比例！）

High-functioning teams are gold and the true key to success. You should be aiming for this experience however you can.

运作良好的团队弥足珍贵，才是成功的真正关键。你应该尽一切可能争取这样的协作体验。

### The Three Pillars of Social Interaction社交互动的三大支柱

So, if teamwork is the best route to producing great software, how does one build (or find) a great team?

既然团队协作是开发出色软件的最佳途径，该怎样建立或找到一个优秀团队呢？

To reach collaborative nirvana, you first need to learn and embrace what I call the “three pillars” of social skills. These three principles aren’t just about greasing the wheels of relationships; they’re the foundation on which all healthy interaction and collaboration are based:

*Pillar 1: Humility*  
&nbsp;&nbsp;&nbsp;&nbsp; You are not the center of the universe (nor is your code!). You’re neither omniscient nor infallible. You’re open to self-improvement.
      
*Pillar 2: Respect*  
&nbsp;&nbsp;&nbsp;&nbsp; You genuinely care about others you work with. You treat them kindly and appreciate their abilities and accomplishments.
      
*Pillar 3: Trust*  
&nbsp;&nbsp;&nbsp;&nbsp; You believe others are competent and will do the right thing, and you’re OK with letting them drive when appropriate.[^5]

要达到理想的协作状态，首先需要学习并认同我所说的社交技能“三大支柱”。这三项原则不只是人际关系的润滑剂，更是一切健康互动与协作的基础：

*支柱1：谦逊*  
&nbsp;&nbsp;&nbsp;&nbsp; 你不是宇宙的中心（你的代码也不是！）。你并非无所不知，也不可能永远不犯错。你愿意不断提升自己。
      
*支柱2：尊重*  
&nbsp;&nbsp;&nbsp;&nbsp; 你真诚地关心与你一起工作的人。你善待他们，欣赏他们的能力和成就。
      
*支柱3：信任*  
&nbsp;&nbsp;&nbsp;&nbsp; 你相信他人有能力，也会做正确的事，并且愿意在适当的时候让他们主导。

If you perform a root-cause analysis on almost any social conflict, you can ultimately trace it back to a lack of humility, respect, and/or trust. That might sound implausible at first, but give it a try. Think about some nasty or uncomfortable social situation currently in your life. At the basest level, is everyone being appropriately humble? Are people really respecting one another? Is there mutual trust?

几乎任何人际冲突，只要分析根本原因，最终都能追溯到谦逊、尊重、信任中的一项或几项有所欠缺。乍听之下也许难以置信，但不妨试一试。想想你眼下生活中某个令人不快或不舒服的人际场景。最基本的问题是：大家都足够谦逊吗？真的互相尊重吗？彼此信任吗？

> [^5]: This is incredibly difficult if you’ve been burned in the past by delegating to incompetent people.  
        如果你过去曾因把工作交给不称职的人而吃过亏，做到这一点就会格外困难。

### Why Do These Pillars Matter?为什么这些支柱很重要？

When you began this chapter, you probably weren’t planning to sign up for some sort of weekly support group. We empathize. Dealing with social problems can be difficult: people are messy, unpredictable, and often annoying to interface with. Rather than putting energy into analyzing social situations and making strategic moves, it’s tempting to write off the whole effort. It’s much easier to hang out with a predictable compiler, isn’t it? Why bother with the social stuff at all?

开始读这一章时，你大概没打算报名参加什么每周互助小组。我们理解这种心情。处理人际问题确实不容易：人很复杂，难以预测，打起交道来还常常让人心烦。与其花精力分析人际局面、考虑应对策略，人们很容易就想干脆放弃这些努力。与行为可预测的编译器打交道，岂不是轻松得多？何必费心处理人际关系？

Here’s a quote from a famous lecture by Richard Hamming:

> By taking the trouble to tell jokes to the secretaries and being a little friendly, I got superb secretarial help. For instance, one time for some idiot reason all the reproducing services at Murray Hill were tied up. Don’t ask me how, but they were. I wanted something done. My secretary called up somebody at Holmdel, hopped [into] the company car, made the hour-long trip down and got it reproduced, and then came back. It was a payoff for the times I had made an effort to cheer her up, tell her jokes and be friendly; it was that little extra work that later paid off for me. By realizing you have to use the system and studying how to get the system to do your work, you learn how to adapt the system to your desires.

以下是理查德·哈明（Richard Hamming）著名演讲中的一段话：

> 我肯花点心思给秘书们讲笑话，待人友善些，便得到了极好的秘书协助。例如，有一次不知什么荒唐原因，Murray Hill 的所有复印服务都忙得不可开交。别问我是怎么回事，反正就是如此。我有份东西需要复印。我的秘书打电话联系了 Holmdel 的一个人，坐上公司的车，花一个小时赶到那里，复印好后又带了回来。这是对我平时花心思逗她开心、给她讲笑话、友善待她的回报。正是这些额外的小小付出，后来让我受益。意识到自己必须借助组织体系，并研究怎样让它帮你完成工作，你就能学会让这个体系服务于自己的目标。

The moral is this: do not underestimate the power of playing the social game. It’s not about tricking or manipulating people; it’s about creating relationships to get things done. Relationships always outlast projects. When you’ve got richer relationships with your coworkers, they’ll be more willing to go the extra mile when you need them.

这个故事的道理是：别低估经营人际关系的力量。这不是欺骗或操纵别人，而是通过建立关系把事情做好。人际关系总比项目更长久。与同事的关系越深厚，他们就越愿意在你需要时多帮一把。

### Humility, Respect, and Trust in Practice 谦逊、尊重和信任的实践

All of this preaching about humility, respect, and trust sounds like a sermon. Let’s come out of the clouds and think about how to apply these ideas in real-life situations. We’re going to examine a list of specific behaviors and examples that you can start with. Many of them might sound obvious at first, but after you begin thinking about them, you’ll notice how often you (and your peers) are guilty of not following them—we’ve certainly noticed this about ourselves!

讲了这么多谦逊、尊重和信任，听起来难免像说教。现在回到实际，看看这些观念如何用于现实情境。下面是一系列具体的行为和例子，可以作为起点。许多做法乍看理所当然，但仔细想想，你就会发现自己和同行经常没有做到。至少，我们在自己身上就看到了不少这样的情况！

#### Lose the ego 丢掉自负

OK, this is sort of a simpler way of telling someone without enough humility to lose their ’tude. Nobody wants to work with someone who consistently behaves like they’re the most important person in the room. Even if you know you’re the wisest person in the discussion, don’t wave it in people’s faces. For example, do you always feel like you need to have the first or last word on every subject? Do you feel the need to comment on every detail in a proposal or discussion? Or do you know somebody who does these things?

说白了，就是请那些不够谦逊的人收起傲慢的态度。没人愿意与总把自己当作全场最重要人物的人共事。即使你知道自己是讨论中最有见识的人，也别在别人面前炫耀。例如，你是否总觉得每个话题都要由自己开场或作结？是否觉得提案或讨论中的每个细节都得点评一番？或者，你身边有没有这样的人？

Although it’s important to be humble, that doesn’t mean you need to be a doormat; there’s nothing wrong with self-confidence. Just don’t come off like a know-it-all. Even better, think about going for a “collective” ego, instead; rather than worrying about whether you’re personally awesome, try to build a sense of team accomplishment and group pride. For example, the Apache Software Foundation has a long history of creating communities around software projects. These communities have incredibly strong identities and reject people who are more concerned with self- promotion.

谦逊固然重要，却不意味着任人欺负。自信没有错，只是别表现得无所不知。更好的做法，是把关注点从个人转向“集体”：与其在意自己是否出色，不如培养团队成就感和集体荣誉感。例如，Apache 软件基金会长期围绕软件项目建设社区。这些社区有极强的集体认同感，不欢迎那些更在意自我宣传的人。

Ego manifests itself in many ways, and a lot of the time, it can get in the way of your productivity and slow you down. Here’s another great story from Hamming’s lecture that illustrates this point perfectly (emphasis ours):

> John Tukey almost always dressed very casually. He would go into an important office and it would take a long time before the other fellow realized that this is a first-class man and he had better listen. For a long time, John has had to overcome this kind of hostility. It’s wasted effort! I didn’t say you should conform; I said, “The appearance of conforming gets you a long way.” If you chose to assert your ego in any number of ways, “I am going to do it my way,” you pay a small steady price throughout the whole of your professional career. And this, over a whole lifetime, adds up to an enormous amount of needless trouble. […] By realizing you have to use the system and studying how to get the system to do your work, you learn how to adapt the system to your desires. Or you can fight it steadily, as a small, undeclared war, for the whole of your life.

自负有许多表现形式，常常会妨碍你的工作效率，拖慢进度。Hamming 演讲中的另一个精彩故事很好地说明了这一点（强调为本书作者所加）：

> John Tukey 几乎总是穿得很随意。他走进重要人物的办公室，对方往往要过好一会儿才意识到，眼前是位一流人才，最好认真听他说话。长期以来，约翰不得不克服这种敌意。这些力气完全是白费！我不是说你应该随波逐流，而是说：“表面上合群，就能让你走得很远。”如果你处处都要彰显自我，坚持“我就要按自己的方式做”，就会在整个职业生涯中不断付出小小的代价。积累一生，便是大量本可避免的麻烦。[…]意识到自己必须借助组织体系，并研究怎样让它帮你完成工作，你就能学会让这个体系服务于自己的目标。另一种选择，则是终其一生都与它对抗，打一场小规模的不宣之战。

#### Learn to give and take criticism 学会提出和接受建设性批评

A few years ago, Joe started a new job as a programmer. After his first week, he really began digging into the codebase. Because he cared about what was going on, he started gently questioning other teammates about their contributions. He sent simple code reviews by email, politely asking about design assumptions or pointing out places where logic could be improved. After a couple of weeks, he was summoned to his director’s office. “What’s the problem?” Joe asked. “Did I do something wrong?” The director looked concerned: “We’ve had a lot of complaints about your behavior, Joe. Apparently, you’ve been really harsh toward your teammates, criticizing them left and right. They’re upset. You need to tone it down.” Joe was utterly baffled. Surely, he thought, his code reviews should have been welcomed and appreciated by his peers. In this case, however, Joe should have been more sensitive to the team’s widespread insecurity and should have used a subtler means to introduce code reviews into the culture—perhaps even something as simple as discussing the idea with the team in advance and asking team members to try it out for a few weeks.

几年前，乔换了一份程序员工作。入职一周后，他开始深入研究代码库。他很关心团队的工作，于是语气温和地向队友询问各自编写的代码，并通过电子邮件发送简短的代码审查意见，礼貌地询问设计假设，或指出逻辑可以改进的地方。几周后，他被叫到主管办公室。“怎么了？”乔问，“我做错什么了吗？”主管显得很担忧：“乔，我们收到很多关于你言行的投诉。听说你对队友很苛刻，动不动就批评他们。大家很不高兴。你得收敛一些。”乔完全摸不着头脑。他原以为，自己的代码审查理应受到同行欢迎和赞赏。但在这种情况下，乔应当更留意团队普遍存在的不安全感，用更委婉的方式把代码审查引入团队文化。也许只要事先与团队讨论这个想法，请大家试行几周，就足够了。

In a professional software engineering environment, criticism is almost never personal—it’s usually just part of the process of making a better project. The trick is to make sure you (and those around you) understand the difference between a constructive criticism of someone’s creative output and a flat-out assault against someone’s character. The latter is useless—it’s petty and nearly impossible to act on. The former can (and should!) be helpful and give guidance on how to improve. And, most important, it’s imbued with respect: the person giving the constructive criticism genuinely cares about the other person and wants them to improve themselves or their work. Learn to respect your peers and give constructive criticism politely. If you truly respect someone, you’ll be motivated to choose tactful, helpful phrasing—a skill acquired with much practice. We cover this much more in Chapter 9.

在专业的软件工程环境中，批评几乎从不针对个人，通常只是改进项目的一部分。关键是确保自己和身边的人都能区分：对创作成果提出建设性批评，与直接攻击一个人的品格，并不是一回事。后者毫无用处，既狭隘，也几乎无法据此改进。前者则可以，而且应该，提供帮助和改进方向。最重要的是，建设性批评包含着尊重：提出批评的人真正关心对方，希望对方或其工作变得更好。要学会尊重同行，礼貌地提出建设性批评。真正尊重一个人，就会愿意选择得体、有帮助的措辞，而这需要大量练习。第9章会更详细地讨论这一点。

On the other side of the conversation, you need to learn to accept criticism as well. This means not just being humble about your skills, but trusting that the other person has your best interests (and those of your project!) at heart and doesn’t actually think you’re an idiot. Programming is a skill like anything else: it improves with practice. If a peer pointed out ways in which you could improve your juggling, would you take it as an attack on your character and value as a human being? We hope not. In the same way, your self-worth shouldn’t be connected to the code you write—or any creative project you build. To repeat ourselves: you are not your code. Say that over and over. You are not what you make. You need to not only believe it yourself, but get your coworkers to believe it, too.

反过来，你也要学会接受批评。这不仅意味着对自己的技能保持谦逊，还要相信对方是为你和项目着想，而不是真的觉得你是个白痴。编程与其他技能一样，都能通过练习提高。如果同伴指出你的杂耍技艺还有哪些改进空间，你会觉得这是在攻击你的人格和个人价值吗？希望不会。同样，你的自我价值也不应与你编写的代码或完成的任何创造性项目绑在一起。再说一遍：你不等于你的代码。把这句话多念几遍。你不等于自己的作品。不仅你自己要相信这一点，还要让同事也相信。

For example, if you have an insecure collaborator, here’s what not to say: “Man, you totally got the control flow wrong on that method there. You should be using the standard xyzzy code pattern like everyone else.” This feedback is full of antipatterns: you’re telling someone they’re “wrong” (as if the world were black and white), demanding they change something, and accusing them of creating something that goes against what everyone else is doing (making them feel stupid). Your coworker will immediately be put on the offense, and their response is bound to be overly emotional.

例如，面对缺乏安全感的合作者，不要这样说：“伙计，你把那个方法的控制流完全搞错了。你应该和大家一样，用标准的 xyzzy 代码模式。”这样的反馈处处都是反面示范：断言对方“错了”，仿佛世界非黑即白；要求对方修改；还指责对方的做法与所有人都不一样，让人觉得自己很蠢。同事会立刻进入反击状态，反应也难免过于情绪化。

A better way to say the same thing might be, “Hey, I’m confused by the control flow in this section here. I wonder if the xyzzy code pattern might make this clearer and easier to maintain?” Notice how you’re using humility to make the question about you, not them. They’re not wrong; you’re just having trouble understanding the code. The suggestion is merely offered up as a way to clarify things for poor little you while possibly helping the project’s long-term sustainability goals. You’re also not demanding anything—you’re giving your collaborator the ability to peacefully reject the suggestion. The discussion stays focused on the code itself, not on anyone’s value or coding skills.

同样的意思，可以换一种更好的说法：“嘿，这部分的控制流我有些没看懂。用 xyzzy 代码模式，会不会更清晰，也更容易维护？”注意，这种谦逊的表达把问题放在自己身上，而不是对方身上。不是对方错了，只是你没能理解代码。建议只是为了帮可怜的你看懂代码，同时也可能有助于项目的长期可持续性。你也没有强求什么，合作者可以平和地拒绝建议。这样，讨论就始终围绕代码本身，而不是任何人的价值或编程能力。

#### Fail fast and iterate 快速失败并持续迭代

There’s a well-known urban legend in the business world about a manager who makes a mistake and loses an impressive $10 million. He dejectedly goes into the office the next day and starts packing up his desk, and when he gets the inevitable “the 
wants to see you in his office” call, he trudges into the CEO’s office and quietly slides a piece of paper across the desk.  
“What’s this?” asks the CEO.  
“My resignation,” says the executive. “I assume you called me in here to fire me.”  
“Fire you?” responds the CEO, incredulously. “Why would I fire you? I just spent $10 million training you!”[^6]  

商界流传着一个著名的故事：一位经理犯错，造成了高达1000万美元的损失。第二天，他垂头丧气地来到办公室，开始收拾桌子。果然，他接到了“CEO让你去他办公室”的电话。他迈着沉重的步子走进 CEO 办公室，默默地把一张纸推过桌面。  
“这是什么？”CEO 问。  
“我的辞呈，”经理说，“我想您叫我来，是要解雇我。”  
“解雇你？”首席执行官难以置信地反问，“我为什么要解雇你？我刚花了1000万美元培训你！”

It’s an extreme story, to be sure, but the CEO in this story understands that firing the executive wouldn’t undo the $10 million loss, and it would compound it by losing a valuable executive who he can be very sure won’t make that kind of mistake again.

这个故事确实有些极端，但其中的首席执行官明白，解雇这位高管既挽回不了1000万美元的损失，还会雪上加霜：公司又失去了一位有价值的高管，而他几乎可以确信，此人不会再犯同样的错误。

At Google, one of our favorite mottos is that “Failure is an option.” It’s widely recognized that if you’re not failing now and then, you’re not being innovative enough or taking enough risks. Failure is viewed as a golden opportunity to learn and improve for the next go-around.[^7] In fact, Thomas Edison is often quoted as saying, “If I find 10,000 ways something won’t work, I haven’t failed. I am not discouraged, because every wrong attempt discarded is another step forward.”

在谷歌，我们最喜欢的格言之一是“失败也是一种选择”。大家普遍认为，如果你连偶尔的失败都没有，说明创新或冒险还不够。失败是学习的宝贵机会，能帮助我们在下次尝试时做得更好。人们常引用托马斯·爱迪生的一句话：“如果我发现了10,000种行不通的方法，那并不意味着我失败了。我不会气馁，因为每排除一种错误的尝试，就又向前迈了一步。”

Over in Google X—the division that works on “moonshots” like self-driving cars and internet access delivered by balloons—failure is deliberately built into its incentive system. People come up with outlandish ideas and coworkers are actively encouraged to shoot them down as fast as possible. Individuals are rewarded (and even compete) to see how many ideas they can disprove or invalidate in a fixed period of time. Only when a concept truly cannot be debunked at a whiteboard by all peers does it proceed to early prototype.

谷歌 X 部门负责自动驾驶汽车、利用气球提供互联网接入等“登月计划”，还特意把失败纳入激励机制。大家提出异想天开的点子，同时鼓励同事尽快找出这些点子行不通的理由。大家会因为在规定时间内证伪或排除想法而获得奖励，甚至互相竞争，看谁排除得更多。只有当所有同行在白板前讨论后，都确实找不出一个构想行不通的理由，它才会进入早期原型阶段。

> [^6]: You can find a dozen variants of this legend on the web, attributed to different famous managers.  
        网上能找到这个传闻的十几种版本，分别被说成是不同知名经理人的故事。

> [^7]: By the same token, if you do the same thing over and over and keep failing, it’s not failure, it’s incompetence.  
        同样的道理，如果你一次又一次地做同样的事情，却不断失败，那不是失败，而是无能。

### Blameless Post-Mortem Culture 无责复盘文化

The key to learning from your mistakes is to document your failures by performing a root-cause analysis and writing up a “postmortem,” as it’s called at Google (and many other companies). Take extra care to make sure the postmortem document isn’t just a useless list of apologies or excuses or finger-pointing—that’s not its purpose. A proper postmortem should always contain an explanation of what was learned and what is going to change as a result of the learning experience. Then, make sure that the postmortem is readily accessible and that the team really follows through on the proposed changes. Properly documenting failures also makes it easier for other people (present and future) to know what happened and avoid repeating history. Don’t erase your tracks—light them up like a runway for those who follow you!

从错误中学习，关键在于分析根本原因，并把失败记录下来。在谷歌及许多其他公司，这份记录称为“事后总结”（译注：国内称为复盘）。务必注意，复盘文档不能只是一份毫无用处的道歉、借口或指责清单，那不是它的目的。合格的复盘必须说明学到了什么，以及据此要作出哪些改变。随后，还要确保文档便于查阅，团队也确实落实了改进措施。妥善记录失败，能让现在和未来的其他人更容易了解事情经过，避免重蹈覆辙。不要抹去自己的足迹，而要像照亮跑道一样，让后来者看清这些足迹！

A good postmortem should include the following:

- A brief summary of the event
- A timeline of the event, from discovery through investigation to resolution
- The primary cause of the event
- Impact and damage assessment
- A set of action items (with owners) to fix the problem immediately
- A set of action items to prevent the event from happening again
- Lessons learned

一份好的复盘文档应包括：

- 事件的简要概述
- 事件时间线，涵盖发现、调查直至解决的全过程
- 事件的主要原因
- 影响和损害评估
- 立即解决问题的行动项，并明确各项负责人
- 防止事件再次发生的行动项
- 经验教训

#### Learn patience 培养耐心

Years ago, I was writing a tool to convert CVS repositories to Subversion (and later, Git). Due to the vagaries of CVS, I kept unearthing bizarre bugs. Because my longtime friend and coworker Karl knew CVS quite intimately, we decided we should work together to fix these bugs.

多年前，我编写了一个把 CVS 代码仓库转换为 Subversion 仓库的工具，后来又支持转换为 Git 仓库。由于 CVS 行为多变，我不断遇到稀奇古怪的缺陷。我的老朋友兼同事 Karl 对 CVS 十分熟悉，于是我们决定一起修复这些问题。

A problem arose when we began pair programming: I’m a bottom-up engineer who is content to dive into the muck and dig my way out by trying a lot of things quickly and skimming over the details. Karl, however, is a top-down engineer who wants to get the full lay of the land and dive into the implementation of almost every method on the call stack before proceeding to tackle the bug. This resulted in some epic interpersonal conflicts, disagreements, and the occasional heated argument. It got to the point at which the two of us simply couldn’t pair-program together: it was too frustrating for us both.

开始结对编程后，问题出现了。我习惯自下而上，喜欢直接钻进问题里，快速尝试各种办法，略过细节，摸索出路。Karl 却习惯自上而下，希望先看清全貌，深入了解调用栈上几乎每个方法的实现，再着手处理缺陷。我们因此产生了严重的人际冲突和分歧，偶尔还会激烈争吵。最后，两个人简直没法继续结对编程，因为彼此都太受挫了。

That said, we had a longstanding history of trust and respect for each other. Combined with patience, this helped us work out a new method of collaborating. We would sit together at the computer, identify the bug, and then split up and attack the problem from two directions at once (top-down and bottom-up) before coming back together with our findings. Our patience and willingness to improvise new working styles not only saved the project, but also our friendship.

不过，我们长期以来一直相互信任、相互尊重。加上一些耐心，我们摸索出了一种新的协作方式：先一起坐在电脑前确认缺陷，再分头从两个方向同时分析问题，一个自上而下，一个自下而上，最后带着各自的发现重新汇合。正是这份耐心，以及尝试新工作方式的意愿，不仅挽救了项目，也挽救了我们的友谊。

#### Be open to influence 乐于接受他人的影响

The more open you are to influence, the more you are able to influence; the more vulnerable you are, the stronger you appear. These statements sound like bizarre contradictions. But everyone can think of someone they’ve worked with who is just maddeningly stubborn—no matter how much people try to persuade them, they dig their heels in even more. What eventually happens to such team members? In our experience, people stop listening to their opinions or objections; instead, they end up “routing around” them like an obstacle everyone takes for granted. You certainly don’t want to be that person, so keep this idea in your head: it’s OK for someone else to change your mind. In the opening chapter of this book, we said that engineering is inherently about trade-offs. It’s impossible for you to be right about everything all the time unless you have an unchanging environment and perfect knowledge, so of course you should change your mind when presented with new evidence. Choose your battles carefully: to be heard properly, you first need to listen to others. It’s better to do this listening before putting a stake in the ground or firmly announcing a decision—if you’re constantly changing your mind, people will think you’re wishy-washy.

越愿意接受他人的影响，你就越能影响他人；越敢于袒露不足，反而越显得强大。这些话听起来似乎自相矛盾。不过，每个人大概都共事过那种固执得让人抓狂的人：别人越劝，他们越不肯让步。这样的队友最终会怎样？根据我们的经验，大家会不再听取他们的意见或反对理由，转而像绕过一个早已习惯的障碍那样，绕开他们。你当然不想成为这样的人，所以请记住：让别人改变你的想法，没有什么不好。本书开篇就说过，工程本质上离不开权衡。除非环境永不变化，而你又掌握了全部知识，否则不可能事事时时都对。因此，有了新证据，当然应该调整看法。要慎重选择哪些事值得争论：想让别人认真听你说，先得认真听别人说。最好在表明立场或明确宣布决定之前就这样做，否则反复改主意，会让人觉得你摇摆不定。

The idea of vulnerability can seem strange, too. If someone admits ignorance of the topic at hand or the solution to a problem, what sort of credibility will they have in a group? Vulnerability is a show of weakness, and that destroys trust, right?

袒露不足这个想法，听起来也许同样奇怪。如果一个人承认不了解眼前的话题，或不知道问题的解法，他在团队里还会有多少公信力？暴露弱点不就是示弱，会破坏信任，对吗？

Not true. Admitting that you’ve made a mistake or you’re simply out of your league can increase your status over the long run. In fact, the willingness to express vulnerability is an outward show of humility, it demonstrates accountability and the willingness to take responsibility, and it’s a signal that you trust others’ opinions. In return, people end up respecting your honesty and strength. Sometimes, the best thing you can do is just say, “I don’t know.”

并非如此。承认自己犯了错，或眼前的事情超出了自己的能力，反而可能提高你长期的威信。愿意袒露不足，本身就是谦逊的表现，既体现责任感和担当，也表明你信任他人的意见。人们反过来会尊重你的诚实和勇气。有时，最好的做法就是坦言：“我不知道。”

Professional politicians, for example, are notorious for never admitting error or ignorance, even when it’s patently obvious that they’re wrong or unknowledgeable about a subject. This behavior exists primarily because politicians are constantly under attack by their opponents, and it’s why most people don’t believe a word that politicians say. When you’re writing software, however, you don’t need to be continually on the defensive—your teammates are collaborators, not competitors. You all have the same goal.

例如，职业政客出了名地不肯承认错误或无知，即使他们明显错了，或显然不了解某个话题，也不例外。这主要是因为他们不断受到对手攻击，也正因此，大多数人对政客的话一个字都不信。但编写软件时，你不必时刻防备：队友是合作者，而不是竞争对手，你们有着共同的目标。

### Being Googley  具备谷歌特质

At Google, we have our own internal version of the principles of “humility, respect, and trust” when it comes to behavior and human interactions.

对于行为和人际交往，谷歌内部也有一套自己的“谦逊、尊重和信任”原则。

From the earliest days of our culture, we often referred to actions as being “Googley” or “not Googley.” The word was never explicitly defined; rather, everyone just sort of took it to mean “don’t be evil” or “do the right thing” or “be good to each other.” Over time, people also started using the term “Googley” as an informal test for culture-fit whenever we would interview a candidate for an engineering job, or when writing internal performance reviews of one another. People would often express opinions about others using the term; for example, “the person coded well, but didn’t seem to have a very Googley attitude.”

在谷歌文化形成之初，我们就常用“Googley”或“不 Googley”来评价某种行为。这个词从未有过明确定义，大家只是大致把它理解为“不作恶”“做正确的事”或“善待彼此”。后来，在面试工程岗位候选人，或为同事撰写内部绩效评价时，人们也开始用“Googley”作为非正式的文化契合度标准。大家常用它来评价别人，例如：“这个人代码写得不错，但态度似乎不太 Googley。”

Of course, we eventually realized that the term “Googley” was being overloaded with meaning; worse yet, it could become a source of unconscious bias in hiring or evaluations. If “Googley” means something different to every employee, we run the risk of the term starting to mean “is just like me.” Obviously, that’s not a good test for hiring
—we don’t want to hire people “just like me,” but people from a diverse set of backgrounds and with different opinions and experiences. An interviewer’s personal desire to have a beer with a candidate (or coworker) should never be considered a valid signal about somebody else’s performance or ability to thrive at Google.

我们最终意识到，“Googley”被赋予了太多含义。更糟的是，它还可能成为招聘或评价中无意识偏见的来源。如果每名员工对这个词的理解都不同，它就可能逐渐变成“和我一样”的代名词。这显然不是好的招聘标准：我们不想招“和我一样”的人，而是希望招到背景、观点和经历各不相同的人。面试官是否愿意与候选人或同事喝一杯，绝不能作为判断对方表现或能否在谷歌取得成功的有效依据。

Google eventually fixed the problem by explicitly defining a rubric for what we mean by “Googleyness”—a set of attributes and behaviors that we look for that represent strong leadership and exemplify “humility, respect, and trust”:

- *Thrives in ambiguity*  
    Can deal with conflicting messages or directions, build consensus, and make progress against a problem, even when the environment is constantly shifting.
- *Values feedback*  
    Has humility to both receive and give feedback gracefully and understands how valuable feedback is for personal (and team) development.
- *Challenges status quo*  
    Is able to set ambitious goals and pursue them even when there might be resistance or inertia from others.
- *Puts the user first*  
    Has empathy and respect for users of Google’s products and pursues actions that are in their best interests.
- *Cares about the team*  
    Has empathy and respect for coworkers and actively works to help them without being asked, improving team cohesion.
- *Does the right thing*  
    Has a strong sense of ethics about everything they do; willing to make difficult or inconvenient decisions to protect the integrity of the team and product.

谷歌最终通过明确定义“谷歌特质”（Googleyness）的评价标准，解决了这个问题。这是一组我们看重的特质和行为，既体现出色的领导力，也践行“谦逊、尊重和信任”：

- *在不确定中有所作为*  
    即使环境不断变化，也能应对相互冲突的信息或指示，建立共识，推动问题的解决。
- *重视反馈*  
    以谦逊、得体的态度接受和给出反馈，理解反馈对个人和团队成长的价值。
- *挑战现状*  
    能够设定远大目标，并付诸追求，即使可能遇到他人的阻力或惯性也不退缩。
- *用户第一*  
    理解并尊重谷歌产品的用户，采取最符合用户利益的行动。
- *关心团队*  
    理解并尊重同事，无需别人开口就主动提供帮助，增强团队凝聚力。
- *做正确的事*  
    凡事都有强烈的道德意识，愿意为维护团队和产品的诚信，作出艰难或会带来不便的决定。

Now that we have these best-practice behaviors better defined, we’ve begun to shy away from using the term “Googley.” It’s always better to be specific about expectations!

如今，对这些良好行为有了更明确的定义，我们也开始少用“Googley”这个词。把期望说具体，总是更好。

## Conclusion 结论

The foundation for almost any software endeavor—of almost any size—is a well- functioning team. Although the Genius Myth of the solo software developer still persists, the truth is that no one really goes it alone. For a software organization to stand the test of time, it must have a healthy culture, rooted in humility, trust, and respect that revolves around the team, rather than the individual. Further, the creative nature of software development requires that people take risks and occasionally fail; for people to accept that failure, a healthy team environment must exist.

几乎所有软件工作，无论规模大小，都以运作良好的团队为基础。虽然独行软件开发者的“天才神话”依然存在，但事实上，没有人真正单凭自己完成一切。软件组织要经得起时间考验，就必须有健康的文化，以谦逊、信任和尊重为根基，以团队而非个人为中心。此外，软件开发的创造性决定了人们需要承担风险，偶尔也会失败。要让大家接受这种失败，就必须营造健康的团队环境。

## TL;DRs  内容提要

- Be aware of the trade-offs of working in isolation.
- Acknowledge the amount of time that you and your team spend communicating and in interpersonal conflict. A small investment in understanding personalities and working styles of yourself and others can go a long way toward improving productivity.
- If you want to work effectively with a team or a large organization, be aware of your preferred working style and that of others.

- 认识到独自工作涉及的权衡。
- 留意自己和团队在沟通及人际冲突上花了多少时间。稍花些心思了解自己和他人的个性、工作方式，就能显著提高工作效率。
- 要在团队或大型组织中有效协作，就要了解自己和他人偏好的工作方式。
