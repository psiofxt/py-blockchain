# stdlib
import hashlib
import json
from time import time
from textwrap import dedent

# third-party
from flask import Flask, jsonify, request

# local
from proof.proof import proof_of_work


class BlockAPI():
    """
    TODO: Docstring for BlockAPI
    """
    def __init__(self, blockchain, node):
        self.blockchain = blockchain
        self.app = Flask(__name__)
        self.node = node


    def run(self):
        app = self.app
        blockchain = self.blockchain
        node = self.node

        @app.route('/mine', methods=['GET'])
        def mine():
            last_block = blockchain.last_block
            last_proof = last_block['proof']
            proof = proof_of_work(last_proof)

            blockchain.new_transaction(
                sender='0',
                recipient=node,
                amount=1,
            )

            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof, previous_hash)

            response = {
                'message': 'New Block Forged',
                'index': block['index'],
                'transactions': block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
            }
            return jsonify(response), 200


        @app.route('/transactions/new', methods=['POST'])
        def new_transaction():
            values = request.get_json()

            required_params = ['sender', 'recipient', 'amount']
            for r in required_params:
                if r not in values:
                    return f'Missing value: {r}, required params are {required_params}', 400

            # Creates a new transaction
            index = blockchain.new_transaction(values['sender'],
                                                    values['recipient'],
                                                    values['amount'])
            response = {'message': f'Transaction will be added to Block {index}'}
            return jsonify(response), 201


        @app.route('/chain', methods=['GET'])
        def full_chain():
            response = {
                'chain': blockchain.chain,
                'length': len(blockchain.chain)
            }
            return jsonify(response), 200

        app.run(host='127.0.0.1', port=5000)
