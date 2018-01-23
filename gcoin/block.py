import json
import hashlib
from time import time

import gcoin.config as cfg
from gcoin.transaction import Transaction


class BlockHeader:
    def __init__(self, previous_hash=None, timestamp=0,
                 difficulty=0, proof=0):
        """Block

        Args:
            previous_hash (str):
            timestamp (float):
            difficulty (int):
            proof (int):
        """
        self.previous_hash = previous_hash
        self.timestamp = timestamp if timestamp else time()
        self.difficulty = difficulty if difficulty else cfg.DIFFICULTY
        self.proof = proof

    def hash(self):
        """Make hash of a header of current block for finding proof

        Don't use 'proof' because there is no 'proof' in new block at the first time.
        """
        header_dump = self.dump()
        header_dump.pop('proof', None)
        header_dump = json.dumps(header_dump, sort_keys=True).encode()
        header_hash = hashlib.sha256(header_dump).hexdigest()

        return header_hash

    def dump(self, proof=True):
        data = {
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'difficulty': self.difficulty
        }

        if proof:
            data['proof'] = self.proof

        return data

    @classmethod
    def init_from_json(cls, data):
        return cls(data['previous_hash'],
                   data['timestamp'],
                   data['difficulty'],
                   data['proof'])


class Block:
    def __init__(self, transactions, previous_hash=None):
        """Block

        Args:
            transactions (list): list of Transaction object
            previous_hash (str):
        """
        self.transactions = transactions
        self.header = BlockHeader(previous_hash)

    @property
    def previous_hash(self):
        return self.header.previous_hash

    @property
    def difficulty(self):
        return self.header.difficulty

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

        header = BlockHeader.init_from_json(data['header'])

        self = cls(transactions)

        self.header = header

        return self

