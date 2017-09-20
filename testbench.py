#!/usr/bin/env python3

import os
import sys
import subprocess as sp
import numpy as np
from hypothesis import given, assume
import hypothesis.strategies as st
from hypothesis.extra.numpy import arrays, array_shapes
import ctypes
import unittest


class CholeskyTester(unittest.TestCase):
    def __init__(self, testname, cholesky_lib):
        super(CholeskyTester, self).__init__(testname)
        self.cholesky = ctypes.cdll.LoadLibrary(cholesky_lib)

    @given(arrays(np.double,
                  array_shapes(min_dims=2, max_dims=2,
                               min_side=3, max_side=1024),
                  elements=st.floats(0, 1000, allow_nan=False)))
    def test_rand(self, a):
        assume(a.shape[0] == a.shape[1])
        size = a.shape[0]
        spdm = np.dot(a, np.transpose(a)) + size*np.identity(size)
        assume(np.array_equal(spdm, np.transpose(spdm)))  # ensure symmetric
        assume((np.linalg.eigvals(spdm) > 0).all())  # ensure positive-definite
        result = np.zeros((size, size), order='C')
        spdm_ptr = spdm.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        result_ptr = result.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        self.cholesky.cholesky(spdm_ptr, result_ptr, size)
        self.assertTrue(np.allclose(spdm, np.dot(result,
                                                 np.transpose(result))))


def descend_dirs(base_dir, lib_dir):
    try:
        os.makedirs(lib_dir)
    except OSError as e:
        if e.errno != 17:
            raise(e)

    artifacts = []
    for d in os.listdir(base_dir):
        if os.path.isdir(d) and not d.startswith('.'):
            os.chdir(os.path.join(base_dir, d))
            with open('./makerules', 'r') as f:
                for l in f:
                    lsplit = l[:-1].split(':')
                    rule = lsplit[1]
                    output_artifact_path = os.path.join(
                        lib_dir, 'lib{0}_{1}.so'.format(d, lsplit[0]))
                    sp.run('{0} -o {1} *.c'.format(
                        rule, output_artifact_path), shell=True, check=True)
                    artifacts.append(output_artifact_path)
    return artifacts


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    lib_dir = os.path.join(base_dir, 'lib')

    artifacts = descend_dirs(base_dir, lib_dir)
    ret = True
    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(CholeskyTester)

    suite = unittest.TestSuite()
    for test_name in test_names:
        for a in artifacts:
            suite.addTest(CholeskyTester(test_name, a))

    sys.exit(unittest.TextTestRunner().run(suite).wasSuccessful())
