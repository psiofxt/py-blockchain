# stdlib
from hashlib import sha256
import json
from time import time
from uuid import uuid4

# third-party

# local


def proof_of_work(last_proof):
    """
    TODO: Docstring
    """

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof


def valid_proof(last_proof, current_proof):
    """
    TODO: Docstring
    """

    guess = f'{last_proof}{current_proof}'.encode()
    guess_hash = sha256(guess).hexdigest()
    return guess_hash[:4] == '0000'
