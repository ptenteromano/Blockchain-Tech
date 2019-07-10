#!/bin/sh

openssl genrsa -out private.pem
openssl rsa -in private.pem -out public.pub -pubout