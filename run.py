# stdlib
from uuid import uuid4

# third-party

# local
from api.blockapi import BlockAPI
from blockchain import Blockchain


if __name__ == '__main__':
    node = str(uuid4()).replace('-', '')
    blockchain = Blockchain()
    blockchain.new_block(100)
    api = BlockAPI(blockchain, node)
    api.run()
