def test_should_write_to_database():
    accounts.create_user("foobar")
    database.put.assert_called_with("foobar")
