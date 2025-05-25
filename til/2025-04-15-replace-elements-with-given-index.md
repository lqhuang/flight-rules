---
title: 'Only Replace Elements with Given Index in Array'
date: 2025-04-15
tags:
  - javascript
  - til
---

In recent dev life, I hope to replace an element at a specific index in an array without mutating the original array. I found two effective and modern aproaches to achieve it.

1. `Object.assign()`

```js
const numbers = [1, 2, 3, 4, 5];
const updatedNumbers = Object.assign([], numbers, { [1]: 'new value' });
console.log(numbers); // [1, 2, 3, 4, 5]
console.log(updatedNumbers); // [1, 'new value', 3, 4, 5]
console.log(numbers === updatedNumbers); // false
```

Ref:

- [javascript - Replace an item at a specific index with vs without mutation - Stack Overflow](https://stackoverflow.com/questions/73428162/replace-an-item-at-a-specific-index-with-vs-without-mutation)
  - [Object.assign() - JavaScript | MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)

2. `prototype.Array.with`

```js
const numbers = [1, 2, 3, 4, 5];
const updatedNumbers = numbers.with(1, 'new value');
console.log(numbers); // [1, 2, 3, 4, 5]
console.log(updatedNumbers); // [1, 'new value', 3, 4, 5]
console.log(numbers === updatedNumbers); // false
```

All modern browsers since 2023 support `with()` method on Array instances.

Ref:

- [Copy an array and replace one element at a specific index with modern JavaScript | Stefan Judis Web Development](https://www.stefanjudis.com/snippets/copy-array-and-replace-one-element-at-index-javascript/): Use `Array.with` to copy an array and update a single entry while doing it.
  - [Array.prototype.with() - JavaScript | MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/with)
