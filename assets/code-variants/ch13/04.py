class PaymentProcessor:
    _credit_card_service: CreditCardService

    def __init__(self, credit_card_service):
        self._credit_card_service = credit_card_service
    ...
