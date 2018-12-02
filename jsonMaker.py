import csv
import pickle

x = open("movies.csv")
y = open("users.csv")

movieIdtoNum = {}
movieNumtoId = {}
with x as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(readCSV):
        if i!=0:
            movieIdtoNum[row[0]] = i
            movieNumtoId[i] = row[0]

usersIdtoNum = {}
usersNumtoId = {}
with y as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(readCSV):
        if i!=0:
            usersIdtoNum[row[0]] = i
            usersNumtoId[i] = row[0]

data = (movieIdtoNum,movieNumtoId,usersIdtoNum,usersNumtoId)
ff = open("mapping.pkl","w")
pickle.dump(data,ff)
ff.close()