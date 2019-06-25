# SECuChain
### Revolutionizing How Financial Institutions Report

<small>Philip Tenteromano</small>
<small>Antonio Segalini</small>
<small>Cesar Reynoso</small>

<hr>

<strong>WIP</strong>

### TODO:
Nonce + TIMESTAMP
- Make nonce 32bit intenger (~4 bill max)

Finish Hybrid Encryption
- We have the AES (symmetric) encrypts pdf with password
- Need RSA public key to encrypt the password
- Send: 
    AES(document) + RSA_PUBLIC_Receiver(password) + RSA_PUBLIC_Sender(password) 
    + HASH(originalPDF) + ?HASH(originalPW)?

Get multiple servers up - connect them

PERSIST the blockchain?
- Possible database store?

<hr>

### Goals:

