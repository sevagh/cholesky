Author: Sevag Hanssian <sevag.hanssian@gmail.com>

=====
Intro
=====

Some Cholesky matrix decomposition implementations and a Python hypothesis testbench.

============
testbench.py
============

Generates symmetric positive-definite matrices using the Hypothesis framework.

Installation:

    $ pip install -r requirements.txt (venv recommended)

Usage:

    $ make
    $ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/mkl/lib/intel64_lin:/opt/intel/lib/intel64_lin:/usr/lib64/openmpi/lib
    $ ./testbench.py lib/*

=================
License/copyright
=================

Cholesky source files are attributed within the source files, with their own licenses. The code that I personally wrote is mostly in testbench.py.

Copyright: Sevag Hanssian 2017 <sevag.hanssian@gmail.com>
