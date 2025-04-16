from pathlib import Path


def get_email_path(email_target, storage_root):
    p = Path(storage_root).expanduser()
    # print(email)
    data_path = str(p) + "/" + email_target
    print("get_email_path data_path:", data_path)
    return data_path
