## Redefines function for pytorch and numpy backends, so that they have same behavior
from copy import deepcopy

import numpy as np

from pgmpy import config


def size(arr):
    if isinstance(arr, np.ndarray):
        return arr.size
    else:
        return arr.nelement()


def copy(arr):
    if config.get_backend() == "numpy":
        if isinstance(arr, np.ndarray):
            return np.array(arr)
        elif isinstance(arr, (int, float)):
            return deepcopy(arr)
    else:
        raise ValueError("torch is not supported")


def tobytes(arr):
    if isinstance(arr, np.ndarray):
        return arr.tobytes()
    else:
        return arr.numpy(force=True).tobytes()


def max(arr, axis=None):
    if axis is not None:
        axis = tuple(axis)

    if isinstance(arr, np.ndarray):
        return np.max(arr, axis=axis)
    else:
        raise ValueError("torch is not supported")


def einsum(*args):
    if config.get_backend() == "numpy":
        return np.einsum(*args)
    else:
        raise ValueError("torch is not supported")


def argmax(arr):
    if isinstance(arr, np.ndarray):
        return np.argmax(arr)
    else:
        raise ValueError("torch is not supported")


def stack(arr_iter):
    if config.get_backend() == "numpy":
        return np.stack(tuple(arr_iter))
    else:
        raise ValueError("torch is not supported")


def to_numpy(arr, decimals=None):

    if decimals is None:
        return np.array(arr)
    else:
        return np.array(arr).round(decimals)


def ravel_f(arr):
    if isinstance(arr, np.ndarray):
        return arr.ravel("F")
    else:
        return to_numpy(arr).ravel("F")


def ones(n):
    if config.get_backend() == "numpy":
        return np.ones(n, dtype=config.get_dtype())

    else:
        raise ValueError("torch is not supported")


def get_compute_backend():
    if config.get_backend() == "numpy":
        return np
    else:
        raise ValueError("torch is not supported")


def unique(arr, axis=0, return_counts=False, return_inverse=False):
    if isinstance(arr, np.ndarray):
        return np.unique(
            arr, axis=axis, return_counts=return_counts, return_inverse=return_inverse
        )
    else:
        raise ValueError("torch is not supported")


def flip(arr, axis=0):
    if isinstance(arr, np.ndarray):
        return np.flip(arr, axis=axis)
    else:
        raise ValueError("torch is not supported")


def transpose(arr, axis):
    if isinstance(arr, np.ndarray):
        return np.transpose(arr, axes=axis)
    else:
        raise ValueError("torch is not supported")


def exp(arr):
    if isinstance(arr, np.ndarray):
        return np.exp(arr)
    else:
        return arr.exp()


def sum(arr):
    if isinstance(arr, np.ndarray):
        return np.sum(arr)
    else:
        raise ValueError("torch is not supported")


def allclose(arr1, arr2, atol):
    if isinstance(arr1, np.ndarray) and isinstance(arr2, np.ndarray):
        return np.allclose(arr1, arr2, atol=atol)
    else:
        raise ValueError("torch is not supported")
