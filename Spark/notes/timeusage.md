# timeusage

In this assignment, we will see three groups of activities

- primary needs(eating, sleeping)
- work
- other

And to observe how people allocate their time on these three activities, and if we can see the differences between women and men, unemployed and employed, and young(less than 22), active(22-55) and elder people.

## Read-in data

第一列是StringType，其他列都是DoubleType.

## Project

Classify the given list of column names into three groups(primary needs, work, other). This method should return a triplet containing the “primary needs” columns list, the “work” columns list and the “other” columns list. 比如"t01"开头的是primary needs, "t05"开头的是working, "t02"开头的是other。在这里需要赞一下scala的模式匹配，实在太厉害了。

The second step is to implement the timeUsageSummary method. 以每一条record(人)为单位记录working status, sex, age, time on primary needs, time on working, time on others.

## Aggregate

Finally, we want to compare the *average time* spent on each activity, for all the combinations of working status, sex and age.