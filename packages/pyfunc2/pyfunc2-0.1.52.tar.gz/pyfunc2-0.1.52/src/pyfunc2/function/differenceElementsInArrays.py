# difference between two arrays
def differenceElementsInArrays(array_a, array_b):
    # Convert both arrays to sets
    set_a = set(array_a)
    set_b = set(array_b)

    # Return the difference
    return list(set_a - set_b)