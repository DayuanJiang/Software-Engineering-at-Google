private void assertUserHasAccessToAccount(User user, Account account) {
    for(long userId: account.getUsersWithAccess()) {
        if(user.getId() == userId) {
            return;
        }
    }
    fail(user.getName() + " cannot access " + account.getName());
}
