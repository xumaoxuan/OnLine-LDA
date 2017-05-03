from collections import OrderedDict
word2id=OrderedDict()
words=[]
tmp=["good","hello","good","fuck","good","hello","zeze"]
items_idx=0
for item in tmp:
    if item in word2id:
        words[word2id.keys().index(item)]+=1
    else:
        word2id[item]=0;
        words.append(1)
print words
print word2id