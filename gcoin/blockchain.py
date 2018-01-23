import gcoin.proof
import gcoin.config as cfg
from gcoin.book import Book
from gcoin.block import Block


class BlockChain:
    def __init__(self, chain=None):
        """init chain with existing chain
        or make this new blockchain

        Args:
            chain: list of dictionary of Block, see load_chain
        """
        self.chain = []
        self.book = Book()
        self.transactions = []

        if chain:
            self.load_chain(chain)
        else:
            self.init_chain()

    def init_chain(self):
        """Make genesis block"""
        genesis_block = Block([], previous_hash=cfg.GENESIS_HASH)

        genesis_proof = gcoin.proof.find_proof(genesis_block)

        genesis_block.proof = genesis_proof

        self.add_block(genesis_block)

    def add_transaction(self, transaction):
        """Add new transaction
        It will only add amount

        Args:
            transaction (obj): Transaction object

        Returns:
            int: index of next block of chain
                return -1 if it's not correct transaction
        """
        if self.book.check_balance(transaction):
            self.transactions.append(transaction)
            return len(self.chain) + 1  # Add this transaction to next block
        else:
            raise Exception('Transaction is wrong.')

    def new_block(self):
        last_block = self.chain[-1]

        block = Block(self.transactions,
                      previous_hash=last_block.hash())

        self.transactions = []

        return block

    def add_block(self, block):
        self.chain.append(block)
        self.book.apply(block.transactions)

    def valid(self):
        """Valid chain"""
        index = 1

        while index < len(self):
            prev_block = self.chain[index-1]
            curr_block = self.chain[index]

            # Check hash with previous hash
            if curr_block.previous_hash != prev_block.hash():
                return False

            # Check proof of current block
            if not gcoin.proof.valid_proof(curr_block):
                return False

            index += 1

        return True

    def load_chain(self, chain):
        """load chain from list of dictionary
        from existing blockchain

        Args:
            chain (list):
                [{
                    transactions: [{
                        sender: 'dsf9s9f0ad'
                        recipient: 'dfsad90fasf'
                        amount: 12
                    }]
                    proof: 318832940000
                    previous_hash: 'fj9afje9ajf9sef0s0f'
                    timestamp: 1506057125.900785
                }]
        """
        for block in chain:
            block = Block.init_from_json(block)
            self.add_block(block)

    def last_block(self):
        return self.chain[-1]

    def dump(self):
        return [block.dump() for block in self.chain]

    def __len__(self):
        return len(self.chain)
