@Test
public void shouldNavigateToPhotosPage() {
    Navigator nav = new Navigator("http://photos.google.com/");
    nav.goToPhotosPage();
    assertThat(nav.getCurrentUrl())).isEqualTo("http://photos.google.com//albums"); // Oops!
}
