import sys
# sys.path.append('../')

from .lasts import lasts
from .config.get_email_path import get_email_path
from .config.get_ftp_path import get_ftp_path


def all_lasts(images=[], lines=3, emails=[], ftps=[], storage_root="", remote_folder="inbox"):
    for email in emails:
        print('storage_root', storage_root)
        images = images + lasts(get_email_path(email["target"], storage_root), int(lines), emails, ftps, storage_root)

    #for ftp in ftps:
    #    images = images + lasts(get_ftp_path(ftp["target"], storage_root), int(lines), emails, ftps, storage_root)

    return images
