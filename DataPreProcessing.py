# -*- coding: utf-8 -*-
import numpy as np
from ReadBulletScreen import BulletScreen
from collections import OrderedDict



class DataPreProcessing(object):
    def __init__(self):
        pass


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

        return docSet


    # def testPrecessing(self,timeInterval):
    #     docSet = self.sliceWithTime(timeInterval)
    #     docVector = []
    #     word2id = OrderedDict()
    #
    #     for index, doc in enumerate(docSet):
    #         for word in doc:
    #
    #             if word in word2id:
    #                 docVector[word2id.keys().index(word)] += 1
    #             else:
    #                 docVector.append(1)
    #                 word2id[word] = 0
    #         print word2id.keys()
    #         print docVector
    #         print len(docVector)



if __name__=="__main__":
    timeInterval=1000
    print DataPreProcessing().sliceWithTime(timeInterval)



