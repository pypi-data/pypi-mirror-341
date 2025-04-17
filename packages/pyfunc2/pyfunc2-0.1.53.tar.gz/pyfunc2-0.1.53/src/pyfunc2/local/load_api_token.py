import os

def load_api_token(filename='.token'):
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            return file.readline().strip()