import os
def dir_list(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]