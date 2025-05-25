---
title: Disable
date: 2025-05-07
tags:
  - macos
---

One day, I found `mds_stores` is always writing to disk in crazy high rate, which is quite anyoying. However, it seems only related to Spotlight service, I don't use Spotlight too much, so I decided to disable it.

```sh
sudo mdutil -a -i off
```

Refs:

- [Spotlight (mds_stores) is writing hundreds of GBs of data to my hard drive after the Sequoia update. | MacRumors Forums](https://forums.macrumors.com/threads/spotlight-mds_stores-is-writing-hundreds-of-gbs-of-data-to-my-hard-drive-after-the-sequoia-update.2438003/)
- [Mds_Stores High CPU Usage[All You Should Know] - EaseUS](https://www.easeus.com/computer-instruction/mds-store.html)
