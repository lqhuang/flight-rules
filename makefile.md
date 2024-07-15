---
title: Makefile Tips
created: 2023-12-06
updated: 2024-07-15
---

## Resources

- [Overview of `make`](https://www.gnu.org/software/make/manual/make.html#Overview)
- [Makefile Tutorials](https://makefiletutorial.com): Learn Makefiles With the
  tastiest examples
- [跟我一起写 Makefile by @haoel](https://seisman.github.io/how-to-write-makefile/index.html)

## Sensible defaults

```makefile
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

# .ONESHELL:
.DELETE_ON_ERROR:

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
```

First two lines are trying to always use a recnent bash in strict mode.

- `.ONESHELL` ensures each Make recipe is ran as one single shell session,
  rather than one new shell per line. **Warning**: If the `.ONESHELL` special
  target appears anywhere in the makefile then all recipe lines for each target
  will be provided to a single invocation of the shell.
- `.DELETE_ON_ERROR` does what it says on the box - if a Make rule fails, it’s
  target file is deleted. This ensures the next time you run Make, it’ll
  properly re-run the failed rule, and guards against broken files. This will
  happen for all targets, not just the one it is before like PHONY. It's a good
  idea to always use this, even though make does not for historical reasons.
- `MAKEFLAGS += --warn-undefined-variables`: This does what it says on the tin -
  if you are referring to Make variables that don’t exist, that’s probably wrong
  and it’s good to get a warning.
- `MAKEFLAGS += --no-builtin-rules`: This disables the bewildering array of
  built in rules to automatically build Yacc grammars out of your data if you
  accidentally add the wrong file suffix. Remove magic, don’t do things unless I
  tell you to, Make.

References:

1. [Your Makefiles are wrong](https://tech.davis-hansson.com/p/make/)
2. [Use Bash Strict Mode (Unless You Love Debugging)](http://redsymbol.net/articles/unofficial-bash-strict-mode/)
3. [10.2 Catalogue of Built-In Rules](https://www.gnu.org/software/make/manual/html_node/Catalogue-of-Rules.html)

## The phases when make run

1. 读入所有的 `Makefile。`
2. 读入被 `include` 的其它 `Makefile。`
3. 初始化文件中的变量。
4. 推导隐式规则，并分析所有规则。
5. 为所有的目标文件创建依赖关系链。
6. 根据依赖关系，决定哪些目标要重新生成。
7. 执行生成命令。

1-5 步为第一个阶段，6-7 为第二个阶段。第一个阶段中，如果定义的变量被使用了，那么
，make 会把其展开在使用的位置。但 make 并不会完全马上展开，make 使用的是拖延战术
，如果变量出现在依赖关系的规则中，那么仅当这条依赖被决定要使用了，变量才会在其内
部展开。

## Makefile doesn't always require recipe line must start with tab

Config `.RECIPEPREFIX` to use other character instead of tab.

```makefile
ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >
```

With this change, a makefile that previously looked like this:

```makefile
hello:
	echo "Hello"
	echo "world"
```

Would look like:

```makefile
hello:
> echo "Hello"
> echo "world"
```

They're totally equivalent.

References:

- [Your Makefiles are wrong](https://tech.davis-hansson.com/p/make/)

## `if-else` pattern in Makefile

Two ways to do if-else pattern in Makefile (looping is very similar):

1. Use `ifeq` and `endif` by Makefile condition syntax
   ```
   conditional-directive-one
   text-if-one-is-true
   else conditional-directive-two
   text-if-two-is-true
   else
   text-if-one-and-two-are-false
   endif
   ```
2. Use `$(if condition,then-part[,else-part])` function for conditionals.
   - If the condition is true then the second argument, `then-part`, is
     evaluated and this is used as the result of the evaluation of the entire if
     function.
   - If the condition is false then the third argument, `else-part`, is
     evaluated and this is the result of the if function.
   - If there is no third argument, the if function evaluates to nothing (the
     empty string).
   - Note that only one of the `then-part` or the `else-part` will be evaluated,
     **never both**. Thus, either can contain side-effects (such as shell
     function calls, etc.)
3. One line `if-else` by Shell script

Refs:

- [Basic if else statement in Makefile](https://stackoverflow.com/questions/58602758/basic-if-else-statement-in-makefile)
- [Makefile looping files with pattern](https://unix.stackexchange.com/questions/347032/makefile-looping-files-with-pattern)
- [Make manual - 7.2 Syntax of Conditionals](https://www.gnu.org/software/make/manual/html_node/Conditional-Syntax.html)
- [Make manual - 8.4 Functions for Conditionals](https://www.gnu.org/software/make/manual/html_node/Conditional-Functions.html)

## First target/goal is the default

Set a default target probably is a good practice. It makes the Makefile more
intuitive by just running `make` to know what would happen.

> By default, make starts with the first target (not targets whose names start
> with `.` unless they also contain one or more `/`).

> By default, the goal is the first target in the makefile (not counting targets
> that start with a period). Therefore, makefiles are usually written so that
> the first target is for compiling the entire program or programs they
> describe. If the first rule in the makefile has several targets, only the
> first target in the rule becomes the default goal, not the whole list. You can
> manage the selection of the default goal from within your makefile using the
> `.DEFAULT_GOAL` variable (see Other Special Variables).

```makefile
# a typical Makefile

.PHONY: help
help:
	@echo "I'm the first target, so I'm the default goal"

whatever_next:
	@echo "..."
```

```makefile
.DEFAULT_GOAL := help

whatever_first:
	@echo "..."

.PHONY: help
help:
	@echo "I'm specified by `.DEFAULT_GOAL`, so I'm the default goal"
```

The above two Makefiles are equivalent that target `help` is the default goal
while running just `make`.

References:

1. [GNU MAKE Manual: 9.2 Arguments to Specify the Goals](https://www.gnu.org/software/make/manual/html_node/Goals.html)
2. [GNU MAKE Manual: 2.3 How make Processes a Makefile](https://www.gnu.org/software/make/manual/html_node/How-Make-Works.html)

## Include other Makefiles

```makefile
include $(wildcard *.mk)
```

Reference:

- I don't know ... Copilot autofilled itself ... It's correct , so I just keep
  it.

## Use `$(shell ...)` to run shell commands

```makefile
# get the current git branch
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
# get the current git commit hash
COMMIT := $(shell git rev-parse --short HEAD)
# get the current git tag
```

## Check if a command exists

```makefile
# check if a command exists
HAS_FOO := $(shell command -v foo 2> /dev/null)
HAS_BAR := $(shell command -v bar 2> /dev/null)
HAS_BAZ := $(shell command -v baz 2> /dev/null)
```

```makefile
tools := hugo terraform aws exiftool jpegoptim optipng mogrify
$(tools):
	@which $@ > /dev/null

.PHONY: serve
serve: hugo
	$(HUGO) server -D

.PHONY: validate
validate: terraform
	$(TERRAFORM) validate
```

- [StackOverflow - Check if a program exists from a Makefile](https://stackoverflow.com/questions/5618615/check-if-a-program-exists-from-a-makefile)
- [Check if a program exists from a Makefile](https://how.wtf/check-if-a-program-exists-from-a-makefile.html)

## Variables expansion in Makefile

> There are different ways that a variable in GNU `make` can get a value; we
> call them the _flavors_ of variables. The flavors are distinguished in how
> they handle the values they are assigned in the makefile, and in how those
> values are managed when the variable is later used and expanded.

- Recursively Expanded Variable Assignment: only looks for the variables when
  the command is used, not when it's defined.
  - `FOO = bar`
  - `FOO ?= bar`
  - `FOO += bar`
- Simply Expanded Variable Assignment: like normal imperative programming --
  only those defined so far get expanded
  - `FOO := bar`
  - `FOO ::= bar`
  - `FOO += bar`
- Immediately Expanded Variable Assignment
  - `FOO :::= bar`
- Conditional Variable Assignment
  - `FOO ?= bar`

```makefile
# Variable Assignment
FOO ?= bar
# is exactly equivalent to this
ifeq ($(origin FOO), undefined)
    FOO = bar
endif
```

- [Make manual - 6.2 The Two Flavors of Variables](https://www.gnu.org/software/make/manual/html_node/Flavors.html)

## Variables defined in `:=` will be expanded immediately when the Makefile is read

including Target-specific variable

```makefile
VARIABLE := $(shell sleep 1; echo "hello")

tar: TMP1 := $(shell sleep 5)
	@echo "so long time"

tar: TMP2 := $(shell sleep 10)

# Example of target variables for pattern rules
#%.c: ONE_VAR = cool
```

According to the manual, variable definitions are parsed as follows:

```makefile
immediate = deferred
immediate ?= deferred
immediate := immediate
immediate ::= immediate
immediate :::= immediate-with-escape
immediate += deferred or immediate
# NOTE: `+=` depends varables where it is defined yet an how it be defined.
immediate != immediate

define immediate
  deferred
endef

...

define immediate :=
  immediate
endef

...
# Check manual for more details about `define` way
```

> [!NOTE]
>
> For the append operator `+=`, the right-hand side is considered immediate if
> the variable was previously set as a simple variable (`:=` or `::=`), and
> deferred otherwise.

But there is a special case for imedate variable defined in target-specific.

A rule is always expanded the same way, regardless of the form:

```
immediate : immediate ; deferred
        deferred
```

That is, the target and prerequisite sections are expanded immediately, and the
recipe used to build the target is always deferred. This is true for explicit
rules, pattern rules, suffix rules, static pattern rules, and simple
prerequisite definitions.

- [Make manual: 3.7 How make Reads a Makefile](https://www.gnu.org/software/make/manual/html_node/Reading-Makefiles.html)

## Automatic Variables

```makefile
hey: one two
	# Outputs "hey", since this is the target name
	echo $@

	# Outputs all prerequisites newer than the target
	echo $?

	# Outputs all prerequisites
	echo $^

	touch hey

one:
	touch one

two:
	touch two

clean:
	rm -f hey one two
```

- [Makefile Tutorial: Automatic Variables](https://makefiletutorial.com/#automatic-variables-and-wildcards)
- [Make manual - 10.5.3 Automatic Variables](https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html)

## Pattern rules and filter to group commands

```makefile
objects = main.o kbd.o command.o display.o \
          insert.o search.o files.o utils.o

edit : $(objects)
	cc -o edit $(objects)

main.o : defs.h
kbd.o : defs.h command.h
command.o : defs.h command.h
display.o : defs.h buffer.h
insert.o : defs.h buffer.h
search.o : defs.h buffer.h
files.o : defs.h buffer.h command.h
utils.o : defs.h

.PHONY : clean
clean :
	-rm edit $(objects)
```

In this style of makefile, you group entries by their prerequisites instead of
by their targets. Here is what one looks like

```makefile
objects = main.o kbd.o command.o display.o \
          insert.o search.o files.o utils.o

edit : $(objects)
	cc -o edit $(objects)

$(objects) : defs.h
kbd.o command.o files.o : command.h
display.o insert.o search.o files.o : buffer.h

.PHONY : clean
clean :
	-rm edit $(objects)
```

> [!NOTE]
>
> about `-` error mark
>
> After each shell invocation returns, make looks at its exit status. If the
> shell completed successfully (the exit status is zero), the next line in the
> recipe is executed in a new shell; after the last line is finished, the rule
> is finished.

> If there is an error (the exit status is nonzero), make gives up on the
> current rule, and perhaps on all rules.

> Sometimes the failure of a certain recipe line does not indicate a problem.
> For example, you may use the mkdir command to ensure that a directory exists.
> If the directory already exists, mkdir will report an error, but you probably
> want make to continue regardless.

> To ignore errors in a recipe line, write a `-` at the beginning of the line’s
> text (after the initial tab). The `-` is discarded before the line is passed
> to the shell for execution.

TODO: pattern rules with filter `$(filter %.o,$(obj_files))`

References:

- [Make manual - 2.5 Letting make Deduce the Recipes](https://www.gnu.org/software/make/manual/html_node/make-Deduces.html)
- [Make manual - 2.6 Another Style of Makefile](https://www.gnu.org/software/make/manual/html_node/Combine-By-Prerequisite.html)
- [Make manual - 5.5 Errors in Recipes](https://www.gnu.org/software/make/manual/html_node/Errors.html)
- [A Super-Simple Makefile for Medium-Sized C/C++ Projects](https://spin.atomicobject.com/2016/08/26/makefile-c-projects/)

## Arithmetic operations for Makefile

1. shell echo
2. shell expr
3. third libs
4. guile / perl

> GNU `make` may be built with support for GNU Guile as an embedded extension
> language. Guile implements the Scheme language. A review of GNU Guile and the
> Scheme language and its features is beyond the scope of this manual: see the
> documentation for GNU Guile and Scheme.

> You can determine if `make` contains support for Guile by examining the
> `.FEATURES` variable; it will contain the word _guile_ if Guile support is
> available.

> The Guile integration provides one new `make` function: `guile`. The guile
> function takes one argument which is first expanded by `make` in the normal
> fashion, then passed to the GNU Guile evaluator. The result of the evaluator
> is converted into a string and used as the expansion of the `guile` function
> in the makefile.

- [Makefile Tricks: Arithmetic – Addition, Subtraction, Multiplication, Division, Modulo, Comparison](https://gist.github.com/pushandplay/2f42415bcf4250ccdf13)
- [How do I perform arithmetic in a makefile?](https://stackoverflow.com/questions/1926063/how-do-i-perform-arithmetic-in-a-makefile)
- [Make Manual - 12.1 GNU Guile Integration](https://www.gnu.org/software/make/manual/html_node/Guile-Integration.html)
- [Guile Manual - 6.6.2.11 Arithmetic Functions](https://www.gnu.org/software/guile/manual/html_node/Arithmetic.html)

## Wilecard recipe

Using wilecard `${*}` and `${@}` to capture different input rule name.

```Makefile
prefix-%:
	@echo "Your input is '${@}' and you catched '${*}'"
```

```console
$ make prefix-foo
Your input is 'prefix-foo' and you catched 'foo'
$ make prefix-bar
Your input is 'prefix-bar' and you catched 'bar'
```

Ref:

- [4.12.1 Syntax of Static Pattern Rules](https://www.gnu.org/software/make/manual/html_node/Static-Usage.html)
