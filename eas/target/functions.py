import math
from eas import helper

def bent_cigar(xs):
    return xs[0]**2 + 10**6 * sum([x**2 for x in xs[1:]])

def discus(xs):
    return 10**6 * xs[0]**2 + sum([x**2 for x in x[1:]])

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