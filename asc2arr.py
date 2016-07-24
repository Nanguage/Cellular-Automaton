#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def asc_to_arr(filename, row, col):
    with open(filename) as f:
        lines = f.readlines()
    result = []
    for l in lines:
        l = l.strip('\n')
        if l is '':
            result.append(np.zeros(col, dtype=np.int))
        else:
            l = l + ' ' * (col*2 - len(l))
            line = []
            for i, c in enumerate(l):
                if i % 2 == 0:
                    if c != ' ':
                        line.append(1)
                    else:
                        line.append(0)
            result.append(line)
    if len(result) != row:
        for i in range(row - len(result)):
            result.append(np.zeros(col, dtype=np.int))
    result = np.array(result, dtype=np.int)
    return result

