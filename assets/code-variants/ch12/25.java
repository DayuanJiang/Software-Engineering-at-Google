private NameService nameService;
private UserStore userStore;

@Before
public void setUp() {
    nameService = new NameService();
    nameService.set("user1", "Donald Knuth");
    userStore = new UserStore(nameService);
}

// [... hundreds of lines of tests ...]

@Test
public void shouldReturnNameFromService() {
    UserDetails user = userStore.get("user1");
    assertThat(user.getName()).isEqualTo("Donald Knuth");
}
