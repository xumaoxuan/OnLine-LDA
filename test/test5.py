import numpy as np

a=np.ones((2,2,2))
b=np.array([[ 1,2],[ 3,4]])


# t=[]
# t.append(np.column_stack((a[1],b[1])))
#
# print a

s=[]
for index,item in enumerate(a):
    s.append(np.column_stack((item,b[index])))
a=np.array(s)
print a





    #print np.column_stack((item,b[index]))

c=np.ones((2,3,2))

#print c[1][2]