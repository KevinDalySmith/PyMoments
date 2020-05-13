from unittest import TestCase
from PyMoments.Combinatorics import *


class TestCombinatorics(TestCase):

    def test_simplex_iter(self):

        # Test empty case
        empty_case_1 = list(simplex_iter(1, [1, 1]))
        empty_case_2 = list(simplex_iter(0, [1]))
        self.assertEqual(len(empty_case_1), 0)
        self.assertEqual(len(empty_case_2), 0)

        # Test one-element cases
        singleton_case_1 = list(simplex_iter(1, [1]))
        singleton_case_2 = list(simplex_iter(5, [1, 2, 3, 4, 5]))
        self.assertListEqual(singleton_case_1, [(1,)])
        self.assertListEqual(singleton_case_2, [(1, 1, 1, 1, 1)])

        # Test some simple cases
        simple_case_1 = set(simplex_iter(4, [1, 2, 3]))
        simple_case_2 = set(simplex_iter(5, [1, 2, 3]))
        simple_case_1_true = {(1, 1, 2), (1, 2, 1)}
        simple_case_2_true = {(1, 1, 3), (1, 2, 2)}
        self.assertSetEqual(simple_case_1, simple_case_1_true)
        self.assertSetEqual(simple_case_2, simple_case_2_true)

    def test_set_partitions(self):

        # Test partitions of an empty set
        s0_parts_est = list(set_partitions([]))
        self.assertEqual(len(s0_parts_est), 0)

        # Test partitions of a 1-element set
        s1 = ['dirigible']
        s1_parts_true = {
            frozenset([('dirigible',)])}
        s1_parts_est = set(map(frozenset, set_partitions(s1)))
        self.assertSetEqual(s1_parts_est, s1_parts_true)

        # Test partitions of a 2-element set
        s2 = [1, -1]
        s2_parts_true = {
            frozenset([(1,), (-1,)]),
            frozenset([(1, -1)])}
        s2_parts_est = set(map(frozenset, set_partitions(s2)))
        self.assertSetEqual(s2_parts_est, s2_parts_true)

        # Test partitions of a 3-element set
        s3 = ['apple', 'banana', 1.4]
        s3_parts_true = {
            frozenset([('apple',), ('banana',), (1.4,)]),
            frozenset([('apple', 'banana'), (1.4,)]),
            frozenset([('apple', 1.4), ('banana',)]),
            frozenset([('apple',), ('banana', 1.4)]),
            frozenset([('apple', 'banana', 1.4)])}
        s3_parts_est = set(map(frozenset, set_partitions(s3)))
        self.assertSetEqual(s3_parts_est, s3_parts_true)

        # Test partitions of a 4-element set
        s4 = [1, 2, 3, 4]
        s4_parts_true = {
            frozenset([(1,), (2,), (3,), (4,)]),
            frozenset([(1, 2), (3,), (4,)]),
            frozenset([(1, 3), (2,), (4,)]),
            frozenset([(1, 4), (2,), (3,)]),
            frozenset([(2, 3), (1,), (4,)]),
            frozenset([(2, 4), (1,), (3,)]),
            frozenset([(3, 4), (1,), (2,)]),
            frozenset([(1, 2), (3, 4)]),
            frozenset([(1, 3), (2, 4)]),
            frozenset([(1, 4), (2, 3)]),
            frozenset([(1, 2, 3), (4,)]),
            frozenset([(1, 2, 4), (3,)]),
            frozenset([(1, 3, 4), (2,)]),
            frozenset([(2, 3, 4), (1,)]),
            frozenset([(1, 2, 3, 4)])}
        s4_parts_est = set(map(frozenset, set_partitions(s4)))
        self.assertSetEqual(s4_parts_est, s4_parts_true)

        # Validate sizes of larger sets
        bell_numbers = [52, 203, 877, 4140, 21147, 115975]
        for n in range(5, 11):
            count = 0
            for _ in set_partitions(list(range(n))):
                count += 1
            self.assertEqual(count, bell_numbers[n-5])

    def test_ff(self):

        self.assertEqual(ff(0, 0), 1)

        for n in range(1, 11):
            self.assertEqual(ff(n, 0), 1)
            ff_true = n
            for i in range(1, n + 1):
                self.assertEqual(ff(n, i), ff_true)
                ff_true *= (n - i)

    def test_factorial(self):

        facts = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
        for n in range(10):
            self.assertEqual(factorial(n), facts[n])

    def test_binom(self):

        # First 5 rows of Pascal's triangle
        self.assertEqual(binom(0, 0), 1)
        self.assertEqual(binom(1, 0), 1)
        self.assertEqual(binom(1, 1), 1)
        self.assertEqual(binom(2, 0), 1)
        self.assertEqual(binom(2, 1), 2)
        self.assertEqual(binom(2, 2), 1)
        self.assertEqual(binom(3, 0), 1)
        self.assertEqual(binom(3, 1), 3)
        self.assertEqual(binom(3, 2), 3)
        self.assertEqual(binom(3, 3), 1)
        self.assertEqual(binom(4, 0), 1)
        self.assertEqual(binom(4, 1), 4)
        self.assertEqual(binom(4, 2), 6)
        self.assertEqual(binom(4, 3), 4)
        self.assertEqual(binom(4, 4), 1)

        # Selected larger values
        self.assertEqual(binom(5, 2), 10)
        self.assertEqual(binom(7, 2), 21)
        self.assertEqual(binom(8, 2), 28)
        self.assertEqual(binom(8, 4), 70)
        self.assertEqual(binom(20, 14), 38760)
