---
title: Scala Tips
created: 2023-02-05
updated: 2024-01-17
---

## Cheatsheet

Thank god! Finally, I get all (?) compiler flags.

- [Compiler Options Lookup Table](https://docs.scala-lang.org/scala3/guides/migration/options-lookup.html)
- [New Compiler Options](https://docs.scala-lang.org/scala3/guides/migration/options-new.html)

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
