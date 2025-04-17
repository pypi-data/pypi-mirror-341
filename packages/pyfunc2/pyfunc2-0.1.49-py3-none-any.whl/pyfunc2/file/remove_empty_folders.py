import os
import shutil

def remove_empty_folders(path_abs):
    walk = list(os.walk(path_abs))
    for path1, _, _ in walk[::-1]:
        #print("remove_empty_folders", path1, os.listdir(path1))
        if len(os.listdir(path1)) == 0:
            # path1 = Path(path)
            # os.remove(path1)
            #print(os.path.isfile(path1))
            #os.remove(path1)
            #os.unlink(path1)
            # Try to remove the tree; if it fails, throw an error using try...except.
            try:
                shutil.rmtree(path1)
                print("remove_empty_folders removed: " + path1)
            except OSError as e:
                print("remove_empty_folders error: %s - %s." % (e.filename, e.strerror))

