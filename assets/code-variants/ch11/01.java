// Verifies a Calculator class can handle negative results.
public void main(String[] args) {
	Calculator calculator = new Calculator();
	int expectedResult = -3;
	int actualResult = calculator.subtract(2, 5); // Given 2, Subtracts 5.
	assert(expectedResult == actualResult);
}
