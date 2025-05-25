---
title: 'Node.js: `console.log` supports format strings'
date: 2025-05-18
tags:
  - til
  - javascript
---

Today I learned that `console.log` in Node.js supports format strings similar. This allows for more structured and readable logging.

We usually use `console.log` like this:

```js
console.log('Event:', JSON.stringify(data));
```

But we can use format strings to make it cleaner:

```js
console.log('Event: %j', { foo: 'bar' });
```

And there are several other format specifiers available:

- `%s`: String
- `%d`: Number
- `%o`: Object to inspect
- `%j`: `JSON.stringify`

Learn from Luciano Mammino's [post](https://bsky.app/profile/loige.co/post/3log24bfbsk2i) on Bluesky. And the reference from the Node.js documentation

- [Util | Node.js v24.0.2 Documentation](https://nodejs.org/api/util.html#utilformatformat-args)
