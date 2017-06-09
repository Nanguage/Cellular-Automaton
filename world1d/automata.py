
import numpy as np
import matplotlib.pyplot as plt

class Automaton():
    """
    Typical 1-dimentional cellular automaton
    """

    def __init__(self, rule:int, size=100, initial=None):
        self.size = size
        if initial:
            self.status = initial
        else:
            self.status = np.zeros(size, dtype=np.uint8)
            self.status[-1] = 1
        assert 0 <= rule < 256
        rule = "{0:08b}".format(rule)
        rule = [int(i) for i in rule]
        self.rule = tuple(rule)

    def neighbor(self, i:int) -> int:
        length = self.status.shape[0]
        ngs = self.status[[i-1, i, (i+1)%length]]
        return 4*ngs[0] + 2*ngs[1] + ngs[2]

    def update(self):
        frame_size = 3
        length = self.status.shape[0]
        _next = self.status.copy()
        for i in range(length):
            _next[i] = self.rule[7 - self.neighbor(i)]
        self.status = _next

    def display(self, start=0, n=100):
        history = []
        for i in range(start):
            self.update()
        for i in range(n):
            history.append(self.status)
            self.update()
        return np.vstack(history)


if __name__ == "__main__":
    a = Automaton(110, size=1000)
    plt.imshow(a.display(n=1000))
    plt.show()