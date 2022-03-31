# jupyter notebook tips

## 配置 notebook extensions

### Install the python package

from `conda`:

    conda install -c conda-forge jupyter_contrib_nbextensions jupyter_nbextensions_configurator

from `pip`:

    pip install jupyter_nbextensions_configurator jupyter_contrib_nbextensions
    pip install jupyterlab_code_formatter

Enable extensions:

    jupyter contrib nbextension install --user
    jupyter nbextensions_configurator enable --user

### Install javascript and css files

This step copies the nbextensions' javascript and css files into the jupyter
server's search directory, and edits some jupyter config files. A jupyter
subcommand is provided for the purpose:

    jupyter contrib nbextension install --user

The command does two things: installs nbextension files, and edits nbconvert
config files. The first part is essentially a wrapper around the
notebook-provided jupyter nbextension install, and copies relevant javascript
and css files to the appropriate jupyter data directory. The second part edits
the config files jupyter_nbconvert_config.jsonand jupyter_notebook_config.json
as noted below in the options. The command can take most of the same options as
the jupyter-provided versions, including

- `--user` to install into the user's home jupyter directories
- `--system` to perform installation into system-wide jupyter directories
- `--sys-prefix` to install into python's `sys.prefix`, useful for instance in
  virtual environments, such as with conda
- `--symlink` to symlink the nbextensions rather than copying each file
  (recommended, on non-Windows platforms).
- `--debug`, for more-verbose output

An analogous `uninstall` command is also provided, to remove all of the
nbextension files from the jupyter directories.

### Enabling/Disabling extensions

Alternatively, and more conveniently, you can use the
`jupyter_nbextensions_configurator` server extension, which is installed as a
dependency of this repo, and can be used to enable and disable the individual
nbextensions, as well as configure their options. You can then open the
nbextensions tab on the tree (dashboard/file browser) notebook page to configure
nbextensions.

    jupyter nbextensions_configurator enable --user

### Ref

1. https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html
2. https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator

## 设置矢量图

让 matplotlib 在 Jupyter Notebook 上面输出矢量图了

    import matplotlib
    import matplotlib.pyplot as plt
    %matplotlib inline
    %config InlineBackend.figure_format = 'svg'

## Jupyter Hub

Refs:

1. https://github.com/jupyterhub/jupyterhub
2. https://jupyterhub.readthedocs.io/en/stable/

## Jupyter Lab

### Install

```shell
conda install -c conda-forge jupyterlab
```

or

```shell
pip install jupyterlab
```

### Run

```
jupyter lab --ip=0.0.0.0 --no-browser
```

or

```
jupyter notebook
```

access `/lab`

## Dashboard

```sh
pip install voila
jupyter labextension install @jupyter-voila/jupyterlab-preview
jupyter serverextension enable voila --sys-prefix
```

Refs:

1. https://github.com/jupyter/dashboards
2. https://github.com/voila-dashboards/voila

## jupyter-themes

https://github.com/dunovank/jupyter-themes

## Interactive Parallel Computing in Python

Refs:

1. https://ipyparallel.readthedocs.io/

## autorealod

    %load_ext autoreload
    %autoreload 2

## Resource

数据分析为什么常用 Jupyter 而不是直接使用 Python 脚本或 Excel? - Charles Wang 的
回答 - 知乎 https://www.zhihu.com/question/37490497/answer/125536948

https://www.zhihu.com/question/59392251
http://clarkchen.github.io/2017/06/05/Jupyter%E5%8F%A6%E7%B1%BB%E5%85%A8%E5%AE%B6%E6%A1%B6/
https://zhuanlan.zhihu.com/p/26739300?group_id=843868091631955968
https://github.com/lhyfst/learn_jupyter

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
