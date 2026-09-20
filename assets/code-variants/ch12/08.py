def display_transaction_results(self, user, transaction):
    self.ui.show_message(f"You bought a {transaction.item_name}")
    if user.balance < LOW_BALANCE_THRESHOLD:
        self.ui.show_message("Warning: your balance is low!")
