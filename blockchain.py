import hashlib
import requests
from block import Block
from crypto import hash
from transaction import Transaction
from urllib.parse import urlparse
from wallet import Wallet
import json


w1 = Wallet(1)
w2 = Wallet(2)
w3 = Wallet(3)
w4 = Wallet(4)
w5 = Wallet(5)
node_wallet = Wallet(6)
reward_wallet = Wallet(999)
previous_hash = '1'
proof=100


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.verified_transactions = []
        self.chain = []
        self.nodes = set()
        self.wallets = [w1, w2, w3, w4, w5]
        self.wallets_ids = [w1.id, w2.id, w3.id, w4.id, w5.id]
        
        self.new_block(previous_hash, proof, reward_wallet)

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
        if guess_hash[:4] == "0000":
            print(guess_hash)
            return True
        else:
            return False

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain():
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def verify_transactions(self):
        """
        Verifies transactions in current_transactions list
        :return: appends all verified transactions to verified_transactions list
        """
        for i in range(0, len(self.current_transactions)):
            if self.current_transactions[i].verify_transaction():
                self.verified_transactions.append(self.current_transactions[i])

    def valid_chain(self):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = self.chain[0]
        current_index = 1

        while current_index < len(self.chain):
            block = self.chain[current_index]
            # print(f'{last_block}')
            # print(f'{block}')
            # print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = hash(last_block)
            if block['previous_hash'] != last_block_hash.hexdigest():
                print("\nCHAIN IS NOT VALID : Block number : ", current_index)
                print(block['previous_hash'])
                print(last_block_hash)
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash.hexdigest()):
                print("\nPROOF IS NOT VALID, index\n")
                return False

            last_block = block
            current_index += 1

        print("\nCHAIN IS VALID\n")
        return True

    def new_transaction(self, sender_wallet, recipient_wallet, amount):
        transaction = Transaction(sender_wallet, recipient_wallet, amount)
        transaction.sign_transaction()


        self.current_transactions.append(transaction.to_dict())
        print(transaction.to_dict())

        neighbours = self.nodes
        #Broadcasting the transaction to all nodes
        for node in neighbours :
            r = requests.post(f"http://{node}/broadcast", json = json.dumps(transaction.to_dict(), indent=4))
            print(r.text)
        return transaction

    def get_wallet(self, wallet_id):
        for w in self.wallets:
            if w.id == wallet_id:
                return w

    def new_block(self, proof, previous_hash, node):
        """
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :param miner: The miner of the block
        :return:
        """
        block = Block(len(self.chain) + 1, self.current_transactions, proof, previous_hash or hash(self.chain[-1]))
        block.sign_block(node)
        # block = {
        #     'index': len(self.chain) + 1,
        #     'timestamp': time(),
        #     'transactions': self.current_transactions,
        #     'proof': proof,
        #     'previous_hash': previous_hash or self.hash(self.chain[-1]),
        # }
        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block.to_dict_signed())
        return block

    def mine(self, node):
        # We run the proof of work algorithm to get the next proof...
        last_block = self.last_block
        proof = self.proof_of_work(last_block)

        # We must receive a reward for finding the proof.
        self.new_transaction(reward_wallet, node_wallet, 1)

        # Forge the new Block by adding it to the chain
        previous_hash = hash(last_block)
        block = self.new_block(proof, previous_hash.hexdigest(),node)

        response = {
            'message': "New Block Forged",
            'index': block.index,
            'transactions': block.transactions,
            'proof': block.proof,
            'previous_hash': block.previous_hash,
            'signature': block.signature.hex()
        }
        print(response)
        return response

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = hash(last_block).hexdigest()

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof


# blockchain = Blockchain()
# blockchain.new_transaction(w1, w2, 5)
# blockchain.new_transaction(w3, w4, 15)
# blockchain.new_transaction(w5, w1, 11)
# print("Current transactions are : \n")
# for i in range(0, len(blockchain.current_transactions)):
# print(blockchain.current_transactions[i], "\n")
# print("Current chain : \n")
# for x in range(0, len(blockchain.chain)):
# print(blockchain.chain[x], "\n")
# blockchain.mine()
# print("chain after mining : \n")
# for y in range(0, len(blockchain.chain)):
# print(blockchain.chain[y])
# blockchain.valid_chain()

# print("Verifying transactions : ")
# blockchain.verify_transactions()
# for x in range(0, len(blockchain.verified_transactions)):
#     print(blockchain.verified_transactions[x])
