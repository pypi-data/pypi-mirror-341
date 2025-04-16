# a python script with a function name: "archive_path_list" and parameters:
# filename for archive, extension for archive, list of paths to archive in selected type of archive

import os
import shutil
import tempfile


def archive_path_list(filename, extension, paths_dict, archive_path="./"):
    if extension not in ['tar', 'zip']:
        raise ValueError('Invalid extension! Accepted values: tar, zip')

    archive_name = f'{filename}.{extension}'
    full_archive_path = os.path.join(archive_path, archive_name)

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            for path, archive_dir in paths_dict.items():
                if os.path.isdir(path):
                    dst = os.path.join(tmpdir, archive_dir)
                    shutil.copytree(path, dst, dirs_exist_ok=True)
                else:
                    print(f'{path} is not a directory. Skipping...')

            shutil.make_archive(filename, extension, tmpdir)
        # Move the archive to the desired location
        shutil.move(archive_name, full_archive_path)

        return f'Archive {full_archive_path} created successfully!'

    except Exception as e:
        print(f'An error occurred while archiving: {e}')


"""
# Example usage    
paths_to_archive = ['/path/to/file1', '/path/to/file2', '/path/to/directory']
archive_path_list('archive_name', 'zip', paths_to_archive)

This function will create a archive with the given filename and extension, and it will contain all the files/d

"""
