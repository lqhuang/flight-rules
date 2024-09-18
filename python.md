---
title: Python Tips
created: 2019-01-01
updated: 2024-01-17
---

## Difference between `numpy.asarray` and `numpy.array`

The definition of asarray is:

```python
def asarray(a, dtype=None, order=None):
    return array(a, dtype, copy=False, order=order)
```

So it is like array, except it has fewer options, and `copy=False`. array has
`copy=True` by default.

The main difference is that array (by default) will make a copy of the object,
while asarray will not unless necessary.

ref:

- [What is the difference between np.array() and np.asarray()?](https://stackoverflow.com/questions/14415741/numpy-array-vs-asarray)

## 利用 Conda 在 64b-it 平台上创建 32-bit 的环境

通过环境变量(environmental variables)进行配置

    set CONDA_FORCE_32BIT=1
    conda create -n py27_32bit python=2.7

Refs:

1. [Conda is mixing 32-bit and 64-bit packages](https://github.com/conda/conda/issues/1744)
2. [using-multiple-python-engines-32bit-64bit](https://stackoverflow.com/questions/33709391/using-multiple-python-engines-32bit-64bit-and-2-7-3-5)

## Enable rasterized (光栅化) for matplotlib

Improve size of vector graphics (eg: svg, pdf, eps format)

```python
import pylab as py
arr = py.randn(100000, 2)
py.plot(arr[:,0], arr[:,1], 'o', alpha=0.1, rasterized=True)
py.savefig('dots.pdf', dpi=600)
```

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

1. [Axis line styles](https://matplotlib.org/stable/gallery/axisartist/demo_axisline_style.html)
2. [matplotlib axis arrow tip](https://stackoverflow.com/questions/33737736/matplotlib-axis-arrow-tip/33738359)
3. [How to make 'fuller' axis arrows with matplotlib](https://stackoverflow.com/questions/17646247/how-to-make-fuller-axis-arrows-with-matplotlib)

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

LMT is "local mean time"

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

> [Recommended change to enable conda in your shell](https://github.com/conda/conda/blob/master/CHANGELOG.md#440-2017-12-20)

## `CamelCase` to `camel_case`

Snippet to transform from camel case to snake case

```python
import re

name = 'CamelCaseName'
name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
print(name)  # camel_case_name
```

To handle more advanced cases specially (this is not reversible anymore):

```python
def camel_to_snake(name):
    name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()

print(camel_to_snake('camel2_camel2_case'))  # camel2_camel2_case
print(camel_to_snake('getHTTPResponseCode'))  # get_http_response_code
print(camel_to_snake('HTTPResponseCodeXYZ'))  # http_response_code_xyz
```

Snake case to pascal case

```python
name = 'snake_case_name'
name = ''.join(word.title() for word in name.split('_'))
print(name)  # SnakeCaseName
```

Ref:

1. [Elegant Python function to convert CamelCase to snake_case?](https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case)

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

```python
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

1. [Understanding `min_df` and `max_df` in scikit CountVectorizer](https://stackoverflow.com/questions/27697766/understanding-min-df-and-max-df-in-scikit-countvectorizer)

## Hidden variable in `dataclass`

Ref:

- [Python Data-Classes and pandas](https://github.com/sebastian-ahmed/python-etc/tree/main/dataclasses_pandas)

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

1. [Python Tips and Trick, You Haven't Already Seen](https://martinheinz.dev/blog/1)

## Subclass instance attribute in Pydantic (<2.0)

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

1. [多进程场景下, 必须用 if main](https://mp.weixin.qq.com/s?__biz=MzU0OTg3NzU2NA==&mid=2247489119&idx=1&sn=076b0eca8e538615973494a511669ae9&chksm=fba8740cccdffd1ac7b9a0accdcb9dbc190be17000ae1de20e95bc93d26bca59c1855d146c7e&mpshare=1&scene=1&srcid=1029DYm6Gav8PnGJMRyXAe2l&sharer_sharetime=1635489470168&sharer_shareid=a02c97b66753e49e61e3def16e4d4411&exportkey=ATmw3UkoaqFIE13cmYK%2FT18%3D&pass_ticket=R%2BX2oYnRuoXgxtQg6YovU2EyJ1pgYLZPRYAFRm7NjSc0ERiUZEHitsxXWluIPXtT&wx_header=0#rd)
2. [multiprocessing — Process-based parallelism](https://docs.python.org/3/library/multiprocessing.html)

## Find reverse dependency of one package

### From command line:

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

### Use Python script:

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

You can copy these and run with `python -c "..." package-name` fastly. Output
will be like:

```
['starlette', 'httpcore']
```

### Third packages

Use Python package `pip-tools` or
[`pipdeptree`](https://github.com/jazzband/pip-tools)

```shell
pipdeptree -r -p anyio

# anyio==3.5.0
#   - httpcore==0.14.3 [requires: anyio==3.*]
#     - httpx==0.21.1 [requires: httpcore>=0.14.0,<0.15.0]
#       - foam==0.3.0 [requires: httpx]
#   - starlette==0.16.0 [requires: anyio>=3.0.0,<4]
#     - fastapi==0.70.1 [requires: starlette==0.16.0]
#       - foam==0.3.0 [requires: fastapi]
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
all([True, False])  # False
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

**Update 2022-12-13**: A magic trick to use `getattr` and `setattr` for private
varialbe

```python
attr = f'_{self.__class__.__qualname__}__private_var'
val = getattr(self, attr)
setattr(self, attr, val)
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
    'static_libdir': '$prefix/lib',
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

## `side_effect` for `AsyncMock`

The result of `mock()` is an async function which will have the outcome of
`side_effect` or `return_value` after it has been awaited:

- if `side_effect` is a function, the async function will return the result of
  that function,
- if `side_effect` is an exception, the async function will raise the exception,
- if `side_effect` is an iterable, the async function will return the next value
  of the iterable, however, if the sequence of result is exhausted,
  `StopAsyncIteration` is raised immediately,
- if `side_effect` is not defined, the async function will return the value
  defined by `return_value`, hence, by default, the async function returns a new
  `AsyncMock` object.

Ref:
[unittest.mock — mock object library: `AsyncMock`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock)

## Less known magic functions

- `__length_hint__`:
  [PEP 424 – A method for exposing a length hint](https://peps.python.org/pep-0424/)
- `__getattribute__` vs `__getattr__`

> Final meta-programming related magic method we will try out is
> `__getattribute__`. This one looks very similar to the previous `__getattr__`.
> There's however a slight difference - as already mentioned `__getattr__` gets
> invoked only when attribute lookup fails, while `__getattribute__` is invoked
> _before_ attribute lookup is attempted.

- [Python Magic Methods You Haven't Heard About](https://martinheinz.dev/blog/87)

## `deque` cannot use index slice

```python
from collections import deque

d = deque(range(20))
# deque([0, 1, 2])

d[2:4]
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#     d[2:4]
# TypeError: sequence index must be integer, not 'slice'
```

The correct way is to use `islice` to make a lazy iterator.

```python
from itertools import islice

size = len(d)
it = islice(d, size - 10, size)

print(list(it))
# [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

print(list(d)[-10:])
# [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
```

And you should initiate an array by `np.fromiter(iterable, dtype=...)` from
`islice` (also other containers in `itertools`) instead of
`np.asarray()`/`np.array()`.

```python
print(np.asarray(it))
# <itertools.islice object at 0x7fad68bdd800>
print(np.fromiter(it, float))
# [10. 11. 12. 13. 14. 15. 16. 17. 18. 19.]
```

Ref:

- [How to slice a deque?](https://stackoverflow.com/questions/10003143/how-to-slice-a-deque)

## (draft) Cannot invoke `asyncio.get_event_loop().run_untile_complete(...)`

- https://stackoverflow.com/a/51342468
- https://discuss.python.org/t/supporting-asyncio-get-event-loop-run-until-complete-in-repls/5573/13
- https://stackoverflow.com/questions/46827007/runtimeerror-this-event-loop-is-already-running-in-python

## (draft) Unit test notes

1. AsyncMock only have `return_value` after `await`, but sometime, we won't
   `await` it
2. "TypeError: object AsyncMock can't be used in 'await' expression"

Ref: https://pytest-mock.readthedocs.io/en/latest/usage.html

## `fcntl` - the fcntl and ioctl system calls

Python has a std library to perform file control and I/O control on file
descriptors (for example, we could lock files exclusively). It is an interface
to the `fcntl()` and `ioctl()` **Unix** routines.

```python
fh = open("foobar.txt", "w")
fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fnctl.LOCK_NB)
```

- `LOCK_UN` – unlock
- `LOCK_SH` – acquire a shared lock
- `LOCK_EX` – acquire an exclusive lock

Ref:
[fcntl — The fcntl and ioctl system calls](https://docs.python.org/3/library/fcntl.html)

## Pylance and PEP 660 – Editable installs

When your project's building toolchain switch to `pyproject.toml` based, Pylance
(PyRight) cannot normally recognize your "editable" install
(`pip install -e .`). The error hint looks like

```
Import "xxx" coulde not be resolved. Pylance (reportMissingImports)
```

There are three mechanisms now for "Editable Installs":

1. `PEP 660`: using import hooks to direct the import machinery to the package's
   source files
2. `compat` mode: create a special `.pth` file in the target directory
3. `strict` mode: create a tree of file links in an auxiliary directory by using
   symlinks

For `pip` + `setuptools` toolchain, you could switch to `strict`/`compat` mode
while using development mode

```sh
pip install -e . --config-settings editable_mode=strict
```

For `Hatch/Hatchling` or `PDM`, both of them use `.pth` files by default
(identifiable by Pylance). Only use import hooks (PEP 660) if:

- `Hatch/Hatchling`: set `dev-mode-exact` to `true`
- `PDM`: set `editable-backend` to `"editables"`.

Refs:

- [PyLance not recognizing imports from PEP-660 editable installs #3473](https://github.com/microsoft/pylance-release/issues/3473)
- [PEP 660 – Editable installs for pyproject.toml based builds (wheel based)](https://peps.python.org/pep-0660)
- [Development Mode - "Strict" editable installs](https://setuptools.pypa.io/en/latest/userguide/development_mode.html#strict-editable-installs)
- [pylance-release/TROUBLESHOOTING.md#Editable install modules not found](https://github.com/microsoft/pylance-release/blob/main/TROUBLESHOOTING.md#editable-install-modules-not-found)

## Use `conda` to install specific BUILD of a package

The way you install any specific version from that information is:

```sh
conda install pillow=4.2.1=py27h7cd2321_0
# conda install <package_name>=<version>=<build_string>
```

The `pillow` package has a version of `4.2.1`, and a build of `py27h7cd2321_0`.

Besides, it supports `*` as a wildcard like following:

```sh
conda install 'pillow==4.2.1=py27*'
```

Refs:

- [Installing specific BUILD of an anaconda package](https://stackoverflow.com/questions/48128029/installing-specific-build-of-an-anaconda-package)

## Custom flag to override CUDA version by `conda`

> As an effort to maximize accessibility for users with lower connection and/or
> storage bandwidth, there is an ongoing effort to limit installing packages
> compiled for GPUs unnecessarily on CPU-only machines by default. This is
> accomplished by adding a run dependency, `__cuda`, that detects if the local
> machine has a GPU. However, this introduces challenges to users who may prefer
> to still download and use GPU-enabled packages even on a non-GPU machine.

Interesting case:

> For example, login nodes on HPCs often do not have GPUs and their compute
> counterparts with GPUs often do not have internet access. In this case, a user
> can override the default setting via the environment variable
> `CONDA_OVERRIDE_CUDA` to install GPU packages on the login node to be used
> later on the compute node.

> In order to override the default behavior, a user can set the environment
> variable `CONDA_OVERRIDE_CUDA` like below to install TensorFlow with GPU
> support even on a machine with CPU only.
>
> ```sh
> CONDA_OVERRIDE_CUDA="11.2" conda install "tensorflow==2.7.0=cuda112*" -c conda-forge
> ```

- [conda-forge » User Documentation » Tips & tricks](https://conda-forge.org/docs/user/tipsandtricks.html)

## Hint on execute order of decorators

Execution order of decorators in Python sometimes is confused.

```python
@decorator_outer
@decorator_inner
def func():
    ...

# totally equivalent to
decorator_outer(decorator_inner(func))()
```

at the first sight, the execution order is: `decorator_inner` ->
`decorator_outer` -> `func`

But it actually depends on where you place your logic codes inside or outside of
wrapper in decorator.

```python
def decorator_outer(func):
    print("seq 3: Here is executed after inner decorator")

    def wrapper():
        print("seq 5: belong to outer decorator, before `func()`")
        func()
        print("seq 8: belong to outer decorator, after `func()`")

    print("seq 4: Cleanup step for outer decorator")
    return wrapper


def decorator_inner(func):
    print("seq 1: Here is the closest postion to the wrapped function")

    def wrapper():
        print("seq 6: belong to inner decorator, before `func()`")
        func()
        print("seq 7: belong to inner decorator, after `func()`")

    print("seq 2: after wrapper is defined. use for cleanup or something")
    return wrapper


@decorator_outer
@decorator_inner
def func():
    print("* Real function call")


if __name__ == "__main__":
    func()
```

Output will be

```
seq 1: Here is the closest postion to the wrapped function
seq 2: after wrapper is defined. use for cleanup or something
seq 3: Here is executed after inner decorator
seq 4: Cleanup step for outer decorator
seq 5: belong to outer decorator, before `func()`
seq 6: belong to inner decorator, before `func()`
* Real function call
seq 7: belong to inner decorator, after `func()`
seq 8: belong to outer decorator, after `func()`
```

More precisely,

- the code **outside** of wrapper in decorator
  - the inner decorator will complete execution **before** the outer decorator
  - execution affinity: from the nearest to the farthest
  - except `wrapper`, all codes will be pre-executed in sequencely.
- the code **inside** of wrapper in decorator
  - the inner decorator will complete execution **after** the outer decorator
  - execution affinity: from the farthest to the nearest
  - codes before/after real wrapped function follow the FIFO execution order.

For example, in FastAPI or Flask, it's very common to use decorator to do user
authentication and permission control. So, if you put your extended logic inside
of wrapper, you have to carefully note the sequence of decorator

```python
def check_login(func):
    """Check login"""
    def wrapper(*args, **kwargs):
        is_login = False
        if not is_login:
            return {'success': False, "msg": "Not logged in yet"}
        return func(*args, **kwargs)
    return wrapper


def check_data_set_permission(func):
    """Check role and data permission for logged user"""
    def wrapper(*args, **kwargs):
        has_data_set_permission = True
        if not has_data_set_permission:
            return {'success': False, "msg": "No data permission"}
        return func(*args, **kwargs)
    return wrapper
```

Obviously, A user must be logged in already before checking its data accessing
permission. The entrypoint would be like

```python
# bad case
@check_data_set_permission
@check_login
def do_query_dataset(dataset_id):
    ...

# good case
@check_login
@check_data_set_permission
def do_query_dataset(dataset_id):
    ...
```

Refs:

- [Python 装饰器的执行顺序](https://mp.weixin.qq.com/s/PXu-68puFUpxzJRqUHJwBw)

## reduced condas index fetch bandwidth

> The new conda 23.3.1 release from Mar, 2023, by enabling the
> `experimental: ["jlap"]` feature in `.condarc`, conda users can see more than
> a 99% reduction in index fetch bandwith.

```yaml
experimental: ["jlap"]
# flag `jlap`: conda 23.3.1 release from March, 2023
```

Refs:

- [How we reduced conda’s index fetch bandwidth by 99%](https://conda.discourse.group/t/how-we-reduced-condas-index-fetch-bandwidth-by-99/257)

## Faster page iterator / chunk / partition in Python

TIL, Anton posts a article about how to implement a faster page iterator in
Python, sometimes also known as `chunk` or `partition` in other third libraries
like `PyFunctional`, `toolz` and `more-itertools`.

By learning his post, I just realized that `iter` has an alternative function
signature `iter(object, sentinel)`

> Signatures of built-in `iter` function:
>
> - `iter(object)`
> - `iter(object, sentinel)`
>
> If the second argument, `sentinel`, is given, then object must be a callable
> `object`. The iterator created in this case will call `object` with no
> arguments for each call to its `__next__()` method; if the value returned is
> equal to sentinel, `StopIteration` will be raised, otherwise the value will be
> returned.

I also did some benchmark on different implementations of page iterator. Check
codes in [bench_page_iterator.py](./snippets/bench_page_iterator.py). And the
results is here:

```
One-by-one (baseline): 809 ms
Use `append()` to fill page: 942 ms
Use fixed-size page: 792 ms
Use islice: 451 ms
Use islice + plain sentinel: 453 ms
Use `partition` package `toolz`: 429 ms
Use `partition_all` package `toolz`: 431 ms
Use `chunked` from package `more-itertools`: 459 ms
Use `ichunked` from package `more-itertools`: 1648 ms
Use `grouped` from package `PyFunctional`: 464 ms
```

Refs:

- [Page iterator in Python by Anton Zhiyanov](https://antonz.org/page-iterator/)
- [Built-in Functions - `iter`](https://docs.python.org/3/library/itertools.html#itertools.islice)

## Cache dir for `pip`

You can use `pip cache dir` (new in version 20.1) to get the cache directory
that pip is currently configured to use.

Default paths:

- Linux: `~/.cache/pip` and it also respects the `XDG_CACHE_HOME` directory.
- MacOS: `~/Library/Caches/pip`
- Windows: `%LocalAppData%\pip\Cache`

For example, mount a volume to cache dir in Docker (Linux based)

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip pip install ...
```

And

- `pip cache info` provides an overview of the contents of pip’s cache, such as
  the total size and location of various parts of it.
- `pip cache purge` will clear all wheel files from pip’s cache.
- `pip cache list` will list all wheel files from pip’s cache.
- pip’s caching behaviour is disabled by passing the `--no-cache-dir` option.

Ref:

1. [Where is the cache stored](https://pip.pypa.io/en/stable/topics/caching/)

## Useful `pip` options for package management in Docker

While using `pip` to install packages in Docker, there are warnings to remind
you're in dangerous with root permissions. Here are some useful options to
suppress them.

- `--break-system-packages`: Allow pip to modify an EXTERNALLY-MANAGED Python
  installation. Do not recommend in the most cases.
- `--root-user-action`: Action if pip is run as a root user. By default, a
  warning message is shown. Options: ("warn", "ignore")
- `--no-warn-script-location`: Do not warn when installing scripts outside
  `$PATH`
- pip’s command line options can be set with environment variables using the
  format `PIP_<UPPER_LONG_NAME>`. Dashes (`-`) have to be replaced with
  underscores (`_`).
  - `PIP_ROOT_USER_ACTION=ignore` is the same as `--root-user-action=ignore`

Refs:

1. [pip documentation -- pip install](https://pip.pypa.io/en/stable/cli/pip_install/)

## `decimal` and `fractions` for advanced arithmetic

- `decimal`: precise arithmetic with decimal numbers
- `fractions`: support for rational number arithmetic

### Decimal

```python-repl
>>> from decimal import Decimal
>>> 0.1 + 0.2 == 0.3
False
>>> Decimal('0.1') + Decimal('0.2') == Decimal('0.3')
True
```

We can control many aspects of a Decimal number, like, for instance, the
precision:

```
from decimal import localcontext

with localcontext(prec=42) as ctx:
    s = calculate_something()
```

The `getcontext()` and `setcontext()` function accesses a different `Context`
object for each thread (usually current thread).

And if you want to control the defaults so that each thread will use the same
values throughout the application, directly modify the `DefaultContext` object.
This should be done _before_ any threads are started.

- [Python 3 Docs: decimal — Decimal fixed point and floating point arithmetic](https://docs.python.org/3/library/decimal.html)
- [Python 3 Docs: decimal - Working with threads](https://docs.python.org/3/library/decimal.html#working-with-threads)

## Fractions

```python-repl
>>> from fractions import Fraction
>>> f = Fraction(1, 3)
>>> f.numerator
1
>>> f.denominator
3
>>> Fraction('1/3')
Fraction(1, 3)
>>> Fraction('-.125')
Fraction(-1, 8)
```

There are other ways of building fractions, although using `float` and `Decimal`
may lose precision:

```python-repl
>>> Fraction(1/3)
Fraction(6004799503160661, 18014398509481984)
>>> Fraction(Decimal('1') / Decimal('3'))
Fraction(3333333333333333333333333333, 10000000000000000000000000000)
```

### Refs

- [Understanding Numeric Data Types in Python](https://fullspeedpython.com/articles/understanding-numeric-data-types/)
- [PEP 3141 – A Type Hierarchy for Numbers](https://peps.python.org/pep-3141/)

## Some corner cases for Python string interpolation

- [聊一聊 Python 的换行以及转义 (Chinese)](https://mp.weixin.qq.com/s/eR34xJYpKEeUEO7J_76X3A)

## Real application for pattern matching

### Cases from PEP 0636

This will match any sequences having `"drop"` as its first elements. All
remaining elements will be captured in a `list` object which will be bound to
the `objects` variable.

This syntax has similar restrictions as sequence unpacking: you can not have
more than one starred name in a pattern.

```python
match command.split():
    case ["drop", *objects]:
        for obj in objects:
            character.drop(obj, current_room)
```

Capturing matched sub-patterns. The first version of our `"go"` command was
written with a `["go", direction]` pattern. This leads to some code duplication,
but at the same time we get better input validation, and we will not be getting
into that branch if the command entered by the user is `"go figure!"` instead of
a direction. We could try to get the best of both worlds doing the following
(I’ll omit the aliased version without `"go"` for brevity):

```python
match command.split():
    case ["go", ("north" | "south" | "east" | "west") as direction]:
        current_room = current_room.neighbor(direction)
```

This code is a single branch, and it verifies that the word after `"go"` is
really a direction. What we need is a pattern that behaves like the or pattern
but at the same time does a capture. We can do so with an as pattern. The
as-pattern matches whatever pattern is on its left-hand side, but also binds the
value to a name.

```python
match command.split():
    case ["go", ("north" | "south" | "east" | "west") as direction]:
        current_room = current_room.neighbor(direction)
```

Adding conditions to patterns. Guards consist of the `if` keyword followed by
any expression

```python
match command.split():
    case ["go", direction] if direction in current_room.exits:
        current_room = current_room.neighbor(direction)
    case ["go", _]:
        print("Sorry, you can't go that way")
```

Matching objects. The resulting object `event.get()` can have different type and
attributes according to the user action. Rather than writing multiple
`isinstance()` checks, you can use patterns to recognize different kinds of
objects, and also apply patterns to its attributes:

```python
match event.get():
    case Click(position=(x, y)):
        handle_click_at(x, y)
    case KeyPress(key_name="Q") | Quit():
        game.quit()
    case KeyPress(key_name="up arrow"):
        game.go_north()
    ...
    case KeyPress():
        pass # Ignore other keystrokes
    case other_event:
        raise ValueError(f"Unrecognized event: {other_event}")
```

A pattern like `Click(position=(x, y))` only matches if the type of the event is
a subclass of the `Click` class. It will also require that the event has a
`position` attribute that matches the `(x, y)` pattern. If there’s a match, the
locals x and y will get the expected values.

A pattern like `KeyPress()`, with no arguments will match any object which is an
instance of the `KeyPress` class. Only the attributes you specify in the pattern
are matched, and any other attributes are ignored.

Matching positional attributes. The `__match_args__` special attribute defines
an explicit order for your attributes that can be used in patterns like
`case Click((x,y))`. The `(x, y)` pattern will be automatically matched against
the `position` attribute, because the first argument in the pattern corresponds
to the first attribute in your class definition.

```python
class Click:
    __match_args__ = ("position", "button")
    def __init__(self, pos, btn):
        self.position = pos
        self.button = btn
        ...

match event.get():
    case Click((x, y)):
        handle_click_at(x, y)
```

Going to the cloud: Mappings. Via the `json` module, those will be mapped to
Python dictionaries, lists and other builtin objects.

The keys in your mapping pattern need to be literals, but the values can be any
pattern. As in sequence patterns, all subpatterns have to match for the general
pattern to match.

You can use `**rest` within a mapping pattern to capture additional keys in the
subject. Note that if you omit this, extra keys in the subject will be ignored
while matching, i.e. the message
`{"text": "foo", "color": "red", "style": "bold"}` will match the first pattern
in the example above.

```python
for action in actions:
    match action:
        case {"text": message, "color": c}:
            ui.set_text_color(c)
            ui.display(message)
        case {"sleep": duration}:
            ui.wait(duration)
        case {"sound": url, "format": "ogg"}:
            ui.play(url)
        case {"sound": _, "format": _}:
            warning("Unsupported audio format")
```

Matching builtin classes. The code above could use some validation. Given that
messages came from an external source, the types of the field could be wrong,
leading to bugs or security issues.

Any class is a valid match target, and that includes built-in classes like
`bool`, `str` or `int`. That allows us to combine the code above with a class
pattern. So instead of writing `{"text": message, "color": c}` we can use
`{"text": str() as message, "color": str() as c}` to ensure that message and c
are both strings. For many builtin classes (see PEP 634 [^pep-0634] for the
whole list), you can use a positional parameter as a shorthand, writing `str(c)`
rather than `str() as c`. The fully rewritten version looks like this:

```python
for action in actions:
    match action:
        case {"text": str(message), "color": str(c)}:
            ui.set_text_color(c)
            ui.display(message)
        case {"sleep": float(duration)}:
            ui.wait(duration)
        case {"sound": str(url), "format": "ogg"}:
            ui.play(url)
        case {"sound": _, "format": _}:
            warning("Unsupported audio format")
```

- [^pep-0636][PEP 636 – Structural Pattern Matching: Tutorial](https://peps.python.org/pep-0636/)
- [^pep-0634][PEP 634 – Structural Pattern Matching: Specification](https://peps.python.org/pep-0634/)

### Cases from @netbat

Check the structure or the fields of dictionary. Hand-writing these sorts of
checks might result in shorter bytecode. But the Python code would be twistier
and harder to get right.

```python
match event:
    case {
        "issue": {"closed_at": closed},
        "comment": {"created_at": commented},
        } if closed == commented:
        # This is a "Close with comment" comment. Don't do anything for the
        # comment, because we'll also get a "pull request closed" event at
        # the same time, and it will do whatever we need.
        pass

    case {"sender": {"login": who}} if who == get_bot_username():
        # When the bot comments on a pull request, it causes an event, which
        # gets sent to webhooks, including us.  We don't have to do anything
        # for our own comment events.
        pass

    case {"issue": {"pull_request": _}}:
        # The comment is on a pull request. Process it.
        return process_pull_request_comment(event)
```

An interesting use of match is matching on types, which is nicer than isinstance
checks:

```py
match obj:
    case int(0): ...   # special case for 0
    case int(): ...    # any other int
    case float(): ...  # any float
    case _:            # anything else
```

- [^nedbat-matchcase][Real-world match/case](https://nedbatchelder.com/blog/202312/realworld_matchcase.html)

## Using `for-else` to track variables during loops

Usually, we use flag variable to track if found something in loops.

```python
found = False
for f in flowers:
    if f.endswith("z"):
        found = True
        print("Found it!")
        break

if not found:
    print("Not found :(")
```

We probably knew there is keyword `else` for `while` and `for`, but seldom use
it in real word. What's effect of `else` with `while` and `for`? It's activated
if the loop **never reached** `break`.

Hence, the above codes could simplify to

```python
for f in flowers:
    if f.endswith("z"):
        print("Found it!")
        break
else:
    print("Not found :(")
```

But I don't suggest still using flag varibale in the above codes:

```python
for f in flowers:
    if f.endswith("z"):
        print("Found it!")
        break
else:
    found = False  # `found` will become an unbound variable.
    print("Not found :(")
```

Refs:

- [You don't need this in Python](https://www.bitecode.dev/i/139716011/do-not-track)

### Send HTTP requests using python-requests with timeout, session reuse and retry

```python
from requests.adapters import HTTPAdapter, Retry
from requests import Session

retries = Retry(
  total=5, backoff_factor=1, status_forcelist=[502, 503, 504]
)
session = Session()  # reuse tcp connection
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

session.get("https://example.com", timeout=5)  # seconds
```

Ref:

- [GitHub Gist: Send HTTP requests using python-requests with timeout, tcp reuse(session) and retry.](https://gist.github.com/laixintao/e9eae48a835e741969ae06af3ad45f71)

## CPU Count

- affinity: the number of CPUs that a process is bound to
  - not applied in BSD systems
- multiprocessing: `multiprocessing.cpu_count()`
- joblib: `joblib.cpu_count(only_physical_cores=False)`
- psutil: `psutil.cpu_count(logical=True)`
- os: `os.cpu_count()`
- torch
  - `torch.get_num_threads()`
  - `torch.get_num_interop_threads()`

## Threads Config for Numpy

The following environment variables could affect to the real threads used by
numpy when computing.

```
OMP_NUM_THREADS: openmp,
OPENBLAS_NUM_THREADS: openblas,
MKL_NUM_THREADS: mkl,
VECLIB_MAXIMUM_THREADS: accelerate,
NUMEXPR_NUM_THREADS: numexpr
```

Luckily, it now could be set after numpy imported.

Besides above envs, I will recommend `threadpoolctl` to control parallel
behaviors of numpy.

- [Limit number of threads in numpy](https://stackoverflow.com/a/53224849)
- [joblib/threadpoolctl](https://github.com/joblib/threadpoolctl): Python
  helpers to limit the number of threads used in native libraries that handle
  their own internal threadpool (BLAS and OpenMP implementations)
- [Set number of threads after numpy import](https://github.com/numpy/numpy/issues/11826)

## Check devices in JAX

```python
import jax
jax.default_backend()
# JAX defaults to a GPU or TPU if you have one.
# So you can just check it doesn't return "cpu".

jax.local_device_count()
```

- [google/jax/issues/971: how to detect if GPU is being used? (feature request)](https://github.com/google/jax/issues/971)

## Treads in Jax

- https://github.com/google/jax/issues/1539
- https://github.com/google/jax/issues/743
- https://github.com/google/jax/issues/743
- https://github.com/google/jax/issues/6790
- https://github.com/joblib/threadpoolctl/issues/127
- https://bnikolic.co.uk/blog/python/jax/2023/03/22/jax-multithreaded.html
- https://stackoverflow.com/questions/72328521/jax-pmap-with-multi-core-cpu
