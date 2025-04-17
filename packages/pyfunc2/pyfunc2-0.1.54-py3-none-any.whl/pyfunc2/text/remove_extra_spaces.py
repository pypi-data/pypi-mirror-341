
# https://dateutil.readthedocs.io/en/stable/parser.html
# pip install python-dateutil
def remove_extra_spaces(text):
    no_extra_spaces_text = ' '.join(text.split())
    return no_extra_spaces_text

