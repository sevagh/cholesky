#!/usr/bin/env python3

import os
import subprocess as sp
import numpy as np
from hypothesis import given, assume
import hypothesis.strategies as st
from hypothesis.extra.numpy import arrays, array_shapes
import ctypes
import unittest


RULES = {
    'rosetta_code': {
        'rosetta_code_clang': 'clang -shared -Werror -Wall -O3 -lm -fPIC',
        'rosetta_code_gcc': 'gcc -shared -Werror -Wall -O3 -lm -fPIC'
    }
}


class CholeskyTester(unittest.TestCase):
    def __init__(self, lib):
        self.cholesky = ctypes.cdll.LoadLibrary(lib)

    @given(arrays(np.double, array_shapes(min_dims=2, max_dims=2, min_side=3, max_side=512), elements=st.floats(0, 1, allow_nan=False)))
    def test_cholesky_rand(self, matrix):
        assume(matrix.shape[0] == matrix.shape[1])
        spdm = matrix * np.transpose(matrix)  # symmetric positive definite
        assume(np.array_equal(spdm, np.transpose(spdm)))  # ensure symmetric
        size = spdm.shape[0]
        dest = np.zeros((size, size), order='C')
        spdm_ptr = spdm.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        dest_ptr = dest.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        self.cholesky.cholesky(spdm_ptr, dest_ptr, size)
        print(spdm)
        print(dest)

    def test_cholesky_basic_1(self):
        expected = np.array([[5, 0, 0], [3, 3, 0], [-1, 1, 3]])
        a = np.array([[25, 15, -5], [15, 18, 0], [-5, 0, 11]])
        dest = np.zeros((3, 3), order='C')
        a_ptr = a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        dest_ptr = dest.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        self.cholesky.cholesky(a_ptr, dest_ptr, 3)
        print(np.allclose(expected, dest))

    def test_cholesky_basic_2(self):
        expected = np.array([[4.24264, 0, 0, 0], [5.18545, 6.56591, 0, 0], [12.72792, 3.04604, 1.64974, 0], [9.89949, 1.62455, 1.84971, 1.39262]])
        a = np.array([[18, 22, 54, 42], [22, 70, 86, 62], [54, 86, 174, 134]])
        dest = np.zeros((4, 4), order='C')
        a_ptr = a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        dest_ptr = dest.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        self.cholesky.cholesky(a_ptr, dest_ptr, 4)
        print(np.allclose(expected, dest))


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
            for rule_name, rule in RULES.get(d, {}).items():
                output_artifact = 'lib{0}.so'.format(rule_name)
                output_artifact_path = os.path.join(lib_dir,
                                                    output_artifact)
                sp.run('{0} -o {1} *.c'.format(
                    rule, output_artifact_path), shell=True, check=True)
                artifacts.append(output_artifact_path)
    return artifacts


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    lib_dir = os.path.join(base_dir, 'lib')

    artifacts = descend_dirs(base_dir, lib_dir)
    for a in artifacts:
        cholesky_tester = CholeskyTester(a)
        #cholesky_tester.test_cholesky_random()
        cholesky_tester.test_cholesky_basic_1()
        cholesky_tester.test_cholesky_basic_2()
