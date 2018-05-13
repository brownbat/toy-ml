# -*- coding: utf-8 -*-
"""Unit tests for toy-ml.
"""
import unittest
import random
import itertools
import io
import sys
sys.path.append('../')
import ml  # noqa


def test():
    # Here it correctly identifies 'BCDEF' as an example in the category of
    # words that are sequentially alphabetic, as opposed to random letters.
    case = 'BCDEF'
    print(classify(case, [cat_1(), cat_2()], [test_1, test_2, test_3],
          verbose=True))
    print(classify(case, [cat_1(), cat_2()], [test_1, test_2, test_3]))


class TestML(unittest.TestCase):
    def test_classify(self):
        """Classify tests

        Test if classifier can correctly distinguish sequential letters
        from random letters.
        """

        def cat_1():
            """Returns a five character string of sequential cap letters."""
            while True:
                c = random.randint(0, 21)
                s = ''
                for i in range(5):
                    s += chr(ord('A') + c + i)
                yield s

        def cat_2():
            """Returns a five-character string of random capital letters."""
            while True:
                s = ''
                for i in range(5):
                    a = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                    s += a
                yield s

        def test_1(a):
            """Returns 1 if second letter is one higher than first."""
            if ord(a[0]) == ord(a[1]) - 1:
                return 1
            else:
                return 0

        def test_2(a):
            """Returns 1 if third letter is two higher than first."""
            if ord(a[0]) == ord(a[2]) - 2:
                return 1
            else:
                return 0

        def test_3(a, normalized=True):
            """Returns number of simple vowels."""
            count = 0
            for i in a:
                if i in 'AEIOU':
                    count += 1
            if normalized:
                return count // len(a)
            else:
                return count

        case = 'BCDEF'

        # Positive tests
        classified_idx = ml.classify(case, [cat_1(), cat_2()], [test_1, test_2,
                                     test_3])
        assert (classified_idx == 0),\
            "Inccorrectly classified case {}. \n Received: {} \n" +\
            "Expected: {}".format(case, classified_idx, '0')


if __name__ == "__main__":
    unittest.main()  # verbosity = 2)
