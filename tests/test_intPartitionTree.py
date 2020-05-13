from unittest import TestCase
from PyMoments.DataStructures import IntPartitionTree


class TestIntPartitionTree(TestCase):

    def setUp(self):

        # Build up a sample tree
        self.T1 = IntPartitionTree()
        self.T1.set_coef((3, 1, 2), 'apple')
        self.T1.set_coef((1, 1, 4), 'banana')
        self.T1.set_coef((), 'strawberry')
        self.T1.set_coef([2], 'pineapple')
        self.T1.set_coef([1, 2, 3, 1], 'mango')
        self.T1.set_coef([1, 2], 'kiwi')
        self.T1.set_coef([2, 1, 3], 'overwritten')

    def test_get_coef(self):
        self.assertEqual(self.T1.get_coef([]), 'strawberry')
        self.assertEqual(self.T1.get_coef((2,)), 'pineapple')
        self.assertEqual(self.T1.get_coef([1, 2]), 'kiwi')
        self.assertEqual(self.T1.get_coef((1, 2, 3)), 'overwritten')
        self.assertEqual(self.T1.get_coef((1, 4, 1)), 'banana')
        self.assertEqual(self.T1.get_coef([3, 2, 1, 1]), 'mango')
        self.assertIsNone(self.T1.get_coef([1]))
        self.assertIsNone(self.T1.get_coef([3]))
        self.assertIsNone(self.T1.get_coef([1, 3]))
        self.assertIsNone(self.T1.get_coef([1, 2, 3, 4]))

    def test_set_coef(self):

        self.assertEqual(len(self.T1.children), 2)
        self.assertEqual(len(self.T1.children[0].children), 2)
        self.assertEqual(len(self.T1.children[1].children), 0)
        self.assertEqual(len(self.T1.children[0].children[0].children), 4)
        self.assertEqual(self.T1.children[0].min_branch, 1)
        self.assertEqual(self.T1.children[1].min_branch, 2)

        self.assertIsNone(self.T1.children[0].children[0].children[0])
        self.assertIsNone(self.T1.children[0].children[0].children[2])
        self.assertEqual(self.T1.min_branch, 1)
        self.assertEqual(self.T1.children[0].children[0].children[3].min_branch, 4)
        self.assertEqual(len(self.T1.children[0].children[0].children[3].children), 0)

    def test_n_nodes(self):
        self.assertEqual(self.T1.n_nodes(), 9)

    def test_depth(self):
        self.assertEqual(self.T1.depth(), 5)
