import re
import os


def get_url_list(markdown, pattern=r'\[([^\]]+)\]\(([^)]+)\)'):
    # regex pattern to match all markdown links
    link_pattern = re.compile(pattern)
    # extract all matches
    links = link_pattern.findall(markdown)

    # links is a list of tuples where the first element is the link text and the second is the url
    # if you only want the urls, you can do the following:
    url_list = [url for text, url in links]

    return url_list
