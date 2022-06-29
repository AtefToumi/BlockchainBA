import hashlib
import json

from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA384


def create_key():
    return RSA.generate(2048)


def import_public_key(key):
    return key.publickey()


def import_private_key(key):
    return key


def sign(private_key, hashed):
    signer = pkcs1_15.new(private_key)
    return signer.sign(hashed)

def verify_signature(public_key, hashed , signature):
    verifier = pkcs1_15.new(public_key)
    return verifier.verify(hashed, signature)


def hash(block):
    """
    Creates a SHA-256 hash of a Block
    :param block: Block
    """

    # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    block_string = json.dumps(block, sort_keys=True).encode()
    return SHA384.new(block_string)


