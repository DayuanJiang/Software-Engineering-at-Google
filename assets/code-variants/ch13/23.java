@Test
public void grantUserPermission() {
    UserAuthorizer userAuthorizer = new UserAuthorizer(mockUserService, mockPermissionDatabase);
    when(mockPermissionService.getPermission(FAKE_USER)).thenReturn(EMPTY);
    // Call the system under test.
    userAuthorizer.grantPermission(USER_ACCESS);
    // addPermission() is state-changing, so it is reasonable to perform
    // interaction testing to validate that it was called.
    verify(mockPermissionDatabase).addPermission(FAKE_USER, USER_ACCESS);
    // getPermission() is non-state-changing, so this line of code isn’t
    // needed. One clue that interaction testing may not be needed:
    // getPermission() was already stubbed earlier in this test.
    verify(mockPermissionDatabase).getPermission(FAKE_USER);
}
