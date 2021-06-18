import pymongo
from bson.json_util import dumps
import threading
########################## client1 ##################################hari

client1 = pymongo.MongoClient("mongodb+srv://hariharan:cricket20155@cluster0.xlfgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

change_stream1 = client1['user_details'].watch([{
    '$match' : {
        'operationType' : { '$in' : ['update']}
    }
}])

def trial1():
    for change in change_stream1:
        call(0,change["documentKey"]["_id"])

th1 = threading.Thread(target=trial1)
th1.start()



############################################# client2 ##############################################madhu

client2 = pymongo.MongoClient("mongodb+srv://hariharan:cricket20155@madhu007.d9egy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

change_stream2 = client2['user_details'].watch([{
    '$match' : {
        'operationType' : { '$in' : ['update']}
    }
}])

def trial2():
    for change in change_stream2:
        call(1,change["documentKey"]["_id"])

th2 = threading.Thread(target=trial2)
th2.start()




####################################### client3 ######################################bharath


client3 = pymongo.MongoClient("mongodb+srv://hariharan:cricket20155@isproject.feave.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

change_stream3 = client3['user_details'].watch([{
    '$match' : {
        'operationType' : { '$in' : ['update']}
    }
}])


def trial3():
    for change in change_stream3:
        call(2,change["documentKey"]["_id"])

th3 = threading.Thread(target=trial3)
th3.start()

dict = {0 : client1 , 1 : client2 , 2 : client3}


def call(client , id):
    c_client = (client+1)%3

    db_c = dict[c_client]['user_details']
    collection_c = db_c['data']

    res_c = collection_c.find({'_id' : id})

    temp_c = []

    for result in res_c :
        temp_c.append(result)

    temp_c = temp_c[0]

    db = dict[client]['user_details']
    collection = db['data']

    res = collection.find({'_id': id})

    temp = []

    for result in res:
        temp.append(result)

    temp = temp[0]

    if temp_c['from'] != temp['from'] :
        fil = {'_id' : id}
        nv = { "$set" : {'from' : temp_c['from']}}
        collection.update_one(fil , nv)
    elif temp_c['to'] != temp['to'] :
        fil = {'_id' : id}
        nv = { "$set" : {'to' : temp_c['to']}}
        collection.update_one(fil , nv)
    elif temp_c['msg'] != temp['msg'] :
        fil = {'_id' : id}
        nv = { "$set" : {'msg' : temp_c['msg']}}
        collection.update_one(fil , nv)
    elif temp_c['nonce'] != temp['nonce'] :
        fil = {'_id' : id}
        nv = { "$set" : {'nonce' : temp_c['nonce']}}
        collection.update_one(fil , nv)
    elif temp_c['tag'] != temp['tag'] :
        fil = {'_id' : id}
        nv = { "$set" : {'tag' : temp_c['tag']}}
        collection.update_one(fil , nv)
    elif temp_c['time'] != temp['time'] :
        fil = {'_id' : id}
        nv = { "$set" : {'time' : temp_c['time']}}
        collection.update_one(fil , nv)
    elif temp_c['prev_hash'] != temp['prev_hash'] :
        fil = {'_id' : id}
        nv = { "$set" : {'prev_hash' : temp_c['prev_hash']}}
        collection.update_one(fil , nv)


