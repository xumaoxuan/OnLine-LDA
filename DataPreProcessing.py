# -*- coding: utf-8 -*-
import numpy
from ReadBulletScreen import BulletScreen
from collections import OrderedDict
#from OLDATest import OLDAModel
class Document(object):
    def __init__(self):
        self.words = []
        self.length = 0

class DataPreProcessing(object):
    def __init__(self):
        self.docs_count = 0
        self.words_count = 0
        self.docs = []


    def sliceWithTime(self,timeInterval):
        lines,timeLength=BulletScreen().read()
        preTime=0
        lastTime=preTime+timeInterval
        docSet=[]
        for index in xrange(int(timeLength/timeInterval)):
            doc = Document();
            docSet.append(doc)
            while(len(lines)!=0):
                if lines[0]["time"] <=lastTime:
                    doc.words.append(item for item in lines[0]["text"])
                    lines.pop(0)
                else:
                    preTime=lastTime
                    lastTime=preTime+timeInterval
                    break
            doc.length=len(doc.words)
            print doc.length
        return docSet



    def preProcessing(self,timeInterval):
        docSet=self.sliceWithTime(timeInterval)
        self.docs_count = len(docSet)

        #share the same vocabulary
        docVector = []
        word2id = OrderedDict()
        for index,doc in enumerate(docSet):
            for word in doc.words:
                if word in word2id:
                    docVector[word2id.keys().index(word)]+=1
                else:
                    docVector.append(1)
                    word2id[word]=0
            OLDAModel([docVector],[word2id],K,beta,alpha,delta,[0.1,0.1],index)
            #self.docs.append({"docVector":docVector,"word2id":word2id,"words_count":doc.length})



        #instance=OLDAModel(DataPreProcessing().sliceWithTime(300))



if __name__=="__main__":
     print DataPreProcessing().preProcessing(300)



