#!/usr/src/env python
# -*- coding: utf-8 -*-
#author: Chao Gao

###########################################
# 找出赵雷歌词中高频词汇
# 拉了赵雷的三张专辑记下歌词，假装使用python进行词频的分析，这里用到了一个很强的库 jieba
# 其实这是很简单的练习，唉python毕竟已经很生疏了 或者说其实并没怎么学过
# os.listdir 返回的是指定文件夹下文件的列表
# python中list的extend方法是在列表末尾加上多个值 可与append做类比
# Counter计数器
# write result to the file
############################################
import os
from collections import Counter
import jieba  

all_words = []
for filename in os.listdir('data'):
	#print filename
	with open('data/' + filename) as f:
		lyrics = f.read()
		data = jieba.cut(lyrics)
    	all_words.extend(set(data))

count = Counter(all_words)
result = sorted(count.items(), key=lambda x: x[1], reverse=True)

res = open("res.txt", "w")
for word in result:
	res.write(word[0].encode('utf-8') + " " + str(word[1]) + '\n') 
res.close()




