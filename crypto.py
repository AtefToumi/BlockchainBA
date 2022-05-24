import hashlib
import json

from Crypto.PublicKey import RSA


def create_key():
    return RSA.generate(2048)


def import_public_key(key):
    return key.publickey()


def import_private_key(key):
    return key


def sign(key, msg):
    pass


def hash(block):
    """
    Creates a SHA-256 hash of a Block
    :param block: Block
    """

    # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()
