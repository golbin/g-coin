import json
import hashlib
from time import time

from gcoin.transaction import Transaction


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
        self.proof = proof if proof else 10
        self.timestamp = timestamp if timestamp else time()
        self.previous_hash = previous_hash if previous_hash else 'g'

    def hash(self):
        """Make hash of current block"""
        block_dump = json.dumps(self.dump(), sort_keys=True).encode()
        block_hash = hashlib.sha256(block_dump).hexdigest()

        return block_hash

    def dump(self):
        return {
            'transactions': [t.dump() for t in self.transactions],
            'previous_hash': self.previous_hash,
            'proof': self.proof,
            'timestamp': self.timestamp
        }

    @classmethod
    def init_from_json(cls, data):
        transactions = [Transaction.init_from_json(t)
                        for t in data['transactions']]

        return cls(transactions,
                   data['proof'],
                   data['previous_hash'],
                   data['timestamp'])
