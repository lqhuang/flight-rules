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
