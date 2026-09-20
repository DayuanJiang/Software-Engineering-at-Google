def test_sort_numbers_quicksort_is_used():
    # Pass in test doubles that were created by a mocking framework.
    number_sorter = NumberSorter(mock_quicksort, mock_bubble_sort)
    # Call the system under test.
    number_sorter.sort_numbers([3, 1, 2])
    # Validate that number_sorter.sort_numbers() used quicksort. The test
    # will fail if mock_quicksort.sort() is never called (e.g., if
    # mock_bubble_sort is used) or if it's called with the wrong arguments.
    mock_quicksort.sort.assert_called_with([3, 1, 2])
