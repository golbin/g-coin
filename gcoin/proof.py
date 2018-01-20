import hashlib

DIFFICULTY = 1  # number of digits is difficulty
VALID_DIGITS = '0' * DIFFICULTY


def valid_proof(last_proof, proof):
    """ Validates proof

    last digits of hash(last_proof, proof)
        == VALID_DIGITS

    Args:
        last_proof (int): previous proof
        proof (int): proof to validate

    Returns:
        bool:
    """
    proof_seed = '{0}{1}'.format(last_proof, proof).encode()
    proof_hash = hashlib.sha256(proof_seed).hexdigest()

    return proof_hash[:DIFFICULTY] == VALID_DIGITS


def find_proof(last_proof):
    """proof of work

    Args:
        last_proof (int):

    Returns:
        int: proof
    """
    proof = 0

    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof

