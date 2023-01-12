---
title: Network Tips
created: 2022-11-15
updated: 2023-01-12
---

## cURL an IP address with specific domain name

First approach, add `HOST` header let server knows:

    curl http://192.168.100.100 -H 'Host: some.domain.tld'

Second one, use `--resolve <host:port:address>`:

    curl https://domain.tld --resolve 'domain.tld:443:192.168.100.100'

Extra helper, `--connect-to <HOST1:PORT1:HOST2:PORT2>`:

    curl https://domain.example --connect-to domain.example:443:192.168.100.100:443

Refs:

- [How to test a HTTPS URL with a given IP address](https://serverfault.com/questions/443949/how-to-test-a-https-url-with-a-given-ip-address)

## TLDs for private network

For test

```
.test
.example
.invalid
.localhost
```

Undefined, but probably reserved

```
.intranet
.internal
.private
.corp
.lan
.home
```

RFC proposed and recorded

```
.arpa // Infrastructure
.home.arpa // Home network
.local // Apple mDNS
.onion // Onion network
```

User assigned codes

```
.aa
.qm to .qz
.xa to .xz
.zz
```

- [Top level domain/domain suffix for private network?](https://serverfault.com/questions/17255/top-level-domain-domain-suffix-for-private-network)
- [DNS attributes for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html)
- [Internal DNS | Google Cloud](https://cloud.google.com/compute/docs/internal-dns)
- [List of Internet top-level domains](https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains)
- [RFC6762 - Multicast DNS](https://www.rfc-editor.org/rfc/rfc6762.html)
- [RFC8375 - Special-Use Domain 'home.arpa.'](https://www.rfc-editor.org/rfc/rfc8375.html)
- [RFC7686 - The ".onion" Special-Use Domain Name](https://www.rfc-editor.org/rfc/rfc7686.html)
