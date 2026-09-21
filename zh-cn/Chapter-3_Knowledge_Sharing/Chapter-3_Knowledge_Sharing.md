
**CHAPTER  3**

# Knowledge Sharing 

# 第三章 知识共享

**Written by Nina Chen and Mark Barolak**

**Edited by Riona MacNamara**

Your organization understands your problem domain better than some random person on the internet; your organization should be able to answer most of its own questions. To achieve that, you need both experts who know the answers to those questions and mechanisms to distribute their knowledge, which is what we’ll explore in this chapter. These mechanisms range from the utterly simple (Ask questions; Write down what you know) to the much more structured, such as tutorials and classes. Most importantly, however, your organization needs a culture of learning, and that requires creating the psychological safety that permits people to admit to a lack of knowledge.

你的组织比网上随便找来的陌生人更了解自身的问题领域，因此应该能够解答自身的大多数问题。要做到这一点，既需要知道答案的专家，也需要传播这些专家知识的机制。这正是本章要探讨的内容。这些机制既可以很简单，比如提问、写下自己知道的内容，也可以更系统化，比如教程和课程。不过，最重要的是建立学习文化，而这需要营造心理安全感，让人们敢于承认自己有所不知。

## Challenges to Learning 学习的挑战
Sharing expertise across an organization is not an easy task. Without a strong culture of learning, challenges can emerge. Google has experienced a number of these challenges, especially as the company has scaled:

- *Lack of psychological safety*  
    An environment in which people are afraid to take risks or make mistakes in front of others because they fear being punished for it. This often manifests as a culture of fear or a tendency to avoid transparency. 
- *Information islands*  
    Knowledge fragmentation that occurs in different parts of an organization that don’t communicate with one another or use shared resources. In such anenvironment, each group develops its own way of doing things.[^1] This often leads to the following:  
  - **Information fragmentation**  
  	Each island has an incomplete picture of the bigger whole.  
  - **Information duplication**  
  	Each island has reinvented its own way of doing something.  
  - **Information skew**  
  	Each island has its own ways of doing the same thing, and these might or might not conflict.   
- *Single point of failure (SPOF)*  
    A bottleneck that occurs when critical information is available from only a single person. This is related to bus factor, which is discussed in more detail in Chapter 2.  
    SPOFs can arise out of good intentions: it can be easy to fall into a habit of “Let me take care of that for you.” But this approach optimizes for short-term efficiency (“It’s faster for me to do it”) at the cost of poor long-term scalability (the team never learns how to do whatever it is that needs to be done). This mindset also tends to lead to all-or-nothing expertise.  
- *All-or-nothing expertise*  
    A group of people that is split between people who know “everything” and novices, with little middle ground. This problem often reinforces itself if experts always do everything themselves and don’t take the time to develop new experts through mentoring or documentation. In this scenario, knowledge and responsibilities continue to accumulate on those who already have expertise, and new team members or novices are left to fend for themselves and ramp up more slowly.  
- *Parroting*   
    Mimicry without understanding. This is typically characterized by mindlessly copying patterns or code without understanding their purpose, often under the assumption that said code is needed for unknown reasons.
- *Haunted graveyards*   
    Places, often in code, that people avoid touching or changing because they are afraid that something might go wrong. Unlike the aforementioned parroting, haunted graveyards are characterized by people avoiding action because of fear and superstition.  

在组织内共享专业知识并非易事。如果缺乏深厚的学习文化，就可能遇到各种挑战。谷歌也经历过不少这样的挑战，尤其是在公司规模不断扩大的过程中：  

- *缺乏心理安全感*  
	在这样的环境中，人们害怕受到惩罚，因而不敢在别人面前冒险或犯错。这通常表现为恐惧文化，或不愿公开信息的倾向。  
- *信息孤岛*  
	组织各部分之间缺乏沟通，也不使用共享资源，导致知识彼此割裂。在这样的环境中，每个小组都会形成自己的做事方式。[^1] 这往往导致以下情况：  
	- **信息碎片化**  
		每个孤岛都只能看到整体的一部分。  
	- **信息重复**  
		每个孤岛都重复摸索出自己的一套做法。  
	- **信息偏差**  
		对于同一件事，每个孤岛都有自己的做法，这些做法可能相互冲突，也可能并不冲突。  
- *单点故障（SPOF）*  
	当关键信息只能从一个人那里获得时，就会出现瓶颈。这与巴士因子有关，在第二章有详细讨论。  
	SPOF 也可能源于好意：人们很容易养成“让我来帮你处理”的习惯。但这种做法追求短期效率（“我来做更快”），却牺牲了长期可扩展性（团队始终没有学会如何完成需要做的事）。这种心态也容易让专业能力走向两极分化。  
- *专业能力两极分化*  
	一群人分成了“什么都懂”的专家和新手，几乎没有处于中间水平的人。如果专家总是事事亲力亲为，不花时间通过指导或文档培养新的专家，这个问题往往会不断加剧。知识和责任继续集中在已有专业能力的人身上，新成员或新手则只能自己摸索，上手也更慢。  
- *鹦鹉学舌*  
	只模仿，不理解。典型表现是不加思考地复制模式或代码，却不了解其用途，往往只是认为这些代码总有某种自己不知道的必要性。  
- *闹鬼墓地*  
	人们担心出错，因而不敢触碰或修改的地方，通常是代码中的某些部分。与前面的鹦鹉学舌不同，闹鬼墓地的特点是人们出于恐惧和迷信而不敢行动。  

In the rest of this chapter, we dive into strategies that Google’s engineering organizations have found to be successful in addressing these challenges.

本章接下来将深入探讨谷歌工程组织在应对这些挑战时行之有效的策略。

> [^1]: In other words, rather than developing a single global maximum, we have a bunch of local maxima.    
     换句话说，我们得到的不是一个全局最大值，而是一组局部最大值。

## Philosophy  理念

Software engineering can be defined as the multiperson development of multiversion programs.[^2] People are at the core of software engineering: code is an important output but only a small part of building a product. Crucially, code does not emerge spontaneously out of nothing, and neither does expertise. Every expert was once a novice: an organization’s success depends on growing and investing in its people.

软件工程可以定义为由多人开发多版本程序。[^2] 人是软件工程的核心：代码是重要的产出，但在构建产品的工作中只占一小部分。关键在于，代码不会凭空出现，专业知识也一样。每位专家都曾是新手，组织的成功取决于对人才的培养和投入。

Personalized, one-to-one advice from an expert is always invaluable. Different team members have different areas of expertise, and so the best teammate to ask for any given question will vary. But if the expert goes on vacation or switches teams, the team can be left in the lurch. And although one person might be able to provide personalized help for one-to-many, this doesn’t scale and is limited to small numbers of “many.”

专家提供的个性化一对一建议始终十分宝贵。团队成员各有所长，不同的问题适合请教不同的同事。但如果专家休假或调往其他团队，原团队就可能陷入困境。一个人或许能以一对多的方式提供个性化帮助，但这种方式难以扩展，其中的“多”也只能是少数人。

Documented knowledge, on the other hand, can better scale not just to the team but to the entire organization. Mechanisms such as a team wiki enable many authors to share their expertise with a larger group. But even though written documentation is more scalable than one-to-one conversations, that scalability comes with some trade- offs: it might be more generalized and less applicable to individual learners’ situations, and it comes with the added maintenance cost required to keep information relevant and up to date over time.

相比之下，记录成文档的知识更容易在整个团队乃至整个组织内传播。团队 wiki 等机制让多位作者能够向更多人分享专业知识。不过，文档虽然比一对一交流更具可扩展性，也有相应的代价：内容可能更通用，不太贴合个别学习者的具体情况；而要让信息长期保持适用、及时更新，还需要额外的维护投入。

Tribal knowledge exists in the gap between what individual team members know and what is documented. Human experts know these things that aren’t written down. If we document that knowledge and maintain it, it is now available not only to somebody with direct one-to-one access to the expert today, but to anybody who can find and view the documentation.

团队成员知道、却没有写进文档的内容，就是口头知识。这些知识掌握在专家手中，但没有书面记录。如果将其记录下来并持续维护，能获取这些知识的就不再只是眼下能够直接向专家一对一请教的人，而是任何能够找到并阅读文档的人。

```
tribal knowledge：口头知识；是指一种仅存在于某个部落中的信息或知识， 这些知识不为外界所知，没有正式记录， 只能口口相传。
```

So in a magical world in which everything is always perfectly and immediately documented, we wouldn’t need to consult a person any more, right? Not quite. Written knowledge has scaling advantages, but so does targeted human help. A human expert can synthesize their expanse of knowledge. They can assess what information is applicable to the individual’s use case, determine whether the documentation is still relevant, and know where to find it. Or, if they don’t know where to find the answers, they might know who does.

那么，假如真有一个神奇的世界，所有知识都能立即、完整地记录下来，我们就不必再向人请教了，对吗？并非如此。书面知识有利于扩大知识传播的规模，有针对性的人工帮助也一样。专家能够融会贯通自己掌握的广泛知识，判断哪些信息适合提问者的具体场景、文档是否仍然适用，以及到哪里去找。即使不知道答案在哪里，他们也可能知道谁能找到答案。

> [^2]: David Lorge Parnas, Software Engineering: Multi-person Development of Multi-version Programs (Heidelberg: Springer-Verlag Berlin, 2011).  
    David Lorge Parnas，《软件工程：由多人开发多版本程序》（海德堡：Springer-Verlag Berlin，2011）。

Tribal and written knowledge complement each other. Even a perfectly expert team with perfect documentation needs to communicate with one another, coordinate with other teams, and adapt their strategies over time. No single knowledge-sharing approach is the correct solution for all types of learning, and the particulars of a good mix will likely vary based on your organization. Institutional knowledge evolves over time, and the knowledge-sharing methods that work best for your organization will likely change as it grows. Train, focus on learning and growth, and build your own stable of experts: there is no such thing as too much engineering expertise.

口头知识与书面知识相辅相成。即使团队成员个个都是专家，文档也完备无缺，仍然需要彼此沟通、与其他团队协调，并随时间推移调整策略。没有哪一种知识共享方式适合所有学习需求，最佳组合也可能因组织而异。组织积累的知识会不断演变，最有效的知识共享方式也可能随组织成长而变化。开展培训，重视学习与成长，培养自己的专家队伍：工程专业知识永远不嫌多。

## Setting the Stage: Psychological Safety 奠定基础：心理安全感

Psychological safety is critical to promoting a learning environment.

心理安全感是营造学习环境的关键。

To learn, you must first acknowledge that there are things you don’t understand. We should welcome such honesty rather than punish it. (Google does this pretty well, but sometimes engineers are reluctant to admit they don’t understand something.)

学习的第一步，是承认自己有不懂的地方。我们应该欢迎这种坦诚，而不是加以惩罚。（谷歌在这方面做得相当好，但工程师有时仍不愿承认自己有所不知。）

