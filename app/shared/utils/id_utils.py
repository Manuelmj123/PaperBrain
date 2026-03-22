import hashlib


def build_chunk_id(source_hash: str, index: int):

    return hashlib.sha1(
        f"{source_hash}_{index}".encode()
    ).hexdigest()