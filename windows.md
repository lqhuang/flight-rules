---
title: CLI on Windows
created: 2018-11-03
updated: 2018-11-03
---

## Create a proxy to redirect network trafic origined to target host

重定向

```shell
netsh interface portproxy add v4tov4 listenport=4000 listenaddress=127.0.0.1 connectport=4000 connectaddress=172.31.217.98
```

删除

```shell
netsh interface portproxy del v4tov4 listenport=4000 listenaddress=127.0.0.1
```

查看已存在的端口映射

```shell
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
