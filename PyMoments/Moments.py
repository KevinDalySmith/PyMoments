"""
Moments.py
Key functions and helper functions for computing moment statistics.
"""

import numpy as np
from PyMoments.Combinatorics import *
from PyMoments.DataStructures import *


def kstat(data, modes, sample_axis=0, variable_axis=1, coef_tree=None):
    """
    Compute a multivariate k-statistic.

    Parameters
    ----------
    data : NumPy array
        Array of input data. Columns correspond to variables, and each row is an observation.
    modes : sequence of ints
        Multiset of modes (i.e., indices of columns of the data), representing which k-statistic to compute.
    sample_axis : int, optional
        Axis of the data array corresponding to different observations.
        Default is 0, so that each row is a different observation.
    variable_axis : int, optional
        Axis of the data array corresponding to different modes / random variable.
        Default is 1, so that each column is a different mode / random variable.
    coef_tree : IntPartitionTree, optional
        Efficient data structure to memoize coefficients in the computation.
        When evaluating many k-stats on the same data, this tree may be re-used to reduce runtime.

    
    Returns
    -------
    k : float, or array of floats
        If data is a 2D array, returns a single multivariate k-statistic.
        If data is a 3D array or larger, returns an array of the same shape, but
        with the sample axis and variable axis flattened.
    """

    n, d, r = data.shape[sample_axis], data.shape[variable_axis], len(data.shape)
    if coef_tree is None:
        coef_tree = IntPartitionTree()
    slice_left, slice_right = (slice(None),) * variable_axis, (slice(None),) * (r - variable_axis - 1)
    true_sample_axis = sample_axis if sample_axis < variable_axis else sample_axis - 1
    k = 0
    for pi in set_partitions(modes):

        # Get the coefficient of the partition
        block_sizes = [len(block) for block in pi]
        coef = coef_tree.get_coef(block_sizes)
        if coef is None:
            coef = kstat_coef(n, block_sizes)
            coef_tree.set_coef(block_sizes, coef)

        # Compute the power sum product
        power_sum_product = 1
        for block in pi:
            data_slice = slice_left + (block,) + slice_right
            power_sum = np.sum(np.prod(data[data_slice], axis=variable_axis), axis=true_sample_axis)
            power_sum_product *= power_sum

        k += coef * power_sum_product

    return k


def kstat_coef(n, block_sizes):
    """
    Compute the coefficient for a product of power sums in the k-stat formula.

    Parameters
    ----------
    n : int
        Size of the sample.
    block_sizes : sequence of ints
        Sizes of each block in the partition.

    Returns
    -------
    c : float
        Coefficient in the k-stat formula.
    """

    # Iterate over the sum of the indices b1, b2, ..., b|pi|
    sum_over_sizes = 0
    lb, ub = len(block_sizes), sum(block_sizes)
    for s in range(lb, ub+1):

        # Iterate over indices that sum to s
        sum_over_simplex = 0
        for b in simplex_iter(s, block_sizes):

            # Compute product of stirling numbers and factorials for each block
            product_over_blocks = 1
            for k in range(len(block_sizes)):
                stir2_times_fac = b[k] ** block_sizes[k]
                for i_even in range(1, b[k], 2):
                    stir2_times_fac -= binom(b[k], i_even) * ((b[k] - i_even) ** block_sizes[k])
                for i_odd in range(2, b[k], 2):
                    stir2_times_fac += binom(b[k], i_odd) * ((b[k] - i_odd) ** block_sizes[k])

                product_over_blocks *= stir2_times_fac / b[k]

            sum_over_simplex += product_over_blocks

        sum_over_sizes += factorial(s-1) * sum_over_simplex / ff(n, s)

    if len(block_sizes) % 2 == 0:
        return -sum_over_sizes
    else:
        return sum_over_sizes
