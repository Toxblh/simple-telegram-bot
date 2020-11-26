# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from main import just_for_test


class TestSimple(unittest.TestCase):

    def test_welcome(self):
        test_text = 'text'
        self.assertEqual(just_for_test(test_text), test_text)


if __name__ == '__main__':
    unittest.main()
