class TestDoubleCreditCardService implements CreditCardService {
  @Override
  public boolean chargeCreditCard(CreditCard creditCard, Money amount) {
    return true;
  }
}