An enormous part of learning is being able to try things and feeling safe to fail. In a healthy environment, people feel comfortable asking questions, being wrong, and learning new things. This is a baseline expectation for all Google teams; indeed, our research has shown that psychological safety is the most important part of an effective team.

学习很重要的一部分，是敢于尝试，并且不因可能失败而感到不安。在健康的环境中，人们能够坦然提问、犯错、学习新事物。这是对所有谷歌团队的基本要求；事实上，我们的研究表明，心理安全感是高效团队最重要的因素。

### Mentorship 导师制

At Google, we try to set the tone as soon as a “Noogler” (new Googler) engineer joins the company. One important way of building psychological safety is to assign Nooglers a mentor—someone who is not their team member, manager, or tech lead— whose responsibilities explicitly include answering questions and helping the Noogler ramp up. Having an officially assigned mentor to ask for help makes it easier for the newcomer and means that they don’t need to worry about taking up too much of their coworkers’ time.

在谷歌，我们尽量从新工程师，也就是“Noogler”（谷歌新员工），入职时就确立这样的基调。建立心理安全感的一项重要做法，是为新人安排一位导师。导师不是新人的团队成员、经理或技术负责人，其职责明确包括答疑和帮助新人上手。有一位正式指定的导师可以请教，新人就更容易开口，也不必担心占用同事太多时间。

A mentor is a volunteer who has been at Google for more than a year and who is available to advise on anything from using Google infrastructure to navigating Google culture. Crucially, the mentor is there to be a safety net to talk to if the mentee doesn’t know whom else to ask for advice. This mentor is not on the same team as the mentee, which can make the mentee feel more comfortable about asking for help in tricky situations.

导师由在谷歌工作超过一年的志愿者担任，可以就使用谷歌基础设施、适应谷歌文化等各种问题提供建议。关键在于，当新人不知道还能找谁请教时，导师始终是可以求助的人。导师与新人不在同一团队，也能让新人在遇到棘手情况时更安心地寻求帮助。

Mentorship formalizes and facilitates learning, but learning itself is an ongoing process. There will always be opportunities for coworkers to learn from one another, whether it’s a new employee joining the organization or an experienced engineer learning a new technology. With a healthy team, teammates will be open not just to answering but also to asking questions: showing that they don’t know something and learning from one another.

导师制为学习提供了正式安排和便利，但学习本身是持续的过程。无论是新人加入组织，还是有经验的工程师学习新技术，同事之间总有相互学习的机会。在健康的团队中，成员不仅乐于回答问题，也愿意提问，坦承自己不懂的地方，彼此学习。

### Psychological Safety in Large Groups 大群体中的心理安全感

Asking a nearby teammate for help is easier than approaching a large group of mostly strangers. But as we’ve seen, one-to-one solutions don’t scale well. Group solutions are more scalable, but they are also scarier. It can be intimidating for novices to form a question and ask it of a large group, knowing that their question might be archived for many years. The need for psychological safety is amplified in large groups. Every member of the group has a role to play in creating and maintaining a safe environment that ensures that newcomers are confident asking questions and up-and- coming experts feel empowered to help those newcomers without the fear of having their answers attacked by established experts.

向身边的同事求助，比向一大群以陌生人为主的人求助容易。但前面也说过，一对一的方式难以扩展。面向群体的方式更具可扩展性，却也更让人畏惧。新手要组织好问题，再向一大群人提出，而且知道问题可能会被存档多年，难免感到紧张。群体越大，心理安全感就越重要。每位成员都应参与营造和维护安全的环境，让新人敢于提问，也让正在成长的专家放心帮助新人，不必担心自己的回答遭到资深专家攻击。

The most important way to achieve this safe and welcoming environment is for group interactions to be cooperative, not adversarial. Table 3-1 lists some examples of recommended patterns (and their corresponding antipatterns) of group interactions.

要营造安全、友好的环境，最重要的是让群体互动以合作为基础，而不是彼此对抗。表3-1列出了一些推荐的互动模式及其对应的反模式。

Table 3-1. Group interaction patterns

| Recommended patterns (cooperative)                                                     | Antipatterns (adversarial)                                                                 |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Basic questions or mistakes are guided in the proper direction                         | Basic questions or mistakes are picked on, and the person asking the question is chastised |
| Explanations are given with the intent of helping the person asking the question learn | Explanations are given with the intent of showing off one’s own knowledge                  |
| Responses are kind, patient, and helpful                                               | Responses are condescending, snarky, and unconstructive                                    |
| Interactions are shared discussions for finding solutions                              | Interactions are arguments with “winners” and “losers”                                     |

Table 3-1. 团队互动模式

| 推荐的模式（合作型）                | 反模式（对抗型）                          |
| --------------------------------- | -------------------------------------- |
| 对基础问题或错误给予正确引导         | 抓住基础问题或错误不放，责备提问者         |
| 解释是为了帮助提问者学习             | 解释是为了炫耀自己的知识                  |
| 回应友善、耐心，能够提供帮助         | 回应居高临下、尖酸刻薄，缺乏建设性         |
| 通过共同讨论寻找解决方案             | 争论非要分出“赢家”和“输家”               |

