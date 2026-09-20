@Test
public void testDisplayTransactionResults() {
transactionProcessor.displayTransactionResults(newUserWithBalance(LOW_BALANCE_THRESHOLD.plus(dollars(2))), new Transaction("Some Item", dollars(3)));
    assertThat(ui.getText()).contains("You bought a Some Item");
    assertThat(ui.getText()).contains("your balance is low");
}
