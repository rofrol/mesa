#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check that kosmicomp declares the result of a wrapping integer operation
unsigned. Signed overflow is undefined in MSL.

Usage: check_unsigned_result.py KOSMICOMP SHADER.comp.spv mul|neg
"""
import re
import subprocess
import sys

SIGNED = {'char', 'short', 'int', 'long'}

# Statement shapes of the operation in the generated MSL (`tN = ...;`).
SHAPES = {
    'mul': r'^\s*(t\d+)\s*=\s*\w+\s*\*\s*[\w(]',
    'neg': r'^\s*(t\d+)\s*=\s*-\s*t\d+\s*;',
}


def main():
    kosmicomp, shader, op = sys.argv[1:4]
    out = subprocess.run([kosmicomp, shader], check=True, text=True,
                         capture_output=True).stdout
    msl = out[out.index('#include <metal_'):]

    decls = {}
    for m in re.finditer(r'^\s*(\w+?)(\d?)\s+(t\d+)\s*=', msl, re.M):
        decls[m.group(3)] = m.group(1)

    results = re.findall(SHAPES[op], msl, re.M)
    if not results:
        print('no %s found in the generated MSL' % op)
        return 1

    bad = [t for t in results if decls.get(t) in SIGNED]
    for t in bad:
        print('result %s of %s is declared %s' % (t, op, decls[t]))
    return 1 if bad else 0


sys.exit(main())
