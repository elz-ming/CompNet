import hashlib

# Defines a block that will be used in blockchain.py
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    # For display and debug purpose
    def to_dict(self):
        return {
            'index': self.index,
            'transactions': [t.to_dict() for t in self.transactions],  # Assuming transactions are objects that can also be converted to dictionaries
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash,  # Add this line if your Block class stores its own hash
        }
    
    # Defining properties of class to become immutable by using @property, making it read-only

    # @property
    # def index(self): return self._index
    
    # @property
    # def transactions(self): return self._transactions[:]

    # @property
    # def timestamp(self): return self._timestamp

    # @property
    # def previous_hash(self): return self._previous_hash

    # @property
    # def nonce(self): return self._nonce

    # @property
    # def hash(self): return self._hash