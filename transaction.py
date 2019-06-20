#Transaction Object

from Crypto.PublicKey import ECC
from Crypto.Protocol import KDF
import Crypto
key = ECC.generate(curve='P-256')
privatekey = key.export_key(format='PEM')
from Crypto.Hash import SHA256
hash_key = SHA256.new(privatekey.encode('utf-8'))
passw = hash_key.hexdigest()
public_key = KDF.PBKDF2()

private_key = ECC.import_key()

#from Crypto.PublicKey import RSA
#
##create private key and stores it on file names private.pem
#key = RSA.generate(2048)
#private = key.exportKey('PEM').decode('ascii')
#file_out = open("private.pem", "wb") 
#file_out.write(private)
#
##create public key and stores it on file names receiver.pem
#public = key.publickey().exportKey('PEM').decode('ascii')
#file_out = open("receiver.pem", "wb")  
#file_out.write(public)


class transaction:
    def __init__(self):
        self.sender=0
        self.receiver=0
        self.private=0
        self.data=0
        
    def verify(self):
        #Function to verify the transaction
        
    def encrypt(self):
        #Function to encrypt the document into the transaction
        from Crypto.Cipher import AES
        cipher = AES.new(self.private, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(self.data)
        file_out = open("encrypted.bin", "wb")
        [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
        
    def decrypt(self):
        #Function to decrypt the document from the transaction
        key = RSA.importKey(open('private.pem').read())
        cipher = PKCS1_OAEP.new(key)
        message = cipher.decrypt(ciphertext)
        