import numpy as np

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

def init_vector(N, U, L):
    random_diag = np.diag(np.random.uniform(0, 1, N))
    vector = L + np.matmul(random_diag, U - L)
    return vector

    