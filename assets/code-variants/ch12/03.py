def test_should_transfer_funds():
    processor.set_account_balance("me", 150)
    processor.set_account_balance("you", 20)
    processor.process_transaction(new_transaction(sender="me", recipient="you", amount=100))
    assert processor.get_account_balance("me") == 50
    assert processor.get_account_balance("you") == 120

def test_should_not_perform_invalid_transactions():
    processor.set_account_balance("me", 50)
    processor.set_account_balance("you", 20)
    processor.process_transaction(new_transaction(sender="me", recipient="you", amount=100))
    assert processor.get_account_balance("me") == 50
    assert processor.get_account_balance("you") == 20
