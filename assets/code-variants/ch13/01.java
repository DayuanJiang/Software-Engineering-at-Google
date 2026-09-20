class PaymentProcessor {
  private CreditCardService creditCardService;
  ...
  boolean makePayment(CreditCard creditCard, Money amount) {
    if (creditCard.isExpired()) { return false; }
    boolean success = creditCardService.chargeCreditCard(creditCard,  amount);
    return success;
  }
}
