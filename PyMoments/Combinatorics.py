"""
Combinatorics.py
Module of combinatorics-related generators and methods.
"""


def simplex_iter(s, max_vals):
    """
    Generator over all tuples of integers (i1, i2, ..., id) with the following properties:
        * i1 + i2 + ... + id = s
        * i1, i2, ..., id >= 1
        * ij <= max_vals[j]

    Parameters
    ----------
    s : int
        Sum to which the indices are constrained.
    max_vals : sequence of positive ints
        Maximum value that each mode of the index can take on.

    Yields
    ------
    idx : tuple of ints
        Index tuple satisfying the three properties above.
    """
    if s <= 0:
        return
    elif len(max_vals) == 0:
        return
    elif len(max_vals) == 1:
        if max_vals[0] >= s:
            yield (s,)
        else:
            return
    else:
        for i in range(1, 1 + min(max_vals[0], s)):
            for indices in simplex_iter(s - i, max_vals[1:]):
                yield (i,) + indices


def set_partitions(set):
    """
    Generator over all partitions of the given set.

    Parameters
    ----------
    set : sequence of objects
        Set to partition. Note that repeated elements are treated as distinct.

    Yields
    ------
    pi : list of tuples of elements from set
        Partition of the set.
    """
    if len(set) == 0:
        return
    elif len(set) == 1:
        yield [(set[0],)]
    else:
        head = set[0]
        for tail_parts in set_partitions(set[1:]):
            for i, part in enumerate(tail_parts):
                new_part = (head,) + part
                yield tail_parts[:i] + [new_part] + tail_parts[i + 1:]
            yield [(head,)] + tail_parts


def ff(n, i):
    """
    Returns the falling factorial (n)_i.

    Parameters
    ----------
    n : int
        Argument to the falling factorial.
    i : int
        Number of terms to include.

    Returns
    -------
    ff : int
        Falling factorial (n)_i.

    Notes
    -----
    The falling factorial is computes the product n(n-1)...(n-1+1).
    For example, (4)_2 = 4(3) = 12.
    """
    if i <= 0:
        return 1
    elif i == 1:
        return n
    else:
        return n * ff(n-1, i-1)


def factorial(n):
    """
    Computes the factorial n!

    Parameters
    ----------
    n : int
        Argument to the factorial.

    Returns
    -------
    f : int
        Factorial n!
    """
    return ff(n, n-1)


def binom(n, k):
    """
    Computes the binomial coefficient n choose k.
    I.e., computs the number of ways to choose k-element subsets from a collection with n elements.

    Parameters
    ----------
    n : int
        Number of elements in the collection.
    k : int
        Size of subsets of the collection to choose.

    Returns
    -------
    b : int
        Binomial coefficient n choose k.

    Notes
    -----
    The binomial coefficient is given by n! / k! (n-k)!
    Thus, the computation is simplified using falling factorials:
        (n, k) = n! / k! (n-k)! = (n)_k / (k)_(k-1)
    """
    return ff(n, k) // ff(k, k-1)
