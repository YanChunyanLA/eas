from eas import helper
import random
import math

class Factor(object):
    def __init__(self, gen, gen_func):
        self.gen = gen
        self.gen_func = gen_func
        self.current_gen = 1

    def next(self):
        if self.current_gen == self.gen + 1:
            raise('exceed the limit of generation, could not generate a new factor')

        facotr = self.gen_func(self.current_gen)
        self.current_gen += 1

        return facotr

def create_factor(gen, gen_func):
    return Factor(gen, gen_func)

class ConstantFactor(Factor):
    def __init__(self, c, gen):
        Factor.__init__(self, gen, self.constant)
        self.c = c

    def constant(self, g):
        return self.c

class RandomFactor(Factor):
    def __init__(self, l, gen, has_direct=False):
        Factor.__init__(self, gen, self.random)
        self.l = l
        self.has_direct = has_direct

        if not helper.check_is_range(self.l, 2):
            raise('the length of the range must be 2')

    def random(self, g):
        v = random.random()

        if not self.has_direct:
            return v

        f = random.random()

        return v if f > 0.5 else -v

class LinearFactor(Factor):
    def __init__(self, l, gen):
        Factor.__init__(self, gen, self.linear)
        self.l = l

        if not helper.check_is_range(self.l, 2):
            raise('the length of the range must be 2')

        self._low, self._high = self.l[0], self.l[1]
    
    def linear(self, g):
        return self._low + (1 - (g * 1.0) / self.gen) * (self._high - self._low)

class ExpFactor(Factor):
    def __init__(self, l, gen):
        Factor.__init__(self, gen, self.exp)
        self.l = l

        if not helper.check_is_range(self.l, 2):
            raise('the length of the range must be 2')

        self._low, self._high = self.l[0], self.l[1]
    
    def exp(self, g):
        return self._low + (1 - math.e **(math.log((g*1.0) / self.gen))) * (self._high - self._low)