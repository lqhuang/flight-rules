---
title: X Behind Proxy
date: 2019-01-24
tags:
  - linux
  - dev
  - til
---

This article shows how to configure a forward proxy in different environments
and software. 😭

## Environment variables in unix-like system

Add following lines into your `~/.bashrc` or `~/.zshrc`

```sh
export http_proxy=http://username@password:localhost:8118
export https_proxy=http://username@password:localhost:8118
# 172.16.0.0/12 means address range from 172.16.x.x to 172.31.x.x
export no_proxy="localhost, 127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16"
# export no_proxy="::1,fd00::/8" # https://en.wikipedia.org/wiki/Private_network
```

## APT package manager in Debian/Ubuntu

### apt conf

Create file `/etc/apt/apt.conf.d/proxy.conf` and add following configuration:

    Acquire::http::Proxy "http://USER@PASSWD:PROXYHOST:PORT";
    Acquire::https::Proxy "http://USER@PASSWD:PROXYHOST:PORT"
    Acquire::socks::Proxy "socks://[username]:[password]@[webproxy]:[port]/";

### visudo

In some releases sudo is configured in such a way that all environment variables
all cleared when running the command. To keep the value for your http_proxy and
fix this, you need to edit `/etc/sudoers`, run:

```sh
visudo
```

Then find a line that states:

    Defaults env_reset

and add after it:

    Defaults env_keep = "http_proxy ftp_proxy"

Things will start working as expected.

In order to not only fix apt-get but also graphical X11 utils as (e.g synaptic,
mintintall, ...), the following line in `/etc/sudoers` should do the job :

    Defaults env_keep = "http_proxy https_proxy ftp_proxy DISPLAY XAUTHORITY"

## Connect with SSH through a proxy

via cli:

```sh
ssh USER@DEST -o "ProxyCommand=nc -X connect -x PROXYHOST:PROXYPORT %h %p"
```

edit `~/.ssh/config`:

```ssh-config
Host github.com
    HostName  github.com
    User      git
    Port      22
    # ProxyCommand=nc -X connect -x PROXYHOST:PROXYPORT %h %p
    ProxyCommand ncat --proxy 127.0.0.1:1080 %h %pssh-err.log
    ServerAliveInterval 30
    IdentityFile ~\.ssh\github_key
    ForwardX11 yes

# Inside the firewall
Host *
    ProxyCommand nc -X connect -x PROXYHOST:PROXYPORT %h %p
    ServerAliveInterval 30
    ## Speed up SSH session creation
    ## by sharing multiple sessions over a single network connection
    ## reuse already established TCP connection
    # ControlMaster auto  # enables the sharing of multiple sessions over a single network connection.
    # ControlPath ~/.ssh/sockets/%r@%h-%p  # defines a path to the control socket used for connection sharing.
    # ControlPersist 600  # if used together with ControlMaster, tells ssh to keep the master connection open in the background (waiting for future client connections) once the initial client connection has been closed.
    ## macOS Sierra - add passphrases to keychain
    # UseKeychain yes
```

Refs:

