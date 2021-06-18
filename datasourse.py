import os
import pymongo
from hashlib import sha256
from datetime import datetime
difficulty = 2

def call():
    print('success')


client = pymongo.MongoClient("mongodb+srv://hariharan:cricket20155@cluster0.xlfgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
client2 = pymongo.MongoClient("mongodb+srv://hariharan:cricket20155@madhu007.d9egy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
client3 = pymongo.MongoClient("mongodb+srv://hariharan:cricket20155@isproject.feave.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client['user_details']
collection = db['users']
collection1 = db['data']

db2 = client2['user_details']
collection2 = db2['data']

db3 = client3['user_details']
collection3 = db3['data']


def getHash(user):

    res = collection.find({'uname' : user})
    te = []
    for result in res:
        te.append(result['words'])

    return te[0]

def addUserDetails(fullname,uname,passw,str):
    collection.insert_one({'name' : fullname , 'uname' : uname , 'pass' : passw , 'words' : str})


def checkLogin(user , passw):

    res = collection.find({'uname' : user , 'pass' : passw})

    if res.count()  == 1 :
        return True

    return False

def getSecureWords(user):

    res = collection.find({'uname' : user})
    temp = []
    for result in res :
        temp.append(result['words'])

    temp = temp[0].split(" ")
    print('hlo'+str(len(temp)))
    return temp


def addData(fromm,to,enc_msg,nonce,tag,prev_hash):
    res = collection1.estimated_document_count()
    collection1.insert_one({'_id' : res , 'from' : fromm , 'to' : to , 'msg' : enc_msg , 'nonce' : nonce ,
                            'tag' : tag , 'time' : datetime.now().strftime("%H:%M:%S") , 'prev_hash' : prev_hash})

    collection2.insert_one({'_id': res, 'from': fromm, 'to': to, 'msg': enc_msg, 'nonce': nonce,
                            'tag': tag, 'time': datetime.now().strftime("%H:%M:%S"), 'prev_hash': prev_hash})

    collection3.insert_one({'_id': res, 'from': fromm, 'to': to, 'msg': enc_msg, 'nonce': nonce,
                            'tag': tag, 'time': datetime.now().strftime("%H:%M:%S"), 'prev_hash': prev_hash})


def performHash(param, param1, param2, param3, param4, param5, param6, param7):
    res = param+param1+param2+param3+param4+param5+param6+param7
    return sha256(res.encode()).hexdigest()


def getHashKey():
    res = collection1.estimated_document_count()
    res = res-1

    docs = collection1.find({'_id' : res})
    temp = []
    print(res , len(temp))
    for doc in docs:
        temp.append(doc)

    temp = temp[0]
    res = performHash(str(temp['_id']) , temp['from'] ,temp['to'] ,temp['msg'].hex() ,temp['nonce'].hex() , temp['tag'].hex() , temp['time'] , temp['prev_hash'])
    return res

def getData(user):
    res = collection1.find({"to" : user})

    temp = []

    for result in res:
        temp.append(result)

    return temp

# res = collection1.find({'from' : 'harish00201'})
#
# temp = []
#
# for result in res:
#     temp.append(result)
#
# req = temp[0]
#
# res = aes.decrypt_AES_GCM((req['msg'],req['nonce'],req['tag']),req['from'])
# print(res)

#e44aae43a1c8714c9de70e49518944f00348ecd5224b1625efcf87b825a4419f