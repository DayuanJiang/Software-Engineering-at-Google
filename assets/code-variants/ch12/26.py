class UserStoreTest(unittest.TestCase):
    def setUp(self):
        self.name_service = NameService()
        self.name_service.set("user1", "Donald Knuth")
        self.user_store = UserStore(self.name_service)

    def test_should_return_name_from_service(self):
        self.name_service.set("user1", "Margaret Hamilton")
        user = self.user_store.get("user1")
        self.assertEqual(user.name, "Margaret Hamilton")
