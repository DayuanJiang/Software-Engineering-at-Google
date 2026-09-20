@Test
public void emptyAccountShouldNotBeValid() {
    assertThat(processor.isValid(newTransaction().setSender(EMPTY_ACCOUNT))).isFalse();
}

@Test
public void shouldSaveSerializedData() {
    processor.saveToDatabase(newTransaction().setId(123).setSender("me").setRecipient("you").setAmount(100));
    assertThat(database.get(123)).isEqualTo("me,you,100");
}
