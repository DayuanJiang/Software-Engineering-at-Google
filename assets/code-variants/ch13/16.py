def test_credit_card_is_charged():
    # Pass in test doubles that were created by a mocking framework.
    payment_processor = PaymentProcessor(mock_credit_card_server, mock_transaction_processor)
    # Set up stubbing for these test doubles.
    mock_credit_card_server.is_server_available.return_value = True
    mock_transaction_processor.begin_transaction.return_value = transaction
    mock_credit_card_server.init_transaction.return_value = True
    mock_credit_card_server.pay.return_value = False
    mock_transaction_processor.end_transaction.return_value = True
    # Call the system under test.
    payment_processor.process_payment(credit_card, Money.dollars(500))
    # There is no way to tell if the pay() method actually carried out the
    # transaction, so the only thing the test can do is verify that the
    # pay() method was called.
    mock_credit_card_server.pay.assert_called_with(transaction, credit_card, 500)
