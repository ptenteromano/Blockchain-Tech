import subprocess

inputFile = "files/test.pdf"
cipherFile = "test.pdf.enc"
plaintextPw = "password"

# Arguments List:
# password, inputfile, output file

try:
    # ENCRYPTING
    subprocess.check_call(["./encrypt.sh", plaintextPw, inputFile, cipherFile])

    # Temporarily write password to file
    with open('pass.txt', 'w+') as tmpfile:
        tmpfile.write(plaintextPw)

    subprocess.check_call(["bash", "./rsaEncDec.sh"])

    with open(cipherFile, "r") as file:
        data = file.read()

except Exception as error:
    print(error)
    print("encyrpt")

obj = {
    'datastore': data
}

newCiphFile = 'new.pdf.enc'

with open(newCiphFile, "w") as file:
    file.write(data)
try:
    # DECRYPTING
    subprocess.check_call(
        ["./decrypt.sh", plaintextPw, newCiphFile, "output.pdf"])
except:
    print("decrypt")
