import numpy as np
# a=np.array([[1,1],[1,1],[1,1]])
# print a.transpose()
# print a.shape
# b=np.array([1,2])
# print np.dot(a,b.reshape(2,1))
# a = np.array([[1, 2, 3]])
# print a.shape
# print np.dot(a.T,a)
# a=np.ones((3,2,1))
# #print a[2].shape
# for item in a:
#     #print item
#     print item.shape
a = np.array([1, 2, 3])
b=a.reshape(3,1)
print np.dot(b,b.T)