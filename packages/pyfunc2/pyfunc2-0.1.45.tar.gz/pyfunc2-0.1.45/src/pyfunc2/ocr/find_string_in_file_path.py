import os
import sys

sys.path.append('../')

from .find_string_in_pdf import find_string_in_pdf


def find_string_in_file_path(paths, find_text, extension_list=['.pdf']):
    root = '../'
    found_text_list = []
    # path = os.path.join(root, source)
    if not os.path.exists(paths):
        print(f"folder not exist {paths}")
        exit()

    for directory, subdir_list, file_list in os.walk(paths):
        for name in file_list:
            for extension in extension_list:
                if name.endswith(extension):
                    #print(name)
                    path_in = os.path.join(directory, name)
                    #print("path_in: ", path_in)
                    # timestamp = os.path.getmtime(source_name)
                    try:
                        found_text = find_string_in_pdf(path_in, find_text)
                        #print("path_in name found_text : ", path_in, len(found_text))

                        if len(found_text) > 0:
                            #print("from_folder_to_year found_text: ", found_text, len(found_text))
                            found_text_list.append(path_in)
                            #exit()

                    except Exception as e:
                        print(e)
                        continue

    return found_text_list
