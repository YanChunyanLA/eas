import random

def _boundary_strategy(vector, ub, lb):
    for i, _ in enumerate(vector):
        if vector[i] > ub[i]:
            vector[i] = ub[i]
        if vector[i] < lb[i]:
            vector[i] = lb[i]
    return vector


def _c_boundary_strategy(c, u, l):
    if c > u:
        return u
    if c < l:
        return l
    return c


def _middle_strategy(vector, ub, lb):
    for i, _ in enumerate(vector):
        if vector[i] > ub[i] or vector[i] < lb[i]:
            vector[i] = (ub[i] + lb[i]) / 2.0
    return vector


def _c_middle_strategy(c, u, l):
    if c > u or c < l:
        c = (u + l) / 2.0
    return c


def _random_strategy(vector, ub, lb):
    for i, _ in enumerate(vector):
        if vector[i] > ub[i] or vector[i] < lb[i]:
            vector[i] = lb[i] + random.random() * (ub[i] - lb[i])
    return vector


def _c_random_strategy(c, u, l):
    if c > u or c < l:
        c = l + random.random() * (u - l)
    return c


class Boundary(object):
    BOUNDARY = 'use boundary'
    MIDDLE = 'use middle'
    RANDOM = 'use random'

    @staticmethod
    def make_strategy(s):
        if s == Boundary.BOUNDARY:
            return _boundary_strategy
        elif s == Boundary.MIDDLE:
            return _middle_strategy
        else:
            return _random_strategy

    @staticmethod
    def make_c_strategy(s):
        if s == Boundary.BOUNDARY:
            return _c_boundary_strategy
        elif s == Boundary.MIDDLE:
            return _c_middle_strategy
        else:
            return _c_random_strategy



