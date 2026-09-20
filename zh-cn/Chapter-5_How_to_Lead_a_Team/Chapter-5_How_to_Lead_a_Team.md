
**CHAPTER 5**

# How to Lead a Team

# 第五章 如何领导团队

**Written by Brian Fitzpatrick**

**Edited by Riona MacNamara**

We’ve covered a lot of ground so far on the culture and composition of teams writing software, and in this chapter, we’ll take a look at the person ultimately responsible for making it all work.

前面几章已经详细讨论了软件开发团队的文化和组成。本章将介绍最终负责让团队顺利运作的人。

No team can function well without a leader, especially at Google, where engineering is almost exclusively a team endeavor. At Google, we recognize two different leadership roles. A *Manager* is a leader of people, whereas a *Tech Lead* leads technology efforts. Although the responsibilities of these two roles require similar planning skills, they require quite different people skills.

没有领导者，任何团队都无法良好运作。在谷歌尤其如此，因为工程工作几乎完全依靠团队协作。谷歌区分两种领导角色：*经理*负责带人，*技术负责人*负责领导技术工作。这两个角色需要相近的规划能力，但对人际交往能力的要求却很不一样。

A boat without a captain is nothing more than a floating waiting room: unless someone grabs the rudder and starts the engine, it’s just going to drift along aimlessly with the current. A piece of software is just like that boat: if no one pilots it, you’re left with a group of engineers burning up valuable time, just sitting around waiting for something to happen (or worse, still writing code that you don’t need). Although this chapter is about people management and technical leadership, it is still worth a read if you’re an individual contributor because it will likely help you understand your own leaders a bit better.

没有船长的船，不过是漂在水上的等候室：除非有人掌舵并启动引擎，否则它只会漫无目的地随波逐流。软件也像这样一艘船。如果没人掌舵，一群工程师就只能耗费宝贵的时间，坐等事情发生；更糟的是，他们可能还在编写根本不需要的代码。虽然本章讨论的是人员管理和技术领导，但个人贡献者也值得一读，因为它很可能有助于你更好地理解自己的领导。

## Managers and Tech Leads (and Both)  经理、技术负责人及兼任两职者

Whereas every engineering team generally has a leader, they acquire those leaders in different ways. This is certainly true at Google; sometimes an experienced manager comes in to run a team, and sometimes an individual contributor is promoted into a leadership position (usually of a smaller team).

工程团队通常都有领导者，但领导者的产生方式各不相同。谷歌也是如此：有时由经验丰富的经理接手团队，有时则将个人贡献者提拔到领导岗位，通常先让他们带较小的团队。

In nascent teams, both roles will sometimes be filled by the same person: a *Tech Lead Manager* (TLM). On larger teams, an experienced people manager will step in to take on the management role while a senior engineer with extensive experience will step into the tech lead role. Even though manager and tech lead each play an important part in the growth and productivity of an engineering team, the people skills required to succeed in each role are wildly different.

在新组建的团队中，这两个角色有时由同一人担任，称为*技术负责人兼经理*（TLM）。在较大的团队中，通常由具备人员管理经验的经理承担管理职责，由经验丰富的高级工程师担任技术负责人。经理和技术负责人都对工程团队的成长和生产力起着重要作用，但要胜任这两个角色，所需的人际交往能力却大不相同。

### The Engineering Manager  工程经理

Many companies bring in trained people managers who might know little to nothing about software engineering to run their engineering teams. Google decided early on, however, that its software engineering managers should have an engineering background. This meant hiring experienced managers who used to be software engineers, or training software engineers to be managers (more on this later).

许多公司聘请受过专业训练的人员管理者来带领工程团队，这些人可能对软件工程知之甚少，甚至一无所知。谷歌却很早就决定，软件工程经理应当具备工程背景。因此，谷歌要么聘请曾做过软件工程师的资深经理，要么将软件工程师培养成经理，后文会进一步讨论这一点。

At the highest level, an engineering manager is responsible for the performance, productivity, and happiness of every person on their team—including their tech lead— while still making sure that the needs of the business are met by the product for which they are responsible. Because the needs of the business and the needs of individual team members don’t always align, this can often place a manager in a difficult position.

从总体职责来看，工程经理要对团队中每个人的绩效、生产力和幸福感负责，包括技术负责人；同时，还要确保所负责的产品满足业务需求。业务需求与团队成员的个人需求并不总是一致，这往往让经理陷入两难。

### The Tech Lead  技术负责人

The tech lead (TL) of a team—who will often report to the manager of that team—is responsible for (surprise!) the technical aspects of the product, including technology decisions and choices, architecture, priorities, velocity, and general project management (although on larger teams they might have program managers helping out with this). The TL will usually work hand in hand with the engineering manager to ensure that the team is adequately staffed for their product and that engineers are set to work on tasks that best match their skill sets and skill levels. Most TLs are also individual contributors, which often forces them to choose between doing something quickly themselves or delegating it to a team member to do (sometimes) more slowly. The latter is most often the correct decision for the TL as they grow the size and capability of their team.

团队的技术负责人（TL）通常向本团队的经理汇报，负责的自然是产品的技术工作，包括技术决策与选型、架构、优先级、推进速度和整体项目管理。在较大的团队中，可能有项目经理协助管理项目。TL 通常与工程经理紧密合作，确保团队配备足够的人员来开发产品，并将任务分配给技能组合和能力水平最匹配的工程师。大多数 TL 同时也是个人贡献者，因此常常需要作出选择：是自己迅速完成工作，还是交给团队成员去做，即使对方有时会慢一些？要扩大团队规模、提升团队能力，TL 通常应当选择后者。

### The Tech Lead Manager  技术负责人兼经理

On small and nascent teams for which engineering managers need a strong technical skill set, the default is often to have a TLM: a single person who can handle both the people and technical needs of their team. Sometimes, a TLM is a more senior person, but more often than not, the role is taken on by someone who was, until recently, an individual contributor.

在规模较小、刚组建的团队中，工程经理需要很强的技术能力，因此通常会设置 TLM（技术负责人兼经理），由一人同时满足团队在人员管理和技术方面的需求。这个角色有时由较资深的人担任，但更多时候，担任者直到不久前还是个人贡献者。

At Google, it’s customary for larger, well-established teams to have a pair of leaders— one TL and one engineering manager—working together as partners. The theory is that it’s really difficult to do both jobs at the same time (well) without completely burning out, so it’s better to have two specialists crushing each role with dedicated focus.

在谷歌，规模较大、运作成熟的团队通常由两位领导搭档带领：一位 TL（技术负责人）和一位工程经理。这样安排的理由是，一个人很难同时做好这两份工作而不耗尽精力，因此不如让两位各有所长的人分别专注于一个角色，把各自的工作做好。

The job of TLM is a tricky one and often requires the TLM to learn how to balance individual work, delegation, and people management. As such, it usually requires a high degree of mentoring and assistance from more experienced TLMs. (In fact, we recommend that in addition to taking a number of classes that Google offers on this subject, a newly minted TLM seek out a senior mentor who can advise them regularly as they grow into the role.)

TLM（技术负责人兼经理）的工作并不容易，通常需要学会在亲自完成工作、委派任务和人员管理之间取得平衡。因此，TLM 往往需要更有经验的同行给予充分的指导和帮助。（事实上，我们建议新任 TLM 除了参加谷歌提供的相关课程，还应寻找一位资深导师，在自己逐渐适应这个角色的过程中，定期听取导师的建议。）

-----

#### Case Study: Influencing Without Authority  案例研究：不靠职权发挥影响力

It’s generally accepted that you can get folks who report to you to do the work that you need done for your products, but it’s different when you need to get people outside of your organization—or heck, even outside of your product area sometimes—to do something that you think needs to be done. This “influence without authority” is one of the most powerful leadership traits that you can develop.

人们通常认为，你可以要求向你汇报的人完成产品所需的工作。但如果你需要组织之外，甚至产品领域之外的人去做你认为有必要的事，情况就不同了。这种“不靠职权发挥影响力”的能力，是你可以培养的最有力量的领导特质之一。

For example, for years, Jeff Dean, senior engineering fellow and possibly the most well-known Googler *inside* of Google, led only a fraction of Google’s engineering team, but his influence on technical decisions and direction reaches to the ends of the entire engineering organization and beyond (thanks to his writing and speaking outside of the company).

例如，高级工程研究员杰夫·迪安（Jeff Dean）可能是谷歌内部最知名的 Googler。多年来，他直接领导的工程团队只占谷歌的一小部分，但他对技术决策和方向的影响遍及整个工程组织，并凭借对外发表的文章和演讲，延伸到公司之外。

Another example is a team that I started called The Data Liberation Front: with a team of less than a half-dozen engineers, we managed to get more than 50 Google products to export their data through a product that we launched called Google Takeout. At the time, there was no formal directive from the executive level at Google for all products to be a part of Takeout, so how did we get hundreds of engineers to contribute to this effort? By identifying a strategic need for the company, showing how it linked to the mission and existing priorities of the company, and working with a small group of engineers to develop a tool that allowed teams to quickly and easily integrate with Takeout.

另一个例子是我创建的“数据解放阵线”团队。团队不到六名工程师，却成功让50多个谷歌产品通过我们推出的 Google Takeout 导出数据。当时，谷歌高层并未正式要求所有产品接入 Takeout，我们是怎么让数百名工程师参与这项工作的呢？我们找出了公司的一个战略需求，说明它与公司使命和现有优先事项的联系，并与一小组工程师合作开发工具，让各团队能够快速、轻松地接入 Takeout。

-----

## Moving from an Individual Contributor Role to a Leadership Role  从个人贡献者角色转变为领导角色

Whether or not they’re officially appointed, someone needs to get into the driver’s seat if your product is ever going to go anywhere, and if you’re the motivated, impatient type, that person might be you. You might find yourself sucked into helping your team resolve conflicts, make decisions, and coordinate people. It happens all the time, and often by accident. Maybe you never intended to become a “leader,” but somehow it happened anyway. Some people refer to this affliction as “manageritis.”

要让产品有所进展，就得有人掌舵，不论这个人是否得到正式任命。如果你做事主动，又等不及别人行动，这个人可能就是你。你可能不知不觉就开始帮助团队解决冲突、作出决策、协调人员。这种情况很常见，而且往往出于偶然。也许你从没想过要成为“领导者”，却不知怎么就走上了这个岗位。有些人把这称为患上了“经理病”。

Even if you’ve sworn to yourself that you’ll never become a manager, at some point in your career, you’re likely to find yourself in a leadership position, especially if you’ve been successful in your role. The rest of this chapter is intended to help you understand what to do when this happens.

即使你发誓绝不当经理，也很可能在职业生涯的某个阶段走上领导岗位，尤其是当你在原有岗位上表现出色时。本章其余部分将帮助你了解，到那时该怎么做。

We’re not here to attempt to convince you to become a manager, but rather to help show why the best leaders work to serve their team using the principles of humility, respect, and trust. Understanding the ins and outs of leadership is a vital skill for influencing the direction of your work. If you want to steer the boat for your project and not just go along for the ride, you need to know how to navigate, or you’ll run yourself (and your project) onto a sandbar.

我们并不是要说服你当经理，而是想说明，为什么最好的领导者会秉持谦逊、尊重和信任的原则为团队服务。要影响工作的方向，理解领导工作的方方面面是一项重要能力。如果你想为项目掌舵，而不只是搭顺风船，就得懂得如何导航，否则你和项目都会搁浅。

### The Only Thing to Fear Is…Well, Everything  唯一可怕的是……嗯，一切

Aside from the general sense of malaise that most people feel when they hear the word “manager,” there are a number of reasons that most people don’t want to become managers. The biggest reason you’ll hear in the software development world is that you spend much less time writing code. This is true whether you become a TL or an engineering manager, and I’ll talk more about this later in the chapter, but first, let’s cover some more reasons why most of us avoid becoming managers.

大多数人听到“经理”这个词就有些不自在，此外，还有许多理由让人不愿当经理。在软件开发领域，最常听到的主要原因是：写代码的时间会少得多。无论担任 TL 还是工程经理，情况都是如此，后文还会详细讨论。现在先看看，我们大多数人为什么还会回避经理这个角色。

If you’ve spent the majority of your career writing code, you typically end a day with something you can point to—whether it’s code, a design document, or a pile of bugs you just closed—and say, “That’s what I did today.” But at the end of a busy day of “management,” you’ll usually find yourself thinking, “I didn’t do a damned thing today.” It’s the equivalent of spending years counting the number of apples you picked each day and changing to a job growing bananas, only to say to yourself at the end of each day, “I didn’t pick any apples,” happily ignoring the flourishing banana trees sitting next to you. Quantifying management work is more difficult than counting widgets you turned out, but just making it possible for your team to be happy and productive is a big measure of your job. Just don’t fall into the trap of counting apples when you’re growing bananas.[^1]

