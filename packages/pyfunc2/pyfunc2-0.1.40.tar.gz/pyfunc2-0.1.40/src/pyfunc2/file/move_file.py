import shutil
import sys
sys.path.append('../')

from .get_filename_from_path import get_filename_from_path
from .check_and_create_path import check_and_create_path

## move a file from the source path to the destination path.
def move_file(src, dst, out="./duplicated/"):
    ## create destination path with the same filename if empty
    if not dst: dst = out + get_filename_from_path(src)
    ## create dir in path if not exist
    check_and_create_path(dst)
    ## move file from source to destination
    try:
        shutil.move(src, dst)
    except OSError:
        print(f'move_file exist: {dst}')
        print(f'move_file removed: {src}')
        # os.unlink(src)
    else:
        print(f'move_file moved {src} > {dst}')