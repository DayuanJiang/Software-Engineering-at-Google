class PaymentProcessor:
    _credit_card_service: CreditCardService
    ...
    def make_payment(self, credit_card, amount):
        if credit_card.is_expired():
            return False
        success = self._credit_card_service.charge_credit_card(credit_card, amount)
        return success
