# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np
from ReadBulletScreen import BulletScreen
from collections import OrderedDict



class DataPreProcessing(object):
    def __init__(self):
        self.docSet=[]

    def addRestComment(self):
        doc=[]
        while (len(self.lines) != 0):

                for item in self.lines[0]["text"]:
                    doc.append(item)
                self.lines.pop(0)

        self.docSet.append(doc)
        print len(doc)


    def sliceWithTime(self,timeInterval):
        self.lines,timeLength=BulletScreen().run()
        preTime=0
        lastTime=preTime+timeInterval
        for index in xrange(int(timeLength/timeInterval)):
            doc =[]
            while(len(self.lines)!=0):
                if self.lines[0]["time"] <=lastTime:
                    for item in self.lines[0]["text"]:
                        doc.append(item)
                    self.lines.pop(0)
                else:
                    preTime=lastTime
                    lastTime=preTime+timeInterval
                    self.docSet.append(doc)
                    break

            print "doc size %d" % len(doc)
        print "doc size %d" % len(self.lines)
        self.addRestComment()
        print len(self.docSet)
        #self.print_docSet(self.docSet)
        return self.docSet


    # def print_docSet(self,docSet):
    #     with open("data/tmp/data.txt", 'w') as f:
    #         for item in docSet:
    #             f.write(" ".join(item))
    #             #f.write("\n")

if __name__=="__main__":
    timeInterval=1000
    print DataPreProcessing().sliceWithTime(timeInterval)



