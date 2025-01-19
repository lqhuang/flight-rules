---
title: Jupyter Tips
created: 2022-12-08
updated: 2025-01-19
tags:
  - jupyter
  - python
---

## Plot as SVG

Make `matplotlib` output vector graphics format in Jupyter Notebook

```python
import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline
%config InlineBackend.figure_format = 'svg'
```

Save vector graphics format with `matplotlib`

```
plt.savefig('tmp.pdf', bbox_inches='tight')
plt.show()
```

- [如何优雅地使用 Jupyter? - 陈乐群](https://www.zhihu.com/question/59392251)

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

```js
MathJax.Hub.Config({
  tex2jax: {
    inlineMath: [
      ['$', '$'],
      ['\\(', '\\)'],
    ],
    displayMath: [
      ['$$', '$$'],
      ['\\[', '\\]'],
    ],
    processEscapes: true,
  },
  TeX: {
    equationNumbers: { autoNumber: 'AMS' },
    extensions: ['boldsymbol.js'],
    macros: {
      bm: ['\\boldsymbol{#1}', 1],
    },
  },
  'HTML-CSS': {
    imageFont: null,
  },
});
```

ref:

1. https://github.com/mathjax/MathJax/issues/1219
2. https://www.zhihu.com/question/43422855

## Reset password

```
jupyter notebook password
```

## Inline animations in Jupyter

First tune your notebook backend to `widget`:

```python
%matplotlib widget

# %matplotlib notebook
# is deprecated and not recommended for using inside VS Code
```

`inline` means that the plots are shown as png graphics. Those png images cannot be animated. But notice that installed `ipympl` is required to use `widget` backend.

Then ty to use `jshtml` as the animation format:

```python
from IPython.display import HTML
HTML(ani.to_jshtml())
```

where `ani` is the animation object from `matplotlib`.

Refs

- [python - Inline animations in Jupyter - Stack Overflow](https://stackoverflow.com/questions/43445103/inline-animations-in-jupyter)

## Disable show figure object automatically after runned cell

In recent versions of `Matplotlib` and `IPython`, it is sufficient to import `matplotlib.pyplot` and call `pyplot.ion`.

```python
import matplotlib.pyplot as plt

_ = plt.ioff()  # Turn off interactive mode to disable automatic redrawing of the plot

# So you need to call plt.show() or fig explicitly to display the figure

# Warning: This may not work under `%matplotlib inline` mode
```
