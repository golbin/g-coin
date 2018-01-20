from argparse import ArgumentParser

from flask import Flask, jsonify, request

import gcoin.proof as proof
from gcoin.node import Node
from gcoin.blockchain import BlockChain
from gcoin.transaction import Transaction


app = Flask('g-coin')

app.node = Node()
app.blockchain = BlockChain()


@app.route('/transaction', methods=['POST'])
def add_transaction():
    # data.sender(str)
    # data.recipient(str)
    # data.amount(int)
    data = request.get_json()

    transaction = Transaction.init_from_json(data)

    try:
        next_index = app.blockchain.add_transaction(transaction)
    except Exception as e:
        return jsonify({'message': str(e)}), 403

    response = {'message': f'Transaction will be added to {next_index}th block.'}

    return jsonify(response), 201


@app.route('/transaction', methods=['GET'])
def get_pending_transactions():
    transactions = [t.dump() for t in app.blockchain.transactions]

    return jsonify(transactions), 201


@app.route('/mine', methods=['POST'])
def mine():
    """Mining
    Have to make a standalone process
    But it's just a prototype
    """
    last_block = app.blockchain.last_block()

    # Proof of Work
    new_proof = proof.find_proof(last_block.proof)

    # Adding mining rewards
    transaction = Transaction('0', app.node.id, 1)
    app.blockchain.add_transaction(transaction)

    # Make new block with new proof,
    #   transactions and hash of last block
    block = app.blockchain.new_block(new_proof)

    response = {
        'message': "New block is mined!",
        'proof': block.proof,
        'previous_hash': block.previous_hash
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': app.blockchain.dump(),
        'length': len(app.blockchain)
    }

    return jsonify(response), 200


@app.route('/node', methods=['GET'])
def get_all_nodes():
    response = {
        'nodes': list(app.node.neighbor),
        'total': len(app.node)
    }

    return jsonify(response), 201


@app.route('/node', methods=['POST'])
def add_node():
    # data.address(str)
    data = request.get_json()

    app.node.add(data['address'])

    response = {
        'message': 'New app.node is added.',
        'total': len(app.node)
    }

    return jsonify(response), 201


@app.route('/chain/valid', methods=['GET'])
def valid_chain():
    valid = app.blockchain.valid()

    response = {'result': valid}

    return jsonify(response), 200


@app.route('/consensus', methods=['POST'])
def consensus():
    new_blockchain = app.node.consensus_with_neighbor(app.blockchain)

    if new_blockchain:
        app.blockchain = new_blockchain
        response = {'message': 'Our chain was replaced.'}
    else:
        response = {'message': 'I\'m King of the World.'}

    return jsonify(response), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--port', default=5000, type=int)
    args = parser.parse_args()

    app.run(port=args.port)
