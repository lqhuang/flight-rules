---
title: Web Development
created: 2023-04-02
updated: 2023-04-02
---

## Preflight `OPTIONS` request

> A CORS preflight request is a CORS request that checks to see if the CORS
> protocol is understood and a server is aware using specific methods and
> headers.

That's means, before sending a _real_ request, the **browser** will send an
preflight request to check whether the server is aware of CORS protocol. Hence
as the server, we need to response to the preflight request with the correct
status code.

For example, in `caddy`, adding CORS headers to `Response` may still isn't
enough to let web app request from browser access CORS resources. In addition,
we need to respond to preflight `OPTIONS` request either:

```caddyfile
@options {
    method OPTIONS
}
respond @options 204
```

**Warn** It's strange that `caddy` (at least `v2.6.2`) doesn't log the preflight
requests with `DEBUG` level.

> Status Code
>
> Both `200 OK` and `204 No Content` are permitted status codes, but some
> browsers incorrectly believe `204 No Content` applies to the resource and do
> not send the subsequent request to fetch it.

References:

- [Preflight request](https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request)
- [OPTIONS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS)

## Padding scroll position for Sticky Top Navbar

When setting `position: sticky` to a navbar, the navbar will be fixed to the
position you specified (like in top). However, the content will be covered by
the navbar after jumping by anchor (`href=#id`).

```
WRONG (but the common behavior):         CORRECT:
+---------------------------------+      +---------------------------------+
| BAR///////////////////// header |      | //////////////////////// header |
+---------------------------------+      +---------------------------------+
| Here is the rest of the Text    |      | BAR                             |
| ...                             |      |                                 |
| ...                             |      | Here is the rest of the Text    |
| ...                             |      | ...                             |
+---------------------------------+      +---------------------------------+
```

To avoid this, we can add some padding to the scroll position. For example:

```css
html {
  scroll-padding-top: 3em; /* height of sticky header */
}
```

But I don't know why this only works in `html` scope.

References:

- [Fixed page header overlaps in-page anchors](https://stackoverflow.com/questions/4086107/fixed-page-header-overlaps-in-page-anchors)
- [Fixed Headers, On-Page Links, and Overlapping Content, Oh My!](https://css-tricks.com/fixed-headers-on-page-links-and-overlapping-content-oh-my/)
