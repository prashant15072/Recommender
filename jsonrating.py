import json
import pickle
import numpy as np

ff = open("mapping.pkl","r")
data = pickle.load(ff)
ff.close()

def rat(rating):
    if rating==-1:
        return 1
    elif rating==0:
        return 2
    else:
        return 3

movieIdtoNum = data[0]
movieNumtoId = data[1]
usersIdtoNum = data[2]
usersNumtoId = data[3]

for i in range(1,6):
    array = []
    name = "fold" + str(i) + "_train.json"
    nam2 = "train" + str(i) + ".dat"
    json_data = open(name)
    data = json.load(json_data)
    st = ""
    for x in data:
        username = str(x['_id'])
        userNum = usersIdtoNum[username]
        y = x['rated']
        for z in y:
            if str(z)!="submit":
                movieTag = str(z)
                movieNum = movieIdtoNum[movieTag]
                rating =  int(y[z][0])
                array.append((userNum,movieNum,rat(rating)))
                st = st + str(userNum) + "\t" + str(movieNum) + "\t" + str(rating) + "\n"
    nam = "array" + str(i) + "_train.pkl"
    filehandler = open(nam, "w")
    pickle.dump(array, filehandler)
    filehandler.close()
    filehandler2 = open(nam2, "w")
    filehandler2.write(st)
    filehandler2.close()


for i in range(1,6):
    array = []
    name = "fold" + str(i) + "_test.json"
    nam2 = "test" + str(i) + ".dat"
    json_data = open(name)
    data = json.load(json_data)
    st=""
    for x in data:
        username = str(x['_id'])
        userNum = usersIdtoNum[username]
        y = x['rated']
        for z in y:
            if str(z)!="submit":
                movieTag = str(z)
                movieNum = movieIdtoNum[movieTag]
                rating =  int(y[z][0])
                array.append((userNum,movieNum,rat(rating)))
                st = st + str(userNum) + "\t" + str(movieNum) + "\t" + str(rating) + "\n"
    nam = "array" + str(i) + "_test.pkl"
    filehandler = open(nam, "w")
    pickle.dump(array, filehandler)
    filehandler.close()
    filehandler2 = open(nam2, "w")
    filehandler2.write(st)
    filehandler2.close()
