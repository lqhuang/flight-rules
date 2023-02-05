---
title: Scala Tips
created: 2023-02-05
updated: 2023-02-05
---

## sbt: Running commands in cli

`sbt` interprets each command line argument provided to it as a command together
with the command’s arguments. Therefore, to run a command that takes arguments
in batch mode, quote the command using double quotes, and its arguments. For
example,

```sh
sbt "project X" clean "~ compile"
```

Ref:
[Running commands](https://www.scala-sbt.org/1.x/docs/Howto-Running-Commands.html)

## sbt: Temporarily switch to a different Scala version

The scalaVersion configures the version of Scala used for compilation. By
default, sbt also adds a dependency on the Scala library with this version.

```scala
scalaVersion := "2.11.1"
```

To set the Scala version in all scopes to a specific value, use the `++`
command. For example, to temporarily use Scala `2.10.4`, run:

```sbt
> ++ 2.10.4
```

Ref:
[Temporarily switch to a different Scala version](https://www.scala-sbt.org/1.x/docs/Howto-Scala.html#Temporarily+switch+to+a+different+Scala+version)

## (draft) sbt: "~" trigger execution

Symbol `~` in sbt

Refs:

- [Triggered Execution](https://www.scala-sbt.org/1.x/docs/Triggered-Execution.html)
- [Provide multiple commands to run consecutively](https://www.scala-sbt.org/1.x/docs/Howto-Running-Commands.html)
