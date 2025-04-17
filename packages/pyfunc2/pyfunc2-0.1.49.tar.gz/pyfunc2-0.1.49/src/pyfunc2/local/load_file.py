import os

def load_file(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            return file.read()
    else:
        print(f"{filename} file does not exist")