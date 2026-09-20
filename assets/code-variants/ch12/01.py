def process_transaction(self, transaction):
    if self._is_valid(transaction):
        self._save_to_database(transaction)

def _is_valid(self, t):
    return t.amount < t.sender.balance

def _save_to_database(self, t):
    s = f"{t.sender},{t.recipient},{t.amount}"
    self.database.put(t.id, s)

def set_account_balance(self, account_name, balance):
    # Write the balance to the database directly
    ...

def get_account_balance(self, account_name):
    # Read transactions from the database to determine the account balance
    ...
