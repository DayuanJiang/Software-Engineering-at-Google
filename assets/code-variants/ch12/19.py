colors = frozenset({"red", "green", "blue"})
self.assertTrue("orange" in colors)  # unittest, in the JUnit style
self.assertIn("orange", colors)      # a matcher-style assertion, in the Truth style
