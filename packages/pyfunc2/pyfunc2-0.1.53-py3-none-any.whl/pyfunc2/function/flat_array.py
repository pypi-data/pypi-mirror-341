# take two arrays and returns a list of the elements that are not in both arrays
def flat_array(original_array, by_name='value'):
    return [element[by_name] for element in original_array]