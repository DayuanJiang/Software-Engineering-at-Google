
**CHAPTER 12**

# Unit Testing

# 第十二章 单元测试

**Written by Erik Kuefler**

**Edited by Tom Manshreck**

The previous chapter introduced two of the main axes along which Google classifies tests: *size* and *scope*. To recap, size refers to the resources consumed by a test and what it is allowed to do, and scope refers to how much code a test is intended to validate. Though Google has clear definitions for test size, scope tends to be a little fuzzier. We use the term *unit test* to refer to tests of relatively narrow scope, such as of a single class or method. Unit tests are usually small in size, but this isn’t always the case.

上一章介绍了谷歌对测试进行分类的两个主要维度：*规模*和*范围*。简单回顾一下，规模指测试消耗的资源及其允许执行的操作，范围指测试打算验证多少代码。谷歌对测试规模有明确的定义，但测试范围的界定往往稍显模糊。我们用*单元测试*指范围相对较窄的测试，例如针对单个类或方法的测试。按规模划分，单元测试通常属于小型测试，但并不总是如此。

After preventing bugs, the most important purpose of a test is to improve engineers’ productivity. Compared to broader-scoped tests, unit tests have many properties that make them an excellent way to optimize productivity:

- They tend to be small according to Google’s definitions of test size. Small tests are fast and deterministic, allowing developers to run them frequently as part of their workflow and get immediate feedback.
- They tend to be easy to write at the same time as the code they’re testing, allowing engineers to focus their tests on the code they’re working on without having to set up and understand a larger system.
- They promote high levels of test coverage because they are quick and easy to write. High test coverage allows engineers to make changes with confidence that they aren’t breaking anything.
- They tend to make it easy to understand what’s wrong when they fail because each test is conceptually simple and focused on a particular part of the system.
- They can serve as documentation and examples, showing engineers how to use the part of the system being tested and how that system is intended to work.

除了预防bug，测试最重要的目的就是提高工程师的生产力。与范围更广的测试相比，单元测试的许多特性使其成为提高生产力的有效手段：

- 按照谷歌对测试规模的定义，单元测试通常属于小型测试。小型测试运行快、结果确定，开发者可以在日常工作流中频繁运行，及时获得反馈。
- 单元测试通常很容易与被测代码一同编写。工程师可以专注于测试手头的代码，而不必搭建并理解一个更大的系统。
- 单元测试编写起来简单快捷，有助于提高测试覆盖率。较高的覆盖率让工程师更有信心，相信自己的变更不会破坏现有功能。
- 每个单元测试在概念上都很简单，专注于系统的某个特定部分，因此测试失败时，通常很容易判断哪里出了问题。
- 单元测试还可以充当文档和示例，向工程师展示如何使用系统中被测的部分，以及系统应当如何工作。

Due to their many advantages, most tests written at Google are unit tests, and as a rule of thumb, we encourage engineers to aim for a mix of about 80% unit tests and 20% broader-scoped tests. This advice, coupled with the ease of writing unit tests and the speed with which they run, means that engineers run a *lot* of unit tests—it’s not at all unusual for an engineer to execute thousands of unit tests (directly or indirectly) during the average workday.

由于单元测试有诸多优点，谷歌编写的大多数测试都是单元测试。作为一条经验法则，我们建议工程师采用约80%的单元测试和20%的较大范围测试。这一建议，加上单元测试易于编写、运行迅速，意味着工程师会运行*大量*单元测试：在一个普通工作日里，一名工程师直接或间接执行数千个单元测试，完全不足为奇。

Because they make up such a big part of engineers’ lives, Google puts a lot of focus on *test maintainability*. Maintainable tests are ones that “just work”: after writing them, engineers don’t need to think about them again until they fail, and those failures indicate real bugs with clear causes. The bulk of this chapter focuses on exploring the idea of maintainability and techniques for achieving it.

测试在工程师的日常工作中占据如此重要的位置，因此谷歌十分重视*测试*的可维护性。可维护的测试能“省心地工作”：写完之后，工程师不必再操心，直到测试失败；而这些失败应当指向原因明确的真实缺陷。本章主要探讨测试可维护性的含义，以及实现它的方法。

## The Importance of Maintainability  可维护性的重要性

Imagine this scenario: Mary wants to add a simple new feature to the product and is able to implement it quickly, perhaps requiring only a couple dozen lines of code. But when she goes to check in her change, she gets a screen full of errors back from the automated testing system. She spends the rest of the day going through those failures one by one. In each case, the change introduced no actual bug, but broke some of the assumptions that the test made about the internal structure of the code, requiring those tests to be updated. Often, she has difficulty figuring out what the tests were trying to do in the first place, and the hacks she adds to fix them make those tests even more difficult to understand in the future. Ultimately, what should have been a quick job ends up taking hours or even days of busywork, killing Mary’s productivity and sapping her morale.

想象这样一个场景：Mary想给产品添加一个简单的新功能，很快就实现了，也许只写了几十行代码。但当她准备提交变更时，自动化测试系统却返回了满屏错误。她用当天剩下的时间逐一排查这些失败。每一次，变更都没有引入真正的bug，只是打破了测试对代码内部结构的某些假设，因此需要更新测试。她往往很难弄清这些测试原本想验证什么，而为了修好它们所加的临时变通代码，又让测试日后更难理解。最终，本来很快就能完成的工作，却变成了几小时甚至几天的琐碎忙碌，拖累了Mary的工作效率，也消磨了她的士气。

Here, testing had the opposite of its intended effect by draining productivity rather than improving it while not meaningfully increasing the quality of the code under test. This scenario is far too common, and Google engineers struggle with it every day. There’s no magic bullet, but many engineers at Google have been working to develop sets of patterns and practices to alleviate these problems, which we encourage the rest of the company to follow.

这里，测试起到了与预期相反的作用：没有提高生产力，反而拖了后腿，也没有实质性地改善被测代码的质量。这类情况十分常见，谷歌工程师每天都在应对。虽然没有一劳永逸的解决办法，但谷歌的许多工程师一直在总结缓解这些问题的模式和实践，我们也鼓励公司其他人采用。

The problems Mary ran into weren’t her fault, and there was nothing she could have done to avoid them: bad tests must be fixed before they are checked in, lest they impose a drag on future engineers. Broadly speaking, the issues she encountered fall into two categories. First, the tests she was working with were *brittle*: they broke in response to a harmless and unrelated change that introduced no real bugs. Second, the tests were *unclear*: after they were failing, it was difficult to determine what was wrong, how to fix it, and what those tests were supposed to be doing in the first place.

Mary遇到这些问题并不是她的错，她也无从避免：有问题的测试必须在提交之前修好，否则就会拖累后续接手的工程师。大体而言，她遇到的问题分为两类。第一，测试很脆弱：一个无害且与测试无关的变更，并未引入真正的bug，却导致测试失败。第二，测试不清晰：失败之后，很难判断哪里出了问题、如何修复，以及测试原本应该验证什么。

## Preventing Brittle Tests  避免脆弱测试

As just defined, a brittle test is one that fails in the face of an unrelated change to production code that does not introduce any real bugs.[^1] Such tests must be diagnosed and fixed by engineers as part of their work. In small codebases with only a few engineers, having to tweak a few tests for every change might not be a big problem. But if a team regularly writes brittle tests, test maintenance will inevitably consume a larger and larger proportion of the team’s time as they are forced to comb through an increasing number of failures in an ever-growing test suite. If a set of tests needs to be manually tweaked by engineers for each change, calling it an “automated test suite” is a bit of a stretch!

如前所述，脆弱测试是指这样的测试：生产代码发生了与测试无关、也没有引入真正缺陷的变更，测试却因此失败。工程师不得不花时间诊断并修复这些测试。对于只有几名工程师维护的小型代码库，每次变更时调整几个测试，也许算不上大问题。但如果团队经常编写脆弱测试，就不得不在不断扩大的测试套件中排查越来越多的失败，测试维护势必占用团队越来越多的时间。如果每次变更都要由工程师手动调整测试，称它为“自动化测试套件”就有些牵强了！

