import random


def _boundary_strategy(vector, upperxs, lowerxs):
    for i, _ in enumerate(vector):
        if vector[i] > upperxs[i]:
            vector[i] = upperxs[i]
        if vector[i] < lowerxs[i]:
            vector[i] = lowerxs[i]
    return vector


def _c_boundary_strategy(c, upperx, lowerx):
    if c > upperx:
        return upperx
    if c < lowerx:
        return lowerx
    return c


def _middle_strategy(vector, upperxs, lowerxs):
    for i, _ in enumerate(vector):
        if vector[i] > upperxs[i] or vector[i] < lowerxs[i]:
            vector[i] = (upperxs[i] + lowerxs[i]) / 2.0
    return vector


def _c_middle_strategy(c, upperx, lowerx):
    if c > upperx or c < lowerx:
        c = (upperx + lowerx) / 2.0
    return c


def _random_strategy(vector, upperxs, lowerxs):
    for i, _ in enumerate(vector):
        if vector[i] > upperxs[i] or vector[i] < lowerxs[i]:
            vector[i] = lowerxs[i] + random.random() * (upperxs[i] - lowerxs[i])
    return vector


def _c_random_strategy(c, upperx, lowerx):
    if c > upperx or c < lowerx:
        c = lowerx + random.random() * (upperx - lowerx)
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



