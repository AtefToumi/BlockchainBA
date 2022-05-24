from crypto import create_key, import_public_key


class Wallet:
    def __init__(self, id):
        self.id = id
        self.private_key = create_key()
        self.public_key = import_public_key(self.private_key)



    @property
    def address(self):
        # return binascii.hexlify(self.public_key.exportKey(format='DER')).decode('ascii')
        return self.public_key.exportKey().hex()
