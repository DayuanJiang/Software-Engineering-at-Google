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
