# The web-application for our blockchain

import os
from Blockchain import Blockchain
from flask import Flask, jsonify, request, render_template, url_for, redirect
from uuid import uuid4

app = Flask(__name__)

# Init our blockchain
blockchain = Blockchain()

node_address = str(uuid4()).replace("-", "")

# Start our web-app
# These are our routes, You can check out the FLASK documentation:
# http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
# -----------------------
# The Home Route
@app.route("/", methods=["GET"])
def root():
    return (
        render_template(
            "homepage.html", length=blockchain.getLength(), diff=blockchain.difficulty
        ),
        200,
    )


# Route to mine block
@app.route("/mine_block", methods=["GET"])
def mine_block():
    # Retrieve the previous block and nonce
    previous_block = blockchain.getPreviousBlock()
    previous_nonce = previous_block["nonce"]

    # Start the mining process
    nonce, hash_solution, time = blockchain.proofOfWork(previous_nonce)

    # Hash the contents of the prior block
    previous_hash = blockchain.hash(previous_block)
    blockchain.addTransaction(sender=node_address, receiver="Phil", data="Dummy.pdf")

    # Create the new block
    block = blockchain.createBlock(nonce, previous_hash, hash_solution)

    block["message"] = "Congrats, you mined a new Block!"

    return render_template("mineblock.html", block=block, time=time, diff=blockchain.difficulty), 200


# Route to return the entire chain
@app.route("/get_chain", methods=["GET"])
def get_chain():
    return render_template("showchain.html")


# Route to return if chain is valid or not
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
    return render_template("fakeblocks.html"), 200


@app.route("/prune_fakes", methods=["GET"])
def prune_fakes():
    before_prune = blockchain.getLength()
    pruned, last_valid_block = blockchain.pruneFakeBlocks()

    removed = before_prune - last_valid_block

    return render_template("prunefakes.html", pruned=pruned, removed=removed), 200


@app.route("/increase_diff", methods=["POST"])
def increase_diff():
    blockchain.changeDifficulty(increase=True)
    return redirect("/")


@app.route("/decrease_diff", methods=["POST"])
def decrease_diff():
    blockchain.changeDifficulty(increase=False)
    return redirect("/")


# Context for entire app
@app.context_processor
def get_context():
    return dict(
        url_for=dated_url_for, isvalid=blockchain.isChainValid, chain=blockchain.chain
    )


def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename", None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values["q"] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# --------- No Other functions Below This Line --------
# Run the app
localHost = "0.0.0.0"
port = 5000
app.run(host=localHost, port=port)