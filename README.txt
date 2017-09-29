Author: Sevag Hanssian <sevag.hanssian@gmail.com>

=====
Intro
=====

Some Cholesky matrix decomposition implementations and a Python hypothesis testbench.

============
testbench.py
============

Generates symmetric positive-definite matrices using the Hypothesis framework.

* Hypothesis: http://hypothesis.works/
* Numpy: http://www.numpy.org/

Installation (venv recommended):

    $ pip install -r requirements.txt

Usage (for a 32x32 matrix):

    $ make
    $ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/mkl/lib/intel64_lin:/opt/intel/lib/intel64_lin:/usr/lib64/openmpi/lib
    $ ./testbench.py 32 lib/libx.so

Outputs:

* Closeness to numpy's reference linalg.cholesky function
* Memory consumed (https://github.com/fabianp/memory_profiler#api)
* Time taken (https://docs.python.org/3/library/timeit.html)

=================
License/copyright
=================

Cholesky source files are attributed within the source files, with their own licenses. The code that I personally wrote is mostly in testbench.py.

Copyright: Sevag Hanssian 2017 <sevag.hanssian@gmail.com>

=============
Special notes
=============

Intel MKL (https://software.intel.com/en-us/mkl) is not easy to get working. I had to settle for installing all of the RPMs in the tarball (not just running the Intel installer).

    $ sudo find /usr/ -type f -name '*.so*' -exec sh -c "objdump -T {} 2>&1 | grep -v '.*File format not recognized.*' | grep -e '.*pdpotrf.*' && echo {}" \;

Also, there are dependencies on BLAS, LAPACK, SCALAPACK, BLACS, OpenMPI, MPICH, and others. The hardest part of this project was writing the Makefile for the C code.
