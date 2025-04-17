import re

def remove_only_single_spaces(text):
    return re.sub(r'(?<=\S) (?=\S)', '', text)