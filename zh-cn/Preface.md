## Preface 前言

This book is titled *Software Engineering at Google*. What precisely do we mean by software engineering? What distinguishes “software engineering” from “programming” or “computer science”? And why would Google have a unique perspective to add to the corpus of previous software engineering literature written over the past 50 years?

本书名为*《谷歌的软件工程》*。我们所说的软件工程究竟是什么？它与“编程”或“计算机科学”有什么区别？面对过去50年积累的软件工程文献，谷歌又能补充什么独特的视角？

The terms “programming” and “software engineering” have been used interchangeably for quite some time in our industry, although each term has a different emphasis and different implications. University students tend to study computer science and get jobs writing code as “programmers.”

很长一段时间以来，业界一直混用“编程”和“软件工程”这两个术语，尽管它们各有侧重，含义也不相同。大学生通常学习计算机科学，毕业后以“程序员”的身份从事编写代码的工作。

“Software engineering,” however, sounds more serious, as if it implies the application of some theoretical knowledge to build something real and precise. Mechanical engineers, civil engineers, aeronautical engineers, and those in other engineering disciplines all practice engineering. They all work in the real world and use the application of their theoretical knowledge to create something real. Software engineers also create “something real,” though it is less tangible than the things other engineers create.

不过，“软件工程”听起来更为严肃，仿佛意味着运用理论知识，构建真实而精确的东西。机械、土木、航空等领域的工程师都在从事工程实践：在现实世界中运用理论知识，创造实际成果。软件工程师同样如此，只是他们的成果不像其他工程师的作品那样有形。

Unlike those more established engineering professions, current software engineering theory or practice is not nearly as rigorous. Aeronautical engineers must follow rigid guidelines and practices, because errors in their calculations can cause real damage; programming, on the whole, has traditionally not followed such rigorous practices. But, as software becomes more integrated into our lives, we must adopt and rely on more rigorous engineering methods. We hope this book helps others see a path toward more reliable software practices.

与这些更成熟的工程领域相比，软件工程现有的理论和实践还远不够严谨。航空工程师必须遵循严格的规范和实践，因为计算错误可能造成实际损害；而传统编程总体上并未采用如此严格的方法。随着软件日益融入生活，我们必须采用并依靠更严谨的工程方法。希望本书能为读者指明通向更可靠软件实践的路径。

### Programming Over Time 随时间变化的编程

We propose that “software engineering” encompasses not just the act of writing code, but all of the tools and processes an organization uses to build and maintain that code over time. What practices can a software organization introduce that will best keep its code valuable over the long term? How can engineers make a codebase more sustainable and the software engineering discipline itself more rigorous? We don’t have fundamental answers to these questions, but we hope that Google’s collective experience over the past two decades illuminates possible paths toward finding those answers.

我们认为，“软件工程”不仅包括编写代码，还涵盖组织为长期构建和维护代码而采用的所有工具与流程。软件组织应采用哪些实践，才能让代码长期保持价值？工程师如何提高代码库的可持续性，同时让软件工程这门学科更加严谨？我们没有根本性的答案，但希望谷歌过去二十年的集体经验，能为寻找答案提供一些方向。

One key insight we share in this book is that software engineering can be thought of as “programming integrated over time.” What practices can we introduce to our code to make it *sustainable*—able to react to necessary change—over its life cycle, from conception to introduction to maintenance to deprecation?

本书的一个核心观点是，软件工程可以看作“编程在时间上的积分”。从构思、引入，到维护、弃用，我们应采用哪些实践，才能让代码在整个生命周期中保持*可持续性*，也就是能够应对必要的变化？

The book emphasizes three fundamental principles that we feel software organizations should keep in mind when designing, architecting, and writing their code:  

*Time and Change*  
&nbsp;&nbsp;&nbsp;&nbsp; How code will need to adapt over the length of its life

*Scale and Growth*  
&nbsp;&nbsp;&nbsp;&nbsp; How an organization will need to adapt as it evolves

*Trade-offs and Costs*  
&nbsp;&nbsp;&nbsp;&nbsp; How an organization makes decisions, based on the lessons of Time and Change and Scale and Growth

本书强调三个基本原则，我们认为软件组织在设计、确定架构和编写代码时，都应牢记它们：

*时间和变化*  
&nbsp;&nbsp;&nbsp;&nbsp; ​代码需要如何适应整个生命周期中的变化。

*规模和增长*  
&nbsp;&nbsp;&nbsp;&nbsp; ​组织需要如何随着自身发展而调整。

*权衡和成本*  
&nbsp;&nbsp;&nbsp;&nbsp; ​组织如何结合时间与变化、规模与增长方面的经验作出决策。

