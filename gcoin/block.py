import json
import hashlib
from time import time

from gcoin.transaction import Transaction


class BlockHeader:
    def __init__(self, proof=0, previous_hash=None, timestamp=0):
        """Block

        Args:
            proof (int):
            previous_hash (str):
            timestamp (float):
        """
        self.proof = proof
        self.previous_hash = previous_hash
        self.timestamp = timestamp if timestamp else time()

    def hash(self):
        """Make hash of a header of current block for finding proof

        Don't use 'proof' because there is no 'proof' in new block at the first time.
        """
        header_dump = self.dump()
        header_dump.pop('proof', None)
        header_dump = json.dumps(header_dump, sort_keys=True).encode()
        header_hash = hashlib.sha256(header_dump).hexdigest()

        return header_hash

    def dump(self):
        return {
            'previous_hash': self.previous_hash,
            'proof': self.proof,
            'timestamp': self.timestamp
        }

    @classmethod
    def init_from_json(cls, data):
        return cls(data['proof'],
                   data['previous_hash'],
                   data['timestamp'])


class Block:
    def __init__(self, transactions, proof=0,
                 previous_hash=None, timestamp=0):
        """Block

        Args:
            transactions (list): list of Transaction object
            proof (int):
            previous_hash (str):
            timestamp (float):
        """
        self.transactions = transactions
        self.header = BlockHeader(proof, previous_hash, timestamp)

    @property
    def previous_hash(self):
        return self.header.previous_hash

    @property
    def proof(self):
        return self.header.proof

    @proof.setter
    def proof(self, value):
        self.header.proof = value

    def hash(self):
        """Make hash of current block"""
        block_dump = json.dumps(self.dump(), sort_keys=True).encode()
        block_hash = hashlib.sha256(block_dump).hexdigest()

        return block_hash

    def dump(self):
        return {
            'header': self.header.dump(),
            'transactions': [t.dump() for t in self.transactions]
        }

    @classmethod
    def init_from_json(cls, data):
        transactions = [Transaction.init_from_json(t)
                        for t in data['transactions']]

        return cls(transactions,
                   data['header']['proof'],
                   data['header']['previous_hash'],
                   data['header']['timestamp'])

