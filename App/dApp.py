# The web-application for our blockchain

# Imports
from Blockchain import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

# Init our blockchain
blockchain = Blockchain()

node_address = str(uuid4()).replace('-', '')

# Start our web-app
# These are our routes, You can check out the FLASK documentation:
# http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
# -----------------------
# The Home Route
@app.route("/", methods=["GET"])
def root():
    return """<html><body>
            <h1>Welcome to SECuChain!</h1>
            <a href="/get_chain">Look at the Chain</a>
            </body></html>"""


# Route to mine block
@app.route("/mine_block", methods=["GET"])
def mine_block():
    # Retrieve the previous block and nonce
    previous_block = blockchain.getPreviousBlock()
    previous_nonce = previous_block["nonce"]

    # Start the mining process
    nonce, hash_solution = blockchain.proofOfWork(previous_nonce)

    # Hash the contents of the prior block
    previous_hash = blockchain.hash(previous_block)
    blockchain.addTransaction(
        sender=node_address, receiver='Phil', data='Dummy.pdf')

    # Create the new block
    block = blockchain.createBlock(nonce, previous_hash, hash_solution)

    # Return a response in JSON to show the work
    response = {
        "message": "Congrats, You mined a new Block!",
        "blockNum": block["blockNum"],
        "timestamp": block["timestamp"],
        "nonce": block["nonce"],
        "hashSolution": block["hashSolution"],
        "previousHash": block["previousHash"],
        "transactions": block["transactions"]
    }

    # 200 is HTTP status: OK
    return jsonify(response), 200


# Route to return the entire chain
@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}

    return jsonify(response), 200


# Route to return the entire chain
@app.route("/is_valid", methods=["GET"])
def is_valid():
    is_valid, last_good_block = blockchain.isChainValid(blockchain.chain)
    if is_valid:
        msg = "Valid Chain!"
    else:
        msg = "Incorrect, check the last valid block number!"

    response = {"message": msg, "last_valid_block": last_good_block}

    return jsonify(response), 200


# Simulate a fake blocks
@app.route("/fake_blocks", methods=["GET"])
def fake_blocks():
    blockchain.simulateFakeBlocks()
    response = {"message": "Fake blocks generated"}

    return jsonify(response), 200


@app.route("/prune_fakes", methods=["GET"])
def prune_fakes():
    pruned, last_valid_block = blockchain.pruneFakeBlocks()

    if pruned:
        msg = "Fake blocks found and pruned"
    else:
        msg = "No fake blocks found"

    response = {"message": msg, "last_valid_block": last_valid_block}

    return jsonify(response), 200


# --------- No Other functions Below This Line --------
# Run the app
localHost = "0.0.0.0"
port = 5000
app.run(host=localHost, port=port)
