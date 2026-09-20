def test_should_perform_addition():
    calculator = Calculator(RoundingStrategy(), "unused", ENABLE_COSINE_FEATURE, 0.01, calculus_engine, False)
    result = calculator.calculate(new_test_calculation())
    assert result == 5  # Where did this number come from?
