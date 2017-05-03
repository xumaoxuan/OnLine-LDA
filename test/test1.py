# -*- coding: utf-8 -*-
import jieba.posseg as pseg
words = pseg.cut("这是什么啊")
for word, flag in words:
  print('%s %s' % (word, flag))