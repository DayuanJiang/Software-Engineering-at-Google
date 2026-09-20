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
