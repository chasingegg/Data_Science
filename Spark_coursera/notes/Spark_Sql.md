# Spark SQL

three main goals

- support **relational processing** both within Spark programs(RDDs) and on external data sources 
- high performance
- support external data sources like semi-structured data and external databases

## DataFrame

DataFrame is the Spark SQL's core abstraction. **It is conceptually equivalent to a table in a relational database**.可看作是a relational API over RDDs. DataFrame is a distributed collection of rows/records *with a known schema*. DataFrames are **untyped**. 每个element就是一个Row.

### Create DataFrame

- create from RDD, schema reflectively inferred.

  假设有rdd = RDD[(int, string, string)], rdd.toDF('id', 'name', 'city')

- create from RDD, schema explicitly specified

  - create an RDD of Rows
  - create the **schema** represented by a StructType matching the structure of Rows
  - apply the schema to the RDD of Rows by **creataDataFrame** method

  来一段代码

  ```scala
  val schemastring = "name age"
  val fields = schemastring.split(" ")
  .map(filedName => StructField(filedName, StringType, nullable = "true"))
  val schema = StructType(fileds) 

  //convert RDD to Rows
  val rowRDD = peopleRDD.map(_.split(,))
  			.map(attr => Row(attr(0), attr(1).trim))
  			
  val peopleDF = spark.createDataFrame(rowRDD, schema)
  ```

- create by reading in a data source from file

  ```scala
  val df = spark.read.json("....")
  ```

### SQL literal

现在我们有peopleDF这么一个DataFrame, we just have to register our DataFrame as a temporary SQL view first.

SQL literals can be passed to Spark SQL's sql method.

```scala
val adultDF = spark.sql("select * from people where age > 17")
```



Now we can see if we have a DataFrame, we use SQL syntax and do SQL queries on them. But DataFrame has its APIs as well.

接下来就主要focus on DataFrame API了

每一个Scala Type对应SQL里面的dataType

case class Person(name: String, age: int)对应StructType(List(StructField("name", StringType, true), StructField("age", IntegerType, true)))

### API

**show()** 显示出DataFrame的elements 默认是first 20 elements

**printSchema()** print the schema in a tree format 类似于下面这种形式

root 

  |— id: Integer

  |— name: String

Transformations on DataFrames are (1)operations which return  DataFrame as a result, and (2) are lazily evaluated.

当我们要specify columns, there are three ways. 

- using \$     df.filter($"age" > 18)
- refer to the DataFrame        df.filter(df("age") > 18)
- using SQL query string        df.filter("age > 18")

Grouping and aggregating(复习SQL去吧。。。)

**drop()** drop Rows that one conlumn contains null or NaN values

**fill(0)** replace all occurrences of null or NaN in numeric columns with specified value

Joins    df1.join(df2, \$"df1.id" == $"df2.id")

### Optimizations

Two specialized backend components

- Catalyst, query optimizer
- Tungsten, off-heap serializer

**Catalyst compiles Spark SQL programs down to an RDD!**

RDD vs DataFrame 

- RDD not too much structure, difficult to optimize
- DataFrame   lots of structure and optimization opportunities

Catalyst会做的优化

- reordering operations
- reduce the amount of data we must read
- pruning unneeded partitioning

Tungsten会做的优化

- highly-specialized data encoders(more data fits in memory)
- column-based 基于观察大部分操作着重部分特定的列不需要整个Row
- off heap

## Dataset

用DataFrame的时候不能直接使用collect()方法，因为Row是untyped。那如果要both Spark SQL optimizations and type safety 那就要引入Dataset这个概念了。而事实上DataFrame也是一种Dataset。DataFrame = Dataset[Row].

Dataset can be thought as the **typed** distributed collections of data.

Dataset can be thought as the compromise between RDD & DataFrame. More type informations than DataFrame, more optimizations than RDDs. RDD和DataFrame的API可以混用。

Typed columns   **$"price".as[Double]**

后面又是一大串运算，我放弃了。。。







 

