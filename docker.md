---
title: docker tips
published: 2019-04-02
---

## docker: Communication between multiple docker-compose projects

method 1: set `external_links` for `docker-compose`

method 2:

As of compose file version 3.5:

This now works:

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

docker-compose up -d will join a network called 'custom\_network'. If it doesn't exist, it will be created!

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

method 2: use `domainname` in `docker-compose.yml` or `--hostname host.domain.com` for `docker run`

method 3: automatically update by [script](https://stackoverflow.com/questions/36151981/local-hostnames-for-docker-containers)

method 4: `--add-host` for `docker run` / `extra_hosts` for compose file.

ref:

1. https://stackoverflow.com/questions/37242217/access-docker-container-from-host-using-containers-name
2. https://stackoverflow.com/questions/36151981/local-hostnames-for-docker-containers

## Docker daemon doesn't start on boot on CoreOS

it's very interesting that it doesn't start the docker daemon on startup. 

It only starts when I SSH in and do `docker ps`

Then everything work fine again.

> Background:The root of this is because docker is socket activated on CoreOS, ie it doesn't block the boot chain. Early versions of docker were slow to start when you had lots of containers on disk which blocked everything that depended on docker from starting quickly, which caused some interesting failures. – Rob

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

Both `$VARIABLE` and `${VARIABLE}` syntax are supported. Additionally when using the 2.1 file format, it is possible to provide inline default values using typical shell syntax:

* `${VARIABLE:-default}` evaluates to `default` if `VARIABLE` is unset or empty in the environment.
* `${VARIABLE-default}` evaluates to `default` only if `VARIABLE` is unset in the environment.

Similarly, the following syntax allows you to specify mandatory variables:

* `${VARIABLE:?err}` exits with an error message containing `err` if `VARIABLE` is unset or empty in the environment.
* `${VARIABLE?err}` exits with an error message containing `err` if `VARIABLE` is unset in the environment.

Other extended shell-style features, such as `${VARIABLE/foo/bar}`, are not supported.

You can use a `$$` (double-dollar sign) when your configuration needs a literal dollar sign. This also prevents Compose from interpolating a value, so a `$$` allows you to refer to environment variables that you don’t want processed by Compose.

References:

1. [Environment variables in Compose
](https://docs.docker.com/compose/environment-variables)
