# -*- coding: utf-8 -*-
# author: a2htray
# description: factors of the numerial operation

from eas import helper
import random
import math


class Factor(object):
    '''super factor
    '''
    def __init__(self, gen, gen_func):
        '''factor construction method
        :param gen: total number of iterations
        :gen_func: the generation method whose parameter is the number of current iteration
        '''
        self.gen = gen
        self.gen_func = gen_func
        self.current_gen = 1

    def next(self):
        '''next
        a output is represented when it is invoked
        '''
        if self.current_gen == self.gen + 1:
            raise ValueError('exceed the limit of generation, could not generate a new factor')

        facotr = self.gen_func(self.current_gen)
        self.current_gen += 1

        return facotr


def create_factor(gen, gen_func):
    return Factor(gen, gen_func)


class ConstantFactor(Factor):
    '''constant factor
    In each iteration, the output is always the same
    '''
    def __init__(self, c, gen):
        '''
        :param c: a constant value
        :param gen: total number of iterations
        '''
        Factor.__init__(self, gen, self.constant)
        self.c = c

    def constant(self, g):
        return self.c


class RandomFactor(Factor):
    '''random factor
    the factor generated uniformly in the given range.
    '''
    def __init__(self, l, gen, has_direct=False):
        '''
        :param l: the boundaries, iterable object, its size is 2
        :param gen: total number of iterations
        :param has_direct: the flag indicating whether the output has a direct coefficient
        '''
        Factor.__init__(self, gen, self.random)
        self.l = l
        self.has_direct = has_direct

        if not helper.check_is_range(self.l, 2):
            raise ValueError('the length of the range must be 2')

    def random(self, g):
        v = self.l[0] + random.random() * (self.l[1] - self.l[0])

        if not self.has_direct:
            return v

        f = random.random()

        return v if f > 0.5 else -v


class LinearFactor(Factor):
    '''linear factor
    '''
    def __init__(self, l, gen):
        '''
        :param l: the boundaries, iterable object, its size is 2
        :param gen: total number of iterations
        '''
        Factor.__init__(self, gen, self.linear)
        self.l = l

        if not helper.check_is_range(self.l, 2):
            raise ValueError('the length of the range must be 2')

        self._low, self._high = self.l[0], self.l[1]
    
    def linear(self, g):
        return self._low + (1 - (g * 1.0) / self.gen) * (self._high - self._low)


class ExpFactor(Factor):
    '''exponent factor
    '''
    def __init__(self, l, gen):
        '''
        :param l: the boundaries, iterable object, its size is 2
        :param gen: total number of iterations
        '''
        Factor.__init__(self, gen, self.exp)
        self.l = l

        if not helper.check_is_range(self.l, 2):
            raise ValueError('the length of the range must be 2')

        self._low, self._high = self.l[0], self.l[1]
    
    def exp(self, g):
        return self._low + (1 - math.e **(math.log((g*1.0) / self.gen))) * (self._high - self._low)