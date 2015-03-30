import os,sys, heapq
from itertools import imap
from operator import itemgetter

def criteria(line):
    return line.split("=")[0]

print os.path.abspath("Index/")
files = [f for f in os.listdir(os.path.abspath("Index")) if os.path.isfile(os.path.join(os.path.abspath("Index"),f))]
files.sort()
#f=open(os.path.abspath("Index/")+"temp",'w')
#f.write("\n")
#f.close()
print os.listdir(os.path.abspath("Index"))
print files
for i in range(1,len(files)):
    f1=open("Index/"+files[0])
    f2=open("Index/"+files[i])
    sources=[f1,f2]
    dest=open(os.path.abspath("Index")+"/index",'w')
    print os.path.abspath("Index")+"/index"
    decorated = [((criteria(line), line) for line in f) for f in sources]
    merged = heapq.merge(*decorated)
    undecorated = imap(itemgetter(-1), merged)
    dest.writelines(undecorated)
    f1.close()
    f2.close()
    dest.close()
    f=open("Index/"+files[0],'w')
    f1=open(os.path.abspath("Index")+"/index")
    f.write(f1.read())
    f.close()
    f1.close()

