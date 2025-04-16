import os
from email_update import email_update
from file.file_list import file_list
from config.ftp_update import ftp_update


# files = os.list
# files = [f for f in files if os.path.isfile(Direc + '/' + f)]  # Filtering only the files.
# print(*files, sep="\n")

def lasts(image_path, limit=3, emails=[], ftps=[], storage_root=""):
    #email_brama()
    #email_office()

    email_update(emails, storage_root, limit)
    # ftp_update(ftps, storage_root, limit)
    images = file_list(image_path)
    # images = files(image_path)
    #print('::images', images)
    images.sort(key=lambda x: os.path.getmtime(os.path.join(image_path, x)))
    images.reverse()
    return images[:int(limit)]



