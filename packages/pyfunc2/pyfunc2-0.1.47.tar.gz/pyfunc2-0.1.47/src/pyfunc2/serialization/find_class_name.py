import re

def find_class_name(pattern, sentence):
    result = re.search(pattern, sentence)
    if result:
        return result.group(1)
    else:
        return None