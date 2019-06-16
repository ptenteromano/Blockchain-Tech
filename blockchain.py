# Implementatin of our blockchain
# Phil, Cesar, Antonio

# Bring in some needed libraries
from datetime import datetime
import hashlib
import json
from flask import Flask, jsonify # Web API

# Object Oriented blockchain
# The container + chain where our blocks live
class Blockchain:

    # Initialize the chain and the genesis block
    def __init__(self):
        self.chain = []
        self.createBlock(nonce=1, previous_hash='0')
    
    def createBlock(self, nonce, previous_hash):
        block = {
            'blockNum': len(self.chain) + 1, 
            'timestamp': str(datetime.now()),
            'nonce': nonce,
            'previousHash': previous_hash
        }
        self.chain.append(block)
        return block

    def getPreviousBlock(self):
        return self.chain[-1]

    def proofOfWork(self, previous_nonce):
        nonce = 1
        proof_of_work = False
        while proof_of_work is False:
            # WIP --
            # I have other HW to do rn
            # I will handle this
            # hash_operation = 