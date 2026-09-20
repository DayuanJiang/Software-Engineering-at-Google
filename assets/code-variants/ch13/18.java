@Test 
public void sortNumbers_quicksortIsUsed() {
    // Pass in test doubles that were created by a mocking framework.
    NumberSorter numberSorter = new NumberSorter(mockQuicksort, mockBubbleSort);
    // Call the system under test.
    numberSorter.sortNumbers(newList(3, 1, 2));
    // Validate that numberSorter.sortNumbers() used quicksort. The test
    // will fail if mockQuicksort.sort() is never called (e.g., if
    // mockBubbleSort is used) or if it’s called with the wrong arguments.
    verify(mockQuicksort).sort(newList(3, 1, 2));
}
