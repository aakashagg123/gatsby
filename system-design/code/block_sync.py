"""File sync: split into blocks, hash each, upload only blocks the server lacks. Run: python3 block_sync.py"""
import hashlib
import os

BLOCK = 4096


def blocks(data):
    return [data[i:i + BLOCK] for i in range(0, len(data), BLOCK)]


def digest(b):
    return hashlib.sha256(b).hexdigest()


class Server:
    def __init__(self):
        self.store = {}

    def upload(self, data):
        """Returns (blocks uploaded, blocks skipped because the server already had them)."""
        sent = skipped = 0
        for b in blocks(data):
            d = digest(b)
            if d in self.store:
                skipped += 1
            else:
                self.store[d] = b
                sent += 1
        return sent, skipped


if __name__ == "__main__":
    original = os.urandom(BLOCK * 100)                       # a 400 KB file, 100 blocks
    s = Server()
    first = s.upload(original)
    edited = original[:BLOCK * 50] + b"X" + original[BLOCK * 50 + 1:]      # change one byte in block 51
    second = s.upload(edited)
    copy = s.upload(original)                                  # the same file uploaded by another user
    print(f"first upload {first}; after a one-byte edit {second}; a duplicate of the original {copy}")
    assert first == (100, 0) and second == (1, 99) and copy == (0, 100)
    print("block sync ok")
