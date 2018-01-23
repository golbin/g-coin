import gcoin.config as cfg
import gcoin.proof as proof
from gcoin.transaction import Transaction


class Miner:
    def __init__(self, account_id):
        self.account_id = account_id

    def __call__(self, blockchain):
        # Adding mining rewards
        transaction = Transaction(cfg.GENESIS_ACCOUNT_ID,
                                  self.account_id, cfg.AMOUNT_OF_REWARD)
        blockchain.add_transaction(transaction)

        # Make new block with transactions and hash of last block
        new_block = blockchain.new_block()

        # Proof of Work
        new_proof = proof.find_proof(new_block)

        new_block.proof = new_proof

        blockchain.add_block(new_block)

        return new_block

