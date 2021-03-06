---
title: Tips for Docker or Container
created: 2019-04-02
updated: 2022-06-09
tags:
  - docker
  - container
---

## Communication between multiple docker-compose projects

method 1: set `external_links` for `docker-compose`

method 2:

As of compose file version 3.5:

This now works:

```yaml
version: "3.5"

services:
  proxy:
    image: user/image:tag
    ports:
      - "80:80"
    networks:
      - proxynet

networks:
  proxynet:
    name: custom_network
```

docker-compose up -d will join a network called 'custom_network'. If it doesn't
exist, it will be created!

ref:

1. https://stackoverflow.com/questions/38088279/communication-between-multiple-docker-compose-projects
2. https://docs.docker.com/compose/networking/

## Share Compose configurations between files and projects

References:

1. [Share Compose configurations between files and projects](https://docs.docker.com/compose/extends/)

## This system doesn't provide enough entropy

Way 1: mount /dev/urandom from the host as /dev/random into the container

    docker run -v /dev/urandom:/dev/random ...

Way 2: just install the `rng-tools` and run command `sudo rngd -r /dev/urandom`

## Access docker container from host using containers name

method 1: use `dns-proxy-server`

method 2: use `domainname` in `docker-compose.yml` or
`--hostname host.domain.com` for `docker run`

method 3: automatically update by
[script](https://stackoverflow.com/questions/36151981/local-hostnames-for-docker-containers)

method 4: `--add-host` for `docker run` / `extra_hosts` for compose file.

ref:

1. https://stackoverflow.com/questions/37242217/access-docker-container-from-host-using-containers-name
2. https://stackoverflow.com/questions/36151981/local-hostnames-for-docker-containers

## Docker daemon doesn't start on boot on CoreOS

it's very interesting that it doesn't start the docker daemon on startup.

It only starts when I SSH in and do `docker ps`

Then everything work fine again.

> Background:The root of this is because docker is socket activated on CoreOS,
> ie it doesn't block the boot chain. Early versions of docker were slow to
> start when you had lots of containers on disk which blocked everything that
> depended on docker from starting quickly, which caused some interesting
> failures. ??? Rob

solution 1:

    sudo systemctl enable docker

solution 2: using `cloud-init` script

```yaml
#cloud-config
coreos:
  units:
    - name: "docker.service"
      command: "start"
      enable: true
```

Refs

1. [docker-daemon-doesnt-start-on-boot-on-coreos](https://serverfault.com/questions/743087/docker-daemon-doesnt-start-on-boot-on-coreos)

## Environment variables in compose file

Both `$VARIABLE` and `${VARIABLE}` syntax are supported. Additionally when using
the 2.1 file format, it is possible to provide inline default values using
typical shell syntax:

- `${VARIABLE:-default}` evaluates to `default` if `VARIABLE` is unset or empty
  in the environment.
- `${VARIABLE-default}` evaluates to `default` only if `VARIABLE` is unset in
  the environment.

Similarly, the following syntax allows you to specify mandatory variables:

- `${VARIABLE:?err}` exits with an error message containing `err` if `VARIABLE`
  is unset or empty in the environment.
- `${VARIABLE?err}` exits with an error message containing `err` if `VARIABLE`
  is unset in the environment.

Other extended shell-style features, such as `${VARIABLE/foo/bar}`, are not
supported.

You can use a `$$` (double-dollar sign) when your configuration needs a literal
dollar sign. This also prevents Compose from interpolating a value, so a `$$`
allows you to refer to environment variables that you don???t want processed by
Compose.

References:

1. [Environment variables in Compose](https://docs.docker.com/compose/environment-variables)

## Understand how CMD and ENTRYPOINT interact

Both `CMD` and `ENTRYPOINT` instructions define what command gets executed when
running a container. There are few rules that describe their co-operation.

1. Dockerfile should specify at least one of `CMD` or `ENTRYPOINT` commands.
2. `ENTRYPOINT` should be defined when using the container as an executable.
3. `CMD` should be used as a way of defining default arguments for an
   `ENTRYPOINT` command or for executing an ad-hoc command in a container.
4. `CMD` will be overridden when running the container with alternative
   arguments.

The table below shows what command is executed for different `ENTRYPOINT` /
`CMD` combinations:

|                            | No ENTRYPOINT              | ENTRYPOINT exec_entry p1_entry | ENTRYPOINT ["exec_entry", "p1_entry"]          |
| -------------------------- | -------------------------- | ------------------------------ | ---------------------------------------------- |
| No CMD                     | error, not allowed         | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry                            |
| CMD ["exec_cmd", "p1_cmd"] | exec_cmd p1_cmd            | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry exec_cmd p1_cmd            |
| CMD ["p1_cmd", "p2_cmd"]   | p1_cmd p2_cmd              | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry p1_cmd p2_cmd              |
| CMD exec_cmd p1_cmd        | /bin/sh -c exec_cmd p1_cmd | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry /bin/sh -c exec_cmd p1_cmd |

Note: If `CMD` is defined from the base image, setting `ENTRYPOINT` will reset
`CMD` to an empty value. In this scenario, `CMD` must be defined in the current
image to have a value.

Refs:

1. [Understand how CMD and ENTRYPOINT interact](https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact)

## `ENV` variables would not be replaced in `ENTRYPOINT` and `CMD` part

Environment variables are supported by the following list of instructions in the
`Dockerfile`:

- `ADD`
- `COPY`
- `ENV`
- `EXPOSE`
- `FROM`
- `LABEL`
- `STOPSIGNAL`
- `USER`
- `VOLUME`
- `WORKDIR`
- `ONBUILD` (when combined with one of the supported instructions above)

But this replacement won't happen in `ENTRYPOINT` and `CMD` instructions. If you
want to eval them, you need use them as shell variable.

    ENTRYPOINT ["sh -c", "executable", "param1", "param2", "${VAR1}", "${VAR2}"]

or

    ENTRYPOINT executable param1 param2 ${VAR1} ${VAR2}

Refs:

1. [Environment replacement](https://docs.docker.com/engine/reference/builder/#environment-replacement)

## Scope of build-args (for Dockerfile or docker-compose.yml)

> ! Scope of build-args
>
> In your Dockerfile, if you specify `ARG` before the `FROM` instruction, `ARG`
> is not available in the build instructions under `FROM`. If you need an
> argument to be available in both places, also specify it under the `FROM`
> instruction. Refer to the understand how `ARGS` and `FROM` interact section in
> the documentation for usage details.
>
> ! Tip when using boolean values
>
> YAML boolean values (`"true"`, `"false"`, `"yes"`, `"no"`, "`on"`, `"off"`)
> must be enclosed in quotes, so that the parser interprets them as strings.

`FROM` instructions support variables that are declared by any `ARG`
instructions that occur before the first `FROM`.

```Dockerfile
ARG  CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD  /code/run-app

FROM extras:${CODE_VERSION}
CMD  /code/run-extras
```

Refs:

1. [Service configuration reference: build/args](https://docs.docker.com/compose/compose-file/compose-file-v3/#args)
2. [Understand how ARG and FROM interact](https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact)

## Get Docker container IP address in host machine

Refs:

1. [10 Examples of how to get Docker Container IP Address](http://networkstatic.net/10-examples-of-how-to-get-docker-container-ip-address)

## Get Docker container IP address inside container???

...

## Get host IP inside container

Get IPv4 address:

```sh
DOCKER_HOST=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')
```

Get IPv6 address:

S - IPv6 segment = [0-9a-f]{1,4}

```sh
# not test yet
DOCKER_HOST=$(ip -6 addr show docker0 | grep -Po 'inet6 \K(?:%[0-9a-z]+)')
```

Ref:

1. [Docker Tip #65: Get Your Docker Host's IP Address from in a Container](https://nickjanetakis.com/blog/docker-tip-65-get-your-docker-hosts-ip-address-from-in-a-container)
2. [How to get the IP address of the docker host from inside a docker container](https://stackoverflow.com/questions/22944631/how-to-get-the-ip-address-of-the-docker-host-from-inside-a-docker-container)

## Squash all build layers into one

`docker build --squash`: squash ???????????? Docker ????????????????????????????????? layers ???
???????????? layer??????????????????????????????????????? Docker image ???????????????????????????????????????
RUN ?????? clean ??????????????????????????????????????????????????????????????????????????????????????? image
?????? base image ???????????? pull ??? feature ????????????????????????

???????????????????????????????????????????????????

```
# yum
yum clean all
# dnf
dnf clean all
# rvm
rvm cleanup all
# gem
gem cleanup
# cpan
rm -rf ~/.cpan/{build,sources}/*
# pip
rm -rf ~/.cache/pip/*
# apt-get
apt-get clean
```

References:

1. [Docker ???????????????????????????](https://www.kawabangga.com/posts/4676)

## Keep your secrets during building

Do not use `ARG` to pass secrets in `Dockerfile`

> **Warning**:
>
> It is not recommended to use build-time variables for passing secrets like
> github keys, user credentials etc. Build-time variable values are visible to
> any user of the image with the `docker history` command. Refer to the ???Build
> images with BuildKit??? section to learn about secure ways to use secrets when
> building images.

To use `BuildKit`, enable this feature firstly,

    DOCKER_BUILDKIT=1 docker build --help

Add option `--secret id=some-id,src=path-to-env-file` to `docker build`, then
config how to use secrets in `Dockerfile`

    # shows secret from default secret location:
    RUN --mount=type=secret,id=some-id cat /run/secrets/some-id

    # shows secret from custom secret location:
    RUN --mount=type=secret,id=some-id,dst=/foobar/env-name cat /foobar/env-name

!!! Secrets will be only present in the mounted layer, which means you cannot
read that file again in all subsequent `RUN` commands !!!

References:

1. [Build Images with BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/#new-docker-build-secret-information)

## `/dev/shm`

WIP

<https://github.com/vercel/next.js/discussions/16995#discussioncomment-132484>

## Enable forwarding from Docker containers to the outside world

If you're using `docker compose` to manager multiple containers, you would find
Internet access inside services is not available under user-defined bridge
networks except for `network_mode: bridge`.

### Method 1: Enable all subnet

By default, traffic from containers connected to the default bridge network is
**not** forwarded to the outside world. To enable forwarding, you need to change
two settings. These are not Docker commands and they affect the Docker host???s
kernel.

1. Configure the Linux kernel to allow IP forwarding.

   sysctl net.ipv4.conf.all.forwarding=1

2. Change the policy for the `iptables` `FORWARD` policy from `DROP` to
   `ACCEPT`.

   sudo iptables -P FORWARD ACCEPT

These settings do not persist across a reboot, so you may need to add them to a
start-up script.

### Method 2: Add subnet manually

First custom your new created subnet

```yaml
networks:
  default:
    driver: bridge
    ipam:
      config:
        - subnet: 10.10.233.0/24
```

Then add `iptables` rules for this subnet manually,

```sh
DOCKER_SUB_IP="10.10.233.0/24"
iptables -A FORWARD -s ${DOCKER_SUB_IP} -j ACCEPT
iptables -A FORWARD -d ${DOCKER_SUB_IP} -j ACCEPT
iptables -t nat -A POSTROUTING -s ${DOCKER_SUB_IP} ! -d ${DOCKER_SUB_IP} -j MASQUERADE
```

You need to add every subnet you defined in compose file. Of course, you can
join a pre-existing network already finely configurated.

### References:

- [Enable forwarding from Docker containers to the outside world](https://docs.docker.com/network/bridge/#enable-forwarding-from-docker-containers-to-the-outside-world)
- [No internet inside docker-compose service](https://stackoverflow.com/a/68087771)

## Echo to docker logs output from shell script

Docker logs output from **whichever processs was used to launch the container**,
which is indeed PID 1. In some cases will use a "fake" init process so the main
process doesn't run as such, which is also the case if you use
`docker run --init`.

But you still can manually send output to the logs collector (PID 1's stdio
streams) within the container.

```sh
echo "text" >> /proc/1/fd/1  # fd/1 for stdout, fd/0 for stdin
echo "text" >> /proc/1/fd/2  # fd/2 for stderr
```

References:

1. [Redirecting script output to docker logs](https://stackoverflow.com/questions/55444469/redirecting-script-output-to-docker-logs)

## Run post-run actions in container

Sometimes, you probably want to do some extra actions (eg.: init db account,
start specific groups for supervisor, etc) after container started, but
container lacks specifications to execute post commands.

To achieve this, you could use a helper script through **jobs control mode**
from `bash`.

> If you have one main process that needs to start first and stay running but
> you temporarily need to run some other processes (perhaps to interact with the
> main process) then you can use bash???s job control to facilitate that. First,
> the wrapper script:

```bash
#!/bin/bash

# turn on bash's job control
set -m

# Start the primary process and put it in the background
./my_main_process &

# Start the helper process
./my_helper_process

# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns


# now we bring the primary process back into the foreground
# and leave it there
fg %1
```

Then add your script to `ENTRYPOINT`:

```dockerfile
ENTRYPOINT ["/path/to/entrypoint.sh"]
```

References:

1. [Run multiple services in a container](https://docs.docker.com/config/containers/multi-service_container/)

## Cache layers with BuildKit

If you're using a Docker version >= 19.03 you can use BuildKit to enable extra
features like external caches.

> In addition to local build cache, the builder can reuse the cache generated
> from previous builds with the `--cache-from` flag pointing to an image in the
> registry.
>
> To use an image as a cache source, cache metadata needs to be written into the
> image on creation. This can be done by setting
> `--build-arg BUILDKIT_INLINE_CACHE=1` when building the image. After that, the
> built image can be used as a cache source for subsequent builds.

- [Faster CI Builds with Docker Layer Caching and BuildKit](https://testdriven.io/blog/faster-ci-builds-with-docker-cache/)
- [`docker build`: Specifying external cache sources](https://docs.docker.com/engine/reference/commandline/build/#specifying-external-cache-sources)

## Docker Compose cheatsheet for ports

- Specify both ports (`HOST:CONTAINER`)
- Specify just the container port (an ephemeral host port is chosen for the host
  port).
- Specify the host IP address to bind to AND both ports (the default is
  `0.0.0.0`, meaning all interfaces): (`IPADDR:HOSTPORT:CONTAINERPORT`). If
  **HOSTPORT** is empty (for example `127.0.0.1::80`), an ephemeral port is
  chosen to bind to on the host.

```yaml
ports:
  - "3000"
  - "3000-3005"
  - "8000:8000"
  - "9090-9091:8080-8081"
  - "49100:22"
  - "127.0.0.1:8001:8001"
  - "127.0.0.1:5000-5010:5000-5010"
  - "127.0.0.1::5000"
  - "6060:6060/udp"
  - "12400-12500:1240"
```

References:

1. [Compose file version 3 reference: ports](https://docs.docker.com/compose/compose-file/compose-file-v3/#ports)
