#!/usr/bin/env python3

import sys
import numpy as np
from hypothesis import given, assume, settings
import hypothesis.strategies as st
from hypothesis.extra.numpy import arrays, array_shapes
import ctypes as c
import unittest
import timeit
from memory_profiler import memory_usage

RESULTS = {}


def running_average(d, key, newval):
    d[key] = (d.get(key, 0.0) + newval)/2.0


class CholeskyTester(unittest.TestCase):
    def __init__(self, testname, *args, **kwargs):
        super(CholeskyTester, self).__init__(testname)
        self.name = kwargs['name']
        self.cholesky = kwargs['cholesky']

    @given(arrays(np.double,
                  array_shapes(min_dims=2, max_dims=2,
                               min_side=int(sys.argv[1]),
                               max_side=int(sys.argv[1])),
                  elements=st.floats(0, 1000, allow_nan=False)))
    @settings(deadline=None)
    @settings(max_examples=1000)
    def test_rand(self, a):
        global RESULTS
        assume(a.shape[0] == a.shape[1])
        size = a.shape[0]
        spdm = np.dot(a, np.transpose(a)) + size*np.identity(size)
        assume(np.array_equal(spdm, np.transpose(spdm)) and
               (np.linalg.eigvals(spdm) > 0).all())
        out = np.zeros((size, size), order='C')
        cholesky_call = lambda: self.cholesky.cholesky(
            spdm.ctypes.data_as(c.POINTER(c.c_double)),
            out.ctypes.data_as(c.POINTER(c.c_double)), size)
        t = timeit.timeit(cholesky_call, number=1)
        mem_usage = memory_usage(cholesky_call)
        running_average(RESULTS, 'err',
                        np.abs(out - np.linalg.cholesky(spdm)).max())
        running_average(RESULTS, 'runtime', t)
        running_average(RESULTS, 'mem', max(mem_usage))
        self.assertTrue(True)


if __name__ == '__main__':
    try:
        size = int(sys.argv[1])
        name = sys.argv[2]
        artifact = c.cdll.LoadLibrary(name)
    except IndexError:
        print('Re-run with:\t{0} N cholesky1.so cholesky2.so ...'.format(
              sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    test_loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    [suite.addTest(CholeskyTester(t, name=name, cholesky=artifact)) for t in
     test_loader.getTestCaseNames(CholeskyTester)]

    unittest.TextTestRunner().run(suite).wasSuccessful()

    print('RESULTS FOR SIZE {0}:\t{1}'.format(size, sorted(RESULTS.items())))