如果你职业生涯的大部分时间都在写代码，一天结束时，通常可以指着代码、设计文档，或刚关闭的一批 bug 说：“这就是我今天的成果。”可忙了一整天“管理”工作后，你往往会想：“我今天怎么什么正事都没干！”这就像你多年来每天都数自己摘了多少苹果，后来改行种香蕉，却仍在每天收工时说“我一个苹果也没摘”，对身旁长势茂盛的香蕉树视而不见。量化管理工作，比清点生产了多少件产品更难；但让团队能够愉快、高效地工作，本身就是衡量你工作成效的重要标准。不要明明在种香蕉，却还执着于数苹果。

Another big reason for not becoming a manager is often unspoken but rooted in the famous “Peter Principle,” which states that “In a hierarchy every employee tends to rise to his level of incompetence.” Google generally avoids this by requiring that a person perform the job *above* their current level for a period of time (i.e., to “exceeds expectations” at their current level) before being promoted to that level. Most people have had a manager who was incapable of doing their job or was just really bad at managing people,[^2] and we know some people who have worked only for bad managers. If you’ve been exposed only to crappy managers for your entire career, why would you *ever* want to be a manager? Why would you want to be promoted to a role that you don’t feel able to do?

另一个让人不愿当经理的重要原因，往往没有被说出口，却与著名的“彼得原理”有关：“在层级组织中，每个员工都趋向于晋升到自己无法胜任的职位。”为避免这种情况，谷歌通常要求员工先在一段时间内承担高于当前职级的工作，也就是在当前职级上达到“超出预期”，再晋升到相应职级。大多数人都遇到过无法胜任工作，或很不善于带人的经理；我们还认识一些人，他们遇到的经理全都很糟糕。如果整个职业生涯都只接触过这样的经理，你又怎么会**想成为一名经理**？你为什么会想晋升到一个自觉无法胜任的岗位？

> 译者注：彼得原理的推论是，每个职位最终都会由无法胜任该职位的员工占据。层级组织中的工作，多半由尚未晋升到不胜任层级的员工完成。

There are, however, great reasons to consider becoming a TL or manager. First, it’s a way to scale yourself. Even if you’re great at writing code, there’s still an upper limit to the amount of code you can write. Imagine how much code a team of great engineers could write under your leadership! Second, you might just be really good at it—many people who find themselves sucked into the leadership vacuum of a project discover that they’re exceptionally skilled at providing the kind of guidance, help, and air cover a team or a company needs. Someone has to lead, so why not you?

不过，也有充分的理由考虑担任 TL 或经理。首先，这能放大你的作用。即使你再擅长写代码，个人能写出的代码量也有上限。想想看，在你的带领下，一群优秀工程师能写出多少代码！其次，你可能真的很擅长领导工作。许多人因项目缺少领导而被推上这个岗位，随后发现，自己特别擅长为团队或公司提供所需的指导、帮助和外部掩护。总得有人来领导，为什么不能是你？

> [^1]:	Another difference that takes getting used to is that the things we do as managers typically pay off over a longer timeline.
>
> 1 另一个需要适应的区别是，经理所做的工作通常要经过更长时间才会见效。
> 
> [^2]:	Yet another reason companies shouldn’t force people into management as part of a career path: if an engineer is able to write reams of great code and has no desire at all to manage people or lead a team, by forcing them into a management or TL role, you’re losing a great engineer and gaining a crappy manager. This is not only a bad idea, but it’s actively harmful.
>
> 2 这也是公司不该强迫员工把管理岗位作为职业发展必经之路的另一个理由。如果一位工程师能写出大量优秀代码，却完全不想管理人员或带领团队，强行让他担任经理或 TL，就会失去一位优秀工程师，换来一位糟糕的经理。这不仅不明智，还会造成实际伤害。

### Servant Leadership  服务型领导

There seems to be a sort of disease that strikes managers in which they forget about all the awful things their managers did to them and suddenly begin doing these same things to “manage” the people that report to them. The symptoms of this disease include, but are by no means limited to, micromanaging, ignoring low performers, and hiring pushovers. Without prompt treatment, this disease can kill an entire team. The best advice I received when I first became a manager at Google was from Steve Vinter, an engineering director at the time. He said, “Above all, resist the urge to manage.” One of the greatest urges of the newly minted manager is to actively “manage” their employees because that’s what a manager does, right? This typically has disastrous consequences.

经理似乎容易染上一种病：忘记自己曾遭受过上司怎样的糟糕对待，转头就用同样的做法来“管理”下属。症状包括但远不限于：事无巨细地管控员工、无视低绩效员工的问题，以及招聘唯命是从的人。如果不及时治疗，整个团队都可能毁掉。我刚在谷歌当经理时，时任工程总监史蒂夫·温特给了我一条最受用的建议：“最重要的是，克制管人的冲动。”新任经理最大的冲动之一，就是主动去“管理”员工，毕竟这不就是经理的工作吗？然而，这通常会带来灾难性的后果。

The cure for the “management” disease is a liberal application of “servant leadership,” which is a nice way of saying the most important thing you can do as a leader is to serve your team, much like a butler or majordomo tends to the health and well-being of a household. As a servant leader, you should strive to create an atmosphere of humility, respect, and trust. This might mean removing bureaucratic obstacles that a team member can’t remove by themselves, helping a team achieve consensus, or even buying dinner for the team when they’re working late at the office. The servant leader fills in the cracks to smooth the way for their team and advises them when necessary, but still isn’t afraid of getting their hands dirty. The only managing that a servant leader does is to manage both the technical and social health of the team; as tempting  as it might be to focus on purely the technical health of the team, the social health of the team is just as important (but often infinitely more difficult to manage).

治疗这种“管理病”，需要充分践行“服务型领导”。说得直白些，领导者最重要的工作是为团队服务，就像管家照料一家人的生活和福祉。服务型领导者应努力营造谦逊、尊重和信任的氛围：帮助成员清除他们独力无法解决的官僚障碍，帮助团队达成共识，甚至在大家留在办公室加班时买来晚餐。服务型领导者补足缺漏，为团队扫清道路，必要时提供建议，也不怕亲自动手做事。他们唯一要“管理”的，是团队在技术和人际关系两方面的健康状况。人很容易只关注技术，但健康的人际关系同样重要，而且往往难管理得多。

## The Engineering Manager 工程经理

So, what is actually expected of a manager at a modern software company? Before the computing age, “management” and “labor” might have taken on almost antagonistic roles, with the manager wielding all of the power and labor requiring collective action to achieve its own ends. But that isn’t how modern software companies work.

那么，现代软件公司究竟期望经理做什么？在计算机时代之前，“管理方”与“劳方”可能近乎对立：管理方掌握全部权力，劳动者则要靠集体行动争取自己的目标。但现代软件公司并不是这样运作的。

### Manager Is a Four-Letter Word  经理成了骂人的话

Before talking about the core responsibilities of an engineering manager at Google, let’s review the history of managers. The present-day concept of the pointy-haired manager is partially a carryover, first from military hierarchy and later adopted by the Industrial Revolution—more than a hundred years ago! Factories began popping up everywhere, and they required (usually unskilled) workers to keep the machines going. Consequently, these workers required supervisors to manage them, and because it was easy to replace these workers with other people who were desperate for a job, the managers had little motivation to treat their employees well or improve conditions for them. Whether humane or not, this method worked well for many years when the employees had nothing more to do than perform rote tasks.

在讨论谷歌工程经理的核心职责之前，先回顾一下经理这一角色的历史。如今人们所说的“尖头发经理”形象，部分源于军队的等级体系，后来又被工业革命沿用，距今已有一百多年。当时，工厂四处兴起，需要工人维持机器运转，而这些工人通常没有熟练技能。于是，工厂又需要主管来管理工人。其他急需工作的人很容易就能替代现有工人，经理自然缺少善待员工、改善工作条件的动力。不论是否人道，在员工只需机械重复任务的年代，这种方法确实有效运作了很多年。

Managers frequently treated employees in the same way that cart drivers would treat their mules: they motivated them by alternately leading them forward with a carrot, and, when that didn’t work, whipping them with a stick. This carrot-and-stick method of management survived the transition from the factory[^3] to the modern office, where the stereotype of the tough-as-nails manager-as-mule-driver flourished in the middle part of the twentieth century when employees would work at the same job for years and years.

经理常常像赶车人对待骡子一样对待员工：先拿胡萝卜引着往前走，不奏效就挥起大棒。这种胡萝卜加大棒的管理方法，从工厂延续到了现代办公室。20世纪中叶，员工常年待在同一个岗位上，那种强硬得像赶骡人一样的经理形象也随之盛行。

This continues today in some industries—even in industries that require creative thinking and problem solving—despite numerous studies suggesting that the anachronistic carrot and stick is ineffective and harmful to the productivity of creative people. Whereas the assembly-line worker of years past could be trained in days and replaced at will, software engineers working on large codebases can take months to get up to speed on a new team. Unlike the replaceable assembly-line worker, these people need nurturing, time, and space to think and create.

如今，一些行业仍在沿用这种做法，甚至包括需要创造性思考和解决问题的行业，尽管大量研究表明，这套过时的胡萝卜加大棒方法不仅无效，还会损害创意工作者的生产力。过去的流水线工人经过几天培训就能上岗，也可以随时替换；而在大型代码库上工作的软件工程师，加入新团队后可能要几个月才能熟悉工作。与那些可随时替换的流水线工人不同，软件工程师需要培养，也需要时间和空间来思考、创造。


> [^3]:	For more fascinating information on optimizing the movements of factory workers, read up on Scientific Management or Taylorism, especially its effects on worker morale./
> 3   关于如何优化工厂工人的动作，还有许多有趣的资料，可参阅科学管理或泰勒主义，尤其是它们对工人士气的影响。


### Today’s Engineering Manager  当今的工程经理

Most people still use the title “manager” despite the fact that it’s often an anachronism. The title itself often encourages new managers to *manage* their reports. Managers can wind up acting like parents,[^4] and consequently employees react like children. To frame this in the context of humility, respect, and trust: if a manager makes it obvious that they trust their employee, the employee feels positive pressure to live up to that trust. It’s that simple. A good manager forges the way for a team, looking out for their safety and well-being, all while making sure their needs are met. If there’s one thing you remember from this chapter, make it this:
    Traditional managers worry about how to get things done, whereas great managers worry about what things get done (and trust their team to figure out how to do it).

大多数人仍沿用“经理”这个头衔，尽管它往往已经不合时宜。头衔本身常常让新任经理觉得应该去“管”下属。结果，经理像家长一样行事，员工也像孩子一样回应。用谦逊、尊重和信任的原则来看，道理很简单：经理明确表示信任员工，员工就会受到正向激励，努力不辜负这份信任。好的经理为团队开路，关心成员的安全和福祉，并确保他们的需求得到满足。如果你只从本章记住一件事，那应该是：
    传统经理操心如何把事情做成，优秀经理关心做成哪些事，并信任团队能找出具体做法。

A new engineer, Jerry, joined my team a few years ago. Jerry’s last manager (at a different company) was adamant that he be at his desk from 9:00 to 5:00 every day, and assumed that if he wasn’t there, he wasn’t working enough (which is, of course, a ridiculous assumption). On his first day working with me, Jerry came to me at 4:40p.m. and stammered out an apology that he had to leave 15 minutes early because he had an appointment that he had been unable to reschedule. I looked at him, smiled, and told him flat out, “Look, as long as you get your job done, I don’t care what time you leave the office.” Jerry stared blankly at me for a few seconds, nodded, and went on his way. I treated Jerry like an adult; he always got his work done, and I never had to worry about him being at his desk, because he didn’t need a babysitter to get his work done. If your employees are so uninterested in their job that they actually need traditional-manager babysitting to be convinced to work, *that* is your real problem.

几年前，一位名叫杰瑞的工程师加入了我的团队。他在上一家公司时，经理坚持要求他每天从早上9点到下午5点都坐在办公桌前，认为只要不在座位上，就是工作不够投入。这当然是个荒唐的假设。加入我的团队第一天，杰瑞在下午4点40分来找我，结结巴巴地道歉，说有个约定无法改期，必须提前15分钟离开。我看着他笑了笑，直接说：“只要把工作做好，什么时候离开办公室，我不在乎。”杰瑞愣愣地看了我几秒钟，点点头就走了。我把他当成年人对待；他总能完成工作，我也从不需要担心他是否在座位上，因为他不需要保姆盯着才能干活。如果员工对工作毫无兴趣，非要传统经理像保姆一样看管才肯做事，那才是你真正需要解决的问题。

