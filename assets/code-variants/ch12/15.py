def test_should_navigate_to_albums_page():
    base_url = "http://photos.google.com/"
    nav = Navigator(base_url)
    nav.go_to_album_page()
    assert nav.current_url == base_url + "/albums"
