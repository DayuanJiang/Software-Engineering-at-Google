# Pass in a test double that was created by a mocking framework.
access_manager = AccessManager(mock_authorization_service)

# The user ID shouldn't have access if None is returned.
mock_authorization_service.lookup_user.return_value = None
assert not access_manager.user_has_access(USER_ID)

# The user ID should have access if a non-None value is returned.
mock_authorization_service.lookup_user.return_value = USER
assert access_manager.user_has_access(USER_ID)
