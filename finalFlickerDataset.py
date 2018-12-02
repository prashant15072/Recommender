filo = open("test1.dat","r")
xx = filo.readlines()
filo.close()

fill = open("train1.dat","r")
xxx = fill.readlines()
fill.close()


str = ""

for x in xx:
    str = str + x + "\n"

for x in xxx:
    str = str + x + "\n"

filllo = open("finalDataset.txt","w")
filllo.write(str)
filllo.close()
