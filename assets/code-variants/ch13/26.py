def test_sort_numbers():
    number_sorter = NumberSorter(quicksort, bubble_sort)
    # Call the system under test.
    sorted_list = number_sorter.sort_numbers([3, 1, 2])
    # Validate that the returned list is sorted. It doesn't matter which
    # sorting algorithm is used, as long as the right result was returned.
    assert sorted_list == [1, 2, 3]
