import pickle

ff = open("cosimUser1.pkl","r")
data = pickle.load(ff)
ff.close()

# for x in data:
#     for y in x:
#         if y==1:
#             print y

for i in range(925):
    for j in range(925):
        print data[i][j]