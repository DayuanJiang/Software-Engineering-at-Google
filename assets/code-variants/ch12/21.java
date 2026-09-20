@Test
public void shouldAllowMultipleUsers() {
    List < User > users = createUsers(false, false);
    Forum forum = createForumAndRegisterUsers(users);
    validateForumAndUsers(forum, users);
}

@Test
public void shouldNotAllowBannedUsers() {
        List < User > users = createUsers(true);
        Forum forum = createForumAndRegisterUsers(users);
        validateForumAndUsers(forum, users);
}

// Lots more tests...
private static List < User > createUsers(boolean...banned) {
    List < User > users = new ArrayList < > ();
    for(boolean isBanned: banned) {
        users.add(newUser().setState(isBanned ? State.BANNED : State.NORMAL).build());
    }
    return users;
}

private static Forum createForumAndRegisterUsers(List < User > users) {
    Forum forum = new Forum();
    for(User user: users) {
        try {
            forum.register(user);
        } catch(BannedUserException ignored) {}
    }
    return forum;
}

private static void validateForumAndUsers(Forum forum, List < User > users) {
    assertThat(forum.isReachable()).isTrue();
    for(User user: users) {
        assertThat(forum.hasRegisteredUser(user)).isEqualTo(user.getState() == State.BANNED);
    }
}
