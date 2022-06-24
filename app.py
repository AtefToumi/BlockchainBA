import json
from uuid import uuid4

from flask import Flask, jsonify, request
from wallet import Wallet

# Instantiate the Node
from blockchain import Blockchain

app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


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


@app.route('/transactions/all', methods=['GET'])
def all_transactions():
    response = {
        'transactions': json.dumps(blockchain.current_transactions, default=vars)
    }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    response = blockchain.mine()
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
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
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


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
