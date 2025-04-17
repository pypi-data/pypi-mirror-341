import subprocess
def create_path(path_folder):
    subprocess.run(['mkdir', '-p', path_folder])