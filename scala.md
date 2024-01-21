---
title: Scala Tips or Cheatsheet
created: 2023-02-05
updated: 2024-01-17
---

## Cheatsheet

### Scala compiler flags

Thank god! Finally, I get all (?) compiler flags.

- [Compiler Options Lookup Table](https://docs.scala-lang.org/scala3/guides/migration/options-lookup.html)
- [New Compiler Options](https://docs.scala-lang.org/scala3/guides/migration/options-new.html)

### JVM eco system

- [Apache Maven -- Introduction to the Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html)
- [sbt 1.x docs -- Directories](https://www.scala-sbt.org/1.x/docs/Directories.html)

## Scala 3 new syntax: `try ... match case ... catch`

```scala
try parseNumber(input) match
  case i: Integer => handleInt(i)
  case f: Float   => handleFloat(f)
catch
  case e: NumberFormatException => handleException(e)
```

Ref:

- [Martin Odersky (@odersky) on X](https://twitter.com/odersky/status/1736089879350518020)

## sbt: Running "sbt commands" in cli

`sbt` interprets each command line argument provided to it as a command together
with the command’s arguments. Therefore, to run a command that takes arguments
in batch mode, quote the command using double quotes, and its arguments. For
example,

```sh
sbt "project X" clean "~ compile"
```

And there are some notable symbol prefixes of genernal sbt commands:

- `~ <command>` Executes the project specified action or method whenever source
  files change. See Triggered Execution for details.
- `< filename` Executes the commands in the given file. Each command should be
  on its own line. Empty lines and lines beginning with `#` are ignored
- `+ <command>` Executes the project specified action or method for all versions
  of Scala defined in the crossScalaVersions setting.
- `++ <version|home-directory> <command>` Temporarily changes the version of
  Scala building the project and executes the provided command. `<command>` is
  optional. The specified version of Scala is used until the project is
  reloaded, settings are modified (such as by the set or session commands), or
  `++` is run again. `<version>` does not need to be listed in the build
  definition, but it must be available in a repository. Alternatively, specify
  the path to a Scala installation.
- `; A ; B` Execute A and if it succeeds, run B. Note that **the leading
  semicolon is required**.

Ref:

1. [Running commands](https://www.scala-sbt.org/1.x/docs/Howto-Running-Commands.html)
2. [Command Line Reference](https://www.scala-sbt.org/1.x/docs/Command-Line-Reference.html)
3. [Triggered Execution](https://www.scala-sbt.org/1.x/docs/Triggered-Execution.html)

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

## sbt: "~" trigger execution

sbt provides the ability (`~` command) to monitor the input files for a
particular task and repeat the task when changes to those files occur.

A common use-case is continuous compilation. The following commands will make
sbt -
`watch for source changes in the Test and Compile (default) configurations`
respectively and re-run the compile command.

```sbt
> ~ Test / compile
> ~ compile
```

Using `~` help that multiple commands can be scheduled at once by prefixing each
command with a semicolon. For example, the following runs `clean` and then
`compile` each time a source file changes:

```sbt
> ~ ;clean;compile
```

The behavior of triggered execution can be configured via a number of settings.

- `watchTriggers: Seq[Glob]`
- `watchTriggeredMessage: (Int, Path, Seq[String]) => Option[String]`
- `watchInputOptions: Seq[Watch.InputOption]`
- `watchBeforeCommand: () => Unit`
- `watchLogLevel`
- `watchInputParser: Parser[Watch.Action]`
- `watchStartMessage: (Int, ProjectRef, Seq[String]) => Option[String]`
- `watchOnIteration: (Int, ProjectRef, Seq[String]) => Watch.Action`
- `watchForceTriggerOnAnyChange: Boolean`
- `watchPersistFileStamps: Boolean`
- `watchAntiEntropy: FiniteDuration`

Refs:

- [Triggered Execution](https://www.scala-sbt.org/1.x/docs/Triggered-Execution.html)
- [Provide multiple commands to run consecutively](https://www.scala-sbt.org/1.x/docs/Howto-Running-Commands.html)
- [Triggered Execution - Configuration](https://www.scala-sbt.org/1.x/docs/Triggered-Execution.html#Configuration)

## Cheatsheet for pattern matching

Simply remember that `@` symbol cannot use to catch type, and `:` symbol cannot
use to extract specific pattern (unapply).

```scala
import scala.util.Random

abstract class PL
case class Scala(creator: String, age: Int, version: Int) extends PL
case class Other(name: String, age: Int, version: Int)    extends PL

val that =
  Random.shuffle(List(Scala("scala", 20, 3), Other("Any", 30, 22))).head

that match {
  case x: Scala         => x.age
  case Scala(_, age, _) => age - 15

  // It also works
  case lang @ Scala(_, age, _) if lang.version != 2 => age
  // matching for Scala with only 'scala' name ... it works
  case lang @ Scala(_, _, 2) => lang.age

  /*
   * The following two cases wouldn't work and failed to compile
   */
  /* want to match Other type */
  // case lang @ Other => ???
  /* matching for language with only version 2. */
  // case lang: Scala(_, _, 2) => ???

  // While using `@` symbol, the right side is an unapplied Instance
  case lang @ Other(_, _, _) => lang.age + 10
  // While using `:` symbol, the right side is a type
  case lang: Other => lang.age + 10

  case _ => 0
}
```

## Case class inheritance is so wrong

In scala, case-to-case inheritance is prohibited. The main cause is the
**equality** problem. Case classes come with a supplied implementation of
`equals` and `hashCode`, equality of its sub class is quite fragile.

Through case-to-case inheritance is limited by compiler, we still could make
corner case to show that:

```scala
case class ColoredPoint(x: Int, y: Int, c: String)
class RedPoint(x: Int, y: Int)   extends ColoredPoint(x, y, "red")
class GreenPoint(x: Int, y: Int) extends ColoredPoint(x, y, "green")

val colored = ColoredPoint(0, 0, "red")
val red1    = new RedPoint(0, 0)
val red2    = new RedPoint(0, 0)
val green   = new GreenPoint(0, 0)

/*
 * Why? `equals` method from parent class is called?
 */
red1 equals colored // true
red2 equals colored // true
red1 equals red2    // true

red1 == colored // true
red2 == colored // true
red1 == red2    // true

colored equals green // false
red1 equals green    // false
red2 equals green    // false

colored == green // false
red1 == green    // false
red2 == green    // false
```

Yeah, it's so wrong.

1. [What is _so_ wrong with case class inheritance?](https://stackoverflow.com/questions/11158929/what-is-so-wrong-with-case-class-inheritance)
