def test_should_navigate_to_photos_page():
    nav = Navigator("http://photos.google.com/")
    nav.go_to_photos_page()
    assert nav.current_url == "http://photos.google.com//albums"  # Oops!
