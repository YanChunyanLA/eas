import unittest
from eas.base.utils import init_vector
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_something(self):
        a = np.array([1, 2, 3], dtype=float)
        b = np.array([2, 3, 4], dtype=float)
        rs = np.random.random(size=3)
        print((b - a)*rs + a)

        print(init_vector(3, a, b))


if __name__ == '__main__':
    unittest.main()
