import pickle

fnarray = []
fnset = set()
dict = {}

for x in range(1,6):
    nam = "array" + str(x) + "_train.pkl"
    filo = open(nam,"r")
    array = pickle.load(filo)
    filo.close()
    for y in array:
        usr = y[0]
        itm = y[1]
        rt = y[2]
        if usr in dict:
            dict[usr].add(itm)
        else:
            ss = set()
            ss.add(itm)
            dict[usr] = ss
        st = (usr,itm)
        if not st in fnset:
            fnset.add(st)
            fnarray.append((usr,itm,rt))

for x in range(1,6):
    nam = "array" + str(x) + "_test.pkl"
    filo = open(nam,"r")
    array = pickle.load(filo)
    filo.close()
    for y in array:
        usr = y[0]
        itm = y[1]
        rt = y[2]
        if usr in dict:
            dict[usr].add(itm)
        else:
            ss = set()
            ss.add(itm)
            dict[usr] = ss
        st = (usr,itm)
        if not st in fnset:
            fnset.add(st)
            fnarray.append((usr,itm,rt))


for i in range(1,924):
    if i not in dict:
        fnarray.append((i, 146, 3))
        fnarray.append((i, 113, 3))
        fnarray.append((i, 326, 3))
    elif len(dict[i])==1:
        if not (i,146) in fnset:
            fnarray.append((i, 146, 3))
        if not (i,113) in fnset:
            fnarray.append((i, 113, 3))
        if not (i,326) in fnset:
            fnarray.append((i, 326, 3))

# dico = {}
# for xxx in fnarray:
#     u = xxx[0]
#     i = xxx[1]
#     r = xxx[2]
#     if u in dico:
#         dico[u].add(i)
#     else:
#         ss = set()
#         ss.add(i)
#         dico[u] = ss
#
# for i in range(1,924):
#     if i not in dico or len(dico[i])==1:
#         print "error!!!!"

# malign = set()
# for x in dict:
#     if len(dict[x])<=1:
#         malign.add(x)

fnarray.sort(key=lambda x: x[0])

st = ""
pt=0
for x in fnarray:
    st = st + str(pt) + "\t" + str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]) + "\n"
    pt+=1

fl = open("finalDataset.txt","w")
fl.write(st)
fl.close()