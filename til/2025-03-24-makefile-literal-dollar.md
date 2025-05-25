---
title: 'Using a `$` literal in Makefile'
date: 2025-03-24
tags:
  - til
  - makefile
---

What if you want to use a literal `$` in Makefile? For example, you want to use literally `/path/to/${HOME}`.

Use `$$` to escape the `$` character, like this:

```makefile
path = /path/to/$$HOME
```

Ref

- [makefile - Using a $ literal in a GNU Makefile path - Stack Overflow](https://stackoverflow.com/questions/18143805/using-a-literal-in-a-gnumakefile-path)
