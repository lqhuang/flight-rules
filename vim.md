---
title: Vim Tips
created: 2019-12-04
updated: 2023-01-14
---

## Save with root permission

    :w !sudo tee %
    :w !sudo tee > /dev/null %

References:

1. [How does the vim "write with sudo" trick work?](https://stackoverflow.com/questions/2600783/how-does-the-vim-write-with-sudo-trick-work)

## Delete to end of line

Short tips:

- Delete to end of line: `d$`/`D`
- Delete to end of line **and** turn into `INSERT` mode: `c$`/`C`

Long explains:

`d$` will delete from the current cursor position to the end of the current
line. `D` (uppercase D) is a synonym for `d$` (lowercase D + dollar sign).

`$` moves to the end of the line (memonic: likes in regexps). So `d$` deletes to
the end of the line. Similarly, `e` moves to the end of the current word, and
`w` moves to the beginning of the next word, hence `de` deletes the end of the
current word, and `dw` additionally deletes the following whitespace.

Ref:

- [Delete from cursor to end of line in `vi`](https://unix.stackexchange.com/questions/4415/delete-from-cursor-to-end-of-line-in-vi)
