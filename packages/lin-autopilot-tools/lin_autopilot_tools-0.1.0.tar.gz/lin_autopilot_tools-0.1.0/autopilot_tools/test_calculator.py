import unittest
from calculator import add, sub

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_sub(self):
        self.assertEqual(sub(2, 2), 0)
        self.assertEqual(sub(2, 2), 1)