---
title: LaTex Notes
created: 2017-02-13
updated: 2025-01-14
---

## Resources

- [The Art of LaTeX: Common Mistakes, and Advice for Typesetting Beautiful, Delightful Proofs](https://fanpu.io/blog/2023/latex-tips/)
- [MiKTeX](https://miktex.org/)
  - [“Just enough TeX”](https://miktex.org/kb/just-enough-tex)
  - [TeX Directory Structure](https://miktex.org/kb/tds)
  - [MiKTeX Manual](https://docs.miktex.org/manual/)
    - [Part II. Reference](https://docs.miktex.org/manual/reference.html)
    - [Chapter 10. Run-Time Defaults](https://docs.miktex.org/manual/defaults.html)

## Setup `miktex` after installation

After installing `miktex`, you have to finish the setup via `miktexsetup` (if prefer cli).

By default `miktex` will install the packages under the user's home directory `${HOME}/bin`. If you want to install the packages under `${HOME}/.local/bin`, you can run the following command with option `--user-install=${HOME}/.local/bin`.

```sh
# or you may try run `miktexsetup cleanup` to remove the old links
miktexsetup finish --user-link-target-directory="${HOME}/.local/bin"
```

And you could use `miktex links list` to check all installed links.

According to TDS (TeX Directory Structure), the TEXMF root directories managed by MiKTeX are the following:

- UserConfig: for user-specific configuration files
- UserData: for user-specific data files (format files, font caches, ...)
- UserInstall: the installation destination for packages installed by the user

And the localtion of these directories is:

Linux

- UserConfig: `$HOME/.miktex/texmfs/config`
- UserData: `$HOME/.miktex/texmfs/data`
- UserInstall: `$HOME/.miktex/texmfs/install`

macOS

- UserConfig: `$HOME/Library/Application Support/MiKTeX/texmfs/config`
- UserData: `$HOME/Library/Application Support/MiKTeX/texmfs/data`
- UserInstall: `$HOME/Library/Application Support/MiKTeX/texmfs/install`

Refs:

- [Install MiKTeX for Linux](https://miktex.org/howto/install-miktex-unx)
- [TEXMF root directories](https://miktex.org/kb/texmf-roots)
- [`miktex-links` — manage links from scripts and formats to executables](https://docs.miktex.org/manual/miktex-links.html)

## float object always fill a full page

相关的参数是

| Counter        | Description                                | Default |
| -------------- | ------------------------------------------ | ------- |
| `topnumber`    | maximum number of floats at top of page    | 2       |
| `bottomnumber` | maximum number of floats at bottom of page | 1       |
| `totalnumber`  | maximum number of floats on a page         | 3       |

| Command              | Description                                           | Default |
| :------------------- | :---------------------------------------------------- | :-----: |
| `\topfraction`       | maximum fraction of page for floats at top            |   0.7   |
| `\bottomfraction`    | maximum fraction of page for floats at bottom         |   0.3   |
| `\textfraction`      | minimum fraction of page for text                     |   0.2   |
| `\floatpagefraction` | minimum fraction of floatpage that should have floats |   0.5   |

比较有效的方法是调整 `float` 对象可以占用页面的比例，而不至于占据整个页面

References:

1. [Avoid that figure gets its own page](https://tex.stackexchange.com/questions/68516/avoid-that-figure-gets-its-own-page)
2. [Controlling figure and table placement in LaTeX](https://robjhyndman.com/hyndsight/latex-floats/)

## tlmgr cannot setup tlpdb

    (running on Debian, switching to user mode!)
    Cannot determine type of tlpdb from /home/lqhuang/texmf!
    cannot setup TLPDB in /home/lqhuang/texmf at /usr/bin/tlmgr line 6424.

Solution:

    tlmgr init-usertree

Refs:

1. [tlmgr cannot setup TLPDB](https://tex.stackexchange.com/questions/137428/tlmgr-cannot-setup-tlpdb)

## Upgrade LaTex across major version

    (running on Debian, switching to user mode!)
    tlmgr: Remote repository is newer than local (2017 < 2018)
    Cross release updates are only supported with
        update-tlmgr-latest(.sh/.exe) --update
    Please see https://tug.org/texlive/upgrade.html for details.

Refs:

1. [TeX Live - Quick install](https://tug.org/texlive/quickinstall.html)

## Find missing packages/files

To search packages upon keyword, try

    tlmgr search --global --all beamer

To find a file flagged as missing try

    tlmgr search --global --file ptmr7t.mf.

Without --global, texlive will search only your local database, where the file
is obviously missing. Once the package found, you can install it

    tlmgr install thispackage

Refs:

1. [find-the-right-package-for-missing-files-in-texlive](https://tex.stackexchange.com/questions/274536/find-the-right-package-for-missing-files-in-texlive)

## Which is the best directory to keep my .sty files?

> If you want to install your own `.sty` files, then you should copy the files into the directory `tex/latex/mystuff` relative to a new [TEXMF root directory](https://miktex.org/kb/texmf-roots).
>
> Example (Mac/Linux):
>
> - Create a new TEXMF root: `mkdir ~/mytexmf`
> - Create a sub directory: `mkdir -p ~/mytexmf/tex/latex/mystuff`
> - Copy your `.cls` and/or `.sty `files to `~/mytexmf/tex/latex/mystuff`
> - Register the TEXMF root directory `~/mytexmf`

## Install a package by miktex

```sh
miktex package install package-id
miktex package list
# ...
# miktex package update
# miktex package upgrade
```

Refs:

- [`miktex-packages` — manage MiKTeX packages](https://docs.miktex.org/manual/miktex-packages.html)
