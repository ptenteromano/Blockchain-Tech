import hashlib


class Transaction:
    def __init__(self):
        self.receiver = ""
        self.sender = {}
        self.document = ""

    def addSender(self, sndr):
        self.senderTxView = sndr
        self.senderPublicKey = sndr['publicKey']

    def addReceiver(self, rcvr):
        self.receiverTxView = rcvr
        self.receiverPublicKey = rcvr['publicKey']

    def encryptTransaction(self, document, plaintextPw):
        try:
            with open(document, "r") as file:
                docData = file.read()
        except:
            return "Cannot Find File"

        # hash, rsaPw, rsaPw, sndr, rcvr, encPw, sign(hash, sndr, rcvr)
        encryptedData = {
            "hash": hashlib.sha256(str(docData).encode()).hexdigest()
        }

        cipherDoc = "cipherDoc.enc"
        subprocess.check_call(["./encrypt.sh", plaintextPw, inputFile, cipherDoc])

        with open(cipherDoc, "r") as file:
            encData = file.read()
        
        # two down
        encryptedData["aesCipher"] = encData

        # Start 
        self.receiverPublicKey

        del plaintextPw

    def sendTransaction(self):
        self.document

