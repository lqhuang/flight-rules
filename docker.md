---
title: Docker Tips
created: 2019-04-02
updated: 2022-01-09
---

## docker: Communication between multiple docker-compose projects

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

## docker: Share Compose configurations between files and projects

References:

1. https://docs.docker.com/compose/extends/

## this system doesn't provide enough entropy

Way 1: mount /dev/urandom from the host as /dev/random into the container

    docker run -v /dev/urandom:/dev/random ...

Way 2: just install the `rng-tools` and run command `sudo rngd -r /dev/urandom`

## docker: Access docker container from host using containers name

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
> failures. – Rob

solution 1:

    sudo systemctl enable docker

solution 2: using `cloud-init` script

```ymal
#cloud-config
coreos:
  units:
    - name: "docker.service"
      command: "start"
      enable: true
```

Refs

1. [docker-daemon-doesnt-start-on-boot-on-coreos](https://serverfault.com/questions/743087/docker-daemon-doesnt-start-on-boot-on-coreos)

## Environment variables in Compose

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

## Get Docker container IP address in host machine

Refs:

1. [10 Examples of how to get Docker Container IP Address](http://networkstatic.net/10-examples-of-how-to-get-docker-container-ip-address)

## Get Docker container IP address inside container???

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
