
**CHAPTER 13**

# Test Doubles

# 第十三章 测试替身

**Written by Andrew Trenk and Dillon Bly**

**Edited by Tom Manshreck**

Unit tests are a critical tool for keeping developers productive and reducing defects in code. Although they can be easy to write for simple code, writing them becomes difficult as code becomes more complex.

单元测试是保障开发者生产力、减少代码缺陷的重要工具。代码简单时，单元测试可能很容易编写；但随着代码变得复杂，编写单元测试也会更加困难。

For example, imagine trying to write a test for a function that sends a request to an external server and then stores the response in a database. Writing a handful of tests might be doable with some effort. But if you need to write hundreds or thousands of tests like this, your test suite will likely take hours to run, and could become flaky due to issues like random network failures or tests overwriting one another’s data.

例如，假设要为这样一个函数编写测试：它向外部服务器发送请求，再把响应存入数据库。花些工夫，也许能写出几个测试。但如果需要编写成百上千个这样的测试，整个测试套件可能要运行数小时，还可能因随机网络故障、测试相互覆盖数据等问题而变得不稳定。

Test doubles come in handy in such cases. A test double is an object or function that can stand in for a real implementation in a test, similar to how a stunt double can stand in for an actor in a movie. The use of test doubles is often referred to as mocking, but we avoid that term in this chapter because, as we’ll see, that term is also used to refer to more specific aspects of test doubles.

这时，测试替身就能派上用场。测试替身是在测试中代替真实实现的对象或函数，就像电影中的特技替身代替演员一样。使用测试替身常被称为 mocking，但本章避免用这个术语统称这类做法，因为后文会看到，它也用来指测试替身的某些更具体的用法。

Perhaps the most obvious type of test double is a simpler implementation of an object that behaves similarly to the real implementation, such as an in-memory database. Other types of test doubles can make it possible to validate specific details of your system, such as by making it easy to trigger a rare error condition, or ensuring a heavyweight function is called without actually executing the function’s implementation.

最容易想到的一类测试替身，也许就是对象的简化实现：行为与真实实现相似，例如内存数据库。其他类型的测试替身则便于验证系统的特定细节，例如更容易地触发罕见错误，或在不实际执行某个开销很大的函数的情况下，确认代码确实调用了它。

The previous two chapters introduced the concept of small tests and discussed why they should comprise the majority of tests in a test suite. However, production code often doesn’t fit within the constraints of small tests due to communication across multiple processes or machines. Test doubles can be much more lightweight than real implementations, allowing you to write many small tests that execute quickly and are not flaky.

前两章介绍了小型测试的概念，并讨论了为什么测试套件应以小型测试为主。然而，生产代码往往需要跨进程或跨机器通信，无法满足小型测试的约束。测试替身可以比真实实现轻量得多，让你能够编写大量运行迅速、结果稳定的小型测试。

## The Impact of Test Doubles on Software Development  测试替身对软件开发的影响

The use of test doubles introduces a few complications to software development that require some trade-offs to be made. The concepts introduced here are discussed in more depth throughout this chapter:

*Testability*  
    To use test doubles, a codebase needs to be designed to be testable—it should be possible for tests to swap out real implementations with test doubles. For example, code that calls a database needs to be flexible enough to be able to use a test double in place of a real database. If the codebase isn’t designed with testing in mind and you later decide that tests are needed, it can require a major commitment to refactor the code to support the use of test doubles.

*Applicability*  
    Although proper application of test doubles can provide a powerful boost to engineering velocity, their improper use can lead to tests that are brittle, complex, and less effective. These downsides are magnified when test doubles are used improperly across a large codebase, potentially resulting in major losses in productivity for engineers. In many cases, test doubles are not suitable and engineers should prefer to use real implementations instead.

*Fidelity*  
    Fidelity refers to how closely the behavior of a test double resembles the behavior of the real implementation that it’s replacing. If the behavior of a test double significantly differs from the real implementation, tests that use the test double likely wouldn’t provide much value—for example, imagine trying to write a test with a test double for a database that ignores any data added to the database and always returns empty results. But perfect fidelity might not be feasible; test doubles often need to be vastly simpler than the real implementation in order to be suitable for use in tests. In many situations, it is appropriate to use a test double even without perfect fidelity. Unit tests that use test doubles often need to be supplemented by larger-scope tests that exercise the real implementation.

使用测试替身会给软件开发带来一些复杂性，需要作出权衡。本章后续内容将深入讨论以下概念：

*可测试性*  
    要使用测试替身，代码库的设计就必须具备可测试性：测试应当能够用测试替身替换真实实现。例如，调用数据库的代码需要足够灵活，才能用测试替身代替真实数据库。如果代码库在设计时没有考虑测试，后来才决定补充测试，就可能需要投入大量精力重构代码，才能支持测试替身。

*适用性*  
    正确使用测试替身可以显著加快开发，但使用不当也会让测试变得脆弱、复杂，降低测试的有效性。如果在大型代码库中普遍误用测试替身，这些问题就会被放大，可能严重损害工程师的生产力。许多情况下并不适合使用测试替身，工程师应优先考虑真实实现。

*保真度*  
    保真度是指测试替身的行为与所替代的真实实现有多接近。如果两者的行为相差很大，使用这个替身的测试可能就没有多少价值。例如，假设用一个数据库替身来编写测试，但这个替身会忽略所有写入的数据，始终返回空结果。不过，完全保真未必可行；测试替身往往需要比真实实现简单得多，才适合用于测试。在许多情况下，即使不能完全保真，使用测试替身仍然合适。使用测试替身的单元测试，通常还需要范围更大、会执行真实实现的测试作为补充。

## Test Doubles at Google 谷歌的测试替身

At Google, we’ve seen countless examples of the benefits to productivity and software quality that test doubles can bring to a codebase, as well as the negative impact they can cause when used improperly. The practices we follow at Google have evolved over time based on these experiences. Historically, we had few guidelines on how to effectively use test doubles, but best practices evolved as we saw common patterns and antipatterns arise in many teams’ codebases.

在谷歌，我们见过无数实例：测试替身能够提高生产力和软件质量，使用不当也会带来负面影响。谷歌的相关实践正是基于这些经验逐步演变而来。早期，我们很少就如何有效使用测试替身提供指导；后来，随着许多团队的代码库中反复出现相似的模式和反模式，最佳实践才逐渐形成。

One lesson we learned the hard way is the danger of overusing mocking frameworks, which allow you to easily create test doubles (we will discuss mocking frameworks in more detail later in this chapter). When mocking frameworks first came into use at Google, they seemed like a hammer fit for every nail—they made it very easy to write highly focused tests against isolated pieces of code without having to worry about how to construct the dependencies of that code. It wasn’t until several years and countless tests later that we began to realize the cost of such tests: though these tests were easy to write, we suffered greatly given that they required constant effort to maintain while rarely finding bugs. The pendulum at Google has now begun swinging in the other direction, with many engineers avoiding mocking frameworks in favor of writing more realistic tests.

我们付出代价才学到的一条教训，是过度使用模拟框架（mocking framework）存在风险。这类框架可以轻松创建测试替身，本章后面会详细介绍。模拟框架刚在谷歌投入使用时，看起来像一把能应付所有钉子的锤子：工程师很容易就能针对隔离的代码片段编写范围集中的测试，不必操心如何构造代码的依赖。但几年过去，写下无数测试之后，我们才开始意识到代价：这些测试虽然容易编写，却需要持续投入精力维护，又很少发现缺陷，让我们吃了不少苦头。如今，谷歌的倾向开始转向另一端，许多工程师不再使用模拟框架，而是编写更贴近真实情况的测试。

Even though the practices discussed in this chapter are generally agreed upon at Google, the actual application of them varies widely from team to team. This variance stems from engineers having inconsistent knowledge of these practices, inertia in an existing codebase that doesn’t conform to these practices, or teams doing what is easiest for the short term without thinking about the long-term implications.

虽然本章讨论的实践在谷歌得到普遍认可，但各团队的实际应用差别很大。原因包括：工程师对这些实践的了解程度不同；现有代码库不符合这些实践，又难以改变惯有做法；或者团队只顾眼前方便，没有考虑长期影响。

## Basic Concepts 基本概念

Before we dive into how to effectively use test doubles, let’s cover some of the basic concepts related to them. These build the foundation for best practices that we will discuss later in this chapter.

在深入讨论如何有效使用测试替身之前，先介绍几个基本概念，为本章后面的最佳实践打下基础。

### An Example Test Double 测试替身示例

