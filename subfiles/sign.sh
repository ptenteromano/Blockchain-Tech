# Philip Tenteromano
# 6/15/2019

# Print out passed argument
echo "$1"

# Pipe argument into a hash, pipe hash into the private key for signing

# Create signature with Private Key
echo "$1" | openssl sha256 | openssl dgst -sha256 -sign key.pem > signature.bin

# Verify Message with Public Key
echo "$1" | openssl sha256 | openssl dgst -sha256 -verify public.pem -signature signature.bin 

# Verify false
echo "Trying to verify: $1 $1"
echo "$1 $1" | openssl sha256 | openssl dgst -sha256 -verify public.pem -signature signature.bin 
