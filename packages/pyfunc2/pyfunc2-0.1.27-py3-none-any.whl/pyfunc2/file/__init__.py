# Auto-generated __init__.py



# Import necessary modules and functions here
from get_filename_from_path import get_filename_from_path
from get_hash import get_hash
from move_file import move_file
from remove_empty_folders import remove_empty_folders
from archive_path_list import archive_path_list
from check_and_create_path import check_and_create_path
from check_and_create_path_from_filepath import check_and_create_path_from_filepath
from check_existing_folder_list_in_path import check_existing_folder_list_in_path
from convert_pdf_to_base64 import convert_pdf_to_base64
from create import create_folder
from dir_list import dir_list
from file_list import file_list
from find_duplicates import find_duplicates
from get_hash_sha256 import get_hash_sha256
from is_file_hidden import is_file_hidden
from is_path_hidden import is_path_hidden
from move_duplicate_files import move_duplicate_files
from pdf_merge import merge_pdfs
from remove_duplicates import remove_duplicates
from remove_duplicates_in_path import remove_duplicates_in_path
from sum_year_from_path_to_file import sum_year_from_path_to_file
from sum_year_from_path_to_file import scan_recursive

# Public API of the package
__all__ = [get_filename_from_path, get_hash, move_file, remove_empty_folders, archive_path_list, check_and_create_path, check_and_create_path_from_filepath, check_existing_folder_list_in_path, convert_pdf_to_base64, create_folder, dir_list, file_list, find_duplicates, get_hash_sha256, is_file_hidden, is_path_hidden, move_duplicate_files, merge_pdfs, remove_duplicates, remove_duplicates_in_path, sum_year_from_path_to_file, scan_recursive]


# Version of the pyfunc2 package
import sys
sys.path.append('../')
from _version import __version__