1. [Connect with SSH through a proxy](https://stackoverflow.com/questions/19161960/connect-with-ssh-through-a-proxy)
2. [ssh through authentication requiring proxy](https://unix.stackexchange.com/questions/447780/ssh-through-authentication-requiring-proxy)

## SBT behind proxy

1. Using environment variables `JAVA_OPTS` or `SBT_OPTS`:

```sh
export JAVA_OPTS="$JAVA_OPTS -Dhttp.proxyHost=yourserver -Dhttp.proxyPort=8080 -Dhttp.proxyUser=username -Dhttp.proxyPassword=password"
```

2. Set when call:

```sh
sbt -Dhttps.proxyHost=yourserver -Dhttps.proxyPort=8080
```

3. Edit `sbt/sbtconfig.txt`:

```sh
-Dhttp.proxyHost=PROXYHOST
-Dhttp.proxyPort=PROXYPORT
-Dhttp.proxyUser=USERNAME
-Dhttp.proxyPassword=XXXX

-Dhttps.proxyHost=PROXYHOST
-Dhttps.proxyPort=PROXYPORT
-Dhttps.proxyUser=USERNAME
-Dhttps.proxyPassword=XXXX
```

Refs:

1. [How to use sbt from behind proxy?](https://stackoverflow.com/questions/13803459/how-to-use-sbt-from-behind-proxy)
2. [Java Docs Networking Properties](https://docs.oracle.com/javase/8/docs/api/java/net/doc-files/net-properties.html)
3. [Setup-Notes](https://www.scala-sbt.org/1.x/docs/Setup-Notes.html)

## Docker

### Start a new container

Set the proxy environment variables when starting the container.

```shell
docker run \
    -e HTTP_PROXY=http://username:password@proxy2.domain.com \
    -e HTTPS_PROXY=http://username:password@proxy2.domain.com \
    target-image
```

To verify if the configuration is working, start a container and print its env:

```sh
docker run --rm busybox env
```

Refs:

1. [How to configure docker container proxy?](https://stackoverflow.com/questions/47827496/how-to-configure-docker-container-proxy)

### inside a container

Create or edit the file `~/.docker/config.json` in the home directory of the
user which starts containers. Add JSON such as the following, substituting the
type of proxy with `httpsProxy`, `ftpProxy` or `noProxy`.

When you create or start new containers, the environment variables are set
automatically within the container.

```json
{
  "proxies": {
    "default": {
      "httpProxy": "http://127.0.0.1:3001",
      "httpsProxy": "http://127.0.0.1:3001",
      "noProxy": "*.test.example.com,.example2.com"
    }
  }
}
```

Refs:

- [Configure Docker to use a proxy server](https://docs.docker.com/network/proxy/)

### docker daemon

The Docker daemon uses the `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`
environmental variables in its start-up environment to configure HTTP or HTTPS
proxy behavior. You cannot configure these environment variables using the
daemon.json file.

This example overrides the default docker.service file.

If you are behind an HTTP or HTTPS proxy server, for example in corporate
settings, you need to add this configuration in the Docker systemd service file.

1. Create a systemd drop-in directory for the docker service:

```sh
sudo mkdir -p /etc/systemd/system/docker.service.d
```

2. Create a file named

```
/etc/systemd/system/docker.service.d/http-proxy.conf
```

that adds the `HTTP_PROXY` environment variable:

```systemd
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:80/" "HTTPS_PROXY=https://proxy.example.com:443/" "NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
```

3. Flush changes:

```sh
sudo systemctl daemon-reload
```

4. Restart Docker:

```sh
sudo systemctl restart docker
```

5. Verify that the configuration has been loaded:

```sh
systemctl show --property=Environment docker
```

Refs:

- [Control Docker with systemd](https://docs.docker.com/config/daemon/systemd/)

## Snap

First one, snapd reads `/etc/environment`, so setting the usual proxy
environment variables there works. On Ubuntu, that's done automatically for you
by Settings -> Network -> Network proxy, so as long as you restart snapd after
changing that file you should be set.

```sh
http_proxy=http://PROXYHOST:PORT
https_proxy=http://PROXYHOST:PORT
```

Second one, create a drop-in configuration for `snapd.service`

    sudo systemctl edit snapd.service

Add in the following:

```systemd
[Service]
Environment=http_proxy=http://proxy:port
Environment=https_proxy=http://proxy:port
```

After execute one of two options, restart service to apply changes,

```sh
sudo systemctl restart snapd
```

Refs:

1. [How to install snap packages behind web proxy on Ubuntu 16.04](https://askubuntu.com/questions/764610/how-to-install-snap-packages-behind-web-proxy-on-ubuntu-16-04)
2. [Snap Store Proxy documentation](https://docs.ubuntu.com/snap-store-proxy/en/)

## npm behind proxy

Usually, npm will read your environment variables `http_proxy` and
`https_proxy`.

But you still could set individual proxy by adding lines to your `~/.npmrc`:

    maxsockets=1  # sometimes proxy server has a limit of max connections
    proxy=http://[username]:[password]@[proxyhost]:[port]
    https-proxy=http://[username]:[password]@[proxyhost]:[port]
    noproxy="localhost,127.0.0.1,192.168.*.*"

## full list of private network

IPv4:

    localhost;
    127.*;
    # 10.0.0.0/8
    10.*;
    # 172.16.0.0/12
    172.16.*;172.17.*; ...; 172.30.*;172.31.*;
    # 192.168.0.0/16
    192.168.*

## Awesome list (appended at: 2023-02-26)

顺便推荐一个 proxy settings 和一个 mirrors 的列表

- [comwrg/package-manager-proxy-settings](https://github.com/comwrg/package-manager-proxy-settings):
  记录各个包管理器代理设置坑点。
- [eryajf/Thanks-Mirror](https://github.com/eryajf/Thanks-Mirror): 整理记录各个
  包管理器，系统镜像，以及常用软件的好用镜像，Thanks Mirror。
