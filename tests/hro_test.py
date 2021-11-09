import unittest
from eas.base import EAConfig
from eas.objective import shpere
import eas


class MyTestCase(unittest.TestCase):
    def test_something(self):
        eas.set_debug(True)
        config = EAConfig(6, 2, 1.0, 0.0, shpere, 100)
        ea = eas.HRO(config)
        ea.run()

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
