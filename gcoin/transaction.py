
class Transaction:
    def __init__(self, sender, recipient, amount):
        """Transaction

        Args:
            sender (str):
            recipient (str):
            amount (int): positive number
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

        if amount < 1:
            raise Exception('Amount have to be positive number.')

    def dump(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

    @classmethod
    def init_from_json(cls, data):
        return cls(data['sender'],
                   data['recipient'],
                   data['amount'])
