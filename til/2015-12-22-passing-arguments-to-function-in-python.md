---
title: Python 函数的四种参数传递方式
created: 2015-12-22
updated: 2024-05-22
tags:
  - Python
draft: true
---

Python 中函数传递参数有四种形式

```python
func1(a, b, c)
func2(a=1, b=2, c=3)
func3(*args)
func4(**kargs)
```

第一种 `func1(a, b, c)` 是直接将实参赋予形参, 根据位置做匹配, 即严格要求实参的数
量与形参的数量位置相等.

第二种 `func2(a=1, b=2, c=3)` 根据键值对的形式做实参与形参的匹配, 通过这种式就可
以忽略了参数的位置关系, 直接根据关键字来进行赋值, 同时该种传参方式还有个好处就是
可以在调用函数的时候作为个别选填项, 不要求数量上的相等, 即可以 `func2(3, 4)` 来
调用 `func2` 函数, 这里关键就是前面的 3, 4 覆盖了原来 `a`, `b` 两个形参的值, 但
`c` 还是不变采用原来的默认值 3, 这种模式相较第一种更加灵活, 不仅可以通过
`func2(c=5, a=2, b=7)` 来打乱形参的位置, 而且可以在但没有对应形参传递的时候常用
定义函数时的默认值.

第三种 `func3(*args)`, 这传参方式是可以传入任意个参数, 这些若干参数都被放到了
Tuple 元组中赋值给形参 `args`, 之后要在函数中使用这些形参, 直接操作 `args` 这个
Tuple 元组就可以了, 这样的好处是在参数的数量上没有了限制, 但是因为是 Tuple, 其本
身还是有次序的.

第四种 `func4(**kargs)`最为灵活, 其是以键值对字典的形式向函数传参, 含有第二种位
置的灵活的同时具有第三种方式的数量上的无限制.

最后要强调的是四种传递方式混合使用, `func5(arg, args=value, *args, **kargs)`, 但
四种方式混用时要遵守：

- `args=value` 需在 `arg` 之后
- `*args` 需在 `args=value` 之后
- `**kargs` 需在 `*args` 之后

赋值过程为

1. 按顺序把传给 `args` 的实参赋值给对应的形参
2. `args=value` 形式的实参赋值给形参
3. 将多余出的即键值对行后的零散实参打包组成一个 Tuple 传递给 `*args`
4. 将多余的 `key=value` 形式的实参打包正一个 dicrionary 传递给 `**kargs`

Refs:

1. [python 函数的四种参数传递方式](https://lazybios.com/2013/04/four-kinds-of-function-argment-pass-in-python/)
2. https://twitter.com/mathsppblog/status/1588589939100241920
3. https://neuronize.dev/mastering-python-function-arguments-a-comprehensive-guide
