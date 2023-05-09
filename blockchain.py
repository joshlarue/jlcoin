import hashlib as hasher
import datetime as date
import json
from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS
import requests
node = Flask(__name__)
CORS(node)

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode("UTF-8"))
        return sha.hexdigest()

def create_genesis_block():
    return Block(0, date.datetime.now(), {
        "proof-of-work": 9,
        "transaactions": None
        }, "0")
    

miner_address = "josh"
blockchain = []
blockchain.append(create_genesis_block())
this_node_transactions = []
peer_nodes = []
mining = True

@node.route('/txion', methods=['POST'])
def transactions():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_node_transactions.append(new_txion)

        print("New transaction")
        print("FROM: {}".format(new_txion['from']))
        print("TO: {}".format(new_txion['to']))
        print("AMOUNT: {}\n".format(new_txion['amount']))
        print("Transaction submission successful.\n")
        
    transaction = request.get_json()
    f = open("blockchain.txt", "a")
    f.write("TIME: {}\n".format(date.datetime.now()))
    f.write("FROM: {}\n".format(transaction['from']))
    f.write("TO: {}\n".format(transaction['to']))
    f.write("AMOUNT: {}\n\n".format(transaction['amount']))
    f.close()
    
    return json.dumps({"message": "Transaction successful"})

def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor

@node.route('/mine', methods = ['GET'])
def mine():
    last_block = blockchain[len(blockchain) -1]
    last_proof = last_block.data['proof-of-work']

    proof = proof_of_work(last_proof)

    this_node_transactions.append(
        {"from": "network", "to": miner_address, "amount": 1}
    )

    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_node_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash

    this_node_transactions[:] = []

    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )

    blockchain.append(mined_block)

    f = open("blockchain.txt", "a")
    f.write(str(new_block_data))
    f.close()

    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    })

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = []
    for block in blockchain:
        block_dict = {
            "index": str(block.index),
            "timestamp": str(block.timestamp),
            "data": str(block.data),
            "hash": block.hash
        }
        chain_to_send.append(block_dict)
    chain_to_send_json = json.dumps(chain_to_send)
    return chain_to_send_json

def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        block = requests.get(node_url + '/blocks').content
        other_chains.append(block)
    return other_chains

def consensus():
    other_chains = find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    blockchain = longest_chain

@node.route('/')
def index():
    return render_template('index.html')

node.run()