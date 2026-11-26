# Copyright 2025 LunarG, Inc.
# Copyright 2025 Google LLC
# SPDX-License-Identifier: MIT

subdir('bridge')
subdir('compiler')
subdir('util')
subdir('clc')
subdir('libkk')
subdir('vulkan')

kosmicomp = executable(
    'kosmicomp',
    files('kosmicomp.c'),
    dependencies : [idep_nir, idep_vtn, idep_vulkan_runtime_headers, idep_vulkan_util_headers],
    link_with: [libkk],
    link_args: ['-Wl,-undefined,dynamic_lookup'],
)

foreach t : [['imul', 'mul'], ['ineg', 'neg']]
    test(
        'kosmicomp-unsigned-' + t[0],
        prog_python,
        args : [
            files('tests/check_unsigned_result.py'),
            kosmicomp,
            files('tests/' + t[0] + '_wrap.comp.spv'),
            t[1],
        ],
        suite : ['kosmickrisp'],
    )
endforeach
