import gcoin.proof as proof
from gcoin.transaction import Transaction


GENESIS_ACCOUNT_ID = '0'
AMOUNT_OF_REWARD = 1


class Miner:
    def __init__(self, account_id):
        self.account_id = account_id

    def __call__(self, blockchain):
        last_block = blockchain.last_block()

        # Proof of Work
        new_proof = proof.find_proof(last_block.proof)

        # Adding mining rewards
        transaction = Transaction(GENESIS_ACCOUNT_ID,
                                  self.account_id, AMOUNT_OF_REWARD)
        blockchain.add_transaction(transaction)

        # Make new block with new proof,
        #   transactions and hash of last block
        block = blockchain.new_block(new_proof)

        return block
