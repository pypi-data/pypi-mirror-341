import os
from pathlib import Path


def check_and_create_path(dest_path):
    # print(dirname)
    # print(fname)
    path = Path(dest_path)
    if not os.path.exists(str(path)):
        try:
            path.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            print(f'check_and_create_path exist: {dest_path}')
        else:
            print(f'check_and_create_path created: {dest_path}')
