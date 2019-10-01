import pickle   # importing package

ff = open("cosimUser1.pkl","r") # opening file in reading mode
data = pickle.load(ff)
ff.close()                      # closing file

# for x in data:
#     for y in x:
#         if y==1:
#             print y

for i in range(925):
    for j in range(925):
        print data[i][j]        # printing data