Throughout the chapters, we have tried to tie back to these themes and point out ways in which such principles affect engineering practices and allow them to be sustainable. (See [Chapter 1 ](#_bookmark3)for a full discussion.)

全书各章都会围绕这些主题展开，说明它们如何影响工程实践，并使实践具备可持续性。完整讨论见[第1章](#_bookmark3)。

### Google’s Perspective 谷歌的视角

Google has a unique perspective on the growth and evolution of a sustainable soft‐ ware ecosystem, stemming from our scale and longevity. We hope that the lessons we have learned will be useful as your organization evolves and embraces more sustainable practices.

谷歌的规模和长期积累，让我们对可持续软件生态系统的成长与演进形成了独特视角。希望这些经验能帮助你的组织在发展过程中采用更具可持续性的实践。

We’ve divided the topics in this book into three main aspects of Google’s software engineering landscape:
- Culture
- Processes
- Tools

本书从三个主要方面介绍谷歌的软件工程：
- 文化
- 流程
- 工具

Google’s culture is unique, but the lessons we have learned in developing our engineering culture are widely applicable. Our chapters on Culture ([Part II](#_bookmark100)) emphasize the collective nature of a software development enterprise, that the development of software is a team effort, and that proper cultural principles are essential for an organization to grow and remain healthy.

谷歌的文化有其独特之处，但建设工程文化的经验具有广泛适用性。文化篇（[第二部分](#_bookmark100)）强调软件开发的集体性：开发软件依靠团队协作，恰当的文化原则对于组织成长和保持健康至关重要。

The techniques outlined in our Processes chapters ([Part III](#_bookmark579)) are familiar to most soft‐ ware engineers, but Google’s large size and long-lived codebase provides a more complete stress test for developing best practices. Within those chapters, we have tried to emphasize what we have found to work over time and at scale as well as identify areas where we don’t yet have satisfying answers.

流程篇（[第三部分](#_bookmark579)）介绍的方法，大多数软件工程师并不陌生。但谷歌庞大的规模和长期维护的代码库，让这些最佳实践经受了更充分的压力测试。这些章节着重介绍哪些做法能够经受时间和规模的考验，也会指出我们仍未找到满意答案的领域。

Finally, our Tools chapters ([Part IV](#_bookmark1363)) illustrate how we leverage our investments in tooling infrastructure to provide benefits to our codebase as it both grows and ages. In some cases, these tools are specific to Google, though we point out open source or third-party alternatives where applicable. We expect that these basic insights apply to most engineering organizations.

最后，工具篇（[第四部分](#_bookmark1363)）说明，我们如何通过投入工具基础设施，使不断增长、逐渐老化的代码库持续受益。有些工具是谷歌专用的，但我们也会在适当之处介绍开源或第三方替代方案。我们认为，这些基本认识适用于大多数工程组织。

The culture, processes, and tools outlined in this book describe the lessons that a typical software engineer hopefully learns on the job. Google certainly doesn’t have a monopoly on good advice, and our experiences presented here are not intended to dictate what your organization should do. This book is our perspective, but we hope you will find it useful, either by adopting these lessons directly or by using them as a starting point when considering your own practices, specialized for your own problem domain.

本书介绍的文化、流程和工具，涵盖了一名软件工程师理应在工作中逐步掌握的经验。好的建议当然不只来自谷歌，我们也无意用这些经验规定你的组织该怎么做。书中呈现的是我们的视角，希望它对你有用：既可以直接借鉴，也可以以此为起点，探索适合自身问题领域的实践。

Neither is this book intended to be a sermon. Google itself still imperfectly applies many of the concepts within these pages. The lessons that we have learned, we learned through our failures: we still make mistakes, implement imperfect solutions, and need to iterate toward improvement. Yet the sheer size of Google’s engineering organization ensures that there is a diversity of solutions for every problem. We hope that this book contains the best of that group.

本书也不是说教。即使在谷歌，书中的许多理念也尚未得到完美实践。这些经验来自失败：我们仍会犯错，采用的方案仍有不足，也仍需不断迭代改进。不过，谷歌工程组织的庞大规模，使每个问题都有多种解决思路。希望本书收录了其中最有价值的部分。

### What This Book Isn’t 本书不讨论什么

This book is not meant to cover software design, a discipline that requires its own book (and for which much content already exists). Although there is some code in this book for illustrative purposes, the principles are language neutral, and there is little actual “programming” advice within these chapters. As a result, this text doesn’t cover many important issues in software development: project management, API design, security hardening, internationalization, user interface frameworks, or other language-specific concerns. Their omission in this book does not imply their lack of importance. Instead, we choose not to cover them here knowing that we could not provide the treatment they deserve. We have tried to make the discussions in this book more about engineering and less about programming.

本书不打算讨论软件设计，这门学科值得专门成书，而且已经有丰富的相关资料。书中的少量代码用于举例，所讨论的原则与具体语言无关，也很少涉及具体的“编程”建议。因此，本书没有覆盖软件开发中的许多重要主题，例如项目管理、API 设计、安全加固、国际化、用户界面框架，以及特定编程语言的问题。没有讨论并不意味着它们不重要，而是因为我们无法在本书中给予它们应有的深入论述。我们希望把重点放在工程，而不是编程上。

### Parting Remarks 临别赠言

This text has been a labor of love on behalf of all who have contributed, and we hope that you receive it as it is given: as a window into how a large software engineering organization builds its products. We also hope that it is one of many voices that helps move our industry to adopt more forward-thinking and sustainable practices. Most important, we further hope that you enjoy reading it and can adopt some of its lessons to your own concerns.

本书凝聚了所有参与者的热爱与心血。希望你能按我们的初衷看待它：一扇了解大型软件工程组织如何构建产品的窗口。也希望它能与其他声音一道，推动业界采用更有前瞻性、更可持续的实践。最重要的是，希望你读得愉快，并能把其中一些经验用于自己的问题。



*— Tom Manshreck*





