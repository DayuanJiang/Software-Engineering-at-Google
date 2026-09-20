def test_should_allow_multiple_users():
    user1 = new_user(state=State.NORMAL)
    user2 = new_user(state=State.NORMAL)

    forum = Forum()
    forum.register(user1)
    forum.register(user2)

    assert forum.has_registered_user(user1)
    assert forum.has_registered_user(user2)

def test_should_not_register_banned_users():
    user = new_user(state=State.BANNED)

    forum = Forum()
    try:
        forum.register(user)
    except BannedUserError:
        pass

    assert not forum.has_registered_user(user)
