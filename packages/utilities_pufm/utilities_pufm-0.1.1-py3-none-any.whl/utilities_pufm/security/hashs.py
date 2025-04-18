import hashlib

def get_md5(text: str):
    return hashlib.md5(text.encode()).hexdigest()