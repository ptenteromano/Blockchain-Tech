import subprocess

inputFile = 'files/test.pdf'
cipherFile = 'test.pdf.enc'
plaintextPw = 'password'

# Arguments List:
# password, inputfile, output file

try:
    # ENCRYPTING
    subprocess.check_call(['./encrypt.sh', plaintextPw, inputFile, cipherFile])
except:
    print("encyrpt")

try:
    # DECRYPTING
    subprocess.check_call(['./decrypt.sh', plaintextPw, cipherFile, "output.pdf"])
except:
    print('decrypt')

    