> [^4]: If you have kids, the odds are good that you can remember with startling clarity the first time you said something to your child that made you stop and exclaim (perhaps even aloud), “Holy crap, I’ve become my mother.”
>
> 4 如果你有孩子，很可能对这样一个瞬间记忆犹新：你第一次对孩子说出某句话，突然愣住，心想，甚至脱口而出：“天哪，我怎么变得跟我妈一样了！”
-----

#### Failure Is an Option  允许失败

Another way to catalyze your team is to make them feel safe and secure so that they can take greater risks by building psychological safety—meaning that your team members feel like they can be themselves without fear of negative repercussions from you or their team members. Risk is a fascinating thing; most humans are terrible at evaluating risk, and most companies try to avoid risk at all costs. As a result, the usual modus operandi is to work conservatively and focus on smaller successes, even when taking a bigger risk might mean exponentially greater success. A common saying at Google is that if you try to achieve an impossible goal, there’s a good chance you’ll fail, but if you fail trying to achieve the impossible, you’ll most likely accomplish far more than you would have accomplished had you merely attempted something you knew you could complete. A good way to build a culture in which risk taking is accepted is to let your team know that it’s OK to fail.

激发团队活力的另一种方法，是建立心理安全感，让大家安心尝试、敢于承担更大的风险。也就是说，成员可以做真实的自己，不必害怕你或其他成员会因此给他们带来不利后果。风险很有意思：大多数人不擅长评估风险，大多数公司却想不惜一切代价规避风险。因此，人们往往采取保守的做法，只求小成，即使承担更大的风险可能带来呈指数级增长的成果。谷歌常说，尝试实现不可能的目标，很可能失败；但即使失败，取得的成果也很可能远超只尝试那些有把握完成的事情。要建立接受冒险的文化，一个好办法就是让团队知道：失败是允许的。

So, let’s get that out of the way: it’s OK to fail. In fact, we like to think of failure as a way of learning a lot really quickly (provided that you’re not repeatedly failing at the same thing). In addition, it’s important to see failure as an opportunity to learn and not to point fingers or assign blame. Failing fast is good because there’s not a lot at stake. Failing slowly can also teach a valuable lesson, but it is more painful because more is at risk and more can be lost (usually engineering time). Failing in a manner that affects customers is probably the least desirable failure that we encounter, but it’s also one in which we have the greatest amount of structure in place to learn from failures. As mentioned earlier, every time there is a major production failure at Google, we perform a postmortem. This procedure is a way to document the events that led to the actual failure and to develop a series of steps that will prevent it from happening in the future. This is neither an opportunity to point fingers, nor is it intended to introduce unnecessary bureaucratic checks; rather, the goal is to strongly focus on the core of the problem and fix it once and for all. It’s very difficult, but quite effective (and cathartic).

先把话说清楚：失败是允许的。我们更愿意把失败视为在短时间内学到很多东西的方式，前提是不要在同一件事上反复失败。还要把失败当作学习机会，而不是指责他人、追究过错的机会。尽早失败有好处，因为此时投入还少。拖到很晚才失败，也能留下宝贵教训，却更加痛苦，因为牵涉的风险更大，损失也可能更多，通常损失的是工程师的时间。影响客户的失败，大概是我们最不愿遇到的一类；但对于这类失败，我们也建立了最完备的学习机制。如前文所述，谷歌每次发生重大生产故障，都会进行事后复盘，记录导致故障的事件，并制定防止重演的措施。复盘不是为了指责谁，也不是为了增加不必要的官僚检查，而是要紧盯问题根源，将其彻底解决。这很难，却相当有效，也能帮助大家释放情绪。

Individual successes and failures are a bit different. It’s one thing to laud individual successes, but looking to assign individual blame in the case of failure is a great way to divide a team and discourage risk taking across the board. It’s alright to fail, but fail as a team and learn from your failures. If an individual succeeds, praise them in front of the team. If an individual fails, give constructive criticism in private.[^5] Whatever the case, take advantage of the opportunity and apply a liberal helping of humility, respect, and trust to help your team learn from its failures.

对待个人的成功与失败，则要有所区别。表扬个人的成功是一回事，失败后执意找个人来责怪，则很容易分裂团队，让所有人都不敢冒险。失败可以接受，但应由团队共同承担，并从中学习。个人取得成功，就在团队面前表扬；个人遭遇失败，就私下提出建设性的批评。无论哪种情况，都要抓住机会，充分践行谦逊、尊重和信任，帮助团队从失败中学习。

------

> [^5]: Public criticism of an individual is not only ineffective (it puts people on the defense), but rarely necessary, and most often is just mean or cruel. You can be sure the rest of the team already knows when an individual has failed, so there’s no need to rub it in.  
>
> 5 公开批评个人不仅无效，会让人产生防御心理，而且很少有必要，更多时候只是刻薄，甚至残忍。某个人出了问题，团队其他成员肯定早已知道，没必要再让他难堪。

## Antipatterns  反模式

Before we go over a litany of “design patterns” for successful TLs and engineering managers, we’re going to review a collection of the patterns that you *don’t* want to follow if you want to be a successful manager. We’ve observed these destructive patterns in a handful of bad managers that we’ve encountered in our careers, and in more than a few cases, ourselves.

在介绍优秀 TL 和工程经理采用的一系列“设计模式”之前，先看看要做好经理就*不该*遵循的模式。在职业生涯中，我们在一些糟糕经理身上见过这些破坏性做法；不少时候，我们自己也犯过同样的错。

### Antipattern: Hire Pushovers   反模式：招聘唯命是从的人

If you’re a manager and you’re feeling insecure in your role (for whatever reason), one way to make sure no one questions your authority or threatens your job is to hire people you can push around. You can achieve this by hiring people who aren’t as smart or ambitious as you are, or just people who are more insecure than you. Even though this will cement your position as the team leader and decision maker, it will mean a lot more work for you. Your team won’t be able to make a move without you leading them like dogs on a leash. If you build a team of pushovers, you probably can’t take a vacation; the moment you leave the room, productivity comes to a screeching halt. But surely this is a small price to pay for feeling secure in your job, right?

如果你身为经理，却因某种原因对自己的地位缺乏安全感，有一种办法能确保没人质疑你的权威或威胁你的职位：招聘任你摆布的人。你可以找不如你聪明、不如你有进取心，或只是比你更缺乏安全感的人。这样固然能巩固你作为团队领导和决策者的地位，却也会让你的工作量大增。你得像牵着狗一样带着他们，否则团队寸步难行。建起一支唯命是从的团队后，你大概连假都休不了：你一走出房间，工作就戛然而止。不过，为了保住职位上的安全感，这点代价总算不了什么，对吧？

Instead, you should strive to hire people who are smarter than you and can replace you. This can be difficult because these very same people will challenge you on a regular basis (in addition to letting you know when you make a mistake). These very same people will also consistently impress you and make great things happen. They’ll be able to direct themselves to a much greater extent, and some will be eager to lead the team, as well. You shouldn’t see this as an attempt to usurp your power; instead, look at it as an opportunity for you to lead an additional team, investigate new opportunities, or even take a vacation without worrying about checking in on the team every day to make sure it’s getting its work done. It’s also a great chance to learn and grow—it’s a lot easier to expand your expertise when surrounded by people who are smarter than you.

你真正应该做的，是努力招聘比自己聪明、能够接替自己的人。这可能并不容易，因为他们会经常质疑你的看法，也会在你犯错时指出来。但同样是这些人，会不断让你刮目相看，做出出色的成果。他们更能自主安排工作，有些人还会渴望带领团队。不要把这视为夺权，而要把它看作机会：你可以再带一个团队，探索新的可能，甚至安心休假，不必每天查看团队是否正常工作。这也是学习和成长的好机会，身边都是比自己聪明的人，拓展专业能力会容易得多。

### Antipattern: Ignore Low Performers  反模式：忽略低绩效员工

Early in my career as a manager at Google, the time came for me to hand out bonus letters to my team, and I grinned as I told my manager, “I love being a manager!” Without missing a beat, my manager, a long-time industry veteran, replied, “Sometimes you get to be the tooth fairy, other times you have to be the dentist.”

我刚在谷歌当经理不久，有一次要给团队发奖金通知，便笑着对自己的经理说：“我喜欢当经理！”他是位资深的行业老手，立刻接道：“有时你是送礼的牙仙，有时你得当拔牙的牙医。”

It’s never any fun to pull teeth. We’ve seen team leaders do all the right things to build incredibly strong teams only to have these teams fail to excel (and eventually fall apart) because of just one or two low performers. We understand that the human aspect is the most challenging part of writing software, but the most difficult part of dealing with humans is handling someone who isn’t meeting expectations. Sometimes, people miss expectations because they’re not working long enough or hard enough, but the most difficult cases are when someone just isn’t capable of doing their job no matter how long or hard they work.

拔牙从来不是件愉快的事。我们见过一些领导，各方面都做得对，也建起了很强的团队，却因为一两个低绩效成员，始终无法让团队发挥出应有的水平，最终甚至分崩离析。我们知道，软件开发中最难处理的是人的问题；而与人打交道时，最难的又是帮助那些表现达不到预期的人。有时，他们只是工作时间不足或不够努力；更棘手的情况是，无论花多少时间、付出多少努力，他们都无法胜任工作。

Google’s Site Reliability Engineering (SRE) team has a motto: “Hope is not a strategy.” And nowhere is hope more overused as a strategy than in dealing with a low performer. Most team leaders grit their teeth, avert their eyes, and just *hope* that the low performer either magically improves or just goes away. Yet it is extremely rare that this person does either.

谷歌的网站可靠性工程（SRE）团队有句座右铭：“希望不是策略。”而在处理低绩效员工的问题时，人们尤其容易把希望当成策略。大多数团队领导只是咬牙忍着，装作没看见，*希望*对方奇迹般地进步，或者自行离开。然而，这两种情况都极少发生。

While the leader is hoping and the low performer isn’t improving (or leaving), high performers on the team waste valuable time pulling the low performer along, and team morale leaks away into the ether. You can be sure that the team knows the low performer is there even if you’re ignoring them—in fact, the team is *acutely* aware of who the low performers are, because they have to carry them.

领导一味抱着希望，低绩效员工却既不进步也不离开，这时，团队里的高绩效成员就得耗费宝贵的时间替他们补位，团队士气也会一点点流失。即使你选择无视，团队也一定知道问题的存在。事实上，谁表现不佳，团队再清楚不过，因为其他人必须替这些人分担工作。

Ignoring low performers is not only a way to keep new high performers from joining your team, but it’s also a way to encourage existing high performers to leave. You eventually wind up with an entire team of low performers because they’re the only ones who can’t leave of their own volition. Lastly, you aren’t even doing the low performer any favors by keeping them on the team; often, someone who wouldn’t do well on your team could actually have plenty of impact somewhere else.

无视低绩效问题，不仅会让新的高绩效员工不愿加入，也会促使现有的高绩效员工离开。到最后，团队只会剩下低绩效员工，因为只有他们没法想走就走。而且，把他们留在团队里，也没有帮到他们本人。一个不适合你团队的人，往往可能在别处发挥很大作用。

The benefit of dealing with a low performer as quickly as possible is that you can put yourself in the position of helping them up or out. If you immediately deal with a low performer, you’ll often find that they merely need some encouragement or direction to slip into a higher state of productivity. If you wait too long to deal with a low performer, their relationship with the team is going to be so sour and you’re going to be so frustrated that you’re not going to be able to help them.

尽早处理低绩效问题，你才有余地帮助对方改善表现，或者离开团队。及时介入时，你往往会发现，他们只需一些鼓励或指导就能提高生产力。拖得太久，他们与团队的关系就会严重恶化，你也会沮丧到无力再提供帮助。

How do you effectively coach a low performer? The best analogy is to imagine that you’re helping a limping person learn to walk again, then jog, then run alongside the rest of the team. It almost always requires temporary micromanagement, but still a whole lot of humility, respect, and trust—particularly respect. Set up a specific time frame (say, two months) and some very specific goals you expect them to achieve in that period. Make the goals small, incremental, and measurable so that there’s an opportunity for lots of small successes. Meet with the team member every week to check on progress, and be sure you set really explicit expectations around each upcoming milestone so that it’s easy to measure success or failure. If the low performer can’t keep up, it will become quite obvious to both of you early in the process. At this point, the person will often acknowledge that things aren’t going well and decide to quit; in other cases, determination will kick in and they’ll “up their game” to meet expectations. Either way, by working directly with the low performer, you’re catalyzing important and necessary changes.

