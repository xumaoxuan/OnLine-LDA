# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np
import random
from DataPreProcessing import DataPreProcessing
from collections import OrderedDict
class OLDAModel(object):
    def __init__(self,K,a,b,delta,w,docs_count=1,iter_times=1000,top_words_num=10,\
                 thetafile="data/file/theta.txt",phifile="data/file/phi.txt",Bfile="data/file/B.txt",topNDocument="data/file"):

        self.thetafile = thetafile
        self.phifile = phifile
        self.Bfile = Bfile
        self.topNDocument=topNDocument

        self.K = K
        self.iter_times = iter_times
        self.top_words_num = top_words_num
        self.w = np.array(w)
        self.alpha=a
        self.b=b
        self.docs_count = 1
        self.delta=delta
        self.topNDocument


    def initialize(self):

        # p,概率向量 double类型，存储采样的临时变量
        # nw,词word在主题topic上的分布
        # nwsum,每各topic的词的总数
        # nd,每个doc中各个topic的词的总数
        # ndsum,每各doc中词的总数

        self.p = np.zeros(self.K)
        self.nw = np.zeros((self.docs_length, self.K))  # V*K
        self.nwsum = np.zeros(self.K)  # 1*K
        self.nd = np.zeros((self.docs_count, self.K))  # M*K
        self.ndsum = np.zeros(self.docs_count)  # 1*M
        self.Z = np.array(
            [[0 for y in xrange(self.docs_length)] for x in xrange(self.docs_count)])  # M*doc.size()，文档中词的主题分布  M*V

        # 随机先分配类型
        for x in xrange(self.docs_count):  # M*V  #caveat  M = 1
            self.ndsum[x] = np.sum(self.word2id.values())   # caveat only has one document
            for y in xrange(self.docs_length):
                topic = random.randint(0, self.K - 1)
                self.Z[x][y] = topic
                self.nw[y][topic] += 1  # caveat
                self.nd[x][topic] += 1
                self.nwsum[topic] += 1




        self.theta = np.array([[0.0 for y in xrange(self.K)] for x in xrange(self.docs_count)])  # M*K
        self.phi = np.array([[0.0 for y in xrange(self.docs_length)] for x in xrange(self.K)])  # K*V


    def sampling(self, i, j):   #M*V

            topic = self.Z[i][j]


            self.nw[j][topic] -= 1   #caveat   word=j

            self.nd[i][topic] -= 1
            self.nwsum[topic] -= 1
            self.ndsum[i] -= 1

            # Vbeta = self.dpre.words_count * self.beta
            # Kalpha = self.K * self.alpha
            # self.p = (self.nw[word] + self.beta) / (self.nwsum + Vbeta) * \
            #          (self.nd[i] + self.alpha) / (self.ndsum[i] + Kalpha)

            #1*k
            self.Vbeta=np.sum(self.beta,axis=1)
            Kalpha = self.K * self.alpha

            self.p = (self.nw[j] + self.beta.T[j]) / (self.nwsum + self.Vbeta) * \
                         (self.nd[i] + self.alpha) / (self.ndsum[i] + Kalpha)

            #self.phi[i] = (self.nw.T[i] + self.beta[i]) / (self.nwsum[i] + np.sum(self.beta, axis=1))


            for k in xrange(1, self.K):
                self.p[k] += self.p[k - 1]

            u = random.uniform(0, self.p[self.K - 1])
            for topic in xrange(self.K):
                if self.p[topic] > u:
                    break

            self.nw[j][topic] += 1
            self.nwsum[topic] += 1
            self.nd[i][topic] += 1
            self.ndsum[i] += 1
            return topic

    def estimation(self):

        for x in xrange(self.iter_times):
            for i in xrange(self.docs_count):   #M*V
                for j in xrange(self.docs_length):
                    topic = self.sampling(i,j)
                    self.Z[i][j] = topic

            #display current Timeslice top-N topic

        self.topNword()
        self._B()


    def topNword(self):
        self._phi()
        topN=[]
        for item in self.phi:
            temp={key:item[index] for index,key in enumerate(self.word2id.keys())}
            temp2=sorted(temp.items(),key=lambda d:d[1],reverse=True)
            #print temp2
            topN.append([temp2[i][0]for i in xrange(self.top_words_num)])
        #print topN
        self.saveTopNWord(topN)



    def _theta(self):    #M*K
        for i in xrange(self.docs_count):
            self.theta[i] = (self.nd[i] + self.alpha) / (self.ndsum[i] + self.K * self.alpha)

    def _phi(self):  #K*V
        for i in xrange(self.K):
            self.phi[i] = (self.nw.T[i] + self.beta[i]) / (self.nwsum[i] +self.beta[i])

    def _B(self): #K*V*delta
        temp=[]  #trick
        if self.t==0:
            for index,item in enumerate(self.B):
                temp.append(np.column_stack((item, self.phi[index])))
            self.B=np.array(temp)
        else:
            for index,item in enumerate(self.B):
                temp.append(np.column_stack((item[:, 1:], self.phi[index])))
            self.B = np.array(temp)



    #self.p = (self.nw[j] + self.beta.T[j]) / (self.nwsum + Vbeta) * \
    #                 (self.nd[i] + self.alpha) / (self.ndsum[i] + Kalpha)


    def saveTopNWord(self,topN):
        with open(str(self.topNDocument) + "/" + str(self.t+1) + ".txt", 'w') as f:
            for x in xrange(len(topN)):
                f.write("topic" + str(x) + " :" + "\n")
                for y in xrange(len(topN[x])):
                    f.write(topN[x][y] + '\t')
                f.write('\n')

    def save(self):

        #保存theta文章-主题分布
        with open(self.thetafile,'w') as f:
            for x in xrange(self.docs_count):
                for y in xrange(self.K):
                    f.write(str(self.theta[x][y]) + '\t')
                f.write('\n')

        #保存phi词-主题分布
        with open(self.phifile,'w') as f:
            for x in xrange(self.K):
                for y in xrange(self.docs_length):
                    f.write(str(self.phi[x][y]) + '\t')
                f.write('\n')


        #sava evolutional matrix
        with open(self.Bfile,'a') as f:
            for x in xrange(self.K):
                for y in xrange(self.docs_length):
                    f.write(str(self.B[x][y]) + '\t')
                f.write('\n')



    def augumentedB(self):
        while self.B.shape[1] < self.docs_length:
            temp = []
            for index, item in enumerate(self.B):
                temp.append(np.row_stack((item, np.zeros(self.delta + 1))))
            self.B = np.array(temp)
    def augumentedBeta(self):
        print "haha"
        print self.beta.shape
        self.beta=(np.column_stack((self.beta, np.zeros((self.beta.shape[0],self.docs_length-self.beta.shape[1])))))
        print self.beta.shape
        print self.docs_length

    def initializeBandBeta(self):
        # initialize B and beta
        if self.t == 0:
            self.beta = np.full((self.K, self.docs_length), self.b, dtype=float)  # K*V
            self.B = np.zeros((self.K, self.docs_length, self.delta), dtype=float)  # K*V*delta
        else:
            self.augumentedBeta()
            self.augumentedB()
            for index, item in enumerate(self.B):
                self.beta[index] = np.dot(item, self.w)


    def process(self,timeInterval):
        docSet = DataPreProcessing().sliceWithTime(timeInterval)

        # share the same vocabulary
        #docVector = []
        word2id = OrderedDict()
        print len(docSet)
        print "what"
        for index, doc in enumerate(docSet):
            self.t=index
            for word in doc:
                if word in word2id:
                    word2id[word]+= 1
                else:
                    word2id[word] = 1

            self.docs_length = len(word2id)
            self.word2id=word2id
            print self.docs_length
            self.initializeBandBeta()
            self.initialize()    #initialize the parameters
            self.estimation()
            print self.Vbeta


        #output
        self._theta()
        #self._phi()
        self.save()



if __name__=="__main__":

    K=5
    alpha=10
    beta=0.1
    delta=1
    timeInterval=1200
    olda=OLDAModel(K, alpha, beta, delta, [0.3, 0.7]) # assume all the elements of w vector sum to one
    olda.process(timeInterval)