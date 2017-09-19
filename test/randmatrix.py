import numpy as np
from hypothesis.strategies import floats
from hypothesis.extra.numpy import arrays
import ctypes


def _generate_matrix(x):
    return arrays(np.double, (x, x), elements=floats(
        0, 1, allow_nan=False)).example()


def test_cholesky_lib(lib):
    for size in [0, 8, 16, 32, 64, 128, 256, 512, 1024]:
        print('For size {0}'.format(size))
        arr = _generate_matrix(size)
        dest = np.zeros((size, size), order='C')
        arr_ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        dest_ptr = dest.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        lib_ = ctypes.cdll.LoadLibrary(lib)
        lib_.cholesky(arr_ptr, dest_ptr, size)
        print(arr)
        print(dest)