怎样才能有效指导低绩效员工？可以把这想成帮助一个步履蹒跚的人重新学会走路，再开始慢跑，最后跟上团队一起跑。这几乎总需要暂时采取细致管控的方式，但仍要充分秉持谦逊、尊重和信任，尤其是尊重。设定明确的期限，例如两个月，并列出希望对方在这段时间内达到的具体目标。目标要小，循序渐进，而且可以衡量，让对方有机会不断取得小的成功。每周见面检查进展，并明确说明对下一个里程碑的期望，方便双方判断是否达标。如果对方跟不上，双方都会在早期察觉。到了这一步，对方往往会承认情况不理想并决定离开；也有人会下定决心，提高表现以达到预期。无论是哪种结果，直接与低绩效员工一起解决问题，都能推动必要而重要的改变。

### Antipattern: Ignore Human Issues  反模式：忽视人的问题

A manager has two major areas of focus for their team: the social and the technical. It’s rather common for managers to be stronger in the technical side at Google, and because most managers are promoted from a technical job (for which the primary goal of their job was to solve technical problems), they can tend to ignore human issues. It’s tempting to focus all of your energy on the technical side of your team because, as an individual contributor, you spend the vast majority of your time solving technical problems. When you were a student, your classes were all about learning the technical ins and outs of your work. Now that you’re a manager, however, you ignore the human element of your team at your own peril.

经理需要关注团队的两个主要方面：人际关系和技术。在谷歌，经理更擅长技术的情况很常见。他们大多从技术岗位晋升而来，原先的主要任务就是解决技术问题，因此容易忽视人的问题。把全部精力放在技术上很自然：当个人贡献者时，你的大部分时间都在解决技术问题；当学生时，课程教的也是工作所需的各种技术知识。但现在你是经理，忽视团队中人的因素，就要承担由此带来的风险。

Let’s begin with an example of a leader ignoring the human element in his team. Years ago, Jake had his first child. Jake and Katie had worked together for years, both remotely and in the same office, so in the weeks following the arrival of the new baby, Jake worked from home. This worked out great for the couple, and Katie was totally fine with it because she was already used to working remotely with Jake. They were their usual productive selves until their manager, Pablo (who worked in a different office), found out that Jake was working from home for most of the week. Pablo was upset that Jake wasn’t going into the office to work with Katie, despite the fact that Jake was just as productive as always and that Katie was fine with the situation. Jake attempted to explain to Pablo that he was just as productive as he would be if he came into the office and that it was much easier on him and his wife for him to mostly work from home for a few weeks. Pablo’s response: “Dude, people have kids all the time. You need to go into the office.” Needless to say, Jake (normally a mild-mannered engineer) was enraged and lost a lot of respect for Pablo.

先看一个领导忽视团队中人的因素的例子。几年前，杰克迎来了第一个孩子。他与凯蒂共事多年，既远程合作过，也在同一个办公室工作过。因此，孩子出生后的几周，杰克选择在家办公。这对杰克夫妇很有帮助，凯蒂也完全接受，因为她早已习惯与杰克远程合作。两人工作效率一如往常，直到在另一处办公室工作的经理帕布罗发现，杰克每周大部分时间都在家办公。尽管杰克的产出没有下降，凯蒂也没有意见，帕布罗仍对杰克不去办公室与凯蒂一起工作感到不满。杰克试着解释，在家与在办公室的效率一样，而且这几周主要在家办公，能让他和妻子轻松许多。帕布罗却说：“伙计，生孩子又不是什么稀罕事。你得来办公室。”不用说，平日温和的杰克被激怒了，对帕布罗的尊重也大打折扣。

There are numerous ways in which Pablo could have handled this differently: he could have showed some understanding that Jake wanted to spend more time at home with his wife and, if his productivity and team weren’t being affected, just let him continue to do so for a while. He could have negotiated that Jake go into the office for one or two days a week until things settled down. Regardless of the end result, a little bit of empathy would have gone a long way toward keeping Jake happy in this situation.

帕布罗本有许多别的处理方式。他可以理解杰克想多在家陪伴妻子的心情，只要工作效率和团队不受影响，就允许他再这样安排一段时间；也可以与杰克协商，在家里的情况稳定下来之前，每周到办公室一两天。无论最后怎样安排，多一点同理心，就能大大减轻杰克的不快。

### Antipattern: Be Everyone’s Friend  反模式：试图成为每个人的朋友

The first foray that most people have into leadership of any sort is when they become the manager or TL of a team of which they were formerly members. Many leads don’t want to lose the friendships they’ve cultivated with their teams, so they will sometimes work extra hard to maintain friendships with their team members after becoming a team lead. This can be a recipe for disaster and for a lot of broken friendships. Don’t confuse friendship with leading with a soft touch: when you hold power over someone’s career, they might feel pressure to artificially reciprocate gestures of friendship.

大多数人第一次担任领导，是在原来所在的团队里成为经理或 TL。许多人不愿失去与同事建立的友谊，于是上任后格外努力地维系关系。这可能酿成大问题，甚至让许多友谊破裂。不要把友谊与温和的领导方式混为一谈：当你有权影响一个人的职业发展时，对方可能迫于压力，勉强回应你示好的举动。

Remember that you can lead a team and build consensus without being a close friend of your team (or a monumental hard-ass). Likewise, you can be a tough leader without tossing your existing friendships to the wind. We’ve found that having lunch with your team can be an effective way to stay socially connected to them without making them uncomfortable—this gives you a chance to have informal conversations outside the normal work environment.

请记住，要带领团队、建立共识，既不必与每个人都成为密友，也不必变得蛮横严苛。同样，做一个严格的领导，也不意味着要舍弃已有的友谊。我们发现，与团队共进午餐是保持交往又不让人不自在的有效方式，大家有机会离开日常工作环境，轻松聊一聊。

Sometimes, it can be tricky to move into a management role over someone who has been a good friend and a peer. If the friend who is being managed is not self- managing and is not a hard worker, it can be stressful for everyone. We recommend that you avoid getting into this situation whenever possible, but if you can’t, pay extra attention to your relationship with those folks.

有时，成为昔日好友、原来同级同事的经理，会很棘手。如果这位朋友不能自我管理，工作也不努力，所有人都可能承受压力。我们建议尽量避免这种情况；无法避免时，就要格外留意与这些人的关系。

### Antipattern: Compromise the Hiring Bar  反模式：降低招聘标准

Steve Jobs once said: “A people hire other A people; B people hire C people.” It’s incredibly easy to fall victim to this adage, and even more so when you’re trying to hire quickly. A common approach I’ve seen outside of Google is that a team needs to hire 5 engineers, so it sifts through a pile of applications, interviews 40 or 50 people, and picks the best 5 candidates regardless of whether they meet the hiring bar.

史蒂夫·乔布斯曾说：“A 类人才招聘 A 类人才，B 类人才招聘 C 类人才。”人很容易陷入这句话描述的困境，急着招人时尤其如此。我在谷歌之外见过一种常见做法：团队需要5名工程师，于是筛选一批申请，面试40或50人，再选出其中最好的5人，却不管他们是否真正达到招聘标准。

This is one of the fastest ways to build a mediocre team.

这是建立一个平庸团队的最快方式之一。

The cost of finding the appropriate person—whether by paying recruiters, paying for advertising, or pounding the pavement for references—pales in comparison to the cost of dealing with an employee who you never should have hired in the first place. This “cost” manifests itself in lost team productivity, team stress, time spent managing the employee up or out, and the paperwork and stress involved in firing the employee. That’s assuming, of course, that you try to avoid the monumental cost of just leaving them on the team. If you’re managing a team for which you don’t have a say over hiring and you’re unhappy with the hires being made for your team, you need to fight tooth and nail for higher-quality engineers. If you’re still handed substandard engineers, maybe it’s time to look for another job. Without the raw materials for a great team, you’re doomed.

为了找到合适的人选，无论是付费请招聘人员帮忙、投放广告，还是四处寻求推荐，花费都远小于处理一个本不该录用的员工所需的成本。这些成本包括团队生产力下降、成员承受压力、帮助对方改善表现或离职所需的时间，以及解雇时的文书工作和心理压力。这还假定你会采取行动，避免把人一直留在团队里造成更大的代价。如果你带团队却在招聘上没有发言权，而且对招进来的人不满意，就必须竭力争取更优秀的工程师。如果公司仍不断给你安排不达标的人，也许该考虑换一份工作了。没有组建优秀团队所需的人才，你注定会失败。

### Antipattern: Treat Your Team Like Children  反模式：像对待孩子一样对待团队成员

The best way to show your team that you don’t trust it is to treat team members like kids—people tend to act the way you treat them, so if you treat them like children or prisoners, don’t be surprised when that’s how they behave. You can manifest this behavior by micromanaging them or simply by being disrespectful of their abilities and giving them no opportunity to be responsible for their work. If it’s permanently necessary to micromanage people because you don’t trust them, you have a hiring failure on your hands. Well, it’s a failure unless your goal was to build a team that you can spend the rest of your life babysitting. If you hire people worthy of trust and show these people you trust them, they’ll usually rise to the occasion (sticking with the basic premise, as we mentioned earlier, that you’ve hired good people).

要让团队知道你不信任他们，最直接的办法就是把成员当孩子。你怎样对待别人，别人往往就会怎样行事；把他们当孩子或囚犯，就别惊讶于他们表现得像孩子或囚犯。事无巨细地管控员工、不尊重他们的能力、不给他们独立负责工作的机会，都是这样的表现。如果因为不信任而必须长期细致管控，那说明招聘已经失败了，除非你的目标本来就是组建一支需要你照看一辈子的团队。招来值得信任的人，并让他们感受到你的信任，他们通常就会承担起责任。当然，这仍建立在前面所说的基本前提上：你招到的是优秀的人。

The results of this level of trust go all the way to more mundane things like office and computer supplies. As another example, Google provides employees with cabinets stocked with various and sundry office supplies (e.g., pens, notebooks, and other “legacy” implements of creation) that are free to take as employees need them. The IT department runs numerous “Tech Stops” that provide self-service areas that are like a mini electronics store. These contain lots of computer accessories and doodads (power supplies, cables, mice, USB drives, etc.) that would be easy to just grab and walk off with en masse, but because Google employees are being trusted to check these items out, they feel a responsibility to Do The Right Thing. Many people from typical corporations react in horror to hearing this, exclaiming that surely Google is hemorrhaging money due to people “stealing” these items. That’s certainly possible, but what about the costs of having a workforce that behaves like children or that has to waste valuable time formally requesting cheap office supplies? Surely that’s more expensive than the price of a few pens and USB cables.

这种信任也体现在办公用品、电脑配件等日常小事上。例如，谷歌设有装满各种办公用品的柜子，里面有笔、笔记本等“传统”创作工具，员工可以按需取用。IT 部门还设有许多“技术站”，其中的自助区像小型电子产品商店，备有电源、线缆、鼠标、U 盘等各种配件和小物件。人们很容易一股脑拿走一大堆，但谷歌信任员工会自行办理领用，他们也就觉得有责任按规矩做事。许多来自传统企业的人听说后大吃一惊，认定总有人会“偷”东西，谷歌一定因此损失惨重。这当然有可能，但如果员工表现得像孩子，或者必须浪费宝贵时间正式申请廉价办公用品，代价又有多大？那肯定比几支笔和几根 USB 线贵得多。

## Positive Patterns  积极模式

Now that we’ve covered antipatterns, let’s turn to positive patterns for successful leadership and management that we’ve learned from our experiences at Google, from watching other successful leaders and, most of all, from our own leadership mentors. These patterns are not only those that we’ve had great success implementing, but the patterns that we’ve always respected the most in the leaders who we follow.

介绍完反模式，再来看看有助于成功领导和管理团队的正向做法。它们来自我们在谷歌的实践、对其他优秀领导者的观察，更重要的是来自指导我们学习领导工作的导师。这些做法不仅在我们的实践中成效显著，也是我们始终最欣赏自己所追随的领导者的地方。

### Lose the Ego   放下自负

We talked about “losing the ego” a few chapters ago when we first examined humility, respect, and trust, but it’s especially important when you’re a team leader. This pattern is frequently misunderstood as encouraging people to be doormats and let others walk all over them, but that’s not the case at all. Of course, there’s a fine line between being humble and letting others take advantage of you, but humility is not the same as lacking confidence. You can still have self-confidence and opinions without being an egomaniac. Big personal egos are difficult to handle on any team, especially in the team’s leader. Instead, you should work to cultivate a strong collective team ego and identity.

