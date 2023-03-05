import rsa
import base64 
import os
import math

def generateKeys():
    if open('keys') != 1:
        os.mkdir('C:/projects/keys')

    (publicKey, privateKey) = rsa.newkeys(1024)
    with open('keys/publicKey.pem', 'wb') as p:
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

def deconstructSTR(message, public_key):
    if len(message) > 117:
        length = len(message)
        iterations = math.floor(length/117)
        encryptedStorage = []
        encryptedStorage.clear()

        for x in range(iterations-1):
            if x == 0:
                message_segment = message[0:116]
                encryptedStorage.append(str(encrypt(message_segment, public_key)))
            else:
                message_segment = message[(x*117):((x+1)*117)-1]
            
            encryptedStorage.append(str(encrypt(message_segment, public_key)))

        else: 
            return encryptedStorage
        
    else: 
        return rsa.encrypt(message.encode(), public_key) 

def decrypt(ciphertext, private_key):
    if type(ciphertext) == list:
        iterations = len(ciphertext)
        decipheredList = []
        decipheredList.clear()

        for x in range(iterations-1):
            if x == 0:
                message_segment = str(ciphertext[0:116])
                #decipheredList.append(message_segment)
                decipheredList.append(rsa.decrypt(message_segment, private_key).decode())
            else:
                message_segment = ciphertext[(x*117):((x+1)*117)-1]
            
            decipheredList.append(rsa.decrypt(str(message_segment), private_key).decode())

        else:
            return decipheredList
        
    return rsa.decrypt(ciphertext, private_key).decode()
    
def txtToString(fileName):
    with open(fileName, 'r') as file:
        string = file.read()
    return string

def encodePDF(fileName, public_key):
    with open(fileName, "rb") as pdf_file:
        encoded_str = base64.b64encode(pdf_file.read())

    return deconstructSTR(encoded_str, public_key)

def decodePDF(encrypted_str, private_key, fileName):
    encoded_str = decrypt(encrypted_str, private_key)
    decoded_str = base64.b64decode(encoded_str)
    file = open(fileName, 'wb')
    file.write(decoded_str)

def encodeIMAGE(fileName, public_key):
    with open(fileName, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())

    return deconstructSTR(str(my_string), public_key)

def decodeIMAGE(encrypted_str, private_key, fileName):
    encodedImage_str = decrypt(encrypted_str, private_key)
    with open(fileName, 'wb') as im:
        im.write(base64.decodebytes(encodedImage_str))



privateKey, publicKey = loadKeys()
#print(publicKey)
#print('\n')
#print(privateKey)
#print('\n')

message = txtToString('test.txt')
image = 'megamind.png'
encrypted_message = deconstructSTR(message, publicKey)
#encrypted_image = encodeIMAGE(image, publicKey)

#print(encrypted_message)
print(decrypt(encrypted_message, privateKey))
print('\n')

#print(encrypted_image)
#print('\n')
#print(decodeIMAGE(encrypted_image, privateKey))
