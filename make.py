#!/usr/bin/env python2

from __future__ import print_function
import os
import shutil
import subprocess as sp
import sys
from ctypes import cdll

RULES = {
    'rosetta_code': {
        'rosetta_code_clang': 'clang -shared -Werror -Wall -O3 -lm -fPIC',
        'rosetta_code_gcc': 'gcc -shared -Werror -Wall -O3 -lm -fPIC'
    }
}


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
                ret = sp.call('{0} -o {1} *.c'.format(
                    rule, output_artifact_path), shell=True)
                if ret == 0:
                    print('Successfully compiled {0}.\n\tOut artifact:\t{1}\n'.
                          format(rule_name, output_artifact))
                else:
                    print('Failed to compile {0}:\n\t{1}'.format(
                        rule_name, rule), file=sys.stderr)
                    sys.exit(1)
                artifacts.append(output_artifact_path)
    return artifacts


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError('Incorrect arguments')

    base_dir = os.path.abspath(os.path.dirname(__file__))
    lib_dir = os.path.join(base_dir, 'lib')

    if sys.argv[1] == 'build':
        artifacts = descend_dirs(base_dir, lib_dir)
        sys.exit(0)
    if sys.argv[1] == 'clean':
        shutil.rmtree(lib_dir)
        sys.exit(0)
    elif sys.argv[1] == 'test':
        artifacts = descend_dirs(base_dir, lib_dir)
        for a in artifacts:
            lib = cdll.LoadLibrary(a)
            lib.cholesky([], 0)
