import numpy as np

def make_key(obj):
    """ For an arbitrarily nested list, tuple, set, or dict, convert all numpy arrays to
    tuples of their data and metadata, convert all lists and dicts to tuples, and store
    every item alongside its type. This creates an object that can be used as a
    dictionary key to represent the original types and data of the nested objects that
    might otherwise not be able to be used as a dictionary key due to not being
    hashable."""
    if isinstance(obj, (list, tuple)):
        return tuple(make_key(item) for item in obj)
    elif isinstance(obj, set):
        return set(make_key(item) for item in obj)
    elif isinstance(obj, dict):
        return tuple((key, make_key(value)) for key, value in obj.items())
    elif isinstance(obj, np.ndarray):
        return obj.tobytes(), obj.dtype, obj.shape
    else:
        return type(obj), obj


def lru_cache(maxsize=128):
    """Decorator to cache up to `maxsize` most recent results of a function call. Custom
    implementation instead of using `functools.lru_cache()`, so that we can create
    dictionary keys for unhashable types like numpy arrays, which do not work with
    `functools.lru_cache()`."""

    def decorator(func):
        import functools, collections

        cache = collections.OrderedDict()

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            cache_key = make_key((args, kwargs))
            try:
                result = cache[cache_key]
            except KeyError:
                try:
                    result = cache[cache_key] = func(*args, **kwargs)
                except Exception as e:
                    # We don't want the KeyError in the exception:
                    raise e from None
            cache.move_to_end(cache_key)
            while len(cache) > maxsize:
                cache.popitem(last=False)
            return result

        return wrapped

    return decorator


from .currents import (
    Transport,
    piecewise_minjerk_and_coast,
    solve_two_coil,
    interpolate_with_relative_durations,
)
from .coils_RbRb import make_coils
from .polynomials import linear

__all__ = [
    'make_coils',
    'Transport',
    'piecewise_minjerk_and_coast',
    'linear',
    'lru_cache',
    'solve_two_coil',
    'two_coil_zero_beta',
    'interpolate_with_relative_durations',
]
