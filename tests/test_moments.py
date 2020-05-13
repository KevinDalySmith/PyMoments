from unittest import TestCase
from PyMoments.Moments import *
from PyMoments.DataStructures import IntPartitionTree
from numpy.testing import assert_array_almost_equal
import os.path


class TestMoments(TestCase):

    def test_kstat_small(self):

        # Create random dataset
        m, d, n = 10, 5, 1000
        X = np.random.randn(m, d, n)
        coef_tree = IntPartitionTree()
        K = lambda modes: kstat(X, modes, sample_axis=2, variable_axis=1, coef_tree=coef_tree)

        # Test means
        means = np.mean(X, axis=2)
        for i in range(d):
            assert_array_almost_equal(means[:, i], K((i,)))

        # Test covariances
        for i in range(d):
            for j in range(i + 1):
                s11 = np.sum(X[:, i, :], axis=1) * np.sum(X[:, j, :], axis=1)
                s2 = np.sum(X[:, i, :] * X[:, j, :], axis=1)
                cov = (s2 / (n - 1)) - (s11 / (n * (n - 1)))
                assert_array_almost_equal(cov, K((i, j)))

        # Test third-order stats
        for i in range(d):
            for j in range(i + 1):
                for k in range(j + 1):
                    s111 = np.sum(X[:, i, :], axis=1) * np.sum(X[:, j, :], axis=1) * np.sum(X[:, k, :], axis=1)
                    s12 = np.sum(X[:, i, :], axis=1) * np.sum(X[:, j, :] * X[:, k, :], axis=1) + \
                          np.sum(X[:, j, :], axis=1) * np.sum(X[:, i, :] * X[:, k, :], axis=1) + \
                          np.sum(X[:, k, :], axis=1) * np.sum(X[:, j, :] * X[:, i, :], axis=1)
                    s3 = np.sum(X[:, i, :] * X[:, j, :] * X[:, k, :], axis=1)
                    k3_true = (2 * s111 - n * s12 + (n ** 2) * s3) / (n * (n-1) * (n-2))
                    assert_array_almost_equal(k3_true, K((i, j, k)))

    def test_kstat_against_nkm(self):

        # Test 4th and 5th order k-stats against the R package "kStatistics":
        # https://cran.r-project.org/web/packages/kStatistics/index.html

        # Load test files
        file_path = os.path.abspath(os.path.dirname(__file__))
        data_path = os.path.join(file_path, './data/test_10path_data.csv')
        index_path = os.path.join(file_path, './data/test_10path_tests.csv')
        data = np.loadtxt(data_path)
        tests = np.loadtxt(index_path)
        alphas = np.array(tests[:, :-1], dtype=int)
        true_kstats = tests[:, -1]

        # Run tests
        coef_tree = IntPartitionTree()
        K = lambda modes: kstat(data, modes, sample_axis=0, variable_axis=1, coef_tree=coef_tree)

        for t in range(alphas.shape[0]):
            modes = tuple()
            for i in range(10):
                modes += (i,) * alphas[t, i]
            assert_array_almost_equal(K(modes), true_kstats[t], decimal=5)

    def test_kstat_coef(self):

        # Coefficients from mean
        self.assertAlmostEqual(kstat_coef(1, [1]), 1)
        self.assertAlmostEqual(kstat_coef(10, [1]), 1/10)

        # Coefficients from covariance
        self.assertAlmostEqual(kstat_coef(2, [1, 1]), -1/2)
        self.assertAlmostEqual(kstat_coef(10, [1, 1]), -1/90)
        self.assertAlmostEqual(kstat_coef(2, [2]), 1)
        self.assertAlmostEqual(kstat_coef(10, [2]), 1/9)

        # Coefficients from 3rd k-stat
        self.assertAlmostEqual(kstat_coef(3, [1, 1, 1]), 1/3)
        self.assertAlmostEqual(kstat_coef(10, [1, 1, 1]), 1/360)
        self.assertAlmostEqual(kstat_coef(3, [1, 2]), -1/2)
        self.assertAlmostEqual(kstat_coef(10, [1, 2]), -1/72)
        self.assertAlmostEqual(kstat_coef(3, [3]), 3/2)
        self.assertAlmostEqual(kstat_coef(10, [3]), 5/36)

        # Coefficients from 4th k-stat
        self.assertAlmostEqual(kstat_coef(4, [1, 1, 1, 1]), -1/4)
        self.assertAlmostEqual(kstat_coef(10, [1, 1, 1, 1]), -6/(10*9*8*7))
        self.assertAlmostEqual(kstat_coef(4, [1, 1, 2]), 1/3)
        self.assertAlmostEqual(kstat_coef(10, [1, 1, 2]), 2/(9*8*7))
        self.assertAlmostEqual(kstat_coef(4, [2, 2]), -1/2)
        self.assertAlmostEqual(kstat_coef(10, [2, 2]), -1/56)
        self.assertAlmostEqual(kstat_coef(4, [1, 3]), -5/6)
        self.assertAlmostEqual(kstat_coef(10, [1, 3]), -11/(9*8*7))
