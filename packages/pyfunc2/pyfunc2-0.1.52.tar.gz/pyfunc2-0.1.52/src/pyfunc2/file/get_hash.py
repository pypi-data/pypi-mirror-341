import hashlib

def get_hash(file_path):
    """
    This function returns the SHA-1 hash of the file
    """
    with open(file_path, 'rb') as file:
        bytes = file.read()
        return hashlib.sha1(bytes).hexdigest()
