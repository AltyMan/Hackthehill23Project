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
        #print(length)
        iterations = math.floor(length/117)
        #print(iterations)
        #print(length%117)
        encryptedStorage = []
        encryptedStorage.clear()

        for x in range(iterations+1):
            message_segment = message[(x*117):((x+1)*117)]
            encryptedStorage.append(encrypt(message_segment, public_key))
        else:
            message_segment = message[((iterations+2)*117):
                                      (((iterations+3)*117)-(length%117))]
            encryptedStorage.append(encrypt(message_segment, public_key))
            return encryptedStorage
        
    else: 
        return rsa.encrypt(message.encode(), public_key) 

def decrypt(ciphertext, private_key):
    if type(ciphertext) == list:
        print("")
        iterations = len(ciphertext)
        decipheredList = []
        decipheredList.clear()

        for x in range(iterations-1):
            decryptedItem = rsa.decrypt(ciphertext[x], private_key).decode()
            decipheredList.append(decryptedItem)

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
    theString = concatenate(encodedImage_str)

    with open(fileName, 'wb') as im:
        im.write(base64.decodebytes(bytes(theString.encode())))

def concatenate(list):
    length = len(list)
    iterations = math.floor(length/117)
    decrypted_message = ""

    for x in range(iterations):
        decrypted_message += list[x]
    else:
        return decrypted_message

privateKey, publicKey = loadKeys()
#print(publicKey)
#print('\n')
#print(privateKey)
#print('\n')

message = txtToString('test.txt')
image = 'megamind.png'
pdf = 'research_results_hackathon_2023.pdf'
encrypted_message = deconstructSTR(message, publicKey)
#encrypted_image = encodeIMAGE(image, publicKey)
#encrypted_pdf = encodePDF(pdf, publicKey)

print(*encrypted_message, sep='')
decryptedList = decrypt(encrypted_message, privateKey)
#decrypted_message = concatenate(decryptedList)
print(*decryptedList, sep='')
#print('')