def test_should_perform_addition():
    calculator = new_calculator()
    result = calculator.calculate(new_calculation(2, Operation.PLUS, 3))
    assert result == 5
