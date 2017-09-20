#!/usr/bin/env python3

import time
import sys
import numpy as np
from hypothesis import given, assume, settings
import hypothesis.strategies as st
from hypothesis.extra.numpy import arrays, array_shapes
import ctypes
import unittest

TIME_RESULTS = {}


class CholeskyTester(unittest.TestCase):
    def __init__(self, testname, cholesky_lib):
        super(CholeskyTester, self).__init__(testname)
        self.cholesky = cholesky_lib

    @given(arrays(np.double,
                  array_shapes(min_dims=2, max_dims=2,
                               min_side=3, max_side=2048),
                  elements=st.floats(0, 1000, allow_nan=False)))
    @settings(deadline=None)
    @settings(max_iterations=10000)
    def test_rand(self, a):
        global TIME_RESULTS
        assume(a.shape[0] == a.shape[1])
        size = a.shape[0]
        spdm = np.dot(a, np.transpose(a)) + size*np.identity(size)
        assume(np.array_equal(spdm, np.transpose(spdm)))  # ensure symmetric
        assume((np.linalg.eigvals(spdm) > 0).all())  # ensure positive-definite
        result = np.zeros((size, size), order='C')
        spdm_ptr = spdm.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        result_ptr = result.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        ts = time.time()
        self.cholesky.cholesky(spdm_ptr, result_ptr, size)
        te = time.time()
        try:
            prev_time = TIME_RESULTS[size]
            divide_factor = 2
        except KeyError:
            prev_time = 0.0
            divide_factor = 1
        TIME_RESULTS[size] = (prev_time + (te - ts))/divide_factor
        self.assertTrue(np.allclose(spdm, np.dot(result,
                                                 np.transpose(result))))


if __name__ == '__main__':
    try:
        artifact = sys.argv[1]
    except IndexError:
        print('Re-run with:\t{0} <path-to-cholesky-.so>', file=sys.stderr)
        sys.exit(1)
    loaded_artifact = ctypes.cdll.LoadLibrary(artifact)

    print('Running testbench for: {0}'.format(artifact.split('/')[-1]))
    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(CholeskyTester)

    suite = unittest.TestSuite()
    for test_name in test_names:
        suite.addTest(CholeskyTester(test_name, loaded_artifact))

    ret = unittest.TextTestRunner().run(suite).wasSuccessful()

    for (size, time_taken) in TIME_RESULTS.items():
        print('{0}\t{1}'.format(size, time_taken))

    sys.exit(ret)
