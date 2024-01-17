---
title: Tips for Docker or Container
created: 2019-04-02
updated: 2024-01-17
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

Way 1: mount `/dev/urandom` from the host as `/dev/random` into the container

    docker run -v /dev/urandom:/dev/random ...

Way 2: just install the `rng-tools` and run command `sudo rngd -r /dev/urandom`

## Access docker container from host using containers name

Method 1: use `dns-proxy-server`

Method 2 (recommend!): use `hostname` in `docker-compose.yml` or
`--hostname host.domain.com` for `docker run`

Method 3: automatically update by
[script](https://stackoverflow.com/questions/36151981/local-hostnames-for-docker-containers)

Method 4: `--add-host` for `docker run` / `extra_hosts` for compose file.

ref:

1. [Access docker container from host using containers name](https://stackoverflow.com/questions/37242217/access-docker-container-from-host-using-containers-name)
2. [Local hostnames for Docker containers](https://stackoverflow.com/questions/36151981/local-hostnames-for-docker-containers)

## Docker daemon doesn't start on boot on CoreOS

it's very interesting that it doesn't start the docker daemon on startup.

It only starts when I SSH in and do `docker ps`

Then everything work fine again.

> Background:The root of this is because docker is socket activated on CoreOS,
> ie it doesn't block the boot chain. Early versions of docker were slow to
> start when you had lots of containers on disk which blocked everything that
> depended on docker from starting quickly, which caused some interesting
> failures. – Rob

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
allows you to refer to environment variables that you don’t want processed by
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

## Get Docker container IP address inside container?

...

## Get host IP inside or outside container

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

### Hard codes sometimes work

> Sometimes hard code is also work. AFAIK, in the case of Docker for Linux
> (standard distribution), the IP address of the host will always be
> `172.17.0.1`.

Based on this thought, we could check from host to get default HOST IP.

```
docker network inspect bridge -f '{{range .IPAM.Config}}{{.Gateway}}{{end}}'
```

Refs:

1. [Docker Tip #65: Get Your Docker Host's IP Address from in a Container](https://nickjanetakis.com/blog/docker-tip-65-get-your-docker-hosts-ip-address-from-in-a-container)
2. [How to get the IP address of the docker host from inside a docker container](https://stackoverflow.com/questions/22944631/how-to-get-the-ip-address-of-the-docker-host-from-inside-a-docker-container)
3. [How to get the IP address of the docker host from inside a docker container](https://stackoverflow.com/a/67160733)

### Updated solution from official implementation

In the past, `host.docker.internal` was a host alias for the gateway IP address
inside of Docker, but only worked on Docker Desktop for macOS/Windows. Now,
`host.docker.internal` is available on Linux, too. However, version `20.10.0` of
Docker was released in December 2020, and the subsequent versions support using
the `host.docker.internal` command to connect to the host on Linux machines.

Through this alias, you still you need to provide the following run flag

```sh
docker run ... --add-host=host.docker.internal:host-gateway ...
```

or configure it in compose file

```yaml
services:
  app:
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

The `--add-host` flag supports a special `host-gateway` value that resolves to
the internal IP address of the host. This is useful when you want containers to
connect to services running on the host machine.

> [!Note] If you have set port mapping `127.0.0.1:8080:8080`, you probably
> cannot access that container by `host.docker.internal:80` from other
> containers. You need to use `172.17.0.1:8080:8080` instead, where the
> `172.17.0.1` is the gateway IP address of `bridge` network.

> [!Warning] `host.docker.internal` or `gateway.docker.internal` both are the
> special DNS name and only **natively** supported on Docker Desktop for macOS
> and Windows.

Refs:

1. [How to connect to the Docker host from inside a Docker container?](https://medium.com/@TimvanBaarsen/how-to-connect-to-the-docker-host-from-inside-a-docker-container-112b4c71bc66)
2. [Reference / Command-line reference / Docker CLI / docker run](https://docs.docker.com/engine/reference/commandline/run/#add-host)
3. [Host Docker Internal in Linux](https://www.delftstack.com/howto/docker/host-docker-internal/)

## Minimize the number of layers

In older versions of Docker, it was important that you minimized the number of
layers in your images to ensure they were performant. The following features
were added to reduce this limitation:

- **Important** Only the instructions `RUN`, `COPY`, and `ADD` create layers.
  Other instructions create temporary intermediate images, and don't increase
  the size of the build.
- Where possible, use multi-stage builds, and only copy the artifacts you need
  into the final image. This allows you to include tools and debug information
  in your intermediate build stages without increasing the size of the final
  image.

Ref:

1. [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#minimize-the-number-of-layers)

## Squash all build layers into one

`docker build --squash`: squash 功能会在 Docker 完成构建之后，将所有的 layers 压
缩成一个 layer，也就是说，最终构建出来的 Docker image 只有一层。所以，如上在多个
RUN 中写 clean 命令，其实也可以。我不太喜欢这种方式，因为前文提到的，多个 image
共享 base image 以及加速 pull 的 feature 其实就用不到了。

一些常见的包管理器删除缓存的方法：

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

1. [Docker 镜像构建的一些技巧](https://www.kawabangga.com/posts/4676)

## Keep your secrets during building

Do not use `ARG` to pass secrets in `Dockerfile`

> **Warning**:
>
> It is not recommended to use build-time variables for passing secrets like
> github keys, user credentials etc. Build-time variable values are visible to
> any user of the image with the `docker history` command. Refer to the "Buil"
> images with BuildKit” section to learn about secure ways to use secrets when
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

## Enable forwarding from Docker containers to the outside world

If you're using `docker compose` to manager multiple containers, you would find
Internet access inside services is not available under user-defined bridge
networks except for `network_mode: bridge`.

### Method 1: Enable all subnet

By default, traffic from containers connected to the default bridge network is
**not** forwarded to the outside world. To enable forwarding, you need to change
two settings. These are not Docker commands and they affect the Docker host’s
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
> main process) then you can use bash’s job control to facilitate that. First,
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

## Add CA Certificates to Alpine image

```shell
apk add --no-cache ca-certificates && update-ca-certificates
```

## `shm_size`

> What is `/dev/shm`? `/dev/shm` is nothing but implementation of traditional
> **shared memory** concept. It is an efficient means of passing data between
> **processes**.
>
> `shm` / `shmfs` is also known as `tmpfs`, which is a common name for a
> temporary file storage facility on many Unix-like operating systems. It is
> intended to appear as a mounted file system, but one which uses virtual memory
> instead of a persistent storage device.

In container, `shm_size` could be set in both build and run stage. Increasing
`shm_size` may improve serveral programs' perfomace which affected by IPC (inter
process communication).

For example:

1. PostgreSQL is an process-based parallel model, so `shm_size` is important
   when `postgresql` is running inside of docker.

2. Cache for nodejs application and reduce bundling size

   > Before `RUN yarn install --production`, you can also add
   > `ENV YARN_CACHE_FOLDER=/dev/shm/yarn_cache`. This will reduce the size of
   > the final image because it will no longer contain unneeded archives in yarn
   > cache dir. It is something like `~/.yarn/cache` by default, while
   > `/dev/shm` is a temp folder that’s not included in the image.

   > By default, the size of `/dev/shm` is quite small so you might end up with
   > "no space on disk" error when running yarn install. Adding `--shm-size 1G`
   > to docker build command solves this.

   > Adding `--frozen-lockfile` to yarn install is also a good idea. This
   > argument makes sure that the dependencies you end up with are what you
   > expect them to be.

   > Similarly to `--frozen-lockfile`, `npm ci --only-production` is also a good
   > idea. The main benefit is if dependencies in the package lock do not match
   > those in package.json, npm ci will exit with an error, instead of updating
   > the package lock.

Refs:

- [What Is `/dev/shm` And Its Practical Usage](https://www.cyberciti.biz/tips/what-is-devshm-and-its-practical-usage.html)
- [When should I use `/dev/shm/` and when should I use `/tmp/`?](https://superuser.com/questions/45342/when-should-i-use-dev-shm-and-when-should-i-use-tmp)
- [What is the best way to use NextJS with docker? #16995](https://github.com/vercel/next.js/discussions/16995#discussioncomment-132484)

## Capabilities for container

By default, containers are "unprivileged" and is not allowed to access any
devices, but a "privileged" container is given access to all devices

| cli flag       | Features                                   |
| -------------- | ------------------------------------------ |
| `--cap-add`    | Add Linux capabilities                     |
| `--cap-drop`   | Drop Linux capabilities                    |
| `--privileged` | Give extended privileges to this container |

Example for compose file:

```
privileged: true
cap_add:
  - ALL
cap_drop:
  - NET_ADMIN
  - SYS_ADMIN
```

The full list of capabilities is available on the Linux man page

Ref:

- [capabilities(7) — Linux manual page](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [Capabilities - Docker - Beginners | Intermediate | Advanced](https://dockerlabs.collabnix.com/advanced/security/capabilities/)

## `tini`

What is Tini?

> Tini is the simplest `init` you could think of. All Tini does is spawn a
> single child (Tini is meant to be run in a container), and wait for it to exit
> all the while reaping zombies and performing signal forwarding.

Why is this tip here?

> If you are using Docker 1.13 or greater, Tini is included in Docker itself.
> This includes all versions of Docker CE. To enable Tini, just pass the
> `--init` flag to docker run

Refs:

- [krallin/tini](https://github.com/krallin/tini): A tiny but valid `init` for
  containers
- [Compose file specification #init](https://docs.docker.com/compose/compose-file/#init)
- [What is advantage of tini?#8](https://github.com/krallin/tini/issues/8)
- [執行 Docker 容器可使用 dumb-init 或 tini 改善程序優雅結束的問題](https://blog.miniasp.com/post/2021/07/09/Use-dumb-init-in-Docker-Container)

### Updating file content by VIM is using file copy instead write directly default

TIL, the `inode` value of a file changes after being modified by Vim (in
default), that's probably the reason why I always have to restart containers to
apply changes.

```vim
:h backupcopy
```

```
"yes"  make a copy of the file and overwrite the original one
"no"   rename the file and write a new one
"auto" one of the previous, what works best
```

Without `set backupcopy=yes`

```console
$ inotifywait -m test.txt
Setting up watches.
Watches established.
test.txt OPEN
test.txt CLOSE_NOWRITE,CLOSE
test.txt OPEN
test.txt ACCESS
test.txt CLOSE_NOWRITE,CLOSE
test.txt MOVE_SELF
test.txt ATTRIB
test.txt DELETE_SELF
```

With `set backupcopy=yes`

```console
$ inotifywait -m test.txt
Setting up watches.
Watches established.
test.txt OPEN
test.txt CLOSE_NOWRITE,CLOSE
test.txt OPEN
test.txt ACCESS
test.txt CLOSE_NOWRITE,CLOSE
test.txt OPEN
test.txt ACCESS
test.txt CLOSE_NOWRITE,CLOSE
test.txt MODIFY
test.txt OPEN
test.txt MODIFY
test.txt CLOSE_WRITE,CLOSE
test.txt ATTRIB
```

Refs:

- [Twitter status from @laixintao](https://twitter.com/laixintao/status/1651149195401887746)
- [VIM options 'backupcopy'](https://vimdoc.sourceforge.net/htmldoc/options.html#'backupcopy')
- [Why inode value changes when we edit in "vi" editor?](https://unix.stackexchange.com/questions/36467/why-inode-value-changes-when-we-edit-in-vi-editor)
- [set `backupcopy=yes` doesn't work still writes the file twice](https://vi.stackexchange.com/questions/11629/set-backupcopy-yes-doesnt-still-writes-the-file-twice)

## Provenance attestations

The provenance attestations include facts about the build process, which are a
set of features that allows users to verify the authenticity and integrity of
the content of a (Docker) container.

Provenance attestations follow the
[SLSA provenance schema, version 0.2](https://slsa.dev/provenance/v0.2#schema).

```yaml
provenance: false
# or
provenance: mode=min,inline-only=true
```

For docker cli, To create a provenance attestation, pass the
`--attest type=provenance` option to the docker `buildx` build command:

```bash
docker buildx build --tag <namespace>/<image>:<version> \
  --attest type=provenance,mode=[min,max] .
```

But, up to May 20, 2023, the different container registries (ghcr.io, gcp, aws,
...) have different support status and compatibilities. For example, using
default options to build container by GitHub Action `docker/build-push-action`,
your registry will show `unknown/unknown` architecture. One solution is to
disable provenance

```yaml
provenance: false
```

This may cause output image cannot run on Google Cloud Run or AWS Lambda/ECS.
For now, you could the following config to fix them.

```yaml
provenance: mode=min,inline-only=true
```

Refs:

- [docker/build-push-action](https://github.com/docker/build-push-action)
- [GitHub Action produces unknown architecture and OS](https://github.com/docker/build-push-action/issues/820)
- [revert disable provenance by default if not set](https://github.com/docker/build-push-action/pull/784)
- [Default image output from buildx v0.10 cannot run on Google Cloud Run or AWS Lambda/ECS](https://github.com/gabrieldemarmiesse/python-on-whales/issues/407)
- [Provenance attestations](https://docs.docker.com/build/attestations/slsa-provenance/)

## Execute command as another user or root in Alpine-based image

`su` and `sudo` (limited) both not work in Alpine-based image. The `su-exec` can
be used in alpine. Do add it the package, if not already available, add the
following to your Dockerfile

```Dockerfile
RUN apk add --no-cache su-exec
```

Inside your scripts you'd run inside docker you can use the following to become
another user:

```
exec su-exec <my-user> <my command>
```

Ref:

- [Use sudo inside Dockerfile (Alpine)](https://stackoverflow.com/questions/49225976/use-sudo-inside-dockerfile-alpine)

## Here-Documents

Here-documents allow redirection of subsequent Dockerfile lines to the input of
`RUN` or `COPY` commands. A alternative method run command in one line without
`\` and `$$`.

Example for running a multi-line script

```dockerfile
# syntax=docker/dockerfile:1
FROM debian
RUN <<EOT bash
  set -ex
  apt-get update
  apt-get install -y vim
EOT
```

If the command only contains a here-document, its contents is evaluated with the
default shell.

```dockerfile
# syntax=docker/dockerfile:1
FROM debian
RUN <<EOT
  mkdir -p foo/bar
EOT
```

Alternatively, shebang header can be used to define an interpreter.

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.6
RUN <<EOT
#!/usr/bin/env python
print("hello world")
EOT
```

Example for creating inline files (`COPY`)

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ARG FOO=bar
COPY <<-EOT /app/foo
hello ${FOO}
EOT
```

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
COPY <<-"EOT" /app/script.sh
echo hello ${FOO}
EOT
RUN FOO=abc ash /app/script.sh
```

Bonus

> `<<-EOF` will ignore leading tabs in your heredoc, while `<<EOF` will not.
> From man page of the Bourne Shell, if, the hyphen (`-`) is appended to `<<`:
>
> 1. leading tabs are stripped from word before the shell input is read (but
>    after parameter and command substitution is done on word);
> 2. leading tabs are stripped from the shell input as it is read and before
>    each line is compared with word; and
> 3. shell input is read up to the first line that literally matches the
>    resulting word, or to an EOF.

Ref:

- [Dockerfile Docs: Here-Documents](https://docs.docker.com/engine/reference/builder/#here-documents)

## Prune unused Docker objects

Clean and remove unused Docker objects, such as images, containers, volumes,
networks and even system are able to free up disk space by running `prune`
command

```sh
docker image prune
docker container prune
docker volume prune
docker network prune

# The docker `system prune` command is a shortcut that prunes images,
# containers, and networks. Volumes are not pruned by default, and you
# must specify the `--volumes` flag for docker system prune to prune
# volumes.
docker system prune
```

Bypassing prompts `-a/--all`, `--filter`, `-f/--forece` to customize different
behaviors.

Ref:

- [Prune unused Docker objects](https://docs.docker.com/config/pruning/)

## Docker engine behind proxy

If you are behind an HTTP proxy server, for example in corporate settings, you
may have to configure the Docker daemon to use the proxy server for operations
such as pulling and pushing images. The daemon (`dockerd`) can be configured in
three ways:

1. Using environment variables (`HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`).
2. Using the `http-proxy`, `https-proxy`, and `no-proxy` fields in the daemon
   configuration file (Docker Engine 23.0 or newer).
3. Using the `--http-proxy`, `--https-proxy`, and `--no-proxy` command-line
   options. (Docker Engine 23.0 or newer).

### Cnnfigure daemon (dockerd) via config

In Docker Engine version 23.0 and later versions, you may also configure proxy
behavior for the daemon in the `daemon.json` file:

```json
{
  "proxies": {
    "http-proxy": "http://proxy.example.com:3128",
    "https-proxy": "https://proxy.example.com:3129",
    "no-proxy": "*.test.example.com,.example.org,127.0.0.0/8"
  }
}
```

These configurations **override** the default `docker.service` systemd file.

```
--http-proxy string                     HTTP proxy URL to use for outgoing traffic
--https-proxy string                    HTTPS proxy URL to use for outgoing traffic
```

For rootless mode, the location of `daemon.json` is
`~/.config/docker/daemon.json`.

The `--validate` option for `dockerd` allows to validate a configuration file
without starting the Docker daemon. A non-zero exit code is returned for invalid
configuration files.

```sh
dockerd --validate --config-file=/tmp/valid-config.json
```

### Configure `systemd` via ENV

The Docker daemon uses the following environment variables in its **start-up**
environment to configure HTTP or HTTPS proxy behavior:

- `HTTP_PROXY`
- `http_proxy`
- `HTTPS_PROXY`
- `https_proxy`
- `NO_PROXY`
- `no_proxy`

So pass these environment variables to `dockerd` via `systemd` config file is
available. But notice that `daemon.json` **overrides** the default
docker.service systemd file.

Create a systemd drop-in directory for the docker service

```sh
sudo mkdir -p /etc/systemd/system/docker.service.d

# The location of systemd configuration files are **different**
# when running Docker in **rootless** mode
mkdir -p ~/.config/systemd/user/docker.service.d
```

Create a file named
`/path-depends-on-your-case/docker.service.d/http-proxy.conf` that adds the
`HTTP_PROXY` environment variable:

```conf
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:3128"
Environment="HTTPS_PROXY=http://proxy.example.com:3129"
Environment="NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
```

Flush changes and restart Docker

```sh
# regular install
sudo systemctl daemon-reload
sudo systemctl restart docker

# rootless
systemctl --user daemon-reload
systemctl --user restart docker
```

Verify that the configuration has been loaded and matches the changes you made,
for example:

```sh
# regular install
sudo systemctl show --property=Environment docker

# rootless mode
systemctl --user show --property=Environment docker

# Expected console output
# > Environment=HTTP_PROXY=http://proxy.example.com:3128 HTTPS_PROXY=http://proxy.example.com:3129 NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp
```

### Ref

- [Daemon CLI (dockerd): Proxy configuration](https://docs.docker.com/engine/reference/commandline/dockerd/#proxy-configuration)
- [Configure the daemon with systemd](https://docs.docker.com/config/daemon/systemd/)

## `COPY` vs `ADD`

`COPY` and `ADD` are both Dockerfile instructions that serve similar purposes.

```Dockerfile
COPY [--chown=<user>:<group>] [--chmod=<perms>] [--checksum=<checksum>] <src>... <dest>
ADD [--chown=<user>:<group>] [--chmod=<perms>] [--checksum=<checksum>] <src>... <dest>
```

Both instructions will copy new files from `<src>` and add them to the
container's filesystem at path `<dest>`. The major difference between `COPY` and
`ADD` is

1. If `<src>` is a URL or Git repo **and** `<dest>` does not end with a
   **trailing slash**, then a file is downloaded from the URL and copied to
   `<dest>`.

2. If `<src>` is a local tar archive in a recognized compression format
   (`identity`, `gzip`, `bzip2` or `xz`) then it is unpacked as a directory.
   When a directory is copied or unpacked, it has the same behavior as `tar -x`,
   the result is the union of:

   1. Whatever existed at the destination path and
   2. The contents of the source tree, with conflicts resolved in favor of "2."
      on a file-by-file basis.

   **Warning**: Whether a file is identified as a recognized compression format
   or not is done solely based on the contents of the file, not the name of the
   file.

3. Resources from remote URLs (case 1 & case 2) are not decompressed.

So `COPY` is the same as `ADD`, but without the tar and remote URL handling. In
the most cases, you should use `COPY` to avoid confusion LOL.

> [!Note]
>
> 1. Each `<src>` may contain wildcards and matching will be done using Go's
>    filepath.Match rules.
>
> 2. For both `COPY` and `ADD`, if `<src>` is a directory, the entire contents
>    of the directory are copied, including filesystem metadata. **But** the
>    directory itself is not copied, just its contents.

Refs:

- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

### Bonus 1: Add a git repository by `ADD` directly

This form allows adding a git repository to an image directly, **without** using
the `git` command inside the image:

```Dockerfile
ADD [--keep-git-dir=<boolean>] <git ref> <dir>
```

The `--keep-git-dir=true` flag adds the .git directory. This flag defaults to
false.

What's more, to add a private repo via SSH, create a `Dockerfile` with the
following form:

```
ADD git@git.example.com:foo/bar.git /bar
```

This `Dockerfile` can be built with `docker build --ssh` or
`buildctl build --ssh`, e.g.,

```sh
docker build --ssh default
buildctl build --frontend=dockerfile.v0 --local context=. --local dockerfile=. --ssh default
```

- [Adding a git repository ADD <git ref> <dir>](https://docs.docker.com/engine/reference/builder/#adding-a-git-repository-add-git-ref-dir)

### (draft) Bonus 2: `--link`

### Bonus 3: `filepath.Match` pattern for Golang

Match reports whether name matches the shell file name pattern. The pattern
syntax is:

```
pattern:
	{ term }
term:
	'*'         matches any sequence of non-Separator characters
	'?'         matches any single non-Separator character
	'[' [ '^' ] { character-range } ']'
	            character class (must be non-empty)
	c           matches character c (c != '*', '?', '\\', '[')
	'\\' c      matches character c

character-range:
	c           matches character c (c != '\\', '-', ']')
	'\\' c      matches character c
	lo '-' hi   matches character c for lo <= c <= hi
```

On Windows, escaping is disabled. Instead, `\\` is treated as path separator.

Ref

- [Go Packages - `filepath` package](https://pkg.go.dev/path/filepath#Match)

## (draft) Speed up build process by cache

1. Cache docker images
2. Cache docker layers
3. Cache dependencies
4. Cache build tools
5. Cache build artifacts

## (draft) Trust and Security

- [Trust](https://docs.docker.com/engine/security/trust/)

## Init system for containers

1. You’re Using the Wrong ENTRYPOINT Form
2. Your Entrypoint Is a Shell Script and You Didn’t exec
3. Bonus Best Practice: Let Someone Else Be PID 1
4. You’re Listening for the Wrong Signal

- [Why Your Dockerized Application Isn’t Receiving Signals](https://hynek.me/articles/docker-signals/)
- [Introducing dumb-init, an init system for Docker containers](https://engineeringblog.yelp.com/2016/01/dumb-init-an-init-for-docker.html)

### `--init` for `docker run` and `init: true` for `docker-compose` file

Built in `tini` as PID 1, which is a tiny but valid `init` for containers.

- [What's the docker-compose equivalent of docker run --init?](https://stackoverflow.com/questions/50356032/whats-the-docker-compose-equivalent-of-docker-run-init)

### What does docker `STOPSIGNAL` do?

`SIGTERM` is the default signal sent to containers to stop them.

`STOPSIGNAL` does allow you to override the default signal sent to the
container. Leaving it out of the Dockerfile causes no harm - it will remain the
default of `SIGTERM`

By default, it does this by sending a `SIGTERM` and then wait a short period so
the process can exit gracefully. If the process does not terminate within a
grace period (10s by default, customisable), it will send a `SIGKILL`.

However, your application may be configured to listen to a different signal -
`SIGUSR1` and `SIGUSR2`, for example.

In these instances, you can use the `STOPSIGNAL` Dockerfile instruction to
override the default.

The image's default stopsignal can be overridden per container, using the
`--stop-signal` flag on `docker run` and `docker create`.

Refs:

- [What does Docker STOPSIGNAL do?](https://stackoverflow.com/questions/50898134/what-does-docker-stopsignal-do)
- [Dockerfile reference: STOPSIGNAL](https://docs.docker.com/engine/reference/builder/#stopsignal)

## You may not need `systemd` and `iptables` for docker

While playing WSL2, I found that `systemd` and `iptables` are not necessary for
docker actually.

```sh
# install rootless docker
dockerd-rootless-setuptool.sh install --skip-iptables
# manually start dockerd
dockerd-rootless.sh --iptables=false
```

Refs:

- [Packet filtering and firewalls](https://docs.docker.com/network/packet-filtering-firewalls/)
- [Bypass the Docker --iptables limitations](https://tipstricks.itmatrix.eu/bypass-the-docker-iptables-limitations/)
- [Preventing Docker from manipulating iptables rules](https://www.michelebologna.net/2018/preventing-docker-from-manipulating-iptables-rules/)
