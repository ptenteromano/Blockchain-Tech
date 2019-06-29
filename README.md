# SECuChain
### Revolutionizing How Financial Institutions Report

<small>Philip Tenteromano</small>
<small>Antonio Segalini</small>
<small>Cesar Reynoso</small>

<hr>

<strong>WIP</strong>

### How to install
1. Run `bash install.sh` to start

### TODO:
Nonce + TIMESTAMP
- Make nonce 32bit intenger (~4 bill max)
- Unsigned
- Change block configuration (not likely for us)

Finish Hybrid Encryption
- We have the AES (symmetric) encrypts pdf with password
- Need RSA public key to encrypt JUST password
- Sender sends: 
    AES(document) + RSA_PUBLIC_Receiver(password) + RSA_PUBLIC_Sender(password) 
    + HASH(originalPDF) + ?HASH(originalPW)?

Clean up directories
Make bash aes and rsa Encrypt/Decrypt more general

Generate RSA's for all new members and make wallets

Get multiple servers up - connect them

PERSIST the blockchain?
- Possible database store?

Mempool for transactions
- Staging area

### Thoughts?
How to entice the miners?
- Fees?

<hr>

### Goals:

### Resources:

-Cryptography Python Package
https://pycryptodome.readthedocs.io/en/latest/src/cipher/pkcs1_v1_5.html
This contains, RSA Key creating, encryption and decryption

