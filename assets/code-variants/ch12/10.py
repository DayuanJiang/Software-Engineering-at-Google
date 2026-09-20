def test_display_transaction_results_shows_item_name():
    transaction_processor.display_transaction_results(User(), Transaction("Some Item"))
    assert "You bought a Some Item" in ui.get_text()

def test_display_transaction_results_shows_low_balance_warning():
    transaction_processor.display_transaction_results(
        new_user_with_balance(LOW_BALANCE_THRESHOLD + dollars(2)), Transaction("Some Item", dollars(3)))
    assert "your balance is low" in ui.get_text()
