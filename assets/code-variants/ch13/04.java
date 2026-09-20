class PaymentProcessor {
  private CreditCardService creditCardService;

  PaymentProcessor(CreditCardService creditCardService) {
    this.creditCardService = creditCardService;
  }
  ...
}
