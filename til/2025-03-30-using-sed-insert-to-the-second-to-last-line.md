---
title: Using sed to insert content into the second-to-last line of a file.
date: 2025-03-30
tags:
  - unix
---

`sed` could do more than just replace content. Acutally it has a richable script system.

```nginx
{
    ...
    {
        ...
    }
    include conf.d/*.conf  # position and content I hope to edit
}
```

For example, I recently want to insert a simple line into `nginx.conf` at the second-to-last line, `sed` is pretty suitable for that. With the help of manuals and stackoverflow, I completed it by

```
sed -i '$i \ \ \ \ include conf.d/*.conf;' nginx.conf
```

where `$` matchs the last line (LOL), `i` stands insert and `\ ` hints the space what I wanted.

The two main concepts in `sed` is Addresses (address or address-range) and Command.

With one or two more addresses, command will only be executed for input lines which match that addresses. Address-range type (seperates by comman `,`) is also well supported.

```sh
# Example: replace every occurrence of 'hello' with 'world' on lines 10-20
sed '10,20 s/hello/world/' input.txt > output.txt
```

Some interesting address

- `first~step` match every step'th line starting with line `first`. For example, `sed -n 1~2p` will print all the odd-numbered lines in the input stream
- `addr,+N` will match addr1 and the N lines following addr1

For the command, `s/regexp/replacement` is the famous and frequently used one. There're also other address commands like

- `a`: Append text
- `r filename`: Append text read from 'filename'
- `d`: Delete pattern space.

By scripting the addresses and command, `sed` is literally a powerful stream editor.

References:

1. [linux - sed, insert file before last line - Super User](https://superuser.com/questions/781558/sed-insert-file-before-last-line)
2. [sed(1) - Linux man page](https://linux.die.net/man/1/sed)
3. [sed.sf.net - The sed $HOME](https://sed.sourceforge.io/#scripts)
