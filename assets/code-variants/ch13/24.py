def test_display_greeting_render_user_name():
    mock_user_service.get_user_name.return_value = "Fake User"
    user_greeter.display_greeting()
    # Call the system under test.
    # The test will fail if any of the arguments to set_text() are changed.
    user_prompt.set_text.assert_called_with("Fake User", "Good morning!", "Version 2.1")
    # The test will fail if set_icon() is not called, even though this
    # behavior is incidental to the test since it is not related to
    # validating the user name.
    user_prompt.set_icon.assert_called_with(IMAGE_SUNSHINE)
