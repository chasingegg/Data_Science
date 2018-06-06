# stackoverflow

The overall goal of this assignment is to implement a distributed k-means algorithm which clusters posts on the popular question-answer platform StackOverflow according to their score. 

## K-means recall

首先重温一下kmeans, kmeans是一个经典聚类算法。

- 选取k个点作为初始聚类中心
- 对于每个点计算出最近的聚类中心，并将其分配给最近的那个聚类中心
- 对于每一个新聚类计算出新的聚类中心
- 通过计算新旧聚类中心的square distance来判断是否收敛，如果收敛结束算法，如果不收敛继续第二步。

## The Data

数据格式为

- postTypeId: type 1表示question 2表示answer
- id: unique标识符
- acceptedAnswer: id of the accepted answer post
- parentId: 对于answer: id of the corresponding question, 对于question: missing
- score: The stackoverflow score
- tag: indicates the programming language that the post is about

接下来要做data processing

## Grouping questions and answers

我们所要得到的结果是RDD[(QID, Itreable[(Question, Answer)])] QID是question的id和answer的parentId

首先通过postTypeId == 1, 2 filter出question和answer再做一下map，接下里做一下join，最后进行groupByKey将相同QID的组合聚合起来。

## Computing scores

RDD[(QID, Itreable[(Question, Answer)])]  => RDD[(Question, Iterable[(Answer)])]  => RDD[(Question, maxScore)]

## Creating vectors for clustering

Prepare the input for the clustering algorithm. Transform the scored RDD into a vectors RDD containing the vectors to be clustered.

结果是RDD[(int, int)] 

- index of the language(tag)
- the highest answer score

**使用cache将重复使用的RDD持久化**

## Kmeans clustering 

- pairing each vector with the index of the closet mean
- computing the new means by averaging the values of each other

## Computing cluster details

得到我们最终要的结果

