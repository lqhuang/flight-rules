#!/usr/bin/env python3
# ruff: noqa: E731
# Modified and tuned from: https://antonz.org/page-iterator/
import itertools
import timeit

USE_THIRD = True
try:
    from functional import seq
    from more_itertools import chunked, ichunked
    from toolz import partition, partition_all
except ModuleNotFoundError:
    USE_THIRD = False

###########################
# Utils and mock functions
###########################


def reader(a, b):
    """Yields numbers in range [a, b)"""
    n = a
    while n < b:
        yield n
        n += 1


def process_single(record):
    """Processes a single record (kinda)"""
    record  # type: ignore


def process_batch(page):
    """Processes records in batch (kinda)"""
    for record in page:
        record  # type: ignore


def switch_arg_order(fn):
    """Switches first two arguments of a function"""
    return lambda b, a: fn(a, b)


######################################
# Page iterators in different flavors
######################################


def paginate_append(iterable, page_size):
    """Uses list.append() to fill pages"""
    page = []
    for item in iterable:
        page.append(item)
        if len(page) == page_size:
            yield page
            page = []
    yield page


def paginate_fixed(iterable, page_size):
    """Uses fixed-size page"""
    page = [None] * page_size
    idx = 0
    for item in iterable:
        page[idx] = item
        idx += 1
        if idx == page_size:
            yield page
            idx = 0
    yield page[:idx]


def paginate_slice(iterable, page_size):
    """Uses sliced iterator to yield pages"""
    it = iter(iterable)
    slicer = lambda: tuple(itertools.islice(it, page_size))
    # Note:
    #
    # Signature:
    #   iter(object)
    #   iter(object, sentinel)
    #
    # If the second argument, `sentinel`, is given, then object must be a callable
    # object. The iterator created in this case will call `object` with no arguments
    # for each call to its `__next__()` method; if the value returned is equal to
    # sentinel, `StopIteration` will be raised, otherwise the value will be returned.
    return iter(slicer, ())


def paginate_slice_sentinel(iterable, page_size):
    """Uses simple sliced iterator to yield pages"""
    it = iter(iterable)
    try:
        while True:
            batch = tuple(itertools.islice(it, page_size))
            if batch == ():
                raise StopIteration
            yield batch
    except StopIteration:
        return


def paginate_zip(iterable, page_size):
    """Uses zip or zip_longest to yield pages (from `toolz`)"""
    args = (iter(iterable),) * page_size
    return itertools.zip_longest(*args, fillvalue=None)


if USE_THIRD:

    def paginate_wrapper_functional(iterable, page_size):
        """Uses `seq` from `functional` package"""
        return seq(iterable).grouped(page_size)  # type: ignore


############
# Benchmark
############


def one_by_one(a, b):
    """Processes records one-by-one, without pagination"""
    rdr = reader(a, b)
    for record in rdr:
        process_single(record)


def batch(paginator, page_size, a, b):
    """Processes records in batches, with pagination"""
    rdr = reader(a, b)
    for page in paginator(rdr, page_size):
        process_batch(page)


def benchmark():
    """Compares different iteration methods"""
    times = 10

    page_size = 1000
    a = 10_000_000
    b = 20_000_000

    fn = lambda: one_by_one(a, b)
    total = timeit.timeit(fn, number=times)
    it_time = round(total * 1000 / times)
    print(f"One-by-one (baseline): {it_time} ms")

    fn = lambda: batch(paginate_append, page_size, a, b)
    total = timeit.timeit(fn, number=times)
    it_time = round(total * 1000 / times)
    print(f"Use `append()` to fill page: {it_time} ms")

    fn = lambda: batch(paginate_fixed, page_size, a, b)
    total = timeit.timeit(fn, number=times)
    it_time = round(total * 1000 / times)
    print(f"Use fixed-size page: {it_time} ms")

    fn = lambda: batch(paginate_slice, page_size, a, b)
    total = timeit.timeit(fn, number=times)
    it_time = round(total * 1000 / times)
    print(f"Use islice: {it_time} ms")

    fn = lambda: batch(paginate_slice_sentinel, page_size, a, b)
    total = timeit.timeit(fn, number=times)
    it_time = round(total * 1000 / times)
    print(f"Use islice + plain sentinel: {it_time} ms")

    if USE_THIRD:
        fn = lambda: batch(switch_arg_order(partition), page_size, a, b)  # type: ignore
        total = timeit.timeit(fn, number=times)
        it_time = round(total * 1000 / times)
        print(f"Use `partition` package `toolz`: {it_time} ms")

        fn = lambda: batch(switch_arg_order(partition_all), page_size, a, b)  # type: ignore  # noqa: E501
        total = timeit.timeit(fn, number=times)
        it_time = round(total * 1000 / times)
        print(f"Use `partition_all` package `toolz`: {it_time} ms")

        fn = lambda: batch(chunked, page_size, a, b)  # type: ignore
        total = timeit.timeit(fn, number=times)
        it_time = round(total * 1000 / times)
        print(f"Use `chunked` from package `more-itertools`: {it_time} ms")  # type: ignore  # noqa: E501

        fn = lambda: batch(ichunked, page_size, a, b)  # type: ignore
        total = timeit.timeit(fn, number=times)
        it_time = round(total * 1000 / times)
        print(f"Use `ichunked` from package `more-itertools`: {it_time} ms")

        fn = lambda: batch(paginate_wrapper_functional, page_size, a, b)
        total = timeit.timeit(fn, number=times)
        it_time = round(total * 1000 / times)
        print(f"Use `grouped` from package `PyFunctional`: {it_time} ms")


if __name__ == "__main__":
    benchmark()
