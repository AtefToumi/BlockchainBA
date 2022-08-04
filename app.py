import json
import random
import time
# Instantiate the Node
from blockchain import Blockchain
from flask import Flask, jsonify, request
from node import Node
from threading import Thread
from transaction import verify_transaction
from uuid import uuid4
from wallet import Wallet

app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()
# blockchain.register_node("http://127.0.0.1:5000")
# blockchain.register_node("http://127.0.0.1:5001")
current_node = Node()
gen_wallet = Wallet(666)


def generate_transactions(node_id):
    while True:
        wallet1 = random.randrange(1, 5)
        wallet2 = random.randrange(1, 5)
        amount = random.randrange(1, 20)
        blockchain.new_transaction(blockchain.wallets[wallet1], blockchain.wallets[wallet2], amount, True)
        print(
            f'node {node_id} created a Transaction from Wallet {wallet1} to Wallet {wallet2} with {amount} COINS transfered')
        sleep_time = random.randrange(10, 30)
        print(f'Next Transaction in {sleep_time} seconds')
        time.sleep(sleep_time)


def generate_mining():
    while True:
        sleep_time = (random.randrange(50, 100))
        print(f"Mining in {sleep_time} seconds")
        time.sleep(sleep_time)
        blockchain.mine(current_node)


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender_wallet_id', 'recipient_wallet_id', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    sender_wallet = blockchain.get_wallet(values['sender_wallet_id'])
    recipient_wallet = blockchain.get_wallet(values['recipient_wallet_id'])
    # Create a new Transaction
    broadcast = True
    transaction = blockchain.new_transaction(sender_wallet, recipient_wallet,
                                             values['amount'], broadcast)

    response = {
        'message': f'Transaction will be added to the next Block',
        'transaction': json.dumps(transaction.to_dict())
    }

    return jsonify(response), 201


@app.route('/start/gen_transactions', methods=['POST'])
def gen_transactions():
    values = request.get_json()
    node_id = values['node_id']
    required = ['node_id']
    if not all(k in values for k in required):
        return 'Missing values', 400
    thread = Thread(target=generate_transactions, args=(node_id,))
    thread.start()
    response = {
        "message": f'thread {node_id} started successfully'
    }
    return jsonify(response), 201


@app.route('/stop/gen_transactions', methods=['GET'])
def stop_thread():
    pass


@app.route('/start/gen_mine', methods=['GET'])
def start_mine():
    thread = Thread(target=generate_mining)
    thread.start()

    return jsonify({"message": "Thread started successfully"}), 201


@app.route('/broadcast', methods=['POST'])
def broadcast_transaction():
    payload = request.get_json()
    transaction = json.loads(payload)
    signature = transaction['signature']
    sender_wallet_public_key = bytes.fromhex(transaction['sender_wallet_public_key'])
    del transaction['signature']
    print("Transaction received : ", transaction)
    # print("Sender's wallet ID is : ", transaction["sender_wallet_ID"])
    # print("Signature is : ", signature)
    # print("Signature reconverted is : ", bytes.fromhex(signature))
    signature_bytes = bytes.fromhex(signature)
    sender_wallet = blockchain.get_wallet(transaction['sender_wallet_ID'])
    if verify_transaction(transaction, sender_wallet_public_key, signature_bytes):
        blockchain.current_transactions.append(transaction)
        return jsonify({'message': "Transaction verified and will be added to the next block"}), 201
    else:
        return jsonify({'message': 'signature is invalid, transaction is not accepted'})


@app.route('/broadcast/block', methods=['POST'])
def broadcast_block():
    payload = request.get_json()
    print(payload)
    test_chain = blockchain
    test_chain.chain.append(json.loads(payload))
    if test_chain.valid_chain():
        print("CHAIN IS VALIIIIIID")
    else:
        print("CHAIN IS NOOOOOOOOT VALIIIIID")
    response = {'message': "block has been sent"}
    return jsonify(response), 201


@app.route('/genesis', methods=['GET'])
def genesis_block():
    gen_block = blockchain.new_block('1', 100, gen_wallet)
    response = {
        'genesis block ': json.dumps(gen_block.to_dict_signed())
    }
    return jsonify(response), 201


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
        "current nodes": list(blockchain.nodes)
    }
    return response, 201


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