Imagine an ecommerce site that needs to process credit card payments. At its core, it might have something like the code shown in [Example 13-1](#_bookmark1068).

假设有一个需要处理信用卡支付的电子商务网站，其核心代码可能如例13-1所示。

*Example* *13-1.* *A* *credit* *card* *service*

```java
class PaymentProcessor {
  private CreditCardService creditCardService;
  ...
  boolean makePayment(CreditCard creditCard, Money amount) {
    if (creditCard.isExpired()) { return false; }
    boolean success = creditCardService.chargeCreditCard(creditCard,  amount);
    return success;
  }
}

```

It would be infeasible to use a real credit card service in a test (imagine all the transaction fees from running the test!), but a test double could be used in its place to *simulate* the behavior of the real system. The code in Example 13-2 shows an extremely simple test double.

在测试中使用真实的信用卡服务并不可行，想想运行测试会产生多少交易手续费！不过，可以用测试替身来*模拟*真实系统的行为。例13-2展示了一个极其简单的测试替身。

*Example 13-2. A trivial test double*

```java
class TestDoubleCreditCardService implements CreditCardService {
  @Override
  public boolean chargeCreditCard(CreditCard creditCard, Money amount) {
    return true;
  }
}
```

Although this test double doesn’t look very useful, using it in a test still allows us to test some of the logic in the makePayment() method. For example, in Example 13-3, we can validate that the method behaves properly when the credit card is expired because the code path that the test exercises doesn’t rely on the behavior of the credit card service.

这个测试替身虽然看起来用处不大，但仍能帮助我们测试 makePayment() 方法中的部分逻辑。例如，在例13-3中，可以验证信用卡过期时该方法的行为是否正确，因为测试执行的代码路径并不依赖信用卡服务的行为。

*Example 13-3. Using the test double*

```java
@Test public void cardIsExpired_returnFalse() {
	boolean success = paymentProcessor.makePayment(EXPIRED_CARD, AMOUNT);
    assertThat(success).isFalse();
}
```

The following sections in this chapter will discuss how to make use of test doubles in more complex situations than this one.

本章后续各节将讨论如何在更复杂的情况下使用测试替身。

### Seams

```txt
Seams是可以更改程序中的行为而无需在指定位置进行编辑的地方。
```

Code is said to be [*testable* ](https://oreil.ly/yssV2)if it is written in a way that makes it possible to write unit tests for the code. A [*seam* ](https://oreil.ly/pFSFf)is a way to make code testable by allowing for the use of test doubles—it makes it possible to use different dependencies for the system under test rather than the dependencies used in a production environment.

如果代码的编写方式允许为其编写单元测试，就称为[*可测试代码*](https://oreil.ly/yssV2)。[*seam*](https://oreil.ly/pFSFf)（接缝）通过允许使用测试替身来实现可测试性，使被测系统能够换用不同于生产环境的依赖。

[*Dependency* *injection* ](https://oreil.ly/og9p9)is a common technique for introducing seams. In short, when a class utilizes dependency injection, any classes it needs to use (i.e., the class’s *dependencies*) are passed to it rather than instantiated directly, making it possible for these dependencies to be substituted in tests.

[*依赖注入*](https://oreil.ly/og9p9)是引入接缝的常见技术。简而言之，采用依赖注入的类不会自行实例化所需的其他类，而是由外部传入这些*依赖*，因此测试可以替换它们。

[Example 13-4 ](#_bookmark1074)shows an example of dependency injection. Rather than the constructor creating an instance of CreditCardService, it accepts an instance as a parameter.

例13-4展示了依赖注入：构造函数接收一个 CreditCardService 实例作为参数，而不是自行创建实例。

*Example* *13-4.* *Dependency* *injection*

```java
class PaymentProcessor {
  private CreditCardService creditCardService;

  PaymentProcessor(CreditCardService creditCardService) {
    this.creditCardService = creditCardService;
  }
  ...
}

```

The code that calls this constructor is responsible for creating an appropriate Credit CardService instance. Whereas the production code can pass in an implementation of CreditCardService that communicates with an external server, the test can pass in a test double, as demonstrated in [Example 13-5](#_bookmark1075).

调用这个构造函数的代码负责创建合适的 CreditCardService 实例。生产代码可以传入与外部服务器通信的 CreditCardService 实现，而测试则可以传入测试替身，如例13-5所示。

*Example 13-5. Passing in a test double*

```java
PaymentProcessor paymentProcessor =
    new PaymentProcessor(new TestDoubleCreditCardService());
```

To reduce boilerplate associated with manually specifying constructors, automated dependency injection frameworks can be used for constructing object graphs automatically. At Google, [Guice](https://github.com/google/guice)and [Dagger](https://google.github.io/dagger)are automated dependency injection frameworks that are commonly used for Java code.

为减少手动指定构造函数所需的样板代码，可以使用自动依赖注入框架来构造对象图。在谷歌，Java 代码常用的自动依赖注入框架有 [Guice](https://github.com/google/guice) 和 [Dagger](https://google.github.io/dagger)。

With dynamically typed languages such as Python or JavaScript, it is possible to dynamically replace individual functions or object methods. Dependency injection is less important in these languages because this capability makes it possible to use real implementations of dependencies in tests while only overriding functions or methods of the dependency that are unsuitable for tests.

在 Python、JavaScript 等动态类型语言中，可以动态替换单个函数或对象方法。因此，依赖注入在这些语言中没有那么重要：测试可以使用依赖的真实实现，只替换其中不适合测试的函数或方法。

Writing testable code requires an upfront investment. It is especially critical early in the lifetime of a codebase because the later testability is taken into account, the more difficult it is to apply to a codebase. Code written without testing in mind typically needs to be refactored or rewritten before you can add appropriate tests.

编写可测试代码需要前期投入，在代码库生命周期的早期尤其如此。越晚考虑可测试性，就越难让代码库具备这一特性。编写时没有考虑测试的代码，通常需要先重构或重写，才能补上适当的测试。

### Mocking Frameworks 模拟框架

A *mocking framework* is a software library that makes it easier to create test doubles within tests; it allows you to replace an object with a *mock*, which is a test double whose behavior is specified inline in a test. The use of mocking frameworks reduces boilerplate because you don’t need to define a new class each time you need a test double.

*模拟框架*是一种软件库，便于在测试中创建测试替身。它允许用模拟对象（mock）替换一个对象；模拟对象是一类测试替身，其行为直接在测试中指定。使用模拟框架可以减少样板代码，因为不必每次需要测试替身时都定义一个新类。

Example 13-6 demonstrates the use of [Mockito](https://site.mockito.org/), a mocking framework for Java. Mockito creates a test double for CreditCardService and instructs it to return a specific value.

 例13-6演示了 Java 模拟框架 [Mockito](https://site.mockito.org/) 的用法：为 CreditCardService 创建一个测试替身，并指定它返回某个值。

*Example 13-6. Mocking frameworks*

```java
class PaymentProcessorTest {
...
PaymentProcessor paymentProcessor;

// Create a test double of CreditCardService with just one line of code.
@Mock CreditCardService mockCreditCardService;

@Before public void setUp() {
    // Pass in the test double to the system under test.
    paymentProcessor = new PaymentProcessor(mockCreditCardService);
}

@Test public void chargeCreditCardFails_returnFalse() {
    // Give some behavior to the test double: it will return false
    // anytime the chargeCreditCard() method is called. The usage of
    // “any()” for the method’s arguments tells the test double to
    // return false regardless of which arguments are passed.
    when(mockCreditCardService.chargeCreditCard(any(), any())
    	.thenReturn(false);
    boolean success = paymentProcessor.makePayment(CREDIT_CARD, AMOUNT);
    assertThat(success).isFalse();
  }
}
```

Mocking frameworks exist for most major programming languages. At Google, we use Mockito for Java, [the googlemock component of Googletest](https://github.com/google/googletest)for C++, and [unittest.mock](https://oreil.ly/clzvH)for Python.

大多数主流编程语言都有模拟框架。在谷歌，Java 使用 Mockito，C++ 使用 [Googletest的googlemock组件](https://github.com/google/googletest)，Python 使用 [uni-ttest.mock](https://oreil.ly/clzvH)。

Although mocking frameworks facilitate easier usage of test doubles, they come with some significant caveats given that their overuse will often make a codebase more difficult to maintain. We cover some of these problems later in this chapter.

模拟框架虽然让测试替身更容易使用，但也有一些重要的注意事项：过度使用往往会让代码库更难维护。本章后面将介绍其中的一些问题。

## Techniques for Using Test Doubles 测试替身的使用技术

There are three primary techniques for using test doubles. This section presents a brief introduction to these techniques to give you a quick overview of what they are and how they differ. Later sections in this chapter go into more details on how to effectively apply them.

使用测试替身主要有三种技术。本节先简要介绍其含义和区别，后续各节再详细讨论如何有效运用。

An engineer who is aware of the distinctions between these techniques is more likely to know the appropriate technique to use when faced with the need to use a test double.

了解这些技术之间的区别，工程师就更容易在需要测试替身时作出合适的选择。

### Faking 使用伪实现

A [*fake*](https://oreil.ly/rymnI) is a lightweight implementation of an API that behaves similar to the real implementation but isn’t suitable for production; for example, an in-memory database. Example 13-7presents an example of faking.

 伪实现（[*fake*](https://oreil.ly/rymnI)）是 API 的轻量级实现，行为与真实实现相似，但不适合用于生产环境，例如内存数据库。例13-7展示了伪实现的用法。

*Example 13-7. A simple* *fake*

```java
// Creating the fake is fast and easy.
AuthorizationService fakeAuthorizationService = new FakeAuthorizationService();
AccessManager accessManager = new AccessManager(fakeAuthorizationService):

// Unknown user IDs shouldn’t have access.
assertFalse(accessManager.userHasAccess(USER_ID));

// The user ID should have access after it is added to
// the authorization service. 
fakeAuthorizationService.addAuthorizedUser(new User(USER_ID));
assertThat(accessManager.userHasAccess(USER_ID)).isTrue();

```

Using a fake is often the ideal technique when you need to use a test double, but a fake might not exist for an object you need to use in a test, and writing one can be challenging because you need to ensure that it has similar behavior to the real implementation, now and in the future.

需要测试替身时，伪实现通常是理想选择。但测试所需的对象未必有现成的伪实现，而自行编写也并不容易，因为必须确保它现在及将来的行为都与真实实现相似。

### Stubbing 打桩

[*Stubbing*](https://oreil.ly/gmShS)is the process of giving behavior to a function that otherwise has no behavior on its own—you specify to the function exactly what values to return (that is, you *stub* the return values).

打桩是为原本没有自身行为的函数指定行为的过程：明确指定函数应返回哪些值，也就是为返回值设置桩。

[Example 13-8](#_bookmark1093) illustrates stubbing. The when(...).thenReturn(...) method calls from the Mockito mocking framework specify the behavior of the lookupUser() method.

例13-8展示了打桩：调用 Mockito 模拟框架的 when(...).thenReturn(...) 方法，指定 lookupUser() 方法的行为。

*Example* *13-8.* *Stubbing*

```java
// Pass in a test double that was created by a mocking framework.
AccessManager accessManager = new AccessManager(mockAuthorizationService):

// The user ID shouldn’t have access if null is returned. 
when(mockAuthorizationService.lookupUser(USER_ID)).thenReturn(null);
assertThat(accessManager.userHasAccess(USER_ID)).isFalse();

// The user ID should have access if a non-null value is returned.   
when(mockAuthorizationService.lookupUser(USER_ID)).thenReturn(USER);
assertThat(accessManager.userHasAccess(USER_ID)).isTrue();
```

Stubbing is typically done through mocking frameworks to reduce boilerplate that would otherwise be needed for manually creating new classes that hardcode return values.

打桩通常通过模拟框架完成，省去手动创建新类并硬编码返回值所需的样板代码。

Although stubbing can be a quick and simple technique to apply, it has limitations, which we’ll discuss later in this chapter.

打桩虽然用起来简单快捷，但也有局限，后文将进一步讨论。

### Interaction Testing 交互测试

[*Interaction testing*](https://oreil.ly/zGfFn)is a way to validate *how* a function is called without actually calling the implementation of the function. A test should fail if a function isn’t called the correct way—for example, if the function isn’t called at all, it’s called too many times, or it’s called with the wrong arguments.

交互测试用于验证函数的调用方式，而不实际执行函数的实现。如果调用方式不正确，例如根本没有调用、调用次数过多或传入了错误参数，测试就应该失败。

Example 13-9 presents an instance of interaction testing. The verify(...) method from the Mockito mocking framework is used to validate that lookupUser() is called as expected.

例13-9展示了交互测试：使用 Mockito 模拟框架的 verify(...) 方法，验证 lookupUser() 是否按预期被调用。

*Example* *13-9. Interaction testing*

```java
// Pass in a test double that was created by a mocking framework.
AccessManager accessManager = new AccessManager(mockAuthorizationService);
accessManager.userHasAccess(USER_ID);

// The test will fail if accessManager.userHasAccess(USER_ID) didn’t call
// mockAuthorizationService.lookupUser(USER_ID).
verify(mockAuthorizationService).lookupUser(USER_ID);

```

Similar to stubbing, interaction testing is typically done through mocking frameworks. This reduces boilerplate compared to manually creating new classes that contain code to keep track of how often a function is called and which arguments were passed in.

与打桩类似，交互测试通常也通过模拟框架完成。这样就不必手动创建新类来记录函数的调用次数和传入参数，从而减少样板代码。

Interaction testing is sometimes called [*mocking*](https://oreil.ly/IfMoR). We avoid this terminology in this chapter because it can be confused with mocking frameworks, which can be used for stubbing as well as for interaction testing.

交互测试有时被称为 mocking。本章避免用这个术语称呼交互测试，以免与模拟框架混淆，因为模拟框架既可用于打桩，也可用于交互测试。

As discussed later in this chapter, interaction testing is useful in certain situations but should be avoided when possible because overuse can easily result in brittle tests.

后文将说明，交互测试在某些情况下很有用，但应尽可能避免，因为过度使用很容易让测试变得脆弱。

### Real Implementations 真实实现

Although test doubles can be invaluable testing tools, our first choice for tests is to use the real implementations of the system under test’s dependencies; that is, the same implementations that are used in production code. Tests have higher fidelity when they execute code as it will be executed in production, and using real implementations helps accomplish this.

测试替身虽然是很有价值的测试工具，但我们的首选仍是使用被测系统所依赖的真实实现，也就是生产代码中使用的实现。测试中的代码执行方式越接近生产环境，保真度就越高；使用真实实现有助于做到这一点。

At Google, the preference for real implementations developed over time as we saw that overuse of mocking frameworks had a tendency to pollute tests with repetitive code that got out of sync with the real implementation and made refactoring difficult. We’ll look at this topic in more detail later in this chapter.

谷歌对真实实现的偏好是逐渐形成的。我们发现，过度使用模拟框架往往会让测试充斥着重复代码，这些代码容易与真实实现脱节，也会增加重构难度。本章后面将进一步讨论这个问题。

Preferring real implementations in tests is known as [*classical testing*](https://oreil.ly/OWw7h). There is also a style of testing known as *mockist testing*, in which the preference is to use mocking frameworks instead of real implementations. Even though some people in the software industry practice mockist testing (including the [creators of the first mocking](https://oreil.ly/_QWy7) [frameworks](https://oreil.ly/_QWy7)), at Google, we have found that this style of testing is difficult to scale. It requires engineers to follow [strict guidelines when designing the system under test](http://jmock.org/oopsla2004.pdf), and the default behavior of most engineers at Google has been to write code in a way that is more suitable for the classical testing style.

在测试中优先使用真实实现的风格，称为[*经典测试*](https://oreil.ly/OWw7h)。另一种风格则是*模拟派测试*（mockist testing），优先使用模拟框架而不是真实实现。软件行业中确实有人采用模拟派测试，包括[第一个模拟框架](https://oreil.ly/_QWy7)的创造者，但谷歌的经验是，这种风格很难推广到大规模开发中。它要求工程师遵循[设计被测系统时的严格准则](http://jmock.org/oopsla2004.pdf)，而谷歌大多数工程师通常写出的代码更适合经典测试风格。

### Prefer Realism Over Isolation 优先考虑真实性，而非隔离性

Using real implementations for dependencies makes the system under test more realistic given that all code in these real implementations will be executed in the test. In contrast, a test that utilizes test doubles isolates the system under test from its dependencies so that the test does not execute code in the dependencies of the system under test.

为依赖使用真实实现，意味着测试中会执行这些实现的全部代码，因此被测系统更接近真实情况。相比之下，测试替身会把被测系统与其依赖隔离开来，测试便不会执行那些依赖中的代码。

We prefer realistic tests because they give more confidence that the system under test is working properly. If unit tests rely too much on test doubles, an engineer might need to run integration tests or manually verify that their feature is working as expected in order to gain this same level of confidence. Carrying out these extra tasks can slow down development and can even allow bugs to slip through if engineers skip these tasks entirely when they are too time consuming to carry out compared to running unit tests.

我们更倾向于贴近真实情况的测试，因为它们更能让人确信被测系统工作正常。如果单元测试过度依赖测试替身，工程师可能还得运行集成测试，或手动验证功能是否符合预期，才能获得同等程度的信心。这些额外工作会拖慢开发；如果它们比运行单元测试耗时太多，工程师甚至可能直接跳过，让缺陷漏网。

Replacing all dependencies of a class with test doubles arbitrarily isolates the system under test to the implementation that the author happens to put directly into the class and excludes implementation that happens to be in different classes. However, a good test should be independent of implementation—it should be written in terms of the API being tested rather than in terms of how the implementation is structured.

把一个类的所有依赖都替换为测试替身，实际上是人为地把被测系统限定在作者恰好写进这个类的实现之内，排除了恰好放在其他类中的实现。然而，好的测试应当独立于实现：围绕被测 API 编写，而不是围绕实现的组织方式编写。

Using real implementations can cause your test to fail if there is a bug in the real implementation. This is good! You *want* your tests to fail in such cases because it indicates that your code won’t work properly in production. Sometimes, a bug in a real implementation can cause a cascade of test failures because other tests that use the real implementation might fail, too. But with good developer tools, such as a Continuous Integration (CI) system, it is usually easy to track down the change that caused the failure.

真实实现中如果存在缺陷，使用它的测试就可能失败。这是好事！你正是希望测试在这种情况下失败，因为这说明代码在生产环境中无法正常工作。有时，一个真实实现中的缺陷会引发连锁反应，让其他使用它的测试也失败。但借助持续集成（CI）系统等良好的开发工具，通常很容易定位到引发失败的变更。

-----

#### Case Study: @DoNotMock 案例研究：@DoNotMock

At Google, we’ve seen enough tests that over-rely on mocking frameworks to motivate the creation of the @DoNotMock annotation in Java, which is available as part of the [ErrorProne](https://github.com/google/error-prone)static analysis tool. This annotation is a way for API owners to declare, “this type should not be mocked because better alternatives exist.”

谷歌有太多测试过度依赖模拟框架，这促使我们为 Java 创建了 @DoNotMock 注解，并将其作为 [ErrorProne](https://github.com/google/error-prone) 静态分析工具的一部分提供。API 维护者可以用这个注解声明：“不要为这个类型创建模拟对象，因为有更好的替代方案。”

If an engineer attempts to use a mocking framework to create an instance of a class or interface that has been annotated as @DoNotMock, as demonstrated in Example 13-10, they will see an error directing them to use a more suitable test strategy, such as a real implementation or a fake. This annotation is most commonly used for value objects that are simple enough to use as-is, as well as for APIs that have well-engineered fakes available.

如果工程师试图用模拟框架为标有 @DoNotMock 的类或接口创建实例，就会看到一条错误提示，要求改用更合适的测试策略，例如真实实现或伪实现，如例13-10所示。这个注解最常用于足够简单、可以直接使用的值对象，以及已有完善伪实现的 API。

*Example* *13-10. The @DoNotMock annotation*

```java
@DoNotMock("Use SimpleQuery.create() instead of mocking.")
public abstract class Query {
  public abstract String getQueryValue();
}
```

Why would an API owner care? In short, it severely constrains the API owner’s ability to make changes to their implementation over time. As we’ll explore later in the chapter, every time a mocking framework is used for stubbing or interaction testing, it duplicates behavior provided by the API.

API 维护者为什么在意这个问题？简而言之，为 API 创建模拟对象会严重限制维护者后续修改实现的能力。正如后文将讨论的，每次使用模拟框架打桩或进行交互测试，都在重复定义 API 提供的行为。

When the API owner wants to change their API, they might find that it has been mocked thousands or even tens of thousands of times throughout Google’s codebase! These test doubles are very likely to exhibit behavior that violates the API contract of the type being mocked—for instance, returning null for a method that can never return null. Had the tests used the real implementation or a fake, the API owner could make changes to their implementation without first fixing thousands of flawed tests.

API 维护者想修改 API 时，可能会发现谷歌代码库中已经为它创建了数千甚至数万个模拟对象！这些测试替身很可能违反被模拟类型的 API 契约，例如，让一个绝不会返回 null 的方法返回 null。如果测试使用真实实现或伪实现，API 维护者就能直接修改实现，不必先修复成千上万个有问题的测试。

-----

### How to Decide When to Use a Real Implementation 如何决定何时使用真实实现

A real implementation is preferred if it is fast, deterministic, and has simple dependencies. For example, a real implementation should be used for a [*value object*](https://oreil.ly/UZiXP). Examples include an amount of money, a date, a geographical address, or a collection class such as a list or a map.

如果真实实现运行快、行为具有确定性、依赖简单，就应优先使用。例如，[*值对象*](https://oreil.ly/UZiXP)就应使用真实实现，包括金额、日期、地理地址，以及列表、映射等集合类。

However, for more complex code, using a real implementation often isn’t feasible. There might not be an exact answer on when to use a real implementation or a test double given that there are trade-offs to be made, so you need to take the following considerations into account.

不过，代码比较复杂时，使用真实实现往往并不可行。何时用真实实现、何时用测试替身，涉及各种权衡，未必有明确答案，因此需要考虑以下因素。

#### Execution time 执行时间

One of the most important qualities of unit tests is that they should be fast—you want to be able to continually run them during development so that you can get quick feedback on whether your code is working (and you also want them to finish quickly when run in a CI system). As a result, a test double can be very useful when the real implementation is slow.

单元测试最重要的特性之一是运行快。开发过程中，你需要反复运行测试，及时了解代码是否工作正常；在 CI 系统中运行时，也希望它们尽快完成。因此，真实实现较慢时，测试替身就可能很有用。

How slow is too slow for a unit test? If a real implementation added one millisecond to the running time of each individual test case, few people would classify it as slow. But what if it added 10 milliseconds, 100 milliseconds, 1 second, and so on?

对单元测试来说，多慢才算太慢？如果真实实现让每个测试用例多运行1毫秒，很少有人会觉得慢。但如果多出10毫秒、100毫秒、1秒，甚至更长呢？

There is no exact answer here—it can depend on whether engineers feel a loss in productivity, and how many tests are using the real implementation (one second extra per test case may be reasonable if there are five test cases, but not if there are 500). For borderline situations, it is often simpler to use a real implementation until it becomes too slow to use, at which point the tests can be updated to use a test double instead.

这没有确切答案，可能取决于工程师是否感到工作效率下降，以及有多少测试使用这个真实实现。只有5个测试用例时，每个多运行1秒也许可以接受；有500个时，就未必了。对于难以判断的情况，通常最简单的办法是先使用真实实现，等到确实慢得无法接受，再把测试改为使用测试替身。

Parellelization of tests can also help reduce execution time. At Google, our test infrastructure makes it trivial to split up tests in a test suite to be executed across multiple servers. This increases the cost of CPU time, but it can provide a large savings in developer time. We discuss this more in [Chapter 18](#_bookmark1596).

并行运行测试也有助于缩短执行时间。在谷歌，测试基础设施让我们能轻松地把测试套件拆分到多台服务器上执行。这样会增加 CPU 时间成本，却能节省大量开发者时间。第18章将进一步讨论这一点。

Another trade-off to be aware of: using a real implementation can result in increased build times given that the tests need to build the real implementation as well as all of its dependencies. Using a highly scalable build system like [Bazel ](https://bazel.build/)can help because it caches unchanged build artifacts.

还需要考虑另一项权衡：使用真实实现可能延长构建时间，因为测试需要构建它及其全部依赖。[Bazel](https://bazel.build/) 这类可扩展性强的构建系统可以缓存没有变化的构建产物，有助于缓解这个问题。

#### Determinism 确定性

A test is [*deterministic*](https://oreil.ly/brxJl)if, for a given version of the system under test, running the test always results in the same outcome; that is, the test either always passes or always fails. In contrast, a test is [*nondeterministic*](https://oreil.ly/5pG0f)if its outcome can change, even if the system under test remains unchanged.

对于被测系统的某个固定版本，如果测试每次运行都得到相同结果，即始终通过或始终失败，就称其具有[*确定性*](https://oreil.ly/brxJl)。反之，即使被测系统没有变化，测试结果仍可能改变，就称其具有[*非确定性*](https://oreil.ly/5pG0f)。

[Nondeterminism in tests ](https://oreil.ly/71OFU)can lead to flakiness—tests can occasionally fail even when there are no changes to the system under test. As discussed in Chapter 11, flakiness harms the health of a test suite if developers start to distrust the results of the test and ignore failures. If use of a real implementation rarely causes flakiness, it might not warrant a response, because there is little disruption to engineers. But if flakiness hap‐pens often, it might be time to replace a real implementation with a test double because doing so will improve the fidelity of the test.

[测试中的非确定性](https://oreil.ly/71OFU)会导致测试不稳定：即使被测系统没有变化，测试也可能偶尔失败。第11章讨论过，如果开发者因此不再信任测试结果，开始忽略失败，测试套件的健康就会受损。如果真实实现很少导致测试不稳定，对工程师的干扰很小，也许不必专门处理。但如果频繁出现不稳定的情况，就可能需要用测试替身替换真实实现，因为这样能提高测试的保真度。

A real implementation can be much more complex compared to a test double, which increases the likelihood that it will be nondeterministic. For example, a real implementation that utilizes multithreading might occasionally cause a test to fail if the output of the system under test differs depending on the order in which the threads are executed.

真实实现可能比测试替身复杂得多，也更容易表现出非确定性。例如，真实实现如果使用多线程，而被测系统的输出又受线程执行顺序影响，就可能偶尔导致测试失败。

A common cause of nondeterminism is code that is not [hermetic](https://oreil.ly/aes__); that is, it has dependencies on external services that are outside the control of a test. For example, a test that tries to read the contents of a web page from an HTTP server might fail if the server is overloaded or if the web page contents change. Instead, a test double should be used to prevent the test from depending on an external server. If using a test double is not feasible, another option is to use a hermetic instance of a server, which has its life cycle controlled by the test. Hermetic instances are discussed in more detail in the next chapter.

非确定性的一个常见原因是代码不具备封闭性，也就是依赖测试无法控制的外部服务。例如，测试从 HTTP 服务器读取网页内容时，可能因服务器过载或网页内容变化而失败。应当用测试替身消除对外部服务器的依赖。如果无法使用测试替身，也可以使用生命周期由测试控制的封闭服务器实例。下一章将详细讨论封闭实例。

Another example of nondeterminism is code that relies on the system clock given that the output of the system under test can differ depending on the current time. Instead of relying on the system clock, a test can use a test double that hardcodes a specific time.

依赖系统时钟的代码也是一个例子：被测系统的输出可能随当前时间变化。测试可以改用一个把时间固定为特定值的测试替身，不再依赖系统时钟。

#### Dependency construction 构造依赖

When using a real implementation, you need to construct all of its dependencies. For example, an object needs its entire dependency tree to be constructed: all objects that it depends on, all objects that these dependent objects depend on, and so on. A test double often has no dependencies, so constructing a test double can be much simpler compared to constructing a real implementation.

使用真实实现时，需要构造它的全部依赖。以一个对象为例，必须构造整棵依赖树：它依赖的所有对象、那些对象依赖的其他对象，依此类推。测试替身通常没有依赖，因此构造起来往往比真实实现简单得多。

As an extreme example, imagine trying to create the object in the code snippet that follows in a test. It would be time consuming to determine how to construct each individual object. Tests will also require constant maintenance because they need to be updated when the signature of these objects’ constructors is modified:

举一个极端的例子：假设要在测试中创建下面代码里的对象。仅仅弄清每个对象该如何构造，就可能花费很多时间。测试还需要持续维护，因为只要这些对象的构造函数签名发生变化，就必须更新测试：

```java
Foo foo = new Foo(new A(new B(new C()), new D()), new E(), ..., new Z());
```

It can be tempting to instead use a test double because constructing one can be trivial. For example, this is all it takes to construct a test double when using the Mockito mocking framework:

这时很容易想改用测试替身，因为构造它可能十分简单。例如，使用 Mockito 模拟框架时，只需以下代码：

```java
@Mock 
Foo mockFoo;
```

Although creating this test double is much simpler, there are significant benefits to using the real implementation, as discussed earlier in this section. There are also often significant downsides to overusing test doubles in this way, which we look at later in this chapter. So, a trade-off needs to be made when considering whether to use a real implementation or a test double.

创建这个测试替身虽然简单得多，但如本节前面所述，真实实现也有显著优势。以这种方式过度使用测试替身，往往还会带来严重问题，后文会进一步说明。因此，选择真实实现还是测试替身，需要作出权衡。

Rather than manually constructing the object in tests, the ideal solution is to use the same object construction code that is used in the production code, such as a factory method or automated dependency injection. To support the use case for tests, the object construction code needs to be flexible enough to be able to use test doubles rather than hardcoding the implementations that will be used for production.

理想的办法不是在测试中手动构造对象，而是复用生产代码中的对象构造逻辑，例如工厂方法或自动依赖注入。为了支持测试，这些构造逻辑必须足够灵活，允许使用测试替身，不能写死为生产环境所用的实现。

## Faking 使用伪实现

If using a real implementation is not feasible within a test, the best option is often to use a fake in its place. A fake is preferred over other test double techniques because it behaves similarly to the real implementation: the system under test shouldn’t even be able to tell whether it is interacting with a real implementation or a fake. Example 13-11illustrates a fake file system. 

如果测试无法使用真实实现，通常最好的选择是用伪实现代替。相较于其他测试替身技术，伪实现更值得优先考虑，因为它的行为与真实实现相似：被测系统甚至不应察觉自己是在与真实实现还是伪实现交互。例13-11展示了一个文件系统的伪实现。

*Example* *13-11.* *A* *fake* *file* *system*

```java
// This fake implements the FileSystem interface. This interface is also
// used by the real implementation.
public class FakeFileSystem implements FileSystem {
    // Stores a map of file name to file contents. The files are stored in
    // memory instead of on disk since tests shouldn’t need to do disk I/O.
    private Map < String, String > files = new HashMap< > ();
    
    @Override
    public void writeFile(String fileName, String contents) {
        // Add the file name and contents to the map.
        files.add(fileName, contents);
    }
  
    @Override
    public String readFile(String fileName) {
        String contents = files.get(fileName);
        // The real implementation will throw this exception if the
        // file isn’t found, so the fake must throw it too.
        if(contents == null) {
            throw new FileNotFoundException(fileName);
        }
        return contents;
    }
}
```

### Why Are Fakes Important? 伪实现为什么重要？

Fakes can be a powerful tool for testing: they execute quickly and allow you to effectively test your code without the drawbacks of using real implementations.

伪实现可以成为强大的测试工具：运行迅速，能有效测试代码，又避免了使用真实实现的弊端。

A single fake has the power to radically improve the testing experience of an API. If you scale that to a large number of fakes for all sorts of APIs, fakes can provide an enormous boost to engineering velocity across a software organization.

一个伪实现就能大幅改善某个 API 的测试体验。如果为各种 API 提供大量伪实现，就能显著加快整个软件组织的开发速度。

At the other end of the spectrum, in a software organization where fakes are rare, velocity will be slower because engineers can end up struggling with using real implementations that lead to slow and flaky tests. Or engineers might resort to other test double techniques such as stubbing or interaction testing, which, as we’ll examine later in this chapter, can result in tests that are unclear, brittle, and less effective.

反过来，如果一个软件组织很少提供伪实现，开发速度就会较慢。工程师可能不得不艰难地使用真实实现，使测试运行缓慢、结果不稳定；也可能转而采用打桩或交互测试等其他测试替身技术。后文会说明，这些技术可能让测试含义不清、变得脆弱，有效性也随之降低。

### When Should Fakes Be Written? 何时应该编写伪实现？

A fake requires more effort and more domain experience to create because it needs to behave similarly to the real implementation. A fake also requires maintenance: whenever the behavior of the real implementation changes, the fake must also be updated to match this behavior. Because of this, the team that owns the real implementation should write and maintain a fake.

编写伪实现需要投入更多精力，也需要更多领域经验，因为它的行为必须与真实实现相似。伪实现还需要维护：真实实现的行为发生变化时，伪实现也必须相应更新。因此，应由负责真实实现的团队编写和维护伪实现。

If a team is considering writing a fake, a trade-off needs to be made on whether the productivity improvements that will result from the use of the fake outweigh the costs of writing and maintaining it. If there are only a handful of users, it might not be worth their time, whereas if there are hundreds of users, it can result in an obvious productivity improvement.

团队考虑编写伪实现时，需要权衡它带来的生产力提升能否超过编写和维护成本。如果只有少数使用者，也许不值得投入；如果有数百名使用者，就可能带来明显的生产力提升。

To reduce the number of fakes that need to be maintained, a fake should typically be created only at the root of the code that isn’t feasible for use in tests. For example, if a database can’t be used in tests, a fake should exist for the database API itself rather than for each class that calls the database API.

为减少需要维护的伪实现数量，通常只应在无法用于测试的那部分代码的根部提供伪实现。例如，如果数据库无法用于测试，就应为数据库 API 本身提供伪实现，而不是为每个调用该 API 的类都写一个。

Maintaining a fake can be burdensome if its implementation needs to be duplicated across programming languages, such as for a service that has client libraries that allow the service to be invoked from different languages. One solution for this case is to create a single fake service implementation and have tests configure the client libraries to send requests to this fake service. This approach is more heavyweight compared to having the fake written entirely in memory because it requires the test to communicate across processes. However, it can be a reasonable trade-off to make, as long as the tests can still execute quickly.

如果需要用多种编程语言分别编写同一个伪实现，维护负担就可能很重。例如，某个服务提供多种语言的客户端库，供不同语言的代码调用。一种解决办法是只编写一个服务的伪实现，再由测试配置客户端库，让请求发往这个伪服务。与完全在内存中运行的伪实现相比，这种做法开销更大，因为测试需要跨进程通信。不过，只要测试仍能快速运行，这样的权衡就可能合理。

### The Fidelity of Fakes 伪实现的保真度

Perhaps the most important concept surrounding the creation of fakes is *fidelity*; in other words, how closely the behavior of a fake matches the behavior of the real implementation. If the behavior of a fake doesn’t match the behavior of the real implementation, a test using that fake is not useful—a test might pass when the fake is used, but this same code path might not work properly in the real implementation.

编写伪实现时，最重要的概念也许就是*保真度*，也就是其行为与真实实现有多接近。如果两者的行为不一致，使用伪实现的测试就没有用：测试在伪实现上可能通过，但同一代码路径换用真实实现后却可能无法正常工作。

Perfect fidelity is not always feasible. After all, the fake was necessary because the real implementation wasn’t suitable in one way or another. For example, a fake database would usually not have fidelity to a real database in terms of hard drive storage because the fake would store everything in memory.

完全保真并非总能做到。毕竟，正是因为真实实现在某些方面不适合测试，才需要伪实现。例如，数据库的伪实现通常不会在硬盘存储方面保持与真实数据库一致，因为它会把所有数据都存放在内存中。

Primarily, however, a fake should maintain fidelity to the API contracts of the real implementation. For any given input to an API, a fake should return the same output and perform the same state changes of its corresponding real implementation. For example, for a real implementation of database.save(itemId), if an item is successfully saved when its ID does not yet exist but an error is produced when the ID already exists, the fake must conform to this same behavior.

不过，最重要的是，伪实现应遵守真实实现的 API 契约。对于 API 的任意给定输入，伪实现应返回与真实实现相同的输出，并作出相同的状态变更。例如，database.save(itemId) 的真实实现在记录 ID 尚不存在时成功保存记录，在 ID 已存在时则报错，伪实现也必须遵循这一行为。

One way to think about this is that the fake must have perfect fidelity to the real implementation, but *only from the perspective of the test*. For example, a fake for a hashing API doesn’t need to guarantee that the hash value for a given input is exactly the same as the hash value that is generated by the real implementation—tests likely don’t care about the specific hash value, only that the hash value is unique for a given input. If the contract of the hashing API doesn’t make guarantees of what specific hash values will be returned, the fake is still conforming to the contract even if it doesn’t have perfect fidelity to the real implementation.

可以这样理解：伪实现必须与真实实现完全一致，但这一要求仅限于测试所关注的角度。例如，哈希 API 的伪实现不必保证同一输入产生的哈希值与真实实现完全相同；测试可能并不关心具体数值，只关心给定输入的哈希值是否唯一。如果 API 契约没有承诺返回哪些具体哈希值，那么即使伪实现与真实实现并非完全一致，它仍然遵守契约。

Other examples where perfect fidelity typically might not be useful for fakes include latency and resource consumption. However, a fake cannot be used if you need to explicitly test for these constraints (e.g., a performance test that verifies the latency of a function call), so you would need to resort to other mechanisms, such as by using a real implementation instead of a fake.

延迟和资源消耗也是类似的例子：伪实现在这些方面完全保真，通常没有多少用处。但如果需要专门测试这些约束，例如通过性能测试验证函数调用延迟，就不能使用伪实现，而要采用其他办法，比如改用真实实现。

A fake might not need to have 100% of the functionality of its corresponding real implementation, especially if such behavior is not needed by most tests (e.g., error handling code for rare edge cases). It is best to have the fake fail fast in this case; for example, raise an error if an unsupported code path is executed. This failure communicates to the engineer that the fake is not appropriate in this situation.

伪实现未必需要覆盖真实实现的100%功能，尤其是大多数测试用不到的行为，例如罕见边界情况的错误处理。对于不支持的功能，最好让伪实现尽早失败，例如执行到不受支持的代码路径时立即报错。这样就能明确告知工程师：这个伪实现不适合当前场景。

### Fakes Should Be Tested  伪实现也需要测试

A fake must have its *own* tests to ensure that it conforms to the API of its corresponding real implementation. A fake without tests might initially provide realistic behavior, but without tests, this behavior can diverge over time as the real implementation evolves.

伪实现必须有自己的*测试*，以确保它符合对应真实实现的 API。没有测试的伪实现，起初的行为也许很接近真实实现，但随着真实实现演进，两者的行为可能逐渐偏离。

One approach to writing tests for fakes involves writing tests against the API’s public interface and running those tests against both the real implementation and the fake (these are known as [*contract tests*](https://oreil.ly/yuVlX)). The tests that run against the real implementation will likely be slower, but their downside is minimized because they need to be run only by the owners of the fake.

一种办法是针对 API 的公开接口编写测试，再分别用真实实现和伪实现运行同一套测试，这称为[*契约测试*](https://oreil.ly/yuVlX)。在真实实现上运行测试可能更慢，但只需由伪实现的维护者运行，因此额外负担可以控制在较小范围内。

### What to Do If a Fake Is Not Available 没有伪实现怎么办？

If a fake is not available, first ask the owners of the API to create one. The owners might not be familiar with the concept of fakes, or they might not realize the benefit they provide to users of an API.

如果没有现成的伪实现，首先应请 API 维护者提供一个。他们可能还不了解伪实现的概念，或没有意识到它能为 API 使用者带来多少好处。

If the owners of an API are unwilling or unable to create a fake, you might be able to write your own. One way to do this is to wrap all calls to the API in a single class and then create a fake version of the class that doesn’t talk to the API. Doing this can also be much simpler than creating a fake for the entire API because often you’ll need to use only a subset of the API’s behavior anyway. At Google, some teams have even contributed their fake to the owners of the API, which has allowed other teams to benefit from the fake.

如果 API 维护者不愿或无法提供伪实现，也可以考虑自行编写。一种做法是把所有 API 调用封装到一个类中，再为这个类编写一个不调用该 API 的伪实现。由于通常只用到 API 的部分行为，这样做往往比实现整个 API 的替身简单得多。在谷歌，一些团队甚至把自己的伪实现贡献给 API 维护者，让其他团队也能受益。

Finally, you could decide to settle on using a real implementation (and deal with the trade-offs of real implementations that are mentioned earlier in this chapter), or resort to other test double techniques (and deal with the trade-offs that we will mention later in this chapter).

最后，也可以选择接受真实实现，并承担本章前面讨论的相应代价；或者采用其他测试替身技术，作出本章后面将讨论的权衡。

In some cases, you can think of a fake as an optimization: if tests are too slow using a real implementation, you can create a fake to make them run faster. But if the speedup from a fake doesn’t outweigh the work it would take to create and maintain the fake, it would be better to stick with using the real implementation.

在某些情况下，可以把伪实现看作一种优化：如果使用真实实现时测试太慢，就编写伪实现来加速。但如果节省的时间不足以抵偿编写和维护伪实现的投入，就不如继续使用真实实现。

## Stubbing 打桩

As discussed earlier in this chapter, stubbing is a way for a test to hardcode behavior for a function that otherwise has no behavior on its own. It is often a quick and easy way to replace a real implementation in a test. For example, the code in [Example 13-12 ](#_bookmark1144)uses stubbing to simulate the response from a credit card server.

如前文所述，打桩是在测试中为原本没有自身行为的函数硬编码行为。它通常能简单快捷地替换测试中的真实实现。例如，例13-12通过打桩模拟信用卡服务器的响应。

*Example* *13-12.* *Using* *stubbing* *to* *simulate* *responses*

```java
@Test public void getTransactionCount() {
transactionCounter = new TransactionCounter(mockCreditCardServer);
// Use stubbing to return three transactions.
when(mockCreditCardServer.getTransactions()).thenReturn( newList(TRANSACTION_1, TRANSACTION_2, TRANSACTION_3));
assertThat(transactionCounter.getTransactionCount()).isEqualTo(3);
}
```

### The Dangers of Overusing Stubbing  过度使用打桩的危害

Because stubbing is so easy to apply in tests, it can be tempting to use this technique anytime it’s not trivial to use a real implementation. However, overuse of stubbing can result in major losses in productivity for engineers who need to maintain these tests.

打桩很容易，因此只要真实实现用起来稍有麻烦，人们就容易想改用打桩。然而，过度打桩可能严重损害测试维护者的生产力。

#### Tests become unclear 测试变得不清晰

Stubbing involves writing extra code to define the behavior of the functions being stubbed. Having this extra code detracts from the intent of the test, and this code can be difficult to understand if you’re not familiar with the implementation of the system under test.

打桩需要额外编写代码，定义被打桩函数的行为。这些代码会掩盖测试的意图；如果不熟悉被测系统的实现，还可能很难读懂。

A key sign that stubbing isn’t appropriate for a test is if you find yourself mentally stepping through the system under test in order to understand why certain functions in the test are stubbed.

如果为了理解测试为什么给某些函数打桩，你必须在脑中逐步推演被测系统的执行过程，这就是一个重要信号：这个测试可能不适合打桩。

#### Tests become brittle 测试变得脆弱

Stubbing leaks implementation details of your code into your test. When implementation details in your production code change, you’ll need to update your tests to reflect these changes. Ideally, a good test should need to change only if user-facing behavior of an API changes; it should remain unaffected by changes to the API’s implementation.

打桩会把代码的实现细节引入测试。生产代码的实现细节一旦变化，就需要相应更新测试。理想情况下，只有 API 面向用户的行为发生变化时，好的测试才需要修改；API 内部实现的变化不应影响测试。

#### Tests become less effective 测试有效性降低

With stubbing, there is no way to ensure the function being stubbed behaves like the real implementation, such as in a statement like that shown in the following snippet that hardcodes part of the contract of the add() method (*“If 1 and 2 are passed in, 3* *will be returned”*):

打桩无法保证函数的行为与真实实现一致。例如，下面的语句硬编码了 add() 方法的部分契约（*“传入1和2时，返回3”*）：

```java
when(stubCalculator.add(1, 2)).thenReturn(3);
```

Stubbing is a poor choice if the system under test depends on the real implementation’s contract because you will be forced to duplicate the details of the contract, and there is no way to guarantee that the contract is correct (i.e., that the stubbed function has fidelity to the real implementation).

如果被测系统依赖真实实现的契约，打桩就不是一个好选择。你不得不重新定义契约的细节，却无法保证这些定义正确，也就无法保证打桩后的函数忠实于真实实现。

Additionally, with stubbing there is no way to store state, which can make it difficult to test certain aspects of your code. For example, if you call database.save(item) on either a real implementation or a fake, you might be able to retrieve the item by calling database.get(item.id()) given that both of these calls are accessing internal state, but with stubbing, there is no way to do this.

此外，打桩无法存储状态，这会增加测试某些代码行为的难度。例如，在真实实现或伪实现上调用 database.save(item) 后，可能可以通过 database.get(item.id()) 取回这条记录，因为两个调用都访问内部状态；但打桩无法做到这一点。

An example of overusing stubbing.

一个过度打桩的例子。

Example 13-13 illustrates a test that overuses stubbing.

例13-13展示了一个过度打桩的测试。

*Example* *13-13.* *Overuse* *of* *stubbing*

```java
@Test
public void creditCardIsCharged() {
    // Pass in test doubles that were created by a mocking framework.
    paymentProcessor = new PaymentProcessor(mockCreditCardServer, mockTransactionProcessor);
    // Set up stubbing for these test doubles. 
    when(mockCreditCardServer.isServerAvailable()).thenReturn(true);
    when(mockTransactionProcessor.beginTransaction()).thenReturn(transaction);
    when(mockCreditCardServer.initTransaction(transaction)).thenReturn(true);
    when(mockCreditCardServer.pay(transaction, creditCard, 500)).thenReturn(false);
    when(mockTransactionProcessor.endTransaction()).thenReturn(true);
    // Call the system under test.
    paymentProcessor.processPayment(creditCard, Money.dollars(500));
    // There is no way to tell if the pay() method actually carried out the
    // transaction, so the only thing the test can do is verify that the
    // pay() method was called.
    verify(mockCreditCardServer).pay(transaction, creditCard, 500);
}
```

Example 13-14 rewrites the same test but avoids using stubbing. Notice how the test is shorter and that implementation details (such as how the transaction processor is used) are not exposed in the test. No special setup is needed because the credit card server knows how to behave.

例13-14重写了同一个测试，但不再打桩。可以看到，测试更短了，也没有暴露交易处理器的用法等实现细节。由于信用卡服务器本身已经具备所需行为，不需要进行特殊设置。

*Example* *13-14.* *Refactoring* *a* *test* *to* *avoid* *stubbing*

```java
@Test
public void creditCardIsCharged() {
    paymentProcessor = new PaymentProcessor(creditCardServer, transactionProcessor);
    // Call the system under test.
    paymentProcessor.processPayment(creditCard, Money.dollars(500));
    // Query the credit card server state to see if the payment went through.
    assertThat(creditCardServer.getMostRecentCharge(creditCard)).isEqualTo(500);
}
```

We obviously don’t want such a test to talk to an external credit card server, so a fake credit card server would be more suitable. If a fake isn’t available, another option is to use a real implementation that talks to a hermetic credit card server, although this will increase the execution time of the tests. (We explore hermetic servers in the next chapter.)

显然，我们不希望这个测试连接外部信用卡服务器，因此使用信用卡服务器的伪实现更合适。如果没有伪实现，也可以使用与封闭信用卡服务器通信的真实实现，不过这会延长测试执行时间。（下一章将讨论封闭服务器。）

### When Is Stubbing Appropriate? 何时适合打桩？

Rather than a catch-all replacement for a real implementation, stubbing is appropriate when you need a function to return a specific value to get the system under test into a certain state, such as Example 13-12 that requires the system under test to return a non-empty list of transactions. Because a function’s behavior is defined inline in the test, stubbing can simulate a wide variety of return values or errors that might not be possible to trigger from a real implementation or a fake.

打桩并不是替代真实实现的通用办法。它适用于需要让函数返回特定值、使被测系统进入某种状态的情况，例如例13-12要求被测系统返回非空的交易列表。函数行为直接在测试中定义，因此打桩能够模拟各种返回值或错误，其中一些可能无法通过真实实现或伪实现触发。

To ensure its purpose is clear, each stubbed function should have a direct relationship with the test’s assertions. As a result, a test typically should stub out a small number of functions because stubbing out many functions can lead to tests that are less clear. A test that requires many functions to be stubbed can be a sign that stubbing is being overused, or that the system under test is too complex and should be refactored.

为了让打桩的目的明确，每个被打桩的函数都应与测试断言直接相关。因此，一个测试通常只应给少数函数打桩；打桩太多会让测试难以理解。如果一个测试需要给很多函数打桩，可能说明打桩已被滥用，或者被测系统过于复杂，需要重构。

Note that even when stubbing is appropriate, real implementations or fakes are still preferred because they don’t expose implementation details and they give you more guarantees about the correctness of the code compared to stubbing. But stubbing can be a reasonable technique to use, as long as its usage is constrained so that tests don’t become overly complex.

即使适合打桩，仍应优先考虑真实实现或伪实现。它们不会暴露实现细节，相比打桩，也能为代码的正确性提供更多保证。不过，只要控制使用范围，不让测试变得过于复杂，打桩仍是一种合理的技术。

## Interaction Testing  交互测试

As discussed earlier in this chapter, interaction testing is a way to validate how a function is called without actually calling the implementation of the function.

如前文所述，交互测试用于验证函数的调用方式，而不实际执行函数的实现。

Mocking frameworks make it easy to perform interaction testing. However, to keep tests useful, readable, and resilient to change, it’s important to perform interaction testing only when necessary.

模拟框架让交互测试变得容易。但要让测试有用、易读，又能适应代码变化，就应只在必要时使用交互测试。

### Prefer State Testing Over Interaction Testing 优先使用状态测试，而非交互测试

In contrast to interaction testing, it is preferred to test code through [*state* *testing*](https://oreil.ly/k3hSR).

测试代码时，应优先使用[*状态测试*](https://oreil.ly/k3hSR)，而非交互测试。

With state testing, you call the system under test and validate that either the correct value was returned or that some other state in the system under test was properly changed. Example 13-15 presents an example of state testing.

状态测试会调用被测系统，然后验证返回值是否正确，或系统中的其他状态是否已按预期改变。例13-15展示了一个状态测试。

*Example 13-15. State testing*

 ```java
 @Test
 public void sortNumbers() {
     NumberSorter numberSorter = new NumberSorter(quicksort, bubbleSort);
     // Call the system under test.
     List sortedList = numberSorter.sortNumbers(newList(3, 1, 2));
     // Validate that the returned list is sorted. It doesn’t matter which
     // sorting algorithm is used, as long as the right result was returned.
     assertThat(sortedList).isEqualTo(newList(1, 2, 3));
 }
 ```

Example 13-16 illustrates a similar test scenario but instead uses interaction testing. Note how it’s impossible for this test to determine that the numbers are actually sorted, because the test doubles don’t know how to sort the numbers—all it can tell you is that the system under test tried to sort the numbers.

 例13-16展示了类似场景，但改用交互测试。这个测试无法确认数字是否真的排好序，因为测试替身根本不会排序；它只能说明被测系统尝试过对数字排序。

*Example* *13-16.* *Interaction* *testing*

```java
@Test 
public void sortNumbers_quicksortIsUsed() {
    // Pass in test doubles that were created by a mocking framework.
    NumberSorter numberSorter = new NumberSorter(mockQuicksort, mockBubbleSort);
    // Call the system under test.
    numberSorter.sortNumbers(newList(3, 1, 2));
    // Validate that numberSorter.sortNumbers() used quicksort. The test
    // will fail if mockQuicksort.sort() is never called (e.g., if
    // mockBubbleSort is used) or if it’s called with the wrong arguments.
    verify(mockQuicksort).sort(newList(3, 1, 2));
}
```

At Google, we’ve found that emphasizing state testing is more scalable; it reduces test brittleness, making it easier to change and maintain code over time.

谷歌的经验是，以状态测试为主更适合大规模开发：它能降低测试的脆弱性，让代码在长期演进中更容易修改和维护。

The primary issue with interaction testing is that it can’t tell you that the system under test is working properly; it can only validate that certain functions are called as expected. It requires you to make an assumption about the behavior of the code; for example, “*If* *database.save(item) is called, we assume the item will be saved to the database.*” State testing is preferred because it actually validates this assumption (such as by saving an item to a database and then querying the database to validate that the item exists).

交互测试的主要问题在于，它无法说明被测系统是否正常工作，只能验证某些函数是否按预期被调用。因此，你必须假设代码会有某种行为，例如：“调用 *database.save(item)* 后，记录就会保存到数据库中。”状态测试更值得优先采用，因为它会实际验证这一假设，例如保存记录后再查询数据库，确认记录确实存在。

Another downside of interaction testing is that it utilizes implementation details of the system under test—to validate that a function was called, you are exposing to the test that the system under test calls this function. Similar to stubbing, this extra code makes tests brittle because it leaks implementation details of your production code into tests. Some people at Google jokingly refer to tests that overuse interaction testing as [*change-detector* *tests* ](https://oreil.ly/zkMDu)because they fail in response to any change to the production code, even if the behavior of the system under test remains unchanged.

交互测试的另一个缺点是依赖被测系统的实现细节：验证某个函数是否被调用，就等于让测试知道被测系统会调用这个函数。与打桩一样，这些额外代码把生产代码的实现细节引入测试，让测试变得脆弱。谷歌有人戏称这类过度依赖交互测试的测试为[*变更检测器测试*](https://oreil.ly/zkMDu)，因为即使被测系统的行为没有变化，生产代码的任何改动也会让它们失败。

### When Is Interaction Testing Appropriate? 什么时候适合进行交互测试？

There are some cases for which interaction testing is warranted:

- You cannot perform state testing because you are unable to use a real implementation or a fake (e.g., if the real implementation is too slow and no fake exists). As a fallback, you can perform interaction testing to validate that certain functions are called. Although not ideal, this does provide some basic level of confidence that the system under test is working as expected.
- Differences in the number or order of calls to a function would cause undesired behavior. Interaction testing is useful because it could be difficult to validate this behavior with state testing. For example, if you expect a caching feature to reduce the number of calls to a database, you can verify that the database object is not accessed more times than expected. Using Mockito, the code might look similar to this:

在某些情况下，交互测试是有必要的：

- 无法使用真实实现或伪实现，因而无法进行状态测试。例如，真实实现太慢，又没有现成的伪实现。此时可以退而使用交互测试，验证某些函数确实被调用。虽然不理想，但至少能为被测系统是否按预期工作提供一些基本信心。
- 函数调用的次数或顺序不同，会导致不希望出现的行为。状态测试可能很难验证这一点，此时交互测试就很有用。例如，如果希望缓存减少数据库调用，可以验证数据库对象的访问次数没有超过预期。使用 Mockito 时，代码可能如下：

```java
verify(databaseReader, atMostOnce()).selectRecords();
```

Interaction testing is not a complete replacement for state testing. If you are not able to perform state testing in a unit test, strongly consider supplementing your test suite with larger-scoped tests that do perform state testing. For instance, if you have a unit test that validates usage of a database through interaction testing, consider adding an integration test that can perform state testing against a real database. Larger-scope testing is an important strategy for risk mitigation, and we discuss it in the next chapter.

交互测试不能完全替代状态测试。如果单元测试无法进行状态测试，应认真考虑补充范围更大、能够检查状态的测试。例如，某个单元测试通过交互测试验证数据库的使用方式，就可以考虑添加集成测试，对真实数据库进行状态测试。扩大测试范围是降低风险的重要策略，下一章将进一步讨论。

#### Best Practices for Interaction Testing 交互测试的最佳实践

When performing interaction testing, following these practices can reduce some of the impact of the aforementioned downsides.

进行交互测试时，遵循以下实践可以减轻前述问题带来的部分影响。

#### Prefer to perform interaction testing only for state-changing functions  尽量只对改变状态的函数进行交互测试

When a system under test calls a function on a dependency, that call falls into one of two categories:
- *State-changing*
    Functions that have side effects on the world outside the system under test. Examples: 

```java
sendEmail(), saveRecord(), logAccess().
```

- *Non-state-changing*
Functions that don’t have side effects; they return information about the world outside the system under test and don’t modify anything. Examples: 
```java
getUser(), findResults(), readFile().
```

被测系统调用依赖中的函数时，调用可分为两类：

*改变状态*
	会对被测系统之外的环境产生副作用的函数。例如：

```java
sendEmail(), saveRecord(), logAccess().
```

- *不改变状态*
没有副作用的函数：返回被测系统之外的信息，但不作任何修改。例如：

```java
getUser(), findResults(), readFile()。
```

In general, you should perform interaction testing only for functions that are state- changing. Performing interaction testing for non-state-changing functions is usually redundant given that the system under test will use the return value of the function to do other work that you can assert. The interaction itself is not an important detail for correctness, because it has no side effects.

一般来说，只应对改变状态的函数进行交互测试。对于不改变状态的函数，被测系统会利用其返回值完成其他工作，而这些工作的结果可以用断言验证，因此额外验证交互通常是多余的。交互本身没有副作用，并不是决定正确性的关键细节。

Performing interaction testing for non-state-changing functions makes your test brittle because you’ll need to update the test anytime the pattern of interactions changes. It also makes the test less readable given that the additional assertions make it more difficult to determine which assertions are important for ensuring correctness of the code. By contrast, state-changing interactions represent something useful that your code is doing to change state somewhere else.

对不改变状态的函数进行交互测试，会让测试变得脆弱：交互方式一变，就得更新测试。额外的断言还会降低可读性，让人难以分清哪些断言才真正关系到代码的正确性。相比之下，改变状态的交互表明代码确实完成了有用的工作，改变了其他地方的状态。

Example 13-17 demonstrates interaction testing on both state-changing and non- state-changing functions.

例13-17展示了针对改变状态和不改变状态这两类函数的交互测试。

*Example 13-17. State-changing and non-state-changing interactions*  *例13-17：改变状态与不改变状态的交互*

```java
@Test
public void grantUserPermission() {
    UserAuthorizer userAuthorizer = new UserAuthorizer(mockUserService, mockPermissionDatabase);
    when(mockPermissionService.getPermission(FAKE_USER)).thenReturn(EMPTY);
    // Call the system under test.
    userAuthorizer.grantPermission(USER_ACCESS);
    // addPermission() is state-changing, so it is reasonable to perform
    // interaction testing to validate that it was called.
    verify(mockPermissionDatabase).addPermission(FAKE_USER, USER_ACCESS);
    // getPermission() is non-state-changing, so this line of code isn’t
    // needed. One clue that interaction testing may not be needed:
    // getPermission() was already stubbed earlier in this test.
    verify(mockPermissionDatabase).getPermission(FAKE_USER);
}
```

#### Avoid overspecification 避免过度限定

In Chapter 12, we discuss why it is useful to test behaviors rather than methods. This means that a test method should focus on verifying one behavior of a method or class rather than trying to verify multiple behaviors in a single test.

第12章讨论了为什么应围绕行为而不是方法编写测试。也就是说，一个测试方法应专注于验证某个方法或类的一种行为，而不是在同一个测试中验证多种行为。

When performing interaction testing, we should aim to apply the same principle by avoiding overspecifying which functions and arguments are validated. This leads to tests that are clearer and more concise. It also leads to tests that are resilient to changes made to behaviors that are outside the scope of each test, so fewer tests will fail if a change is made to a way a function is called.

交互测试也应遵循这一原则，避免对要验证的函数和参数作出过多限定。这样测试会更清晰、更简洁，也能不受测试范围之外的行为变化影响。因此，即使某个函数的调用方式改变，也只会有较少的测试失败。

Example 13-18 illustrates interaction testing with overspecification. The intention of the test is to validate that the user’s name is included in the greeting prompt, but the test will fail if unrelated behavior is changed.

例13-18展示了限定过多的交互测试。它本来只想验证问候提示中是否包含用户姓名，但无关行为的变化也会让测试失败。

 *Example* *13-18.* *Overspecified* *interaction* *tests*

```java
@Test public void displayGreeting_renderUserName() {
    when(mockUserService.getUserName()).thenReturn("Fake User");
    userGreeter.displayGreeting();
    // Call the system under test.
    // The test will fail if any of the arguments to setText() are changed.
    verify(userPrompt).setText("Fake User", "Good morning!", "Version 2.1");
    // The test will fail if setIcon() is not called, even though this
    // behavior is incidental to the test since it is not related to
    // validating the user name.
    verify(userPrompt).setIcon(IMAGE_SUNSHINE);
}
```

[Example 13-19](#_bookmark1176) illustrates interaction testing with more care in specifying relevant arguments and functions. The behaviors being tested are split into separate tests, and each test validates the minimum amount necessary for ensuring the behavior it is testing is correct.

例13-19在指定要验证的参数和函数时更加谨慎。不同的行为分别由独立的测试验证，每个测试只检查确认相应行为正确所必需的最少内容。

 *Example 13-19. Well-specified interaction tests*  *例13-19：限定恰当的交互测试*

```java
@Test 
public void displayGreeting_renderUserName() {
    when(mockUserService.getUserName()).thenReturn("Fake User");
    userGreeter.displayGreeting(); // Call the system under test. 
    verify(userPrompter).setText(eq("Fake User"), any(), any());
}

@Test 
public void displayGreeting_timeIsMorning_useMorningSettings() {
    setTimeOfDay(TIME_MORNING);
    userGreeter.displayGreeting(); // Call the system under test. 
    verify(userPrompt).setText(any(), eq("Good morning!"), any());
    verify(userPrompt).setIcon(IMAGE_SUNSHINE);
}
```

## Conclusion 总结

We’ve learned that test doubles are crucial to engineering velocity because they can help comprehensively test your code and ensure that your tests run fast. On the other hand, misusing them can be a major drain on productivity because they can lead to tests that are unclear, brittle, and less effective. This is why it’s important for engineers to understand the best practices for how to effectively apply test doubles.

测试替身对开发速度至关重要：它们有助于全面测试代码，并确保测试快速运行。但使用不当也可能严重损害生产力，让测试含义不清、变得脆弱，有效性降低。因此，对工程师而言，了解有效使用测试替身的最佳实践十分重要。

There is often no exact answer regarding whether to use a real implementation or a test double, or which test double technique to use. An engineer might need to make some trade-offs when deciding the proper approach for their use case.

应该使用真实实现还是测试替身，又该选择哪种测试替身技术，往往没有确切答案。工程师在为具体场景选择合适方法时，可能需要作出一些权衡。

Although test doubles are great for working around dependencies that are difficult to use in tests, if you want to maximize confidence in your code, at some point you still want to exercise these dependencies in tests. The next chapter will cover larger-scope testing, for which these dependencies are used regardless of their suitability for unit tests; for example, even if they are slow or nondeterministic.

测试替身能帮助绕过难以用于测试的依赖，但要尽可能确信代码正确，最终仍需在测试中实际运行这些依赖。下一章将介绍范围更大的测试：即使依赖运行缓慢或具有非确定性，不适合单元测试，也仍会纳入这些测试。

## TL;DRs  内容提要

- A real implementation should be preferred over a test double.
- A fake is often the ideal solution if a real implementation can’t be used in a test.
- Overuse of stubbing leads to tests that are unclear and brittle.
- Interaction testing should be avoided when possible: it leads to tests that are brittle because it exposes implementation details of the system under test.

- 应优先使用真实实现，而非测试替身。
- 如果测试无法使用真实实现，伪实现通常是理想选择。
- 过度打桩会让测试含义不清、变得脆弱。
- 应尽可能避免交互测试，因为它会暴露被测系统的实现细节，让测试变得脆弱。
