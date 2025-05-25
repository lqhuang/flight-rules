---
title: Verify created `systemd` service or timer files
date: 2025-03-23
tags:
  - systemd
  - linux
---

Today, I learned how to verify that the systemd files we created

```sh
systemd-analyze verify /etc/systemd/system/helloworld.*
```

> I found SUSE also provides a nice documentation about Linux. Awesome!

- [Working with systemd Timers](https://documentation.suse.com/smart/systems-management/html/systemd-working-with-timers/index.html)
