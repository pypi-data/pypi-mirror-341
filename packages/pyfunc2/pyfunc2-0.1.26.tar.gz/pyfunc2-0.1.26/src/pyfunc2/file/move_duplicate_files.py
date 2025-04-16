import os
import hashlib
import sys

sys.path.append('../')

from file.move_file import move_file
from file.get_hash_sha256 import get_hash_sha256


# Python script to move duplicated files based on content:
def move_duplicate_files(directory, duplicated, extension=".pdf"):
    # Dictionary to store file hashes and paths
    file_hashes = {}
    # Traverse the directory recursively
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                file_hash = get_hash_sha256(file_path)
                if file_hash in file_hashes and file_path != file_hashes[file_hash]:
                    duplic = file_hashes[file_hash]
                    print(f"move_duplicate_files duplicated: {file_path} => {duplic}")
                    # move only the shortest path
                    move_file_path = file_path
                    if len(file_path) > len(duplic):
                        move_file_path = duplic
                        print(f"move {move_file_path}")

                    # os.remove(file_path)
                    move_file(move_file_path, '', duplicated)
                else:
                    file_hashes[file_hash] = file_path
