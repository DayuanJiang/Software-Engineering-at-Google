# pytest lets nested classes play the role of describe() blocks.
class TestMultiplication:
    class TestWithAPositiveNumber:
        positive_number = 10

        def test_is_positive_with_another_positive_number(self):
            assert self.positive_number * 10 > 0

        def test_is_negative_with_a_negative_number(self):
            assert self.positive_number * -10 < 0

    class TestWithANegativeNumber:
        negative_number = 10

        def test_is_negative_with_a_positive_number(self):
            assert self.negative_number * 10 < 0

        def test_is_positive_with_another_negative_number(self):
            assert self.negative_number * -10 > 0
