def assert_user_has_access_to_account(user, account):
    for user_id in account.users_with_access:
        if user.id == user_id:
            return
    pytest.fail(f"{user.name} cannot access {account.name}")
