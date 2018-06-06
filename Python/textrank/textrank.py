#!/usr/src/env python
# -*- coding: utf-8 -*-
# TextRank 博客 http://xiaosheng.me/2017/04/08/article49/
# 从PageRank转变而来，可以用来做关键字的提取。TextRank的计算公式其实跟PageRank可以认为是一样的
# 只不过就是要考虑权重的因素(算PageRank的时候就是均摊权值)
# 在TextRank构建的图中，节点是句子，权值就是两个句子的相似程度 

# 提取关键字的时候，单词作为图的节点，把权值都设成1，此时其实退化成PageRank
# 把文本拆分成单词，将这一些单词设定一个简单的滑动窗口，每个窗口内的任意两个单词之间存在一条边

# 如果是要提取关键句，一般认为所有句子都是相邻的，不需要窗口提取。相似程度的计算公式一般是重合
# 单词数量除以总单词数量

import sys
import pandas as pd
import jieba.analyse

def textrank(data, topK):
    idList, titleList, abstractList = data['id'], data['title'], data['abstract']
    ids, title, keys = [], [], []
    for i in range(len(idList)):
        text = '%s。%s' % (titleList[i], abstractList[i]) #拼接
        jieba.analyse.set_stop_words('data/stopWord.txt')
        print("\"", titleList[i], "\"", " 10 keywords - TextRank :")
        keywords = jieba.analyse.textrank(text, topK = topK, allowPOS=('n','nz','v','vd','vn','l','a','d'))
        word_split = " ".join(keywords)
        print(word_split)
        keys.append(word_split.encode("utf-8"))
        ids.append(idList[i])
        title.append(titleList[i])
    result = pd.DataFrame({"id":ids, "title":title, "key":keys}, columns=['id', 'title', 'key'])
    return result

if __name__ == "__main__":
    dataFile = 'data/sample_data.csv'
    data = pd.read_csv(dataFile)
    result = textrank(data, 10)
    result.to_csv("result/keys_textrank.csv", index=False)