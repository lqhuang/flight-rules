---
title: Prefer using `node` directly instead of `npm run` in Node.js container application
date: 2025-05-19
tags:
  - til
  - container
---

When the `docker stop` command is executed, it sends a signal to the container (`SIGTERM` by default).

In a Node.js containerized application, if you run the application using `npm run`, it will start a new shell to run commands, which may not handle the `SIGTERM` signal properly to cause issues during graceful shutdown.

Bad case: Signal are not propeagated by the shell

```console
/usr/bin/containerd-shim-runc-v2 -namespace ...
  \_ npm start
      \_ sh -c node index.js
          \_ node index.js
```

Good practice

```console
/usr/bin/containerd-shim-runc-v2 -namespace ...
  \_ node index.js
```

Ref

- [Ensure a Graceful Termination for a Containerized Node.js Application
  Challenge by Ivan Velichko](https://labs.iximiuz.com/challenges/graceful-termination-for-nodejs-container)
