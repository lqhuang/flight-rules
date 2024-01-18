---
title: CLI on Windows
created: 2018-11-03
updated: 2023-11-09
---

## Create a proxy to redirect network trafic origined to target host

重定向

```powershell
netsh interface portproxy add v4tov4 listenport=4000 listenaddress=127.0.0.1 connectport=4000 connectaddress=172.31.217.98
```

删除

```powershell
netsh interface portproxy del v4tov4 listenport=4000 listenaddress=127.0.0.1
```

查看已存在的端口映射

```powershell
netsh interface portproxy show v4tov4
netstat -ano | find 4000
```

- [Can I redirect/route IP adress to another IP address (windows)](https://serverfault.com/questions/712970/can-i-redirect-route-ip-adress-to-another-ip-address-windows)

## UTC Timestamp issue when dual booting Windows and Linux

While Debian prefer to keep the hardware clock in UTC (this prevents the need to
change it on daylight savings and timezone changes) other systems (like Windows)
by default keeps the hardware clock synchronized to local time.

To fix this issue, you can either update `timedatectl` to use local time (not
recommended already) or update Windows to use UTC time instead of local time.

Save the following content to a file with `.reg` extension

```reg
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation]
"RealTimeIsUniversal"=dword:00000001
```

and double click it to import the registry settings. Reboot Windows to take the
change effect.

Refs:

1. [Debian Wiki: Hardware clock and system time when dual booting](https://wiki.debian.org/DateTime#Hardware_clock_and_system_time_when_dual_booting)
2. [Does Windows 7 support UTC as BIOS time?](https://superuser.com/questions/185773/does-windows-7-support-utc-as-bios-time)

## Print ip route table

```powershell
route print
```

## Windows change default shell to powershell

On the server side, configure the default ssh shell in the windows registry.

- `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\OpenSSH\DefaultShell` - full path of the
  shell executable.
- `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\OpenSSH\DefaultShellCommandOption`
  (optional) - switch that the configured default shell requires to execute a
  command, immediately exit and return to the calling process. By default this
  is `-c`. Powershell cmdlets to set powershell bash as default shell
- `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\OpenSSH\DefaultShellEscapeArguments`
  (optional) - flag that allow you to skip escaping the arguments of default
  shell. By default this is `0`. This option is only applicable to shells other
  than `powershell`, `bash`, `cygwin`, `cmd`, and `ssh-shellhost.exe`.

```powershell
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -PropertyType String -Force
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShellCommandOption -Value "/c" -PropertyType String -Force
```

Refs:

1. [Win32-OpenSSH Wiki: DefaultShell](https://github.com/PowerShell/Win32-OpenSSH/wiki/DefaultShell)

## OpenSSH utility scripts to fix file permissions

OpenSSH is already available in Windows 10 1803 and later. However, it may cause
some issues when using pubkey to connect from other hosts. The following scripts
can be used to fix the file permissions.

```powershell
Import-Module .\OpenSSHUtils.psd1 -Force
Repair-AuthorizedKeyPermission -FilePath %systemdrive%\Users\<user>\.ssh\authorized_keys
```

Double check access permissions on authorized_keys (only System, Administrators
and owner can have access).

```powershell
icacls %systemdrive%\Users\<user>\.ssh\authorized_keys
```

If `sshd_config` is modified then restart the sshd service

```powershell
net stop sshd
net start sshd
```

Check the references for more details.

Refs:

1. [OpenSSH utility scripts to fix file permissions](https://github.com/PowerShell/Win32-OpenSSH/wiki/OpenSSH-utility-scripts-to-fix-file-permissions)
2. [ssh.exe examples: Setup server-side (`sshd`)](https://github.com/PowerShell/Win32-OpenSSH/wiki/ssh.exe-examples#setup-server-side-sshd)

## Windows 10 / Windows 11: Outdated audio driver make the system unstable and cause BSOD

> If you’re having issues with BSODs and other errors/maybe even really bad
> frame rate. It’s probably your Realtek audio driver I’ve had this issue on
> multiple PCs and it’s always been the Realtek audio. To fix it you could try
> reinstalling the driver but I’ve had no luck with that. What’s worked for me
> is using one of five drivers.
>
> 1. Old driver from Realtek site probably not recommended as it’s the old
>    control panel also and not even made for windows 11 but still works.
> 2. Generic high definition audio driver may not have all the features though
> 3. Realtek-UAD-generic driver on GitHub it should equivalent to your default
>    driver just much newer.
> 4. AAF Optimus driver has a lot more features then the stock driver and could
>    enhance your audio quality
> 5. Just disable Realtek audio if you have no use for it

I had the very similar issue and I simply disable my onboard audio device in
BIOS, then things work fine now.

Refs:

- [ PSA: If you’re having issues after the 23H2 update please read ](https://www.reddit.com/r/windows/comments/17p9toh/psa_if_youre_having_issues_after_the_23h2_update/)
