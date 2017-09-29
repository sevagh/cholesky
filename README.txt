Author: Sevag Hanssian <sevag.hanssian@gmail.com>

============
Introduction
============

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
    $ ./test/testbench.py 32 lib/lib*

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

Find all notes and observations in `doc/` directory.
