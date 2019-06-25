#!/bin/sh

# Remember to change permissions on these files
# `chmod u+x ---.sh`

# First arg - password
# Second Arg - input file (ciphertext)
# Third Arg - output file (decrypted)

# Works with file location
openssl aes-256-cbc -d -a -in "$2" -out "$3" -k "$1"

# Works with raw string variable -- throws error on large size
# echo "$2" | openssl aes-256-cbc -d -a -out "$3" -k "$1"