---
title: Tips for WSL
created: 2024-01-10
updated: 2024-01-21
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

- https://askubuntu.com/questions/1339980/enable-ssh-in-wsl-system
  - ssh @windows-host: wsl
- https://www.ibm.com/docs/en/tnpm/1.4.5?topic=ss-configure-openssh-server-start-up-system-boot
- https://exampleconfig.com/view/openssh-centos6-etc-rc-d-init-d-sshd
- https://askubuntu.com/questions/1144447/the-ssh-instead-of-ssh-in-etc-init-d
- http://www.styma.org/SunAtHome/sample_files/sshd.html
- https://jmmv.dev/2022/02/wsl-ssh-access.html

## Cons: Multiple WSL instances

Currently (2024-01-15), WSL 2 have no support for multiple instances.

> It does not say anything about being able to register the distribution under a
> given name. The only _documented_ way is to export the distro and re-import it
> under a different name.

- https://wpclouddeploy.com/how-to-use-multiple-wsl-instances-for-development/
- https://github.com/microsoft/WSL/issues/9977