前几章初次讨论谦逊、尊重和信任时，我们就谈过“放下自负”；对团队领导来说，这一点尤其重要。它常被误解为鼓励人做受气包，任人欺负，其实完全不是。谦逊与任人占便宜之间确实有一条微妙的界线，但谦逊不等于缺乏自信。你可以有信心、有主见，而不必自高自大。在任何团队里，过于膨胀的个人自我都难以应对，出现在领导身上尤其如此。你应该培养的，是强烈的团队自豪感和集体认同。

Part of “losing the ego” is trust: you need to trust your team. That means respecting the abilities and prior accomplishments of the team members, even if they’re new to your team.

“放下自负”的一部分是信任团队：尊重成员的能力和已有成就，即使他们刚刚加入团队。

If you’re not micromanaging your team, you can be pretty certain the folks working in the trenches know the details of their work better than you do. This means that although you might be the one driving the team to consensus and helping to set the direction, the nuts and bolts of how to accomplish your goals are best decided by the people who are putting the product together. This gives them not only a greater sense of ownership, but also a greater sense of accountability and responsibility for the success (or failure) of their product. If you have a good team and you let it set the bar for the quality and rate of its work, it will accomplish more than by you standing over team members with a carrot and a stick.

只要你没有事无巨细地管控团队，就几乎可以肯定，一线成员比你更了解工作细节。因此，虽然你可能负责推动共识、协助确定方向，但实现目标的具体方法，最好交给实际开发产品的人决定。这不仅会增强他们的主人翁意识，也会让他们更愿意对产品的成败负责、承担相应责任。如果团队足够优秀，让他们自己设定工作质量和速度的标准，取得的成果会比你拿着胡萝卜和大棒盯着他们更多。

Most people new to a leadership role feel an enormous responsibility to get everything right, to know everything, and to have all the answers. We can assure you that you will not get everything right, nor will you have all the answers, and if you act like you do, you’ll quickly lose the respect of your team. A lot of this comes down to having a basic sense of security in your role. Think back to when you were an individual contributor; you could smell insecurity a mile away. Try to appreciate inquiry: when someone questions a decision or statement you made, remember that this person is usually just trying to better understand you. If you encourage inquiry, you’re much more likely to get the kind of constructive criticism that will make you a better leader of a better team. Finding people who will give you good constructive criticism is incredibly difficult, and it’s even more difficult to get this kind of criticism from people who “work for you.” Think about the big picture of what you’re trying to accomplish as a team, and accept feedback and criticism openly; avoid the urge to be territorial.

大多数刚担任领导的人都觉得责任重大，认为自己必须事事做对、无所不知，回答所有问题。我们可以肯定地告诉你：你不可能全做对，也不可能知道所有答案。假装自己做得到，只会很快失去团队的尊重。这在很大程度上取决于你对自身角色是否有基本的安全感。回想你还是个人贡献者时，别人心里没底，你往往一眼就能看出来。要学会欢迎提问：别人质疑你的决定或说法时，通常只是想更好地理解你。鼓励提问，才更容易获得建设性的批评，让自己和团队一起进步。愿意提出有价值批评的人本就难找，要让“为你工作”的人开口就更难。着眼于团队共同目标，坦然接受反馈和批评，克制维护个人地盘的冲动。

The last part of losing the ego is a simple one, but many engineers would rather be boiled in oil than do it: apologize when you make a mistake. And we don’t mean you should just sprinkle “I’m sorry” throughout your conversation like salt on popcorn— you need to sincerely mean it. You are absolutely going to make mistakes, and whether or not you admit it, your team is going to know you’ve made a mistake. Your team members will know regardless of whether they talk to you (and one thing is guaranteed: they *will* talk about it with one another). Apologizing doesn’t cost money. People have enormous respect for leaders who apologize when they screw up, and contrary to popular belief, apologizing doesn’t make you vulnerable. In fact, you’ll usually gain respect from people when you apologize, because apologizing tells people that you are level headed, good at assessing situations, and—coming back to humility, respect, and trust—humble.

放下自负的最后一点很简单，却让许多工程师宁愿下油锅也不愿做：犯错时道歉。我们不是让你像给爆米花撒盐一样，把“对不起”随口撒进每段对话，而是要真心实意地道歉。你一定会犯错，无论承不承认，团队都会知道。成员也许不当面说，但有一点可以肯定：他们彼此之间*会*谈论这件事。道歉不花钱，犯错后愿意道歉的领导却很受尊重。与常见看法相反，道歉不会让你显得软弱，反而通常会赢得尊重，因为它表明你头脑冷静、善于判断形势，而且谦逊。这又回到了谦逊、尊重和信任这三项原则。

### Be a Zen Master  像禅师一样沉着

As an engineer, you’ve likely developed an excellent sense of skepticism and cynicism, but this can be a liability when you’re trying to lead a team. This is not to say that you should be naively optimistic at every turn, but you would do well to be less vocally skeptical while still letting your team know you’re aware of the intricacies and obstacles involved in your work. Mediating your reactions and maintaining your calm is more important as you lead more people, because your team will (both unconsciously and consciously) look to you for clues on how to act and react to whatever is going on around you.

作为工程师，你可能早已练就敏锐的质疑能力，也习惯了冷眼看事，但在带领团队时，这些习惯可能成为负担。这不是让你凡事天真乐观，而是要少把怀疑挂在嘴边，同时让团队知道，你清楚工作中的复杂之处和障碍。带领的人越多，就越要控制反应、保持冷静，因为成员会有意无意地观察你，判断该如何面对周围发生的事。

A simple way to visualize this effect is to see your company’s organization chart as a chain of gears, with the individual contributor as a tiny gear with just a few teeth all the way at one end, and each successive manager above them as another gear, ending with the CEO as the largest gear with many hundreds of teeth. This means that every time that individual’s “manager gear” (with maybe a few dozen teeth) makes a single revolution, the “individual’s gear” makes two or three revolutions. And the CEO can make a small movement and send the hapless employee, at the end of a chain of six or seven gears, spinning wildly! The farther you move up the chain, the faster you can set the gears below you spinning, whether or not you intend to.

可以把公司的组织结构想成一串相互咬合的齿轮：个人贡献者位于最末端，是只有几个齿的小齿轮；向上每一级经理对应一个更大的齿轮，直到 CEO，成为有几百个齿的最大齿轮。这样一来，直属“经理齿轮”可能有几十个齿，每转一圈，“个人齿轮”就得转两三圈。CEO 只要稍微动一下，就能让隔着六七个齿轮的末端员工忙得团团转！层级越高，越容易让下面的齿轮飞转，不论你是否有意如此。

Another way of thinking about this is the maxim that the leader is always on stage. This means that if you’re in an overt leadership position, you are always being watched: not just when you run a meeting or give a talk, but even when you’re just sitting at your desk answering emails. Your peers are watching you for subtle clues in your body language, your reactions to small talk, and your signals as you eat lunch. Do they read confidence or fear? As a leader, your job is to inspire, but inspiration is a 24/7 job. Your visible attitude about absolutely everything—no matter how trivial—is unconsciously noticed and spreads infectiously to your team.

也可以用一句格言来理解：“领导者始终站在台上。”只要处于显眼的领导岗位，你就时刻受到关注，不只是在主持会议或演讲时，即使坐在桌前回复邮件也一样。同事会从你的肢体语言、闲聊时的反应，甚至午餐时的一举一动中捕捉细微信号。他们看到的是信心，还是恐惧？领导者的职责是激励他人，而这是一项全天候的工作。无论事情多么微小，你表现出的态度都会被人不自觉地留意到，并感染整个团队。

One of the early managers at Google, Bill Coughran, a VP of engineering, had truly mastered the ability to maintain calm at all times. No matter what blew up, no matter what crazy thing happened, no matter how big the firestorm, Bill would never panic. Most of the time he’d place one arm across his chest, rest his chin in his hand, and ask questions about the problem, usually to a completely panicked engineer. This had the effect of calming them and helping them to focus on solving the problem instead of running around like a chicken with its head cut off. Some of us used to joke that if someone came in and told Bill that 19 of the company’s offices had been attacked by space aliens, Bill’s response would be, “Any idea why they didn’t make it an even 20?”

谷歌早期的经理之一、工程副总裁比尔·考夫兰，就真正做到了始终沉着。无论出了什么故障、发生多么离谱的事、掀起多大的风波，他都不慌。大多数时候，他会将一条胳膊横在胸前，用手托着下巴，向往往已经慌乱不堪的工程师询问问题。这能让对方冷静下来，专注于解决问题，而不是像无头苍蝇一样乱撞。我们曾开玩笑说，要是有人来报告，公司19处办公室遭到外星人袭击，比尔大概会问：“知道他们为什么不凑个整，袭击20处吗？”

This brings us to another Zen management trick: asking questions. When a team member asks you for advice, it’s usually pretty exciting because you’re finally getting the chance to fix something. That’s exactly what you did for years before moving into a leadership position, so you usually go leaping into solution mode, but that is the last place you should be. The person asking for advice typically doesn’t want *you* to solve their problem, but rather to help them solve it, and the easiest way to do this is to ask this person questions. This isn’t to say that you should replace yourself with a Magic 8 Ball, which would be maddening and unhelpful. Instead, you can apply some humility, respect, and trust and try to help the person solve the problem on their own by trying to refine and explore the problem. This will usually lead the employee to the answer,[^6] and it will be that person’s answer, which leads back to the ownership and responsibility we went over earlier in this chapter. Whether or not you have the answer, using this technique will almost always leave the employee with the impression that you did. Tricky, eh? Socrates would be proud of you.

这又引出了一个禅师式的管理技巧：提问。团队成员来请教时，你通常会很兴奋，因为终于又有机会解决问题了。这正是你在走上领导岗位前做了多年的事，因此你很容易立刻开始想办法替对方解决，但这恰恰最不该做。来请教的人通常不是想让*你*代为解决，而是希望得到帮助，自己解决问题；最简单的帮助方式就是提问。当然，不是让你用“魔力8球”来代替自己，那只会让人抓狂，毫无帮助。你应该秉持谦逊、尊重和信任，帮助对方厘清并探索问题，自己找到办法。这样通常能引导他找到答案，而且那是他自己的答案，也就回到了前文讨论的主人翁意识和责任。不论你是否知道答案，这种方法几乎总会让对方觉得你知道。挺巧妙，对吧？苏格拉底会为你骄傲的。

> [^6]: See also “Rubber duck debugging.”
>
> 6   另请参见“橡皮鸭调试”。

### Be a Catalyst  成为催化剂（促进者）

In chemistry, a catalyst is something that accelerates a chemical reaction, but which itself is not consumed in the reaction. One of the ways in which catalysts (e.g., enzymes) work is to bring reactants into close proximity: instead of bouncing around randomly in a solution, the reactants are much more likely to favorably interact with one another when the catalyst helps bring them together. This is a role you’ll often need to play as a leader, and there are a number of ways you can go about it.

在化学中，催化剂能加快反应，自身却不会在反应中被消耗。酶等催化剂的一种作用方式，是让反应物彼此靠近。相比在溶液中随机游动，经催化剂聚到一起的反应物更容易发生所需的相互作用。领导者也常常需要扮演这样的角色，而且有多种做法。

One of the most common things a team leader does is to build consensus. This might mean that you drive the process from start to finish, or you just give it a gentle push in the right direction to speed it up. Working to build team consensus is a leadership skill that is often used by unofficial leaders because it’s one way you can lead without any actual authority. If you have the authority, you can direct and dictate direction, but that’s less effective overall than building consensus.[^7] If your team is looking to move quickly, sometimes it will voluntarily concede authority and direction to one or more team leads. Even though this might look like a dictatorship or oligarchy, when it’s done voluntarily, it’s a form of consensus.

促成共识，是团队领导最常做的事之一。你可以全程推动，也可以只顺着正确方向轻推一把，让过程加快。没有正式头衔的领导者经常运用这项技能，因为不掌握实际职权，也能借此带领团队。有职权时，你当然可以直接下令、指定方向，但总体效果不如建立共识。如果团队希望快速推进，有时会自愿把决策权和确定方向的权力交给一位或几位领导。这看似独裁或寡头决策，但只要出于自愿，也是一种共识。

