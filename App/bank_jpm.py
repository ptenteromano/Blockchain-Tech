# The web-application for our blockchain

# Citi bank
import os
from Blockchain import Blockchain
from flask import Flask, jsonify, request, \
    render_template, url_for, redirect, flash
from uuid import uuid4
import urllib.request
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Init our blockchain
blockchain = Blockchain()

node_name = "JP Morgan"
node_address = str(uuid4()).replace("-", "")

nodes = [{"name": node_name, "address": node_address, "isSelf": True}]

connectNodes = ["http://0.0.0.0:5001/", "http://0.0.0.0:5002/", "http://0.0.0.0:5003/"]

testAdd = {"name": "BOA", "address": 1234, "isSelf": False}
nodes.append(testAdd)
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
    blockchain.addTransaction(
        sender=node_address, receiver="Phil", data="Dummy.pdf")

    # Create the new block
    block = blockchain.createBlock(nonce, previous_hash, hash_solution)

    block["message"] = "Congrats, you mined a new Block!"

    return render_template("mineblock.html", block=block, time=time, diff=blockchain.difficulty), 200


# Route to return the entire chain
@app.route("/get_chain", methods=["GET"])
def get_chain():
    return render_template("showchain.html")

@app.route("/get_chain_json", methods=["GET"])
def get_chain_json():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'difficulties': blockchain.difficultyArray
    }
    return jsonify(response), 200

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

# -----------
# Transactions
@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        json = request.get_json()
        transaction_keys = ["sender", "receiver", "data"]

        if not all(key for key in transaction_keys):
            return "Some elements of transaction are missing", 400

        block_num = blockchain.addTransaction(
            json["sender"], json["receiver"], json["data"])

        response = {
            "message": f"This transaction added to block number {block_num}"}
        return jsonify(response), 201
    else:
        return redirect("/"), 200

# ------------
# Decentralization
@app.route("/connect_nodes", methods=["GET"])
def connect_nodes():
    for node in connectNodes:
        blockchain.addNode(node)
    return redirect("/")

@app.route("/replace_chain", methods=["GET"])
def replace_chain():
    is_chain_replaced = blockchain.replaceChain()
    
    if is_chain_replaced:
        msg = "Chain has been replaced by another nodes"
    else:
        msg = "Your chain is the largest one!"

    return render_template("/showchain.html", msg=msg)

# ------------------
# Upload Files section
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "/files/jpm/"

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Config of type of files allowed
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload_file", methods=["GET"])
def upload_form():
    return render_template("uploadform.html"), 200


@app.route("/upload_successful", methods=["GET"])
def upload_succ():

    otherNodes = [
        {'name': "Citi", 'address': '0.0.0.0:5002'},
        {'name': "BoA", 'address': '0.0.0.0:5003'}
    ]

    return render_template("uploadsuccess.html",  nodes=otherNodes), 200

# Upload file function
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File(s) successfully uploaded')
        return redirect('/upload_successful')

# ----------------
# Context for entire app
@app.context_processor
def get_context():
    return dict(
        url_for=dated_url_for, isvalid=blockchain.isChainValid, chain=blockchain.chain, user=node_name, numNodes=blockchain.getNumNodes
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
port = 5001
app.run(host=localHost, port=port)
