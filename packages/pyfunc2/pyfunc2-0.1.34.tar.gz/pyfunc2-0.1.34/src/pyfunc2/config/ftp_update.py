from ftp_download import ftp_download
from get_ftp_path import get_ftp_path

def ftp_update(ftps, storage_root, limit=3):
    for ftp in ftps:
        data_path = get_ftp_path(ftp["target"], storage_root)
        ftp_download(ftp["server"], ftp["username"], ftp["password"], data_path, ftp["source"], limit)