> [^7]:	Attempting to achieve 100% consensus can also be harmful. You need to be able to decide to proceed even if not everyone is on the same page or there is still some uncertainty.  
> 7 追求全体一致也可能有害。即使大家尚未完全达成一致，或仍有一些不确定性，你也需要能够决定继续推进。

### Remove Roadblocks  消除障碍

Sometimes, your team already has consensus about what you need to do, but it hit a roadblock and became stuck. This could be a technical or organizational roadblock, but jumping in to help the team get moving again is a common leadership technique. There are some roadblocks that, although virtually impossible for your team members to get past, will be easy for you to handle, and helping your team understand that you’re glad (and able) to help out with these roadblocks is valuable.

有时，团队已经就该做什么达成共识，却被障碍卡住了。障碍可能来自技术，也可能来自组织；及时介入，帮助团队重新推进，是常见的领导方法。有些障碍，成员几乎不可能独力跨过，你却能轻松解决。让团队知道你愿意，也有能力帮助清除这些障碍，很有价值。

One time, a team spent several weeks trying to work past an obstacle with Google’s legal department. When the team finally reached its collective wits’ end and went to its manager with the problem, the manager had it solved in less than two hours simply because he knew the right person to contact to discuss the matter. Another time, a team needed some server resources and just couldn’t get them allocated. Fortunately, the team’s manager was in communication with other teams across the company and managed to get the team exactly what it needed that very afternoon. Yet another time, one of the engineers was having trouble with an arcane bit of Java code. Although the team’s manager was not a Java expert, she was able to connect the engineer to another engineer who knew exactly what the problem was. You don’t need to know all the answers to help remove roadblocks, but it usually helps to know the people who do. In many cases, knowing the right person is more valuable than knowing the right answer.

有一次，一个团队为了解决与谷歌法务部门有关的障碍，忙了好几个星期。直到大家实在无计可施，才去找经理，而经理不到两小时就解决了问题，只因为他知道该找谁商量。另一次，团队需要服务器资源，却始终分配不到。幸好经理与公司其他团队保持联系，当天下午就设法拿到了所需资源。还有一次，一位工程师被一段晦涩的 Java 代码难住了。经理虽然不是 Java 专家，却帮他联系上了另一位恰好了解问题的工程师。清除障碍不需要你知道所有答案，但认识知道答案的人，通常很有帮助。很多时候，认识合适的人比知道正确答案更有价值。

### Be a Teacher and a Mentor  成为一名教师和导师

One of the most difficult things to do as a TL is to watch a more junior team member spend 3 hours working on something that you know you can knock out in 20 minutes. Teaching people and giving them a chance to learn on their own can be incredibly difficult at first, but it’s a vital component of effective leadership. This is especially important for new hires who, in addition to learning your team’s technology and codebase, are learning your team’s culture and the appropriate level of responsibility to assume. A good mentor must balance the trade-offs of a mentee’s time learning versus their time contributing to their product as part of an effective effort to scale the team as it grows.

对 TL 来说，最难的事情之一，是看着资历较浅的成员花3小时，去做一件自己20分钟就能完成的事。教别人、让别人有机会自主学习，起初可能非常难，但这是有效领导不可缺少的一环。对新员工尤其如此：他们不仅要熟悉团队的技术和代码库，还要了解团队文化，以及自己应承担多大责任。好的导师必须权衡被指导者用于学习和实际贡献产品的时间，帮助团队在不断成长的同时有效扩大规模。

Much like the role of manager, most people don’t apply for the role of mentor—they usually become one when a leader is looking for someone to mentor a new team member. It doesn’t take a lot of formal education or preparation to be a mentor. Primarily, you need three things: experience with your team’s processes and systems, the ability to explain things to someone else, and the ability to gauge how much help your mentee needs. The last thing is probably the most important—giving your mentee enough information is what you’re supposed to be doing, but if you overexplain things or ramble on endlessly, your mentee will probably tune you out rather than politely tell you they got it.

与担任经理类似，大多数人并不是主动申请当导师，而是在领导寻找合适的人指导新成员时承担了这一角色。做导师不需要大量正规培训或准备，主要需要三样东西：熟悉团队的流程和系统，能把事情讲清楚，以及能判断被指导者需要多少帮助。最后一点可能最重要。你应当提供足够的信息，但如果解释过头、说个没完，对方很可能早已不再听，而不会礼貌地告诉你“我懂了”。

### Set Clear Goals  设定清晰目标

This is one of those patterns that, as obvious as it sounds, is solidly ignored by an enormous number of leaders. If you’re going to get your team moving rapidly in one direction, you need to make sure that every team member understands and agrees on what the direction is. Imagine your product is a big truck (and not a series of tubes). Each team member has in their hand a rope tied to the front of the truck, and as they work on the product, they’ll pull the truck in their own direction. If your intention is to pull the truck (or product) northbound as quickly as possible, you can’t have team members pulling every which way—you want them all pulling the truck north. If you’re going to have clear goals, you need to set clear priorities and help your team decide how it should make trade-offs when the time comes.

这条做法听起来显而易见，却被大量领导者彻底忽略。要让团队朝一个方向快速前进，必须确保每位成员都理解并认同这个方向。把产品想成一辆大卡车，而不是一串管子。每位成员手里都握着一根绑在车头的绳子，做产品时就向自己的方向拉。如果目标是让卡车，也就是产品，尽快向北走，就不能让大家各拉各的，而要一起向北用力。要有清晰的目标，就得明确优先级，并帮助团队确定需要作取舍时该如何权衡。

The easiest way to set a clear goal and get your team pulling the product in the same direction is to create a concise mission statement for the team. After you’ve helped the team define its direction and goals, you can step back and give it more autonomy, periodically checking in to make sure everyone is still on the right track. This not only frees up your time to handle other leadership tasks, it also drastically increases the efficiency of your team. Teams can (and do) succeed without clear goals, but they typically waste a great deal of energy as each team member pulls the product in a slightly different direction. This frustrates you, slows progress for the team, and forces you to use more and more of your own energy to correct the course.

要明确目标，让团队朝同一方向推动产品，最简单的办法是写一份简明的团队使命说明。帮助团队确定方向和目标后，你就可以退后一步，给他们更多自主权，只需定期查看，确保大家没有偏离轨道。这样既能腾出时间处理其他领导工作，也能显著提高团队效率。没有明确目标，团队也可能成功，事实上确实有这样的团队；但由于每个人用力的方向略有不同，往往会浪费大量精力。这既让你沮丧，也拖慢团队进展，还迫使你花越来越多的精力纠正方向。

### Be Honest  以诚待人

This doesn’t mean that we’re assuming you are lying to your team, but it merits a mention because you’ll inevitably find yourself in a position in which you can’t tell your team something or, even worse, you need to tell everyone something they don’t want to hear. One manager we know tells new team members, “I won’t lie to you, but I will tell you when I can’t tell you something or if I just don’t know.”

这并不是说我们认定你在对团队撒谎，而是因为你难免遇到有些事不能说的情况；更难的时候，还必须告诉大家一些他们不愿听的消息。我们认识的一位经理会对新成员说：“我不会骗你。如果有些事不能告诉你，或者我也不知道，我会明说。”

If a team member approaches you about something you can’t share, it’s OK to just tell them you know the answer but are not at liberty to say anything. Even more common is when a team member asks you something you don’t know the answer to: you can tell that person you don’t know. This is another one of those things that seems blindingly obvious when you read it, but many people in a manager role feel that if they don’t know the answer to something, it proves that they’re weak or out of touch. In reality, the only thing it proves is that they’re human.

如果成员问起不能透露的事，你完全可以告诉他：自己知道答案，但无权透露。更常见的是，你也不知道答案，那就直接说不知道。这同样是看起来显而易见、却很难做到的事。许多经理觉得，不知道答案就说明自己无能，或不了解情况。其实，这只能说明他们也是普通人。

Giving hard feedback is…well, hard. The first time you need to tell one of your reports that they made a mistake or didn’t do their job as well as expected can be incredibly stressful. Most management texts advise that you use the “compliment sandwich” to soften the blow when delivering hard feedback. A compliment sandwich looks something like this:

    You’re a solid member of the team and one of our smartest engineers. That being said, your code is convoluted and almost impossible for anyone else on the team to understand. But you’ve got great potential and a wicked cool T-shirt collection.

提出批评性的反馈……确实很难。第一次告诉下属他犯了错，或者工作没有达到预期时，你可能承受很大压力。大多数管理书籍建议用“赞美三明治”来减轻这类反馈的冲击，大致像这样：

    你是团队可靠的一员，也是我们最聪明的工程师之一。话虽如此，你的代码很绕，团队里其他人几乎都看不懂。不过，你很有潜力，而且收藏的 T 恤也酷极了。

Sure, this softens the blow, but with this sort of beating around the bush, most people will walk out of this meeting thinking only, “Sweet! I’ve got cool T-shirts!” We *strongly* advise against using the compliment sandwich, not because we think you should be unnecessarily cruel or harsh, but because most people won’t hear the critical message, which is that something needs to change. It’s possible to employ respect here: be kind and empathetic when delivering constructive criticism without resorting to the compliment sandwich. In fact, kindness and empathy are critical if you want the recipient to hear the criticism and not immediately go on the defensive.

这样固然能减轻冲击，但绕来绕去，多数人谈完后记住的只是：“太好了！我的 T 恤很酷！”我们强烈建议不要用“赞美三明治”，不是要你无谓地刻薄苛责，而是因为多数人会漏掉关键信息：有些地方必须改变。你完全可以尊重对方，用善意和同理心提出建设性批评，而不靠“赞美三明治”包装。事实上，要让对方听进去，而不是立刻产生防御心理，善意和同理心至关重要。

Years ago, a colleague picked up a team member, Tim, from another manager who insisted that Tim was impossible to work with. He said that Tim never responded to feedback or criticism and instead just kept doing the same things he’d been told he shouldn’t do. Our colleague sat in on a few of the manager’s meetings with Tim to watch the interaction between the manager and Tim, and noticed that the manager  made extensive use of the compliment sandwich so as not to hurt Tim’s feelings. When they brought Tim onto their team, they sat down with him and very clearly explained that Tim needed to make some changes to work more effectively with the team:

    We’re quite sure that you’re not aware of this, but the way that you’re interacting with the team is alienating and angering them, and if you want to be effective, you need to refine your communication skills, and we’re committed to helping you do that.

几年前，一位同事从另一位经理那里接收了成员蒂姆。原经理坚称，蒂姆根本无法合作，从不理会反馈和批评，明明被告知不该做的事，还是照做不误。同事旁听了两人几次会谈，观察他们的互动，发现经理为了不伤蒂姆的感情，大量使用“赞美三明治”。蒂姆加入新团队后，同事与他坐下来谈，明确说明要与团队更有效地合作，就必须作出改变：  
    我们相信，你自己还没有意识到，但你与团队相处的方式正在让大家疏远你、对你感到愤怒。要有效开展工作，你需要改进沟通方式，我们也会认真帮助你做到这一点。

They didn’t give Tim any compliments or candy-coat the issue, but just as important, they weren’t mean—they just laid out the facts as they saw them based on Tim’s performance with the previous team. Lo and behold, within a matter of weeks (and after a few more “refresher” meetings), Tim’s performance improved dramatically. Tim just needed very clear feedback and direction.

同事没有表扬蒂姆，也没有粉饰问题；但同样重要的是，措辞并不刻薄，只是根据蒂姆在原团队的表现，陈述自己看到的事实。结果，仅仅几周，再加上几次后续提醒，蒂姆的表现就显著改善了。他需要的只是清楚、直接的反馈和指导。

When you’re providing direct feedback or criticism, your delivery is key to making sure that your message is heard and not deflected. If you put the recipient on the defensive, they’re not going to be thinking of how they can change, but rather how they can argue with you to show you that you’re wrong. Our colleague Ben once managed an engineer who we’ll call Dean. Dean had extremely strong opinions and would argue with the rest of the team about anything. It could be something as big as the team’s mission or as small as the placement of a widget on a web page; Dean would argue with the same conviction and vehemence either way, and he refused to let anything slide. After months of this behavior, Ben met with Dean to explain to him that he was being too combative. Now, if Ben had just said, “Dean, stop being such a jerk,” you can be pretty sure Dean would have disregarded it entirely. Ben thought hard about how he could get Dean to understand how his actions were adversely affecting the team, and he came up with the following metaphor:

    Every time a decision is made, it’s like a train coming through town—when you jump in front of the train to stop it, you slow the train down and potentially annoy the engineer driving the train. A new train comes by every 15 minutes, and if you jump in front of every train, not only do you spend a lot of your time stopping trains, but eventually one of the engineers driving the train is going to get mad enough to run right over you. So, although it’s OK to jump in front of some trains, pick and choose the ones you want to stop to make sure you’re stopping only the trains that really matter.

