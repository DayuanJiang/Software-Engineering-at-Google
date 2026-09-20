# Verifies a Calculator class can handle negative results.
def main():
    calculator = Calculator()
    expected_result = -3
    actual_result = calculator.subtract(2, 5)  # Given 2, Subtracts 5.
    assert expected_result == actual_result
