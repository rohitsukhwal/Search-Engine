import xml.sax
import cgi
import csv
from nltk.corpus import stopwords
from stemming.porter2 import stem
import nltk
import re
import collections
import sys


cachedStopWords = stopwords.words("english")
'''
def write_to_file(filename,od):
        wf=open(filename,'w')
        for i in od:
            strin=str(i)+" -> "
            for j in od[i]:
                strin+="id = " 
                strin+=str(j[0])
                strin+=",fc = " 
                strin+= str(j[1])
                strin+=";"
            strin+='\n'
            wf.write(strin)
        wf.close()

'''

class WikiContentHandler(xml.sax.ContentHandler):
     def __init__(self):
             xml.sax.ContentHandler.__init__(self)
             self._tflag=0
             self._iflag=0
             self._xflag=0
             self._idcount=0
             self.words=[]
             self.invert={}
             self.gc=0
     def startElement(self, name, attrs):
        if name == "title":
                self._title=""
                self._tflag=1
        elif name == "text":
                self._text=""
                self._xflag=1
        elif name == "id":
            if self._idcount%3==0:
                    self._Id=""
                    self._iflag=1
            self._idcount+=1
            


     def characters(self,content):
         if(self._tflag==1):
             self._title+=content.encode('ascii', 'ignore').lower()
         elif(self._iflag==1):
             self._Id+=content.encode('ascii', 'ignore')
         elif(self._xflag==1):
             self._text+=content.encode('ascii', 'ignore').lower()
                    

     def endElement(self, name):
        if  name == "title":
                self._tflag=0
          #      print self._title
        elif name == "text":
                 if sys.getsizeof(self.invert)>1000000:
                      odinv = collections.OrderedDict(sorted (self.invert.items(), key=lambda t: t[0])) 
                      filename="index/f"+str(self.gc)
                      wf=open(str(filename),'w')
                      for i in odinv:
                        strin=str(i)+" -> "
                        for j in odinv[i]:
                            strin+="id = " 
                            strin+=str(j)
                            strin+=";"
                        strin+='\n'
                        wf.write(strin)
                      wf.close()
                      self.gc=self.gc+1
                      self.invert={}
                 
                 self._xflag= 0
                 #self._text=nltk.word_tokenize(self._text)
                 tok = ([stem(word) for word in nltk.word_tokenize(self._text) if word not in cachedStopWords])
                 for i in tok:
                     if re.match('\w+$',i) and not(re.match('\d+$',i)):
                         self.words.append(i)
                 sett=set(self.words)        
                 count={}
                 for i in self.words:
                     if i not in count:
                             count[i]=1
                     else:
                             count[i]+=1

                 for i in sett:
                     strin =self._Id + ",freq = "+str(count[i])
                     if i not in self.invert and i is not 'infobox' :
                         self.invert[i]=[strin]
                     elif i in self.invert:   
                         self.invert[i].append(strin)
                 self.words=[]        
                 
                     
                 
                 #for i in self.invert:
                 #   print i + " -> " + self.invert[i][0]+ "," + str(self.invert[i][1])
                 #print len(self.invert)
                 #print self._text
                 #for i in self.words:
                    # print i + " ",
        elif name == "id":
             if self._idcount%3==1:
                     self._iflag= 0
         #            print self._Id
        
        elif name == "file":
            if self.invert:
                      odinv = collections.OrderedDict(sorted (self.invert.items(), key=lambda t: t[0]))
                      filename="index/f"+str(self.gc)
                      wf=open(str(filename),'w')
                      for i in odinv:
                        strin=str(i)+" -> "
                        for j in odinv[i]:
                            strin+="id = " 
                            strin+=str(j)
                            strin+=";"
                        strin+='\n'
                        wf.write(strin)
                      wf.close()
                      self.gc=self.gc+1
                      self.invert={}



'''        elif name=="file": 
            if self.invert:
                odinv = collections.OrderedDict(self.invert)
                write_to_file("index/f"+str(self.gc),odinv)
                self.gc=self.gc+1
                self.invert={}
'''

def main(fname):
    source=open(fname)
    xml.sax.parse(source, WikiContentHandler())
'''    parser = xml.sax.make_parser()
    parser.setContentHandler(WikiContentHandler())             
    parser.parse(open(fname,"r"))
'''

if __name__ == "__main__":
    main(sys.argv[1])

