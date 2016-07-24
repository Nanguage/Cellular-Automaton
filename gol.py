#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

plt.ion()

class World(object):
    '''
    The parent of other world.
    
    These method can be rewrite:
    init_status, update, display
    '''

    def __init__(self, size=(39,39)):
        self.delay = 0.1
        self.row = size[0]
        self.col = size[1]
        self.init_status()
        
        self._next = self.status.copy()
        self.loop_count = 0


    def init_status(self):
        r = np.random.randn(self.row, self.col)
        self.status = np.where(r>0, 1, 0)
        # self.status = np.zeros((self.row, self.col))

    def update(self):
        for i in range(self.row):
            for j in range(self.col):
                alive = self.status[i,j]
                count = self.neighbors((i,j))
                if alive and count < 2:
                    self._next[i,j] = 0
                elif alive and count > 3:
                    self._next[i,j] = 0
                elif not alive and count == 3:
                    self._next[i,j] = 1
        self.loop_count += 1
        # print(self.loop_count)
        self.status = self._next.copy()

    def display(self):
        print("  " + "="*(self.col) + str(self.loop_count) + "="*(self.col))
        # print(self.status)
        for i in range(self.row):
            line = "|| "
            for j in range(self.col):
                if self.status[i,j]:
                    line += '# '
                else:
                    line += '  '
            line += "||"
            print(line)
        print("  " + "="*(self.col) + "="*len(str(self.loop_count)) + "="*(self.col))

    def neighbors(self, pos=(0,0)):
        row, col = self.row-1, self.col-1
        alive = self.status[pos[0], pos[1]]
        if (pos[0] > 0 and pos[0] < row) and \
                (pos[1] > 0 and pos[1] < col):
            # pos not at edge (1 ~ row-1, 1 ~ col-1)
            return self.status[(pos[0]-1):(pos[0]+2),
                    (pos[1]-1):(pos[1]+2)].sum() - alive
        elif pos[0] == 0 and pos[1] != 0 and pos[1] != col:
            # (0, 1 ~ col-1)
            count = self.status[0:2, (pos[1]-1):(pos[1]+2)].sum() - alive
            count += self.status[row, (pos[1]-1):(pos[1]+2)].sum()
            return count
        elif pos[0] != 0 and pos[0] != row and pos[1] == col:
            # (1 ~ row-1, col)
            count = self.status[(pos[0]-1):(pos[0]+2), (col-1):].sum() - alive
            count += self.status[(pos[0]-1):(pos[0]+2), 0].sum()
            return count
        elif pos[0] == row and pos[1] !=0 and pos[1] != col:
            # (row, 1 ~ col-1)
            count = self.status[(row-1):, (pos[1]-1):(pos[1]+2)].sum() - alive
            count += self.status[0, (pos[1]-1):(pos[1]+2)].sum()
            return count
        elif pos[0] != 0 and pos[0] != row and pos[1] == 0:
            # (1 ~ row-1, 0)
            count = self.status[(pos[0]-1):(pos[0]+2), 0:2].sum() - alive
            count += self.status[(pos[0]-1):(pos[0]+2), col].sum()
            return count
        elif pos == (0,0):
            count = self.status[0:2, 0:2].sum() - alive + \
                    self.status[row, 0:2].sum() + \
                    self.status[0:2, col].sum() + \
                    self.status[row, col]
            return count
        elif pos == (0,col):
            count = self.status[0:2, (col-1):].sum() - alive + \
                    self.status[row, (col-1):].sum() + \
                    self.status[0:2, 0].sum() + \
                    self.status[row, 0]
            return count
        elif pos == (row,col):
            count = self.status[(row-1):, (col-1):].sum() - alive + \
                    self.status[0, (col-1):].sum() + \
                    self.status[(row-1):, 0].sum() + \
                    self.status[0, 0]
            return count
        else: # pos = (row,0)
            count = self.status[(row-1):, 0:2].sum() - alive + \
                    self.status[0, 0:2].sum() + \
                    self.status[(row-1):, col].sum() + \
                    self.status[0, col]
            return count

    def run(self, update=None, limit=20000):
        c = 0
        while 1:
            c += 1
            if c > limit: break
            self.display()
            if update is not None:
                update()
            else:
                self.update()
            plt.pause(self.delay)


class WorldGUI(World):
    ''' use matplotlib to display'''
    def __init__(self, size):
        super(WorldGUI, self).__init__(size)
        plt.figure()
        self._img_plot = plt.imshow(self.status, interpolation="nearest", cmap = plt.cm.gray)
        plt.show(block=False)

    def display(self):
        self._img_plot.set_data(self.status)
        plt.draw()

        
if __name__ == '__main__':
    # w = WorldGUI(size)
    w = WorldGUI((100,100))
    w.run(limit=100)
