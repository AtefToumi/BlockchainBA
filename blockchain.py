import hashlib
import json
from crypto import hash
from block import Block
from transaction import Transaction
from wallet import Wallet

w1 = Wallet(1)
w2 = Wallet(2)
w3 = Wallet(3)
w4 = Wallet(4)
w5 = Wallet(5)
node_wallet = Wallet(6)
reward_wallet = Wallet(999)


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.wallets = [w1, w2, w3, w4, w5]

        self.new_block(previous_hash='1', proof=100)

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def new_transaction(self, sender_wallet, recipient_wallet, amount):
        transaction = Transaction(sender_wallet, recipient_wallet, amount)
        self.current_transactions.append(transaction.get_dict())
        return transaction

    def check_wallet(self, wallet_id):
        for w in self.wallets:
            if w.id == wallet_id:
                return True
            else:
                return False

    def new_block(self, proof, previous_hash):
        """
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :param miner: The miner of the block
        :return:
        """
        block = Block(len(self.chain) + 1, self.current_transactions, proof, previous_hash or hash(self.chain[-1]))
        # block = {
        #     'index': len(self.chain) + 1,
        #     'timestamp': time(),
        #     'transactions': self.current_transactions,
        #     'proof': proof,
        #     'previous_hash': previous_hash or self.hash(self.chain[-1]),
        # }
        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block.get_dict())
        return block

    def mine(self):
        # We run the proof of work algorithm to get the next proof...
        last_block = self.last_block
        proof = self.proof_of_work(last_block)

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        blockchain.new_transaction(
            reward_wallet.id,
            node_wallet.id,
            1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = hash(last_block)
        block = self.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block.index,
            'transactions': block.transactions,
            'proof': block.proof,
            'previous_hash': block.previous_hash,
            # 'signature': block['signature']
        }
        print(response)

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof


blockchain = Blockchain()
blockchain.new_transaction(w1.id, w2.id, 5)
blockchain.new_transaction(w3.id, w4.id, 15)
blockchain.new_transaction(w5.id, w1.id, 11)
print("Current transactions are : \n", blockchain.current_transactions , "\n")
print("Current chain : \n", blockchain.chain, "\n")
blockchain.mine()
print("chain after mining : \n", blockchain.chain, "\n")
