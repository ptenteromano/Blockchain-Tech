# Implementatin of our blockchain
# Phil, Cesar, Antonio

# Bring in some needed libraries
from datetime import datetime
import hashlib
import json

# Object Oriented blockchain
# The container + chain where our blocks live


class Blockchain:

    # Initialize the chain and the genesis block
    def __init__(self):
        self.chain = []
        self.createBlock(nonce=1, previous_hash='0')
        self.diffculty = "0000"

    # Block format is a dictonary
    def createBlock(self, nonce, previous_hash):
        block = {
            'blockNum': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'nonce': nonce,
            'previousHash': previous_hash
        }
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
                str(new_nonce ** 2 - previous_nonce ** 2).encode('utf-8')).hexdigest()

            if hash_operation[:len(self.diffculty)] == self.diffculty:
                proof_of_work = True
            else:
                new_nonce += 1

        return new_nonce

    # Hash the contents of a block's dictionary
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode('utf-8')

        return hashlib.sha256(encoded_block).hexdigest()

    # Check if chain has all valid blocks
    def isChainValid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block['previousHash'] != self.hash(previous_block):
                return False, block_index

            previous_nonce = previous_block['nonce']
            nonce = block['nonce']

            hash_operation = hashlib.sha256(
                str(nonce ** 2 - previous_nonce ** 2).encode('utf-8')).hexdigest()

            if hash_operation[:len(self.diffculty)] != self.diffculty:
                return False, block_index

            # Move forward in the chain if everything checks out
            previous_block = block
            block_index += 1

        return True, len(self.chain)

    # Function to append bogus blocks to chain
    def simulateFakeBlocks(self):
        for _ in range(2):
            self.chain.append({
                'blockNum': len(self.chain) + 1,
                'timestamp': "Never",
                'nonce': -1,
                'previousHash': 'FAKE BLOCK'
            })

    def pruneFakeBlocks(self):
        is_valid, last_good_block = self.isChainValid(self.chain)

        if not is_valid:
            self.chain = self.chain[:last_good_block]
            return True
        return False


# --- Testing Functions below ---
# bc = Blockchain()

# print(bc.isChainValid(bc.chain))
