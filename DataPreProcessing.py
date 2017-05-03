import numpy
import ReadBulletScreen
from collections import OrderedDict
class Document(object):
    def __init__(self):
        self.words = []
        self.length = 0

class DataPreProcessing(object):
    def __init__(self):
        self.docs_count = 0
        self.words_count = 0
        self.docs = []
        self.word2id = {}

    def sliceWithTime(self,timeInterval):
        lines,timeLength=ReadBulletScreen.ReadBulletScreen().read()
        preTime=0
        lastTime=preTime+timeInterval
        docSet=[]
        #ins=0
        for index in xrange(int(timeLength/timeInterval)):
            doc = Document();
            docSet.append(doc)
            #ins+=1
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
            #print ins


        return docSet

    def preProcessing(self,timeInterval):
        docSet=self.sliceWithTime(timeInterval)
        for doc in docSet:
            pass




if __name__=="__main__":
    print DataPreProcessing().sliceWithTime(900)



