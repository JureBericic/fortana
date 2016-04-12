#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import os


root_folder = '/home/jure/programming/mc_shms_single'
output_folder = 'analysis'

fortextensions = set(['.f', '.inc'])
commentmarks = set(['C', 'D', '*', '!'])


# Get all Fortan files in project directory.
fortfiles = []

for dirpath, dirnames, filenames in os.walk(root_folder):
    # Skip git directory.
    if '.git' in dirnames:
        dirnames.remove('.git')

    fortfiles.extend([
        os.path.join(dirpath, filename)
        for filename in filenames
        if (os.path.splitext(filename)[1].lower() in fortextensions) and
        ('_sub' not in filename)
        ])


# Get all programs, subroutines and functions defined in project.
programs = []
subroutines = []
functions = []

for fortfile in fortfiles:
    with open(fortfile, 'r') as fi:
        rel_path = os.path.relpath(fortfile, root_folder)
        for line in fi:
            line_up_tok = line.upper().split()
            if line_up_tok == [] or line_up_tok[0][0] in commentmarks:
                continue

            if line_up_tok[0] == 'PROGRAM':
                programs.append([line_up_tok[1], rel_path])

            elif line_up_tok[0] == 'SUBROUTINE':
                subroutines.append([line_up_tok[1].split('(')[0], rel_path])

            elif 'FUNCTION' in line_up_tok:
                i = line_up_tok.index('FUNCTION')
                # Check if comment starts before keyword.
                comment = False
                for token in line_up_tok[i]:
                    if '!' in token:
                        comment = True
                        continue
                if not comment:
                    functions.append([
                        line_up_tok[i+1].split('(')[0], rel_path])


if not os.path.exists(output_folder):
    os.makedirs(output_folder)


with open(os.path.join(output_folder, 'list.txt'), 'w') as fo:
    fo.write('Programs:\n')
    fo.write('=========\n')
    for program in sorted(programs):
        fo.write('{} : {}\n'.format(program[0], program[1]))
    fo.write('\n')

    fo.write('Subroutines:\n')
    fo.write('============\n')
    for subroutine in sorted(subroutines):
        fo.write('{} : {}\n'.format(subroutine[0], subroutine[1]))
    fo.write('\n')

    fo.write('Functions:\n')
    fo.write('==========\n')
    for function in sorted(functions):
        fo.write('{} : {}\n'.format(function[0], function[1]))
    fo.write('\n')



print('\nDone.')
