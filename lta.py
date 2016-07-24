#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Langton Ant (
https://zh.wikipedia.org/wiki/%E5%85%B0%E9%A1%BF%E8%9A%82%E8%9A%81)
in python
'''
import time

import numpy as np

from gol import WorldGUI, World
from asc2arr import asc_to_arr

class Ant(object):
    def __init__(self, pos, dire, mapsize):
        self.pos = pos
        self.dir = dire
        self.map = mapsize

    def roate(self):
        self.dir -= (np.pi/2)
        self.dir = self.dir % (2 * np.pi)

    def contraroate(self):
        self.dir += (np.pi/2)
        self.dir = self.dir % (2 * np.pi)

    def step(self):
        y, x = self.pos
        r, c = self.map
        dy = np.sin(self.dir)
        dx = np.cos(self.dir)
        self.pos = (round(y-dy)%r, round(x+dx)%c)
        print dy,dx,self.pos

    def backstep(self):
        y, x = self.pos
        r, c = self.map
        dy = -np.sin(self.dir)
        dx = -np.cos(self.dir)
        self.pos = (round(y-dy)%r, round(x+dx)%c)


class AntWorld(WorldGUI):
    '''Langton Ants'''
    def __init__(self, size=(39,39)):
        # self.ant = Ant((size[0]//2-1,size[1]//2-1), 'l', size)
        self.ant = Ant((size[0]//2-1,size[1]//2-1), -np.pi, size)
        super(AntWorld, self).__init__(size)

    def init_status(self):
        # self.status = np.zeros((self.row, self.col), dtype=np.int)
        # self.status[0,0] = 1
        self.status = asc_to_arr('./pattern/test2.txt',39,39)

    def update(self):
        y, x = self.ant.pos
        alive = self.status[y, x]
        print(self.loop_count)
        print str(self.ant.pos) + ' ' + str(alive) + ' ' + str(self.ant.dir)
        if alive:
            self.ant.roate()
            self.status[y, x] = 0
            self.ant.step()
        else:
            self.ant.contraroate()
            self.status[y, x] = 1
            self.ant.step()
        self.loop_count += 1

    def update_rev(self):
        self.ant.backstep()
        y, x = self.ant.pos
        alive = self.status[y, x]
        print(self.loop_count)
        print str(self.ant.pos) + ' ' + str(alive) + ' ' + str(self.ant.dir)
        if alive:
            self.status[y, x] = 0
            self.ant.roate()
        else:
            self.status[y, x] = 1
            self.ant.contraroate()
        self.loop_count -= 1

    def run(self, limit):
        super(AntWorld, self).run(update=self.update,limit=limit)

    def run_not_show(self, steps):
        for i in xrange(steps): self.update()

    def run_rev(self, limit):
        super(AntWorld, self).run(update=self.update_rev, limit=limit)

    def go_then_back(self, limit=300):
        self.run(limit)
        print("Reverse Now!")
        time.sleep(3)
        self.run_rev(limit)


if __name__ == '__main__':
    # aw = AntWorld((60,60))
    # aw = AntWorld((5,5))
    aw = AntWorld()
    aw.delay = 0.01
    # aw.go_then_back(700)
    aw.run_not_show(2000)
    aw.run_rev(2000)
