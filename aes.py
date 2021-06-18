from Crypto.Cipher import AES
import scrypt, os, binascii
import hashlib
import datasourse

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def aes(user):
    hash_string = datasourse.getHash(user)
    sha_signature = encrypt_string(hash_string)[0:32]
    return sha_signature

def encrypt_AES_GCM(msg, user):
    hash = aes(user).encode()
    aesCipher = AES.new(hash, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg.encode())
    return ciphertext, aesCipher.nonce, authTag

def decrypt_AES_GCM(encryptedMsg, user):
    hash = aes(user).encode()
    (ciphertext, nonce, authTag) = encryptedMsg
    aesCipher = AES.new(hash, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

# hash = aes('harish00201')
# print("Encryption key:", len(hash[0:32]))
#
# msg = 'Hello how r u'
# encryptedMsg = encrypt_AES_GCM(msg, 'harish00201')
# print("EncryptedMsg:", {
#     'ciphertext': str(binascii.hexlify(encryptedMsg[0]))[2:-1],
#     'aesIV': binascii.hexlify(encryptedMsg[1]),
#     'authTag': binascii.hexlify(encryptedMsg[2])
# })
#
# decryptedMsg = decrypt_AES_GCM(encryptedMsg, 'harish00201')
# print("DecryptedMsg:", str(decryptedMsg))
#
# str="b'06f8f496633b86f91b41e352d0'"
#
#
# print(encryptedMsg[0].hex())
# print(binascii.hexlify(encryptedMsg[0]).decode('utf-8').encode('utf-8'))
# print(binascii.hexlify(encryptedMsg[0]).decode())


# import pymongo
# client = pymongo.MongoClient("mongodb+srv://hariharan:cricket20155@cluster0.xlfgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = client['user_details']
# collection1 = db['data']
# res = collection1.find({'from' : 'harish00201'})
#
# temp = []
#
# for result in res:
#     temp.append(result)
#
# req = temp[0]
#
# res = decrypt_AES_GCM((req['msg'],req['nonce'],req['tag']),req['from'])
# print(res)
# print(req['msg'],req['nonce'],req['tag'])
