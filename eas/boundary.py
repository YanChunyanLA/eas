import random


def _boundary_strategy(vector, upperxs, lowerxs):
    for i, _ in enumerate(vector):
        if vector[i] > upperxs[i]:
            vector[i] = upperxs[i]
        if vector[i] < lowerxs[i]:
            vector[i] = lowerxs[i]
    return vector


def _middle_strategy(vector, upperxs, lowerxs):
    for i, _ in enumerate(vector):
        if vector[i] > upperxs[i] or vector[i] < lowerxs[i]:
            vector[i] = (upperxs[i] + lowerxs[i]) / 2.0
    return vector


def _random_strategy(vector, upperxs, lowerxs):
    for i, _ in enumerate(vector):
        if vector[i] > upperxs[i] or vector[i] < lowerxs[i]:
            vector[i] = lowerxs[i] + random.random() * (upperxs[i] - lowerxs[i])
    return vector


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


