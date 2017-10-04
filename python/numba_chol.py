import numpy as np
from numba import jit


@jit
def cholesky(in_arr, out_arr, n):
    np.copyto(out_arr, np.linalg.cholesky(in_arr))
