 #!/bin/sh
 
# --- This generates RSA w/ password --- 
# # Use Public Key to Encrypt
# openssl rsautl -in pass.txt -out pass.enc -pubin -inkey rsa/public.pub -encrypt
# rm pass.txt

# # Use Private Key to Decrypt
# openssl rsautl -in pass.enc -out pass.dec -inkey rsa/private.pem -decrypt
# rm pass.enc

# Use Public Key to Encrypt
openssl rsautl -in pass.txt -out pass.enc -pubin -inkey key.pub -encrypt
rm pass.txt

cat pass.enc
# Use Private Key to Decrypt
openssl rsautl -in pass.enc -out pass.dec -inkey key.pem -decrypt
rm pass.enc
cat pass.dec