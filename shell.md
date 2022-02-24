---
title: Shell Tips
created: 2019-01-20
updated: 2022-02-24
---

# Shell related tips

## Useful rules

1. [BashFAQ](https://mywiki.wooledge.org/BashFAQ)
2. [BashPitfalls](https://mywiki.wooledge.org/BashPitfalls)
3. [BashGuide](https://mywiki.wooledge.org/BashGuide)
4. [BashSheet](https://mywiki.wooledge.org/BashSheet)
5. [BashProgramming](https://mywiki.wooledge.org/BashProgramming)
6. [Bash Reference Manual](https://www.gnu.org/software/bash/manual/html_node/index.html)
7. [Advanced Bash-Scripting Guide](http://tldp.org/LDP/abs/html/)

## Shell: Use variable inside single quote

Unfortunately, you can't expand variables in single quotes. But you can end single quotes and start double quotes, though:

    echo 'visit:"'"$site"'"'

Or, you can backslash double quotes inside of double quotes:

    echo "visit:\"$site\""

References:

1. [print-value-inside-variable-inside-single-quote](https://unix.stackexchange.com/questions/209971/is-there-any-way-to-print-value-inside-variable-inside-single-quote)

## Shell: Single and double quotes are different in Bash

Single `''` quotes won't interpolate anything, but double quotes `""` will, including: variables, backticks, certain `\` escapes, etc.

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

Refs:

1. https://unix.stackexchange.com/questions/306111/what-is-the-difference-between-the-bash-operators-vs-vs-vs
2. https://stackoverflow.com/questions/669452/is-double-square-brackets-preferable-over-single-square-brackets-in-bash
3. https://serverfault.com/questions/52034/what-is-the-difference-between-double-and-single-square-brackets-in-bash

## Shell: Test if a string contains a substring

### Method 1

You need to interpolate the $testseq variable with one of the following ways:

- `$file == *_"$testseq"_*` (here `$testseq` considered as a fixed string).
- `$file == *_${testseq}_*` (here `$testseq` considered as a pattern).

Or the `_` immediately after the variable's name will be taken as part of the variable's name (it's a valid character in a variable name).

The issue you are having is due to the fact that `_` is a valid character in a variable name. The shell will thus see `*_$testseq_*` as "`*_` followed by the value of the variable `$testseq_` and an `*`". The variable `$testseq_` is undefined, so it will be expanded to an empty string, and you end up with `*_*`, which obviously matches the `$file` value that you have. You may expect to get `True` as long as the filename in `$file` contains at least one underscore.

To properly delimit the name of the variable, use `"..."` around the expansion: `*_"$testseq"_*`. This would use the value of the variable as a string. Would you want to use the value of the variable as a pattern, use `*_${testseq}_*` instead.

Another quick fix is to include the underscores in the value of `$testseq`:

```shell
testseq="_gen_"  # instead of testseq="gen"
```

and then just use `*"$testseq"*` as the pattern (for a string comparison).

### Method 2

Use the `=~` operator to make regular expression comparsions in bash (and only work in bash):

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

The special parameters `*` and `@` have special meaning when in double quotes (see [Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html#Shell-Parameter-Expansion)).

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

1. Use `printf`, just like in C. It's available in any POSIXly Bourne Shell (zsh, ksh, bash, ...)

```shell
FILE=$(printf %04d 42).txt
echo "$FILE"
0042.txt
```

2. Another internal command typeset. Earlier, we had seen the usage of typeset in arithmetic operations. typeset has an option `-Z` which is used for zero padding. So, just declare a variable using typeset with the required padding as shown below

```shell
$ typeset -Z4 x
$ x=23
$ echo $x
0023
```

Note: This option `-Z` in typeset is not present in all the shells. ksh has this option.

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

> `${RANDOM}` is generated by using your current process ID (PID) and the current time/date as defined by the number of seconds elapsed since 1970. -- from Abhijeet Rastogi

> Each time this parameter is referenced, a random integer between 0 and 32767 is generated. -- from `man bash`

You shouldn't be using `${RANDOM}` for security purposes. For example, if you want to generate a random number between 1 and 10:

```shell
echo $(( ${RANDOM} % 10 + 1 ))
# or
echo ${RNADOM} % 10 + 1 | bc
```

This is not an uniform distribution, because 0 to 32767 (unsigned 15-bit int or signed 16-bit int) obviously can not divide evenly into groups of 10.

However, you could divide it into 8 groups equally, this would be useful to choose a random CUDA device:

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

Read random bytes from `/dev/urandom` or `/dev/random` and convert it to interger.

>     od -A n -N 2 -t u2 /dev/urandom
>
> That'll read two bytes and print them as an unsigned int; you still have to do your clipping.

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

test exit code status

`hash foo 2>/dev/null`: works with Z shell (Zsh), Bash, Dash and ash.

`type -p foo`: it appears to work with Z shell, Bash and ash (BusyBox), but not Dash (it interprets -p as an argument).

`command -v foo`: works with Z shell, Bash, Dash, but not ash (BusyBox) (-ash: command: not found).

Also note that `builtin` is not available with ash and Dash.

Refs:

1. [How can I check if a program exists from a Bash script?](https://stackoverflow.com/a/24856148)

### Fast if else alternatives

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

### Bash: File test operators

The test command takes one of the following syntax forms:

```
test EXPRESSION
[ EXPRESSION ]
[[ EXPRESSION ]]
```

The test command includes the following FILE operators that allow you to test for particular types of files:

- `-b FILE` - True if the FILE exists and is a special block file.
- `-c FILE` - True if the FILE exists and is a special character file.
- `-d FILE` - True if the FILE exists and is a directory.
- `-e FILE` - True if the FILE exists and is a file, regardless of type (node, directory, socket, etc.).
- `-f FILE` - True if the FILE exists and is a regular file (not a directory or device).
- `-G FILE` - True if the FILE exists and has the same group as the user running the command.
- `-h FILE` - True if the FILE exists and is a symbolic link.
- `-g FILE` - True if the FILE exists and has set-group-id (sgid) flag set.
- `-k FILE` - True if the FILE exists and has a sticky bit flag set.
- `-L FILE` - True if the FILE exists and is a symbolic link.
- `-O FILE` - True if the FILE exists and is owned by the user running the command.
- `-p FILE` - True if the FILE exists and is a pipe.
- `-r FILE` - True if the FILE exists and is readable.
- `-S FILE` - True if the FILE exists and is a socket.
- `-s FILE` - True if the FILE exists and has nonzero size.
- `-u FILE` - True if the FILE exists and set-user-id (suid) flag is set.
- `-w FILE` - True if the FILE exists and is writable.
- `-x FILE` - True if the FILE exists and is executable.

Refs:

1. [How to Check if a File or Directory Exists in Bash](https://linuxize.com/post/bash-check-if-file-exists)
