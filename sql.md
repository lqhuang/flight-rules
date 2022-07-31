---
title: "SQL Tips"
created: 2020-01-01
updated: 2022-03-31
---

## pandas or SQLAlchemy

### 通过 Mixin 实现 tablename 自动申明

https://www.etuan.com/zx/134-26014.html
https://www.osgeo.cn/sqlalchemy/orm/extensions/declarative/mixins.html

### SQLAlchemy ORM conversion to pandas DataFrame

Combine `sqlalchemy` and `pandas`:

    df = pd.read_sql(query.statement, query.session.bind)
    # Or with params
    c = query.statement.compile(query.session.bind)
    df = pandas.read_sql(c.string, query.session.bind, params=c.params)

References:

1. [SQLAlchemy ORM conversion to pandas DataFrame](https://stackoverflow.com/questions/29525808/sqlalchemy-orm-conversion-to-pandas-dataframe)

###

Problem:

df.to_sql()

Adding (Insert or update if key exists) option to `.to_sql`

upsert =?

https://github.com/pandas-dev/pandas/issues/14553

way 1:

```python
session.bulk_update_mappings(
  Table,
  pandas_df.to_dict(orient='records)
)
```

Ref:

https://www.codementor.io/bruce3557/graceful-data-ingestion-with-sqlalchemy-and-pandas-pft7ddcy6

https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.bulk_update_mappings
https://docs.sqlalchemy.org/en/13/orm/persistence_techniques.html#bulk-operations

way 2:

```python
insert_values = df.to_dict(orient='records')
insert_statement = sqlalchemy.dialects.postgresql.insert(table).values(insert_values)
upsert_statement = insert_statement.on_conflict_do_update(
    constraint='fact_case_pkey',
    set_= df.to_dict(orient='dict')
)
```

References:

1. [INSERT…ON CONFLICT (Upsert)](https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#insert-on-conflict-upsert)
2. [INSERT…ON DUPLICATE KEY UPDATE (Upsert)](https://docs.sqlalchemy.org/en/13/dialects/mysql.html#insert-on-duplicate-key-update-upsert)

## round the datetime or timestamp to nearest time frequency

https://stackoverflow.com/questions/19290879/mysql-round-the-datetime-to-15-minute/19291116

```sql
SET time_zone='+00:00';
SELECT
    FROM_UNIXTIME( FLOOR(Timestamp / (1000 * 60 * 5 )) * (1000 * 60 * 5) / 1000 ) as datetime,
    MAX(High) as high,
    MIN(Low) as low,
    SUM(Volume) as volume
FROM
    some_table
WHERE
    Timestamp BETWEEN 1582109400000 AND 1582195800000
GROUP BY
    datetime
ORDER BY
    datetime
```

Try `round` and `ceil` for different approximation methods

## Last row of a group

feature for windows function is required

窗口函数简介

### 什么叫窗口？

窗口的概念非常重要，它可以理解为记录集合，窗口函数也就是在满足某种条件的记录集合
上执行的特殊函数。对于每条记录都要在此窗口内执行函数，有的函数随著记录不同，窗口
大小都是固定的，这种属于静态窗口；有的函数则相反，不同的记录对应著不同的窗口，这
种动态变化的窗口叫滑动窗口。

### 窗口函数和普通聚合函数的区别

窗口函数和普通聚合函数也很容易混淆，二者区别如下：

- 聚合函数是将多条记录聚合为一条；而窗口函数是每条记录都会执行，有几条记录执行完
  还是几条。
- 聚合函数也可以用于窗口函数中。

注意：如果不加 order by, 就没有窗口，计算范围是整个分区；如果加上 order by, 默认
窗口是 range between unbounded preceding and current row，就是排序后从分区第一行
一直到当前行为止。

由于我们需要求的是每个用户的第一个和最后一个订单，所以这里要指定窗口：从第一行
unbounded preceding 到最后一行 unbounded following。

```sql
SET time_zone='+00:00';

SELECT * FROM (
  SELECT
    FROM_UNIXTIME(FLOOR(Timestamp / (1000 * 60 * 60 )) * (1000 * 60 * 60) / 1000) as datetime,
    FIRST_VALUE(Open) OVER barw as open,
    MAX(High)         OVER barw as high,
    MIN(Low)          OVER barw as low,
    LAST_VALUE(Close) OVER barw as close,
    SUM(Volume)       OVER barw as volume
  FROM
    BTC_USDT
  WHERE
    Timestamp >= 1582109400000 AND Timestamp <= 1582195800000
  WINDOW
    barw AS (PARTITION BY datetime ORDER BY Timestamp ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  ORDER BY
    datetime
) as WINDOWED GROUP BY datetime;
```

CTE format:

```sql
SET time_zone='+00:00';

WITH windowed AS (
  SELECT
    FROM_UNIXTIME(FLOOR(Timestamp / (1000 * 60 * 60 )) * (1000 * 60 * 60) / 1000) as datetime,
    FIRST_VALUE(Open) OVER barw as open,
    MAX(High)         OVER barw as high,
    MIN(Low)          OVER barw as low,
    LAST_VALUE(Close) OVER barw as close,
    SUM(Volume)       OVER barw as volume
  FROM
    BTC_USDT
  WHERE
    Timestamp >= 1582109400000 AND Timestamp <= 1582195800000
  WINDOW
    barw AS (PARTITION BY datetime ORDER BY Timestamp ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  ORDER BY
    datetime
)
SELECT * FROM windowed GROUP BY datetime;
```

References:

1. https://dev.mysql.com/doc/refman/8.0/en/window-functions-usage.html
2. https://stackoverflow.com/questions/1313120/retrieving-the-last-record-in-each-group-mysql
3. https://tding.top/archives/c6e31643.html
4. http://mysql.taobao.org/monthly/2018/11/09

## 性能分析

http://mysql.taobao.org/monthly/2018/12/09/
http://mysql.taobao.org/monthly/2018/11/06/

## 连续 consecutive count

## server default

https://github.com/sqlalchemy/sqlalchemy/issues/3444#issuecomment-441929498
https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime/33532154#33532154

## Close idle connections

```sql
WITH inactive_connections AS (
    SELECT
        pid,
        rank() over (partition by client_addr order by backend_start ASC) as rank
    FROM
        pg_stat_activity
    WHERE
        -- Exclude the thread owned connection (ie no auto-kill)
        pid <> pg_backend_pid( )
    AND
        -- Exclude known applications connections
        application_name !~ '(?:psql)|(?:pgAdmin.+)'
    AND
        -- Include connections to the same database the thread is connected to
        datname = current_database()
    AND
        -- Include connections using the same thread username connection
        usename = current_user
    AND
        -- Include inactive connections only
        state in ('idle', 'idle in transaction', 'idle in transaction (aborted)', 'disabled')
    AND
        -- Include old connections (found with the state_change field)
        current_timestamp - state_change > interval '5 minutes'
)
SELECT
    pg_terminate_backend(pid)
FROM
    inactive_connections
WHERE
    rank > 1 -- Leave one connection for each application connected to the database
```

```sql
WITH inactive_connections AS (
    SELECT
        pid,
        datname,
        state,
        usename,
        application_name,
        client_addr,
        state_change,
        query
    FROM
        pg_stat_activity
    WHERE
        -- Exclude the thread owned connection (ie no auto-kill)
        pid <> pg_backend_pid()
    AND
        -- Exclude known applications connections
        application_name !~ '(?:psql)|(?:pgAdmin.+)'
    AND
        -- Include inactive connections only
        state in ('idle', 'idle in transaction', 'idle in transaction (aborted)', 'disabled')
    AND
        -- Include old connections (found with the state_change field)
        current_timestamp - state_change > interval '5 minutes'
)
SELECT
    pg_terminate_backend(pid)
FROM
    inactive_connections;
```

References:

https://stackoverflow.com/questions/12391174/how-to-close-idle-connections-in-postgresql-automatically/30769511

## Check a value against a sequence in `asyncpg`

`expression IN $1` is not a valid PostgreSQL syntax. To check a value against a
sequence use `expression = any($1::mytype[])`, where `mytype` is the array
element type.

References:

1. [FAQ: Why do I get PostgresSyntaxError when using expression IN $1?](https://magicstack.github.io/asyncpg/current/faq.html#why-do-i-get-postgressyntaxerror-when-using-expression-in-1)
2. [Issue #94: Passing a list as parameter](https://github.com/MagicStack/asyncpg/issues/94)

## PostgreSQL: server-side timeouts

As documented runtime configs:

- `statement_timeout` (integer)
  - Abort any statement that takes more than the specified amount of time. If
    `log_min_error_statement` is set to `ERROR` or lower, the statement that
    timed out will also be logged. If this value is specified without units, it
    is taken as milliseconds. A value of zero (the default) disables the
    timeout.
  - The timeout is measured from the time a command arrives at the server until
    it is completed by the server. If multiple SQL statements appear in a single
    simple-Query message, the timeout is applied to each statement separately.
    (PostgreSQL versions before 13 usually treated the timeout as applying to
    the whole query string.) In extended query protocol, the timeout starts
    running when any query-related message (Parse, Bind, Execute, Describe)
    arrives, and it is canceled by completion of an Execute or Sync message.
  - Setting `statement_timeout` in `postgresql.conf` is not recommended because
    it would affect all sessions.
- `lock_timeout` (integer)
- `idle_in_transaction_session_timeout` (integer)
- `idle_session_timeout` (integer)

You can also set the timeout in your connected sessions:

```sql
SET statement_timeout = 10000;
SELECT * from your_table;
```

Refs:

1. [Is it possible to limit timeout on Postgres server?](https://dba.stackexchange.com/questions/164419/is-it-possible-to-limit-timeout-on-postgres-server)
2. [Docs: 20.11. Client Connection Defaults](https://www.postgresql.org/docs/current/runtime-config-client.html)
