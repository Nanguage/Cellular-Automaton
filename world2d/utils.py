# -*- coding: utf-8 -*-

import os

import numpy as np
from numpy.fft import fft2, ifft2, fftshift
import imageio

def asc_to_arr(filename, row, col):
    """
    transform asc text file to numpy array
    """
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


def fft_convolve2d(x,y):
    """
    2D convolution, using FFT
    borrowed from:
      https://github.com/thearn/game-of-life/blob/master/lib/lib.py#L4
    """
    fr = fft2(x)
    fr2 = fft2(np.flipud(np.fliplr(y)))
    m,n = fr.shape
    cc = np.real(ifft2(fr*fr2))
    cc = np.roll(cc, - int(m / 2) + 1, axis=0)
    cc = np.roll(cc, - int(n / 2) + 1, axis=1)
    return cc


def gen_gif(imgs, gif_path):
    """ write a set of images to a gif file. """
    with imageio.get_writer(gif_path, mode='I') as writer:
        for img in imgs:
            writer.append_data(img)
