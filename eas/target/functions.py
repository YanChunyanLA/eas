import math
from eas import helper
import numpy as np
import random


def Shpere(xs):
    return sum([x for x in xs])


def bent_cigar(xs):
    return xs[0]**2 + 10**6 * sum([x**2 for x in xs[1:]])


def discus(xs):
    return 10**6 * xs[0]**2 + sum([x**2 for x in xs[1:]])


def weierstrass(a, b, kmax):
    def f(xs):
        D = len(xs)
        part1 = sum([sum([a**k * math.cos(2 * math.pi * b**2 * (x + 0.5)) for k in range(kmax + 1)]) for x in xs])
        part2 = D * sum([a**k * math.cos(2 * math.pi * b**k * 0.5) for k in range(kmax + 1)])

        return part1 - part2

    return f


def rosenbrock(xs):
    return sum([100 * (xs[i + 1]**2 - xs[i])**2 + (1 - xs[i])**2 for i in range(len(xs) - 1)])


def griewank(xs):
    return 1.0 / 4000 * sum([x for x in xs]) + 1 - helper.multiply([x / math.sqrt(i + 2) for i, x in enumerate(xs)])


def elliptic(f_star):
    def exp_elliptic(xs):
        d = len(xs)
        return sum([(10 ** 6) ** ((i - 1) / (d - 1)) * xs[i - 1] ** 2 for i in range(1, d + 1)]) + f_star

    return exp_elliptic


def rastrigin(f_star):
    def exp_rastrigin(xs):
        return sum([x**2 + 10 * math.cos(2 * math.pi * x) + 10 for x in xs]) + f_star

    return exp_rastrigin


def exp_ackley(xs):
    d = len(xs)
    p1 = math.sqrt(1.0 / d * sum([x**2 for x in xs]))
    p2 = 1.0 / d * sum([math.cos(2 * math.pi * x) for x in xs])

    return -20 * math.exp(-0.2 * p1) - math.exp(p2) + 20 + math.e


def exp_schwefel(xs):
    d = len(xs)
    result = 0
    for i in range(d):
        temp = 0
        for j in range(i):
            temp += xs[j]
        result += temp**2
    return result


def exp_rosenbrock(xs):
    d = len(xs)
    print(np.dot(xs, np.random.rand(4, 4)))
    return sum([100 * (xs[i]**2 - xs[i+1])**2 + (xs[i] - 1)**2 for i in range(0, d - 1)])


def f1(xs):
    return sum([x ** 2 for x in xs])


def f2(xs):
    p1 = sum([abs(x) for x in xs])
    p2 = helper.multiply([abs(x) for x in xs])
    return p1 + p2


def f3(xs):
    d = len(xs)
    result = 0
    for i in range(d):
        temp = 0
        for j in range(i):
            temp += xs[j]
        result += temp**2
    return result


def f4(xs):
    return max([abs(x) for x in xs])


def f5(xs):
    d = len(xs)
    count = 0.0
    for i in range(d-1):
        count += (100 * (xs[i+1] - xs[i] ** 2) ** 2 + (xs[i] - 1) ** 2)
    return count


def f6(xs):
    return sum([(math.floor(x + 0.5)) ** 2 for x in xs])


# f7需要注意
def f7(xs):
    return sum([abs(x * math.sin(x) + 0.1 * x) for x in xs])


def f8(xs):
    d = len(xs)
    return sum([-x * math.sin(np.sqrt(abs(x))) for x in xs]) + d * 418.98288727243369


def f9(xs):
    return sum([x**2 - 10 * math.cos(2 * math.pi * x) + 10 for x in xs])


def f10(xs):
    d = len(xs)
    p1 = math.sqrt(1.0 / d * sum([x ** 2 for x in xs]))
    p2 = 1.0 / d * sum([math.cos(2 * math.pi * x) for x in xs])

    return -20 * math.exp(-0.2 * p1) - math.exp(p2) + 20 + math.e


def f11(xs):
    p1 = sum([x ** 2 for x in xs])
    p2 = helper.multiply([math.cos(x / math.sqrt(i + 2)) for i, x in enumerate(xs)])
    return 1.0 / 4000 * p1 - p2 + 1