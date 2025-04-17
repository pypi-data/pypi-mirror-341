import os

def fromFilenametoLinesAsArray(filename='.folders'):
    lines = None
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
    else:
        print(f"{filename} file does not exist")

    return lines