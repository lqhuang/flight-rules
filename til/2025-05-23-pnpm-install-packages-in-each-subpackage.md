---
title: Stupid approach to install packages in each subpackage with pnpm
date: 2025-05-23
tags:
  - shell
  - cli
---

I'm trying to install `eslint` in each subpackage of a monorepo with `pnpm` by listing the packages and then installing it in each package.

```shell
turbo ls --output json | noglob jq .packages.items.[].path | noglob xargs -t -I '{}' -P 1 -- sh -c "pushd {}; pnpm add -D 'eslint'; popd;"
```

Where in the `xargs` command:

- `-t`/`--verbose` is to echo the command to be executed to standard error immediately before it is executed.
- `-I replstr` is to replace the `{}` with the output of the previous command and it implies **execute utility for each input line**. Or you can just use `-I` without `replstr` pattern.
- `-P 1` is to limit the number of parallel processes to 1.
- `--` is to indicate the end of options for `xargs` and the beginning of the command to be executed. This is useful when the command may have options that could be confused with input.
- `sh -c` is to execute multiple commands. This is necessary, otherwise shell will interprete `;` as the seperator.
  - if no `sh -c`, the excution will be `( xargs -t -I '{}' -P 1 -- pushd {} ); pnpm add -D 'eslint'; popd;`

What the smart command does?

Actually, `pnpm` provide the negative pattern for selecting the packages to install

```roff
Filtering options (run the command only on packages that satisfy at least one of the selectors):
      --filter !<selector>                      If a selector starts with ! (or \! in zsh), it means the packages matching the selector must be excluded. E.g., "pnpm
                                                --filter !foo" selects all packages except "foo"
      --filter .                                Includes all packages that are under the current working directory
      --filter .                                Includes all packages that are under the current working directory
      --filter ...^<pattern>                    Includes only the direct and indirect dependents of the matched packages without including the matched packages
                                                themselves. ^ must be doubled at the Windows Command Prompt. E.g.: ...^foo (...^^foo in Command Prompt)
      --filter ...<pattern>                     Includes all direct and indirect dependents of the matched packages. E.g.: ...foo, "...@bar/*"
      --filter <pattern>...                     Includes all direct and indirect dependencies of the matched packages. E.g.: foo...
```

But I don't familiar with it. So ... the above command can simplify to:

```shell
noglob pnpm add -D eslint --filter '!@repo/tsconfig'
```

> `noglob` is a zsh command to disable globbing pattern (like `!@repo`) for the command. It may not be necessary in bash or other config.
