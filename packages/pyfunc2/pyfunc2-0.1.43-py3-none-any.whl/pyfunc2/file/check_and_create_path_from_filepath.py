import os
from pathlib import Path


def check_and_create_path_from_filepath(dest_path):
    dirname, fname = os.path.split(dest_path)
    # print(dirname)
    # print(fname)
    path = Path(dirname)
    if not os.path.exists(str(path)):
        try:
            path.mkdir(parents=False, exist_ok=False)
        except FileExistsError:
            print(f'check_and_create_path exist: {dirname}')
        else:
            print(f'check_and_create_path created: {dirname}')
