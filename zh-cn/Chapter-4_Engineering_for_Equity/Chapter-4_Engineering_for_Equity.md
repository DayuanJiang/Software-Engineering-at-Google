
**CHAPTER 4**

# Engineering for Equity

# 第四章 面向公平的工程实践

**Written by Demma Rodriguez**

**Edited by Riona MacNamara**

In earlier chapters, we’ve explored the contrast between programming as the production of code that addresses the problem of the moment, and software engineering as the broader application of code, tools, policies, and processes to a dynamic and ambiguous problem that can span decades or even lifetimes. In this chapter, we’ll discuss the unique responsibilities of an engineer when designing products for a broad base of users. Further, we evaluate how an organization, by embracing diversity, can design systems that work for everyone, and avoid perpetuating harm against our users.

前几章探讨了编程与软件工程的区别：编程是编写代码，解决眼前的问题；软件工程则更广泛地运用代码、工具、策略和流程，应对不断变化、尚不明确，而且可能持续几十年甚至一生的问题。本章将讨论工程师为广泛的用户群体设计产品时所承担的独特责任。我们还将探讨，组织如何接纳多样性，设计出适合所有人的系统，避免让用户持续受到伤害。

As new as the field of software engineering is, we’re newer still at understanding the impact it has on underrepresented people and diverse societies. We did not write this chapter because we know all the answers. We do not. In fact, understanding how to engineer products that empower and respect all our users is still something Google is learning to do. We have had many public failures in protecting our most vulnerable users, and so we are writing this chapter because the path forward to more equitable products begins with evaluating our own failures and encouraging growth.

软件工程本身还是一个年轻的领域，而我们对它如何影响代表性不足的群体和多元社会的认识，则更加初步。我们写这一章，并不是因为掌握了所有答案。我们并没有。事实上，如何通过工程实践打造能够增强所有用户能力、尊重所有用户的产品，仍是谷歌正在学习的课题。在保护最弱势的用户方面，我们有过许多公开的失败。正因如此，我们才写下这一章：要让产品更加公平，首先就要审视自己的失败，鼓励成长。

We are also writing this chapter because of the increasing imbalance of power between those who make development decisions that impact the world and those who simply must accept and live with those decisions that sometimes disadvantage already marginalized communities globally. It is important to share and reflect on what we’ve learned so far with the next generation of software engineers. It is even more important that we help influence the next generation of engineers to be better than we are today.

写这一章还有一个原因：一方作出影响世界的开发决策，另一方却只能接受这些决策并承受后果，两者之间的权力越来越不平衡。这些决策有时会让世界各地本已边缘化的群体处于不利地位。我们有必要与下一代软件工程师分享并共同反思迄今学到的经验。更重要的是，我们要帮助下一代工程师做得比今天的我们更好。

Just picking up this book means that you likely aspire to be an exceptional engineer. You want to solve problems. You aspire to build products that drive positive outcomes for the broadest base of people, including people who are the most difficult to reach. To do this, you will need to consider how the tools you build will be leveraged to change the trajectory of humanity, hopefully for the better.

拿起这本书，说明你很可能希望成为一名卓越的工程师。你想解决问题，想打造能够为尽可能广泛的人群带来积极成果的产品，包括那些最难触及的人。为此，你需要考虑：你开发的工具会被怎样使用，又将如何改变人类的发展轨迹，希望这种改变能让世界变得更好。

## Bias Is the Default 偏见是默认状态

When engineers do not focus on users of different nationalities, ethnicities, races, genders, ages, socioeconomic statuses, abilities, and belief systems, even the most talented staff will inadvertently fail their users. Such failures are often unintentional; all people have certain biases, and social scientists have recognized over the past several decades that most people exhibit unconscious bias, enforcing and promulgating existing stereotypes. Unconscious bias is insidious and often more difficult to mitigate than intentional acts of exclusion. Even when we want to do the right thing, we might not recognize our own biases. By the same token, our organizations must also recognize that such bias exists and work to address it in their workforces, product development, and user outreach.

如果工程师不关注不同国籍、民族、种族、性别、年龄、社会经济地位、能力和信仰体系的用户，即使才华出众，也会在无意中辜负用户。这类失误往往并非出于有意：每个人都有一定的偏见。过去几十年里，社会科学家已经认识到，大多数人都会表现出无意识偏见，强化并传播已有的刻板印象。无意识偏见隐蔽而有害，往往比有意排斥更难消除。即使想做正确的事，我们也可能察觉不到自己的偏见。同样，组织也必须承认这些偏见的存在，并在员工队伍、产品开发和用户联络工作中着手解决。

Because of bias, Google has at times failed to represent users equitably within their products, with launches over the past several years that did not focus enough on underrepresented groups. Many users attribute our lack of awareness in these cases to the fact that our engineering population is mostly male, mostly White or Asian, and certainly not representative of all the communities that use our products. The lack of representation of such users in our workforce[^1] means that we often do not have the requisite diversity to understand how the use of our products can affect underrepresented or vulnerable users.

由于偏见，谷歌有时未能在产品中公平地体现各类用户的需求，过去几年推出的一些产品对代表性不足的群体关注不够。许多用户认为，我们之所以缺乏这方面的意识，是因为工程师大多是男性，大多是白人或亚裔，显然不能代表使用我们产品的所有群体。这些用户在员工队伍中的代表性不足，意味着我们往往缺少必要的多样性，难以理解产品的使用会如何影响代表性不足或处于弱势的用户。

