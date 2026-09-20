def test_credit_card_is_charged():
    payment_processor = PaymentProcessor(credit_card_server, transaction_processor)
    # Call the system under test.
    payment_processor.process_payment(credit_card, Money.dollars(500))
    # Query the credit card server state to see if the payment went through.
    assert credit_card_server.get_most_recent_charge(credit_card) == 500
