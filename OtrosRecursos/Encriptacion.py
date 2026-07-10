from cryptography.fernet import Fernet

import base64



def cifrar(key):
    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open('demoEncriptacion.txt', 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open('demoEncriptacion.txt', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


#Descifrar
def descifrar(key):
    fernet = Fernet(key)
    with open('demoEncriptacion.txt') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted.encode())
    with open('demoEncriptacion.txt', 'wb') as dec_file:
        dec_file.write(decrypted)
key = "aRt3k"#La complemento con espacios, por que solo acepta 32 bytes en base 64
for i in range(32-len(key)):
    key += " "
key = base64.b64encode(bytes(key, "UTF-8"))

cifrar(key)
descifrar(key)