These antipatterns can emerge unintentionally: someone might be trying to be helpful but is accidentally condescending and unwelcoming. We find the [Recurse Center’s social rules ](https://oreil.ly/zGvAN)to be helpful here:

- *No feigned surprise (“What?! I can’t believe you don’t know what the stack is!”)*  
	Feigned surprise is a barrier to psychological safety and makes members of the group afraid of admitting to a lack of knowledge.
- *No* *“well-actuallys”*  
	Pedantic corrections that tend to be about grandstanding rather than precision.
- *No back-seat driving*  
	Interrupting an existing discussion to offer opinions without committing to the conversation.
- *No subtle “-isms” (“It’s so easy my grandmother could do it!”)*  
	Small expressions of bias (racism, ageism, homophobia) that can make individuals feel unwelcome, disrespected, or unsafe.

这些反模式可能在无意间出现：本想帮忙，却不经意地显得居高临下，让人感到不受欢迎。我们发现，[Recurse中心的社交规则](https://oreil.ly/zGvAN)对此很有帮助：

- *不要故作惊讶（“什么？！你居然不知道栈是什么！”）*    
	故作惊讶会破坏心理安全感，让群体成员不敢承认自己有所不知。  
- *不要以“其实……”的姿态挑错*  
	这种吹毛求疵的纠正，往往是为了出风头，而不是追求准确。
- *不要只在一旁指手画脚*  
	打断正在进行的讨论发表意见，却不真正参与对话。
- *不要流露隐蔽的歧视（“这太简单了，我奶奶都能做！”）*  
	细微的偏见表达，例如种族歧视、年龄歧视或恐同言论，也可能让人感到不受欢迎、不被尊重或不安全。


## Growing Your Knowledge 增进自己的知识

Knowledge sharing starts with yourself. It is important to recognize that you always have something to learn. The following guidelines allow you to augment your own personal knowledge.

知识共享从自己做起。首先要认识到，自己总有东西需要学习。以下准则有助于增进个人知识。

### Ask Questions 提问

If you take away only a single thing from this chapter, it is this: always be learning; always be asking questions.

如果从本章只记住一件事，那就是：持续学习，不断提问。

We tell Nooglers that ramping up can take around six months. This extended period is necessary to ramp up on Google’s large, complex infrastructure, but it also reinforces the idea that learning is an ongoing, iterative process. One of the biggest mistakes that beginners make is not to ask for help when they’re stuck. You might be tempted to struggle through it alone or feel fearful that your questions are “too simple.” “I just need to try harder before I ask anyone for help,” you think. Don’t fall into this trap! Your coworkers are often the best source of information: leverage this valuable resource.

我们会告诉新人，上手可能需要六个月左右。熟悉谷歌庞大而复杂的基础设施确实需要这么长时间，这也强调了一个观念：学习是持续迭代的过程。新手最容易犯的大错之一，就是卡住时不求助。你可能想独自硬撑，或者担心自己的问题“太简单”，心想：“在向别人求助之前，我得再努力一点。”不要落入这个陷阱！同事往往是最好的信息来源，要善用这一宝贵资源。

There is no magical day when you suddenly always know exactly what to do in every situation—there’s always more to learn. Engineers who have been at Google for years still have areas in which they don’t feel like they know what they are doing, and that’s OK! Don’t be afraid to say “I don’t know what that is; could you explain it?” Embrace not knowing things as an area of opportunity rather than one to fear.[^3]

不会有那么神奇的一天，让你突然知道在所有情况下究竟该怎么做。总有更多东西需要学习。即使在谷歌工作多年，工程师也仍会在某些领域感到无从下手，这没有关系！不要怕说：“我不知道那是什么，能解释一下吗？”把未知当作学习的机会，而不是恐惧的对象。[^3]

It doesn’t matter whether you’re new to a team or a senior leader: you should always be in an environment in which there’s something to learn. If not, you stagnate (and should find a new environment).

无论是刚加入团队的新人，还是资深领导者，都应让自己始终处于有东西可学的环境中。否则，你就会停滞不前，也该换个环境了。

It’s especially critical for those in leadership roles to model this behavior: it’s important not to mistakenly equate “seniority” with “knowing everything.” In fact, the more you know, [the more you know you don’t know](https://oreil.ly/VWusg). Openly asking questions[^4] or expressing gaps in knowledge reinforces that it’s OK for others to do the same.

领导者尤其需要以身作则，不要把“资历深”等同于“无所不知”。事实上，你知道的越多，[你知道你不知道的就越多](https://oreil.ly/VWusg)。公开提问[^4]，或坦承自己在知识上的欠缺，能让其他人更确信自己也可以这样做。

On the receiving end, patience and kindness when answering questions fosters an environment in which people feel safe looking for help. Making it easier to overcome the initial hesitation to ask a question sets the tone early: reach out to solicit questions, and make it easy for even “trivial” questions to get an answer. Although engineers could probably figure out tribal knowledge on their own, they’re not here to work in a vacuum. Targeted help allows engineers to be productive faster, which in turn makes their entire team more productive.

对回答问题的人来说，耐心和善意有助于营造让人安心求助的环境。应当尽早定下基调，帮助大家克服最初不敢提问的犹豫：主动邀请提问，让再“小”的问题也容易得到解答。工程师或许能够自行摸索出那些口头知识，但他们并不是来这里孤立工作的。有针对性的帮助能让工程师更快地投入有效工作，进而提高整个团队的生产力。

> [^3]: Impostor syndrome is not uncommon among high achievers, and Googlers are no exception—in fact, a majority of this book’s authors have impostor syndrome. We acknowledge that fear of failure can be difficult for those with impostor syndrome and can reinforce an inclination to avoid branching out.    
     冒名顶替综合征在成就出众的人群中并不少见，谷歌员工也不例外。事实上，本书的大多数作者都有这种感受。我们理解，对这些人来说，害怕失败可能很难克服，也可能使他们更不愿意涉足新的领域。
>
> [^4]: See “[How to ask good questions.](https://jvns.ca/blog/good-questions/).    
    见“如何提出好问题”。

### Understand Context 了解背景

Learning is not just about understanding new things; it also includes developing an understanding of the decisions behind the design and implementation of existing things. Suppose that your team inherits a legacy codebase for a critical piece of infrastructure that has existed for many years. The original authors are long gone, and the code is difficult to understand. It can be tempting to rewrite from scratch rather than spend time learning the existing code. But instead of thinking “I don’t get it” and ending your thoughts there, dive deeper: what questions should you be asking?

学习不仅是了解新事物，也包括理解现有设计与实现背后的决策。假设团队接手了一项关键基础设施的遗留代码库，它已经存在多年，原作者早已离开，代码又很难理解。与其花时间研究现有代码，从头重写似乎更有吸引力。但不要停留在“我看不懂”上，而要继续追问：自己应该提出哪些问题？

Consider the principle of “Chesterson’s fence”: before removing or changing something, first understand why it’s there.
>    In the matter of reforming things, as distinct from deforming them, there is one plain and simple principle; a principle which will probably be called a paradox. There exists in such a case a certain institution or law; let us say, for the sake of simplicity, a fence or gate erected across a road. The more modern type of reformer goes gaily up to it and says, “I don’t see the use of this; let us clear it away.” To which the more intelligent type of reformer will do well to answer: “If you don’t see the use of it, I certainly won’t let you clear it away. Go away and think. Then, when you can come back and tell me that you do see the use of it, I may allow you to destroy it.”

不妨想想“切斯特顿的栅栏”原则：在移除或改变某样东西之前，先弄清它为什么存在。
>   要改良事物，而不是把它改坏，有一条简单明了的原则，不过有人可能会称它为悖论。假设现有某种制度或法律；为便于说明，就把它想成横在路上的一道栅栏或大门。新派改革者兴冲冲地走上前说：“我看不出这有什么用，拆掉吧。”更明智的改革者则会这样回答：“如果你看不出它的用处，我当然不会让你拆掉它。先回去想清楚。等你能回来告诉我，你已经明白它的用处时，我才可能允许你拆掉它。”

This doesn’t mean that code can’t lack clarity or that existing design patterns can’t be wrong, but engineers have a tendency to reach for “this is bad!” far more quickly than is often warranted, especially for unfamiliar code, languages, or paradigms. Google is not immune to this. Seek out and understand context, especially for decisions that seem unusual. After you’ve understood the context and purpose of the code, consider whether your change still makes sense. If it does, go ahead and make it; if it doesn’t, document your reasoning for future readers.

这并不是说代码不可能晦涩，或现有设计模式不可能出错，而是工程师往往还没有充分依据，就急着断言“这太糟糕了！”，尤其在面对不熟悉的代码、语言或范式时。谷歌也不例外。应当主动了解背景，尤其是那些看起来不寻常的决策。弄清代码的背景和用途后，再判断自己的修改是否仍然合理。如果合理，就着手修改；如果不合理，就把理由记下来，留给后来的读者。

Many Google style guides explicitly include context to help readers understand the rationale behind the style guidelines instead of just memorizing a list of arbitrary rules. More subtly, understanding the rationale behind a given guideline allows authors to make informed decisions about when the guideline shouldn’t apply or whether the guideline needs updating. See Chapter 8.

谷歌的许多风格指南会明确交代背景，帮助读者理解规则背后的理由，而不是死记一串看似任意的规定。更深一层的价值在于，理解理由后，代码作者才能有依据地判断某条规则何时不适用，或是否需要更新。参见第8章。

## Scaling Your Questions: Ask the Community 扩大求助范围：向社区提问

Getting one-to-one help is high bandwidth but necessarily limited in scale. And as a learner, it can be difficult to remember every detail. Do your future self a favor: when you learn something from a one-to-one discussion, write it down.

一对一求助的沟通带宽很高，但能覆盖的人数必然有限。作为学习者，也很难记住每个细节。不妨帮未来的自己一个忙：从一对一讨论中学到东西时，就把它记下来。

Chances are that future newcomers will have the same questions you had. Do them a favor, too, and share what you write down.

后来加入的新人很可能会遇到和你一样的问题。也帮他们一个忙，把记下来的内容分享出去。

Although sharing the answers you receive can be useful, it’s also beneficial to seek help not from individuals but from the greater community. In this section, we examine different forms of community-based learning. Each of these approaches—group chats, mailing lists, and question-and-answer systems—have different trade-offs and complement one another. But each of them enables the knowledge seeker to get help from a broader community of peers and experts and also ensures that answers are broadly available to current and future members of that community.

分享自己得到的答案固然有用，直接向更广泛的社区而非个人求助也有好处。本节将讨论几种依托社区的学习形式：群聊、邮件列表和问答系统。它们各有取舍，也相互补充，但都能让求知者向更多同行和专家寻求帮助，并让社区当前及未来的成员都能广泛获取这些答案。

### Group Chats 群聊

When you have a question, it can sometimes be difficult to get help from the right person. Maybe you’re not sure who knows the answer, or the person you want to ask is busy. In these situations, group chats are great, because you can ask your question to many people at once and have a quick back-and-forth conversation with whoever is available. As a bonus, other members of the group chat can learn from the question and answer, and many forms of group chat can be automatically archived and searched later.

遇到问题时，有时很难找到合适的人求助：你可能不知道谁有答案，也可能想请教的人正忙。这时，群聊就很有用。你可以同时向多人提问，与有空的人快速来回交流。此外，群内其他成员也能从问答中学习，而且许多群聊工具支持自动存档，方便日后搜索。

Group chats tend to be devoted either to topics or to teams. Topic-driven group chats are typically open so that anyone can drop in to ask a question. They tend to attract experts and can grow quite large, so questions are usually answered quickly. Team- oriented chats, on the other hand, tend to be smaller and restrict membership. As a result, they might not have the same reach as a topic-driven chat, but their smaller size can feel safer to a newcomer.

群聊通常围绕特定主题或团队建立。主题群一般对所有人开放，谁都可以加入提问。这类群容易吸引专家，人数也可能很多，因此问题通常能很快得到解答。团队群则往往人数较少，并限制成员加入。它们的覆盖范围可能不如主题群，但较小的群体也能让新人更有安全感。

Although group chats are great for quick questions, they don’t provide much structure, which can make it difficult to extract meaningful information from a conversation in which you’re not actively involved. As soon as you need to share information outside of the group, or make it available to refer back to later, you should write a document or email a mailing list.

群聊适合快速提问，但内容缺乏结构，没有直接参与讨论的人往往很难从中提取有用信息。一旦需要把信息分享给群外的人，或留作日后参考，就应该写成文档，或发送到邮件列表。

### Mailing Lists 邮件列表

Most topics at Google have a topic-users@ or topic-discuss@ Google Groups mailing list that anyone at the company can join or email. Asking a question on a public mailing list is a lot like asking a group chat: the question reaches a lot of people who could potentially answer it and anyone following the list can learn from the answer. Unlike group chats, though, public mailing lists are easy to share with a wider audience: they are packaged into searchable archives, and email threads provide more structure than group chats. At Google, mailing lists are also indexed and can be discovered by Moma, Google’s intranet search engine.

谷歌的大多数主题都有对应的 Google Groups 邮件列表，地址形如 topic-users@ 或 topic-discuss@，公司内任何人都可以加入或发邮件。在公开邮件列表上提问与群聊很相似：问题能够送达许多可能知道答案的人，所有关注列表的人也都能从回答中学习。不过，公开邮件列表比群聊更容易分享给更广泛的受众：邮件会形成可搜索的存档，讨论串也比群聊更有条理。在谷歌，邮件列表还会被内网搜索引擎 Moma 索引，便于查找。

When you find an answer to a question you asked on a mailing list, it can be tempting to get on with your work. Don’t do it! You never know when someone will need the same information in the future, so it’s a best practice to post the answer back to the list.

在邮件列表上提问后，如果找到了答案，你可能想立刻回去继续工作。先别急！以后随时可能有人需要同样的信息，因此最好先把答案发回邮件列表。

Mailing lists are not without their trade-offs. They’re well suited for complicated questions that require a lot of context, but they’re clumsy for the quick back-and- forth exchanges at which group chats excel. A thread about a particular problem is generally most useful while it is active. Email archives are immutable, and it can be hard to determine whether an answer discovered in an old discussion thread is still relevant to a present-day situation. Additionally, the signal-to-noise ratio can be lower than other mediums like formal documentation because the problem that someone is having with their specific workflow might not be applicable to you.

邮件列表也需要权衡。它适合讨论需要大量背景信息的复杂问题，却不擅长群聊式的快速来回交流。围绕某个问题的讨论串，通常在讨论活跃时最有价值。邮件存档无法修改，因此从旧讨论中找到答案后，很难判断它是否仍适用于眼下的情况。此外，某人在特定工作流中遇到的问题未必与你有关，所以邮件列表的信噪比可能低于正式文档等其他媒介。

------

#### Email at Google  谷歌的电子邮件

Google culture is infamously email-centric and email-heavy. Google engineers receive hundreds of emails (if not more) each day, with varying degrees of actionability. Nooglers can spend days just setting up email filters to deal with the volume of notifications coming from groups that they’ve been autosubscribed to; some people just give up and don’t try to keep up with the flow. Some groups CC large mailing lists onto every discussion by default, without trying to target information to those who are likely to be specifically interested in it; as a result, the signal-to-noise ratio can be a real problem.

谷歌以邮件为中心、邮件量庞大的文化早已出了名。工程师每天会收到数百封甚至更多邮件，其中有些需要采取行动，有些则未必。新人光是设置邮件过滤规则，就可能花上好几天，以应付自动订阅的群组发来的大量通知；有些人干脆放弃，不再试图跟上邮件流。一些群组默认把每次讨论都抄送给大型邮件列表，而不是有针对性地发给可能关心这件事的人，结果信噪比就成了严重问题。

Google tends toward email-based workflows by default. This isn’t necessarily because email is a better medium than other communications options—it often isn’t—rather, it’s because that’s what our culture is accustomed to. Keep this in mind as your organization considers what forms of communication to encourage or invest in.

谷歌通常默认采用基于邮件的工作流。这未必是因为邮件优于其他沟通方式，事实上往往并非如此，而是因为我们的文化已经习惯了它。组织在考虑鼓励或投入哪种沟通方式时，应当记住这一点。

------

### YAQS: Question-and-Answer Platform YAQS：问答平台

YAQS (“Yet Another Question System”) is a Google-internal version of a [Stack Overflow](https://oreil.ly/iTtbm)–like website, making it easy for Googlers to link to existing or work-in-progress code as well as discuss confidential information.

YAQS（“又一个问答系统”）是谷歌内部类似[Stack Overflow](https://oreil.ly/iTtbm)的网站，方便员工引用现有或正在开发的代码，也可以在其中讨论机密信息。

Like Stack Overflow, YAQS shares many of the same advantages of mailing lists and adds refinements: answers marked as helpful are promoted in the user interface, and users can edit questions and answers so that they remain accurate and useful as code and facts change. As a result, some mailing lists have been superseded by YAQS, whereas others have evolved into more general discussion lists that are less focused on problem solving.

与 Stack Overflow 一样，YAQS 具备邮件列表的许多优点，并作了进一步改进：标为有帮助的答案会在界面上优先展示，用户也能编辑问题和答案，使其在代码和实际情况变化后仍然准确、有用。因此，一些邮件列表已被 YAQS 取代，另一些则演变为话题更广泛的讨论列表，不再那么侧重于解决问题。

## Scaling Your Knowledge:You Always Have Something to Teach 扩大知识传播：你总有东西可以教给别人

Teaching is not limited to experts, nor is expertise a binary state in which you are either a novice or an expert. Expertise is a multidimensional vector of what you know: everyone has varying levels of expertise across different areas. This is one of the reasons why diversity is critical to organizational success: different people bring different perspectives and expertise to the table (see Chapter 4). Google engineers teach others in a variety of ways, such as office hours, giving tech talks, teaching classes, writing documentation, and reviewing code.

传授知识并非专家的专利，专业能力也不是非新手即专家的二元状态。它是由你所掌握的知识构成的多维向量：每个人在不同领域的专业水平各不相同。这也是多样性对组织成功至关重要的原因之一，不同的人能带来不同的视角与专长（见第4章）。谷歌工程师通过多种方式传授知识，包括定时答疑、技术讲座、授课、编写文档和代码审查。

### Office Hours 定时答疑

Sometimes it’s really important to have a human to talk to, and in those instances, office hours can be a good solution. Office hours are a regularly scheduled (typically weekly) event during which one or more people make themselves available to answer questions about a particular topic. Office hours are almost never the first choice for knowledge sharing: if you have an urgent question, it can be painful to wait for the next session for an answer; and if you’re hosting office hours, they take up time and need to be regularly promoted. That said, they do provide a way for people to talk to an expert in person. This is particularly useful if the problem is still ambiguous enough that the engineer doesn’t yet know what questions to ask (such as when they’re just starting to design a new service) or whether the problem is about something so specialized that there just isn’t documentation on it.

有时，能直接与人交流非常重要，定时答疑就是一种不错的办法。这类活动按固定时间举行，通常每周一次，由一人或多人就某个主题回答问题。它几乎不会是知识共享的首选：提问者遇到紧急问题时，很难等到下一次答疑；主持者也需要投入时间，并定期宣传活动。不过，它确实提供了与专家当面交流的机会。当问题还很模糊，工程师甚至不知道该问什么时，例如刚开始设计一项新服务，或问题十分专业、根本没有相关文档时，这种方式尤其有用。

### Tech Talks and Classes 技术讲座和课程

Google has a robust culture of both internal and external[^5] tech talks and classes. Our engEDU (Engineering Education) team focuses on providing Computer Science education to many audiences, ranging from Google engineers to students around the world. At a more grassroots level, our g2g (Googler2Googler) program lets Googlers sign up to give or attend talks and classes from fellow Googlers.[^6] The program is wildly successful, with thousands of participating Googlers teaching topics from the technical (e.g., “Understanding Vectorization in Modern CPUs”) to the just-for-fun (e.g., “Beginner Swing Dance”).

谷歌有浓厚的技术讲座与课程文化，既面向内部，也面向外部。[^5] engEDU（工程教育）团队专注于为不同受众提供计算机科学教育，从谷歌工程师到世界各地的学生都包括在内。在员工自发参与的层面，g2g（Googler2Googler）计划让员工可以报名主讲或参加同事开设的讲座和课程。[^6] 该计划非常成功，数千名员工参与授课，主题既有技术内容，例如“理解现代 CPU 中的向量化”，也有纯粹出于兴趣的内容，例如“摇摆舞入门”。

Tech talks typically consist of a speaker presenting directly to an audience. Classes, on the other hand, can have a lecture component but often center on in-class exercises and therefore require more active participation from attendees. As a result, instructor-led classes are typically more demanding and expensive to create and maintain than tech talks and are reserved for the most important or difficult topics. That said, after a class has been created, it can be scaled relatively easily because many instructors can teach a class from the same course materials. We’ve found that classes tend to work best when the following circumstances exist:

- The topic is complicated enough that it’s a frequent source of misunderstanding. Classes take a lot of work to create, so they should be developed only when they’re addressing specific needs.
- The topic is relatively stable. Updating class materials is a lot of work, so if the subject is rapidly evolving, other forms of sharing knowledge will have a better bang for the buck.
- The topic benefits from having teachers available to answer questions and provide personalized help. If students can easily learn without directed help, self- serve mediums like documentation or recordings are more efficient. A number of introductory classes at Google also have self-study versions.
- There is enough demand to offer the class regularly. Otherwise, potential learners will get the information they need in other ways rather than waiting for the class. At Google, this is particularly a problem for small, geographically remote offices.

技术讲座通常以讲者向听众讲解为主。课程虽然也可能包含讲授环节，但往往以课堂练习为核心，需要学员更主动地参与。因此，与技术讲座相比，教师授课的课程通常更难设计和维护，成本也更高，一般只用于最重要或最难的主题。不过，课程设计完成后，扩大授课规模相对容易，因为不同教师可以使用同一套材料。我们发现，课程在以下情况下往往最有效：

- 主题足够复杂，经常引起误解。设计课程需要大量工作，因此只应为明确的需求开发课程。
- 主题相对稳定。更新课程材料很费工夫；如果内容变化很快，采用其他知识共享方式会更划算。
- 教师答疑和个性化帮助对学习这一主题确有价值。如果学员无需指导就能轻松掌握，文档或录播等自学材料会更高效。谷歌的一些入门课程也提供自学版本。
- 需求足以支持定期开课。否则，学习者会通过其他途径获取所需信息，而不是等着开课。在谷歌，规模较小、地理位置偏远的办公室尤其容易遇到这个问题。

> [^5]: https://talksat.withgoogle.com and https://www.youtube.com/GoogleTechTalks, to name a few.    
    https://talksat.withgoogle.com 和 [https://www.youtube.com/GoogleTechTalks](https://www.youtube.com/GoogleTechTalks)，仅举几例。
> [^6]: The g2g program is detailed in: Laszlo Bock, Work Rules!: Insights from Inside Google That Will Transform How You Live and Lead (New York: Twelve Books, 2015). It includes descriptions of different aspects of the program as well as how to evaluate impact and recommendations for what to focus on when setting up similar programs.    
    g2g 计划详见 Laszlo Bock 的《工作规则！：来自谷歌内部、将改变你生活与领导方式的洞见》（纽约：Twelve Books，2015）。书中介绍了该计划的各个方面、如何评估其影响，以及建立类似计划时应重点关注什么。

### Documentation 文档

Documentation is written knowledge whose primary goal is to help its readers learn something. Not all written knowledge is necessarily documentation, although it can be useful as a paper trail. For example, it’s possible to find an answer to a problem in a mailing list thread, but the primary goal of the original question on the thread was to seek answers, and only secondarily to document the discussion for others.

文档是以帮助读者学习为首要目的的书面知识。并非所有写下来的知识都算文档，尽管它们也可以留下有用的记录。例如，邮件列表的讨论串中可能有某个问题的答案，但最初提问的首要目的是寻求答案，为他人记录讨论只是次要目的。

In this section, we focus on spotting opportunities for contributing to and creating formal documentation, from small things like fixing a typo to larger efforts such as documenting tribal knowledge.

本节重点讨论如何发现完善和创建正式文档的机会，小到纠正错别字，大到把口头知识记录下来。

#### Updating documentation 更新文档

The first time you learn something is the best time to see ways that the existing documentation and training materials can be improved. By the time you’ve absorbed and understood a new process or system, you might have forgotten what was difficult or what simple steps were missing from the “Getting Started” documentation. At this stage, if you find a mistake or omission in the documentation, fix it! Leave the campground cleaner than you found it,[^7] and try to update the documents yourself, even when that documentation is owned by a different part of the organization.

初次学习某样东西时，最容易发现现有文档和培训材料的改进空间。等你已经理解并掌握一个新流程或系统，可能早就忘了当初哪里难懂，或“入门”文档漏掉了哪些简单步骤。因此，学习时如果发现文档有错误或遗漏，就动手修正！离开时让营地比来时更干净。[^7] 即使文档由组织内其他部门负责，也应尝试自己更新。

At Google, engineers feel empowered to update documentation regardless of who owns it—and we often do—even if the fix is as small as correcting a typo. This level of community upkeep increased notably with the introduction of g3doc,[^8] which made it much easier for Googlers to find a documentation owner to review their suggestion. It also leaves an auditable trail of change history no different than that for code.

在谷歌，无论文档由谁负责，工程师都认为自己可以参与更新，哪怕只是改一个拼写错误；我们也经常这样做。引入 g3doc[^8] 后，这种共同维护文档的做法明显增多，因为员工更容易找到文档负责人，请其审查修改建议。文档也因此能像代码一样，留下可审计的变更历史。

#### Creating documentation 创建文档

As your proficiency grows, write your own documentation and update existing docs. For example, if you set up a new development flow, document the steps. You can then make it easier for others to follow in your path by pointing them to your document. Even better, make it easier for people to find the document themselves. Any sufficiently undiscoverable or unsearchable documentation might as well not exist. This is another area in which g3doc shines because the documentation is predictably located right next to the source code, as opposed to off in an (unfindable) document or webpage somewhere.

随着熟练程度提高，应当编写自己的文档，并更新现有文档。例如，建立了新的开发流程，就把步骤记下来。以后只要向别人提供文档，就能让他们更容易照着完成。更好的做法，是让人们能够自行找到文档。文档如果难以发现、无法搜到，就几乎等于不存在。这也是 g3doc 的一项优势：文档就在源代码旁边，位置明确，而不是散落在某个难以找到的文档或网页里。

Finally, make sure there’s a mechanism for feedback. If there’s no easy and direct way for readers to indicate that documentation is outdated or inaccurate, they are likely not to bother telling anyone, and the next newcomer will come across the same problem. People are more willing to contribute changes if they feel that someone will actually notice and consider their suggestions. At Google, you can file a documentation bug directly from the document itself.

最后，要确保有反馈机制。如果读者没有简单直接的渠道指出文档过时或不准确，就很可能不再费心反馈，后来的新人也会遇到同样的问题。人们相信自己的建议确实会被关注和考虑时，才更愿意贡献修改。在谷歌，可以直接从文档页面提交文档问题单。

In addition, Googlers can easily leave comments on g3doc pages. Other Googlers can see and respond to these comments and, because leaving a comment automatically files a bug for the documentation owner, the reader doesn’t need to figure out who to contact.

此外，谷歌员工可以很方便地在 g3doc 页面留言，其他员工也能查看和回复。留言会自动为文档负责人创建问题单，因此读者无需先弄清该联系谁。

####  Promoting documentation  推广文档

Traditionally, encouraging engineers to document their work can be difficult. Writing documentation takes time and effort that could be spent on coding, and the benefits that result from that work are not immediate and are mostly reaped by others. Asymmetrical trade-offs like these are good for the organization as a whole given that many people can benefit from the time investment of a few, but without good incentives, it can be challenging to encourage such behavior. We discuss some of these structural incentives in the section “Incentives and recognition” on page 57.

让工程师为自己的工作编写文档，一向不是件容易的事。写文档要投入本可用于编码的时间和精力，收益却不会立刻显现，而且主要由他人获得。少数人投入时间，许多人从中受益，这种付出与收益不对称的安排有利于整个组织；但如果缺乏有效激励，就很难鼓励大家这样做。第57页的“激励与认可”一节将讨论一些制度层面的激励方式。

However, a document author can often directly benefit from writing documentation. Suppose that team members always ask you for help debugging certain kinds of production failures. Documenting your procedures requires an upfront investment of time, but after that work is done, you can save time in the future by pointing team members to the documentation and providing hands-on help only when needed.

不过，文档作者往往也能直接受益。假设团队成员总来请你帮忙排查某类生产故障。把排查步骤记录下来，起初需要投入时间，但完成后就可以请同事先看文档，只在必要时亲自协助，从而节省今后的时间。

Writing documentation also helps your team and organization scale. First, the information in the documentation becomes canonicalized as a reference: team members can refer to the shared document and even update it themselves. Second, the canonicalization may spread outside the team. Perhaps some parts of the documentation are not unique to the team’s configuration and become useful for other teams looking to resolve similar problems.

编写文档也有助于团队和组织扩大规模。首先，文档中的信息成为共同认可的参考依据，团队成员可以查阅，甚至自行更新。其次，这份参考也可能被团队之外的人采用。文档中的某些内容未必只适用于本团队的配置，因此也能帮助其他团队解决类似问题。

> [^7]: See “[The Boy Scout Rule](https://oreil.ly/2u1Ce)” and Kevlin Henney, 97 Things Every Programmer Should Know (Boston: O’Reilly, 2010).    
     见“童子军规则”，以及 Kevlin Henney 的《每个程序员都应该知道的97件事》（波士顿：O'Reilly，2010）。
>
> [^8]: g3doc stands for “google3 documentation.” google3 is the name of the current incarnation of Google’s monolithic source repository.    
    g3doc 是“google3 documentation”的缩写。google3 是谷歌当前这套单体源代码仓库的名称。

### Code 代码

At a meta level, code is knowledge, so the very act of writing code can be considered a form of knowledge transcription. Although knowledge sharing might not be a direct intent of production code, it is often an emergent side effect, which can be facilitated by code readability and clarity.

从更高一层看，代码本身就是知识，因此编写代码也可以视为记录知识的一种方式。知识共享未必是生产代码的直接目的，却常常是随之产生的效果；让代码易读、清晰，有助于这种共享。

Code documentation is one way to share knowledge; clear documentation not only benefits consumers of the library, but also future maintainers. Similarly, implementation comments transmit knowledge across time: you’re writing these comments expressly for the sake of future readers (including Future You!). In terms of trade- offs, code comments are subject to the same downsides as general documentation: they need to be actively maintained or they can quickly become out of date, as anyone who has ever read a comment that directly contradicts the code can attest.

代码文档是共享知识的一种方式。清晰的文档不仅帮助库的使用者，也帮助未来的维护者。同样，实现中的注释能让知识跨越时间：写这些注释，本来就是为了未来的读者，包括未来的自己。从权衡的角度看，代码注释与一般文档有同样的缺点：需要主动维护，否则很快就会过时。任何读过与代码直接矛盾的注释的人，都能体会这一点。

Code reviews (see Chapter 9) are often a learning opportunity for both author(s) and reviewer(s). For example, a reviewer’s suggestion might introduce the author to a new testing pattern, or a reviewer might learn of a new library by seeing the author use it in their code. Google standardizes mentoring through code review with the readability process, as detailed in the case study at the end of this chapter.

代码审查（见第9章）往往是作者和审查者共同学习的机会。例如，审查建议可能让作者了解到一种新的测试模式，审查者也可能从作者的代码中认识一个新库。谷歌通过 Readability（可读性认证）流程，将代码审查中的指导标准化。本章末尾的案例研究将详细介绍这一流程。

## Scaling Your Organization’s Knowledge 扩大组织内的知识传播

Ensuring that expertise is appropriately shared across the organization becomes more difficult as the organization grows. Some things, like culture, are important at every stage of growth, whereas others, like establishing canonical sources of information, might be more beneficial for more mature organizations.

组织规模越大，就越难确保专业知识在整个组织内得到适当共享。有些因素，例如文化，在每个成长阶段都很重要；另一些做法，例如建立权威信息源，可能对更成熟的组织更有价值。

### Cultivating a Knowledge-Sharing Culture 培养知识共享文化

Organizational culture is the squishy human thing that many companies treat as an afterthought. But at Google, we believe that focusing on the culture and environment first[^9] results in better outcomes than focusing on only the output—such as the code— of that environment.

组织文化关乎人，难以明确界定，许多公司往往事后才想起它。但在谷歌，我们相信，先关注文化和环境[^9]，比只关注这种环境中的产出，例如代码，能取得更好的结果。

Making major organizational shifts is difficult, and countless books have been written on the topic. We don’t pretend to have all the answers, but we can share specific steps Google has taken to create a culture that promotes learning.

推动重大的组织变革并不容易，讨论这一主题的书籍已经不计其数。我们并不自称掌握了所有答案，但可以分享谷歌为营造学习文化而采取的具体措施。

See the book Work Rules [^10] for a more in-depth examination of Google’s culture.

想更深入地了解谷歌文化，可以参阅《工作规则！》[^10]。

> [^9]: Laszlo Bock, Work Rules!: Insights from Inside Google That Will Transform How You Live and Lead (New York: Twelve Books, 2015).    
  Laszlo Bock，《工作规则！：来自谷歌内部、将改变你生活与领导方式的洞见》（纽约：Twelve Books，2015）。
>
> [^10]: Ibid.   
    同上。

### Respect 尊重

The bad behavior of just a few individuals can make an entire team or community unwelcoming. In such an environment, novices learn to take their questions elsewhere, and potential new experts stop trying and don’t have room to grow. In the worst cases, the group reduces to its most toxic members. It can be difficult to recover from this state.

只要少数人行为恶劣，就足以让整个团队或社区变得不友好。在这样的环境中，新手会转向别处求助，有潜力成长为专家的人也会停止尝试，失去成长空间。最坏的情况下，群体中只剩下那些破坏氛围最严重的人。到了这一步，就很难恢复过来。

Knowledge sharing can and should be done with kindness and respect. In tech, tolerance—or worse, reverence—of the “brilliant jerk” is both pervasive and harmful, but being an expert and being kind are not mutually exclusive. The Leadership section of Google’s software engineering job ladder outlines this clearly:    
    Although a measure of technical leadership is expected at higher levels, not all leadership is directed at technical problems. Leaders improve the quality of the people around them, improve the team’s psychological safety, create a culture of teamwork and collaboration, defuse tensions within the team, set an example of Google’s culture and values, and make Google a more vibrant and exciting place to work. Jerks are not good leaders.

知识共享可以，也应该以善意和尊重为基础。在科技行业，容忍“聪明的混蛋”，甚至推崇这类人的现象既普遍又有害，但专业能力与待人友善并不矛盾。谷歌软件工程师职级标准中的“领导力”部分对此有明确说明：     
    较高职级的工程师需要具备一定的技术领导力，但领导力并不只针对技术问题。领导者应当帮助身边的人提升能力，增强团队的心理安全感，营造团队协作文化，化解内部紧张关系，在践行谷歌文化和价值观方面以身作则，让谷歌成为更有活力、更令人振奋的工作场所。混蛋不是好领导。

This expectation is modeled by senior leadership: Urs Hölzle (Senior Vice President of Technical Infrastructure) and Ben Treynor Sloss (Vice President, Founder of Google SRE) wrote a regularly cited internal document (“No Jerks”) about why Googlers should care about respectful behavior at work and what to do about it.

高层领导也以身作则。Urs Hölzle（技术基础设施高级副总裁）和 Ben Treynor Sloss（副总裁、谷歌 SRE 创始人）撰写了内部文档“No Jerks”，说明谷歌员工为什么应在工作中重视尊重他人，以及具体该怎么做。这份文档经常被引用。

### Incentives and recognition  激励与认可

Good culture must be actively nurtured, and encouraging a culture of knowledge sharing requires a commitment to recognizing and rewarding it at a systemic level. It’s a common mistake for organizations to pay lip service to a set of values while actively rewarding behavior that does not enforce those values. People react to incentives over platitudes, and so it’s important to put your money where your mouth is by putting in place a system of compensation and awards.

良好的文化需要主动培育；要鼓励知识共享，就必须从制度上给予认可和奖励。组织常犯的错误，是嘴上倡导一套价值观，实际却奖励不符合这些价值观的行为。与空泛的口号相比，激励更能影响行动。因此，应建立相应的薪酬和奖励制度，把承诺落到实处。

Google uses a variety of recognition mechanisms, from company-wide standards such as performance review and promotion criteria to peer-to-peer awards between Googlers.

谷歌采用多种认可机制，既有全公司统一的绩效评估和晋升标准，也有同事之间相互授予的奖励。

Our software engineering ladder, which we use to calibrate rewards like compensation and promotion across the company, encourages engineers to share knowledge by noting these expectations explicitly. At more senior levels, the ladder explicitly calls out the importance of wider influence, and this expectation increases as seniority increases. At the highest levels, examples of leadership include the following: 

- Growing future leaders by serving as mentors to junior staff, helping them develop both technically and in their Google role
- Sustaining and developing the software community at Google via code and design reviews, engineering education and development, and expert guidance to others in the field

我们用软件工程师职级标准统一全公司的薪酬、晋升等奖励尺度，并在其中明确写出知识共享的要求，以鼓励工程师分享知识。较高职级的标准明确强调扩大影响力的重要性，而且职级越高，要求也越高。对于最高职级，领导力的表现包括：

- 担任初级员工的导师，帮助他们提升技术能力、在谷歌的岗位上成长，培养未来的领导者。
- 通过代码审查、设计审查、工程教育与人才培养，以及为该领域其他人提供专业指导，维系并发展谷歌的软件社区。

Job ladder expectations are a top-down way to direct a culture, but culture is also formed from the bottom up. At Google, the peer bonus program is one way we embrace the bottom-up culture. Peer bonuses are a monetary award and formal recognition that any Googler can bestow on any other Googler for above-and-beyond work.[^11] For example, when Ravi sends a peer bonus to Julia for being a top contributor to a mailing list—regularly answering questions that benefit many readers—he is publicly recognizing her knowledge-sharing work and its impact beyond her team. Because peer bonuses are employee driven, not management driven, they can have an important and powerful grassroots effect.

职级要求是自上而下引导文化的方式，但文化也会自下而上形成。在谷歌，同事奖金计划就是支持这种自下而上文化的一种做法。任何员工都可以向其他员工颁发同事奖金，以金钱奖励和正式认可，表彰对方超出通常要求的付出。[^11] 例如，Julia 经常在邮件列表上答疑，让许多读者受益，是其中的重要贡献者。Ravi 因此向她颁发同事奖金，就是在公开认可她的知识共享工作及其超出本团队的影响。由于这类奖励由员工而非管理层发起，能从基层产生重要而有力的作用。

Similar to peer bonuses are kudos: public acknowledgement of contributions (typically smaller in impact or effort than those meriting a peer bonus) that boost the visibility of peer-to-peer contributions.

类似的机制还有嘉奖（kudos），即公开表彰同事的贡献，让同事之间的帮助更容易被看见。与获得同事奖金的贡献相比，嘉奖所表彰的贡献通常影响较小，或所需投入较少。

When a Googler gives another Googler a peer bonus or kudos, they can choose to copy additional groups or individuals on the award email, boosting recognition of the peer’s work. It’s also common for the recipient’s manager to forward the award email to the team to celebrate one another’s achievements.

员工向同事颁发奖金或嘉奖时，可以在奖励邮件中抄送其他群组或个人，让同事的工作得到更多认可。获奖者的经理也常会把邮件转发给团队，庆祝成员的成就。

A system in which people can formally and easily recognize their peers is a powerful tool for encouraging peers to keep doing the awesome things they do. It’s not the bonus that matters: it’s the peer acknowledgement.

让人们能够方便、正式地认可同事的制度，是鼓励大家继续作出优秀贡献的有力工具。重要的不是奖金，而是同事的认可。

> [^11]: Peer bonuses include a cash award and a certificate as well as being a permanent part of a Googler’s award record in an internal tool called gThanks.     
    同事奖金包括现金奖励和证书，还会永久保存在内部工具 gThanks 的员工获奖记录中。

### Establishing Canonical Sources of Information 建立权威信息源

Canonical sources of information are centralized, company-wide corpuses of information that provide a way to standardize and propagate expert knowledge. They work best for information that is relevant to all engineers within the organization, which is otherwise prone to information islands. For example, a guide to setting up a basic developer workflow should be made canonical, whereas a guide for running a local Frobber instance is more relevant just to the engineers working on Frobber.

权威信息源是集中管理、面向全公司的信息库，用于统一和传播专家知识。它最适合承载与组织内所有工程师都相关的信息，否则这类信息很容易散落成孤岛。例如，搭建基本开发工作流的指南应成为统一的参考依据，而在本地运行 Frobber 实例的指南，主要与从事 Frobber 开发的工程师有关。

Establishing canonical sources of information requires higher investment than maintaining more localized information such as team documentation, but it also has broader benefits. Providing centralized references for the entire organization makes broadly required information easier and more predictable to find and counters problems with information fragmentation that can arise when multiple teams grappling with similar problems produce their own—often conflicting—guides.

建立权威信息源，比维护团队文档等局部信息需要更多投入，但受益范围也更广。为整个组织提供集中的参考资料，让大家更容易找到普遍需要的信息，也更清楚应该到哪里查找。多个团队处理类似问题时，可能各自编写指南，而且内容往往相互冲突；统一的参考资料有助于应对这种信息碎片化问题。

Because canonical information is highly visible and intended to provide a shared understanding at the organizational level, it’s important that the content is actively maintained and vetted by subject matter experts. The more complex a topic, the more critical it is that canonical content has explicit owners. Well-meaning readers might see that something is out of date but lack the expertise to make the significant structural changes needed to fix it, even if tooling makes it easy to suggest updates.

权威信息面向广泛受众，目的是在组织层面形成共同理解，因此必须由相关领域的专家主动维护和审核。主题越复杂，明确内容负责人就越重要。热心读者可能看出某些内容已经过时，却没有足够的专业知识去完成修正所需的大幅结构调整，即使工具让提交更新建议变得很容易。

Creating and maintaining centralized, canonical sources of information is expensive and time consuming, and not all content needs to be shared at an organizational level. When considering how much effort to invest in this resource, consider your audience. Who benefits from this information? You? Your team? Your product area? All engineers?

创建并维护集中、权威的信息源既费钱又费时，也不是所有内容都需要在整个组织内共享。决定投入多少精力时，应先考虑受众：谁会从这些信息中受益？你自己？你的团队？你所在的产品领域？还是所有工程师？

#### Developer guides  开发者指南

Google has a broad and deep set of official guidance for engineers, including style guides, official software engineering best practices,[^12] guides for code review[^13] and testing,[^14] and Tips of the Week (TotW).[^15]

谷歌为工程师提供了覆盖面广、内容深入的官方指南，包括风格指南、官方软件工程最佳实践[^12]、代码审查指南[^13]、测试指南[^14]，以及每周技巧（TotW）[^15]。

The corpus of information is so large that it’s impractical to expect engineers to read it all end to end, much less be able to absorb so much information at once. Instead, a human expert already familiar with a guideline can send a link to a fellow engineer, who then can read the reference and learn more. The expert saves time by not needing to personally explain a company-wide practice, and the learner now knows that there is a canonical source of trustworthy information that they can access whenever necessary. Such a process scales knowledge because it enables human experts to recognize and solve a specific information need by leveraging common, scalable resources.

资料数量太多，要求工程师从头到尾读完并不现实，更不用说一次吸收全部内容。更好的办法是，由熟悉某项准则的专家把链接发给同事，让对方自行阅读、深入了解。专家不用亲自解释全公司通用的做法，节省了时间；学习者也知道了一个可信赖的权威信息源，今后需要时可以随时查阅。这样，专家就能借助共享且可扩展的资源，识别并满足具体的信息需求，扩大知识传播的规模。

> [^12]:	Such as books about software engineering at Google.    
    例如介绍谷歌软件工程实践的书籍。
>
> [^13]:	See Chapter 9.    
    见第9章。
>
> [^14]:	See Chapter 11    
    见第11章。
>
> [^15]:	Available for multiple languages. Externally available for C++ at https://abseil.io/tips.    
    涵盖多种编程语言，其中 C++ 的内容已公开，可在[https://abseil.io/tips](https://abseil.io/tips)查阅。

#### go/links 短链接

go/links (sometimes referred to as goto/ links) are Google’s internal URL shortener.[^16] Most Google-internal references have at least one internal go/ link. For example, “go/ spanner” provides information about Spanner, “go/python” is Google’s Python developer guide. The content can live in any repository (g3doc, Google Drive, Google Sites, etc.), but having a go/ link that points to it provides a predictable, memorable way to access it. This yields some nice benefits:

- go/links are so short that it’s easy to share them in conversation (“You should check out go/frobber!”). This is much easier than having to go find a link and then send a message to all interested parties. Having a low-friction way to share references makes it more likely that that knowledge will be shared in the first place.
- go/links provide a permalink to the content, even if the underlying URL changes. When an owner moves content to a different repository (for example, moving content from a Google doc to g3doc), they can simply update the go/link’s target URL. The go/link itself remains unchanged.

go/links（有时也称 goto/ links）是谷歌内部的短链接服务。[^16] 大多数内部参考资料至少有一个 go/ 链接。例如，“go/spanner”提供 Spanner 的相关信息，“go/python”指向谷歌的 Python 开发者指南。内容可以放在任何存储位置，如 g3doc、Google Drive 或 Google Sites，但只要有 go/ 链接指向它，就有了一个容易猜到、便于记忆的访问入口。这带来了几个好处：

- go/links 很短，交流时随口就能分享，例如“你应该看看 go/frobber！”。这比先找到链接，再给所有感兴趣的人发消息方便得多。分享参考资料越省事，知识就越有可能被分享出去。
- 即使实际 URL 发生变化，go/links 仍能提供固定的内容入口。负责人把内容移到其他存储位置时，例如从 Google 文档迁到 g3doc，只需更新 go/link 的目标 URL，go/link 本身不用改变。

go/links are so ingrained into Google culture that a virtuous cycle has emerged: a Googler looking for information about Frobber will likely first check go/frobber. If the go/ link doesn’t point to the Frobber Developer Guide (as expected), the Googler will generally configure the link themselves. As a result, Googlers can usually guess the correct go/link on the first try.

go/links 已深深融入谷歌文化，并形成良性循环：员工想查找 Frobber 的信息时，很可能先试试 go/frobber。如果链接没有如预期那样指向 Frobber 开发者指南，通常就会自己配置它。因此，谷歌员工往往第一次就能猜中正确的 go/ 链接。

#### Codelabs 代码实验室

Google codelabs are guided, hands-on tutorials that teach engineers new concepts or processes by combining explanations, working best-practice example code, and code exercises.[^17] A canonical collection of codelabs for technologies broadly used across Google is available at go/codelab. These codelabs go through several rounds of formal review and testing before publication. Codelabs are an interesting halfway point between static documentation and instructor-led classes, and they share the best and worst features of each. Their hands-on nature makes them more engaging than traditional documentation, but engineers can still access them on demand and complete them on their own; but they are expensive to maintain and are not tailored to the learner’s specific needs.

谷歌的 codelab 是带有指导的动手实践教程，结合讲解、体现最佳实践且可运行的示例代码，以及编程练习，向工程师传授新概念或流程。[^17] go/codelab 汇集了谷歌广泛采用的技术所对应的权威教程。这些教程发布前会经过多轮正式审查和测试。Codelab 介于静态文档与教师授课之间，同时具有两者最突出的优点和缺点：动手实践比传统文档更能吸引学习者，工程师又可以按需获取、自行完成；但维护成本高，也无法针对个人需求量身定制。

> [^16]: go/ links are unrelated to the Go language.    
    go/ 链接与 Go 语言无关。
>
> [^17]: External codelabs are available at `https://codelabs.developers.google.com`.    
    对外开放的 codelab 可在 `https://codelabs.developers.google.com` 获取。

#### Static analysis 静态分析

Static analysis tools are a powerful way to share best practices that can be checked programmatically. Every programming language has its own particular static analysis tools, but they have the same general purpose: to alert code authors and reviewers to ways in which code can be improved to follow style and best practices. Some tools go one step further and offer to automatically apply those improvements to the code.

对于能够通过程序检查的最佳实践，静态分析工具是传播它们的有力手段。每种编程语言都有自己的静态分析工具，但总体目标相同：向代码作者和审查者指出改进方向，让代码符合风格规范与最佳实践。有些工具还能进一步自动修改代码，落实这些改进。

Setting up static analysis tools requires an upfront investment, but as soon as they are in place, they scale efficiently. When a check for a best practice is added to a tool, every engineer using that tool becomes aware of that best practice. This also frees up engineers to teach other things: the time and effort that would have gone into manually teaching the (now automated) best practice can instead be used to teach something else. Static analysis tools augment engineers’ knowledge. They enable an organization to apply more best practices and apply them more consistently than would otherwise be possible.

部署静态分析工具需要前期投入，但一旦投入使用，就能高效地扩大覆盖范围。工具新增某项最佳实践的检查后，每位使用它的工程师都能了解到这项实践。这也让工程师腾出时间传授其他知识：原本需要人工讲解的最佳实践，如今由工具自动提示，相应的时间和精力便可用在别处。静态分析工具扩充了工程师的知识，使组织能够采用更多最佳实践，并达到原本难以实现的一致性。

### Staying in the Loop 及时了解动态

Some information is critical to do one’s job, such as knowing how to do a typical development workflow. Other information, such as updates on popular productivity tools, is less critical but still useful. For this type of knowledge, the formality of the information sharing medium depends on the importance of the information being delivered. For example, users expect official documentation to be kept up to date, but typically have no such expectation for newsletter content, which therefore requires less maintenance and upkeep from the owner.

有些信息是完成工作所必需的，例如如何使用常见的开发工作流。另一些信息，例如常用生产力工具的更新，虽然没有那么关键，却仍有用处。共享这类知识时，媒介需要多正式，取决于信息的重要程度。例如，用户希望官方文档及时更新，却通常不会要求已发布的简报也不断更新，因此简报负责人的维护负担较轻。

#### Newsletters 简报

Google has a number of company-wide newsletters that are sent to all engineers, including EngNews (engineering news), Ownd (Privacy/Security news), and Google’s Greatest Hits (report of the most interesting outages of the quarter). These are a good way to communicate information that is of interest to engineers but isn’t mission critical. For this type of update, we’ve found that newsletters get better engagement when they are sent less frequently and contain more useful, interesting content. Otherwise, newsletters can be perceived as spam.

谷歌有多份发给全体工程师的公司级简报，包括 EngNews（工程新闻）、Ownd（隐私与安全新闻），以及 Google’s Greatest Hits（每季度最有意思的故障报告）。这些简报适合传递工程师感兴趣、但对完成任务并非至关重要的信息。我们发现，这类简报适当降低发送频率、增加有用且有趣的内容，更容易吸引读者。否则，就可能被当成垃圾邮件。

Even though most Google newsletters are sent via email, some are more creative in their distribution. Testing on the Toilet (testing tips) and Learning on the Loo (productivity tips) are single-page newsletters posted inside toilet stalls. This unique delivery medium helps the Testing on the Toilet and Learning on the Loo stand out from other newsletters, and all issues are archived online.

谷歌的大多数简报通过邮件发送，但也有更有创意的分发方式。Testing on the Toilet（如厕时学测试，介绍测试技巧）和 Learning on the Loo（如厕时学习，介绍生产力技巧）是贴在厕所隔间内的单页简报。这种独特的传播媒介让它们从其他简报中脱颖而出，所有往期内容也都在线存档。

#### Communities 社区

Googlers like to form cross-organizational communities around various topics to share knowledge. These open channels make it easier to learn from others outside your immediate circle and avoid information islands and duplication. Google Groups are especially popular: Google has thousands of internal groups with varying levels of formality. Some are dedicated to troubleshooting; others, like the Code Health group, are more for discussion and guidance. Internal Google+ is also popular among Googlers as a source of informal information because people will post interesting technical breakdowns or details about projects they are working on.

谷歌员工喜欢围绕不同主题建立跨组织的社区，分享知识。这些开放渠道让人更容易向自己日常圈子之外的人学习，避免信息孤岛和知识重复。Google Groups 尤其受欢迎：谷歌有数千个内部群组，正式程度各不相同。有些专门用于排查问题，有些则更侧重讨论和指导，例如代码健康小组。内部 Google+ 也是员工喜爱的非正式信息来源，人们会在上面发布有意思的技术剖析或自己正在参与的项目的详细情况。

## Readability: Standardized Mentorship Through Code Review 可读性认证：通过代码审查实现标准化指导

At Google, “readability” refers to more than just code readability; it is a standardized, Google-wide mentorship process for disseminating programming language best practices. Readability covers a wide breadth of expertise, including but not limited to language idioms, code structure, API design, appropriate use of common libraries, documentation, and test coverage.

在谷歌，Readability 不只是指代码是否易读，更是一套全公司统一的指导与认证流程，用来传播编程语言的最佳实践。它涵盖广泛的专业知识，包括但不限于语言惯用法、代码结构、API 设计、常用库的恰当使用、文档和测试覆盖率。

Readability started as a one-person effort. In Google’s early days, Craig Silverstein (employee ID #3) would sit down in person with every new hire and do a line-by-line “readability review” of their first major code commit. It was a nitpicky review that covered everything from ways the code could be improved to whitespace conventions. This gave Google’s codebase a uniform appearance but, more important, it taught best practices, highlighted what shared infrastructure was available, and showed new hires what it’s like to write code at Google.

Readability 最初由一个人推动。谷歌早期，Craig Silverstein（员工编号为3）会与每位新人坐在一起，对其第一次较大的代码提交逐行进行“Readability 审查”。审查细致到近乎挑剔，从代码如何改进到空白字符规范，无所不包。这让谷歌代码库的外观保持一致；更重要的是，它传授了最佳实践，指出有哪些共享基础设施可用，也让新人了解在谷歌写代码是怎么一回事。

Inevitably, Google’s hiring rate grew beyond what one person could keep up with. So many engineers found the process valuable that they volunteered their own time to scale the program. Today, around 20% of Google engineers are participating in the readability process at any given time, as either reviewers or code authors.

随着谷歌招聘规模扩大，一个人终究无法应付。许多工程师认为这一流程很有价值，于是自愿投入时间，扩大项目规模。如今，任一时刻大约都有20%的谷歌工程师以审查者或代码作者的身份参与 Readability 流程。

### What Is the Readability Process?  什么是可读性认证流程？

Code review is mandatory at Google. Every changelist (CL)[^18] requires readability approval, which indicates that someone who has readability certification for that language has approved the CL. Certified authors implicitly provide readability approval of their own CLs; otherwise, one or more qualified reviewers must explicitly give readability approval for the CL. This requirement was added after Google grew to a point where it was no longer possible to enforce that every engineer received code reviews that taught best practices to the desired rigor.

谷歌强制要求代码审查。每个变更列表（CL）[^18]都需要获得 Readability 批准，也就是由具备相应语言 Readability 资格的人认可该 CL。如果作者本人已有资格，其 CL 就隐含地满足这一项批准要求；否则，必须由一名或多名具备资格的审查者明确给予 Readability 批准。谷歌规模扩大后，已经无法确保每位工程师都能在代码审查中接受足够严格的最佳实践指导，因此增加了这项要求。

Within Google, having readability certification is commonly referred to as “having readability” for a language. Engineers with readability have demonstrated that they consistently write clear, idiomatic, and maintainable code that exemplifies Google’s best practices and coding style for a given language. They do this by submitting CLs through the readability process, during which a centralized group of readability reviewers review the CLs and give feedback on how much it demonstrates the various areas of mastery. As authors internalize the readability guidelines, they receive fewer and fewer comments on their CLs until they eventually graduate from the process and formally receive readability. Readability brings increased responsibility: engineers with readability are trusted to continue to apply their knowledge to their own code and to act as reviewers for other engineers’ code.

在谷歌内部，通过某种语言的 Readability 认证，通常称为“拥有该语言的 Readability 资格”。这意味着工程师已证明自己能够持续写出清晰、符合语言惯用法且可维护的代码，体现谷歌对该语言的最佳实践和编码风格。认证过程中，作者提交的 CL 由统一的 Readability 审查者团队审查，并获得关于各方面掌握程度的反馈。随着作者逐渐掌握这些准则，CL 收到的审查意见越来越少，最终完成流程，正式获得 Readability 资格。资格也意味着更多责任：工程师被信任会继续将所学用于自己的代码，并为其他工程师审查代码。

Around 1 to 2% of Google engineers are readability reviewers. All reviewers are volunteers, and anyone with readability is welcome to self-nominate to become a readability reviewer. Readability reviewers are held to the highest standards because they are expected not just to have deep language expertise, but also an aptitude for teaching through code review. They are expected to treat readability as first and foremost a mentoring and cooperative process, not a gatekeeping or adversarial one. Readability reviewers and CL authors alike are encouraged to have discussions during the review process. Reviewers provide relevant citations for their comments so that authors can learn about the rationales that went into the style guidelines (“Chesterson’s fence”). If the rationale for any given guideline is unclear, authors should ask for clarification (“ask questions”).

大约1%到2%的谷歌工程师担任 Readability 审查者。他们全是志愿者，任何已获得 Readability 资格的人都可以自荐。对这类审查者的要求极高：不仅要精通语言，还要善于通过代码审查传授知识。他们应把 Readability 首先视为指导与合作的过程，而不是单纯把关或彼此对抗。我们鼓励审查者与 CL 作者在审查中讨论。审查者会为意见提供相关出处，帮助作者理解风格准则背后的理由，也就是前面说的“切斯特顿的栅栏”。如果某条准则的理由不清楚，作者就应该要求解释，即主动“提问”。

> [^18]:  A changelist is a list of files that make up a change in a version control system. A changelist is synonymous with a changeset.    
    变更列表是版本控制系统中构成一次变更的文件清单，与变更集同义。

Readability is deliberately a human-driven process that aims to scale knowledge in a standardized yet personalized way. As a complementary blend of written and tribal knowledge, readability combines the advantages of written documentation, which can be accessed with citable references, with the advantages of expert human reviewers, who know which guidelines to cite. Canonical guidelines and language recommendations are comprehensively documented—which is good!—but the corpus of information is so large[^19] that it can be overwhelming, especially to newcomers.

Readability 刻意采用由人主导的流程，目的是以既标准化又个性化的方式扩大知识传播。它让书面知识与口头知识相互补充：文档提供了可供查阅、引用的依据，专业审查者则知道该引用哪些准则。权威准则和语言使用建议都有全面的文档记录，这当然是好事；但资料数量太多[^19]，也可能令人无从下手，尤其是新人。

> [^19]:  As of 2019, just the Google C++ style guide is 40 pages long. The secondary material making up the complete corpus of best practices is many times longer.    
    截至2019年，仅谷歌 C++ 风格指南就有40页。构成完整最佳实践资料集的配套材料，篇幅还要长数倍。

### Why Have This Process? 为什么需要这一流程？

Code is read far more than it is written, and this effect is magnified at Google’s scale and in our (very large) monorepo.[^20] Any engineer can look at and learn from the wealth of knowledge that is the code of other teams, and powerful tools like Kythe make it easy to find references throughout the entire codebase (see Chapter 17). An important feature of documented best practices (see Chapter 8) is that they provide consistent standards for all Google code to follow. Readability is both an enforcement and propagation mechanism for these standards.

代码被阅读的次数远多于被编写的次数，在谷歌这样的规模和庞大的单体代码仓库中，这一效应尤为明显。[^20] 任何工程师都可以查看其他团队的代码，从中学习丰富的知识；Kythe 等强大工具则让查找整个代码库中的引用变得容易（见第17章）。将最佳实践写成文档（见第8章），一个重要作用就是为谷歌的所有代码提供一致的标准。Readability 既是落实这些标准的机制，也是传播标准的机制。

One of the primary advantages of the readability program is that it exposes engineers to more than just their own team’s tribal knowledge. To earn readability in a given language, engineers must send CLs through a centralized set of readability reviewers who review code across the entire company. Centralizing the process makes a significant trade-off: the program is limited to scaling linearly rather than sublinearly with organization growth, but it makes it easier to enforce consistency, avoid islands, and avoid (often unintentional) drifting from established norms.

Readability 项目的一项主要优势，是让工程师接触到本团队口头知识之外的经验。要获得某种语言的 Readability 资格，工程师必须把 CL 交给统一的 Readability 审查者团队，他们面向全公司审查代码。集中化带来了一项重要取舍：项目所需投入只能随组织规模线性增长，无法做到次线性增长；但更容易保证一致性、避免信息孤岛，以及防止人们偏离既有规范，而这种偏离往往是无意的。

The value of codebase-wide consistency cannot be overstated: even with tens of thousands of engineers writing code over decades, it ensures that code in a given language will look similar across the corpus. This enables readers to focus on what the code does rather than being distracted by why it looks different than code that they’re used to. Large-scale change authors (see Chapter 22) can more easily make changes across the entire monorepo, crossing the boundaries of thousands of teams. People can change teams and be confident that the way that the new team uses a given language is not drastically different than their previous team.

整个代码库保持一致，其价值怎么强调都不为过。即使数万名工程师持续编写了几十年，同一种语言的代码在整个代码库中仍有相似的风格。读者就能专注于代码做了什么，不必分心琢磨它为何与自己熟悉的代码长得不同。负责大规模变更的人（见第22章）也更容易跨越成千上万个团队的边界，修改整个单体代码仓库。工程师调换团队时，也可以确信新团队使用某种语言的方式不会与原团队相差太大。

> [^20]:  For why Google uses a monorepo, see `https://cacm.acm.org/magazines/2016/7/204032-why-google-stores-billions-of-lines-of-code-in-a-single-repository/fulltext`. Note also that not all of Google’s code lives within the monorepo; readability as described here applies only to the monorepo because it is a notion of within- repository consistency.    
    关于谷歌采用单体代码仓库的原因，请参阅 https://cacm.acm.org/magazines/2016/7/204032-why-google-stores-billions-of-lines-of-code-in-a-single-repository/fulltext. 另请注意，谷歌并非所有代码都在这个仓库中；这里介绍的 Readability 只适用于该单体代码仓库，因为它关注的是仓库内部的一致性。

These benefits come with some costs: readability is a heavyweight process compared to other mediums like documentation and classes because it is mandatory and enforced by Google tooling (see Chapter 19). These costs are nontrivial and include the following:

- Increased friction for teams that do not have any team members with readability, because they need to find reviewers from outside their team to give readability approval on CLs.
- Potential for additional rounds of code review for authors who need readability review.
- Scaling disadvantages of being a human-driven process. Limited to scaling linearly to organization growth because it depends on human reviewers doing specialized code reviews.

这些收益也伴随着成本。与文档、课程等方式相比，Readability 是一个较重的流程，因为它是强制要求，并由谷歌的工具强制执行（见第19章）。这些成本不容小觑，包括：

- 如果团队中没有人具备 Readability 资格，就需要到团队外寻找审查者，为 CL 提供 Readability 批准，增加了协作成本。
- 需要接受 Readability 审查的作者，可能要经历额外几轮代码审查。
- 由人主导的流程不利于规模扩展。它依赖人工开展专门的代码审查，因此所需投入只能随组织规模线性增长。

The question, then, is whether the benefits outweigh the costs. There’s also the factor of time: the full effect of the benefits versus the costs are not on the same timescale. The program makes a deliberate trade-off of increased short-term code-review latency and upfront costs for the long-term payoffs of higher-quality code, repository-wide code consistency, and increased engineer expertise. The longer timescale of the benefits comes with the expectation that code is written with a potential lifetime of years, if not decades.[^21]

问题在于，这些收益是否超过成本。还要考虑时间：成本与收益并不是在同样长的时间内充分显现的。这一项目有意接受短期内更长的代码审查等待时间和更高的前期成本，以换取代码质量提升、仓库内代码一致，以及工程师专业能力提高等长期回报。这种长期收益建立在一个预期之上：代码可能使用数年，甚至数十年。[^21]

As with most—or perhaps all—engineering processes, there’s always room for improvement. Some of the costs can be mitigated with tooling. A number of readability comments address issues that could be detected statically and commented on automatically by static analysis tooling. As we continue to invest in static analysis, readability reviewers can increasingly focus on higher-order areas, like whether a particular block of code is understandable by outside readers who are not intimately familiar with the codebase instead of automatable detections like whether a line has trailing whitespace.

与大多数工程流程，或许是所有工程流程一样，Readability 总有改进空间。一些成本可以借助工具降低。不少 Readability 审查意见所指出的问题，其实能够由静态分析工具自动检测并提示。随着我们持续投入静态分析，审查者就可以把更多精力放在较高层次的问题上，例如某段代码能否让不熟悉代码库的外部读者理解，而不是检查行尾是否有多余空白等可自动化的细节。

But aspirations aren’t enough. Readability is a controversial program: some engineers complain that it’s an unnecessary bureaucratic hurdle and a poor use of engineer time. Are readability’s trade-offs worthwhile? For the answer, we turned to our trusty Engineering Productivity Research (EPR) team.

但光有愿望还不够。Readability 一直有争议：一些工程师认为，它是多余的官僚程序，浪费了工程师的时间。这些取舍究竟是否值得？为寻找答案，我们请可信赖的工程生产力研究（EPR）团队进行了研究。

The EPR team performed in-depth studies of readability, including but not limited to whether people were hindered by the process, learned anything, or changed their behavior after graduating. These studies showed that readability has a net positive impact on engineering velocity. CLs by authors with readability take statistically significantly less time to review and submit than CLs by authors who do not have readability.[^22] Self-reported engineer satisfaction with their code quality—lacking more objective measures for code quality—is higher among engineers who have readability versus those who do not. A significant majority of engineers who complete the program report satisfaction with the process and find it worthwhile. They report learning from reviewers and changing their own behavior to avoid readability issues when writing and reviewing code.

EPR 团队深入研究了 Readability，包括流程是否妨碍工作、参与者是否学到知识，以及完成认证后是否改变了行为等。研究表明，Readability 对工程开发速度总体有正面作用。与尚未取得资格的作者相比，已有 Readability 资格的作者，其 CL 的审查和提交耗时显著更短，这一差异具有统计显著性。[^22] 在缺乏更客观的代码质量指标的情况下，就工程师自报的代码质量满意度而言，有资格者也高于没有资格者。完成项目的工程师中，大多数对流程满意，认为值得参与。他们表示，自己从审查者那里学到了知识，并改变了写代码和审查代码的方式，以避免再出现 Readability 审查所关注的问题。

Google has a very strong culture of code review, and readability is a natural extension of that culture. Readability grew from the passion of a single engineer to a formal program of human experts mentoring all Google engineers. It evolved and changed with Google’s growth, and it will continue to evolve as Google’s needs change.

谷歌有浓厚的代码审查文化，Readability 是这种文化的自然延伸。它从一位工程师的热情出发，发展为由专家指导全体谷歌工程师的正式项目。它随谷歌的成长而演变，也将继续随谷歌的需求变化而调整。

> [^21]:  For this reason, code that is known to have a short time span is exempt from readability requirements. Examples include the experimental/ directory (explicitly designated for experimental code and cannot push to production) and the Area 120 program, a workshop for Google’s experimental products.     
    因此，明确只会短期使用的代码可以豁免 Readability 要求。例如 experimental/ 目录中的代码（明确用于实验，不能发布到生产环境），以及 Area 120 项目中的代码；后者是谷歌实验性产品的孵化项目。
>
> [^22]:  This includes controlling for a variety of factors, including tenure at Google and the fact that CLs for authors who do not have readability typically need additional rounds of review compared to authors who already have readability.    
    研究控制了多种因素，包括在谷歌的任职时间，以及尚未取得 Readability 资格的作者所提交的 CL，通常比已有资格的作者需要更多轮审查这一事实。

## Conclusion 结论

Knowledge is in some ways the most important (though intangible) capital of a software engineering organization, and sharing of that knowledge is crucial for making an organization resilient and redundant in the face of change. A culture that promotes open and honest knowledge sharing distributes that knowledge efficiently across the organization and allows that organization to scale over time. In most cases, investments into easier knowledge sharing reap manyfold dividends over the life of a company.

从某些方面看，知识是软件工程组织最重要的资本，尽管它是无形的。共享知识对于组织在变化面前保持韧性、具备必要的冗余至关重要。鼓励开放、坦诚共享知识的文化，能够让知识高效地传播到整个组织，并支持组织持续扩大规模。大多数情况下，为降低知识共享的难度而作出的投入，会在公司的生命周期内带来数倍回报。

## TL;DRs  内容提要

- Psychological safety is the foundation for fostering a knowledge-sharing environment.
- Start small: ask questions and write things down.
- Make it easy for people to get the help they need from both human experts and documented references.
- At a systemic level, encourage and reward those who take time to teach and broaden their expertise beyond just themselves, their team, or their organization.
- There is no silver bullet: empowering a knowledge-sharing culture requires a combination of multiple strategies, and the exact mix that works best for your organization will likely change over time.

- 心理安全感是营造知识共享环境的基础。
- 从小事做起：提问，并把所学记录下来。
- 让人们能够方便地从专家和文档资料中获得所需帮助。
- 从制度上鼓励和奖励那些愿意花时间传授知识，并将专业知识传播到个人、团队或组织之外的人。
- 没有万能的办法：培育知识共享文化需要多种策略配合，最适合组织的组合也可能随时间变化。
