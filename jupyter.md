---
title: Jupyter Tips
updated: 2022-07-08
tags:
  - jupyter
  - python
---

## Plot as SVG

Make `matplotlib` output vector graphics format in Jupyter Notebook

    import matplotlib
    import matplotlib.pyplot as plt
    %matplotlib inline
    %config InlineBackend.figure_format = 'svg'

## jupyter-themes

- https://github.com/dunovank/jupyter-themes

## Interactive Parallel Computing in Python

Refs:

1. https://ipyparallel.readthedocs.io/

## autorealod

```jupyter
%load_ext autoreload
%autoreload 2
```

## Let `mathjax` support `\bm` synatx

    MathJax.Hub.Config({
      tex2jax: {
        inlineMath: [['$','$'], ['\\(','\\)']],
        displayMath: [['$$', '$$'], ["\\[", "\\]"]],
        processEscapes: true
      },
      TeX: {
        equationNumbers: { autoNumber: "AMS" },
        extensions: ["boldsymbol.js"],
        macros: {
          bm: ["\\boldsymbol{#1}", 1]
        }
      },
      'HTML-CSS': {
        imageFont: null
      }
    });

ref:

1. https://github.com/mathjax/MathJax/issues/1219
2. https://www.zhihu.com/question/43422855

## Reset password

```
jupyter notebook password
```
