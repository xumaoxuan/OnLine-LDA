# -*- coding: utf-8 -*-
import numpy as np
import random
from DataPreProcessing import DataPreProcessing
class OLDAModel(object):
    def __init__(self,docVector,word2id,K,b,a,delta,w,t,B,docs_count=1,iter_times=100,top_words_num=10,\
                 thetafile="data/file/theta.txt",phifile="data/file/phifile",Bfile="data/file/B.txt"):


        #
        # 模型参数
        # 聚类个数K，迭代次数iter_times,每个类特征词个数top_words_num,超参数α（alpha） β(beta)
        #
        self.docVector = docVector
        self.docs_count = docs_count
        self.docs_length = len(docVector)

        self.K = K

        self.iter_times = iter_times
        self.top_words_num = top_words_num
        self.t=t
        self.w=np.array(w)  #delta*1


        self.thetafile = thetafile
        self.phifile = phifile
        self.Bfile=Bfile
        #self.topNfile = topNfile
        #self.tassginfile = tassginfile
        #self.paramfile = paramfile
        self.B=B


        #B
        self.beta=0
        if self.t==0:
            self.beta = np.full((self.K,self.docs_length), b,dtype=float)   #K*V
            #self.B=np.zeros((self.K,self.docs_length,delta),dtype=float)    #K*V*delta
        else:
            self.beta = np.full((self.K, self.docs_length), b, dtype=float)
            for index,item in enumerate(self.B):
                #print item.shape
                self.beta[index] = np.dot(item, self.w)
        self.alpha = a

        # p,概率向量 double类型，存储采样的临时变量
        # nw,词word在主题topic上的分布
        # nwsum,每各topic的词的总数
        # nd,每个doc中各个topic的词的总数
        # ndsum,每各doc中词的总数


        self.p = np.zeros(self.K)
        self.nw = np.zeros((self.docs_length, self.K))        # V*K
        self.nwsum = np.zeros(self.K)   # 1*K
        self.nd = np.zeros((self.docs_count,self.K))    #M*K
        self.ndsum = np.zeros(self.docs_count)    #1*M
        self.Z = np.array(
            [[0 for y in xrange(self.docs_length)] for x in xrange(self.docs_count)])  # M*doc.size()，文档中词的主题分布  M*V

        # 随机先分配类型
        for x in xrange(len(self.Z)):   #M*V
            self.ndsum[x] = np.sum(docVector[x])
            for y in xrange(self.docs_length):

                topic = random.randint(0, self.K - 1)
                self.Z[x][y] = topic
                self.nw[y][topic] += 1  #caveat
                self.nd[x][topic] += 1
                self.nwsum[topic] += 1

        self.theta = np.array([[0.0 for y in xrange(self.K)] for x in xrange(self.docs_count)])  #M*K
        self.phi = np.array([[0.0 for y in xrange(self.docs_length)] for x in xrange(self.K)])   #K*V



    def sampling(self, i, j):   #M*V

            topic = self.Z[i][j]
            #word = self.dpre.docs[i].words[j]
            #self.nw[word][topic] -= 1

            self.nw[j][topic] -= 1   #caveat   word=j

            self.nd[i][topic] -= 1
            self.nwsum[topic] -= 1
            self.ndsum[i] -= 1

            # Vbeta = self.dpre.words_count * self.beta
            # Kalpha = self.K * self.alpha
            # self.p = (self.nw[word] + self.beta) / (self.nwsum + Vbeta) * \
            #          (self.nd[i] + self.alpha) / (self.ndsum[i] + Kalpha)

            #1*k
            Vbeta=np.sum(self.beta,axis=1)
            Kalpha = self.K * self.alpha

            self.p = (self.nw[j] + self.beta.T[j]) / (self.nwsum + Vbeta) * \
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

        self._theta()
        self._phi()
        self._B()
        self.save()
        return self.B


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
        with open(self.Bfile,'a+') as f:
            for x in xrange(self.K):
                for y in xrange(self.docs_length):
                    f.write(str(self.B[x][y]) + '\t')
                f.write('\n')


    #def process(self):



