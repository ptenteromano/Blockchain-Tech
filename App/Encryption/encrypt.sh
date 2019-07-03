#!/bin/sh

# Remember to change permissions on these files
# `chmod u+x ---.sh`

# First arg - password
# Second Arg - input file (plaintext)
# Third Arg - output file (ciphertext)

openssl aes-256-cbc -a -salt -in "$2" -out "$3" -k "$1"