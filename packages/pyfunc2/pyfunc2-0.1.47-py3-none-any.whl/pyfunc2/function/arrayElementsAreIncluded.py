# difference between two arrays
def arrayElementsAreIncluded(array_a, array_b):
    # Convert both lists to sets
    set_a = set(array_a)
    set_b = set(array_b)

    # Check if set A is a subset of set B
    return set_a.issubset(set_b)