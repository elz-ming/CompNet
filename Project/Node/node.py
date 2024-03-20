from flask import Flask, jsonify, request
from blockchain import Blockchain
from network import Network
from transaction import Transaction
from uuid import uuid4


app = Flask(__name__) # Instantiate the Node
blockchain = Blockchain() # Instantiate the Blockchain
network =  Network() # Instantiate the network

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        network.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': network.get_nodes(),
    }
    return jsonify(response), 201

@app.route('/nodes/list', methods=['GET'])
def list_nodes():
    nodes = network.get_nodes()
    response = {
        'total_nodes': nodes
    }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    response = "mine_logic"
    return jsonify(response), 201

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # Extract the transaction data from the request
    values = request.get_json()

    # Check required fields
    required_fields = ['sender', 'recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {'message': 'Missing values'}
        return jsonify(response), 400
    
    new_trans = Transaction(values['sender'], values['recipient'], values['amount'])
    blockchain.add_new_transaction(new_trans.to_dict)

    response = {'message': 'Transaction will be added to the next block'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': [block.to_dict() for block in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return jsonify(response), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
