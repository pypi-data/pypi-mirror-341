import re


def find_words(text):
    pattern = r'\b\w+\b'
    words = re.findall(pattern, text)

    return words


def test():
    text = "Hello, world! Python is a great language, isn't it?"
    words = find_words(text)

    for word in words:
        print(word)
