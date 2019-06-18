# The web-application for our blockchain


# Imports
from flask import Flask, jsonify  # Web API
from blockchain import Blockchain

# Init our blockchain
blockchain = Blockchain()

# Start our web-app
app = Flask(__name__)

# These are our routes, You can check out the FLASK documentation:
# http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
# -----------------------
# A dummy root route
@app.route('/', methods=['GET'])
def root():
    return jsonify({'root': "Please check out postman!"})

# Route to mine block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    # Retrieve the previous block and nonce
    previous_block = blockchain.getPreviousBlock()
    previous_nonce = previous_block['nonce']

    # Start the mining process
    nonce = blockchain.proofOfWork(previous_nonce)

    # Hash the contents of the prior block
    previous_hash = blockchain.hash(previous_block)

    # Create the new block
    block = blockchain.createBlock(nonce, previous_hash)

    # Return a response in JSON to show the work
    response = {
        "message": "Congrats, You mined a new Block!",
        "blockNum": block["blockNum"],
        "timestamp": block["timestamp"],
        "nonce": block["nonce"],
        "previousHash": block["previousHash"]
    }

    # 200 is HTTP status: OK
    return jsonify(response), 200

# Route to return the entire chain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
     }

    return jsonify(response), 200

# Run the app
localHost = '0.0.0.0'
port = 5000
app.run(host=localHost, port=port)
