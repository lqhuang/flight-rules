---
title: LaTex Notes
created: 2017-02-13
updated: 2022-02-24
---

# latex-flight-rules and latex-tips

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

Without --global, texlive will search only your local database, where the file is obviously missing. Once the package found, you can install it

    tlmgr install thispackage

Refs:

1. [find-the-right-package-for-missing-files-in-texlive](https://tex.stackexchange.com/questions/274536/find-the-right-package-for-missing-files-in-texlive)
