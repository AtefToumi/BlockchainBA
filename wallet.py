import collections

from crypto import create_key, import_public_key, sign, verify_signature
from Crypto.Hash import SHA384
import hashlib
import json


class Wallet:
    def __init__(self, id):
        self.id = id
        self.private_key = create_key()
        self.public_key = import_public_key(self.private_key)

    @property
    def address(self):
        # return binascii.hexlify(self.public_key.exportKey(format='DER')).decode('ascii')
        return self.public_key.exportKey().hex()

    def to_dict(self):
        return collections.OrderedDict({
            "wallet_ID": self.id,
            "public_key": self.public_key.exportKey().hex(),
        })

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
#
# w1 = Wallet(1)
# message = b"i love you"
# h = SHA384.new(message)
# print(h)
# signature = sign(w1.private_key, h)
# signature1 = "blalblalba"
# try:
#     verify_signature(w1.public_key, h, signature)
#     print("The signature is valid")
# except(ValueError,TypeError):
#     print("The signature is NOT valid")

w1 = Wallet(1)