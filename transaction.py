# Transaction Object

from Crypto.PublicKey import ECC
from Crypto.Protocol import KDF
import Crypto

key = ECC.generate(curve="P-256")
privatekey = key.export_key(format="PEM")
from Crypto.Hash import SHA256

hash_key = SHA256.new(privatekey.encode("utf-8"))
passw = hash_key.hexdigest()
public_key = KDF.PBKDF2()

private_key = ECC.import_key()

class transaction:
    def __init__(self):
        self.sender = ""
        self.receiver = ""
        self.private = True
        self.data = None

    def verify(self):
        # Function to verify the transaction
        pass

    def encrypt(self):
        # Function to encrypt the document into the transaction
        from Crypto.Cipher import AES

        cipher = AES.new(self.private, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(self.data)
        file_out = open("encrypted.bin", "wb")
        [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]

    def decrypt(self):
        # Function to decrypt the document from the transaction
        key = RSA.importKey(open("private.pem").read())
        cipher = PKCS1_OAEP.new(key)
        message = cipher.decrypt(ciphertext)

