def test_display_greeting_render_user_name():
    mock_user_service.get_user_name.return_value = "Fake User"
    user_greeter.display_greeting()  # Call the system under test.
    user_prompter.set_text.assert_called_with("Fake User", ANY, ANY)

def test_display_greeting_time_is_morning_use_morning_settings():
    set_time_of_day(TIME_MORNING)
    user_greeter.display_greeting()  # Call the system under test.
    user_prompt.set_text.assert_called_with(ANY, "Good morning!", ANY)
    user_prompt.set_icon.assert_called_with(IMAGE_SUNSHINE)
