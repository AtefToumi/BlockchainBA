from Crypto.Signature import pkcs1_15

from Crypto.Hash import SHA256

from Crypto.PublicKey import RSA

message = b'To be signed'

key = RSA.import_key(open('private_key.der').read())

h = SHA256.new(message)

signature = pkcs1_15.new(key).sign(h)