class PaymentProcessorTest(unittest.TestCase):
    ...
    def setUp(self):
        # Create a test double of CreditCardService with just one line of code.
        self.mock_credit_card_service = Mock(spec=CreditCardService)
        # Pass in the test double to the system under test.
        self.payment_processor = PaymentProcessor(self.mock_credit_card_service)

    def test_charge_credit_card_fails_return_false(self):
        # Give some behavior to the test double: it will return False
        # anytime the charge_credit_card() method is called, regardless of
        # which arguments are passed.
        self.mock_credit_card_service.charge_credit_card.return_value = False
        success = self.payment_processor.make_payment(CREDIT_CARD, AMOUNT)
        self.assertFalse(success)
