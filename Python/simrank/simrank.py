#!/usr/src/env python
# -*- coding: utf-8 -*-
# SimRank 相似度度量 假如a和b分别与对象c和d有关联，如果c和d是相似的，则a和b也是相似的

# 这是一个二分图的例子 用户和电影 给所有用户对和电影对分别进行相似度度量
# 如果两用户选择的电影比较类似，则这两个用户也比较类似， 反之亦然
# S(A,B) = C / dout(A) / dout(B) * (sum(S(A_in, B_in)))

import numpy
from numpy import matrix

with open("data/sample.txt", "r") as logf:
    logs = [log.strip() for log in logf.readlines()]

logs_tuple = [ tuple(log.split(",")) for log in logs ]
queries = list(set([log[0] for log in logs_tuple]))
ads = list(set([log[1] for log in logs_tuple]))

graph = numpy.matrix(numpy.zeros([len(queries), len(ads)]))
for log in logs_tuple:
    query = log[0]
    ad = log[1]
    q_i = queries.index(query)
    a_i = ads.index(ad)
    graph[q_i, a_i] += 1

print(graph)
# print(graph[0])
# print(graph[0].tolist())
# print(graph.transpose()[0])

query_sim = matrix(numpy.identity(len(queries))) # 自己和自己的相似度为1，所以初始化为单位矩阵
ad_sim = matrix(numpy.identity(len(ads)))

def get_ads_num(query):
    q_i = queries.index(query)
    return graph[q_i]

def get_queries_num(ad):
    a_i = ads.index(ad)
    return graph.transpose()[a_i]

def get_ads(query):
    s = get_ads_num(query).tolist()[0]
    return [ ads[ad] for ad in range(len(s)) if s[ad] > 0 ]

def get_queries(ad):
    s = get_queries_num(ad).tolist()[0]
    return [ queries[x] for x in range(len(s)) if s[x] > 0 ]

def query_simrank(q1, q2, C):
    # print(get_ads_num(q1).tolist()[0])
    if q1 == q2:
        return 1
    if get_ads_num(q1).sum() == 0 or get_ads_num(q2).sum() == 0:
        return 0
    temp = 0
    for ad_i in get_ads(q1):
        for ad_j in get_ads(q2):
            i = ads.index(ad_i)
            j = ads.index(ad_j)
            temp += ad_sim[i, j]
    return C / get_ads_num(q1).sum() / get_ads_num(q2).sum() * temp

def ad_simrank(a1, a2, C):
    if a1 == a2:
        return 1
    if get_queries_num(a1).sum() == 0 or get_queries_num(a2).sum() == 0:
        return 0
    prefix = C / (get_queries_num(a1).sum() * get_queries_num(a2).sum())
    temp = 0
    for query_i in get_queries(a1):
        for query_j in get_queries(a2):
            i = queries.index(query_i)
            j = queries.index(query_j)
            temp += query_sim[i,j]
    return C / (get_queries_num(a1).sum() * get_queries_num(a2).sum()) * temp

def simrank(C = 0.8, times = 1):
    global query_sim, ad_sim

    for iteration in range(times):
        new_query_sim = matrix(numpy.identity(len(queries)))
        for q_i in queries:
            for q_j in queries:
                i = queries.index(q_i)
                j = queries.index(q_j)
                new_query_sim[i, j] = query_simrank(q_i, q_j, C)
        
        new_ad_sim = matrix(numpy.identity(len(ads)))
        for a_i in ads:
            for a_j in ads:
                i = ads.index(a_i)
                j = ads.index(a_j)
                new_ad_sim[i, j] = ad_simrank(a_i, a_j, C)

        query_sim = new_query_sim
        ad_sim = new_ad_sim
    
if __name__ == "__main__":
    print(queries)
    print(ads)
    simrank()
    print(query_sim)
    print(ad_sim)
        
