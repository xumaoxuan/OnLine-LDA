#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import jieba.posseg as pseg
import jieba.analyse
import random
from  numpy  import *
import uniout
try:
    import cPickle as pickle
except ImportError:
    import pickle
class dataMiningHousework:

    def __init__(self):

        #self.category = {"Law": 0, "Art": 1, "Sports": 2, "Military": 3,"Game":4,"Computer":5,"Education": 6, "Stock": 7, "House": 8, "History": 9}
        self.category={}

        self.categoryTemp=0;#用来区分类别的  不同的类别对应不同的数字
        self.stopWords={}
        for line in open("stopWords.txt").readlines():
            self.stopWords[line.strip()] = 0

    def createVocabList(self,dataSet):
        vocabSet = set([])  # create empty set
        for document in dataSet:
            vocabSet = vocabSet | set(document)  # union of the two sets
        return list(vocabSet)

    def trainNB0(self,trainMatrix,trainCategory):
        numTrainDocs
        #numTrainDocs = len(trainMatrix)
        numWords = len(trainMatrix[0])
        print "numWords:"+str(numWords)
        #print len(self.category)
        pAbusiveList=[0]*len(self.category)
        #print pAbusiveList
        #print trainCategory
        for i in trainCategory:
            pAbusiveList[i]+=1

        pAbusiveList=array(pAbusiveList)/float(numTrainDocs)  #对所有类比的都计算其概率
        #print pAbusiveList
        pNumTemp = []
        temp = []
        for i in range(len(self.category)):  # p0Denom = 2.0; p1Denom = 2.0;
            temp.append(2.0)
            temp2 = ones(numWords)
            pNumTemp.append(temp2)
        pDenom = array(temp)    #一维
        pNum = array(pNumTemp)  #二维

        #print pDenom
        #print pNum

        for i in range(numTrainDocs):
            pNum[trainCategory[i]]+=trainMatrix[i]
            pDenom[trainCategory[i]]+=sum(trainMatrix[i])

        pVect=[]
        for i in range(len(self.category)):
            pTemp = log(pNum[i]/pDenom[i])
            pVect.append(pTemp)

        return array(pVect),pAbusiveList



    def bagOfWords2VecMN(self,vocabList,inputSet):
        returnVec = [0]*len(vocabList)
        for word in inputSet:
            if word in vocabList:
                returnVec[vocabList.index(word)] += 1
        return returnVec

    def textParse(self,parseList): #去除标点符号
        #input is big string, #output is word list
        list=[]


        return parseList

    def classifyNB(self,vec2Classify,pVect,pAbusiveList):
        max=-9999999999999 #arbitsize
        index=-1
        for i in range(len(self.category)):
            p=sum(vec2Classify*pVect[i])+log(pAbusiveList[i])
            #print p
            if p>max:
                max=p
                index=i
        return index

    def spamTest(self,trainDir):
        currentdir=trainDir

        dirList = os.listdir(currentdir)
        docList = [];
        classList = [];

        totalFile = 0;
        jieba.analyse.set_stop_words("stopWords.txt")
        for dir in dirList:
            if dir == ".DS_Store":
                continue
            for file in os.listdir(currentdir + "/" + dir):
                #b = re.match("^[a-zA-Z0-9]*-([a-zA-Z]*)([0-9]*)\.txt$", file)
                #if b:
                    if file == ".DS_Store":
                        continue

                    #leibie=dir.split(".")[0]
                    if (dir not in self.category):
                        self.category[dir]=self.categoryTemp
                        self.categoryTemp+=1

                    print currentdir + "/" + dir + "/" + file
                    try:
                        #wordList = self.textParse(pseg.lcut(open(currentdir + "/" + dir + "/" + file).read().decode("gbk").encode("utf-8")))
                        #wordList=self.textParse(jieba.analyse.extract_tags(open(currentdir + "/" + dir + "/" + file).read().decode("gbk").encode("utf-8"),topK=20))
                        #wordList = jieba.analyse.textrank(open(currentdir + "/" + dir + "/" + file).read().decode("gbk").encode("utf-8"), topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
                        wordList = jieba.analyse.textrank(open(currentdir + "/" + dir + "/" + file).read(), topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
                        print wordList
                        totalFile += 1
                        docList.append(wordList)
                        classList.append(self.category[dir])
                    except Exception,e:
                            print Exception, ":", e

        vocabList = self.createVocabList(docList)
        self.storeVocabList(vocabList)
        return



        trainingSet = range(totalFile)  # 按照索引来计算
        print totalFile
        testSet = []                   # 按照索引来计算
        # for i in range(totalFile/10):  # 按照索引来计算
        #     randIndex = int(random.uniform(0, len(trainingSet)))
        #     testSet.append(trainingSet[randIndex])
        #     del (trainingSet[randIndex])

        trainMat = []   #向量化的所有的训练集
        trainClasses = []  #训练集的类别
        print self.category

        for docIndex in trainingSet:  # train the classifier (get probs) trainNB0
            print docIndex
            trainMat.append(self.bagOfWords2VecMN(vocabList, docList[docIndex]))
            trainClasses.append(classList[docIndex])
        #print trainClasses
        pVect,pAbusiveList = self.trainNB0(array(trainMat), array(trainClasses))
        self.storeTrainSet(pVect,pAbusiveList,self.category)
        print "trainSet finished"
        # errorCount = 0
        # print testSet
        # for docIndex in testSet:  # classify the remaining items
        #     wordVector = self.bagOfWords2VecMN(vocabList, docList[docIndex])
        #     s=self.classifyNB(array(wordVector), pVect, pAbusiveList)
        #     #print s
        #     if s != classList[docIndex]:
        #         errorCount += 1
        #         #print "classification error", docList[docIndex]
        # print 'the error rate is: ', float(errorCount*100)/len(testSet)


    def storeTrainSet(self, pVect,pAbusiveList,category):

        # fw = open("vocabList_trainSet", 'wb')
        # pickle.dump(vocabList, fw)
        # fw.close()

        fw2=open("pVect_trainSet","wb")
        pickle.dump(pVect, fw2)
        fw2.close()

        fw3 = open("pAbusiveList_trainSet", "wb")
        pickle.dump(pAbusiveList, fw3)
        fw3.close()

        fw4 = open("category_trainSet", "wb")
        pickle.dump(category, fw4)
        fw4.close()

    def storeVocabList(self,vocabList):
        fw = open("vocabList_trainSet", 'wb')
        pickle.dump(vocabList, fw)
        fw.close()




if __name__=='__main__':
    trainDir="/Users/yinfeng/PycharmProjects/612/MachineLearning/dataMiningHomework/test/answer"
    test=dataMiningHousework()
    test.spamTest(trainDir)