import collections
from crypto import sign, hash
from time import time


class Block:
    def __init__(self, index, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = time()
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def to_dict(self):
        return collections.OrderedDict({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "proof": self.proof,
            "previous_hash": self.previous_hash,
        })

    def to_dict_signed(self):
        return collections.OrderedDict({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "proof": self.proof,
            "previous_hash": self.previous_hash,
            "signature": self.signature.hex()
        })

    def sign_block(self, node):
        hashed_transaction = hash(self.to_dict())
        signature = sign(node.private_key, hashed_transaction)
        setattr(self, 'signature', signature)

    # def valid_block():
    #     block = self.chain[current_index]
    #     print(f'{last_block}')
    #     # print(f'{block}')
    #     # print("\n-----------\n")
    #     # Check that the hash of the block is correct
    #     last_block_hash = hash(last_block)
    #     if block['previous_hash'] != last_block_hash.hexdigest():
    #         print("\nCHAIN IS NOT VALID : Block number : ", current_index)
    #         print(block['previous_hash'])
    #         print(last_block_hash)
    #         return False
    #
    #     # Check that the Proof of Work is correct
    #     if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash.hexdigest()):
    #         print("\nPROOF IS NOT VALID, index\n")
    #         return False
    #
    #     last_block = block
    #     current_index += 1
    #
    # print("\nCHAIN IS VALID\n")
    # return True
