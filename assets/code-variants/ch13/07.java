// Creating the fake is fast and easy.
AuthorizationService fakeAuthorizationService = new FakeAuthorizationService();
AccessManager accessManager = new AccessManager(fakeAuthorizationService):

// Unknown user IDs shouldn’t have access.
assertFalse(accessManager.userHasAccess(USER_ID));

// The user ID should have access after it is added to
// the authorization service. 
fakeAuthorizationService.addAuthorizedUser(new User(USER_ID));
assertThat(accessManager.userHasAccess(USER_ID)).isTrue();
