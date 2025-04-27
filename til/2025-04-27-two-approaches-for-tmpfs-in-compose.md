---
title: Two Approaches to Create `tmpfs` volume for Container Compose
date: 2025-04-27
tags:
  - docker
---

I meet a strange issue that application in container cannot access `/tmp/app` because of the volume isn't mounted/mapped correctly ??? So I have to mapping a `tmpfs` volume manually to `/tmp/app` for the application to work.

After some investigation, the `tmpfs` volume can be created in two different ways in `compose.yaml`:

1. Using `tmpfs` directly in the `services` section:

   ```yaml
   services:
     app:
       image: your-image
       tmpfs:
         - /tmp/app
         - /var/tmp/app
   ```

2. Using `tmpfs` in the `volumes` section and then referencing it in the `services` section:

   ```yaml
   services:
     app:
       image: your-image
       volumes:
         - defined-volume:/tmp/app

   volumes:
     defined-volume:
       driver: local
       driver_opts:
         type: tmpfs
         device: tmpfs
   ```
