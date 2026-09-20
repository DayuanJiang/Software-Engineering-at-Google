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
