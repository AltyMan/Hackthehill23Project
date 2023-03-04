import rsa
import base64 

def generateKeys():
    (publicKey, privateKey) = rsa.newkeys(1024)
    with open('keys/publcKey.pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open('keys/privateKey.pem', 'wb') as f:
        f.write(privateKey.save_pkcs1('PEM'))

def loadKeys():
    with open('keys/publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as f:
        privateKey = rsa.PrivateKey.load_pkcs1(f.read())
    return privateKey, publicKey

def encrypt(message, public_key):
    return rsa.encrypt(message.encode(), public_key)

def decrypt(ciphertext, private_key):
    try:
        return rsa.decrypt(ciphertext, private_key).decode()
    except:
        return False

def encodePDF(fileName, public_key):
    with open(fileName, "rb") as pdf_file:
        encoded_str = base64.b64encode(pdf_file.read())

    return encrypt(encoded_str, public_key)

def decodePDF(encrypted_str, private_key, fileName):
    encoded_str = decrypt(encrypted_str, private_key)
    decoded_str = base64.b64decode(encrypted_str)
    file = open(fileName, 'wb')
    file.write(encoded_str)
