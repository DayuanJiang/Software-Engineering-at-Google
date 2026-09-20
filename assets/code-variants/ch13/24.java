@Test public void displayGreeting_renderUserName() {
    when(mockUserService.getUserName()).thenReturn("Fake User");
    userGreeter.displayGreeting();
    // Call the system under test.
    // The test will fail if any of the arguments to setText() are changed.
    verify(userPrompt).setText("Fake User", "Good morning!", "Version 2.1");
    // The test will fail if setIcon() is not called, even though this
    // behavior is incidental to the test since it is not related to
    // validating the user name.
    verify(userPrompt).setIcon(IMAGE_SUNSHINE);
}
