---
title: Tips for Pandas
created: unknown
updated: 2022-06-02
draft: true
---

## Append new row to dataframe

https://stackoverflow.com/questions/10715965/add-one-row-to-pandas-dataframe

list of dict is faster than dataframe.append()

## Show `nan` value

```python df_nan = df[df.isna().any(axis=1)]
print(df_nan)
```

https://stackoverflow.com/questions/43424199/display-rows-with-one-or-more-nan-values-in-pandas-dataframe

## Print options

```python
pd.set_option("display.max_columns", 30)
print(df_nan)
```

```python
with pd.option_context("display.max_rows",10):
   print(pd.get_option("display.max_rows"))
   print(pd.get_option("display.max_rows"))
```

## Using a custom function in Pandas groupby

In the previous example, we passed a column name to the groupby method. You can
also pass your own function to the groupby method. This function will receive an
index number for each row in the DataFrame and should return a value that will
be used for grouping. This can provide significant flexibility for grouping rows
using complex logic.

As an example, imagine we want to group our rows depending on whether the stock
price increased on that particular day. We would use the following:

```python
def increased(idx):
    return df.loc[idx].close > df.loc[idx].open

df.groupby(increased).groups
```

```plain
{False: Int64Index([2, 3, 4, 7, 8, 9, 13, 14], dtype='int64'),
 True: Int64Index([0, 1, 5, 6, 10, 11, 12], dtype='int64')}
```

References:

1. https://kite.com/blog/python/pandas-groupby-count-value-count/

## 在其他列上 aggregate

one or more columns

groupby 操作后继续的 aggregate 默认是针对 groupby 的那一列，如果要对其他列进行操
作，需要进一步指定 columns

```python
df.groupby("column_A").agg({"column_B": lambda x: x})
```

也可以进行一系列操作

```python
df.groupby("column_A").agg({"column_B": ["mean", "sum", "max"]})
```

PS: agg 默认是对 Columns 进行处理

References:

1. [group-by-aggregate-pandas](https://jamesrledoux.com/code/group-by-aggregate-pandas)
2. [pandas.DataFrame.agg](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.agg.html)

## Select most common values

```python
df.groupby("column_A").agg(lambda x:x.value_counts().index[0])
```

`pandas` >= 0.16: the "mode" function (most common element) `pd.Series.mode` is
available.

```python
df.groupby("column_A").agg(pd.Series.mode)
```

References:

1. [groupby-pandas-dataframe-and-select-most-common-value](https://stackoverflow.com/questions/15222754/groupby-pandas-dataframe-and-select-most-common-value)

## pandas drop inf

`df.dropna()` doesn't drop `Inf/-Inf` in default. Two methods to drop `Inf`
value.

First one, replace `inf` to `nan`:

    df.replace((np.inf, -np.inf), np.nan).dropna()

Second, use context option `use_inf_as_na`,

```python
with pd.option_context("mode.user_inf_as_na", True):
    df = df.dropna()
```

permanently with

    pd.set_option("use_inf_as_na", True)

References:

1. https://stackoverflow.com/questions/17477979/dropping-infinite-values-from-dataframes-in-pandas

## counting consecutive positive value in Python

先用 shift 进行转换然后判断是否和前一个元素是不同的用 cumsum() 计算出台阶 step
level 用 groupby 和 cumcount 进行分组统计

Second method:

groupby function from `itertools`

Ref:

1. [Counting consecutive positive value in Python array](https://stackoverflow.com/questions/27626542/counting-consecutive-positive-value-in-python-array)
2. [How to groupby consecutive values in pandas DataFrame](https://stackoverflow.com/questions/40802800/how-to-groupby-consecutive-values-in-pandas-dataframe)

## multiple aggregation for same column

Named aggregation

"但是不能混用"

Ref:

1. [Multiple aggregations of the same column](https://stackoverflow.com/questions/12589481/multiple-aggregations-of-the-same-column-using-pandas-groupby-agg)

## converting table to hierarchical tree structure with pandas

1. generate dict-like data

use `collections.defaultdict`

2. keep dataframe

MultiIndex

refs:

1. https://stackoverflow.com/questions/49491418/converting-table-directly-to-tree-structure-with-pandas
2. https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html
3. https://jakevdp.github.io/PythonDataScienceHandbook/03.05-hierarchical-indexing.html

## check missing datetime

https://stackoverflow.com/questions/52044348/check-for-any-missing-dates-in-the-index

## Efficiently iterating over rows in a Pandas DataFrame

https://mlabonne.github.io/blog/iterating-over-rows-pandas-dataframe/
