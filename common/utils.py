from __future__ import division, print_function

class Limits(float):
    def __new__(self, value, minval, maxval):
        return float.__new__(self, value)

    def __init__(self, value, minval, maxval):
        if value >= minval and value <= maxval:
            float.__init__(value)
            self.minval = minval
            self.maxval = maxval
        else:
            raise Exception('Value out of bounds.')

    def min(self):
        return self.minval

    def max(self):
        return self.maxval
