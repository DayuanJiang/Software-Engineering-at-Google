def test_get_transaction_count():
    transaction_counter = TransactionCounter(mock_credit_card_server)
    # Use stubbing to return three transactions.
    mock_credit_card_server.get_transactions.return_value = [TRANSACTION_1, TRANSACTION_2, TRANSACTION_3]
    assert transaction_counter.get_transaction_count() == 3
