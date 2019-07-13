 #!/bin/sh

# Use Public Key to Encrypt
# openssl rsautl -in pass.txt -out pass.enc -pubin -inkey key.pub -encrypt
echo "$1" | openssl rsautl -encrypt -out pass.enc -pubin -inkey rsa/public.pub

# cat pass.enc
# Use Private Key to Decrypt
openssl rsautl -in pass.enc -out pass.dec -inkey rsa/private.pem -decrypt
rm pass.enc
# cat pass.dec