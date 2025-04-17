from pyfunc2.function.differenceElementsInArrays import differenceElementsInArrays

def test_differenceElementsInArrays_basic():
    assert sorted(differenceElementsInArrays([1, 2, 3], [2, 3, 4])) == [1]

def test_differenceElementsInArrays_empty():
    assert differenceElementsInArrays([], [1, 2]) == []

def test_differenceElementsInArrays_no_diff():
    assert differenceElementsInArrays([1, 2], [1, 2]) == []
