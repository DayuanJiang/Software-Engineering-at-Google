def test_empty_account_should_not_be_valid():
    assert not processor._is_valid(new_transaction(sender=EMPTY_ACCOUNT))

def test_should_save_serialized_data():
    processor._save_to_database(new_transaction(id=123, sender="me", recipient="you", amount=100))
    assert database.get(123) == "me,you,100"
