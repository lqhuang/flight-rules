---
title: Rust Tips
created: 2022-06-04
updated: 2022-08-13
---

## Install with existed Rust under `/usr/bin`

Can't install rustup because of existing rust that I can't remove

error:

```
error: it looks like you have an existing installation of Rust at:
error: /usr/bin
error: rustup cannot be installed alongside Rust. Please uninstall first
error: if this is what you want, restart the installation with `-y'
error: cannot install while Rust is installed
```

Use `RUSTUP_INIT_SKIP_PATH_CHECK` env to skip check

    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | RUSTUP_INIT_SKIP_PATH_CHECK=yes sh

Ref:

1. https://github.com/rust-lang/rustup/issues/953
2. https://github.com/rust-lang/rustup/pull/705

## Easiest way to merge HashMaps in @rustlang?

```rust
use std::collections::HashMap;

// Mutating one map
fn merge1(map1: &mut HashMap<(), ()>, map2: HashMap<(), ()>) {
        map1.extend(map2);

}

// Without mutation
fn merge2(map1: HashMap<(), ()>, map2: HashMap<(), ()>) -> HashMap<(), ()> {
        map1.into_iter().chain(map2).collect()

}

// If you only have a reference to the map to be merged in
fn merge_from_ref(map: &mut HashMap<(), ()>, map_ref: &HashMap<(), ()>) {
        map.extend(map_ref.into_iter().map(|(k, v)| (k.clone(), v.clone())));

}
```

Ref:

1. https://stackoverflow.com/questions/27244465/merge-two-hashmaps-in-rust

### Fast time tic-tock

```rust
std::time::SystemTime::now()
    .duration_since(std::time::UNIX_EPOCH)
    .unwrap()
    .as_millis()
```

### Improve arg signature for `Option`

如果一个函数接收一个 `Option` 的参数，比如：

```rust
fn a(value: Option<i32>)
```

这个参数可以优化为：

```rust
fn a(value: impl Into<Option<i32>>)
```

这样

```rust
a(10)
a(Some(10))
a(None)
```

都可以用，比较方便