------

#### Case Study: Google Misses the Mark on Racial Inclusion  案例研究：谷歌在种族包容方面的失误

In 2015, software engineer Jacky Alciné pointed out[^2] that the image recognition algorithms in Google Photos were classifying his black friends as “gorillas.” Google was slow to respond to these mistakes and incomplete in addressing them.

2015年，软件工程师 Jacky Alciné 指出，谷歌照片的图像识别算法把他的黑人朋友归类为“大猩猩”。谷歌对这些错误反应迟缓，处理也不彻底。

What caused such a monumental failure? Several things:
- Image recognition algorithms depend on being supplied a “proper” (often meaning “complete”) dataset. The photo data fed into Google’s image recognition algorithm was clearly incomplete. In short, the data did not represent the population.
- Google itself (and the tech industry in general) did not (and does not) have much black representation,[^3] and that affects decisions subjective in the design of such algorithms and the collection of such datasets. The unconscious bias of the organization itself likely led to a more representative product being left on the table.
- Google’s target market for image recognition did not adequately include such underrepresented groups. Google’s tests did not catch these mistakes; as a result, our users did, which both embarrassed Google and harmed our users.

如此严重的失误是怎样发生的？原因有几个：
- 图像识别算法依赖“适当的”数据集，这通常意味着数据集需要“完整”。输入谷歌图像识别算法的照片数据显然不完整。简而言之，这些数据未能代表整个人群。
- 谷歌本身以及整个科技行业，过去和现在都缺乏足够的黑人代表性，这会影响算法设计和数据集收集中的主观决策。组织自身的无意识偏见，很可能让我们错失了打造更具代表性产品的机会。
- 谷歌为图像识别设定的目标市场，没有充分涵盖这些代表性不足的群体。测试没能发现错误，最终由用户发现了问题。这既让谷歌难堪，也伤害了用户。

As late as 2018, Google still had not adequately addressed the underlying problem.[^4]

直到2018年，谷歌仍未妥善解决这一根本问题。

------

In this example, our product was inadequately designed and executed, failing to properly consider all racial groups, and as a result, failed our users and caused Google bad press. Other technology suffers from similar failures: autocomplete can return offensive or racist results. Google’s Ad system could be manipulated to show racist or offensive ads. YouTube might not catch hate speech, though it is technically outlawed on that platform.

在这个案例中，产品的设计和实现都存在不足，没有充分考虑所有种族群体，因而辜负了用户，也让谷歌遭到负面报道。其他技术也有类似的失误：自动补全可能返回冒犯性或种族主义内容；谷歌的广告系统可能被人操纵，展示种族主义或冒犯性广告；YouTube 可能漏掉仇恨言论，尽管平台规定禁止这类内容。

In all of these cases, the technology itself is not really to blame. Autocomplete, for example, was not designed to target users or to discriminate. But it was also not resilient enough in its design to exclude discriminatory language that is considered hate speech. As a result, the algorithm returned results that caused harm to our users. The harm to Google itself should also be obvious: reduced user trust and engagement with the company. For example, Black, Latinx, and Jewish applicants could lose faith in Google as a platform or even as an inclusive environment itself, therefore undermining Google’s goal of improving representation in hiring.

这些问题并不能真正归咎于技术本身。例如，自动补全并不是为针对或歧视用户而设计的，但其设计也不够稳健，未能排除那些被视为仇恨言论的歧视性语言。结果，算法返回的内容伤害了用户。对谷歌自身的损害也应当不难看出：用户对公司的信任和参与度下降。例如，黑人、拉丁裔（Latinx）和犹太裔求职者可能对谷歌这个平台失去信任，甚至不再相信谷歌本身是一个包容的工作环境。这会妨碍谷歌通过招聘提升员工代表性的目标。

How could this happen? After all, Google hires technologists with impeccable education and/or professional experience—exceptional programmers who write the best code and test their work. “Build for everyone” is a Google brand statement, but the truth is that we still have a long way to go before we can claim that we do. One way to address these problems is to help the software engineering organization itself look like the populations for whom we build products.

为什么会这样？毕竟，谷歌聘用的技术人才拥有出色的教育背景、专业经验，或兼具两者。他们是卓越的程序员，会编写最好的代码，也会测试自己的工作成果。“为所有人打造产品”是谷歌的品牌宣言，但要真正做到这一点，我们还有很长的路要走。解决这些问题的方法之一，就是让软件工程组织的人员构成，更能代表我们所服务的用户群体。

> [^1]:    Google’s 2019 Diversity Report.
> 1 谷歌的2019年多样性报告。
>
> [^2]:    @jackyalcine. 2015. “Google Photos, Y’all Fucked up. My Friend’s Not a Gorilla.” Twitter, June 29, 2015.https://twitter.com/jackyalcine/status/615329515909156865.
> 2 @jackyalcine. 2015. “谷歌照片，你们他妈的搞砸了。我的朋友不是大猩猩。”Twitter，2015年6月29日。https://twitter.com/jackyalcine/status/615329515909156865
>
> [^3]:    Many reports in 2018–2019 pointed to a lack of diversity across tech. Some notables include the National Center for Women & Information Technology, and Diversity in Tech./
> 3  2018-2019年的许多报告指出，整个科技行业都缺乏多样性。其中较知名的报告来自国家女性与信息技术中心和 Diversity in Tech。
>
> [^4]:    Tom Simonite, “When It Comes to Gorillas, Google Photos Remains Blind,” Wired, January 11, 2018.
> 4    Tom Simonite，《谷歌照片仍然识别不了大猩猩》，《连线》，2018年1月11日。

