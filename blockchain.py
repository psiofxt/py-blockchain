# stdlib
import hashlib
import json
from time import time

# third-party

# local
from proof.proof import proof_of_work


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

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
