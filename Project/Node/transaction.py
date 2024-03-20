class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }
    
    # Defining properties of class to become immutable by using @property, making it read-only
    @property
    def sender(self): return self._sender

    @property
    def recipient(self): return self._recipient

    @property
    def amount(self): return self._amount