# Implementatin of our blockchain
# Phil, Cesar, Antonio

# Object Oriented blockchain
# The container + chain where our blocks live

# Bring in some needed libraries
from datetime import datetime
import hashlib
import json
from urllib.parse import urlparse
import requests
from timeit import default_timer as timer


class Blockchain:

    # Initialize the chain and the genesis block
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.difficulty = "0000"
        self.difficultyArray = []
        self.createBlock(1, "0", None)  # Genesis block
        self.nodes = set()
        self.users = {}

    # This dict keeps track of all clients/miners using the chain
    def addUser(self, userId, publickey, miner=False):
        self.users[userId] = {"publicKey": publickey, "isMiner": miner}

    # Either add or subtract a "0" from the difficulty
    def changeDifficulty(self, increase=True):
        if increase:
            self.difficulty += "0"
        else:
            self.difficulty = self.difficulty[:-1]

    def getLength(self):
        return len(self.chain)

    # Block format is a dictonary
    # Hash_solution is the puzzle that solved it
    def createBlock(self, nonce, previous_hash, hash_solution):
        block = {
            "blockNum": len(self.chain) + 1,
            "timestamp": str(datetime.now().replace(microsecond=0)),
            "nonce": nonce,
            "hashSolution": hash_solution,
            "previousHash": previous_hash,
            "transactions": self.transactions,
        }

        # Empty the transactions
        self.transactions = []
        self.chain.append(block)
        self.difficultyArray.append(self.difficulty)

        return block

    # Returns the last block in the chain
    def getPreviousBlock(self):
        return self.chain[-1]

    # Solving the hash with the nonce
    def proofOfWork(self, previous_nonce):
        new_nonce = 1
        proof_of_work = False

        start = timer()
        while proof_of_work is False:
            # We can define our own proof-of-work puzzle (n**2 - pn**2) in this case
            hash_solution = hashlib.sha256(
                str((new_nonce ** 2 - previous_nonce ** 2) + len(self.chain)).encode(
                    "utf-8"
                )
            ).hexdigest()

            if hash_solution[: len(self.difficulty)] == self.difficulty:
                proof_of_work = True
            else:
                new_nonce += 1
        end = timer()

        return new_nonce, hash_solution, round(end - start, 6)

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
                print("No!")
                return False, block_index

            previous_nonce = previous_block["nonce"]
            nonce = block["nonce"]

            hash_operation = hashlib.sha256(
                str((nonce ** 2 - previous_nonce ** 2) +
                    block_index).encode("utf-8")
            ).hexdigest()

            try:
                difficultyAtBlock = self.difficultyArray[block_index]
                if hash_operation[:len(difficultyAtBlock)] != difficultyAtBlock:
                    return False, block_index
            except:
                print(len(self.difficultyArray), len(self.chain))
                

            # Move forward in the chain if everything checks out
            previous_block = block
            block_index += 1

        return True, len(self.chain)

    # Creates a transaction and returns the future next block number
    def addTransaction(self, sender, receiver, data):
        self.transactions.append(
            {"sender": sender, "receiver": receiver, "document": data}
        )

        previous_block = self.getPreviousBlock()

        return previous_block["blockNum"] + 1

    # Returns the address of a new node on the network
    def addNode(self, addressOfNode):
        parsed_url = urlparse(addressOfNode)
        self.nodes.add(parsed_url.netloc)

    def getNumNodes(self):
        return len(self.nodes)

    # Find the best chain-by-consensus on network (longest chain)
    def replaceChain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            try:
                response = requests.get(f"http://{node}/get_chain_json")

                if response.status_code == 200:
                    length = response.json()["length"]
                    chain = response.json()["chain"]
                    difficulties = list(response.json()["difficulties"])
                    print(len(difficulties), difficulties)

                    if length > max_length:  # (self.isChainValid(chain)):
                        print("yes!")
                        max_length = length
                        longest_chain = chain
                        chain_difficulties = difficulties
            except:
                continue

        if longest_chain:
            self.chain = longest_chain
            self.difficultyArray = chain_difficulties
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
                    "transactions": [
                        {
                            "sender": "You",
                            "receiver": "Theif",
                            "document": {"Your Bank Account": 123456789},
                        }
                    ],
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
