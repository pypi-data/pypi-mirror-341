import os
import datetime
import dateutil.parser as dparser
# pip3 install python-dateutil
# pip3 install pillow
# pip3 install image
# pip3 install regex
import sys

sys.path.append('../')
from .get_date_from_pdf import get_date_from_pdf
from .get_date_from_pdf_pattern import get_date_from_pdf_pattern


# move from IN to selected month
def from_folder_to_year(source="./", subfolder="", extension_list=['.pdf']):
    # print(source, dest)
    root = '../'
    # path = os.path.join(root, source)
    paths = source
    if not os.path.exists(paths):
        print(f"folder not exist {paths}")
        exit()

    for directory, subdir_list, file_list in os.walk(paths):
        for name in file_list:
            for extension in extension_list:
                if name.endswith(extension):
                    print(name)
                    path_in = os.path.join(directory, name)
                    print("path_in: ", path_in)
                    # timestamp = os.path.getmtime(source_name)
                    try:
                        invoice_date = get_date_from_pdf(
                            path_in,
                            get_date_from_pdf_pattern.format_out_list,
                            get_date_from_pdf_pattern.pattern_clean_list,
                            get_date_from_pdf_pattern.pattern_input_list
                        )

                        print("from_folder_to_year invoice_date: ", invoice_date, len(invoice_date))

                        if len(invoice_date):

                            path_folder = os.path.join(root, str(invoice_date[0]), "expenses",
                                                       str(invoice_date[1]), subfolder)
                            print("from_folder_to_yearpath_folder: ", path_folder)

                            if not os.path.exists(path_folder):
                                os.makedirs(path_folder)

                            path_out = os.path.join(path_folder, name)

                            print(path_out)
                            # exit()
                            # modified_date = str(datetime.datetime.fromtimestamp(timestamp)).replace(':', '.')
                            # target_name = os.path.join(directory, f'{modified_date}_{name}')
                            # target_name = os.path.join(directory, f'{modified_date}_{name}')

                            print(f'FROM: {path_in} TO: {path_out}')
                            os.rename(path_in, path_out)
                    except Exception as e:
                        print(e)
                        continue
                    # exit()
