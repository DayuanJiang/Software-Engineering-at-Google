@Test
public void creditCardIsCharged() {
    paymentProcessor = new PaymentProcessor(creditCardServer, transactionProcessor);
    // Call the system under test.
    paymentProcessor.processPayment(creditCard, Money.dollars(500));
    // Query the credit card server state to see if the payment went through.
    assertThat(creditCardServer.getMostRecentCharge(creditCard)).isEqualTo(500);
}
