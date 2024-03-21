# Test_1 - Creation of a block
from block import Block
import time

genesis_block = Block(0, [], time.time(), "0")
genesis_block.hash = genesis_block.compute_hash()
# print(genesis_block.hash)

# Test_2 - Creation of a blockchain
from blockchain import Blockchain
import time

myBlockchain = Blockchain()
def create_fake_transaction():
    return {"sender": "Alice", "recipient": "Bob", "amount": 5}
for i in range (1, 5):
    transactions = [create_fake_transaction() for _ in range(2)]
    new_block = Block(index=i, transactions=transactions, timestamp=time.time(), previous_hash=myBlockchain.chain[-1].hash)
    myBlockchain.add_block(new_block)
# for block in myBlockchain.chain:
#     print(f"Block {block.index}: {block.hash}")

# if myBlockchain.is_valid_chain():
#     print("VALID")
# else:
#     print("Not VALID")


# Test_3 - Creation of a transaction
from transaction import Transaction

transaction1 = Transaction('Alice', 'Bob', 50)
transaction2 = Transaction('Bob', 'Charlie', 25)
# print("Transaction 1:", transaction1.to_dict())
# print("Transaction 2:", transaction2.to_dict())

# Test_4 - Testing out node.py new_transaction function
import requests

url = 'http://127.0.0.1:5000/transactions/new'
payload = {
    'sender': 'Alice',
    'recipient': 'Bob',
    'amount': 10
}
headers = {'Contrent-Type':'application/json'}

response = requests.post(url, json=payload, headers=headers)
print(response.json())