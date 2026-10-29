"""ctypes wrapper for kp_check.so (build: gcc -O2 -shared -fPIC -o kp_check.so kp_check.c)."""
import ctypes
import os

_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kp_check.so"))
_lib.find_kernelless.restype = ctypes.c_uint64
_lib.find_kernelless.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint64), ctypes.c_int]
_lib.kernel_of.restype = ctypes.c_int
_lib.kernel_of.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint64), ctypes.c_uint64]


def find_kernelless(out, maxsize=None):
    """out[v] = bitmask of out-neighbours. Smallest S (bitmask) with D[S] kernel-less, or 0."""
    n = len(out)
    arr = (ctypes.c_uint64 * n)(*out)
    return _lib.find_kernelless(n, arr, n if maxsize is None else maxsize)


def has_kernel(out, S):
    n = len(out)
    arr = (ctypes.c_uint64 * n)(*out)
    return bool(_lib.kernel_of(n, arr, S))


_lib128 = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kp_check128.so"))
_lib128.find_kernelless128.restype = None
_lib128.find_kernelless128.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint64), ctypes.c_int,
                                       ctypes.POINTER(ctypes.c_uint64)]


def find_kernelless128(out, maxsize=None):
    """Same as find_kernelless, for up to 127 vertices (Python ints as masks)."""
    n = len(out)
    M = (1 << 64) - 1
    arr = (ctypes.c_uint64 * (2 * n))(*[x for o in out for x in (o & M, o >> 64)])
    res = (ctypes.c_uint64 * 2)()
    _lib128.find_kernelless128(n, arr, n if maxsize is None else maxsize, res)
    return res[0] | (res[1] << 64)
