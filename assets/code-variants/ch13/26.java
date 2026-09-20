@Test
public void sortNumbers() {
    NumberSorter numberSorter = new NumberSorter(quicksort, bubbleSort);
    // Call the system under test.
    List sortedList = numberSorter.sortNumbers(newList(3, 1, 2));
    // Validate that the returned list is sorted. It doesn’t matter which
    // sorting algorithm is used, as long as the right result was returned.
    assertThat(sortedList).isEqualTo(newList(1, 2, 3));
}
