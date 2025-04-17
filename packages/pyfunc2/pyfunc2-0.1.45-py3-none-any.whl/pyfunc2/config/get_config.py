import json
import os
from pathlib import Path

def get_config(root = '~', folder ="/.rpi-zero/", filename = "config.json", key = "user"):
    p = Path(root).expanduser()
    print(p)
    email_config_path = str(p) + folder
    email_config_file = email_config_path + filename
    print(email_config_file)

    #cwd = p.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(email_config_path)  # Get all the files in that directory
    #print("Files in %r: %s" % (email_config_path, files))

    # load the configuration data from the JSON file
    with open(email_config_file) as f:
        config_list = json.load(f)
        if key in config_list:
            return config_list[key]
        else:
            print("key " + key + " not exist")

    return False