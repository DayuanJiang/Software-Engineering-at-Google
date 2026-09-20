@Test 
public void displayGreeting_renderUserName() {
    when(mockUserService.getUserName()).thenReturn("Fake User");
    userGreeter.displayGreeting(); // Call the system under test. 
    verify(userPrompter).setText(eq("Fake User"), any(), any());
}

@Test 
public void displayGreeting_timeIsMorning_useMorningSettings() {
    setTimeOfDay(TIME_MORNING);
    userGreeter.displayGreeting(); // Call the system under test. 
    verify(userPrompt).setText(any(), eq("Good morning!"), any());
    verify(userPrompt).setIcon(IMAGE_SUNSHINE);
}
