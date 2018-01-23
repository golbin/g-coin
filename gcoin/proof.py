import hashlib

import gcoin.config as cfg


def valid_proof(block, proof=None):
    """ Validates proof

    last digits of hash(previous_block.header, proof)
        == config.VALID_DIGITS

    Args:
        block (obj):
        proof (int): proof to validate

    Returns:
        bool:
    """
    proof = proof if proof else block.proof

    proof_seed = '{0}{1}'.format(block.header.hash(),
                                 proof).encode()

    proof_hash = hashlib.sha256(proof_seed).hexdigest()

    return proof_hash[:cfg.DIFFICULTY] == cfg.VALID_DIGITS


def find_proof(block):
    """proof of work

    Args:
        block (obj):

    Returns:
        int: proof
    """
    proof = 0

    while valid_proof(block, proof) is False:
        proof += 1

    return proof

