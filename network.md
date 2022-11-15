---
title: Network Tips
created: 2022-11-15
updated: 2022-11-15
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
