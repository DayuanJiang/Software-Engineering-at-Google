def test_should_allow_multiple_users():
    users = create_users(False, False)
    forum = create_forum_and_register_users(users)
    validate_forum_and_users(forum, users)

def test_should_not_allow_banned_users():
    users = create_users(True)
    forum = create_forum_and_register_users(users)
    validate_forum_and_users(forum, users)

# Lots more tests...

def create_users(*banned):
    users = []
    for is_banned in banned:
        users.append(new_user(state=State.BANNED if is_banned else State.NORMAL))
    return users

def create_forum_and_register_users(users):
    forum = Forum()
    for user in users:
        try:
            forum.register(user)
        except BannedUserError:
            pass
    return forum

def validate_forum_and_users(forum, users):
    assert forum.is_reachable()
    for user in users:
        assert forum.has_registered_user(user) == (user.state == State.BANNED)
