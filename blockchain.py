# stdlib
import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

# third-party

# local
from proof.proof import proof_of_work, valid_proof


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

    def register_node(self, address):
        """
        TODO: Register docstring
        """
        parsed = urlparse(address)
        self.nodes.add(parsed.netloc)

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new Block and adds it to the chain

        :param proof: The proof given by the Proof of Work algorithm, int
        :param previous_hash: Hash of the previous Block (Optional), string
        :return: A dictionary of the new block's data, dict
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if \
                                              len(self.chain) else 0
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Adds a new transaction to the list of transactions

        :param sender: Address of the Sender, str
        :param receipient: Address of the Recipient, str
        :param amount: Amount of the transaction, int
        :return: The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    def valid_chain(self, chain):
        """
        TODO: Valid chain docstring
        """
        last_block = chain[0]
        current = 1

        while current < len(chain):
            block = chain[current]
            print(f'{last_block}')
            print(f'{block}')
            print('\n-----------\n')

            if not block['previous_hash'] == self.hash(last_block):
                return False

            if not valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current += 1

        return True

    def resolve_conflicts(self):
        """
        TODO: Resolve conflicts docstring
        """
        neighbors = self.nodes
        new_chain = None

        max_len = len(self.chain)

        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_len and self.valid_chain(chain):
                    max_len = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    @staticmethod
    def hash(block):
        # Hashes a block
        # Must use ensure the dictionary is ordered so that there are no
        # inconsistencies within the blockchain data
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain (the latest)
        return self.chain[-1]
