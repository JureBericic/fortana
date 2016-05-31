#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import os
import re

import file_tree


output_folder = 'analysis'
commentmarks = set(['C', 'D', '*', '!'])


# Find all fortran files.
fortfiles = file_tree.FileTree(
    '/home/jure/programming/mc_shms_single',
    skip_dirs=['infiles', 'outfiles', 'workfiles', '.git'],
    extensions=['f', 'inc']
)


# Pass 1.
# Find names of all defined programs, subroutines and functions.
programs = []
subroutines = []
functions = []

for fortfile in fortfiles.files:
    with open(fortfile, 'r') as fi:
        rel_path = os.path.relpath(fortfile, fortfiles.root_folder)
        for line in fi:
            line_up_tok = line.upper().split()
            if line_up_tok == [] or line_up_tok[0][0] in commentmarks:
                continue

            if line_up_tok[0] == 'PROGRAM':
                programs.append((line_up_tok[1], rel_path))

            elif line_up_tok[0] == 'SUBROUTINE':
                subroutines.append((line_up_tok[1].split('(')[0], rel_path))

            elif 'FUNCTION' in line_up_tok:
                i = line_up_tok.index('FUNCTION')
                # Check if comment starts before keyword.
                comment = False
                for token in line_up_tok[:i]:
                    if '!' in token:
                        comment = True
                        continue
                if not comment:
                    functions.append((
                        line_up_tok[i+1].split('(')[0], rel_path))


# Pass 2.
# Find all cals to defined subroutines and programs.
s_subroutines = set([subroutine[0] for subroutine in subroutines])
s_functions = set(function[0] for function in functions)
re_functions = [
    re.compile(r"[^a-zA-Z0-9]("+function+"\()") for function in s_functions]

subroutine_calls = []
function_calls = []

for fortfile in fortfiles.files:
    with open(fortfile, 'r') as fi:
        rel_path = os.path.relpath(fortfile, fortfiles.root_folder)
        for line in fi:
            line_up = line.upper()
            line_up_tok = line_up.split()

            if line_up_tok == [] or line_up[0] in commentmarks:
                continue

            if line_up_tok[0] == 'CALL':
                subroutine = line_up_tok[1].split('(')[0]
                if subroutine in s_subroutines:
                    subroutine_calls.append((subroutine, rel_path))

            # TODO: check if function call in comment.
            ln1 = ''.join(line_up.split())
            for re_function, function in zip(re_functions, s_functions):
                match = re_function.search(ln1)
                if match:
                    #print(function + ' : ' + ln1)
                    function_calls.append((function, rel_path))


subroutine_calls = set(subroutine_calls)
function_calls = set(function_calls)

print(subroutine_calls)
print()
print(function_calls)



print('\nDone.')
