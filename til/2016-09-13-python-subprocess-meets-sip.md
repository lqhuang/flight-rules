---
title: When Python `subprocess` module meets macOS SIP
date: 2016-09-13
tags:
  - python
  - macos
---

当使用 `subprocess.Popen(command, shell=True)` 时

macOS 系统的 System Integrity Protection (SIP) 会导致 subprocess 无法得到正确的
环境变量。

```
dyld: Library not loaded:
```

> - https://support.apple.com/en-us/HT204899
>
> - http://www.macworld.com/article/2948140/os-x/private-i-el-capitans-system-integrity-protection-will-shift-utilities-functions.html

利用

```py
env = os.environ
subprocess.Popen(command, env=env, shell=True)
```

也无法解决。

`shell = False` 以后，Popen 的第一个参数应该是一个 args 的 list，可以利用 `shlex.split()` 来正确的分割 command。关于 `shell=False/True` 的问题可以看 Popen 的文档。

> Popen's first argument should be a list of args. Otherwise you're telling it
> to find an executable named strangely. You can use `shlex.split()` to split
> correctly

The correct way to call `Popen` is:

```py
Popen(shlex.split(command), shell=False, stdin=PIPE)
```

Further reading:

- [Popen docs](https://docs.python.org/2/library/subprocess.html#popen-constructor)
