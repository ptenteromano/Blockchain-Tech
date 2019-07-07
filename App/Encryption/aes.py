import subprocess

inputFile = "files/test.pdf"
cipherFile = "test.pdf.enc"
# plaintextPw = "ThisIsAReallyBigAndBad!!!%!@#$%^&*()_+PASSword"
print("Input a password please")
plaintextPw = input()

# Arguments List:
# password, inputfile, output file

try:
    # ENCRYPTING
    subprocess.check_call(["./encrypt.sh", plaintextPw, inputFile, cipherFile])

    # Encrypt password
    subprocess.check_call(["bash", "./rsaEncDec.sh", plaintextPw])

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

f = open("pass.dec","r+")
passDec = ''
for line in f:
    passDec += (line).replace('\n', '')

try:
    # DECRYPTING
    subprocess.check_call(
        ["./decrypt.sh", passDec, newCiphFile, "output.pdf"])
except:
    print("decrypt")
