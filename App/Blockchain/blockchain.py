# Implementatin of our blockchain
# Phil, Cesar, Antonio

# Bring in some needed libraries
from datetime import datetime
import hashlib
import json

# 2nd part
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Object Oriented blockchain
# The container + chain where our blocks live


class Blockchain:

    # Initialize the chain and the genesis block
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.createBlock(1, "0", None)  # Genesis block
        self.diffculty = "0000"
        self.nodes = set()
        self.users = {}

    # This dict keeps track of all clients/miners using the chain
    def addUser(self, userId, publickey, miner=False):
        self.users[userId] = {"publicKey": publickey, "isMiner": miner}

    # Either add or subtract a "0" from the difficulty
    def changeDifficulty(self, increase=True):
        if increase:
            self.diffculty += "0"
        else:
            self.diffculty = self.diffculty[:-1]

    # Block format is a dictonary
    # Hash_solution is the puzzle that solved it
    def createBlock(self, nonce, previous_hash, hash_solution):
        block = {
            "blockNum": len(self.chain) + 1,
            "timestamp": str(datetime.now()),
            "nonce": nonce,
            "hashSolution": hash_solution,
            "previousHash": previous_hash,
            "transactions": self.transactions
        }
        # Empty the transactions
        self.transactions = []

        self.chain.append(block)
        return block

    # Returns the last block in the chain
    def getPreviousBlock(self):
        return self.chain[-1]

    # Solving the hash with the nonce
    def proofOfWork(self, previous_nonce):
        new_nonce = 1
        proof_of_work = False

        while proof_of_work is False:
            # We can define our own proof-of-work puzzle (n**2 - pn**2) in this case
            hash_operation = hashlib.sha256(
                str((new_nonce ** 2 - previous_nonce ** 2) + len(self.chain)).encode(
                    "utf-8"
                )
            ).hexdigest()

            if hash_operation[: len(self.diffculty)] == self.diffculty:
                proof_of_work = True
            else:
                new_nonce += 1

        return new_nonce, hash_operation

    # Hash the contents of the entire block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode("utf-8")

        return hashlib.sha256(encoded_block).hexdigest()

    # Check if chain has all valid blocks
    def isChainValid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block["previousHash"] != self.hash(previous_block):
                return False, block_index

            previous_nonce = previous_block["nonce"]
            nonce = block["nonce"]

            hash_operation = hashlib.sha256(
                str((nonce ** 2 - previous_nonce ** 2) +
                    block_index).encode("utf-8")
            ).hexdigest()

            if hash_operation[: len(self.diffculty)] != self.diffculty:
                return False, block_index

            # Move forward in the chain if everything checks out
            previous_block = block
            block_index += 1

        return True, len(self.chain)

    # Creates a transaction and returns the future next block number
    def addTransaction(self, sender, receiver, data):
        self.transactions.append({
            "sender": sender,
            "receiver": receiver,
            "document": data
        })

        previous_block = self.getPreviousBlock()

        return previous_block['blockNum'] + 1

    # Returns the address of a new node on the network
    def addNode(self, addressOfNode):
        parsed_url = urlparse(addressOfNode)
        self.nodes.add(parsed_url.netloc)

    # Find the best chain-by-consensus on network (longest chain)
    def replaceChain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f"http://{node}/get_chain")

            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                if length > max_length and self.isChainValid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False

    # Functions to append bogus blocks to chain and remove

    def simulateFakeBlocks(self):
        for _ in range(2):
            self.chain.append(
                {
                    "blockNum": len(self.chain) + 1,
                    "timestamp": "Never",
                    "nonce": -1,
                    "previousHash": "FAKE BLOCK",
                }
            )

    def pruneFakeBlocks(self):
        is_valid, last_valid_block = self.isChainValid(self.chain)

        if not is_valid:
            self.chain = self.chain[:last_valid_block]
            return True, last_valid_block
        return False, last_valid_block


# --- Testing Functions below ---
# bc = Blockchain()

# print(bc.isChainValid(bc.chain))
