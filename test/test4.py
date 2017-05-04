import numpy as np
K=2
V=2
delta=np.array([1,2])


beta=np.full((K,V),2)
B=np.ones((K,V,2))
print beta.shape
#print beta
for index,item in enumerate(B):
     beta[index]=np.dot(item,delta.reshape(2,1)).T

print beta
print "haha"
print beta[0]

