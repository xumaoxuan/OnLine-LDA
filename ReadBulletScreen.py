# -*- coding: utf-8 -*-
import numpy
import re
import jieba.posseg as pseg
import jieba.analyse
import uniout


class ReadBulletScreen(object):
    def __init__(self):
        self.lines=[]
        self.timelength=0

    def read(self):
        #f = open("data/515862.txt", "r")
        #self.timelength = 18377
        #f = open("data/551683.txt", "r")
        #self.timelength = 6122
        f = open("data/601124.txt", "r")
        self.timelength = 9238
        jieba.analyse.set_stop_words("stopWords.txt")
        lines = f.readlines()
        tempLine=[]

        for line in lines:
            pattern=re.compile("^<d p=\"(.+)\">(.+)</d>")
            m=pattern.match(line)
            if m:
                tempLine.append({"time":int(float(m.group(1).split(',')[0])), \
                                   "text":[word  for word,flag in pseg.cut(m.group(2)) if flag in ["n","ns","v","vn","nr","vd","ng","i"]]
                                })

        for index,item in enumerate(tempLine):
            if len(item["text"])==0:
                del(tempLine[index])

        self.lines=sorted(tempLine, key= lambda e:(e.__getitem__('time')))

        return self.lines,self.timelength



if __name__=="__main__":
     print ReadBulletScreen().read()