直接提出反馈或批评时，能否让对方听进去而不是挡回来，关键在表达方式。如果让对方产生防御心理，他想的就不是如何改变，而是如何反驳、证明你错了。我们的同事本曾带过一位工程师，这里叫他迪安。迪安主见很强，凡事都要与团队其他人争论。大到团队使命，小到网页上一个小部件的位置，他都同样坚决、激烈地争辩，什么都不肯放过。几个月后，本找他谈话，指出他太爱争斗。如果本只是说“迪安，别再这么混蛋了”，迪安大概根本不会理会。本认真想过怎样让他理解自己的行为对团队的负面影响，于是用了下面这个比喻：

    每作出一个决定，就像有一列火车驶过小镇。你跳到车前拦住它，就会让列车减速，还可能惹恼司机。每15分钟就有一列新火车经过；如果每列都拦，你不仅要花大量时间拦车，最后还会有某个司机气得直接从你身上碾过去。所以，拦下某些列车没有问题，但要有所选择，只拦那些真正重要的。

This anecdote not only injected a bit of humor into the situation, but also made it easier for Ben and Dean to discuss the effect that Dean’s “train stopping” was having on the team in addition to the energy Dean was spending on it.

这个比喻既增添了一点幽默，也让本和迪安更容易讨论：迪安不断“拦火车”，除了耗费自己的精力，还会给团队带来什么影响。

### Track Happiness  追踪幸福感

As a leader, one way you can make your team more productive (and less likely to leave) in the long term is to take some time to gauge their happiness. The best leaders we’ve worked with have all been amateur psychologists, looking in on their team members’ welfare from time to time, making sure they get recognition for what they do, and trying to make certain they are happy with their work. One TLM we know makes a spreadsheet of all the grungy, thankless tasks that need to be done and makes certain these tasks are evenly spread across the team. Another TLM watches the hours his team is working and uses comp time and fun team outings to avoid burnout and exhaustion. Yet another starts one-on-one sessions with his team members by dealing with their technical issues as a way to break the ice, and then takes some time to make sure each engineer has everything they need to get their work done. After they’ve warmed up, he talks to the engineer for a bit about how they’re enjoying the work and what they’re looking forward to next.

领导者要长期提高团队生产力、减少成员离职，可以花些时间了解大家的幸福感。与我们共事过的那些最优秀的领导，都像业余心理学家：不时关心成员的身心状况，确保他们的工作得到认可，并尽力让他们对工作满意。我们认识的一位 TLM 用电子表格列出所有繁琐、吃力不讨好的任务，确保它们在团队中均衡分配。另一位 TLM 留意团队的工时，通过补休和有趣的集体外出活动防止倦怠、疲惫。还有一位，在一对一会谈开始时先谈技术问题，让气氛轻松下来，再确认工程师是否具备完成工作所需的条件。等聊开了，他才进一步询问对方对工作的感受，以及接下来有什么期待。

A good simple way to track your team’s happiness[^8] is to ask the team member at the end of each one-on-one meeting, “What do you need?” This simple question is a great way to wrap up and make sure each team member has what they need to be productive and happy, although you might need to carefully probe a bit to get details. If you ask this every time you have a one-on-one, you’ll find that eventually your team will remember this and sometimes even come to you with a laundry list of things it needs to make everyone’s job better.

追踪团队幸福感有个简单有效的办法：每次一对一会谈结束时，问成员一句“你需要什么？”这个问题适合用来收尾，帮助你确认每个人都具备愉快、高效工作所需的条件，不过有时还需要细心追问，才能了解具体情况。坚持每次都问，团队就会记住这个问题，有时甚至会主动带着一长串需求来找你，帮助大家改善工作。

> [^8]:	Google also runs an annual employee survey called “Googlegeist” that rates employee happiness across many dimensions. This provides good feedback but isn’t what we would call “simple.”
>
> 8 谷歌还通过名为“Googlegeist”的年度员工调查，从多个维度评估员工幸福感。这能提供有价值的反馈，但算不上我们这里所说的“简单”。

## The Unexpected Question  意想不到的问题

Shortly after I started at Google, I had my first meeting with then-CEO Eric Schmidt, and at the end Eric asked me, “Is there anything you need?” I had prepared a million defensive responses to difficult questions or challenges but was completely unprepared for this. So I sat there, dumbstruck and staring. You can be sure I had something ready the next time I was asked that question!

刚加入谷歌不久，我第一次与时任首席执行官埃里克·施密特（Eric Schmidt）会面。临结束时，他问：“你有什么需要吗？”我为可能遇到的难题和质疑准备了无数应对说辞，却完全没料到这个问题，只能坐在那里，瞪着眼说不出话来。可以肯定的是，下次再有人这样问，我就有答案了！

It can also be worthwhile as a leader to pay some attention to your team’s happiness outside the office. Our colleague Mekka starts his one-on-ones by asking his reports to rate their happiness on a scale of 1 to 10, and oftentimes his reports will use this as a way to discuss happiness in *and* outside of the office. Be wary of assuming that people have no life outside of work—having unrealistic expectations about the amount of time people can put into their work will cause people to lose respect for you, or worse, to burn out. We’re not advocating that you pry into your team members’ personal lives, but being sensitive to personal situations that your team members are going through can give you a lot of insight as to why they might be more or less productive at any given time. Giving a little extra slack to a team member who is currently having a tough time at home can make them a lot more willing to put in longer hours when your team has a tight deadline to hit later.

领导者也值得关注成员在工作之外是否过得愉快。我们的同事梅卡在一对一会谈开头，会请下属用1到10分评价自己的幸福感，对方也常借此谈起工作内外的感受。不要假定别人的生活里只有工作：对他们能投入多少时间抱有不切实际的期望，会让他们失去对你的尊重，甚至耗尽精力。我们不是鼓励你窥探成员的私生活，而是说，体察他们正在经历的个人处境，有助于理解为什么他们在某段时间产出较高或较低。成员家里正遇到难处时，多给一点余地，等将来团队必须赶上紧迫的期限，他们也会更愿意多投入些时间。

A big part of tracking your team members’ happiness is tracking their careers. If you ask a team member where they see their career in five years, most of the time you’ll get a shrug and a blank look. When put on the spot, most people won’t say much about this, but there are usually a few things that everyone would like to do in the next five years: be promoted, learn something new, launch something important, and work with smart people. Regardless of whether they verbalize this, most people are thinking about it. If you’re going to be an effective leader, you should be thinking about how you can help make all those things happen and let your team know you’re thinking about this. The most important part of this is to take these implicit goals and make them explicit so that when you’re giving career advice you have a real set of metrics with which to evaluate situations and opportunities.

关注成员的职业发展，是追踪幸福感的重要一环。如果问他们希望五年后的职业生涯是什么样，多半只会得到耸肩和茫然的目光。突然被这样问，大多数人说不出多少，但通常都有几件未来五年想做的事：晋升、学习新东西、推出重要成果、与聪明人共事。无论说不说出来，多数人都在想这些。要成为有效的领导者，你就应考虑怎样帮助他们实现这些愿望，并让团队知道你在为此思考。最重要的是，把未明说的目标明确下来，这样提供职业建议时，才有具体标准来评估处境和机会。

Tracking happiness comes down to not just monitoring careers, but also giving your team members opportunities to improve themselves, be recognized for the work they do, and have a little fun along the way.

追踪幸福感，不只是关注职业进展，还要让成员有机会提升自己，让付出得到认可，并在这个过程中享受一些乐趣。

## Other Tips and Tricks  其他提示和窍门

Following are other miscellaneous tips and tricks that we at Google recommend when you’re in a leadership position:

- *Delegate, but get your hands dirty*  
    When moving from an individual contributor role to a leadership role, achieving a balance is one of the most difficult things to do. Initially, you’re inclined to do all of the work yourself, and after being in a leadership role for a long time, it’s easy to get into the habit of doing none of the work yourself. If you’re new to a leadership role, you probably need to work hard to delegate work to other engineers on your team, even if it will take them a lot longer than you to accomplish that work. Not only is this one way for you to maintain your sanity, but also it’s how the rest of your team will learn. If you’ve been leading teams for a while or if you pick up a new team, one of the easiest ways to gain the team’s respect and get up to speed on what they’re doing is to get your hands dirty—usually by taking on a grungy task that no one else wants to do. You can have a resume and a list of achievements a mile long, but nothing lets a team know how skillful and dedicated (and humble) you are like jumping in and actually doing some hard work.

- *Seek to replace yourself*
    Unless you want to keep doing the exact same job for the rest of your career, seek to replace yourself. This starts, as we mentioned earlier, with the hiring process: if you want a member of your team to replace you, you need to hire people capable of replacing you, which we usually sum up by saying that you need to “hire people smarter than you.” After you have team members capable of doing your job, you need to give them opportunities to take on more responsibilities or occasionally lead the team. If you do this, you’ll quickly see who has the most aptitude to lead as well as who wants to lead the team. Remember that some people prefer to just be high-performing individual contributors, and that’s OK. We’ve always been amazed at companies that take their best engineers and—against their wishes—throw these engineers into management roles. This usually subtracts a great engineer from your team and adds a subpar manager.

- *Know when to make waves*  
    You will (inevitably and frequently) have difficult situations crop up in which every cell in your body is screaming at you to do nothing about it. It might be the engineer on your team whose technical chops aren’t up to par. It might be the person who jumps in front of every train. It might be the unmotivated employee who is working 30 hours a week. “Just wait a bit and it will get better,” you’ll tell yourself. “It will work itself out,” you’ll rationalize. Don’t fall into this trap—these are the situations for which you need to make the biggest waves and you need to make them now. Rarely will these problems work themselves out, and the longer you wait to address them, the more they’ll adversely affect the rest of the team and the more they’ll keep you up at night thinking about them. By waiting, you’re only delaying the inevitable and causing untold damage in the process. So act, and act quickly.

- *Shield* *your team from chaos*  
    When you step into a leadership role, the first thing you’ll usually discover is that outside your team is a world of chaos and uncertainty (or even insanity) that you never saw when you were an individual contributor. When I first became a manager back in the 1990s (before going back to being an individual contributor), I was taken aback by the sheer volume of uncertainty and organizational chaos that was happening in my company. I asked another manager what had caused this sudden rockiness in the otherwise calm company, and the other manager laughed hysterically at my naivete: the chaos had always been present, but my previous manager had shielded me and the rest of my team from it.

- *Give your team air cover*  
    Whereas it’s important that you keep your team informed about what’s going on “above” them in the company, it’s just as important that you defend them from a lot of the uncertainty and frivolous demands that can be imposed upon you from outside your team. Share as much information as you can with your team, but don’t distract them with organizational craziness that is extremely unlikely to ever actually affect them.

- *Let your team know when they’re doing well*  
    Many new team leads can get so caught up in dealing with the shortcomings of their team members that they neglect to provide positive feedback often enough. Just as you let someone know when they screw up, be sure to let them know when they do well, and be sure to let them (and the rest of the team) know when they knock one out of the park.

下面是我们在谷歌推荐的其他建议，供担任领导者时参考： 

- *委派任务，也要亲自动手*  
    从个人贡献者转向领导角色，最难的事情之一就是找到平衡。起初，你容易什么都自己做；带团队久了，又容易养成什么都不亲自做的习惯。刚上任时，你大概需要刻意练习把任务交给团队里的其他工程师，即使他们完成工作所需的时间比你长得多。这不仅能避免你忙到难以承受，也是其他成员学习的机会。如果你已带队一段时间，或刚接手新团队，赢得尊重、熟悉团队工作的一个简单办法，就是亲自动手，通常是接下一件别人不愿做的繁琐任务。无论履历多么丰富、成就清单多么长，都不如实际投入一项艰苦工作，更能让团队看见你的能力、投入和谦逊。

- *寻求继任者*  
    除非你想在余下的职业生涯里一直做同样的工作，否则就应寻找能接替自己的人。正如前文所说，这从招聘时就开始了：想让团队成员接替你，就得招有这种能力的人，也就是我们常说的“招聘比自己聪明的人”。有了能胜任你工作的人，还要给他们承担更多责任、偶尔带领团队的机会。这样很快就能看出，谁最有领导才能，谁又真正愿意带队。有些人更愿意做高绩效的个人贡献者，这完全没问题。有些公司却违背优秀工程师的意愿，硬把他们推上管理岗位，我们始终对此感到惊讶。这样做通常只是让团队少了一位优秀工程师，多了一位不称职的经理。

