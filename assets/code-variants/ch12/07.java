@Test
public void shouldPerformAddition() { 
    Calculator calculator = newCalculator();
    int result = calculator.calculate(newCalculation(2, Operation.PLUS, 3));
    assertThat(result).isEqualTo(5);
}
