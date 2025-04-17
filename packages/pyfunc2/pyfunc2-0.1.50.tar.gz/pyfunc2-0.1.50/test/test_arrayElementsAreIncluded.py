import pytest
from pyfunc2.function.arrayElementsAreIncluded import arrayElementsAreIncluded

def test_arrayElementsAreIncluded_true():
    assert arrayElementsAreIncluded([1, 2], [1, 2, 3]) is True

def test_arrayElementsAreIncluded_false():
    assert arrayElementsAreIncluded([1, 4], [1, 2, 3]) is False
