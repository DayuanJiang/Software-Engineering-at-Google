def test_grant_user_permission():
    user_authorizer = UserAuthorizer(mock_user_service, mock_permission_database)
    mock_permission_service.get_permission.return_value = EMPTY
    # Call the system under test.
    user_authorizer.grant_permission(USER_ACCESS)
    # add_permission() is state-changing, so it is reasonable to perform
    # interaction testing to validate that it was called.
    mock_permission_database.add_permission.assert_called_with(FAKE_USER, USER_ACCESS)
    # get_permission() is non-state-changing, so this line of code isn't
    # needed. One clue that interaction testing may not be needed:
    # get_permission() was already stubbed earlier in this test.
    mock_permission_database.get_permission.assert_called_with(FAKE_USER)
