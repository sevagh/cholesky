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
    def __init__(self, testname, cholesky_libs):
        super(CholeskyTester, self).__init__(testname)
        self.choleskies = cholesky_libs

    @given(arrays(np.double,
                  array_shapes(min_dims=2, max_dims=2,
                               min_side=3, max_side=2048),
                  elements=st.floats(0, 1000, allow_nan=False)))
    @settings(deadline=None)
    @settings(max_examples=100)
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
        # this part should loop around all choleskies
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
        self.assertTrue(np.allclose(result, np.linalg.cholesky(spdm),
                                    rtol=0.001,
                                    atol=0.001))


if __name__ == '__main__':
    artifacts = sys.argv[1:]
    if not len(artifacts):
        print('Re-run with:\t{0} cholesky1.so cholesky2.so ...'.format(
            sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    a_ = {a: ctypes.cdll.LoadLibrary(a) for a in artifacts}

    test_loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    [suite.addTest(CholeskyTester(t, a_)) for t in
        test_loader.getTestCaseNames(CholeskyTester)]

    ret = unittest.TextTestRunner().run(suite).wasSuccessful()

    for (size, time_taken) in TIME_RESULTS.items():
        print('{0}\t{1}'.format(size, time_taken))

    sys.exit(ret)
