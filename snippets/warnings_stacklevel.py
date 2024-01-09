#!/usr/bin/env python3
# Inspired from https://gist.github.com/sharoonthomas/2779418
import warnings

# Developer specific warning are usually ignored when run from itnerpreter
# Force it to be displayed always
warnings.simplefilter("always", DeprecationWarning)


def level_1_warning(not_reqd_arg=None):
    if not_reqd_arg is not None:
        warnings.warn("A level 1 warning", DeprecationWarning, stacklevel=1)
    return True


def level_2_warning(not_reqd_arg=None):
    if not_reqd_arg is not None:
        warnings.warn("A level 2 warning", DeprecationWarning, stacklevel=2)
    return True


def level_3_warning(not_reqd_arg=None):
    if not_reqd_arg is not None:
        warnings.warn("A level 3 warning", DeprecationWarning, stacklevel=3)
    return True


def level_4_warning(not_reqd_arg=None):
    if not_reqd_arg is not None:
        warnings.warn("A level 4 warning", DeprecationWarning, stacklevel=4)
    return True


def level_5_warning(not_reqd_arg=None):
    if not_reqd_arg is not None:
        warnings.warn("A level 5 warning", DeprecationWarning, stacklevel=5)
    return True


def level_6_warning(not_reqd_arg=None):
    if not_reqd_arg is not None:
        warnings.warn("A level 6 warning", DeprecationWarning, stacklevel=6)
    return True


def level_7_warning(not_reqd_arg=None):
    if not_reqd_arg is not None:
        warnings.warn("A level 7 warning", DeprecationWarning, stacklevel=7)
    return True


def nested_function():
    level_3_warning("Not None")  # level 3 warning inside nested function
    level_4_warning("Not None")
    level_5_warning("Not None")
    level_6_warning("Not None")
    level_7_warning("Not None")


def deep_nested_function():
    nested_function()


def deeper_nested_function():
    deep_nested_function()


if __name__ == "__main__":
    level_1_warning("Not None")
    level_2_warning("Not None")
    level_3_warning("Not None")
    print()
    deeper_nested_function()