Brittle tests cause pain in codebases of any size, but they become particularly acute at Google’s scale. An individual engineer might easily run thousands of tests in a single day during the course of their work, and a single large-scale change (see [Chapter 22](#_bookmark1935)) can trigger hundreds of thousands of tests. At this scale, spurious breakages that affect even a small percentage of tests can waste huge amounts of engineering time. Teams at Google vary quite a bit in terms of how brittle their test suites are, but we’ve identified a few practices and patterns that tend to make tests more robust to change.

脆弱测试在任何规模的代码库中都会带来麻烦，在谷歌这样的规模下，问题尤其严重。一名工程师在一天的工作中就可能运行数千个测试，而一次大规模变更（见第22章）可能触发数十万个测试。在这种规模下，即使只有一小部分测试出现并非真实缺陷所致的失败，也会浪费大量工程师时间。谷歌各团队的测试套件在脆弱程度上差异很大，但我们已经总结出一些实践和模式，通常能让测试更经得起代码变更。

> [^1]: Note that this is slightly different from a flaky test, which fails nondeterministically without any change to production code./
> 1  注意，这与不稳定测试略有不同：不稳定测试在生产代码没有任何变化时，也会非确定性地失败。

### Strive for Unchanging Tests  力求让测试无需改动

Before talking about patterns for avoiding brittle tests, we need to answer a question: just how often should we expect to need to change a test after writing it? Any time spent updating old tests is time that can’t be spent on more valuable work. Therefore, *the ideal test is unchanging*: after it’s written, it never needs to change unless the requirements of the system under test change.

在讨论如何避免脆弱测试之前，需要先回答一个问题：测试写好后，我们预期多久需要修改一次？更新旧测试占用的时间，就无法用于更有价值的工作。因此，*理想的测试无需改动*：一旦写好，除非被测系统的需求发生变化，否则就不必再改。

What does this look like in practice? We need to think about the kinds of changes that engineers make to production code and how we should expect tests to respond to those changes. Fundamentally, there are four kinds of changes:

- *Pure refactorings*  
	When an engineer refactors the internals of a system without modifying its interface, whether for performance, clarity, or any other reason, the system’s tests shouldn’t need to change. The role of tests in this case is to ensure that the refactoring didn’t change the system’s behavior. Tests that need to be changed during a refactoring indicate that either the change is affecting the system’s behavior and isn’t a pure refactoring, or that the tests were not written at an appropriate level of abstraction. Google’s reliance on large-scale changes (described in Chapter 22) to do such refactorings makes this case particularly important for us.

- *New features*  
	When an engineer adds new features or behaviors to an existing system, the system’s existing behaviors should remain unaffected. The engineer must write new tests to cover the new behaviors, but they shouldn’t need to change any existing tests. As with refactorings, a change to existing tests when adding new features suggest unintended consequences of that feature or inappropriate tests.

- *Bug fixes*  
	Fixing a bug is much like adding a new feature: the presence of the bug suggests that a case was missing from the initial test suite, and the bug fix should include that missing test case. Again, bug fixes typically shouldn’t require updates to existing tests.

- *Behavior changes*  
	Changing a system’s existing behavior is the one case when we expect to have to make updates to the system’s existing tests. Note that such changes tend to be significantly more expensive than the other three types. A system’s users are likely to rely on its current behavior, and changes to that behavior require coordination with those users to avoid confusion or breakages. Changing a test in this case indicates that we’re breaking an explicit contract of the system, whereas changes in the previous cases indicate that we’re breaking an unintended contract. Low- level libraries will often invest significant effort in avoiding the need to ever make a behavior change so as not to break their users.

落实到实践中，这意味着什么？我们需要考虑工程师会对生产代码作出哪些变更，以及测试应当如何响应。基本上，变更可以分为四类：

- *纯粹的重构*  
  工程师在不改变系统接口的前提下重构内部实现时，无论是为了改善性能、提高代码清晰度，还是出于其他原因，都不应需要修改测试。此时，测试的作用是确保重构没有改变系统行为。如果重构时必须修改测试，就说明变更影响了系统行为，并非纯粹的重构；或者测试没有选对抽象层次。Google依靠大规模变更（见第22章）进行这类重构，因此这一点对我们尤其重要。

- *新功能*  
  工程师为现有系统添加功能或行为时，系统原有的行为应当保持不变。工程师必须编写新测试来覆盖新行为，但不应需要修改任何已有测试。与重构类似，如果添加新功能时必须修改已有测试，就说明该功能可能带来了意外影响，或者原有测试写得不恰当。

- *Bug修复*  
  修复bug与添加新功能很相似：bug的存在说明原有测试套件遗漏了一个用例，修复bug时应当补上这个测试用例。同样，修复缺陷通常也不应需要更新已有测试。

- *行为变更*  
  改变系统的既有行为，是我们预期需要更新已有测试的唯一情况。注意，这类变更的成本往往远高于另外三类。系统用户很可能依赖当前行为，改变行为时需要与他们协调，以免造成困惑或功能失效。此时修改测试，说明我们正在打破系统的一项明确契约；而在前面几种情况下修改测试，则说明我们打破了一项无意间形成的契约。底层库往往会投入大量精力，尽量避免改变行为，以免影响使用者。

The takeaway is that after you write a test, you shouldn’t need to touch that test again as you refactor the system, fix bugs, or add new features. This understanding is what makes it possible to work with a system at scale: expanding it requires writing only a small number of new tests related to the change you’re making rather than potentially having to touch every test that has ever been written against the system. Only breaking changes in a system’s behavior should require going back to change its tests, and in such situations, the cost of updating those tests tends to be small relative to the cost of updating all of the system’s users.

要点是，测试写好之后，重构系统、修复bug或添加新功能时，都不应需要再改它。这一认识使大规模开发和维护系统成为可能：扩展系统时，只需为当前变更补充少量相关测试，而不是可能要修改所有为该系统编写过的测试。只有系统行为发生不兼容变更时，才应需要回头修改测试；而此时，更新测试的成本，通常远小于让所有系统用户适配变更的成本。

### Test via Public APIs  通过公共API进行测试

Now that we understand our goal, let’s look at some practices for making sure that tests don’t need to change unless the requirements of the system being tested change. By far the most important way to ensure this is to write tests that invoke the system being tested in the same way its users would; that is, make calls against its public API [rather than its implementation details](https://oreil.ly/ijat0). If tests work the same way as the system’s users, by definition, change that breaks a test might also break a user. As an additional bonus, such tests can serve as useful examples and documentation for users.

明确目标之后，来看看如何做到只有被测系统的需求改变时，才需要修改测试。其中最重要的做法，是让测试像用户一样调用系统，也就是调用公共API，[而不是其实现细节](https://oreil.ly/ijat0)。如果测试和用户以相同方式使用系统，那么按定义，导致测试失败的变更也可能影响用户。此外，这样的测试还能为用户提供有用的示例和文档。

Consider Example 12-1, which validates a transaction and saves it to a database.

来看例12-1：它验证一笔交易，并将其保存到数据库中。

*Example* *12-1.* *A transaction API *  *例12-1.交易API*

```java 
public void processTransaction(Transaction transaction) {
    if(isValid(transaction)) {
        saveToDatabase(transaction);
    }
}
private boolean isValid(Transaction t) {
    return t.getAmount() < t.getSender().getBalance();
}
private void saveToDatabase(Transaction t) {
    String s = t.getSender() + "," + t.getRecipient() + "," + t.getAmount();
    database.put(t.getId(), s);
}
public void setAccountBalance(String accountName, int balance) {
    // Write the balance to the database directly
}
public void getAccountBalance(String accountName) {
    // Read transactions from the database to determine the account balance
}
```

A tempting way to test this code would be to remove the “private” visibility modifiers and test the implementation logic directly, as demonstrated in Example 12-2.

测试这段代码时，很容易想到去掉“私有”可见性修饰符，直接测试实现逻辑，如例12-2所示。

*Example 12-2. A naive test of a transaction API’s implementation*  *例12-2.交易 API 实现的简单测试*

```java
@Test
public void emptyAccountShouldNotBeValid() {
    assertThat(processor.isValid(newTransaction().setSender(EMPTY_ACCOUNT))).isFalse();
}

@Test
public void shouldSaveSerializedData() {
    processor.saveToDatabase(newTransaction().setId(123).setSender("me").setRecipient("you").setAmount(100));
    assertThat(database.get(123)).isEqualTo("me,you,100");
}

```

This test interacts with the transaction processor in a much different way than its real users would: it peers into the system’s internal state and calls methods that aren’t publicly exposed as part of the system’s API. As a result, the test is brittle, and almost any refactoring of the system under test (such as renaming its methods, factoring them out into a helper class, or changing the serialization format) would cause the test to break, even if such a change would be invisible to the class’s real users.

这个测试使用交易处理器的方式，与真实用户截然不同：它查看系统内部状态，调用了并未作为系统API公开的方法。因此，这个测试很脆弱。几乎任何内部重构，例如重命名方法、将方法提取到辅助类，或改变序列化格式，都会使测试失败，即使类的真实用户完全察觉不到这些变化。

Instead, the same test coverage can be achieved by testing only against the class’s public API, as shown in Example 12-3.[^2]

其实，只通过类的公共 API 进行测试，也能达到相同的测试覆盖程度，如例12-3所示（注2）。

*Example 12-3. Testing the public API*  *例12-3. 测试公共API*

```java
@Test
public void shouldTransferFunds() {
    processor.setAccountBalance("me", 150);
    processor.setAccountBalance("you", 20);
    processor.processTransaction(newTransaction().setSender("me").setRecipient("you").setAmount(100));
    assertThat(processor.getAccountBalance("me")).isEqualTo(50);
    assertThat(processor.getAccountBalance("you")).isEqualTo(120);
}

@Test
public void shouldNotPerformInvalidTransactions() {
    processor.setAccountBalance("me", 50);
    processor.setAccountBalance("you", 20);
    processor.processTransaction(newTransaction().setSender("me").setRecipient("you").setAmount(100));
    assertThat(processor.getAccountBalance("me")).isEqualTo(50);
    assertThat(processor.getAccountBalance("you")).isEqualTo(20);
}

```

Tests using only public APIs are, by definition, accessing the system under test in the same manner that its users would. Such tests are more realistic and less brittle because they form explicit contracts: if such a test breaks, it implies that an existing user of the system will also be broken. Testing only these contracts means that you’re free to do whatever internal refactoring of the system you want without having to worry about making tedious changes to tests.

按定义，只使用公共API的测试，与用户访问被测系统的方式相同。这样的测试更贴近实际，也更不容易因无关变更而失败，因为它们确立了明确的契约：如果测试失败，就意味着系统的现有用户也会受到影响。只测试这些契约，就可以自由重构系统内部，而不必担心还要繁琐地修改测试。

> [^2]:	This is sometimes called the "Use the front door first principle.”
>
> 2   这有时被称为“优先走前门原则”。

It’s not always clear what constitutes a “public API,” and the question really gets to the heart of what a “unit” is in unit testing. Units can be as small as an individual function or as broad as a set of several related packages/modules. When we say “public API” in this context, we’re really talking about the API exposed by that unit to third parties outside of the team that owns the code. This doesn’t always align with the notion of visibility provided by some programming languages; for example, classes in Java might define themselves as “public” to be accessible by other packages in the same unit but are not intended for use by other parties outside of the unit. Some languages like Python have no built-in notion of visibility (often relying on conventions like prefixing private method names with underscores), and build systems like Bazel can further restrict who is allowed to depend on APIs declared public by the programming language.

哪些接口属于“公共API”，并不总是显而易见；这实际上触及了单元测试的核心问题：什么才算一个“单元”？单元可以小到一个函数，也可以大到几个相关包或模块的集合。这里的“公共API”，指的是单元向负责该代码的团队之外的第三方公开的API。这不一定与编程语言提供的可见性概念一致。例如，Java中的类可能声明为“公共”，以便同一单元中的其他包访问，却并不打算供单元之外的使用者调用。Python等语言没有内置的可见性概念，通常依靠约定，例如在私有方法名之前加下划线。而Bazel等构建系统，还能进一步限制哪些代码可以依赖那些在语言层面声明为公共的API。

Defining an appropriate scope for a unit and hence what should be considered the public API is more art than science, but here are some rules of thumb:

- If a method or class exists only to support one or two other classes (i.e., it is a “helper class”), it probably shouldn’t be considered its own unit, and its functionality should be tested through those classes instead of directly.
- If a package or class is designed to be accessible by anyone without having to consult with its owners, it almost certainly constitutes a unit that should be tested directly, where its tests access the unit in the same way that the users would.
- If a package or class can be accessed only by the people who own it, but it is designed to provide a general piece of functionality useful in a range of contexts (i.e., it is a “support library”), it should also be considered a unit and tested directly. This will usually create some redundancy in testing given that the support library’s code will be covered both by its own tests and the tests of its users. However, such redundancy can be valuable: without it, a gap in test coverage could be introduced if one of the library’s users (and its tests) were ever removed.

如何为单元划定合适的范围，并据此界定它的公共API，与其说有科学定式，不如说更依赖经验判断。不过，以下几条经验法则可供参考：

- 如果一个方法或类仅用于支持另外一两个类，也就是充当“辅助类”，通常就不应把它视为独立单元；应当通过使用它的类测试其功能，而不是直接测试它。

- 如果一个包或类的设计允许任何人直接使用，无须事先咨询其负责人，那么它几乎肯定是一个应当直接测试的单元。测试访问它的方式，应当与用户相同。

- 如果一个包或类只有负责它的人才能使用，但它提供的是适用于多种场景的通用功能，也就是一个“支持库”，同样应把它视为单元并直接测试。这通常会造成一定的测试冗余，因为支持库的代码既被自身测试覆盖，也被使用方的测试覆盖。但这样的冗余可能有价值：否则，一旦移除某个使用方及其测试，就可能在支持库的测试覆盖中留下缺口。

At Google, we’ve found that engineers sometimes need to be persuaded that testing via public APIs is better than testing against implementation details. The reluctance is understandable because it’s often much easier to write tests focused on the piece of code you just wrote rather than figuring out how that code affects the system as a whole. Nevertheless, we have found it valuable to encourage such practices, as the extra upfront effort pays for itself many times over in reduced maintenance burden. Testing against public APIs won’t completely prevent brittleness, but it’s the most important thing you can do to ensure that your tests fail only in the event of meaningful changes to your system.

在谷歌，有时需要花些工夫说服工程师：通过公共API测试，比针对实现细节测试更好。这种犹豫可以理解，毕竟直接测试刚写好的那段代码，往往远比弄清它如何影响整个系统容易。不过，我们发现推广这种做法很有价值：前期多花的精力，会通过后续维护负担的减少得到多倍回报。通过公共API测试，无法完全消除测试的脆弱性，但若要让测试只在系统发生实质性变化时才失败，这是最重要的一步。

### Test State, Not Interactions  测试状态，而不是交互

Another way that tests commonly depend on implementation details involves not which methods of the system the test calls, but how the results of those calls are verified. In general, there are two ways to verify that a system under test behaves as expected. With *state testing*, you observe the system itself to see what it looks like after invoking with it. With *interaction testing*, you instead check that the system took an expected sequence of actions on its collaborators [in response to invoking it](https://oreil.ly/3S8AL). Many tests will perform a combination of state and interaction validation.

测试对实现细节的另一种常见依赖，不在于调用系统的哪些方法，而在于如何验证调用结果。通常有两种方式验证被测系统的行为是否符合预期。*状态测试*观察系统本身，检查调用之后系统处于什么状态。*交互测试*则检查系统是否按预期顺序操作了协作对象，[以响应调用它](https://oreil.ly/3S8AL)的请求。许多测试会同时验证状态和交互。

Interaction tests tend to be more brittle than state tests for the same reason that it’s more brittle to test a private method than to test a public method: interaction tests check *how* a system arrived at its result, whereas usually you should care only *what* the result is. [Example 12-4 ](#_bookmark971)illustrates a test that uses a test double (explained further in [Chapter 13](#_bookmark1056)) to verify how a system interacts with a database.

交互测试往往比状态测试更脆弱，原因与测试私有方法比测试公共方法更脆弱相同：交互测试检查系统是*如何*得出结果的，而通常应该关注的只是结果是*什么*。例12-4使用测试替身（第13章会进一步介绍）来验证系统如何与数据库交互。

*Example  12-4. A brittle interaction test*  *例12-4.  脆弱的交互测试*

```java
@Test
public void shouldWriteToDatabase() {
    accounts.createUser("foobar");
    verify(database).put("foobar");
}
```

The test verifies that a specific call was made against a database API, but there are a couple different ways it could go wrong:
- If a bug in the system under test causes the record to be deleted from the database shortly after it was written, the test will pass even though we would have wanted it to fail.

- If the system under test is refactored to call a slightly different API to write an equivalent record, the test will fail even though we would have wanted it to pass.

这个测试验证是否调用了某个特定的数据库API，但在以下两种情况下都会得出错误结论：

- 如果被测系统中的缺陷导致记录刚写入数据库不久就被删除，测试本该失败，却仍会通过。
- 如果重构后的系统改用一个略有不同的API写入等价记录，测试本该通过，却会失败。

It’s much less brittle to directly test against the state of the system, as demonstrated in Example 12-5.

直接验证系统状态，测试就不容易因无关变更而失败，如例12-5所示。

*Example 12-5. Testing against state*  *例12-5. 针对状态的测试*

```java
@Test
public void shouldCreateUsers() {
    accounts.createUser("foobar");
    assertThat(accounts.getUser("foobar")).isNotNull();
}
```

This test more accurately expresses what we care about: the state of the system under test after interacting with it.

这个测试更准确地表达了我们真正关心的事：与被测系统交互之后，它处于什么状态。

The most common reason for problematic interaction tests is an over reliance on mocking frameworks. These frameworks make it easy to create test doubles that record and verify every call made against them, and to use those doubles in place of real objects in tests. This strategy leads directly to brittle interaction tests, and so we tend to prefer the use of real objects in favor of mocked objects, as long as the real objects are fast and deterministic.

交互测试出现问题，最常见的原因是过度依赖mocking框架。这些框架让人很容易创建测试替身，用它们记录并验证每一次调用，再在测试中替代真实对象。这种策略会直接导致脆弱的交互测试。因此，只要真实对象运行快、行为确定，我们就倾向于使用真实对象，而不是模拟对象。

## Writing Clear Tests  编写清晰的测试

Sooner or later, even if we’ve completely avoided brittleness, our tests will fail. Failure is a good thing—test failures provide useful signals to engineers, and are one of the main ways that a unit test provides value.
Test failures happen for one of two reasons:[^3]

- The system under test has a problem or is incomplete. This result is exactly what tests are designed for: alerting you to bugs so that you can fix them.
- The test itself is flawed. In this case, nothing is wrong with the system under test, but the test was specified incorrectly. If this was an existing test rather than one that you just wrote, this means that the test is brittle. The previous section discussed how to avoid brittle tests, but it’s rarely possible to eliminate them entirely.

即使完全避免了脆弱性，测试迟早还是会失败。这是好事：测试失败能为工程师提供有用的信号，也是单元测试发挥价值的主要方式之一。
测试失败的原因有以下两种：

- 被测系统有问题，或实现尚不完整。这正是测试的目的：提醒你存在bug，以便修复。
- 测试本身有缺陷。此时被测系统没有问题，但测试设定有误。如果出错的是已有测试，而不是刚写好的测试，就说明它是脆弱测试。上一节介绍了如何避免脆弱测试，但通常很难彻底消除。

When a test fails, an engineer’s first job is to identify which of these cases the failure falls into and then to diagnose the actual problem. The speed at which the engineer can do so depends on the test’s clarity. A clear test is one whose purpose for existing and reason for failing is immediately clear to the engineer diagnosing a failure. Tests fail to achieve clarity when their reasons for failure aren’t obvious or when it’s difficult to figure out why they were originally written. Clear tests also bring other benefits, such as documenting the system under test and more easily serving as a basis for new tests.

测试失败时，工程师首先要判断属于哪一种情况，再诊断具体问题。完成这项工作的速度，取决于测试是否清晰。清晰的测试能让排查失败的工程师立刻明白：这个测试为何存在，又为何失败。如果失败原因不明显，或者难以弄清最初为什么要写这个测试，它就不够清晰。清晰的测试还有其他好处，例如可作为被测系统的文档，也更容易成为编写新测试的基础。

Test clarity becomes significant over time. Tests will often outlast the engineers who wrote them, and the requirements and understanding of a system will shift subtly as it ages. It’s entirely possible that a failing test might have been written years ago by an engineer no longer on the team, leaving no way to figure out its purpose or how to fix it. This stands in contrast with unclear production code, whose purpose you can usually determine with enough effort by looking at what calls it and what breaks when it’s removed. With an unclear test, you might never understand its purpose, since removing the test will have no effect other than (potentially) introducing a subtle hole in test coverage.

时间越久，测试是否清晰就越重要。测试往往在作者离开之后仍会继续存在；随着系统逐渐老化，其需求和人们对它的理解也会悄然变化。一个失败的测试，完全可能出自多年前就已离开团队的工程师之手，让接手的人无从判断其目的，也不知道如何修复。生产代码不清晰时，情况有所不同：只要肯花工夫，查看哪些代码调用了它，以及删掉它会破坏什么，通常就能弄清它的用途。但对于不清晰的测试，你可能始终无法理解其目的，因为删掉它除了可能在测试覆盖中留下一个隐蔽缺口之外，并不会产生其他影响。

In the worst case, these obscure tests just end up getting deleted when engineers can’t figure out how to fix them. Not only does removing such tests introduce a hole in test coverage, but it also indicates that the test has been providing zero value for perhaps the entire period it has existed (which could have been years).

最坏的情况是，工程师不知道如何修复，最终只好删掉这些难以理解的测试。这不仅会在测试覆盖中留下缺口，也说明这些测试可能在存在的整个期间都没有发挥任何价值，而这段时间也许长达数年。

For a test suite to scale and be useful over time, it’s important that each individual test in that suite be as clear as possible. This section explores techniques and ways of thinking about tests to achieve clarity.

要让测试套件不断扩展并长期发挥作用，其中每个测试都应尽可能清晰。本节将介绍有助于实现这一目标的技巧和思路。

> [^3]: These are also the same two reasons that a test can be “flaky.” Either the system under test has a nondeterministic fault, or the test is flawed such that it sometimes fails when it should pass.
>
> 3   测试结果“不稳定”也出于这两个原因：要么被测系统存在非确定性故障，要么测试本身有缺陷，导致它有时在本应通过的情况下失败。

### Make Your Tests Complete and Concise  让测试完整且简洁

Two high-level properties that help tests achieve clarity are completeness and conciseness. A test is complete when its body contains all of the information a reader needs in order to understand how it arrives at its result. A test is concise when it contains no other distracting or irrelevant information. Example 12-6 shows a test that is neither complete nor concise:

从整体上看，清晰的测试应具备完整性和简洁性。完整，是指测试主体包含读者理解测试如何得出结果所需的全部信息；简洁，是指其中没有无关或分散注意力的信息。例12-6中的测试既不完整，也不简洁：

*Example 12-6. An incomplete and cluttered test*   *例12-6. 一个不完整且杂乱的测试*

```java
@Test
public void shouldPerformAddition() {
    Calculator calculator = new Calculator(new RoundingStrategy(), "unused", ENABLE_COSINE_FEATURE, 0.01, calculusEngine, false);
    int result = calculator.calculate(newTestCalculation());
    assertThat(result).isEqualTo(5); // Where did this number come from?
}
```

The test is passing a lot of irrelevant information into the constructor, and the actual important parts of the test are hidden inside of a helper method. The test can be made more complete by clarifying the inputs of the helper method, and more concise by using another helper to hide the irrelevant details of constructing the calculator, as illustrated in Example 12-7.

这个测试向构造函数传入了大量无关信息，却把真正重要的部分藏在辅助方法里。明确写出传给辅助方法的输入，可以让测试更完整；再用另一个辅助方法隐藏构造计算器时的无关细节，就能让测试更简洁，如例12-7所示。

*Example 12-7. A complete, concise test*  *例 12-7. A. 完整且简洁的测试*

```java
@Test
public void shouldPerformAddition() { 
    Calculator calculator = newCalculator();
    int result = calculator.calculate(newCalculation(2, Operation.PLUS, 3));
    assertThat(result).isEqualTo(5);
}
```

Ideas we discuss later, especially around code sharing, will tie back to completeness and conciseness. In particular, it can often be worth violating the DRY (Don’t Repeat Yourself) principle if it leads to clearer tests. Remember: a test’s body should contain all of the information needed to understand it without containing any irrelevant or distracting information.

后面讨论的许多做法，尤其是代码共享，都与完整性和简洁性有关。特别是，只要能让测试更清晰，适当违反DRY（不要重复自己）原则往往值得。请记住：**测试主体应包含理解它所需的全部信息，但不应包含无关或分散注意力的信息**。

### Test Behaviors, Not Methods  测试行为，而不是方法

The first instinct of many engineers is to try to match the structure of their tests to the structure of their code such that every production method has a corresponding test method. This pattern can be convenient at first, but over time it leads to problems: as the method being tested grows more complex, its test also grows in complexity and becomes more difficult to reason about. For example, consider the snippet of code in Example 12-8, which displays the results of a transaction.

许多工程师的第一反应，是让测试结构与代码结构一一对应，为生产代码中的每个方法编写一个测试方法。这种做法起初可能很方便，但时间一长就会出问题：被测方法越来越复杂，相应的测试也越来越复杂，越来越难以理解。来看例12-8中的代码片段，它用于显示交易结果。

*Example 12-8. A transaction snippet*  *例12-8. 交易处理代码片段*

```java
public void displayTransactionResults(User user, Transaction transaction) {
    ui.showMessage("You bought a " + transaction.getItemName());
    if(user.getBalance() < LOW_BALANCE_THRESHOLD) {
        ui.showMessage("Warning: your balance is low!");
    }
}
```
It wouldn’t be uncommon to find a test covering both of the messages that might be shown by the method, as presented in Example 12-9.

用一个测试同时覆盖这个方法可能显示的两条消息，是很常见的做法，如例12-9所示。

*Example 12-9. A method-driven test*   *例12-9. 方法驱动的测试*

```java
@Test
public void testDisplayTransactionResults() {
transactionProcessor.displayTransactionResults(newUserWithBalance(LOW_BALANCE_THRESHOLD.plus(dollars(2))), new Transaction("Some Item", dollars(3)));
    assertThat(ui.getText()).contains("You bought a Some Item");
    assertThat(ui.getText()).contains("your balance is low");
}

```

With such tests, it’s likely that the test started out covering only the first method. Later, an engineer expanded the test when the second message was added (violating the idea of unchanging tests that we discussed earlier). This modification sets a bad precedent: as the method under test becomes more complex and implements more functionality, its unit test will become increasingly convoluted and grow more and more difficult to work with.

这样的测试很可能最初只覆盖第一个方法。后来添加第二条消息时，工程师又扩充了这个测试，违背了前面所说的“测试应当无需改动”的理念。这开了一个不好的头：随着被测方法日益复杂、功能不断增多，对应的单元测试也会越来越繁杂，越来越难维护。

The problem is that framing tests around methods can naturally encourage unclear tests because a single method often does a few different things under the hood and might have several tricky edge and corner cases. There’s a better way: rather than writing a test for each method, write a test for each behavior.[^4] A behavior is any guarantee that a system makes about how it will respond to a series of inputs while in a particular state.[^5] Behaviors can often be expressed using the words “given,” “when,” and “then”: “Given that a bank account is empty, when attempting to withdraw money from it, then the transaction is rejected.” The mapping between methods and behaviors is many-to-many: most nontrivial methods implement multiple behaviors, and some behaviors rely on the interaction of multiple methods. The previous example can be rewritten using behavior-driven tests, as presented in Example 12-10.

问题在于，围绕方法组织测试，容易让测试变得不清晰：一个方法内部往往做了几件不同的事，还可能涉及多个棘手的边界情况和特殊情况。更好的做法是，不为每个方法写一个测试，而为每个行为写一个测试。行为指系统作出的保证：处于某种状态时，它会如何响应一系列输入。行为通常可以用“给定……，当……，则……”来描述：“给定一个余额为零的银行账户，当尝试从中提款时，则拒绝这笔交易。”方法与行为是多对多关系：多数稍复杂的方法会实现多个行为，而某些行为又依赖多个方法的交互。前面的例子可以改写为行为驱动测试，如例12-10所示。

*Example 12-10. A behavior-driven test*   *例12-10. 行为驱动的测试*

```java
@Test
public void displayTransactionResults_showsItemName() {
    transactionProcessor.displayTransactionResults(new User(), new Transaction("Some Item"));
    assertThat(ui.getText()).contains("You bought a Some Item");
}

@Test
public void displayTransactionResults_showsLowBalanceWarning() {
    transactionProcessor.displayTransactionResults(newUserWithBalance(LOW_BALANCE_THRESHOLD.plus(dollars(2))), new Transaction("Some Item", dollars(3)));
    assertThat(ui.getText()).contains("your balance is low");
}

```

The extra boilerplate required to split apart the single test is more than worth it, and the resulting tests are much clearer than the original test. Behavior-driven tests tend to be clearer than method-oriented tests for several reasons. First, they read more like natural language, allowing them to be naturally understood rather than requiring laborious mental parsing. Second, they more clearly express cause and effect because each test is more limited in scope. Finally, the fact that each test is short and descriptive makes it easier to see what functionality is already tested and encourages engineers to add new streamlined test methods instead of piling onto existing methods.

拆分测试虽然增加了一些样板代码，但完全值得，得到的测试比原来清晰得多。行为驱动测试通常比面向方法的测试更清晰，原因有三。首先，它们读起来更接近自然语言，容易直接理解，不必费力地在脑中解析。其次，每个测试的范围更窄，因此因果关系更明确。最后，测试简短且表意清楚，既方便查看哪些功能已经得到测试，也能促使工程师编写新的精简测试方法，而不是不断往已有方法里堆内容。

> [^4]:	See `https://testing.googleblog.com/2014/04/testing-on-toilet-test-behaviors-not.html` and `https://dannorth.net/introducing-bdd`.
>
> 4 见 `https://testing.googleblog.com/2014/04/testing-on-toilet-test-behaviors-not.html` 和 `https://dannorth.net/introducing-bdd`。
>
> [^5]: Furthermore, a feature (in the product sense of the word) can be expressed as a collection of behaviors.
>
> 5 此外，产品意义上的一项功能，可以表示为一组行为。

#### Structure tests to emphasize behaviors  用测试结构突出行为

Thinking about tests as being coupled to behaviors instead of methods significantly affects how they should be structured. Remember that every behavior has three parts: a “given” component that defines how the system is set up, a “when” component that defines the action to be taken on the system, and a “then” component that validates the result.[^6] Tests are clearest when this structure is explicit. Some frameworks like Cucumber and Spock directly bake in given/when/then. Other languages can use whitespace and optional comments to make the structure stand out, such as that shown in Example 12-11.

让测试对应行为，而不是方法，会显著影响测试的组织方式。每个行为都包含三个部分：“given”定义系统的初始设置，“when”定义对系统执行的操作，“then”验证结果。明确呈现这三个部分，测试才最清晰。Cucumber和Spock等框架直接支持given/when/then结构；使用其他语言时，可以通过空白分隔，必要时再加上注释，突出这一结构，如例12-11所示。

*Example 12-11. A well-structured test*  *例12-11. 一个结构良好的测试*

```java  
@Test
public void transferFundsShouldMoveMoneyBetweenAccounts() {
    // Given two accounts with initial balances of $150 and $20
    Account account1 = newAccountWithBalance(usd(150));
    Account account2 = newAccountWithBalance(usd(20));
    // When transferring $100 from the first to the second account
    bank.transferFunds(account1, account2, usd(100));
    // Then the new account balances should reflect the transfer 
    assertThat(account1.getBalance()).isEqualTo(usd(50));
    assertThat(account2.getBalance()).isEqualTo(usd(120));
}

```

This level of description isn’t always necessary in trivial tests, and it’s usually sufficient to omit the comments and rely on whitespace to make the sections clear. However, explicit comments can make more sophisticated tests easier to understand. This pattern makes it possible to read tests at three levels of granularity:

1. A reader can start by looking at the test method name (discussed below) to get a rough description of the behavior being tested.
2. If that’s not enough, the reader can look at the given/when/then comments for a formal description of the behavior.
3. Finally, a reader can look at the actual code to see precisely how that behavior is expressed.

简单测试不一定需要这么详细的描述，通常省去注释、只用空白分隔各部分就够了。但对于复杂测试，明确的注释有助于理解。采用这种模式，可以从三个层次阅读测试：

1. 先看测试方法名（下文会讨论），大致了解被测行为。
2. 如果还不够，再看given/when/then注释，了解对行为的正式描述。
3. 最后查看具体代码，准确理解这一行为是如何表达的。

This pattern is most commonly violated by interspersing assertions among multiple calls to the system under test (i.e., combining the “when” and “then” blocks). Merging the “then” and “when” blocks in this way can make the test less clear because it makes it difficult to distinguish the action being performed from the expected result.

最常见的反例，是在对被测系统的多次调用之间穿插断言，也就是把“when”和“then”块混在一起。这样合并“then”和“when”块，会让人难以区分执行的操作与预期结果，从而降低测试的清晰度。

When a test does want to validate each step in a multistep process, it’s acceptable to define alternating sequences of when/then blocks. Long blocks can also be made more descriptive by splitting them up with the word “and.” Example 12-12 shows what a relatively complex, behavior-driven test might look like.

如果测试确实需要逐步验证一个多步骤过程，可以交替编排when/then块。对于较长的块，也可以用“and”分隔，使各部分的含义更清楚。例12-12展示了一个相对复杂的行为驱动测试。

*Example 12-12. Alternating when/then blocks within a test*   *例12-12. 在一个测试中交替使用when/then块*

```java
@Test
public void shouldTimeOutConnections() {
    // Given two users
    User user1 = newUser();
    User user2 = newUser();
    // And an empty connection pool with a 10-minute timeout
    Pool pool = newPool(Duration.minutes(10));
    // When connecting both users to the pool
    pool.connect(user1);
    pool.connect(user2);
    // Then the pool should have two connections
    assertThat(pool.getConnections()).hasSize(2);
    // When waiting for 20 minutes
    clock.advance(Duration.minutes(20));
    // Then the pool should have no connections
    assertThat(pool.getConnections()).isEmpty();
    // And each user should be disconnected 
    assertThat(user1.isConnected()).isFalse();
    assertThat(user2.isConnected()).isFalse();
}

```

When writing such tests, be careful to ensure that you’re not inadvertently testing multiple behaviors at the same time. Each test should cover only a single behavior, and the vast majority of unit tests require only one “when” and one “then” block.

编写这类测试时，要小心，不要无意间同时测试多个行为。每个测试应只覆盖一个行为，绝大多数单元测试只需一个“when”块和一个“then”块。

> [^6]: These components are sometimes referred to as “arrange,” “act,” and “assert.”
>
> 6 这三个部分有时也称为“准备”“执行”和“断言”。

#### Name tests after the behavior being tested  以被测试的行为命名测试

Method-oriented tests are usually named after the method being tested (e.g., a test for the updateBalance method is usually called testUpdateBalance). With more focused behavior-driven tests, we have a lot more flexibility and the chance to convey useful information in the test’s name. The test name is very important: it will often be the first or only token visible in failure reports, so it’s your best opportunity to communicate the problem when the test breaks. It’s also the most straightforward way to express the intent of the test.

面向方法的测试通常以被测方法命名，例如，测试 updateBalance 方法时，测试名通常是 testUpdateBalance。行为驱动测试更聚焦，命名也更灵活，可以在名称中传达更多有用信息。测试名很重要：它往往是失败报告中首先出现、甚至唯一可见的标识，因此也是测试失败时说明问题的最佳机会。同时，它还是表达测试意图最直接的方式。

A test’s name should summarize the behavior it is testing. A good name describes both the actions that are being taken on a system and the expected outcome. Test names will sometimes include additional information like the state of the system or its environment before taking action on it. Some languages and frameworks make this easier than others by allowing tests to be nested within one another and named using strings, such as in Example 12-13, which uses Jasmine.

测试名应概括所测试的行为。好的名称既说明对系统执行了什么操作，也说明预期结果是什么，有时还会交代操作前系统或环境的状态。有些语言和框架允许嵌套测试，并用字符串命名，因此更容易表达这些信息。例12-13使用Jasmine展示了这种方式。

*Example 12-13. Some sample nested naming patterns*  *例12-13. 嵌套命名模式示例*

```java
describe("multiplication", function() {
    describe("with a positive number", function() {
        var positiveNumber = 10;
        it("is positive with another positive number", function() {
            expect(positiveNumber * 10).toBeGreaterThan(0);
        });
        it("is negative with a negative number", function() {
            expect(positiveNumber * -10).toBeLessThan(0);
        });
    });
    describe("with a negative number", function() {
        var negativeNumber = 10;
        it("is negative with a positive number", function() {
            expect(negativeNumber * 10).toBeLessThan(0);
        });
        it("is positive with another negative number", function() {
            expect(negativeNumber * -10).toBeGreaterThan(0);
        });
    });
});

```

Other languages require us to encode all of this information in a method name, leading to method naming patterns like that shown in Example 12-14.

使用其他语言时，则需要把这些信息全部写进方法名，于是就有了例12-14所示的命名方式。

*Example 12-14. Some sample method naming patterns*  例12-14. 方法命名模式示例

```Java
multiplyingTwoPositiveNumbersShouldReturnAPositiveNumber 
multiply_postiveAndNegative_returnsNegative 
divide_byZero_throwsException
````

Names like this are much more verbose than we’d normally want to write for methods in production code, but the use case is different: we never need to write code that calls these, and their names frequently need to be read by humans in reports. Hence, the extra verbosity is warranted.

这样的名称，比生产代码中通常采用的方法名长得多，但使用场景不同：我们无须编写代码来调用这些测试方法，却经常要在报告中阅读它们的名称。因此，多写一些描述是合理的。

Many different naming strategies are acceptable so long as they’re used consistently within a single test class. A good trick if you’re stuck is to try starting the test name with the word “should.” When taken with the name of the class being tested, this naming scheme allows the test name to be read as a sentence. For example, a test of a BankAccount class named shouldNotAllowWithdrawalsWhenBalanceIsEmpty can be read as “BankAccount should not allow withdrawals when balance is empty.” By reading the names of all the test methods in a suite, you should get a good sense of the behaviors implemented by the system under test. Such names also help ensure that the test stays focused on a single behavior: if you need to use the word “and” in a test name, there’s a good chance that you’re actually testing multiple behaviors and should be writing multiple tests!

只要在同一个测试类中保持一致，多种命名策略都可以接受。如果想不出合适的名称，可以试着用表示“应当”的词开头。这样，测试名与被测类名连起来，就能读成一句话。例如，BankAccount类有一个名为shouldNotAllowWithdrawalsWhenBalanceIsEmpty的测试，可以读作“BankAccount不应允许在余额为零时提款”。读完一个套件中所有测试方法的名称，就应能较好地了解被测系统实现了哪些行为。这种命名也有助于让测试专注于单一行为：如果测试名中需要用到“and”，很可能说明你在测试多个行为，应该拆成多个测试！

### Don’t Put Logic in Tests  不要在测试中放入逻辑

Clear tests are trivially correct upon inspection; that is, it is obvious that a test is doing the correct thing just from glancing at it. This is possible in test code because each test needs to handle only a particular set of inputs, whereas production code must be generalized to handle any input. For production code, we’re able to write tests that ensure complex logic is correct. But test code doesn’t have that luxury—if you feel like you need to write a test to verify your test, something has gone wrong!

清晰的测试，其正确性应当一目了然，也就是扫一眼便知道它做对了。测试代码能做到这一点，是因为每个测试只需处理一组特定输入，而生产代码必须具备通用性，能够处理各种输入。生产代码有复杂逻辑时，可以编写测试来验证；测试代码却不能再依靠同样的办法。如果你觉得还需要写一个测试来验证测试本身，就说明已经出了问题！

Complexity is most often introduced in the form of logic. Logic is defined via the imperative parts of programming languages such as operators, loops, and conditionals. When a piece of code contains logic, you need to do a bit of mental computation to determine its result instead of just reading it off of the screen. It doesn’t take much logic to make a test more difficult to reason about. For example, does the test in Example 12-15 look correct to you?

复杂性最常通过逻辑引入。这里的逻辑，指由编程语言中的运算符、循环和条件分支等命令式构造表达的计算。代码一旦包含逻辑，就不能直接从屏幕上读出结果，而需要在脑中推算。即使只有一点逻辑，也会增加理解测试的难度。例如，你觉得例12-15中的测试正确吗？

*Example 12-15. Logic concealing a bug*  *例12-15. 掩盖bug的逻辑*

```java
@Test
public void shouldNavigateToAlbumsPage() {
    String baseUrl = "http://photos.google.com/";
    Navigator nav = new Navigator(baseUrl);
    nav.goToAlbumPage();
    assertThat(nav.getCurrentUrl()).isEqualTo(baseUrl + "/albums");
}
```

There’s not much logic here: really just one string concatenation. But if we simplify the test by removing that one bit of logic, a bug immediately becomes clear, as demonstrated in Example 12-16.

这里的逻辑很少，实际上只有一次字符串拼接。但去掉这点逻辑、简化测试后，一个缺陷就立刻显现出来，如例12-16所示。

*Example 12-16. A test without logic reveals the bug*  *例12-16. 没有逻辑的测试揭示了bug*

```java
@Test
public void shouldNavigateToPhotosPage() {
    Navigator nav = new Navigator("http://photos.google.com/");
    nav.goToPhotosPage();
    assertThat(nav.getCurrentUrl())).isEqualTo("http://photos.google.com//albums"); // Oops!
}
```

When the whole string is written out, we can see right away that we’re expecting two slashes in the URL instead of just one. If the production code made a similar mistake, this test would fail to detect a bug. Duplicating the base URL was a small price to pay for making the test more descriptive and meaningful (see the discussion of DAMP versus DRY tests later in this chapter).

把整个字符串写出来，就能立刻看出，测试期望的URL中有两个斜杠，而不是一个。如果生产代码也犯了类似错误，这个测试就发现不了。为了让测试更清楚地表达含义，重复写出基础URL只是很小的代价，参见本章后面对DAMP与DRY测试的讨论。

If humans are bad at spotting bugs from string concatenation, we’re even worse at spotting bugs that come from more sophisticated programming constructs like loops and conditionals. The lesson is clear: in test code, stick to straight-line code over clever logic, and consider tolerating some duplication when it makes the test more descriptive and meaningful. We’ll discuss ideas around duplication and code sharing later in this chapter.

人不擅长发现字符串拼接中的缺陷，就更不擅长发现循环、条件分支等复杂编程结构中的缺陷。因此，测试代码应优先采用顺序执行的直白代码，而不是巧妙的逻辑；只要能让测试更清楚地表达含义，就可以考虑容忍一些重复。本章后面还会讨论重复与代码共享。

### Write Clear Failure Messages  给出清晰的失败信息

One last aspect of clarity has to do not with how a test is written, but with what an engineer sees when it fails. In an ideal world, an engineer could diagnose a problem just from reading its failure message in a log or report without ever having to look at the test itself. A good failure message contains much the same information as the test’s name: it should clearly express the desired outcome, the actual outcome, and any relevant parameters.

清晰度的最后一个方面，不在于测试怎样编写，而在于失败时工程师能看到什么。理想情况下，只看日志或报告中的失败信息，就能诊断问题，无须再查看测试本身。好的失败信息与好的测试名应包含大致相同的信息：清楚说明预期结果、实际结果，以及所有相关参数。

Here’s an example of a bad failure message:

下面是一条不够清晰的失败信息：

```Java
Test failed: account is closed
```

Did the test fail because the account was closed, or was the account expected to be closed and the test failed because it wasn’t? A better failure message clearly distinguishes the expected from the actual state and gives more context about the result:

测试究竟是因为账户已关闭而失败，还是原本期望账户已关闭，却发现它仍未关闭？更好的失败信息会明确区分预期状态和实际状态，并提供更多结果相关的上下文：

```java
Expected an account in state CLOSED, but got account:
<{name: "my-account", state: "OPEN"}
```

Good libraries can help make it easier to write useful failure messages. Consider the assertions in Example 12-17 in a Java test, the first of which uses classical JUnit asserts, and the second of which uses Truth, an assertion library developed by Google:

好的库能帮助我们更容易地写出有用的失败信息。来看例12-17中的Java测试断言：第一个使用传统的JUnit断言，第二个使用Google开发的断言库Truth：

*Example 12-17. An assertion using the Truth library*   *例12-17.  使用Truth库的断言*

```java
Set<String> colors = ImmutableSet.of("red", "green", "blue"); 
assertTrue(colors.contains("orange")); // JUnit 
assertThat(colors).contains("orange"); // Truth
```

Because the first assertion only receives a Boolean value, it is only able to give a generic error message like “expected `true` but was `false`,” which isn’t very informative in a failing test output. Because the second assertion explicitly receives the subject of the assertion, it is able to give a much more useful error message: AssertionError: <[red, green, blue]> should have contained `orange`.”

第一个断言只接收布尔值，因此只能给出“预期为`true`，实际为`false`”之类的通用错误信息，对排查测试失败帮助不大。第二个断言直接接收被断言的对象，因此能给出更有用的错误信息：“AssertionError: <[red, green, blue]>应当包含`orange`”。

Not all languages have such helpers available, but it should always be possible to manually specify the important information in the failure message. For example, test assertions in Go conventionally look like Example 12-18.

并非所有语言都有这样的辅助工具，但总可以手动把关键信息写进失败信息。例如，Go中的测试断言通常采用例12-18所示的形式。

*Example 12-18. A test assertion in Go*   *例12-18. Go中的测试断言*

```golang
result: = Add(2, 3)
if result != 5 {
    t.Errorf("Add(2, 3) = %v, want %v", result, 5)
}
```

## Tests and Code Sharing: DAMP, Not DRY  测试和代码共享：DAMP，而不是DRY

One final aspect of writing clear tests and avoiding brittleness has to do with code sharing. Most software attempts to achieve a principle called DRY—“Don’t Repeat Yourself.” DRY states that software is easier to maintain if every concept is canonically represented in one place and code duplication is kept to a minimum. This approach is especially valuable in making changes easier because an engineer needs to update only one piece of code rather than tracking down multiple references. The downside to such consolidation is that it can make code unclear, requiring readers to follow chains of references to understand what the code is doing.

要编写清晰且不脆弱的测试，最后还要考虑代码共享。大多数软件都力求遵循DRY原则，也就是“不要重复自己”。按照DRY原则，如果每个概念都只有一处权威表示，并尽量减少重复代码，软件就会更容易维护。这尤其有助于简化变更：工程师只需更新一处代码，无须追踪多处引用。但集中代码也有代价：读者可能必须沿着一连串引用查找，才能弄清代码在做什么，从而降低代码的清晰度。

In normal production code, that downside is usually a small price to pay for making code easier to change and work with. But this cost/benefit analysis plays out a little differently in the context of test code. Good tests are designed to be stable, and in fact you usually want them to break when the system being tested changes. So DRY doesn’t have quite as much benefit when it comes to test code. At the same time, the costs of complexity are greater for tests: production code has the benefit of a test suite to ensure that it keeps working as it becomes complex, whereas tests must stand by themselves, risking bugs if they aren’t self-evidently correct. As mentioned earlier, something has gone wrong if tests start becoming complex enough that it feels like they need their own tests to ensure that they’re working properly.

对于一般的生产代码，为了让代码更易修改和使用，这点代价通常不大。但对测试代码，成本与收益的权衡有所不同。好的测试应当保持稳定；事实上，当被测系统发生变化时，通常正是希望测试能够失败。因此，DRY给测试代码带来的收益没有那么大。同时，复杂性在测试中的代价更高：生产代码变复杂时，还有测试套件保证它继续正常工作；测试本身却只能靠自己，如果不能一眼看出是否正确，就可能藏有缺陷。如前所述，如果测试复杂到似乎还需要另一套测试来验证其正确性，就说明出了问题。

Instead of being completely DRY, test code should often strive to be DAMP—that is, to promote “Descriptive And Meaningful Phrases.” A little bit of duplication is OK in tests so long as that duplication makes the test simpler and clearer. To illustrate, Example 12-19 presents some tests that are far too DRY.

测试代码通常不应一味追求DRY，而应力求DAMP，也就是采用“描述清楚、含义明确的表达”。只要能让测试更简单、更清晰，少量重复完全可以接受。例12-19展示了一些过于追求DRY的测试。

*Example 12-19. A test that is too DRY*   *例12-19. 一个过于DRY的测试*

```java
@Test
public void shouldAllowMultipleUsers() {
    List < User > users = createUsers(false, false);
    Forum forum = createForumAndRegisterUsers(users);
    validateForumAndUsers(forum, users);
}

@Test
public void shouldNotAllowBannedUsers() {
        List < User > users = createUsers(true);
        Forum forum = createForumAndRegisterUsers(users);
        validateForumAndUsers(forum, users);
}

// Lots more tests...
private static List < User > createUsers(boolean...banned) {
    List < User > users = new ArrayList < > ();
    for(boolean isBanned: banned) {
        users.add(newUser().setState(isBanned ? State.BANNED : State.NORMAL).build());
    }
    return users;
}

private static Forum createForumAndRegisterUsers(List < User > users) {
    Forum forum = new Forum();
    for(User user: users) {
        try {
            forum.register(user);
        } catch(BannedUserException ignored) {}
    }
    return forum;
}

private static void validateForumAndUsers(Forum forum, List < User > users) {
    assertThat(forum.isReachable()).isTrue();
    for(User user: users) {
        assertThat(forum.hasRegisteredUser(user)).isEqualTo(user.getState() == State.BANNED);
    }
}
```

The problems in this code should be apparent based on the previous discussion of clarity. For one, although the test bodies are very concise, they are not complete: important details are hidden away in helper methods that the reader can’t see without having to scroll to a completely different part of the file. Those helpers are also full of logic that makes them more difficult to verify at a glance (did you spot the bug?). The test becomes much clearer when it’s rewritten to use DAMP, as shown in Example 12-20.

根据前面对清晰度的讨论，这段代码的问题应该不难发现。首先，测试主体虽然简洁，却不完整：重要细节藏在辅助方法中，读者必须滚动到文件的另一处才能看到。辅助方法里又充满逻辑，难以一眼确认是否正确。你发现其中的缺陷了吗？按照DAMP原则改写后，测试就清晰多了，如例12-20所示。

*Example 12-20. Tests should be DAMP*   *例12-20. 测试应遵循DAMP*

```java  
@Test
public void shouldAllowMultipleUsers() {
    User user1 = newUser().setState(State.NORMAL).build();
    User user2 = newUser().setState(State.NORMAL).build();

    Forum forum = new Forum();
    forum.register(user1);
    forum.register(user2);

    assertThat(forum.hasRegisteredUser(user1)).isTrue();
    assertThat(forum.hasRegisteredUser(user2)).isTrue();
}

@Test
public void shouldNotRegisterBannedUsers() {
    User user = newUser().setState(State.BANNED).build();

    Forum forum = new Forum();
    try {
        forum.register(user);
    } catch(BannedUserException ignored) {}

    assertThat(forum.hasRegisteredUser(user)).isFalse();
}
```

These tests have more duplication, and the test bodies are a bit longer, but the extra verbosity is worth it. Each individual test is far more meaningful and can be understood entirely without leaving the test body. A reader of these tests can feel confident that the tests do what they claim to do and aren’t hiding any bugs.

这些测试的重复更多，主体也稍长，但增加的代码值得。每个测试的含义都清楚得多，只看测试主体就能完整理解。读者可以确信，这些测试确实验证了它们声称要验证的内容，没有暗藏bug。

DAMP is not a replacement for DRY; it is complementary to it. Helper methods and test infrastructure can still help make tests clearer by making them more concise, factoring out repetitive steps whose details aren’t relevant to the particular behavior being tested. The important point is that such refactoring should be done with an eye toward making tests more descriptive and meaningful, and not solely in the name of reducing repetition. The rest of this section will explore common patterns for sharing code across tests.

DAMP并不取代DRY，而是对DRY的补充。辅助方法和测试基础设施仍然有用：把重复且细节与当前被测行为无关的步骤提取出去，可以让测试更简洁、更清晰。关键在于，重构应以更清楚地表达测试含义为目标，而不只是为了减少重复。本节接下来将介绍在测试之间共享代码的常见模式。

### Shared  Values  共享值

Many tests are structured by defining a set of shared values to be used by tests and then by defining the tests that cover various cases for how these values interact. Example 12-21 illustrates what such tests look like.

许多测试会先定义一组共享值，再编写测试，覆盖这些值在各种情况下如何交互。例12-21展示了这种组织方式。

*Example 12-21. Shared values with ambiguous names*  *例12-21. 名称不明确的共享值*

```java
private static final Account ACCOUNT_1 = Account.newBuilder()
    .setState(AccountState.OPEN).setBalance(50).build();

private static final Account ACCOUNT_2 = Account.newBuilder()
    .setState(AccountState.CLOSED).setBalance(0).build();

private static final Item ITEM = Item.newBuilder()
    .setName("Cheeseburger").setPrice(100).build();

// Hundreds of lines of other tests...

@Test
public void canBuyItem_returnsFalseForClosedAccounts() {
    assertThat(store.canBuyItem(ITEM, ACCOUNT_1)).isFalse();
}

@Test
public void canBuyItem_returnsFalseWhenBalanceInsufficient() {
    assertThat(store.canBuyItem(ITEM, ACCOUNT_2)).isFalse();
}
```

This strategy can make tests very concise, but it causes problems as the test suite grows. For one, it can be difficult to understand why a particular value was chosen for a test. In Example 12-21, the test names fortunately clarify which scenarios are being tested, but you still need to scroll up to the definitions to confirm that ACCOUNT_1 and ACCOUNT_2 are appropriate for those scenarios. More descriptive constant names (e.g.,CLOSED_ACCOUNT and ACCOUNT_WITH_LOW_BALANCE) help a bit, but they still make it more difficult to see the exact details of the value being tested, and the ease of reusing these values can encourage engineers to do so even when the name doesn’t exactly describe what the test needs.

这种策略能让测试非常简洁，但随着测试套件扩大，就会出现问题。首先，读者可能很难理解，测试为什么选择某个特定值。例12-21中的测试名还算清楚，说明了所测场景，但仍需向上翻到定义处，才能确认ACCOUNT_1和ACCOUNT_2是否适合这些场景。换成更具描述性的常量名，例如CLOSED_ACCOUNT 和 ACCOUNT_WITH_LOW_BALANCE，会有所帮助，但读者仍然不容易看清测试值的具体细节。而且，复用这些值太方便，也会促使工程师继续复用，即使名称并不能准确表达测试所需的值。

Engineers are usually drawn to using shared constants because constructing individual values in each test can be verbose. A better way to accomplish this goal is to construct data using helper methods (see Example 12-22) that require the test author to specify only values they care about, and setting reasonable defaults7 for all other values. This construction is trivial to do in languages that support named parameters, but languages without named parameters can use constructs such as the Builder pattern to emulate them (often with the assistance of tools such as AutoValue):

工程师倾向于使用共享常量，通常是因为在每个测试里单独构造值需要写很多代码。更好的做法是通过辅助方法构造数据（见例12-22）：测试作者只需指定自己关心的值，其余值都采用合理的默认值。支持命名参数的语言很容易做到这一点；不支持的语言，也可以通过构建器模式等方式模拟，通常还能借助AutoValue等工具：

*Example 12-22. Shared values using helper methods*   *例12-22. 使用辅助方法的共享值*

```java
# A helper method wraps a constructor by defining arbitrary defaults for 
# each of its parameters.
def newContact(
        firstName = "Grace", lastName = "Hopper", phoneNumber = "555-123-4567"):
    return Contact(firstName, lastName, phoneNumber)

# Tests call the helper, specifying values for only the parameters that they
# care about.
def test_fullNameShouldCombineFirstAndLastNames(self):
    def contact = newContact(firstName = "Ada", lastName = "Lovelace") self.assertEqual(contact.fullName(), "Ada Lovelace")

// Languages like Java that don’t support named parameters can emulate them
// by returning a mutable "builder" object that represents the value under
// construction.
private static Contact.Builder newContact() {
    return Contact.newBuilder()
        .setFirstName("Grace")
        .setLastName("Hopper")
        .setPhoneNumber("555-123-4567");
}

// Tests then call methods on the builder to overwrite only the parameters
// that they care about, then call build() to get a real value out of the
// builder. @Test
public void fullNameShouldCombineFirstAndLastNames() {
    Contact contact = newContact()
        .setFirstName("Ada").setLastName("Lovelace")
        .build();
    assertThat(contact.getFullName()).isEqualTo("Ada Lovelace");
}
```

Using helper methods to construct these values allows each test to create the exact values it needs without having to worry about specifying irrelevant information or conflicting with other tests.

通过辅助方法构造值，每个测试都能创建恰好符合自身需要的数据，无须指定无关信息，也不必担心与其他测试冲突。

> [^7]: In many cases, it can even be useful to slightly randomize the default values returned for fields that aren’t explicitly set. This helps to ensure that two different instances won’t accidentally compare as equal, and makes it more difficult for engineers to hardcode dependencies on the defaults.
>
> 7 在许多情况下，对未显式设置的字段所返回的默认值作少量随机化，甚至也有帮助。这样有助于避免两个不同实例在比较时意外相等，也能让工程师更难通过硬编码来依赖这些默认值。

### Shared Setup  共享初始化

A related way that tests shared code is via setup/initialization logic. Many test frameworks allow engineers to define methods to execute before each test in a suite is run. Used appropriately, these methods can make tests clearer and more concise by obviating the repetition of tedious and irrelevant initialization logic. Used inappropriately, these methods can harm a test’s completeness by hiding important details in a separate initialization method.

另一种相关的代码共享方式，是复用准备或初始化逻辑。许多测试框架允许定义在套件中每个测试运行前执行的方法。用得恰当，就能免去重复、繁琐且无关的初始化逻辑，让测试更清晰、更简洁；用得不当，则会把重要细节藏进单独的初始化方法，破坏测试的完整性。

The best use case for setup methods is to construct the object under tests and its collaborators. This is useful when the majority of tests don’t care about the specific arguments used to construct those objects and can let them stay in their default states. The same idea also applies to stubbing return values for test doubles, which is a concept that we explore in more detail in Chapter 13.

初始化方法最适合用来构造被测对象及其协作对象。如果大多数测试不关心构造这些对象的具体参数，也允许它们保持默认状态，这种做法就很有用。同样的思路也适用于为测试替身预设返回值，也就是打桩；第13章会详细介绍这一概念。

One risk in using setup methods is that they can lead to unclear tests if those tests begin to depend on the particular values used in setup. For example, the test in Example 12-23 seems incomplete because a reader of the test needs to go hunting to discover where the string “Donald Knuth” came from.

初始化方法有一个风险：如果测试开始依赖初始化时使用的特定值，就可能变得不清晰。例如，例12-23中的测试显得不完整，因为读者必须到别处寻找字符串“Donald Knuth”的来源。

*Example 12-23. Dependencies on values in setup methods*   *例12-23. 依赖初始化方法中的值*

```java
private NameService nameService;
private UserStore userStore;

@Before
public void setUp() {
    nameService = new NameService();
    nameService.set("user1", "Donald Knuth");
    userStore = new UserStore(nameService);
}

// [... hundreds of lines of tests ...]

@Test
public void shouldReturnNameFromService() {
    UserDetails user = userStore.get("user1");
    assertThat(user.getName()).isEqualTo("Donald Knuth");
}
```

Tests like these that explicitly care about particular values should state those values directly, overriding the default defined in the setup method if need be. The resulting test contains slightly more repetition, as shown in Example 12-24, but the result is far more descriptive and meaningful.

如果测试明确关心某些特定值，就应直接写出这些值，必要时覆盖setup方法中定义的默认值。这样虽会增加少量重复，却能更清楚地表达测试含义，如例12-24所示。

*Example 12-24. Overriding values in setup Methods*   *例12-24. 覆盖初始化方法中的值*

```java
private NameService nameService;
private UserStore userStore;

@Before
public void setUp() {
    nameService = new NameService();
    nameService.set("user1", "Donald Knuth");
    userStore = new UserStore(nameService);
}

@Test
public void shouldReturnNameFromService() {
    nameService.set("user1", "Margaret Hamilton");
    UserDetails user = userStore.get("user1");
    assertThat(user.getName()).isEqualTo("Margaret Hamilton");
}
```

### Shared  Helpers  and  Validation  共享辅助方法和验证

The last common way that code is shared across tests is via “helper methods” called from the body of the test methods. We already discussed how helper methods can be a useful way for concisely constructing test values—this usage is warranted, but other types of helper methods can be dangerous.

最后一种常见的共享方式，是在测试方法主体中调用“辅助方法”。前面已经介绍，用辅助方法简洁地构造测试值，是合理的做法；但其他类型的辅助方法可能带来风险。

One common type of helper is a method that performs a common set of assertions against a system under test. The extreme example is a validate method called at the end of every test method, which performs a set of fixed checks against the system under test. Such a validation strategy can be a bad habit to get into because tests using this approach are less behavior driven. With such tests, it is much more difficult to determine the intent of any particular test and to infer what exact case the author had in mind when writing it. When bugs are introduced, this strategy can also make them more difficult to localize because they will frequently cause a large number of tests to start failing.

一类常见的辅助方法，会对被测系统执行一组共用断言。极端情况下，每个测试方法最后都会调用同一个验证方法，对系统执行一组固定检查。这种策略容易形成坏习惯，因为测试会偏离以行为为中心的组织方式。读者更难判断某个测试的意图，也更难推断作者当时具体考虑了什么场景。引入bug时，这种策略还会增加定位难度，因为一处缺陷往往就会导致大量测试失败。

More focused validation methods can still be useful, however. The best validation helper methods assert a single conceptual fact about their inputs, in contrast to general-purpose validation methods that cover a range of conditions. Such methods can be particularly helpful when the condition that they are validating is conceptually simple but requires looping or conditional logic to implement that would reduce clarity were it included in the body of a test method. For example, the helper method in Example 12-25 might be useful in a test covering several different cases around account access.

不过，更聚焦的验证方法仍然有用。好的验证辅助方法，应只针对输入断言一个概念上的事实，而不是像通用验证方法那样检查一系列条件。如果所验证的条件概念简单，实现时却需要循环或条件分支，把逻辑直接放进测试主体又会降低清晰度，这样的辅助方法就尤其有用。例如，在覆盖账户访问的几种不同情况的测试中，例12-25所示的辅助方法可能很有帮助。

*Example 12-25. A conceptually simple test*   *例12-25. 概念上简单的测试*

```java
private void assertUserHasAccessToAccount(User user, Account account) {
    for(long userId: account.getUsersWithAccess()) {
        if(user.getId() == userId) {
            return;
        }
    }
    fail(user.getName() + " cannot access " + account.getName());
}
```

### Defining Test Infrastructure  定义测试基础设施

The techniques we’ve discussed so far cover sharing code across methods in a single test class or suite. Sometimes, it can also be valuable to share code across multiple test suites. We refer to this sort of code as test infrastructure. Though it is usually more valuable in integration or end-to-end tests, carefully designed test infrastructure can make unit tests much easier to write in some circumstances.

目前讨论的技巧，都是在同一个测试类或套件的不同方法之间共享代码。有时，在多个测试套件之间共享代码也很有价值，我们把这类代码称为测试基础设施。它通常在集成测试或端到端测试中更有用，但设计得当时，也能在某些情况下大幅降低单元测试的编写难度。

Custom test infrastructure must be approached more carefully than the code sharing that happens within a single test suite. In many ways, test infrastructure code is more similar to production code than it is to other test code given that it can have many callers that depend on it and can be difficult to change without introducing breakages. Most engineers aren’t expected to make changes to the common test infrastructure while testing their own features. Test infrastructure needs to be treated as its own separate product, and accordingly, test infrastructure must always have its own tests.

相比单个测试套件内的代码共享，自定义测试基础设施需要更谨慎地设计和维护。它可能有许多依赖它的调用方，修改时又很难避免破坏现有用法，因此在很多方面更接近生产代码，而不是其他测试代码。通常不应要求工程师在测试自己的功能时，还得修改共用的测试基础设施。应当把测试基础设施视为独立产品，因此，它也必须始终配备自己的测试。

Of course, most of the test infrastructure that most engineers use comes in the form of well-known third-party libraries like JUnit. A huge number of such libraries are available, and standardizing on them within an organization should happen as early and universally as possible. For example, Google many years ago mandated Mockito as the only mocking framework that should be used in new Java tests and banned new tests from using other mocking frameworks. This edict produced some grumbling at the time from people comfortable with other frameworks, but today, it’s universally seen as a good move that made our tests easier to understand and work with.

当然，多数工程师使用的测试基础设施，主要是JUnit等知名第三方库。这类库选择很多，组织应尽早、尽可能全面地统一选型。例如，Google多年前就规定，新增Java测试只能使用Mockito作为模拟框架，不得使用其他模拟框架。当时，一些习惯了其他框架的人颇有怨言；但如今，大家普遍认为这是正确的决定，让测试更容易理解和维护。

## Conclusion 总结

Unit tests are one of the most powerful tools that we as software engineers have to make sure that our systems keep working over time in the face of unanticipated changes. But with great power comes great responsibility, and careless use of unit testing can result in a system that requires much more effort to maintain and takes much more effort to change without actually improving our confidence in said system.

单元测试是软件工程师最强大的工具之一，能帮助我们确保系统在长期演进、面对意外变更时仍然正常工作。但能力越强，责任也越大。单元测试使用不当，可能让系统的维护和修改都费力得多，却没有真正增强我们对系统的信心。

Unit tests at Google are far from perfect, but we’ve found tests that follow the practices outlined in this chapter to be orders of magnitude more valuable than those that don’t. We hope they’ll help you to improve the quality of your own tests!

谷歌的单元测试远非完美，但我们发现，遵循本章实践的测试，其价值比不遵循的测试高出几个数量级。希望这些做法也能帮助你提高测试质量！

## TL;DRs  内容提要

- Strive for unchanging tests.

- Test via public APIs.

- Test state, not interactions.

- Make your tests complete and concise.

- Test behaviors, not methods.

- Structure tests to emphasize behaviors.

- Name tests after the behavior being tested.

- Don’t put logic in tests.

- Write clear failure messages.

- Follow DAMP over DRY when sharing code for tests.

- 力求让测试无需改动。

- 通过公共API进行测试。

- 测试状态，而不是交互。

- 让测试完整且简洁。

- 测试行为，而不是方法。

- 用测试结构突出行为。

- 以被测行为命名测试。

- 不要把逻辑放在测试中。

- 编写清晰的失败信息。

- 共享测试代码时，优先遵循DAMP，而不是DRY。
