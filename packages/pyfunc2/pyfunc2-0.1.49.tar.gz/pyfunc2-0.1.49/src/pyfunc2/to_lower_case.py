

def convert_char(char):
    if char >= 'A' and char <= 'Z':
        return chr(ord(char) + 32)
    return char


def to_lower_case(string):
    newString = []
    for char in string:
        newString.append(convert_char(char))
    return ''.join(newString)