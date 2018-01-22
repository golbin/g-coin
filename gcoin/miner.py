import gcoin.config as cfg
import gcoin.proof as proof
from gcoin.transaction import Transaction


class Miner:
    def __init__(self, account_id):
        self.account_id = account_id

    def __call__(self, blockchain):
        last_block = blockchain.last_block()

        # Proof of Work
        new_proof = proof.find_proof(last_block.proof)

        # Adding mining rewards
        transaction = Transaction(cfg.GENESIS_ACCOUNT_ID,
                                  self.account_id, cfg.AMOUNT_OF_REWARD)
        blockchain.add_transaction(transaction)

        # Make new block with new proof,
        #   transactions and hash of last block
        block = blockchain.new_block(new_proof)

        return block
