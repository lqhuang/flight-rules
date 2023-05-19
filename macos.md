---
title: Tips for macOS
created: 2023-01-29
updated: 2023-05-16
---

## Resources

- [Gist - macOS Internals](https://gist.github.com/kconner/cff08fe3e0bb857ea33b47d965b3e19f)

## Remove `.DS_Store` via Terminal

Recursively remove all `.DS_Store` files from your machine

```sh
sudo find / -name ".DS_Store" -depth -exec rm {} \;
```

To do the same thing for a specific directory only:

```sh
find . -name '*.DS_Store' -type f -delete
```

Disable `.DS_Store` on external drives. Note that you may need to log out and/or
restart your machine after executing this command.

```sh
defaults write com.apple.desktopservices DSDontWriteNetworkStores true
```

Ref:

- [Remove .DS_Store in macOS](https://wp-mix.com/remove-ds_store-in-macos/)

## Configure repeat scheduled power events (`sleep`/`wakeup`/`shutdown`) in macOS 13 Ventura

Ventura (macOS 13) has removed scheduled `sleep`/`wakeup`/`shutdown`, but CLI
interface to set **repeat** scheduled power events is still supported for now.

The usage is

```shell
# man pmset
sudo pmset repeat type weekdays HH:mm:ss
# type - one of sleep, wake, poweron, shutdown, wakeorpoweron
# weekdays - a subset of MTWRFSU ("M" and "MTWRF" are valid strings)
```

For example, if you want your Mac to sleep at 11:30 a.m every weekday, change
the command to:

```sh
sudo pmset repeat sleep MTWRF 11:30:00.
```

Here,

- M: Monday
- T: Tuesday
- W: Wednesday
- R: Thursday
- F: Friday
- S: Saturday
- U: Sunday

Another example for combination of `wakeorpoweron`/`sleep`

```
sudo pmset repeat wakeorpoweron T 12:00:00 sleep MTWRFSU 20:00:00
```

Cancel "repeat" schedules

```sh
sudo pmset repeat cancel
```

Check current scheduled events from cli

```sh
pmset -g sched
```

Or you could find the same info in the app System Information (tab: Hardware ->
Power)

Refs:

- [How to Change macOS Sleep Settings? (Ventura Updated)](https://iboysoft.com/news/how-to-change-macos-sleep-settings.html)
- [Schedule Mac To Shutdown, Sleep, Wake in Ventura (Examples)](https://www.howtoisolve.com/how-to-schedule-mac-turn-on-off-and-sleep-wake/)

## macOS doesn't source `~/.bashrc` when open a new terminal

TL;DR: In masOS, `.bash_profile` is used instead of `.bashrc`.

Why?:

`.[bash_]profile` and `.bashrc` can be used on both macOS and Linux. The former
is loaded when the shell is a **login shell**; the latter when it is not. But

- Linux runs a login shell when the user logs into a graphical session, and
  then, when you open a terminal application, those shells are **non-login**
  shells.
- Whereas macOS does not run a shell upon graphical login, and when you run a
  shell from `Terminal.app`, that is a **login** shell.

For bash, when a "login shell" starts up, it reads the file

- `/etc/profile` (must)

1. `~/.bash_profile`
2. `~/.bash_login`
3. `~/.profile`

**For the last three configs, whichever one exists, it only reads one of these,
checking for them in the order mentioned**

Then when a login shell exits, bash reads and executes commands from the file
`~/.bash_logout`, if it exists.

When an **interactive** shell that is **not a login** shell is started,, it
reads the file

- `/etc/bashrc`
- `~/.bashrc`

(That's why Linux doesn't use `~/.bash_profile`)

Note that when bash is invoked with the name "sh", it tries to mimic the startup
sequence of the Bourne shell ("sh") as closely as possible. In particular, a
non-login shell invoked as "sh" does not read any dot files by default.

When you start a new Terminal window, the shell that is started is a "login
shell".

When you start a sub-shell (by typing a shell's name at the command-prompt), you
get a "non-login shell".

For example, using `bash` to create a new shell (non-login shell) will not load
`.bash_profile`, but using `tmux` to create a new terminal (login shell) will
load `.bash_profile`.

macOS is unusual in that it runs **each terminal session** as a login shell.
Typically, most other versions of unix and linux will encounter a login shell
only if either:

- They logged in from a tty, not through a GUI.
  - In this case, `.bash_profile` will not be sourced.
- They logged in remotely, such as through SSH
  - Yeah, it load `.bash_profile` first.

> If you want your aliases to work in both login and non-login shells (and you
> usually do), you should put them in `.bashrc` and source `.bashrc` in your
> `.bash_profile`, with a line like this:
>
> ```bash
> [ -r ~/.bashrc ] && . ~/.bashrc
> ```
>
> This applies to any system using bash.

However, what shouble be notable is, accessing macOS from SSH, macOS still
doesn't source `.bashrc` either (explained above). Also, there is a big
differnce between ZSH and BASH. If `.zprofile` and `.zshrc` both exist, macOS
zsh will load them both in sequence.

For ZSH, commands are first read from `/etc/zshenv`, this cannot be overridden.
Commands are then read from `~/.zshenv`.

If the shell is a login shell, commands are read from `/etc/zprofile` and then
`~/.zprofile`. Then, if the shell is interactive, commands are read from
`/etc/zshrc` and then `~/.zshrc`.

Finally, if the shell is a login shell, `/etc/zlogin` and `~/.zlogin` are read.
When a login shell exits, the files `~/.zlogout` and then `/etc/zlogout` are
read.

Why there are both `~/.zprofile` and `~/.zlogin`, when they are both for login
shells: the answer is the obvious one, that one is run before, one after
`~/.zshrc`.

In macOS (not for other UNIX distribution), most time you're using interactive
shell and the general startup order is:

1. `/etc/zshenv`
2. `~/.zshenv`
3. `/etc/zprofile`
4. `~/.zprofile`
5. `/etc/zshrc`
6. `~/.zshrc`
7. `/etc/zlogin`
8. `~/.zlogin` ... Init completed.
9. `~/.zlogout`
10. `/etc/zlogout`

Refs:

1. [Mac OS X .bashrc not working](https://superuser.com/questions/244964/mac-os-x-bashrc-not-working)
2. [Why doesn't .bashrc run automatically?](https://apple.stackexchange.com/questions/12993/why-doesnt-bashrc-run-automatically)
3. [What startup files are read by the shell? (shell configuration)](http://hayne.net/MacDev/Notes/unixFAQ.html#shellStartup)
4. [How-to: Terminal/profile startup files in macOS](https://ss64.com/osx/syntax-profile.html)

## ZSH: What is meant by an interactive and a login shell.

After my searching, I think in ZSH there probably is no `login` or `non-login`
shell, but `interactive` and `non-interactive` shell.

> macOS is unusual in that it runs **each terminal session** as a login shell.

This makes sense?

> Basically, the shell is just there to take a list of commands and run them; it
> doesn't really care whether the commands are in a file, or typed in at the
> terminal. In the second case, when you are typing at a prompt and waiting for
> each command to run, the shell is **interactive**; in the other case, when the
> shell is reading commands from a file, it is, consequently,
> **non-interactive**. A list of commands used in this second way --- typically
> by typing something like `zsh filename`, although there are shortcuts --- is
> called a **script**, as if the shell was acting in a play when it read from it
> (and shells can be real hams when it comes to playacting). When you start up a
> script from the keyboard, there are actually two zsh's around: the interactive
> one you're typing at, which is waiting for another, non-interactive one to
> finish running the script. Almost nothing that happens in the second one
> affects the first; they are different copies of zsh.

For example, `zsh` will open an interactive shell in terminal, but
`zsh -c 'echo "hi"'` or `zsh filename` run scripts in a non-interactive shell

Simple tests to know whether is a login shell

```bash
if [[ -o login ]]; then; print yes; else; print no; fi
```

Ok, fine, I found similar and detail explaniation from BASH Guide

> A **login** shell is one whose first character of argument zero is a `-`, or
> one started with the `--login` option.
>
> An **interactive** shell is one started without non-option arguments and
> without the `-c` option whose standard input and error are both connected to
> terminals (as determined by `isatty(3)`), or one started with the `-i` option.
> `PS1` is set and `$-` includes `i` if `bash` is interactive, allowing a shell
> script or a startup file to test this state.

Refs:

- [ZSH Guide Chapter 2: What to put in your startup files](https://zsh.sourceforge.io/Guide/zshguide02.html)
- Bash Manual

## Questions still: What about non-interactive but login shell?

- non-interactive + login
- non-interactive + non-login

...

## Create a password-protected zip archive on macOS

Yeah, you cannot do it with GUI. Open terminal and then

```bash
zip -er archive.zip /content-you-wanna-compress
```

Terminal will show a prompt to let you confirm your secret.

## Diving into a hidden macOS tool - networkQuality

The networkQuality tool is a built-in tool released in macOS Monterey that can
help diagnose network issues and measure network performance.

```sh
networkQuality -v
```

This command starts the tool and performs the default set of tests, displaying
the results in the Terminal window.

```
=== SUMMARY ====
Uplink capacity: 4.140 Mbps (Accuracy: High)
Downlink capacity: 736.244 Mbps (Accuracy: High)
Responsiveness: Low (90 RPM) (Accuracy: High)
Idle Latency: 122.667 milliseconds (Accuracy: High)
Interface: lo0
Uplink bytes transferred: 21.890 MB
Downlink bytes transferred: 1.127 GB
Uplink Flow count: 8
Downlink Flow count: 16
Start: 5/16/23, 16:44:44
End: 5/16/23, 16:45:00
OS Version: Version 13.3.1 (a) (Build 22E772610a)
```

Usage

```
USAGE: networkQuality [-C <configuration_url>] [-c] [-h] [-I <network interface name>] [-k] [-p] [-r host] [-s] [-v]
    -C: override Configuration URL or path (with scheme file://)
    -c: Produce computer-readable output
    -h: Show help (this message)
    -I: Bind test to interface (e.g., en0, pdp_ip0,...)
    -k: Disable certificate validation
    -p: Use Private Relay
    -r: Connect to host or IP, overriding DNS for initial config request
    -s: Run tests sequentially instead of parallel upload/download
    -v: Verbose output
```

Even more, it allow you to create your own server as test server.

- [Diving into a hidden macOS tool - networkQuality](https://cyberhost.uk/the-hidden-macos-speedtest-tool-networkquality/)