## Understanding the Need for Diversity 了解多样性的必要性

At Google, we believe that being an exceptional engineer requires that you also focus on bringing diverse perspectives into product design and implementation. It also means that Googlers responsible for hiring or interviewing other engineers must contribute to building a more representative workforce. For example, if you interview other engineers for positions at your company, it is important to learn how biased outcomes happen in hiring. There are significant prerequisites for understanding how to anticipate harm and prevent it. To get to the point where we can build for everyone, we first must understand our representative populations. We need to encourage engineers to have a wider scope of educational training.

在谷歌，我们认为，卓越的工程师还需要注重将多元视角融入产品设计与实现。这也意味着，负责招聘或面试其他工程师的谷歌员工，必须为建设更具代表性的员工队伍作出贡献。例如，如果你负责为公司的工程师岗位面试候选人，就需要了解招聘中带有偏见的结果是如何产生的。要懂得如何预见并防止伤害，需要先具备一些重要的基础。要为所有人打造产品，我们首先必须了解需要代表的人群，并鼓励工程师接受范围更广的教育和培训。

The first order of business is to disrupt the notion that as a person with a computer science degree and/or work experience, you have all the skills you need to become an exceptional engineer. A computer science degree is often a necessary foundation. However, the degree alone (even when coupled with work experience) will not make you an engineer. It is also important to disrupt the idea that only people with computer science degrees can design and build products. Today, [most programmers do have a computer science degree](https://oreil.ly/2Bu0H); they are successful at building code, establishing theories of change, and applying methodologies for problem solving. However, as the aforementioned examples demonstrate, *this approach is insufficient for inclusive and* *equitable engineering*.

首先要打破一种观念：拥有计算机科学学位、工作经验，或兼具两者，就掌握了成为卓越工程师所需的全部技能。计算机科学学位往往是必要的基础，但仅有学位，即使再加上工作经验，也不足以让你成为一名工程师。同样需要打破的，还有“只有计算机科学专业毕业的人才能设计和打造产品”这一观念。如今，大多数程序员确实拥有计算机科学学位；他们擅长编写代码、建立变革理论，并运用各种方法解决问题。然而，前面的例子表明，*这些还不足以实现兼顾包容与公平的工程实践*。

Engineers should begin by focusing all work within the framing of the complete ecosystem they seek to influence. At minimum, they need to understand the population demographics of their users. Engineers should focus on people who are different than themselves, especially people who might attempt to use their products to cause harm. The most difficult users to consider are those who are disenfranchised by the processes and the environment in which they access technology. To address this challenge, engineering teams need to be representative of their existing and future users. In the absence of diverse representation on engineering teams, individual engineers need to learn how to build for all users.

工程师首先应把所有工作放到自己希望影响的整个生态系统中考量。至少，要了解用户的人口统计特征。工程师应关注与自己不同的人，尤其是那些可能试图利用产品造成伤害的人。最难兼顾的用户，是那些在获取技术时，因相关流程和环境而被剥夺权益的人。要应对这一挑战，工程团队的人员构成就需要能够代表现有和未来的用户。如果团队缺乏多元代表性，每位工程师就需要学习如何为所有用户打造产品。

## Building Multicultural Capacity 培养多元文化能力

One mark of an exceptional engineer is the ability to understand how products can advantage and disadvantage different groups of human beings. Engineers are expected to have technical aptitude, but they should also have the *discernment* to know when to build something and when not to. Discernment includes building the capacity to identify and reject features or products that drive adverse outcomes. This is a lofty and difficult goal, because there is an enormous amount of individualism that goes into being a high-performing engineer. Yet to succeed, we must extend our focus beyond our own communities to the next billion users or to current users who might be disenfranchised or left behind by our products.

卓越工程师的一个标志，是能理解产品会如何让不同人群受益或受损。工程师固然要有技术能力，也应有*判断力*，知道什么时候该开发某样东西，什么时候不该开发。这包括识别并拒绝会带来不良后果的功能或产品的能力。这是一个远大而艰难的目标，因为成为高绩效工程师的过程带有浓厚的个人主义色彩。然而，要取得成功，我们必须把目光投向自身群体之外，关注未来的十亿用户，或那些可能因我们的产品而被剥夺权益、被落下的现有用户。

Over time, you might build tools that billions of people use daily—tools that influence how people think about the value of human lives, tools that monitor human activity, and tools that capture and persist sensitive data, such as images of their children and loved ones, as well as other types of sensitive data. As an engineer, you might wield more power than you realize: the power to literally change society. It’s critical that on your journey to becoming an exceptional engineer, you understand the innate responsibility needed to exercise power without causing harm. The first step is to recognize the default state of your bias caused by many societal and educational factors. After you recognize this, you’ll be able to consider the often-forgotten use cases or users who can benefit or be harmed by the products you build.

随着时间推移，你可能会开发出数十亿人每天使用的工具：影响人们如何看待生命价值的工具，监测人类活动的工具，以及采集并持久保存敏感数据的工具，例如用户的孩子和亲人的照片，以及其他类型的敏感数据。身为工程师，你掌握的权力可能比自己意识到的更大，甚至足以真正改变社会。在成为卓越工程师的过程中，理解行使权力时随之而来的责任，避免造成伤害，至关重要。第一步是承认，许多社会和教育因素使偏见成为你默认状态的一部分。认识到这一点，才能考虑那些常被忽略的用例，以及可能因你的产品而受益或受害的用户。

The industry continues to move forward, building new use cases for artificial intelligence (AI) and machine learning at an ever-increasing speed. To stay competitive, we drive toward scale and efficacy in building a high-talent engineering and technology workforce. Yet we need to pause and consider the fact that today, some people have the ability to design the future of technology and others do not. We need to understand whether the software systems we build will eliminate the potential for entire populations to experience shared prosperity and provide equal access to technology.

业界不断向前发展，为人工智能（AI）和机器学习开拓应用场景的速度也越来越快。为保持竞争力，我们在建设高水平工程与技术人才队伍时，追求规模和成效。然而，我们也需要停下来想一想：今天，有些人能够设计技术的未来，另一些人却没有这样的机会。我们需要了解所构建的软件系统，是否会使整个群体失去共享繁荣的可能性，并提供平等获取技术的机会。〔译注：原文末句的逻辑关系不够明确，暂保留其表述。〕

Historically, companies faced with a decision between completing a strategic objective that drives market dominance and revenue and one that potentially slows momentum toward that goal have opted for speed and shareholder value. This tendency is exacerbated by the fact that many companies value individual performance and excellence, yet often fail to effectively drive accountability on product equity across all areas. Focusing on underrepresented users is a clear opportunity to promote equity. To continue to be competitive in the technology sector, we need to learn to engineer for global equity.

过去，企业在两种选择之间作取舍时，选择的是速度和股东价值：一是完成有助于主导市场、增加收入的战略目标，二是采取可能放慢这一进程的行动。许多公司看重个人绩效和卓越表现，却往往未能在各个领域有效落实产品公平的责任，这进一步加剧了上述倾向。关注代表性不足的用户，显然是促进公平的机会。要在科技行业保持竞争力，我们就需要学习如何通过工程实践促进全球公平。

Today, we worry when companies design technology to scan, capture, and identify people walking down the street. We worry about privacy and how governments might use this information now and in the future. Yet most technologists do not have the requisite perspective of underrepresented groups to understand the impact of racial variance in facial recognition or to understand how applying AI can drive harmful and inaccurate results.

如今，企业开发技术来扫描街上行人、采集影像并识别身份时，我们会感到担忧。我们担心隐私，也担心政府现在和未来可能如何使用这些信息。然而，大多数技术人员缺少代表性不足群体的必要视角，因而难以理解种族差异如何影响人脸识别，也难以理解应用人工智能为何会产生有害且不准确的结果。

Currently, AI-driven facial-recognition software continues to disadvantage people of color or ethnic minorities. Our research is not comprehensive enough and does not include a wide enough range of different skin tones. We cannot expect the output to be valid if both the training data and those creating the software represent only a small subsection of people. In those cases, we should be willing to delay development in favor of trying to get more complete and accurate data, and a more comprehensive and inclusive product.

目前，人工智能驱动的人脸识别软件仍然让有色人种或少数族裔处于不利地位。我们的研究不够全面，涵盖的肤色范围也不够广。如果训练数据和软件开发者都只代表一小部分人，就不能指望输出结果有效。遇到这种情况，我们应当愿意推迟开发，努力获取更完整、更准确的数据，打造更全面、更具包容性的产品。

Data science itself is challenging for humans to evaluate, however. Even when we do have representation, a training set can still be biased and produce invalid results. A study completed in 2016 found that more than 117 million American adults are in a law enforcement facial recognition database.[^5] Due to the disproportionate policing of Black communities and disparate outcomes in arrests, there could be racially biased error rates in utilizing such a database in facial recognition. Although the software is being developed and deployed at ever-increasing rates, the independent testing is not. To correct for this egregious misstep, we need to have the integrity to slow down and ensure that our inputs contain as little bias as possible. Google now offers statistical training within the context of AI to help ensure that datasets are not intrinsically biased.

不过，数据科学本身也很难由人来评估。即使相关群体已有代表，训练集仍可能带有偏差，产生无效结果。2016年完成的一项研究发现，超过1.17亿名美国成年人被收录在执法部门的人脸识别数据库中。黑人社区承受了不成比例的警务执法，逮捕结果也存在群体差异，因此，利用这类数据库进行人脸识别时，错误率可能带有种族偏差。软件开发和部署的速度不断加快，独立测试却没有跟上。要纠正这一严重失误，我们需要秉持正直，放慢脚步，确保输入中的偏差尽可能少。谷歌现在提供人工智能领域的统计学培训，以帮助确保数据集本身不带有偏差。

Therefore, shifting the focus of your industry experience to include more comprehensive, multicultural, race and gender studies education is not only your responsibility, but also the responsibility of your employer. Technology companies must ensure that their employees are continually receiving professional development and that this development is comprehensive and multidisciplinary. The requirement is not that one individual take it upon themselves to learn about other cultures or other demographics alone. Change requires that each of us, individually or as leaders of teams, invest in continuous professional development that builds not just our software development and leadership skills, but also our capacity to understand the diverse experiences throughout humanity.

因此，拓宽行业经验的关注范围，将更全面的多元文化、种族和性别研究教育纳入其中，既是你的责任，也是雇主的责任。科技公司必须确保员工持续接受全面、跨学科的专业培养。这并不是要求某个人独自承担了解其他文化或人口群体的任务。要实现改变，我们每个人，无论作为个人还是团队负责人，都需要持续投入职业发展，不仅提升软件开发和领导能力，也提升理解人类多样化经历的能力。

> [^5]:    Stephen Gaines and Sara Williams. “The Perpetual Lineup: Unregulated Police Face Recognition in America.”
>
> 5    斯蒂芬·盖恩斯和莎拉·威廉姆斯。《永不结束的列队辨认：美国不受监管的警方人脸识别》。
乔治敦法律学院隐私与技术中心，2016年10月18日。

## Making Diversity Actionable 将多样性付诸行动

Systemic equity and fairness are attainable if we are willing to accept that we are all accountable for the systemic discrimination we see in the technology sector. We are accountable for the failures in the system. Deferring or abstracting away personal accountability is ineffective, and depending on your role, it could be irresponsible. It is also irresponsible to fully attribute dynamics at your specific company or within your team to the larger societal issues that contribute to inequity. A favorite line among diversity proponents and detractors alike goes something like this: “We are working hard to fix (insert systemic discrimination topic), but accountability is hard. How do we combat (insert hundreds of years) of historical discrimination?” This line of inquiry is a detour to a more philosophical or academic conversation and away from focused efforts to improve work conditions or outcomes. Part of building multicultural capacity requires a more comprehensive understanding of how systems of inequality in society impact the workplace, especially in the technology sector.

只要愿意承认，科技行业中出现的系统性歧视是我们每个人的责任，就有可能实现系统性的公平与公正。我们必须为体系中的失败负责。推诿个人责任，或将其抽象化，都无济于事；根据你所担任的角色，这样做还可能是不负责任的。同样，把自己公司或团队中的状况，完全归因于造成不公平的宏观社会问题，也是不负责任的。无论支持还是反对多样性，人们都常说这样一番话：“我们正努力解决（填入某种系统性歧视问题），但落实责任很难。我们该如何对抗延续了（填入几百年）的历史歧视？”这种追问会把讨论引向哲学或学术层面，偏离改善工作条件或结果的具体努力。培养多元文化能力，需要更全面地理解社会中的不平等体系如何影响职场，尤其是科技行业。

If you are an engineering manager working on hiring more people from underrepresented groups, deferring to the historical impact of discrimination in the world is a useful academic exercise. However, it is critical to move beyond the academic conversation to a focus on quantifiable and actionable steps that you can take to drive equity and fairness. For example, as a hiring software engineer manager, you’re accountable for ensuring that your candidate slates are balanced. Are there women or other underrepresented groups in the pool of candidates’ reviews? After you hire someone, what opportunities for growth have you provided, and is the distribution of opportunities equitable? Every technology lead or software engineering manager has the means to augment equity on their teams. It is important that we acknowledge that, although there are significant systemic challenges, we are all part of the system. It is our problem to fix.

如果你是一名工程经理，希望招到更多来自代表性不足群体的员工，那么讨论歧视在世界各地留下的历史影响，是一项有益的学术活动。但关键是要超越学术讨论，着眼于自己能够采取的、可量化且可执行的步骤，推动公平与公正。例如，作为负责招聘的软件工程经理，你有责任确保候选人名单的构成均衡。进入评估范围的候选人中，是否有女性或其他代表性不足群体的成员？招人之后，你提供了哪些成长机会？这些机会分配得是否公平？每位技术负责人或软件工程经理都有办法提升团队的公平性。我们必须承认：尽管系统性挑战严峻，但我们都是这个体系的一部分，解决问题也是我们的责任。

## Reject Singular Approaches 摒弃单一方法

We cannot perpetuate solutions that present a single philosophy or methodology for fixing inequity in the technology sector. Our problems are complex and multifactorial. Therefore, we must disrupt singular approaches to advancing representation in the workplace, even if they are promoted by people we admire or who have institutional power.

我们不能继续沿用仅凭一种理念或方法就想解决科技行业不公平问题的方案。这些问题很复杂，涉及多种因素。因此，我们必须打破依靠单一方法提升职场代表性的做法，即使倡导这种做法的是我们敬佩的人，或在机构中掌握权力的人。

One singular narrative held dear in the technology industry is that lack of representation in the workforce can be addressed solely by fixing the hiring pipelines. Yes, that is a fundamental step, but that is not the immediate issue we need to fix. We need to recognize systemic inequity in progression and retention while simultaneously focusing on more representative hiring and educational disparities across lines of race, gender, and socioeconomic and immigration status, for example.

科技行业推崇的一种单一解释是，只要改善招聘渠道，就能解决员工队伍代表性不足的问题。这确实是基础性的一步，但并不是我们眼前需要解决的问题。我们需要认识到晋升和留任中的系统性不公平，同时关注招聘中的代表性，以及种族、性别、社会经济地位、移民身份等方面的教育差距。

In the technology industry, many people from underrepresented groups are passed over daily for opportunities and advancement. Attrition among Black+ Google employees outpaces attrition from all other groups and confounds progress on representation goals. If we want to drive change and increase representation, we need to evaluate whether we’re creating an ecosystem in which all aspiring engineers and other technology professionals can thrive.

在科技行业，每天都有许多来自代表性不足群体的人，在机会分配和晋升中被忽视。谷歌 Black+ 员工的流失率高于所有其他群体，阻碍了员工代表性目标的实现。如果想推动改变、提升代表性，我们就需要评估：自己是否正在营造一个让所有有抱负的工程师及其他技术专业人员都能成长发展的生态系统。

Fully understanding an entire problem space is critical to determining how to fix it. This holds true for everything from a critical data migration to the hiring of a representative workforce. For example, if you are an engineering manager who wants to hire more women, don’t just focus on building a pipeline. Focus on other aspects of the hiring, retention, and progression ecosystem and how inclusive it might or might not be to women. Consider whether your recruiters are demonstrating the ability to identify strong candidates who are women as well as men. If you manage a diverse engineering team, focus on psychological safety and invest in increasing multicultural capacity on the team so that new team members feel welcome.

要确定如何解决问题，充分了解整个问题空间至关重要。从关键的数据迁移，到招聘能够代表不同群体的员工，道理都一样。例如，如果你是工程经理，希望招到更多女性，就不要只关注招聘渠道建设。还要考察招聘、留任和晋升生态系统的其他方面，看看它们对女性是否具有包容性。招聘人员是否有能力在女性和男性中同样识别出优秀候选人？如果你管理着一支多元化工程团队，就应关注心理安全感，投入资源培养团队的多元文化能力，让新成员感到受欢迎。

A common methodology today is to build for the majority use case first, leaving improvements and features that address edge cases for later. But this approach is flawed; it gives users who are already advantaged in access to technology a head start, which increases inequity. Relegating the consideration of all user groups to the point when design has been nearly completed is to lower the bar of what it means to be an excellent engineer. Instead, by building in inclusive design from the start and raising development standards for development to make tools delightful and accessible for people who struggle to access technology, we enhance the experience for all users.

如今常见的做法是，先满足多数用户的使用场景，把针对边缘用例的改进和功能留到以后。但这种做法有缺陷：它让原本就更容易获取技术的用户进一步占得先机，加剧了不公平。等到设计接近完成，才开始考虑所有用户群体，就是在降低优秀工程师的标准。相反，如果从一开始就融入包容性设计，提高开发标准，让那些难以获取技术的人也能使用工具、获得愉快的体验，就能改善所有用户的体验。

Designing for the user who is least like you is not just wise, it’s a best practice. There are pragmatic and immediate next steps that all technologists, regardless of domain, should consider when developing products that avoid disadvantaging or underrepresenting users. It begins with more comprehensive user-experience research. This research should be done with user groups that are multilingual and multicultural and that span multiple countries, socioeconomic class, abilities, and age ranges. Focus on the most difficult or least represented use case first.

为与你最不相似的用户设计产品，不仅明智，也是一项最佳实践。无论从事哪个领域，技术人员在开发产品、避免让用户处于不利地位或代表性不足时，都应考虑一些务实且可以立即采取的行动。首先，要开展更全面的用户体验研究，覆盖不同语言、文化、国家、社会经济阶层、能力和年龄段的用户群体。优先关注最困难或代表性最不足的用例。

## Challenge Established Processes 挑战既定流程

Challenging yourself to build more equitable systems goes beyond designing more inclusive product specifications. Building equitable systems sometimes means challenging established processes that drive invalid results.

要求自己构建更公平的系统，不能只停留在制定更具包容性的产品规格上。有时，这还意味着质疑那些会产生无效结果的既定流程。

Consider a recent case evaluated for equity implications. At Google, several engineering teams worked to build a global hiring requisition system. The system supports both external hiring and internal mobility. The engineers and product managers involved did a great job of listening to the requests of what they considered to be their core user group: recruiters. The recruiters were focused on minimizing wasted time for hiring managers and applicants, and they presented the development team with use cases focused on scale and efficiency for those people. To drive efficiency, the recruiters asked the engineering team to include a feature that would highlight performance ratings—specifically lower ratings—to the hiring manager and recruiter as soon as an internal transfer expressed interest in a job.

来看一个近期接受过公平性影响评估的案例。谷歌的几个工程团队共同开发了一套全球招聘需求申请系统，同时支持外部招聘和内部流动。参与项目的工程师和产品经理，认真听取了他们认定的核心用户群体，也就是招聘人员的需求。招聘人员希望尽量减少用人经理和求职者浪费的时间，因此向开发团队提出了着重为这些人提升规模化处理能力和效率的用例。为提高效率，他们要求加入一项功能：内部员工一旦表达对某个岗位的兴趣，系统就立即向用人经理和招聘人员突出显示其绩效评级，尤其是较低的评级。

On its face, expediting the evaluation process and helping job seekers save time is a great goal. So where is the potential equity concern? The following equity questions were raised:

- Are developmental assessments a predictive measure of performance?
- Are the performance assessments being presented to prospective managers free of individual bias?
- Are performance assessment scores standardized across organizations?

乍看之下，加快评估流程、帮助求职者节省时间，是个很好的目标。那么，其中可能有哪些公平性问题？评估中提出了以下疑问：

- 发展性评估能否作为预测绩效的指标？
- 提供给未来可能接收候选人的经理的绩效评估，是否不带个人偏见？
- 不同组织的绩效评估分数是否采用统一标准？

If the answer to any of these questions is “no,” presenting performance ratings could still drive inequitable, and therefore invalid, results.

只要其中任一问题的答案是“否”，展示绩效评级就仍可能产生不公平、因而无效的结果。

When an exceptional engineer questioned whether past performance was in fact predictive of future performance, the reviewing team decided to conduct a thorough review. In the end, it was determined that candidates who had received a poor performance rating were likely to overcome the poor rating if they found a new team. In fact, they were just as likely to receive a satisfactory or exemplary performance rating as candidates who had never received a poor rating. In short, performance ratings are indicative only of how a person is performing in their given role at the time they are being evaluated. Ratings, although an important way to measure performance during a specific period, are not predictive of future performance and should not be used to gauge readiness for a future role or qualify an internal candidate for a different team. (They can, however, be used to evaluate whether an employee is properly or improperly slotted on their current team; therefore, they can provide an opportunity to evaluate how to better support an internal candidate moving forward.)

一位卓越的工程师提出疑问：过去的绩效真的能预测未来的绩效吗？审查团队因此决定深入调查。最终得出的结论是，曾获较差绩效评级的候选人，如果转到新团队，很可能扭转此前的低评级。事实上，他们获得满意或卓越绩效评级的可能性，与从未得到过低评级的候选人一样。简而言之，绩效评级只能反映一个人在受评期间、所任岗位上的表现。评级虽然是衡量特定时期绩效的重要方式，却不能预测未来绩效，不应据此判断一个人是否已准备好担任未来的岗位，或是否具备转入其他团队的资格。（不过，评级可以帮助判断员工在当前团队中的岗位安排是否合适，从而让我们有机会评估，今后怎样更好地支持这位内部候选人。）

This analysis definitely took up significant project time, but the positive trade-off was a more equitable internal mobility process.

这项分析确实占用了大量项目时间，但换来了更公平的内部流动流程。

## Values Versus Outcomes 价值观与结果

Google has a strong track record of investing in hiring. As the previous example illustrates, we also continually evaluate our processes in order to improve equity and inclusion. More broadly, our core values are based on respect and an unwavering commitment to a diverse and inclusive workforce. Yet, year after year, we have also missed our mark on hiring a representative workforce that reflects our users around the globe. The struggle to improve our equitable outcomes persists despite the policies and programs in place to help support inclusion initiatives and promote excellence in hiring and progression. The failure point is not in the values, intentions, or investments of the company, but rather in the application of those policies at the implementation level.

谷歌长期以来一直积极投入招聘工作。前面的例子也表明，我们一直在评估流程，以提升公平性和包容性。从更广的层面看，我们的核心价值观以尊重为基础，并坚定致力于建设多元、包容的员工队伍。然而，年复一年，我们仍未能招到足以代表全球用户的员工队伍。尽管已有政策和项目支持包容性举措，推动招聘和晋升工作做到更好，要取得更公平的结果，我们仍在艰难探索。问题不在于公司的价值观、意愿或投入，而在于这些政策在执行层面如何落实。

Old habits are hard to break. The users you might be used to designing for today— the ones you are used to getting feedback from—might not be representative of all the users you need to reach. We see this play out frequently across all kinds of products, from wearables that do not work for women’s bodies to video-conferencing software that does not work well for people with darker skin tones.

旧习惯很难改变。你如今习惯为之设计产品、从中获取反馈的那些用户，未必能代表你需要触及的所有用户。各类产品中都常见这种情况：有的可穿戴设备不适配女性身体，有的视频会议软件对肤色较深的人效果不佳。

So, what’s the way out?

1. Take a hard look in the mirror. At Google, we have the brand slogan, “Build For Everyone.” How can we build for everyone when we do not have a representative workforce or engagement model that centralizes community feedback first? We can’t. The truth is that we have at times very publicly failed to protect our most vulnerable users from racist, antisemitic, and homophobic content.
2. Don’t build for everyone. Build with everyone. We are not building for everyone yet. That work does not happen in a vacuum, and it certainly doesn’t happen when the technology is still not representative of the population as a whole. That said, we can’t pack up and go home. So how do we build for everyone? We build with our users. We need to engage our users across the spectrum of humanity and be intentional about putting the most vulnerable communities at the center of our design. They should not be an afterthought.
3. Design for the user who will have the most difficulty using your product. Building for those with additional challenges will make the product better for everyone. Another way of thinking about this is: don’t trade equity for short-term velocity.
4. Don’t assume equity; measure equity throughout your systems. Recognize that decision makers are also subject to bias and might be undereducated about the causes of inequity. You might not have the expertise to identify or measure the scope of an equity issue. Catering to a single userbase might mean disenfranchising another; these trade-offs can be difficult to spot and impossible to reverse. Partner with individuals or teams that are subject matter experts in diversity, equity, and inclusion.
5. Change is possible. The problems we’re facing with technology today, from surveillance to disinformation to online harassment, are genuinely overwhelming. We can’t solve these with the failed approaches of the past or with just the skills we already have. We need to change.

那么，出路是什么？

1. 认真审视自己。谷歌的品牌口号是“为所有人打造产品”。如果没有能代表用户的员工队伍，也没有把群体反馈放在首位的参与模式，我们怎么可能做到这一点？做不到。事实上，在保护最弱势的用户免受种族主义、反犹太主义和恐同内容侵害方面，我们有过备受关注的失败。
2. 不要为所有人打造产品，要与所有人共同打造产品。我们还没有做到为所有人服务。这项工作不会凭空完成，技术尚不能代表整个人群时，就更无从谈起。不过，我们也不能就此放弃。那么，怎样才能为所有人打造产品？与用户一起做。我们需要让来自各种人群的用户参与进来，有意识地把最弱势的群体置于设计的中心，而不是事后才想到他们。
3. 为使用产品时最困难的用户设计。照顾到面临额外挑战的人，会让产品对所有人都更好。换句话说，不要用公平换取短期开发速度。
4. 不要假定系统已经公平；**衡量整个系统的公平性**。要认识到，决策者同样会受偏见影响，也可能对不公平的成因缺乏了解。你未必具备识别公平性问题、衡量其影响范围的专业知识。满足一个用户群体，可能意味着剥夺另一个群体的权益；这些取舍可能很难察觉，后果也可能无法逆转。应与在多样性、公平和包容领域具备专业知识的个人或团队合作。
5. 改变是可能的。如今的技术问题，从监控、虚假信息到网络骚扰，确实让人难以招架。过去失败的方法解决不了这些问题，仅靠我们已有的技能也不够。我们需要改变。

## Stay Curious, Push Forward 保持好奇，继续前行

The path to equity is long and complex. However, we can and should transition from simply building tools and services to growing our understanding of how the products we engineer impact humanity. Challenging our education, influencing our teams and managers, and doing more comprehensive user research are all ways to make progress. Although change is uncomfortable and the path to high performance can be painful, it is possible through collaboration and creativity.

通往公平的道路漫长而复杂。但我们可以，也应该不再只是开发工具和服务，而要不断加深理解：自己设计的产品会怎样影响人类。反思所受的教育，影响团队和管理者，开展更全面的用户研究，都是前进的方式。改变会让人不适，追求高绩效的过程也可能痛苦，但凭借协作和创造力，我们能够做到。

Lastly, as future exceptional engineers, we should focus first on the users most impacted by bias and discrimination. Together, we can work to accelerate progress by focusing on Continuous Improvement and owning our failures. Becoming an engineer is an involved and continual process. The goal is to make changes that push humanity forward without further disenfranchising the disadvantaged. As future exceptional engineers, we have faith that we can prevent future failures in the system.

最后，作为未来的卓越工程师，我们应当首先关注受偏见和歧视影响最大的用户。只要共同努力，专注于持续改进，并为自己的失败承担责任，就能加快进步。成为工程师是一个复杂而持续的过程。我们的目标是作出推动人类前进的改变，同时不进一步剥夺弱势群体的权益。作为未来的卓越工程师，我们相信自己能够防止体系今后再出现失败。

## Conclusion 总结

Developing software, and developing a software organization, is a team effort. As a software organization scales, it must respond and adequately design for its user base, which in the interconnected world of computing today involves everyone, locally and around the world. More effort must be made to make both the development teams that design software and the products that they produce reflect the values of such a diverse and encompassing set of users. And, if an engineering organization wants to scale, it cannot ignore underrepresented groups; not only do such engineers from these groups augment the organization itself, they provide unique and necessary perspectives for the design and implementation of software that is truly useful to the world at large.

开发软件、建设软件组织，都需要团队协作。随着规模扩大，软件组织必须回应用户需求，并在设计中充分考虑用户。在当今互联的计算世界里，用户涵盖本地乃至全球的每一个人。我们需要付出更多努力，让软件开发团队及其产品，都能体现这个广泛而多元的用户群体的价值观。工程组织要扩大规模，就不能忽视代表性不足的群体。来自这些群体的工程师不仅能增强组织本身，还能带来独特而必要的视角，帮助我们设计和实现真正有益于整个世界的软件。

## TL;DRs  内容提要

- Bias is the default.
- Diversity is necessary to design properly for a comprehensive user base.
- Inclusivity is critical not just to improving the hiring pipeline for underrepresented groups, but to providing a truly supportive work environment for all people.
- Product velocity must be evaluated against providing a product that is truly useful to all users. It’s better to slow down than to release a product that might cause harm to some users.

- 偏见是默认状态。
- 要为广泛的用户群体做好设计，多样性不可或缺。
- 包容性不仅是改善代表性不足群体招聘渠道的关键，也是为所有人营造真正支持他们的工作环境的关键。
- 评估产品开发速度时，必须权衡能否提供真正有助于所有用户的产品。与其发布可能伤害部分用户的产品，不如放慢速度。
