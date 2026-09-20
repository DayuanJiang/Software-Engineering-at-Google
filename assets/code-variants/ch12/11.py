def test_transfer_funds_should_move_money_between_accounts():
    # Given two accounts with initial balances of $150 and $20
    account1 = new_account_with_balance(usd(150))
    account2 = new_account_with_balance(usd(20))
    # When transferring $100 from the first to the second account
    bank.transfer_funds(account1, account2, usd(100))
    # Then the new account balances should reflect the transfer
    assert account1.balance == usd(50)
    assert account2.balance == usd(120)
