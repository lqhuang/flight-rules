---
title: Tips for Pandas
created: 2019-01-01
updated: 2023-10-29
---

## Append new row to dataframe

List of `dict` is faster than `dataframe.append()`.

> from Pandas >= 2.0, `append` has been removed!

- [Create a Pandas Dataframe by appending one row at a time](https://stackoverflow.com/questions/10715965/add-one-row-to-pandas-dataframe)

## Show `nan` value

```python
df_nan = df[df.isna().any(axis=1)]
print(df_nan)
```

- [Display rows with one or more NaN values in pandas dataframe](https://stackoverflow.com/questions/43424199/display-rows-with-one-or-more-nan-values-in-pandas-dataframe)

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

1. [How to Use Pandas GroupBy, Counts and Value Counts](https://kite.com/blog/python/pandas-groupby-count-value-count/)

## Aggregate on other columns after groupby

one or more columns

`groupby` 操作后继续的 `aggregate` 默认是针对 `groupby` 的那一列，如果要对其他列
进行操作，需要进一步指定 columns

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

`pandas>=0.16`: the "mode" function (most common element) is added.
`pd.Series.mode` is available.

```python
df.groupby("column_A").agg(pd.Series.mode)
```

References:

1. [groupby-pandas-dataframe-and-select-most-common-value](https://stackoverflow.com/questions/15222754/groupby-pandas-dataframe-and-select-most-common-value)

## Pandas drops `Inf` value

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

1. [Dropping infinite values from dataframes in pandas?](https://stackoverflow.com/questions/17477979/dropping-infinite-values-from-dataframes-in-pandas)

## Counting consecutive positive value in Python

先用 `shift` 进行转换然后判断是否和前一个元素是不同的用 `cumsum()` 计算出台阶
step level 用 `groupby` 和 `cumcount` 进行分组统计

Second method:

`groupby` function from `itertools`

Ref:

1. [Counting consecutive positive value in Python array](https://stackoverflow.com/questions/27626542/counting-consecutive-positive-value-in-python-array)
2. [How to groupby consecutive values in pandas DataFrame](https://stackoverflow.com/questions/40802800/how-to-groupby-consecutive-values-in-pandas-dataframe)

## Multiple aggregation for same column

Named aggregation "但是不能混用"

Ref:

1. [Multiple aggregations of the same column](https://stackoverflow.com/questions/12589481/multiple-aggregations-of-the-same-column-using-pandas-groupby-agg)

## (draft) converting table to hierarchical tree structure with pandas

1. generate dict-like data

use `collections.defaultdict`

2. keep dataframe

MultiIndex

refs:

1. https://stackoverflow.com/questions/49491418/converting-table-directly-to-tree-structure-with-pandas
2. https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html
3. https://jakevdp.github.io/PythonDataScienceHandbook/03.05-hierarchical-indexing.html

## Check missing datetime

> `DatetimeIndex.difference()`

- [check for any missing dates in the index](https://stackoverflow.com/questions/52044348/check-for-any-missing-dates-in-the-index)

## Efficiently iterating over rows in a Pandas DataFrame

> Never use iterrows and itertuples again!

(😅 ???)

1. ❌❌ Iterrows
2. ❌ For loop with .loc or .iloc (3× faster)
3. ❌ Apply (4× faster)
4. ❌ Itertuples (10× faster)
5. ❌ List comprehensions (200× faster)
6. ✅ Pandas vectorization (1500× faster)
7. ✅✅ NumPy vectorization (1900× faster)

- [Efficiently iterating over rows in a Pandas DataFrame](https://mlabonne.github.io/blog/iterating-over-rows-pandas-dataframe/)

## This's a feature not bug

pandas index "feature"

Solution:

example

- [When adding a Series to a DataFrame with a different index, the Series gets turned into all NaNs](https://github.com/pandas-dev/pandas/issues/450)

### 2023-11-08: Yeah I suffered this again...

problem caused: series - series with different index, and one of them is
datetime index

```python
import pandas as pd

a = pd.Series(range(100))
b = pd.Series(range(59))

print(a - b)
print((a - b).sum())

b = pd.Series(range(59), index=(i+1 for i in range(59)))
print(a - b)
print((a - b).sum())
```

### Index alignment feature for operations

- [Operating on Data in Pandas](https://jakevdp.github.io/PythonDataScienceHandbook/03.03-operations-in-pandas.html)
- [Intro to data structures](https://pandas.pydata.org/docs/user_guide/dsintro.html)

## Make groupby apply method parallel

Adds an `apply_parallel` method of making groupby calculation parallel with
multiple prcesses to pandas dataframes & series:

```python
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

@pd.api.extensions.register_dataframe_accessor('apply_parallel')
@pd.api.extensions.register_series_accessor('apply_parallel')
class ApplyParallel:
    """Registers a custom method `apply_parallel` for dataframes & series."""

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, func, args, axis=0):
        """Applies func to a pandas object along the axis.
        Useful with big pandas objects when func can't be easily vectorized.
        func can't be a lambda function because multiprocessing can't pickle it.
        """
        # df.apply(func, axis=1) applies func to each row,
        # but np.array_split(df, n, axis=0) splits df into n chunks of rows,
        # so swap the axis number when working with dataframes.
        if isinstance(self._obj, pd.DataFrame):
            axis = 1 - axis
        # But if the pandas object is a series, the axis is always 0.
        else:
            assert axis == 0
        # Use all the CPUs
        num_jobs = cpu_count()
        with ProcessPoolExecutor(max_workers=num_jobs) as executor:
            # Split your pandas object into chunks
            split_objects = np.array_split(self._obj, num_jobs, axis=axis)
            # Map your function to each split in parallel
            results = executor.map(func, split_objects)
        # Concat them back together
        return pd.concat(results)


# df = pd.DataFrame({'col': list(range(30))})

# def my_func(row):
#     return row.col ** 2

# assert all(df.apply_parallel(my_func, axis=1) == df.apply(my_func, axis=1))
```

Refs:

- [Tweet from @marktenenholtz](https://twitter.com/marktenenholtz/status/1557336004721160192)
- [GitHub Gist - rrherr/apply_parallel.py](https://gist.github.com/rrherr/ae9cb03bcdb0d322eeac156db9494fcd)

## When is inplace in Pandas faster?

Use of The `inplace=True` keyword is discouraged, it's generally seen as bad
practice and often unnecessary. Not only because `inplace=True` breaks method
chaining and efficiency optimization, but also an extra reason which is easy to
miss or forget.[^1][^2]

> Operations that re-arrange the rows of a DataFrame can't be executed without
> copying. Avoid the inplace argument for these methods.
>
> Some DataFrame methods can never operate inplace. Their operation (like
> reordering rows) requires copying, so they create a copy even if you provide
> `inplace=True`.
>
> For these methods, inplace doesn't bring a performance gain.
>
> It's only a "syntactic sugar for reassigning the new result to the calling
> DataFrame/Series."

PDEP-8[^3] is an ongoing proposal to remove `inplcae` keyword from Group 4
methods.

- Group 1: Methods that always operate inplace (no user-control with
  inplace/copy keyword)
- Group 2: Methods that modify the underlying data of the DataFrame/Series
  object and can be done inplace
- Group 3: Methods that modify the DataFrame/Series object, but not the
  pre-existing values
- Group 4: Methods that can never operate inplace

Alright, for methods that can happen with or without copying the `DataFrame`
object, the `inplace` argument (possibly) is OK and can bring performance gains.

- delete rows from the end (`pop`),
- add columns
- delete columns (`drop`)
- mutate the elements (`update`, `where`, `fillna`, `replace`)

But in generally, method chaining style is still recommended.

Refs:

- [^1]
  [When is inplace in Pandas faster?](https://sourcery.ai/blog/pandas-inplace/)
- [^2]
  [Pandas: Avoid inplace](https://docs.sourcery.ai/Reference/Python/Default-Rules/pandas-avoid-inplace/)
- [^3]
  [PDEP-8: In-place methods in pandas](https://github.com/pandas-dev/pandas/pull/51466/files?short_path=f2cc21a#diff-f2cc21ad9c9caffa3506c4719e07e1db49a2a3368bd6b41a1abf90eb8e3e416c)

## `head` and `tail` methods accept a negative value in Pandas

Probably no body knows that `head` and `tail` methods accept a negative value
which is useful to delete the last few rows of data without `drop`.

```python
# For negative values of given input, this function returns all rows
# except the last `|-n|` rows
df.head(-n)
# totally equivalent to
df.iloc[:-n]

# For negative values of given input, this function returns all rows
# except the first `|-n|` rows
df.tail(-n)
# totally equivlant
df.iloc[n:]
```

They are much eaiser to understand and perform well.

```python-repl
>>> %timeit df[:-1]
125 µs ± 132 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

>>> %timeit df.head(-1)
129 µs ± 1.18 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

>>> %timeit df.drop(df.tail(1).index)
751 µs ± 20.4 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
```

Actually, that's also how source codes implement them 😅. But note that these
methods return a **view** instead of a **copy**.

Refs:

- [How to delete the last row of data of a pandas dataframe](https://stackoverflow.com/questions/26921651/how-to-delete-the-last-row-of-data-of-a-pandas-dataframe)
- [Src code for `head` and `tail`](https://github.com/pandas-dev/pandas/blob/v2.1.2/pandas/core/generic.py#L5729-L5804)
