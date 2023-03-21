---
title: Tips for Javascript / Typescript
created: 2023-03-18
updated: 2023-03-21
---

## What is order of items from `Object.entries()` and `Object.values()`

- Before ES2015 (ES6) language spec: Iteration order was technically undefined
- After ES2015 (ES6) language spec: insertion order is preserved, but behavior
  (numeric / string) varies between browsers.
- As of ES2020, property order for these previously untrustworthy methods will
  be guaranteed by the specification to be iterated over in the same
  deterministic manner as the others, due to to the finished proposal: `for-in`
  mechanics.

Generally, object properties (`Object.getOwnPropertyNames()`,
`Reflect.ownKeys(O)`, `[[OwnPropertyKeys]]`) are guaranteed from ES2015:

- Positive integer keys in ascending order
  - **and strings like `"1"` that parse as ints**
- String keys, in insertion order
- Symbol names, in insertion order

From ES2020 The most often used method is guaranteed now:

- `Object.keys()`, `Object.values()`, `Object.entries()`
- `for..in..` loops
- `JSON.stringify()`

These method will iterate in the following order:

1. Numeric array keys, in ascending numeric order
2. All other non-Symbol keys, in insertion order
3. Symbol keys, in insertion order

```js
const obj = {
  3: "3",
  "1": "1", // prettier-ignore
  a: 1,
  c: 3,
  b: 2,
};

console.log(Object.keys(obj));
// [1, 3, "a", "c", "b"]
```

If you need ordered named pairs, use `Map` instead, which purely uses insertion
order. If you just need order, use an `array` or `Set` (which also uses purely
insertion order).

Refs:

1. [Does JavaScript guarantee object property order?](https://stackoverflow.com/questions/5525795/does-javascript-guarantee-object-property-order)
2. [Does ES6 introduce a well-defined order of enumeration for object properties?](https://stackoverflow.com/questions/30076219/does-es6-introduce-a-well-defined-order-of-enumeration-for-object-properties)
