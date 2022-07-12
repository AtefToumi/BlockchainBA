import json
# Instantiate the Node
from blockchain import Blockchain
from transaction import verify_transaction
from flask import Flask, jsonify, request
from node import Node
from uuid import uuid4
from wallet import Wallet
import random
import time
from threading import Thread

app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()
# blockchain.register_node("http://127.0.0.1:5000")
# blockchain.register_node("http://127.0.0.1:5001")
current_node = Node()

def generate_transactions():
    while True :
        print("thread 1")
        blockchain.new_transaction(blockchain.wallets[1], blockchain.wallets[2], random.randrange(1,20) )
        time.sleep(5)

def generate_transactions_2():
    while True :
        print("thread 1")
        blockchain.new_transaction(blockchain.wallets[2], blockchain.wallets[3], random.randrange(1,20) )
        time.sleep(5)

thread_1 = Thread(target = generate_transactions)
thread_2 = Thread(target = generate_transactions_2)


# thread_1.start()
# thread_2.start()

def toJSON():
    return json.dumps(default=lambda o: o.__dict__, sort_keys=True, indent=4)


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender_wallet_id', 'recipient_wallet_id', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    sender_wallet = blockchain.get_wallet(values['sender_wallet_id'])
    recipient_wallet = blockchain.get_wallet(values['recipient_wallet_id'])
    # Create a new Transaction
    transaction = blockchain.new_transaction(sender_wallet, recipient_wallet,
                                             values['amount'])

    response = {
        'message': f'Transaction will be added to the next Block',
        'transaction': json.dumps(transaction.to_dict())
    }

    return jsonify(response), 201


@app.route('/broadcast', methods=['POST'])
def broadcast_transaction():
    payload = request.get_json()
    transaction=json.loads(payload)
    signature = transaction['signature']
    sender_wallet_public_key = bytes.fromhex(transaction['sender_wallet_public_key'])
    del transaction['signature']
    print("Transaction is : ",transaction)
    print("Sender's wallet ID is : ",transaction["sender_wallet_ID"])
    print("Signature is : ", signature)
    print("Signature reconverted is : ", bytes.fromhex(signature))
    signature_bytes= bytes.fromhex(signature)
    sender_wallet = blockchain.get_wallet(transaction['sender_wallet_ID'])
    if verify_transaction(transaction, sender_wallet_public_key, signature_bytes):
        blockchain.current_transactions.append(transaction)
        return jsonify({'current transactions': blockchain.current_transactions}), 201
    else :
        return jsonify({'message': 'signature is invalid, transaction is not accepted'})

@app.route('/broadcast/block', methods=['POST'])
def broadcast_block():
    payload = request.get_json()

    return jsonify({"block is : ": payload})


@app.route('/transactions/all', methods=['GET'])
def all_transactions():
    response = {
        'transactions': json.dumps(blockchain.current_transactions, default=vars)
    }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    response = blockchain.mine(current_node)
    return jsonify(response), 200


# @app.route('/users/new_client', methods=['POST'])
# def new_client():
# pass


@app.route('/wallets', methods=['GET'])
def get_wallets():
    response = {'Wallets available are : ': json.dumps(blockchain.wallets_ids)}
    return jsonify(response), 200


@app.route('/wallets/add', methods=['POST'])
def add_wallet():
    values = request.get_json()
    required = ['wallet_id']
    if not all(k in values for k in required):
        return 'Missing values', 400

    new_wallet = Wallet(values['wallet_id'])
    blockchain.wallets.append(new_wallet)
    blockchain.wallets_ids.append(new_wallet.id)

    response = {'New wallet has been added with ID ': json.dumps(new_wallet.id)}
    return response, 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


@app.route('/node', methods=['GET'])
def node():
    response = {
        "node": json.dumps(current_node.to_dict())
    }
    return response, 201
@app.route('/nodes', methods=['GET'])
def get_nodes():
    response = {
        "current nodes" : list(blockchain.nodes)
    }
    return response, 201

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
