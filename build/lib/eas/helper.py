import numpy as np
import collections


def check_is_range(l, len_of_l):
    return len(l) == len_of_l


def difference(x1, x2):
    return x1 - x2


def factor_multiply(is_matrix_factor, factor, v):
    if is_matrix_factor:
        return np.matmul(factor, v)
    else:
        return factor * v


def multiply(xs):
    if len(xs) == 0:
        return 1
    return xs[0] * multiply(xs[1:])


def init_vector(n, upperxs, lowerxs):
    random_diag = np.diag(np.random.uniform(0, 1, n))
    vector = lowerxs + np.matmul(random_diag, upperxs - lowerxs)
    return vector


def iterable_len(iterable):
    return sum([1 for _ in iterable])


def must_dim_len(vector, n):
    if isinstance(vector, collections.Iterable) and iterable_len(vector) == n:
        return True
    raise TypeError


def must_valid_dimension(n, *args):
    for arg in args:
        must_dim_len(arg, n)
        must_dim_len(arg, n)


def must_callable(o):
    if not callable(o):
        raise TypeError
