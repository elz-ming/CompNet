import time
from block import Block

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    # Adds 1st block to the chain
    def create_genesis_block(self):
        genesis_block = Block(
            index=0, 
            transactions=[], 
            timestamp=time.time(), 
            previous_hash="0"
        )
        self.chain.append(genesis_block)

    # Adds 2nd and incoming blocks to the chain after verification.
    def add_block(self, new_block, proof):
        if self.last_block.hash != new_block.previous_hash or not self.valid_proof(new_block, proof):
            return False
        self.chain.append(new_block)
        return True
    
    # Checks if a block's hash is valid
    def valid_proof(self, block, block_hash):
        return block_hash.startswith('0000') and block_hash == block.hash
    
    # Finds a nonce that results in a valid hash
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0000'):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    # Mines a new block with the unconfirmed transactions
    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        
        last_block = self.last_block
        new_block = Block(
            index=last_block.index+1,
            transactions=self.unconfirmed_transactions,
            timestamp=time.time(),
            previous_hash=last_block.hash
        )

        proof = self.proof_of_work(new_block)
        if self.add_block(new_block, proof):
            self.unconfirmed_transactions = []
            return new_block.index
        return False

    # Add unconfirmed transactions to the list, to be solved 1 by 1
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    # Validates if there's any corruption in data or unauthorized modifications
    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            # Check current block's hash is correct
            if current.hash != current.compute_hash():
                return False
            # Check current block's hash of the previous block is correct
            if current.previous_hash != previous.hash:
                return False
        return True
    
    # Defining properties of class to become immutable by using @property, making it read-only
    @property
    def last_block(self): return self.chain[-1]