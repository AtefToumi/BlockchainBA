import json
from uuid import uuid4

from flask import Flask, jsonify, request

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

    if (blockchain.check_wallet(values['sender_wallet_id']) and blockchain.check_wallet(values['recipient_wallet_id'])):
        # Create a new Transaction
        transaction = blockchain.new_transaction(values['sender_wallet_id'], values['recipient_wallet_id'],
                                                 values['amount'])
    else:
        return jsonify({'message': f'Wallets are incorrect'})

    reponse = {'message': f'Transaction will be added to the next Block',
               'transaction': json.dumps(transaction, indent=4, sort_keys=True, default=vars)
               }

    return jsonify(reponse), 201


@app.route('/transactions/all', methods=['GET'])
def all_transactions():
    response = {
        'transactions': json.dumps(blockchain.current_transactions, default=vars)
    }
    return jsonify(response), 200


@app.route('/users/new_client', methods=['POST'])
def new_client():
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)


