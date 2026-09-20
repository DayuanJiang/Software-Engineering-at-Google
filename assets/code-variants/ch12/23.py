ACCOUNT_1 = Account(state=AccountState.OPEN, balance=50)

ACCOUNT_2 = Account(state=AccountState.CLOSED, balance=0)

ITEM = Item(name="Cheeseburger", price=100)

# Hundreds of lines of other tests...

def test_can_buy_item_returns_false_for_closed_accounts():
    assert not store.can_buy_item(ITEM, ACCOUNT_1)

def test_can_buy_item_returns_false_when_balance_insufficient():
    assert not store.can_buy_item(ITEM, ACCOUNT_2)
