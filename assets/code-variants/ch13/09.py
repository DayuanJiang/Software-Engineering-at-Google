# Pass in a test double that was created by a mocking framework.
access_manager = AccessManager(mock_authorization_service)
access_manager.user_has_access(USER_ID)

# The test will fail if access_manager.user_has_access(USER_ID) didn't call
# mock_authorization_service.lookup_user(USER_ID).
mock_authorization_service.lookup_user.assert_called_with(USER_ID)
