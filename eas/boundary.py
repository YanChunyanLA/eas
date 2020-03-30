import random


def _boundary_strategy(vector, us, ls):
    for i, _ in enumerate(vector):
        if vector[i] > us[i]:
            vector[i] = us[i]
        if vector[i] < ls[i]:
            vector[i] = ls[i]
    return vector


def _c_boundary_strategy(c, u, l):
    if c > u:
        return u
    if c < l:
        return l
    return c


def _middle_strategy(vector, us, ls):
    for i, _ in enumerate(vector):
        if vector[i] > us[i] or vector[i] < ls[i]:
            vector[i] = (us[i] + ls[i]) / 2.0
    return vector


def _c_middle_strategy(c, u, l):
    if c > u or c < l:
        c = (u + l) / 2.0
    return c


def _random_strategy(vector, us, ls):
    for i, _ in enumerate(vector):
        if vector[i] > us[i] or vector[i] < ls[i]:
            vector[i] = ls[i] + random.random() * (us[i] - ls[i])
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



