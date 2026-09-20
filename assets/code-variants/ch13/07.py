# Creating the fake is fast and easy.
fake_authorization_service = FakeAuthorizationService()
access_manager = AccessManager(fake_authorization_service)

# Unknown user IDs shouldn't have access.
assert not access_manager.user_has_access(USER_ID)

# The user ID should have access after it is added to
# the authorization service.
fake_authorization_service.add_authorized_user(User(USER_ID))
assert access_manager.user_has_access(USER_ID)
