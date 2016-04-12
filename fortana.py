#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import os


fldr = '/home/jure/programming/mc_shms_single'

fortextensions = set(['.f', '.inc'])
commentmarks = set(['C', 'D', '*', '!'])


# Get all Fortan files in project directory.
fortfiles = []

for dirpath, dirnames, filenames in os.walk(fldr):
    # Skip git directory.
    if '.git' in dirnames:
        dirnames.remove('.git')

    fortfiles.extend([
        os.path.join(dirpath, filename)
        for filename in filenames
        if os.path.splitext(filename)[1].lower() in fortextensions
        ])


def defines_function(line_up_tok):
    if 'FUNCTION' not in line_up_tok:
        return False

    i = line_up_tok.index('FUNCTION')

    if line_up_tok[0] in commentmarks:
        return False

    for token in line_up_tok[i]:
        if '!' in token:
            return False

    return True


# Get all programs, subroutines and functions defined in project.
programs = []
subroutines = []
functions = []

for fortfile in fortfiles:
    with open(fortfile, 'r') as fi:
        for line in fi:
            line_up_tok = line.upper().split()
            if line_up_tok == [] or line_up_tok[0][0] in commentmarks:
                continue

            if line_up_tok[0] == 'PROGRAM':
                programs.append([line_up_tok[1], fortfile])

            elif line_up_tok[0] == 'SUBROUTINE':
                subroutines.append([line_up_tok[1].split('(')[0], fortfile])

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
                        line_up_tok[i+1].split('(')[0], fortfile])


#for program in programs:
#    print(program)
#for subroutine in subroutines:
#    print(subroutine)
#for function in functions:
#    print(function)


print('\nDone.')
