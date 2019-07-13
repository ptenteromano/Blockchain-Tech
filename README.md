# SECuChain
### Revolutionizing How Financial Institutions Report

<small>Philip Tenteromano</small>
<small>Antonio Segalini</small>
<small>Cesar Reynoso</small>

<hr>

<strong>WIP</strong>

### How to install (Mac)
1. Ensure python3 is installed (try `which python3`)
2. Run `./install.sh` 
     - This changes the permissions on all necessary files
     - This creates a virtual environment (venv) in python3
     - Finally, it installs all necessary dependencies into this venv

<p>Note: type `deactivate` to come out of the `venv`</p>
<p>Note: to return to the `venv`, run the command `source venv/bin/activate`</P>


### Updated to do
- Owner to block miner
- wallets
- transactions


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

