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
