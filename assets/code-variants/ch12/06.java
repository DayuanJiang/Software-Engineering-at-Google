@Test
public void shouldPerformAddition() {
    Calculator calculator = new Calculator(new RoundingStrategy(), "unused", ENABLE_COSINE_FEATURE, 0.01, calculusEngine, false);
    int result = calculator.calculate(newTestCalculation());
    assertThat(result).isEqualTo(5); // Where did this number come from?
}
