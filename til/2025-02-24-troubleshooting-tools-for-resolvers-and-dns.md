---
title: Troubleshooting Tools for Resolvers and DNS Beyond `dig` and `nslookup`
date: 2025-02-24
tags:
  - linux
  - network
---

When troubleshooting DNS issues, we often rely on `dig` and `nslookup`. However, there are other tools that can provide additional insights.

For example, `getent` can be used to query the system's Name Service Switch (NSS) configuration and modules. Helpful to retrieve information about hosts, services, protocols, and more from system databases.

```sh
getent ahosts google.com
getent ahostsv6 microsoft.com
```

And `delv` is a DNSSEC validation tool that can be used to perform DNS queries with DNSSEC validation. It provides more detailed info about DNSSEC signatures and keys.

```console
$ delv @1.1.1.1 dnssec-failed.org  # Non-existent domain
;; resolution failed: failure
$ delv @1.1.1.1 google.com         # DNSSEC unsigned domain
; unsigned answer
google.com.             218     IN      A       172.217.26.238
$ delv @1.1.1.1 example.org.       # DNSSEC signed domain
; fully validated
example.org.            267     IN      A       23.215.0.132
example.org.            267     IN      A       23.215.0.133
example.org.            267     IN      A       96.7.128.186
example.org.            267     IN      A       96.7.128.192
example.org.            267     IN      RRSIG   A 13 2 300 20250605031849 20250515062108 41175 example.org. QRRfEe/g96jWzKlHpUCo7JR//77LlbP5+llaGq2SbWpaNY2WXqXJFguz 876Ck8HDmGt7Bva0RHuphPgJWu5Jdg==
```

Check cache content and monitor DNS queries with local `systemd-resolved`:

```sh
resolvectl show-cache
resolvectl monitor
```

Learn these from [Tools for troubleshooting in one place](https://biriukov.dev/docs/resolver-dual-stack-application/troubleshooting-tools-for-resolvers-and-dns/)

Thanks Viacheslav Biriukov (@biriukov)!
