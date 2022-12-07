---
title: Python Tips
created: 2019-01-01
updated: 2022-11-27
---

## `numpy.asarray` 和 `numpy.array` 的区别

The definition of asarray is:

```python
def asarray(a, dtype=None, order=None):
    return array(a, dtype, copy=False, order=order)
```

So it is like array, except it has fewer options, and `copy=False`. array has
`copy=True` by default.

The main difference is that array (by default) will make a copy of the object,
while asarray will not unless necessary.

ref: https://stackoverflow.com/questions/14415741/numpy-array-vs-asarray

## 利用 Conda 在 64b-it 平台上创建 32-bit 的环境

通过环境变量(environmental variables)进行配置

    set CONDA_FORCE_32BIT=1
    conda create -n py27_32bit python=2.7

Refs:

1. [Conda is mixing 32-bit and 64-bit packages](https://github.com/conda/conda/issues/1744)
2. [using-multiple-python-engines-32bit-64bit](https://stackoverflow.com/questions/33709391/using-multiple-python-engines-32bit-64bit-and-2-7-3-5)

## Enable rasterized (光栅化) for matplotlib

Improve size of vector graphics (eg: svg, pdf, eps format)

Ref:

1. [Slim down your bloated graphics](http://www.astrobetter.com/blog/2014/01/17/slim-down-your-bloated-graphics/)

## Axis Style

```python
from mpl_toolkits.axisartist.axislines import SubplotZero
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
ax = SubplotZero(fig, 111)
fig.add_subplot(ax)

for direction in ["xzero", "yzero"]:
    # adds arrows at the ends of each axis
    ax.axis[direction].set_axisline_style("-|>")

    # adds X and Y-axis from the origin
    ax.axis[direction].set_visible(True)

for direction in ["left", "right", "bottom", "top"]:
    # hides borders
    ax.axis[direction].set_visible(False)

x = np.linspace(-0.5, 1., 100)
ax.plot(x, np.sin(x*np.pi))

plt.show()
```

Refs:

1. https://matplotlib.org/gallery/axisartist/demo_axisline_style.html?highlight=subplotzero
2. https://stackoverflow.com/questions/33737736/matplotlib-axis-arrow-tip/33738359
3. https://stackoverflow.com/questions/17646247/how-to-make-fuller-axis-arrows-with-matplotlib

## Deleting diagonal elements of a numpy array

Readable and efficient enough solution:

```python
def del_diag(matrix):
    m, n = matrix.shape
    return matrix[~np.eye(m, n, dtype=bool)].reshape(m, n - 1)
```

Ref:

1. [Deleting diagonal elements of a numpy array](https://stackoverflow.com/questions/46736258/deleting-diagonal-elements-of-a-numpy-array)

## String format cheatsheet

    format*spec ::= [[fill]align][sign][#][0][width][grouping_option][.precision][type]
    fill ::= <any character>
    align ::= "<" | ">" | "=" | "^"
    sign ::= "+" | "-" | " "
    width ::= digit+
    grouping_option ::= "*" | ","
    precision ::= digit+
    type ::= "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"

Ref:

1. [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#format-specification-mini-language)

## pytz

- Asia/Shanghai
- Asia/Taipei

LMT vs CST

local mean time

TypeError: can't subtract offset-naive and offset-aware datetimes

Ref: https://www.jb51.net/article/163565.htm

## anaconda env activation after 4.4

```shell
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('${HOME}/Software/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "${HOME}/Software/miniconda3/etc/profile.d/conda.sh" ]; then
        . "${HOME}/Software/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="${HOME}/Software/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```

Use

    . /home/<user>/miniconda3/etc/profile.d/conda.sh

Rather than

    export PATH="/home/<user>/miniconda3/bin:$PATH"

https://github.com/conda/conda/blob/master/CHANGELOG.md#440-2017-12-20

## Install package in development mode

The `pip install -e .` command allows you to follow the development branch as it
changes by creating links in the right places and installing the command line
scripts to the appropriate locations.

## CamelCase to camel_case

Ref:

1. https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case

## Split a string at uppercase letters

```python
>>> import re
>>> re.findall('[A-Z][^A-Z]*', 'TheLongAndWindingRoad')
['The', 'Long', 'And', 'Winding', 'Road']
>>> re.findall('[A-Z][^A-Z]*', 'ABC')
['A', 'B', 'C']
```

```python
re.split('(?=[A-Z])', 'theLongAndWindingRoad')
['the', 'Long', 'And', 'Winding', 'Road']
```

All these methods will fail in serveral corner cases, test it via:

- "theLongAndWindingRoad"
- "ABCD"
- "TheLongAndWindingRoad"

```python
re.findall('.[^A-Z]*', 'aboutTheLongAndWindingRoadABC')
```

```python
def split_on_uppercase(s, keep_contiguous=False):
    """

    Args:
        s (str): string
        keep_contiguous (bool): flag to indicate we want to
                                keep contiguous uppercase chars together

    Returns:

    """

    string_length = len(s)
    is_lower_around = (lambda: s[i-1].islower() or
                       string_length > (i + 1) and s[i + 1].islower())

    start = 0
    parts = []
    for i in range(1, string_length):
        if s[i].isupper() and (not keep_contiguous or is_lower_around()):
            parts.append(s[start: i])
            start = i
    parts.append(s[start:])

    return parts

>>> split_on_uppercase('theLongWindingRoad')
['the', 'Long', 'Winding', 'Road']
>>> split_on_uppercase('TheLongWindingRoad')
['The', 'Long', 'Winding', 'Road']
>>> split_on_uppercase('TheLongWINDINGRoadT', True)
['The', 'Long', 'WINDING', 'Road', 'T']
>>> split_on_uppercase('ABC')
['A', 'B', 'C']
>>> split_on_uppercase('ABCD', True)
['ABCD']
>>> split_on_uppercase('')
['']
>>> split_on_uppercase('hello world')
['hello world']
```

Ref:

1. [Split a string at uppercase letters](https://stackoverflow.com/questions/2277352/split-a-string-at-uppercase-letters)

## SQLAlchemy and asyncio (run_in_executor):

1. https://gist.github.com/Tarliton/c494fa972a7a2594372738c96c0654a1
2. https://stackoverflow.com/questions/21078696/why-is-my-scoped-session-raising-an-attributeerror-session-object-has-no-attr
3. https://stackoverflow.com/questions/51446322/flask-sqlalchemy-set-expire-on-commit-false-only-for-current-session
4. https://marlinux.wordpress.com/2017/05/19/python-3-6-asyncio-sqlalchemy/
5. https://davidcaron.dev/sqlalchemy-multiple-threads-and-processes/
6. https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-faq-whentocreate

## Binding process into single core

1. taskset

2. modern python

- `os.sched_setaffinity`
- `os.sched_getaffinity`

3. psutil

```python
proc = psutil.Process() # get self pid proc.cpu_affinity
```

References:

1. https://unix.stackexchange.com/questions/23106/how-to-limit-a-process-to-one-cpu-core-in-linux
2. https://stackoverflow.com/questions/5784389/using-100-of-all-cores-with-the-multiprocessing-module/35371568
3. http://sorami-chi.hateblo.jp/entry/2016/04/29/000000
4. https://www.geeksforgeeks.org/python-os-sched_setaffinity-method/
5. https://stackoverflow.com/questions/36172101/designate-specific-cpu-for-a-process-python-multiprocessing
6. https://stackoverflow.com/questions/5784389/using-100-of-all-cores-with-the-multiprocessing-module/35371568#35371568

### extra: assign run progress in one core exclusively

1. https://superuser.com/questions/1082194/assign-an-individual-core-to-a-process
2. https://diego.assencio.com/?index=4515794de9f941c632d593384ca39dea
3. https://unix.stackexchange.com/questions/326579/how-to-ensure-exclusive-cpu-availability-for-a-running-process
4. https://stackoverflow.com/questions/9072060/one-core-exclusively-for-my-process/9079117#9079117

## Print actual query in SQLAlchemy

```python
print(stmt.compile(dialect=postgresql.dialect(),compile_kwargs={"literal_binds":
True}))
```

References:

1. https://stackoverflow.com/questions/4617291/how-do-i-get-a-raw-compiled-sql-query-from-a-sqlalchemy-expression
2. https://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query/23835766

## Upsert `on_conflict_do_update` in SQLAlchemy

Refs:

1. https://gist.github.com/bhtucker/c40578a2fb3ca50b324e42ef9dce58e1
2. https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#insert-on-conflict-upsert

## Understanding `min_df` and `max_df` in scikit `CountVectorizer`

example:

```
tfidf_vectorizer = TfidfVectorizer(
    max_features=max_features,
    max_df=0.8,
    min_df=3,
    stop_words=None,  # 'english',
    use_idf=True,
    ngram_range=(2, 5),
)
```

explain:

`max_df` is used for removing terms that appear **too frequently**, also known
as "corpus-specific stop words". For example:

- `max_df = 0.50` means "ignore terms that appear in **more than 50% of the
  documents**".
- `max_df = 25` means "ignore terms that appear in **more than 25 documents**".

The default `max_df` is `1.0`, which means "ignore terms that appear in **more
than 100% of the documents**". Thus, the default setting does not ignore any
terms.

`min_df` is used for removing terms that appear **too infrequently**. For
example:

- `min_df = 0.01` means "ignore terms that appear in **less than 1% of the
  documents**".
- `min_df = 5` means "ignore terms that appear in **less than 5 documents**".

The default `min_df` is `1`, which means "ignore terms that appear in **less
than 1 document**". Thus, the default setting does not ignore any terms.

Ref:

1. [understanding-min-df-and-max-df-in-scikit-countvectorizer](https://stackoverflow.com/questions/27697766/understanding-min-df-and-max-df-in-scikit-countvectorizer)

## Hidden variable in `dataclass`

Ref:

https://github.com/sebastian-ahmed/python-etc/tree/main/dataclasses_pandas

## Saving memory with `__slots__`

If you ever wrote a program that was creating really big number of instances of
some class, you might have noticed that your program suddenly needed a lot of
memory. That is because Python uses dictionaries to represent attributes of
instances of classes, which makes it fast but not very memory efficient, which
is usually not a problem. However, if it becomes a problem for your program you
might try using **slots**:

What happens here is that when we define **slots** attribute, Python uses small
fixed-size array for the attributes instead of dictionary, which greatly reduces
memory needed for each instance. There are also some downsides to using
**slots** - we can't declare any new attributes and we are restricted to using
ones on **slots**. Also classes with **slots** can't use multiple inheritance.

Ref:

1. https://martinheinz.dev/blog/1

## Subclass instance attribute in Pydantic

1. `__init_subclass__`

2. GenericModel

```python
from __future__ import annotations

from typing import Generic, TypeVar
from enum import Enum

from pydantic import parse_obj_as
from pydantic.generics import GenericModel


class Super(Enum):
    ...


T = TypeVar("T", bound=Super)


class SubFoo(Super):
    A = "a1"
    B = "b1"
    C = "c1"


class SubBar(Super):
    A = "a2"
    B = "b2"
    C = "c2"


class Foo(GenericModel, Generic[T]):
    status: T


m = Foo[SubFoo](status=SubFoo.A)

a = parse_obj_as(Foo[SubFoo], {"status": "a1"})

print(a)
```

Refs:

1. https://github.com/samuelcolvin/pydantic/issues/1932
2. https://github.com/samuelcolvin/pydantic/issues/1229

### Get generic type in runtime

```python
from __future__ import annotations

from typing import Generic, TypeVar


T1 = TypeVar("T1")
T2 = TypeVar("T2")


class A(Generic[T1, T2]):
    ...


a = A[int, str]()

print(a)
print(a.__dict__)
print(a.__orig_class__.__dict__["__args__"])
print(A[int, str].__dict__["__args__"])
print(type(a).__dict__)  # no information for generic types
```

### `if __main__ == "__name__"` must be required while using `mupltiprocess`

Savely import main module

References:

1. https://mp.weixin.qq.com/s?__biz=MzU0OTg3NzU2NA==&mid=2247489119&idx=1&sn=076b0eca8e538615973494a511669ae9&chksm=fba8740cccdffd1ac7b9a0accdcb9dbc190be17000ae1de20e95bc93d26bca59c1855d146c7e&mpshare=1&scene=1&srcid=1029DYm6Gav8PnGJMRyXAe2l&sharer_sharetime=1635489470168&sharer_shareid=a02c97b66753e49e61e3def16e4d4411&exportkey=ATmw3UkoaqFIE13cmYK%2FT18%3D&pass_ticket=R%2BX2oYnRuoXgxtQg6YovU2EyJ1pgYLZPRYAFRm7NjSc0ERiUZEHitsxXWluIPXtT&wx_header=0#rd
2. https://docs.python.org/zh-cn/3/library/multiprocessing.html#programming-guidelines

## Sequence of python tools' configuration

WIP

1. https://pycqa.github.io/isort/docs/configuration/options.html
2. https://flake8.pycqa.org/en/latest/user/configuration.html
3. https://mypy.readthedocs.io/en/stable/config_file.html
4. https://mypy.readthedocs.io/en/stable/config_file.html#using-a-pyproject-toml-file
5. https://waylonwalker.com/python-tool-config/

## Find reverse dependency of one package

1. From command line:

Step 1. find your `site-packages` directory of your Python environment:

    /home/xxx/miniconda3/envs/some-dist/lib/python3.10/site-packages

Get into this directory, then run

```shell
cd /home/xxx/miniconda3/envs/some-dist/lib/python3.10/site-packages
find . -name METADATA -exec grep -H -i package-name-you-want-to-search {} \; | grep Requires-Dist
```

For example, to find reverse dependency for `anyio`:

```
find . -name METADATA -exec grep -H -i anyio {} \; | grep Requires-Dist
```

will output:

```
./starlette-0.16.0.dist-info/METADATA:Requires-Dist: anyio (<4,>=3.0.0)
./httpcore-0.14.3.dist-info/METADATA:Requires-Dist: anyio (==3.*)
./fastapi-0.70.1.dist-info/METADATA:Requires-Dist: anyio[trio] >=3.2.1,<4.0.0 ; extra == "test"
```

2. Use Python script:

```python
#!/bin/env python3
import pkg_resources
import sys

def find_reverse_deps(package_name):
    return [
        pkg.project_name for pkg in pkg_resources.WorkingSet()
        if package_name in {req.project_name for req in pkg.requires()}
    ]

if __name__ == '__main__':
    print(find_reverse_deps(sys.argv[1]))
```

You can copy these and run with `python -c "..." package-name` fastly.

Output example:

```shell
['starlette', 'httpcore']
```

3. Use Python package `pip-tools` or
   [`pipdeptree`](https://github.com/jazzband/pip-tools)

For example:

```shell
pipdeptree -r -p anyio
```

will output

```
anyio==3.5.0
  - httpcore==0.14.3 [requires: anyio==3.*]
    - httpx==0.21.1 [requires: httpcore>=0.14.0,<0.15.0]
      - foam==0.3.0 [requires: httpx]
  - starlette==0.16.0 [requires: anyio>=3.0.0,<4]
    - fastapi==0.70.1 [requires: starlette==0.16.0]
      - foam==0.3.0 [requires: fastapi]
```

References:

1. [How to find reverse dependency on python package](https://stackoverflow.com/a/62353494)
2. [Show reverse dependencies with pip?](https://stackoverflow.com/a/57657957)
3. [Github - naiquevin/pipdeptree](https://github.com/naiquevin/pipdeptree)
4. [Github - jazzband/pip-tools](https://github.com/jazzband/pip-tools)

## When `any` and `all` apply in empty collections

In Python, logic operators `any` and `all` both are lazy function. Be care to
their output when applying in empty collections.

```python
any([])  # False
all([])  # True
any([True, False])  # True
all([True,False])  # False
```

## Round numbers in Python

Python follows "round half to even" rule, aka "bankers' rounding".

```python
round(7/2)  # 4
round(3/2)  # 2
round(5/2)  # round(2.5) == 2, not 3!
```

Ref:

1. [Rounding](https://en.wikipedia.org/wiki/Rounding#Round_half_to_even)

## Confused args shape for `pool.map`

```python
from time import sleep
from random import random

from concurrent.futures.thread import ThreadPoolExecutor


def func(arg1, arg2, arg3):
    sleep(random() * 3.0)
    print(arg1, arg2, arg3)


def test_args(aaa, *args):
    print(f"{aaa}", args)


if __name__ == "__main__":
    pool = ThreadPoolExecutor(4)

    args_list = [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (10, 11, 12),
    ]
    args_list = [
        (1, 4, 7, 10),
        (2, 5, 8, 11),
        (3, 6, 9, 12),
    ]

    # print(list(zip(*zip(*args_list))))
    test_args("????", *args_list)

    for args in zip(*args_list):
        print(args)
        # func(*args)

    jobs = pool.map(func, *args_list)

    tuple(jobs)
```

## Buffered IO in Python `open()` function.

Python's built-in function `open()` is actually a buffered IO wrapper in most
cases.

> The type of file object returned by the `open()` function depends on the mode.

| mode                                           | concrete instance            |
| ---------------------------------------------- | ---------------------------- |
| text mode (`'w'`, `'r'`, `'wt'`, `'rt'`, etc.) | `io.TextIOWrapper`           |
| read binary mode `rb`                          | `io.BufferedReader`          |
| write binary `wb` and append binary `ab` modes | `io.BufferedWriter`          |
| read/write mode                                | `io.BufferedRandom`          |
| buffering is disabled (`buffering=0`)          | `io.RawIOBase` / `io.FileIO` |

Look back to function signature `open(file, mode='r', buffering=-1, **kwargs)`

> `buffering` is an optional integer used to set the buffering policy. Pass `0`
> to switch buffering off (only allowed in binary mode), `1` to select line
> buffering (only usable in text mode), and an integer > 1 to indicate the size
> in bytes of a fixed-size chunk buffer.

> Note that specifying a buffer size this way applies for binary buffered I/O,
> but `TextIOWrapper` (i.e., files opened with `mode='r+'`) would have another
> buffering. To disable buffering in `TextIOWrapper`, consider using the
> `write_through` flag for
> [`io.TextIOWrapper.reconfigure()`](https://docs.python.org/3/library/io.html#io.TextIOWrapper.reconfigure).

> When no _buffering_ argument is given, the default buffering policy works as
> follows:
>
> - Binary files are buffered in fixed-size chunks; the size of the buffer is
>   chosen using a heuristic trying to determine the underlying device’s “block
>   size” and falling back on `io.DEFAULT_BUFFER_SIZE`. On many systems, the
>   buffer will typically be 4096 or 8192 bytes long.
> - “Interactive” text files (files for which `isatty()` returns True) use line
>   buffering. Other text files use the policy described above for binary files.

Extra comments:

> Text I/O over a binary storage (such as a file) is significantly slower than
> binary I/O over the same storage, because it requires conversions between
> unicode and binary data using a character codec. This can become noticeable
> handling huge amounts of text data like large log files. Also,
> `TextIOWrapper.tell()` and `TextIOWrapper.seek()` are both quite slow due to
> the reconstruction algorithm used.
>
> `StringIO`, however, is a native in-memory unicode container and will exhibit
> similar speed to `BytesIO`.

References:

1. [Built-in Functions: open](https://docs.python.org/3/library/functions.html#open)
2. [io — Core tools for working with streams](https://docs.python.org/3/library/io.html)

## Update `__setter__` in Runtime

Wow, dynamic language XD

```python
def spy_on_changes(obj):
    """Tweak an object instance to show attributes changing."""
    class Wrapper(obj.__class__):
        def __setattr__(self, name, value):
            old = getattr(self, name, '<NOTHING>')
            if old == '<NOTHING>':
                print(f"Assign attr - {name}: {value!r}")
            else:
                print(f"Update attr - {name}: {old!r} -> {value!r}")
            return super().__setattr__(name, value)
    obj.__class__ = Wrapper
```

If you want to spy on changes in some special instances without affecting all
concrete instances of that class, you can wrapper the object instance with above
codes.

```python-repl
>>> obj = SomeClass()
>>> obj.some_attr = "first"
>>> obj.some_attr
'first'

>>> spy_on_changes(obj)
>>> obj.some_attr = "second"
Update attr - some_attr: 'first' -> 'second'

>>> obj.another_attr = "foo"
Assign attr - another_attr: 'foo'
```

Why not just monkey patch `__setattr__`? Here, we can inherit the actual class
then use `super()` method to avoid some custom behaviors in parent.

References:

1. [Ned Batchelder's Status](https://twitter.com/nedbat/status/1533454622450503680)

## What is `conftest.py` for `pytest`

There are four major features with `conftest.py`:

- **Fixtures**: Define fixtures for static data used by tests. This data can be
  accessed by all tests in the suite unless specified otherwise. This could be
  data as well as helpers of modules which will be passed to all tests.
- **External plugin loading**: `conftest.py` is used to import external plugins
  or modules. By defining the following global variable, pytest will load the
  module and make it available for its test. Plugins are generally files defined
  in your project or other modules which might be needed in your tests. You can
  also load a set of predefined plugins as explained
  [here](https://pytest.org/en/latest/plugins.html#requiring-loading-plugins-in-a-test-module-or-conftest-file).
- **Hooks**: You can specify hooks such as setup and teardown methods and much
  more to improve your tests. For a set of available hooks, read
  [Hooks link](https://docs.pytest.org/en/6.2.x/reference.html#hooks).
- **Test root path**: This is a bit of a hidden feature. By defining
  `conftest.py` in your root path, you will have `pytest` recognizing your
  application modules without specifying `PYTHONPATH`. In the background,
  `py.test` modifies your `sys.path` by including all submodules which are found
  from the root path.

`conftest.py` files have directory scope. Therefore, creating targeted fixtures
and helpers is good practice.

Refercens:

1. [Uncommon Uses of Python in Commonly Used Libraries](https://eugeneyan.com/writing/uncommon-python/#a-hidden-feature-of-conftestpy)
2. [pytest fixtures: explicit, modular, scalable](https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files)
3. [In pytest, what is the use of conftest.py files?](https://stackoverflow.com/a/34520971)
4. [scikit-learn/scikit-learn/blob/main/conftest.py](https://github.com/scikit-learn/scikit-learn/blob/main/conftest.py)

### `conda activate ...` doesn't work in shell script

```
CommandNotFoundError: Your shell has not been properly configured to use 'conda activate'.
To initialize your shell, run

    $ conda init <SHELL_NAME>

Currently supported shells are:
  - bash
  - fish
  - tcsh
  - xonsh
  - zsh
  - powershell

See 'conda init --help' for more information and options.

IMPORTANT: You may need to close and restart your shell after running 'conda init'.
```

The reason is functions are not exported by default to be made available in
subshells. So it's recommended to add

    $(conda info --base)/etc/profile.d/conda.sh

or

    eval "$(conda shell.bash hook)"

before `conda activate` in your shell script.

References:

1. [Can't execute `conda activate` from bash script #7980](https://github.com/conda/conda/issues/7980)

## Turn flat list to pair tuple

Usual way to take a flat list of key/value data and turn them into paired tuple
/ dictionary:

```python
flat = ["color", "red", "style", "striped", "debug", True]

flat[::2]
# >>> ['color', 'style', 'debug']
flat[1::2]
# >>> ['red', 'striped', True]

dict(zip(flat[::2], flat[1::2]))
# >>> {'color': 'red', 'style': 'striped', 'debug': True}
```

Prefer approach to make an iterator and zip over it twice, no need to have
multiple lists.

```python
flat = ["color", "red", "style", "striped", "debug", True]
_iter = iter(flat)
dict(zip(_iter, _iter))
# >>> {'color': 'red', 'style': 'striped', 'debug': True}
```

- [Tweet status from @nedbat](https://twitter.com/nedbat/status/1542124221396144129)
- [Tweet reply from @1mikegrn](https://twitter.com/1mikegrn/status/1542147388810399745)

## Python Decorator Library

Outdated gallery with code pieces for Python decorator, but still a good
learning resource.

- [Python Decorator Library](https://wiki.python.org/moin/PythonDecoratorLibrary)

## Object inheritance influences match ordering sequence

Some interesting foot-gun case in Python's pattern match syntax. Order is
important.

```python
from dataclasses import dataclass

@dataclass
class Parent:
    x: int

@dataclass
class Child(Parent):
    y: int

def which(obj):
    match obj:
        case Parent(x):
            print("Parent:", x)
        case Child(x, y):
            print("Child:", x, y)

which(Parent(1))   # --> "Parent: 1"
which(Child(1, 2)) # --> "Parent: 1"
```

In the match statement the specialized subclass should be placed before the
generic base class.

Just as the specialized exceptions should be caught before the generic
Exception.

Exception handling follows similar rules. E.g. if you catch `OSError` before
`ConnectionError`, the `ConnectionError` case will never be hit.

- [Tweet status and replies from @dabeaz](https://twitter.com/dabeaz/status/1458181263257391104)

## `setattr`-series built-in functions cannot access private varialbe inside class

> Notice that code passed to `exec()` or `eval()` does not consider the
> classname of the invoking class to be the current class; this is similar to
> the effect of the `global` statement, the effect of which is likewise
> restricted to code that is byte-compiled together. The same restriction
> applies to `getattr()`, `setattr()` and `delattr()`, as well as when
> referencing `__dict__` directly.

This rule also should be considered inside class itself.

```python
class A:
    def __init__(self):
        setattr(self, '__private_var')
        # You cannot get a `self.__private_var` here even you
        # invoke `setattr` inside this class
```

- [9.6. Private Variables](https://docs.python.org/3/tutorial/classes.html#private-variables)

## 'No space left' raised from `multiprocessing`

```
OSError: [Errno 28] No space left on device
```

Ops, an critical exception raised from my parallel python codes. If you try to
use `df -h` to check disk usage but found everything is ok. Do not worry, it
doesn't stand your disk is almost full.

In most cases happended under `multiprocessing`, it says your shared memory
`/dev/shm` is no space left.

Try to check whether your shared data (like `multiprocessing.Array`) between
subprocesses is larger than your `/dev/shm` (from `df -h /dev/shm`). And may
also be propagated by too many semaphores allocated. Use the following cli

```shell
ipcs -u -c
```

to find how many semaphores are allocated when this happens.

Refs:

- [Github Issues - OSError: \[Errno 28\] No space left on device](https://github.com/psf/black/issues/1036)
- [No space left while using Multiprocessing.Array in shared memory](https://stackoverflow.com/questions/43573500/no-space-left-while-using-multiprocessing-array-in-shared-memory)

## Package binaries and other files with wheel format

If you ship python packages with `wheel` format, there is a special `.data`
directory strucutre to contain serveral auxiliary files.

```python
{
    'bindir': '$eprefix/bin',
    'sbindir': '$eprefix/sbin',
    'libexecdir': '$eprefix/libexec',
    'sysconfdir': '$prefix/etc',
    'sharedstatedir': '$prefix/com',
    'localstatedir': '$prefix/var',
    'libdir': '$eprefix/lib',
    'static_libdir': r'$prefix/lib',
    'includedir': '$prefix/include',
    'datarootdir': '$prefix/share',
    'datadir': '$datarootdir',
    'mandir': '$datarootdir/man',
    'infodir': '$datarootdir/info',
    'localedir': '$datarootdir/locale',
    'docdir': '$datarootdir/doc/$dist_name',
    'htmldir': '$docdir',
    'dvidir': '$docdir',
    'psdir': '$docdir',
    'pdfdir': '$docdir',
    'pkgdatadir': '$datadir/$dist_name'
}
```

For example, adding a cli entrypoint (in `setup.py`) could also be

```py
setup(
    data_files=[("bin", ["bin/you-cli"])],
)
```

instead of

```py
setup(
    entry_points={
        "console_scripts": ["app=app.cmd:app",],
    },
)
```

- [PEP 491 – The Wheel Binary Package Format 1.9](https://peps.python.org/pep-0491/#the-data-directory)
- [tensorchord/envd - fix: put the binary under bin directly](https://github.com/tensorchord/envd/pull/1254#issuecomment-1334902545)

## Different statistics styles of `stddev` function in numerical libraries

Different standard deviation in common numerical libraries

```python
# Population statistics style

## Numpy
import numpy as np
a = np.array([1., 2., 3.])
np.std(a)
# >>> 0.816496580927726

## Tensorflow
import tensorflow as tf
a = tf.convert_to_tensor([1., 2., 3.])
tf.math.reduce_std(a)
# >>> <tf.Tensor: shape=(), dtype=float32, numpy=0.8164966>

# Sample statistics style

## Torch
import torch
a = torch.tensor([1., 2., 3.])
torch.std(a)
# >>> tensor(1.)

## Pandas
import pandas as pd
a = pd.Series([1., 2., 3.])
a.std()
# >>> 1.0
```

The Bessel's correction is known as the unbiased variance (`n-1` in the
denominator)

```python
import torch
a = torch.tensor([1., 2., 3.])

torch.std(a, unbiased=True)  # default
# >>> tensor(1.)
torch.std(a, unbiased=False)  # default
# >>> tensor(0.8165)
```

- [Twitter status from Sebastian Raschka (@rasbt)](https://twitter.com/rasbt/status/1598324299034554368)

## What is the Python Buffer Protocol?

- [An Introduction to the Python Buffer Protocol](https://jakevdp.github.io/blog/2014/05/05/introduction-to-the-python-buffer-protocol/)
