def test_card_is_expired_return_false():
    success = payment_processor.make_payment(EXPIRED_CARD, AMOUNT)
    assert not success
