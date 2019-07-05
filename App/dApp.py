# The web-application for our blockchain


# Imports
from flask import Flask, jsonify  # Web API
from Blockchain import Blockchain

# Init our blockchain
blockchain = Blockchain()

# Start our web-app
app = Flask(__name__)

# These are our routes, You can check out the FLASK documentation:
# http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
# -----------------------
# A dummy root route
@app.route("/", methods=["GET"])
def root():
    return """<html><body>
            <title>SECuchain</title>
            <h1>Welcome to SECuChain!</h1>
            <a href="/get_chain">Look at the Chain<a>
            <br/>
            <a href="/upload_file">Upload a File</a>
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

# Prune the fake blocks
@app.route("/prune_fakes", methods=["GET"])
def prune_fakes():
    pruned, last_valid_block = blockchain.pruneFakeBlocks()

    if pruned:
        msg = "Fake blocks found and pruned"
    else:
        msg = "No fake blocks found"

    response = {"message": msg, "last_valid_block": last_valid_block}

    return jsonify(response), 200

# Upload files codes

import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

# Config of upload

UPLOAD_FOLDER = 'C:/Users/cesar/Desktop'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Config of type of files allowed
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Html Upload File page
@app.route("/upload_file", methods=["GET"])
def upload_form():
	return """<!doctype html>
              <title>SECuchain Multiple Files Upload Page</title>
              <h1>SECuchain Multiple Files Upload Page</h1>
              <h2>Select file(s) to upload</h2>
              <p>
	          Welcome to SECuChain Upload page!
		      <ul class=flashes>
		      You can upload one or several files at a time.
		      <li>Formats supported: txt, pdf, png, jpg, jpeg, gif</li>
		      Max file size is 16MB.
		      </ul>
              <form method="post" action="/" enctype="multipart/form-data">
              <dl>
		      <p>
              <input type="file" name="files[]" multiple="true" autocomplete="off" required>
              </p>
              </dl>
              <p>
		      <input type="submit" value="Submit">
	          </p>
              </form>"""

@app.route("/upload_successful", methods=["GET"])
def upload_succ():
	return """<!doctype html>
              <title>SECuchain Multiple Files Upload Page</title>
              <h1>SECuchain Multiple Files Upload Page</h1>
              <h2>Select file(s) to upload</h2>
              <p>
	          Welcome to SECuChain Upload page!
		      <ul class=flashes>
		      You can upload one or several files at a time.
		      <li>Formats supported: txt, pdf, png, jpg, jpeg, gif</li>
		      Max file size is 16MB.
		      </ul>
              <form method="post" action="/" enctype="multipart/form-data">
              <dl>
              <p>
              Succesfully Uploaded!
              <p>
		      <p>
              <input type="file" name="files[]" multiple="true" autocomplete="off" required>
              </p>
              </dl>
              <p>
		      <input type="submit" value="Submit">
	          </p>
              </form>"""

# Upload file function
@app.route('/', methods=['POST'])
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
	



# --------- No Other functions Below This Line --------
# Run the app
localHost = "0.0.0.0"
port = 5000
app.run(host=localHost, port=port)