- *知道何时不能息事宁人*  
    你不可避免地会经常遇到一些难题，本能却拼命催促你什么也别做。可能是某位工程师技术不过关，可能是那个每列火车都要拦的人，也可能是缺乏动力、每周只工作30小时的员工。你会安慰自己：“再等等就会好。”“它自己会解决的。”不要掉进这个陷阱。这恰恰是最不能息事宁人的时候，而且必须立即行动。这些问题很少会自行消失；拖得越久，对其他成员的影响就越大，也越会让你夜不能寐。等待只是把迟早要做的事往后推，同时造成难以估量的损害。所以，要行动，而且要快。

- *保护团队免受混乱干扰*  
    走上领导岗位后，你首先发现的往往是：团队之外充满混乱和不确定性，甚至近乎疯狂，而当个人贡献者时，你从未见过这些。我在20世纪90年代第一次当经理时（后来又回去做过个人贡献者），就被公司里大量的不确定性和组织混乱震惊了。我问另一位经理，原本平静的公司为什么突然动荡起来。他听后大笑，觉得我太天真：混乱一直都在，只是原来的经理一直替我和团队其他成员挡着。

- *为团队提供掩护*  
    让团队了解公司“上面”发生的事很重要，但同样重要的是，替他们挡住来自团队之外的种种不确定性和无谓要求。尽可能多地分享信息，但不要让那些几乎不可能真正影响团队的组织乱象分散大家的注意力。

- *做得好时，让团队知道*  
    许多新任领导忙于处理成员的不足，却忘了经常给予正面反馈。出了错要指出来，做得好也要明确告诉对方；表现特别出色时，不仅要让本人知道，也要让整个团队知道。

Lastly, here’s something the best leaders know and use often when they have adventurous team members who want to try new things:

*It’s easy to say “yes” to something that’s easy to undo*  
    If you have a team member who wants to take a day or two to try using a new tool or library[^9] that could speed up your product (and you’re not on a tight deadline), it’s easy to say, “Sure, give it a shot.” If, on the other hand, they want to do something like launch a product that you’re going to have to support for the next 10 years, you’ll likely want to give it a bit more thought. Really good leaders have a good sense for when something can be undone, but more things are undoable than you think (and this applies to both technical and nontechnical decisions).

最后还有一条优秀领导者熟知的原则：面对敢于尝试新事物的成员，他们经常用得上。

*容易撤销的事，不妨爽快答应*  
    如果某位成员想花一两天试用新工具或新库，可能让产品运行得更快，而团队又没有紧迫的交付期限，你很容易就能答应：“好，试试看。”反过来，如果他想推出一个未来10年都要持续支持的产品，你大概就得多想一想。优秀领导者善于判断哪些事可以撤销；而实际上，可以撤销的事比你想象的更多，技术决策和非技术决策都是如此。

> [^9]: To gain a better understanding of just how “undoable” technical changes can be, see Chapter 22.  
>
> 9 要更好地理解技术变更究竟可以有多“容易撤销”，参见第22章。

## People Are Like Plants  人如植物

My wife is the youngest of six children, and her mother was faced with the difficult task of figuring out how to raise six very different children, each of whom needed different things. I asked my mother-in-law how she managed this (see what I did there?), and she responded that kids are like plants: some are like cacti and need little water but lots of sunshine, others are like African violets and need diffuse light and moist soil, and still others are like tomatoes and will truly excel if you give them a little fertilizer. If you have six kids and give each one the same amount of water, light, and fertilizer, they’ll all get equal treatment, but the odds are good that *none* of them will get what they actually need.

妻子在六个兄弟姐妹中最小。她母亲面临一项艰巨的任务：养育六个性格迥异、需求各不相同的孩子。我问岳母，她是怎样“管理”过来的（注意到我又用上这个词了吗？）。她回答，孩子就像植物：有的像仙人掌，少浇水、多晒太阳；有的像非洲紫罗兰，需要散射光和湿润的土壤；还有的像番茄，添一点肥就能长得很好。如果六个孩子得到的水、光照和肥料都一样，待遇倒是平等，却很可能没有一个真正得到所需的东西。

And so your team members are also like plants: some need more light, and some need more water (and some need more…fertilizer). It’s your job as their leader to determine who needs what and then give it to them—except instead of light, water, and fertilizer, your team needs varying amounts of motivation and direction.

团队成员也像植物：有的需要更多光照，有的需要更多水，还有的需要更多……肥料。作为领导，你要弄清谁需要什么，再满足他们的需求。只不过，团队需要的不是阳光、水和肥料，而是程度各异的激励与方向指引。

To get all of your team members what they need, you need to motivate the ones who are in a rut and provide stronger direction to those who are distracted or uncertain of what to do. Of course, there are those who are “adrift” and need both motivation and direction. So, with this combination of motivation and direction, you can make your team happy and productive. And you don’t want to give them too much of either—because if they don’t need motivation or direction and you try giving it to them, you’re just going to annoy them.

要让每位成员都得到所需的帮助，就要激励停滞不前的人，为注意力分散或不知该做什么的人提供更明确的方向。有些人茫然无措，既需要激励，也需要指引。把两者恰当地结合起来，就可以让团队愉快而富有成效地工作。但无论哪一种，都不要给得过多：对方不需要时还硬要提供，只会惹人厌烦。

Giving direction is fairly straightforward—it requires a basic understanding of what needs to be done, some simple organizational skills, and enough coordination to break it down into manageable tasks. With these tools in hand, you can provide sufficient guidance for an engineer in need of directional help. Motivation, however, is a bit more sophisticated and merits some explanation.

指明方向相对直接：基本了解要做什么，具备一些组织能力，再通过协调把工作拆成可管理的任务。有了这些，就能为缺少方向的工程师提供足够指导。激励则更复杂一些，需要进一步说明。

### Intrinsic Versus Extrinsic Motivation  内在动机与外在动机

There are two types of motivation: *extrinsic*, which originates from outside forces (such as monetary compensation), and *intrinsic*, which comes from within. In his book *Drive*,[^10] Dan Pink explains that the way to make people the happiest and most productive isn’t to motivate them extrinsically (e.g., throw piles of cash at them); rather, you need to work to increase their intrinsic motivation. Dan claims you can increase intrinsic motivation by giving people three things: autonomy, mastery, and purpose.[^11]

动机分为两类：*外在动机*来自薪酬等外部因素，*内在动机*则源于自身。丹·平克在《驱动》中指出，要让人最快乐、最有生产力，靠的不是外部激励，比如砸下大笔奖金，而是增强内在动机。他认为，要做到这一点，需要给人三样东西：自主性、精进的机会，以及工作的意义。

A person has autonomy when they have the ability to act on their own without someone micromanaging them.[^12] With autonomous employees (and Google strives to hire mostly autonomous engineers), you might give them the general direction in which they need to take the product but leave it up to them to decide how to get there. This helps with motivation not only because they have a closer relationship with the product (and likely know better than you how to build it), but also because it gives them a much greater sense of ownership of the product. The bigger their stake is in the success of the product, the greater their interest is in seeing it succeed.

一个人能够独立行动，不需要别人事无巨细地管控，就具备自主性。对于这样的员工（谷歌也力求主要招聘能自主工作的工程师），你可以给出产品发展的总体方向，把具体实现方式交给他们决定。这能增强动力，不仅因为他们更贴近产品，可能比你更清楚该怎样开发，还因为自主权会增强他们对产品的主人翁意识。他们觉得产品的成功与自己关系越密切，就越希望它成功。

Mastery in its basest form simply means that you need to give someone the opportunity to improve existing skills and learn new ones. Giving ample opportunities for mastery not only helps to motivate people, it also makes them better over time, which makes for stronger teams.[^13] An employee’s skills are like the blade of a knife: you can spend tens of thousands of dollars to find people with the sharpest skills for your team, but if you use that knife for years without sharpening it, you will wind up with a dull knife that is inefficient, and in some cases useless. Google gives ample opportunities for engineers to learn new things and master their craft so as to keep them sharp, efficient, and effective.

精进最基本的含义，就是给人机会提升已有技能、学习新技能。充分提供这样的机会，不仅能增强动力，还能让成员不断成长，使团队更强。员工的技能就像刀锋：你可以花数万美元招来技艺精湛的人，但一把刀若多年只用不磨，最终也会变钝，效率下降，甚至完全派不上用场。谷歌为工程师提供大量学习新事物、精进技艺的机会，让他们保持敏锐，既做得快，也做得好。

Of course, all the autonomy and mastery in the world isn’t going to help motivate someone if they’re doing work for no reason at all, which is why you need to give their work purpose. Many people work on products that have great significance, but they’re kept at arm’s length from the positive effects their products might have on their company, their customers, or even the world. Even for cases in which the product might have a much smaller impact, you can motivate your team by seeking the reason for their efforts and making this reason clear to them. If you can help them to see this purpose in their work, you’ll see a tremendous increase in their motivation and productivity.[14](#_bookmark464) One manager we know keeps a close eye on the email feedback that Google gets for its product (one of the “smaller-impact” products), and whenever she sees a message from a customer talking about how the company’s product has helped them personally or helped their business, she immediately forwards it to the engineering team. This not only motivates the team, but also frequently inspires team members to think about ways in which they can make their product even better.

当然，如果根本不知道为何而做，再多自主权和精进机会也无法激发动力。因此，你还要让成员的工作具有意义。许多人开发的产品意义重大，却看不到产品可能给公司、客户乃至世界带来的积极影响。即使产品影响较小，也可以找出大家付出努力的理由，并把它说清楚，以此激励团队。帮助成员看到工作意义后，你会发现他们的积极性和生产力显著提高。我们认识的一位经理，负责的正是一款“影响较小”的谷歌产品，她密切关注用户发来的反馈邮件。每当客户说起产品如何帮助了自己或自己的业务，她就立即转发给工程团队。这不但能激励大家，也常能启发成员思考怎样进一步改进产品。

> [^10]: See Dan’s fantastic TED talk on this subject.
>
> 10  参见丹关于这一主题的精彩 TED 演讲。
>
> [^11]: This assumes that the people in question are being paid well enough that income is not a source of stress.
>
> 11  前提是，这些人的薪酬已足以让收入不再成为压力来源。
>
> [^12]: This assumes that you have people on your team who don’t need micromanagement.
>
> 12  前提是，你的团队中有不需要事无巨细管控的人。
>
> [^13]:Of course, it also means they’re more valuable and marketable employees, so it’s easier for them to pick up and leave you if they’re not enjoying their work. See the pattern in “Track Happiness” on page 99.
>
> 13  当然，这也意味着他们的价值更高，在人才市场上更有竞争力；如果对工作不满意，他们也更容易另谋高就。参见第99页“追踪幸福感”中的做法。
>
> [^14]: Adam M. Grant, “The Significance of Task Significance: Job Performance Effects, Relational Mechanisms, and Boundary Conditions,” Journal of Applied Psychology, 93, No. 1 (2018), http://bit.ly/task_significance.
>
> 14  Adam M.Grant，《任务重要性的重要性：对工作绩效的影响、关系机制与边界条件》，《应用心理学杂志》，第93卷第1期（2018年），http://bit.ly/task_significance.

## Conclusion  总结

Leading a team is a different task than that of being a software engineer. As a result, good software engineers do not always make good managers, and that’s OK— effective organizations allow productive career paths for both individual contributors and people managers. Although Google has found that software engineering experience itself is invaluable for managers, the most important skills an effective manager brings to the table are social ones. Good managers enable their engineering teams by helping them work well, keeping them focused on proper goals, and insulating them from problems outside the group, all while following the three pillars of humility, trust, and respect.

带领团队与做软件工程师，是两种不同的工作。因此，优秀工程师不一定能成为优秀经理，这没有关系：有效的组织会为个人贡献者和人员管理者都提供良好的职业发展路径。谷歌的经验表明，软件工程经历对经理极为宝贵，但要做好管理，最重要的仍是人际交往能力。优秀经理帮助工程团队顺利工作、专注于正确目标，并免受团队之外的问题干扰，在整个过程中始终遵循谦逊、信任和尊重这三大原则。

## TL;DRs  内容提要

- Don’t “manage” in the traditional sense; focus on leadership, influence, and serving your team.
- Delegate where possible; don’t DIY (Do It Yourself).
- Pay particular attention to the focus, direction, and velocity of your team.

- 不要做传统意义上的“管理”；重点应是领导、影响他人，以及为团队服务。
- 尽可能委派任务，不要事事 DIY（自己动手）。
- 特别关注团队的专注点、方向和推进速度。
