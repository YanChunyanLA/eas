import unittest
from eas.base import Population
from eas.objective import shpere


class MyTestCase(unittest.TestCase):
    def test_something(self):
        p = Population(4, 2, ulimit=1.0, llimit=0.0)
        print(p.apply(shpere).fitness_list())
        print(p.solutions[0].fitness())
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
