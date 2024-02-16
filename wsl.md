---
title: Tips for WSL
created: 2024-01-10
updated: 2024-02-16
tags:
  - linux
  - windows
---

- [Debian sid with systemd on WSL2](https://gist.github.com/fardjad/7ee02761fdaa6b620e0ee8a715121883)
- [salsa.debian.org/debian/WSL](https://salsa.debian.org/debian/WSL): Build
  files for the debian app for the Windows Subsystem for Linux (WSL)
- [Windows Subsystem for Linux Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
  - [Basic commands for WSL](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)
  - [GPU accelerated ML training in WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gpu-compute)

## First of all: Enable WSL

```powershell
# In an elevated PowerShell session
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```

It requires a reboot for Windows system. After rebooting,

```powershell
# Install wsl
wsl --install
# This command wouldn't install concrete Linux distributions
```

Check available distribution

```powershell
# Remote
wsl --list --online
```

## Configure WSL

Two files are required to configure WSL.

- `/etc/wsl.conf`: WSL configuration file inside distribution
  - configurable options: `boot`(`systemd`), `automount`, `network`, `interop`,
    `user`
- `%UserProfile%\.wslconfig`: WSL configuration file for Windows
  - configurable options
    - `[wsl2]` - networking, firewall, dns, proxy, etc.
    - `[experimental]`

Both files do not exist by default.

Refs:

- [Advanced settings configuration in WSL](https://learn.microsoft.com/en-us/windows/wsl/wsl-config)

## How to daemonize without systemd in WSL

- [StackExchange: System has not been booted with systemd as init system (PID 1). Can't operate](https://askubuntu.com/questions/1379425/system-has-not-been-booted-with-systemd-as-init-system-pid-1-cant-operate/1379567)

## SSH Server for WSL

Install and start ssh server in WSL.

```sh
apt install ssh
service ssh start
```

Add boot command to `/etc/wsl.conf` to start ssh server at boot.

```conf
# in your `.wslconfig`
[boot]
command = service ssh start
```

- [Enable SSH in WSL system](https://askubuntu.com/questions/1339980/enable-ssh-in-wsl-system)
  - ssh @windows-host: wsl
- [The ssh instead of ssh in /etc/init.d](https://askubuntu.com/questions/1144447/the-ssh-instead-of-ssh-in-etc-init-d)
- [The is the "init" start/stop script for the OpenSSH server daemon "sshd"](http://www.styma.org/SunAtHome/sample_files/sshd.html)
- [Configuring SSH access into WSL 1 and WSL 2](https://jmmv.dev/2022/02/wsl-ssh-access.html)

## Expose WSL to the network

Though you have listened to `0.0.0.0`/`::` inside WSL 2, it is stilll not
exposed to public by default (network in NAT mode).

By now, you can use `netsh` in windows host to add a proxy to expose WSL ports.

```powershell
New-NetFirewallRule -Name 'OpenSSH-Server-In-WSL' -DisplayName 'OpenSSH Server (WSL)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 2222

netsh interface portproxy add v4tov4 listenport=2222 listenaddress=0.0.0.0 `
connectport=2222 connectaddress=$($(wsl hostname -I).Trim());
netsh interface portproxy show all
```

Don't forget to add firewall rule :)

Refs:

1. [Connecting to WSL2 server via local network [closed]](https://stackoverflow.com/a/74018117)

## Cons: Multiple WSL instances

Currently (2024-01-15), WSL 2 have no support for multiple instances.

> It does not say anything about being able to register the distribution under a
> given name. The only _documented_ way is to export the distro and re-import it
> under a different name.

- [How To Use Multiple WSL Instances For Development](https://wpclouddeploy.com/how-to-use-multiple-wsl-instances-for-development/)
- [Why isn't it possible to install multiple instances of a given distro without using hacks/workarounds? #9977](https://github.com/microsoft/WSL/issues/9977)
