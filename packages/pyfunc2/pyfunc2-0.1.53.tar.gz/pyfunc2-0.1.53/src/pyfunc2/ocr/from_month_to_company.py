import os
import datetime
import dateutil.parser as dparser
# pip3 install python-dateutil
# pip3 install pillow
# pip3 install image
# pip3 install regex
import sys

sys.path.append('../')
from .get_company_from_pdf import get_company_from_pdf


# move from IN to selected month
def from_month_to_company(source="./", company_list=[""], extension_list=['.pdf']):
    """
    move from IN to selected month
    :param source: source folder
    :param company_list: list of companies
    :param extension_list: list of file extensions
    """
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
                        invoice_company = get_company_from_pdf(
                            path_in,
                            [],
                            company_list
                        )

                        print("invoice_company: ", invoice_company)
                        if len(invoice_company):
                            print("from_month_to_company invoice_company: ", invoice_company)

                            path_folder = os.path.join(source, str(invoice_company[0]))
                            # print("from_month_to_company path_folder: ", path_folder)
                            # exit()

                            if not os.path.exists(path_folder):
                                os.makedirs(path_folder)

                            path_out = os.path.join(path_folder, name)
                            # modified_date = str(datetime.datetime.fromtimestamp(timestamp)).replace(':', '.')
                            # target_name = os.path.join(directory, f'{modified_date}_{name}')
                            # target_name = os.path.join(directory, f'{modified_date}_{name}')

                            print(f'from_month_to_company FROM: {path_in} TO: {path_out}')
                            # exit()

                            os.rename(path_in, path_out)
                    except Exception as e:
                        print(e)
                        continue
                    # exit()
