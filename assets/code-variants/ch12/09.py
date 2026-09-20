def test_display_transaction_results():
    transaction_processor.display_transaction_results(
        new_user_with_balance(LOW_BALANCE_THRESHOLD + dollars(2)), Transaction("Some Item", dollars(3)))
    assert "You bought a Some Item" in ui.get_text()
    assert "your balance is low" in ui.get_text()
