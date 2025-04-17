
def multiple_search(text, search_list=[], text_list_out=[]):
    text_occ_list = {}
    # print(search_list)

    for search in search_list:

        matches = text.find(search)
        # print(text, search, matches, len(search))
        # print(search, matches, len(search))

        if matches >= 0:
            # text_list_out.append(text)
            text_occ_list[search] = matches

    sorted(text_occ_list)
    # print("text_occ_list: ", text_occ_list)
    text_list_out = list(text_occ_list.keys())

    # print("text_list_out: ", text_list_out)

    return text_list_out
