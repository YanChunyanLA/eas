import numpy as np
import pandas as pd
from eas.collection import Collection

np.random.seed(1)


def func(xs):
    return sum(xs)


U = [10] * 2
L = [-10] * 2
c = Collection(10, 2, U, L)

print(c.get_collection())


# c[1] = [200, -200]
# print(c[1])
# c.amend_item(1)
# print(c.apply(func))
# c.sort(func)
print(c._collection[1])

# print(pd.DataFrame(c.get_collection()))


# c.sort(func)
# print(c.get_collection())
# s = np.array([20, 20])
# c[2] = s
#
# for i, s in enumerate(c):
#     print(i, s)
# c[1] = [11, 22]
# print(c[1])
#
# print(c.get_collection())

# arr = np.array([[1, 2, 3], [4, 5, 6]])
# print(np.apply_over_axes(func, arr, axes=1))

# print(c.apply(func))