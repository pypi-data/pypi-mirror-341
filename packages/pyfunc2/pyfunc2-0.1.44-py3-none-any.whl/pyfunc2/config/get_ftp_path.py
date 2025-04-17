from pathlib import Path

def get_ftp_path(email_target, storage_root=""):
    p = Path(storage_root).expanduser()
    #print(email)
    data_path = str(p) + "/" + email_target
    print(data_path)
    return data_path