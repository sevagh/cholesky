import numpy as np


def cholesky(in_arr, out_arr, n):
    np.copyto(out_arr, np.linalg.cholesky(in_arr))
