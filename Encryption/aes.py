import subprocess

inputFile = "files/test.pdf"
cipherFile = "test.pdf.enc"
plaintextPw = "password"

# Arguments List:
# password, inputfile, output file

try:
    # ENCRYPTING
    subprocess.check_call(["./encrypt.sh", plaintextPw, inputFile, cipherFile])
    with open(cipherFile, "r") as file:
        data = file.read()  # .replace('\n', '')
except:
    print("encyrpt")

obj = {
    'datastore': data
}

newCiphFile = 'new.pdf.enc'

with open(newCiphFile, "w") as file:
        file.write(data)
try:
    # DECRYPTING
    subprocess.check_call(["./decrypt.sh", plaintextPw, newCiphFile, "output.pdf"])
except:
    print("decrypt")

