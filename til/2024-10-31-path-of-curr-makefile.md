## Path of Current Makefile

```makefile
MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(patsubst %/,%,$(dir $(MKFILE_PATH)))
# version for relative dir path
# CURRENT_DIR := $(notdir $(patsubst %/,%,$(dir $(MKFILE_PATH))))
```

A note by @Brent Bradburn: To reference the _current_ makefile, the use of `$MAKEFILE_LIST` must precede any `include` operations (docs).

> `MAKEFILE_LIST`: Contains the name of each makefile that is parsed by `make`, in the order in which it was parsed. The name is appended just before `make` begins to parse the makefile. Thus, if the first thing a makefile does is examine the last word in this variable, it will be the name of the current makefile. Once the current makefile has used `include`, however, the last word will be the just-included makefile.

Refs:

1. [How to get current relative directory of your Makefile?](https://stackoverflow.com/questions/18136918/how-to-get-current-relative-directory-of-your-makefile)
2. [Current directory example in Makefile](https://gist.github.com/pyrsmk/8a476584dc4eb88a247b586955a982e1): Current directory example in Makefile.
3. [Make Manual - 6.14 Other Special Variables](https://www.gnu.org/software/make/manual/html_node/Special-Variables.html#index-makefiles_002c-and-MAKEFILE_005fLIST-variable)
