@Test public void getTransactionCount() {
transactionCounter = new TransactionCounter(mockCreditCardServer);
// Use stubbing to return three transactions.
when(mockCreditCardServer.getTransactions()).thenReturn( newList(TRANSACTION_1, TRANSACTION_2, TRANSACTION_3));
assertThat(transactionCounter.getTransactionCount()).isEqualTo(3);
}
