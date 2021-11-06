import unittest
from eas.base import Solution, create_indexed_solution
from eas.objective import shpere, bent_cigar


class MyTestCase(unittest.TestCase):
    def test_something(self):
        s: Solution = Solution(2, ulimit=1.)
        self.assertIsInstance(s, Solution, 'is not Solution')
        print(s.raw())

        s = Solution(3, ulimit=[1, 2, 3], llimit=[-1, -2, -3])
        print(s.raw())

        s = Solution(4, ulimit=1.0, llimit=0.0)
        print(s)

    def test_apply(self):
        s = Solution(3, ulimit=[1, 2, 3], llimit=[-1, -2, -3])
        print(s.apply(shpere).fitness())
        print(s.apply(bent_cigar).fitness())

        self.assertEqual(True, True)

    def test_index(self):
        s = create_indexed_solution(1, 3, ulimit=[1, 2, 3], llimit=[-1, -2, -3])
        print(s.apply(shpere).fitness())
        print(s.apply(bent_cigar).fitness())

        self.assertEqual(s.index, 1)


if __name__ == '__main__':
    unittest.main()
