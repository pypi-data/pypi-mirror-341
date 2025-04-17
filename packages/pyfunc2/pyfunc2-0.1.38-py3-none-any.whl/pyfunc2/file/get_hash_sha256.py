import hashlib


def get_hash_sha256(file_path):
    # Read the file in binary mode
    with open(file_path, 'rb') as f:
        # Read the file content in chunks for memory optimization
        chunk_size = 4096
        file_hash = hashlib.sha256()
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            file_hash.update(chunk)
    return file_hash.hexdigest()
