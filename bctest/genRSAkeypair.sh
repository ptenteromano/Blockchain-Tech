#!/bin/sh

# --- This generates RSA w/ password --- 
openssl genrsa -des3 -out private.pem 2048

openssl rsa -in private.pem -outform PEM -pubout -out public.pem
