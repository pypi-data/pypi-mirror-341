import sys
sys.path.append('../')

from get_email_path import get_email_path
from get_ftp_path import get_ftp_path
from os.path import exists as file_exists


def get_path_file(filename, emails, ftps, storage):
    for email in emails:
        data_path = get_email_path(email["target"], storage["root"]) + "/" + filename
        if file_exists(data_path) == True:
            return data_path

    for ftp in ftps:
        data_path = get_ftp_path(ftp["target"], storage["root"]) + "/" + filename
        if file_exists(data_path) == True:
            return data_path

    return ""