class UserStoreTest(unittest.TestCase):
    def setUp(self):
        self.name_service = NameService()
        self.name_service.set("user1", "Donald Knuth")
        self.user_store = UserStore(self.name_service)

    # [... hundreds of lines of tests ...]

    def test_should_return_name_from_service(self):
        user = self.user_store.get("user1")
        self.assertEqual(user.name, "Donald Knuth")
