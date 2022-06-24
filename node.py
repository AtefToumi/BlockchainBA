from crypto import create_key, import_public_key

class Node:
    def __init__(self, address):
        self.address = address
        self.private_key = create_key()
        self.public_key = import_public_key(self.private_key)


