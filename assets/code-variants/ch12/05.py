def test_should_create_users():
    accounts.create_user("foobar")
    assert accounts.get_user("foobar") is not None
