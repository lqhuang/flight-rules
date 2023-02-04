---
title: Shell Tips
created: 2019-01-20
updated: 2023-02-04
---

## Useful rules

1. [BashFAQ](https://mywiki.wooledge.org/BashFAQ)
2. [BashPitfalls](https://mywiki.wooledge.org/BashPitfalls)
3. [BashGuide](https://mywiki.wooledge.org/BashGuide)
4. [BashSheet](https://mywiki.wooledge.org/BashSheet)
5. [BashProgramming](https://mywiki.wooledge.org/BashProgramming)
6. [Bash Reference Manual](https://www.gnu.org/software/bash/manual/html_node/index.html)
7. [Advanced Bash-Scripting Guide](http://tldp.org/LDP/abs/html/)

## Shell: Use variable inside single quote

Unfortunately, you can't expand variables in single quotes. But you can end
single quotes and start double quotes, though:

    echo 'visit:"'"$site"'"'

Or, you can backslash double quotes inside of double quotes:

    echo "visit:\"$site\""

References:

1. [print-value-inside-variable-inside-single-quote](https://unix.stackexchange.com/questions/209971/is-there-any-way-to-print-value-inside-variable-inside-single-quote)

## Shell: Single and double quotes are different in Bash

Single `''` quotes won't interpolate anything, but double quotes `""` will,
including: variables, backticks, certain `\` escapes, etc.

For example, the following script

```shell
#!/bin/sh
MYVAR=sometext
echo "double quotes gives you $MYVAR"
echo 'single quotes gives you $MYVAR'
```

will give this:

```plain
double quotes gives you sometext
single quotes gives you $MYVAR
```

References:

1. [difference-between-single-and-double-quotes-in-bash](https://stackoverflow.com/questions/6697753/difference-between-single-and-double-quotes-in-bash)
2. [Single-Quotes.html#Single-Quotes](https://www.gnu.org/software/bash/manual/html_node/Single-Quotes.html#Single-Quotes)

## Shell: Difference among `[]`, `[[]]`, `{}`, `()`, `(())`

Some of them are **Compound Commands**: A compound command is one of the
following. In most cases a list in a command's description may be separated from
the rest of the command by one or more newlines, and may be followed by a
newline in place of a semicolon.

- `(list)`
- `{ list; }`
- `((expression))`
- `[[expression]]`

Except for:

- `( expression )`: is also an operator, it returns the value of expression.
  This may be used to override the normal precedence of operators.
- `[]`: is a builtin command same with `test expression`

Refs:

1. https://unix.stackexchange.com/questions/306111/what-is-the-difference-between-the-bash-operators-vs-vs-vs
2. https://stackoverflow.com/questions/669452/is-double-square-brackets-preferable-over-single-square-brackets-in-bash
3. https://serverfault.com/questions/52034/what-is-the-difference-between-double-and-single-square-brackets-in-bash
4. [bash(1) — Linux manual page](https://www.man7.org/linux/man-pages/man1/bash.1.html#SHELL_GRAMMAR)

## Shell: Test if a string contains a substring

### Method 1

You need to interpolate the $testseq variable with one of the following ways:

- `$file == *_"$testseq"_*` (here `$testseq` considered as a fixed string).
- `$file == *_${testseq}_*` (here `$testseq` considered as a pattern).

Or the `_` immediately after the variable's name will be taken as part of the
variable's name (it's a valid character in a variable name).

The issue you are having is due to the fact that `_` is a valid character in a
variable name. The shell will thus see `*_$testseq_*` as "`*_` followed by the
value of the variable `$testseq_` and an `*`". The variable `$testseq_` is
undefined, so it will be expanded to an empty string, and you end up with `*_*`,
which obviously matches the `$file` value that you have. You may expect to get
`True` as long as the filename in `$file` contains at least one underscore.

To properly delimit the name of the variable, use `"..."` around the expansion:
`*_"$testseq"_*`. This would use the value of the variable as a string. Would
you want to use the value of the variable as a pattern, use `*_${testseq}_*`
instead.

Another quick fix is to include the underscores in the value of `$testseq`:

```shell
testseq="_gen_"  # instead of testseq="gen"
```

and then just use `*"$testseq"*` as the pattern (for a string comparison).

### Method 2

Use the `=~` operator to make regular expression comparsions in bash (and only
work in bash):

    #!/bin/bash
    file="JetConst_reco_allconst_4j2t.png"
    testseq="gen"
    if [[ $file =~ $testseq ]]; then
        echo "True"
    else
        echo "False"
    fi

References:

1. [test-if-a-string-contains-a-substring](https://unix.stackexchange.com/questions/370889/test-if-a-string-contains-a-substring)
2. [how-to-check-if-a-string-contains-a-substring-in-bash](https://stackoverflow.com/questions/229551/how-to-check-if-a-string-contains-a-substring-in-bash)

## Shell: Best way to include util script

Refs:

1. https://stackoverflow.com/questions/192292/how-best-to-include-other-scripts

## Shell: Loop through an array

First define a array

```shell
declare -a arr=("element1" "element2" "element3")
# or
arr = ("element1"
       "element2" "element3"
       "element4")
```

Then

```shell
## now loop through the above array
for i in "${arr[@]}"; do  # double quotes are required
   echo "$i"
   # or do whatever with individual element of the array
done
```

The special parameters `*` and `@` have special meaning when in double quotes
(see
[Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html#Shell-Parameter-Expansion)).

If no variables used:

```shell
for name in "a" "b" "c" "d" "e" "f"; do
    # do something like: echo $databaseName
done
```

Advanced:

1. Creating an associative array. A dictionary:

```shell
declare -A continent

continent[Vietnam]=Asia
continent[France]=Europe
continent[Argentina]=America

for item in "${!continent[@]}"; do
    printf "$item is in ${continent[$item]} \n"
done
```

Output:

```plain
Argentina is in America
Vietnam is in Asia
France is in Europe
```

2. Array manipulation

```shell

list=()

for i in $(seq 1 5); do
    list+=($i)
done
```

Some intersting behaviors:

```shell
listOfNames="RA
RB
R C
RD"

# To allow for other whitespace in the string:
# 1. add double quotes around the list variable, or
# 2. see the IFS note (under 'Side Notes')

for databaseName in "$listOfNames"   #  <-- Note: Added "" quotes.
do
  echo "$databaseName"  # (i.e. do action / processing of $databaseName here...)
done

# Outputs
# RA
# RB
# R C
# RD
```

No whitespace in the names:

```shell
listOfNames="RA
RB
R C
RD"

for databaseName in $listOfNames  # Note: No quotes
do
  echo "$databaseName"  # (i.e. do action / processing of $databaseName here...)
done

# Outputs
# RA
# RB
# R
# C
# RD
```

Refs:

1. [Loop through an array of strings in Bash](https://stackoverflow.com/questions/8880603/loop-through-an-array-of-strings-in-bash)
2. [Shell-Parameter-Expansion.html#Shell-Parameter-Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html#Shell-Parameter-Expansion)

## Bash: Readlines

Refs:

1. http://mywiki.wooledge.org/DontReadLinesWithFor
2. https://superuser.com/questions/284187/bash-iterating-over-lines-in-a-variable/
3. https://unix.stackexchange.com/questions/24260/reading-lines-from-a-file-with-bash-for-vs-while/24278#24278
4. http://tldp.org/LDP/abs/html/internalvariables.html#IFSREF
5. https://stackoverflow.com/questions/7718307/how-to-split-a-list-by-comma-not-space/23561892#23561892
6. https://stackoverflow.com/questions/13122441/how-do-i-read-a-variable-on-a-while-loop/13122491#13122491

## Shell: How to delete a substring

<!-- ### using shell variables -->

```shell
DATA="abc.out"
pattern=".out"
DATA=${DATA/$pattern/}
echo "DATA=${DATA}"
```

Refs:

1. https://stackoverflow.com/questions/16623835/remove-a-fixed-prefix-suffix-from-a-string-in-bash
2. https://stackoverflow.com/questions/13570327/how-to-delete-a-substring-using-shell-script
3. https://unix.stackexchange.com/questions/311758/remove-specific-word-in-variable

## Shell: Output string with padding

1. Use `printf`, just like in C. It's available in any POSIXly Bourne Shell
   (zsh, ksh, bash, ...)

```shell
FILE=$(printf %04d 42).txt
echo "$FILE"
0042.txt
```

2. Another internal command typeset. Earlier, we had seen the usage of typeset
   in arithmetic operations. typeset has an option `-Z` which is used for zero
   padding. So, just declare a variable using typeset with the required padding
   as shown below

```shell
$ typeset -Z4 x
$ x=23
$ echo $x
0023
```

Note: This option `-Z` in typeset is not present in all the shells. ksh has this
option.

References:

1. [Zero-padding a string/file name in shell script](https://stackoverflow.com/questions/16798770/zero-padding-a-string-file-name-in-shell-script)
2. [How to zero pad a number or a variable?](http://www.theunixschool.com/2012/04/different-ways-to-zero-pad-number-or.html)

## Bash: Get arguments from command line options

References:

1. https://wiki.bash-hackers.org/howto/getopts_tutorial
2. https://mywiki.wooledge.org/BashFAQ/035
3. https://stackoverflow.com/questions/402377/using-getopts-to-process-long-and-short-command-line-options

## Shell: Detect current shell is from a SSH client

```shell
if [[ -n ${SSH_CLIENT} ]] || [ -n ${SSH_TTY} ]; then
  SESSION_TYPE=remote/ssh
```

References:

1. [how-can-i-detect-if-the-shell-is-controlled-from-ssh](https://unix.stackexchange.com/questions/9605/how-can-i-detect-if-the-shell-is-controlled-from-ssh)

## Shell: Catch all arguments inside script

Use quoted `"$@"` instead of `$@`

```
+--------+---------------------------+
| Syntax |      Effective result     |
+--------+---------------------------+
|   $*   |     $1 $2 $3 ... ${N}     |
+--------+---------------------------+
|   $@   |     $1 $2 $3 ... ${N}     |
+--------+---------------------------+
|  "$*"  |    "$1c$2c$3c...c${N}"    |
+--------+---------------------------+
|  "$@"  | "$1" "$2" "$3" ... "${N}" |
+--------+---------------------------+
```

References:

1. [Propagate all arguments in a bash shell script](https://stackoverflow.com/questions/4824590/propagate-all-arguments-in-a-bash-shell-script)

## Shell: Generate random numbers from shell

### `${RANDOM}`

```shell
echo ${RANDOM}
```

> `${RANDOM}` is generated by using your current process ID (PID) and the
> current time/date as defined by the number of seconds elapsed since 1970. --
> from Abhijeet Rastogi

> Each time this parameter is referenced, a random integer between 0 and 32767
> is generated. -- from `man bash`

You shouldn't be using `${RANDOM}` for security purposes. For example, if you
want to generate a random number between 1 and 10:

```shell
echo $(( ${RANDOM} % 10 + 1 ))
# or
echo ${RNADOM} % 10 + 1 | bc
```

This is not an uniform distribution, because 0 to 32767 (unsigned 15-bit int or
signed 16-bit int) obviously can not divide evenly into groups of 10.

However, you could divide it into 8 groups equally, this would be useful to
choose a random CUDA device:

```shell
CUDA_VISIBLE_DEVICES=$(( ${RANDOM} % 8 ))
```

### `shuf` (from gnu core utils)

```shell
shut -i ${MIN}-{MAX} -n ${NUMBER}
# eg: generate 1 random number between 1024 to 65535
shut -i 1024-65535 -n 1
```

### `od`

Read random bytes from `/dev/urandom` or `/dev/random` and convert it to
interger.

>     od -A n -N 2 -t u2 /dev/urandom
>
> That'll read two bytes and print them as an unsigned int; you still have to do
> your clipping.

### `jot` for macOS/FreeBSD

```shell
jot -r ${NUMBER} ${MIN} ${MAX}
# eg:
jot -r 1 1024 65535
# fairer distribution
jot -w %i -r 1 ${MIN} ${MAX_PLUS_1}
```

Note: it may have unfair distributions.

References:

1. [Generating random number between 1 and 10 in Bash Shell Script](https://stackoverflow.com/questions/8988824/generating-random-number-between-1-and-10-in-bash-shell-script)
2. [Random number from a range in a Bash Script](https://stackoverflow.com/questions/2556190/random-number-from-a-range-in-a-bash-script)
3. [Generating Random Numbers in Linux Shell Scripting](https://blog.eduonix.com/shell-scripting/generating-random-numbers-in-linux-shell-scripting/)
4. [Generate random numbers in specific range](https://unix.stackexchange.com/questions/140750/generate-random-numbers-in-specific-range/241199#241199)

## Test executed command exists

Test exit code status

- `hash foo 2>/dev/null`: works with Z shell (Zsh), Bash, Dash and ash.
- `type -p foo`: it appears to work with Z shell, Bash and ash (BusyBox), but
  not Dash (it interprets -p as an argument).
- `command -v foo`: works with Z shell, Bash, Dash, but not ash (BusyBox) (-ash:
  command: not found).

Also note that `builtin` is not available with ash and Dash.

Refs:

1. [How can I check if a program exists from a Bash script?](https://stackoverflow.com/a/24856148)

### Bash: Fast `if-else` alternatives

```
command
status=$?
## run date command ##
cmd="date"
$cmd
## get status ##
status=$?
## take some decision ##
[ $status -eq 0 ] && echo "$cmd command was successful" || echo "$cmd failed"
```

### Bash: Conditional expressions

The test command takes one of the following syntax forms:

```bash
test EXPRESSION  # builtin command
[ EXPRESSION ]  # builtin command
[[ EXPRESSION ]]  # compound command
```

When used with [[, the < and > operators sort lexicographically using the
current locale. The test command sorts using ASCII ordering.

- `-a file`: True if file exists.
- `-b file`: True if file exists and is a block special file.
- `-c file`: True if file exists and is a character special file.
- `-d file`: True if file exists and is a directory.
- `-e file`: True if file exists.
- `-f file`: True if file exists and is a regular file.
- `-g file`: True if file exists and is set-group-id.
- `-h file`: True if file exists and is a symbolic link.
- `-k file`: True if file exists and its ``sticky'' bit is set.
- `-p file`: True if file exists and is a named pipe (FIFO).
- `-r file`: True if file exists and is readable.
- `-s file`: True if file exists and has a size greater than zero.
- `-t fd`: True if file descriptor fd is open and refers to a terminal.
- `-u file`: True if file exists and its set-user-id bit is set.
- `-w file`: True if file exists and is writable.
- `-x file`: True if file exists and is executable.
- `-G file`: True if file exists and is owned by the effective group id.
- `-L file`: True if file exists and is a symbolic link.
- `-N file`: True if file exists and has been modified since it was last read.
- `-O file`: True if file exists and is owned by the effective user id.
- `-S file`: True if file exists and is a socket.
- `file1 -ef file2`: True if file1 and file2 refer to the same device and inode
  numbers.
- `file1 -nt file2`: True if file1 is newer (according to modification date)
  than file2, or if file1 exists and file2 does not.
- `file1 -ot file2`: True if file1 is older than file2, or if file2 exists and
  file1 does not.
- `-o optname`: True if the shell option `optname` is enabled. See the list of
  options under the description of the `-o` option to the set builtin below.
- `-v varname`: True if the shell variable varname is set (has been assigned a
  value).
- `-R varname`: True if the shell variable varname is set and is a name
  reference.
- `-z string`: True if the length of string is zero.
- `-n string`: True if the length of string is non-zero.
- `string1 == string2` / `string1 = string2`: True if the strings are equal. `=`
  should be used with the `test` command for POSIX conformance. When used with
  the `[[` command, this performs pattern matching as described above
  (**Compound Commands**).
- `string1 != string2`: True if the strings are not equal.
- `string1 < string2`: True if string1 sorts before string2 lexicographically.
- `string1 > string2`: True if string1 sorts after string2 lexicographically.
- `arg1 OP arg2`: `OP` is one of `-eq`, `-ne`, `-lt`, `-le`, `-gt`, or `-ge`.
  These arithmetic binary operators return true if arg1 is equal to, not equal
  to, less than, less than or equal to, greater than, or greater than or equal
  to arg2, respectively. Arg1 and arg2 may be positive or negative integers.
  When used with the `[[` command, Arg1 and Arg2 are evaluated as arithmetic
  expressions (see ARITHMETIC EVALUATION above).

Refs:

1. [How to Check if a File or Directory Exists in Bash](https://linuxize.com/post/bash-check-if-file-exists)
2. [bash(1) — Linux manual page](https://www.man7.org/linux/man-pages/man1/bash.1.html#CONDITIONAL_EXPRESSIONS)

## Bash: Reject to run script while no required variable provided

If your script relys on some critical variables and want to fastly fail if a
variable is not defined or has a default `${SOME_VARIABLE:=default}`, try:

```bash
set -u # or set -o nounset
: "$BATCHNUM"
```

Explaination:

> The first line sets the `nounset` option in the shell running the script,
> which aborts if you try to expand an unset variable; the second line expands
> `$BATCHNUM` in the context of a no-op ``:`, to trigger the abort before doing
> anything else.

Of course, a more helpful version is also available:

```bash
if [[ -z "$BATCHNUM" ]]; then
    echo "Must provide 'BATCHNUM' in environment" 1>&2
    exit 1
fi
```

Reference:

1. [Avoid running the script if a variable is not defined](https://unix.stackexchange.com/questions/228331/avoid-running-the-script-if-a-variable-is-not-defined)

## Bash: Job control commands

Job control refers to the ability to selectively stop (**suspend**) the
execution of processes and continue (**resume**) their execution at a later
point. A user typically employs this facility via an interactive interface
supplied jointly by the operating system kernel's terminal driver and bash.

The shell associates a `job` with each pipeline. It keeps a table of currently
executing jobs, which may be listed with the jobs command. When bash starts a
job asynchronously (in the **background**), it prints a line that looks like:

    bash$ sleep 100 &
    [1] 1384

    bash$ jobs
    [1]+  Running                 sleep 100 &

There are a number of ways to refer to a job in the shell. The character `%`
introduces a job specification (**jobspec**). Job number `n` may be referred to
as `%n`.

Then you can bring **job [1]** to foreground again:

```bash
fg %1
```

Enable job controls by using:

```bash
set -m # or set -o monitor
```

Related commands: `fg`, `bg`, `jobs`, `wait`, `kill`, `disown`, `suspend`

And the following is job identifiers:

| Notation | Meaning                                                                 |
| -------- | ----------------------------------------------------------------------- |
| `%N`     | Job number [N]                                                          |
| `%S`     | Invocation (command-line) of job begins with string `S`                 |
| `%?S`    | Invocation (command-line) of job contains within it string `S`          |
| `%%`     | "current" job (last job stopped in foreground or started in background) |
| `%+`     | "current" job (last job stopped in foreground or started in background) |
| `%-`     | Last job                                                                |
| `$!`     | Last background process                                                 |

References:

1. [Advanced Bash-Scripting Guide: 15.1. Job Control Commands](https://tldp.org/LDP/abs/html/x9644.html)
2. [bash(1) — Linux manual page](https://www.man7.org/linux/man-pages/man1/bash.1.html#JOB_CONTROL)

## Bash: Parameter expansion cheatsheet

- `${parameter:-[word]}`: **Use Default Values.** If `parameter` is unset or
  null, the expansion of `word` (or an empty string if `word` is omitted) shall
  be substituted; otherwise, the value of `parameter` shall be substituted.
- `${parameter:=[word]}`: **Assign Default Values.** If `parameter` is unset or
  null, the expansion of `word` (or an empty string if `word` is omitted) shall
  be assigned to `parameter`. In all cases, the final value of `parameter` shall
  be substituted. Only variables, not positional parameters or special
  parameters, can be assigned in this way.
- `${parameter:?[word]}`: **Indicate Error if Null or Unset.** If `parameter` is
  unset or null, the expansion of `word` (or a message indicating it is unset if
  `word` is omitted) shall be written to standard error and the shell exits with
  a non-zero exit status. Otherwise, the value of `parameter` shall be
  substituted. An interactive shell need not exit.
- `${parameter:+[word]}`: **Use Alternative Value.** If `parameter` is unset or
  null, null shall be substituted; otherwise, the expansion of `word` (or an
  empty string if `word` is omitted) shall be substituted.

In the parameter expansions shown previously, use of the `<colon>:` in the
format shall result in a test for a parameter that is unset or null; omission of
the `<colon>:` shall result in a test for a parameter that is only unset. If
parameter is '#' and the colon is omitted, the application shall ensure that
`word` is specified (this is necessary to avoid ambiguity with the string length
expansion). The following table summarizes the effect of the `<colon>:`

| expansion            | `parameter` Set and Not Null | `parameter` Set But Null | `parameter` Unset |
| -------------------- | ---------------------------- | ------------------------ | ----------------- |
| `${parameter:-word}` | substitute `parameter`       | substitute `word`        | substitute `word` |
| `${parameter-word}`  | substitute `parameter`       | substitute null          | substitute `word` |
| `${parameter:=word}` | substitute `parameter`       | assign `word`            | assign `word`     |
| `${parameter=word}`  | substitute `parameter`       | substitute null          | assign `word`     |
| `${parameter:?word}` | substitute `parameter`       | error, exit              | error, exit       |
| `${parameter?word}`  | substitute `parameter`       | substitute null          | error, exit       |
| `${parameter:+word}` | substitute `word`            | substitute null          | substitute null   |
| `${parameter+word}`  | substitute `word`            | substitute `word`        | substitute null   |

In all cases shown with "substitute", the expression is replaced with the value
shown. In all cases shown with "assign", `parameter` is assigned that value,
which also replaces the expression.

References:

1. [Shell & Utilities: 2.6.2 Parameter Expansion](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_06_02)

## Makefile: Sensible defaults

```Makefile
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

.ONESHELL:
.DELETE_ON_ERROR:

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
```

First two lines are trying to always use a recnent bash in strict mode.

- `.ONESHELL` ensures each Make recipe is ran as one single shell session,
  rather than one new shell per line. This both - in my opinion - is more
  intuitive, and it lets you do things like loops, variable assignments and so
  on in bash.
- `.DELETE_ON_ERROR` does what it says on the box - if a Make rule fails, it’s
  target file is deleted. This ensures the next time you run Make, it’ll
  properly re-run the failed rule, and guards against broken files.
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

## Moving around in the command line

There are key shortcuts available in Bash which will help you to move around
faster. They are by the way very similar to the standard emacs keybindings, a
number of key combinations that you will discover in many places and therefore
are very handy to memorize and internalize. The following table is a good
starting point.

| Key combination | Action                                         |
| --------------- | ---------------------------------------------- |
| Ctrl + A        | Move to the beginning of the line              |
| Ctrl + E        | Move to the end of the line                    |
| Alt + B         | Move to the previous word                      |
| Alt + F         | Move to the next word                          |
| Ctrl + U        | Cuts to the beginning of the line              |
| Ctrl + K        | Cuts to the end of the line                    |
| Ctrl + W        | Cuts the previous word                         |
| Ctrl + P        | Browse previously entered commands             |
| Ctrl + R        | Reverse search for previously entered commands |
| Ctrl + Y        | Pastes the text in buffer                      |

Ref:

- [LYM: Moving around in the command line](https://lym.readthedocs.io/en/latest/startingcommands.html#using-to-redirect-output-to-a-file)

## Shell: Use nested variable names for variables

```sh
#!/bin/bash
export HELLO="HELLO"
export HELLOWORLD="Hello, world!"

# This command does not work properly in bash
echo ${${HELLO}WORLD}

# However, a two-step process does work (variable indirection)
export TEMP=${HELLO}WORLD
echo ${!TEMP}
```

Output

```
Hello, world!
```

You can also use `eval`, variable indirection `${!...}`(mentioned above), or
reference variables `declare -n`.

Refs:

- [Can `${var}` parameter expansion expressions be nested in bash?](https://stackoverflow.com/questions/917260/can-var-parameter-expansion-expressions-be-nested-in-bash)
- [Bash - Get the VALUE of 'nested' variable into another variable [Edit: Indirect Variable Expansion]](https://stackoverflow.com/a/46383462)
