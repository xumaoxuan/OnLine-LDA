# -*- coding: utf-8 -*-
import numpy as np
from ReadBulletScreen import BulletScreen
from collections import OrderedDict


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
            doc =[]
            docSet.append(doc)
            while(len(lines)!=0):
                if lines[0]["time"] <=lastTime:
                    for item in lines[0]["text"]:
                        doc.append(item)
                    lines.pop(0)
                else:
                    preTime=lastTime
                    lastTime=preTime+timeInterval
                    break
            print len(doc)
        #print "End"
        #print docSet[0]
        #print len(docSet)
        return docSet

    def preProcessing(self,timeInterval,K,alpha,beta,delta):
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
            # if index==0:  #initialize
            #     B = np.zeros((K,len(docVector), delta), dtype=float)
            #
            # #These words are assumed to have 0 count in φ for all topics in previous streams.
            # while B.shape[1]<len(docVector):
            #     temp=[]
            #     for index,item in enumerate(B):
            #         temp.append(np.row_stack((item,np.zeros(delta+1))))
            #     B=np.array(temp)
            #
            # olda=OLDAModel(docVector,word2id,K,beta,alpha,delta,[0.3,0.7],index,B)   #assume all the elements of w vector sum to one
            # B=olda.estimation()

    def testPrecessing(self,timeInterval):
        docSet = self.sliceWithTime(timeInterval)
        docVector = []
        word2id = OrderedDict()

        for index, doc in enumerate(docSet):
            for word in doc:
                #print word
                if word in word2id:
                    docVector[word2id.keys().index(word)] += 1
                else:
                    docVector.append(1)
                    word2id[word] = 0

        print word2id.keys()
        print len(word2id.keys())
        print docVector
        print len(docVector)


if __name__=="__main__":
    timeInterval=1000
    #K=10
    #alpha=1
    #beta=0.1
    #delta=1
    #DataPreProcessing().preProcessing(1000,K,alpha,beta,delta)
    DataPreProcessing().testPrecessing(timeInterval)



