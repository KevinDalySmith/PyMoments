# PyMoments

PyMoments is a toolkit for unbiased estimation of multivariate statistical moments. 
In the current version (1.0.0), only multivariate <i>k</i>-statistics are implemented,
allowing for the unbiased estimation of cumulants. 
An implementation of <i>h</i>-statistics (for unbiased estimation of central moments) is 
planned for a future release.

## Installation

PyMoments can be installed either from the GitHub 
[source](https://github.com/KevinDalySmith/PyMoments), or via PyPI. 
To install the package from GitHub, first clone the repository:
```
$ git clone https://github.com/KevinDalySmith/PyMoments.git
```
Navigate to the root directory, which contains the ```setup.py``` file.
You can then use setuptools to install the package and run the unit tests:
```
$ python setup.py install
$ python setup.py test
```
Alternatively, PyMoments can be installed using PyPI:
```
$ pip install PyMoments
```
Note that PyMoments requires [NumPy](https://numpy.org/). 
I have only tested the package with NumPy version 1.16.5, but it should be compatible
with older versions.

## Basic Usage

The simplest use case is to compute a multivariate <i>k</i>-statistic from a 2D array of data. 
For example, generate a random sample from a multivariate normal distribution:
```python
import numpy as np
mu = np.zeros(3,)
sigma = np.array([
    [2, 0, 1],
    [0, 2, -1],
    [1, -1, 2]
])
data = np.random.multivariate_normal(mu, sigma, size=(1000,))
```
The ```data``` variable is a 1000 x 3 array, where each column corresponds to one of the three
random variables in the joint distribution, and each row is an observation.

The first <i>k</i>-statistic is identical to the sample mean. Thus, we can compare the first-order
<i>k</i>-statistics for each column of the array, to the simple average:
```python
from PyMoments import kstat

first_order_kstats = [
    kstat(data, (0,)),
    kstat(data, (1,)),
    kstat(data, (2,))
]

sample_means = np.mean(data, axis=0)

print('First-order k-statistics:', first_order_kstats)
print('Sample means:', sample_means) 
```
The method ```kstat(data, (0,))``` computes the first-order <i>k</i>-statistic, from the first column
of the data. As the console output of this example reveals, the first-order <i>k</i>-statistics are
indeed equivalent to the sample means, up to floating point error.

Second-order <i>k</i>-statistics are identical to covariances. Therefore, we can compare the values
of the ```kstat()``` function to the covariance matrix of the data:
```python
second_order_kstats = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        second_order_kstats[i, j] = kstat(data, (i, j))

print('Second-order k-statistics:')
print(second_order_kstats)
print('Covariance matrix:')
print(np.cov(data.T))
```

Higher-order <i>k</i>-statistics become difficult to express in terms of familiar statistics, but
they still provide insight into the underlying distribution.
Third-order <i>k</i>-statistics, for example, are related to the skewness of a distribution. 
Normal distributions have zero skew, and therefore, all third-order <i>k</i>-statistics 
should be fairly close to zero:
```python 
print('Sample third-order k-statistics:') 
print(kstat(data, (0, 1, 2)))
print(kstat(data, (0, 0, 1)))
print(kstat(data, (2, 2, 2)))
```

The second argument to the ```kstat()``` method specifies a multiset of column indices
(as a sequence of integers), which encodes the particular <i>k</i>-statistic to be computed. 
The order of the <i>k</i>-statistic is equal to the length of this multiset.
Note that ```kstat()``` is symmetric with respect to this argument, i.e., permuting the 
indices will have no affect on the output. Repeated indices are allowed; in fact, repeated 
indices are required to compute classical univariate <i>k</i>-statistics:
```python
new_data = np.random.randn(1000, 1)

print('First univariate k-stat:')
print(kstat(new_data, (0,)))

print('Second univariate k-stat:')
print(kstat(new_data, (0, 0)))

print('Third univariate k-stat:')
print(kstat(new_data, (0, 0, 0)))

print('Fourth univariate k-stat:')
print(kstat(new_data, (0, 0, 0, 0)))
```

It should also be pointed out that <i>k</i>-statistics become noisy and difficult to compute with
increasing order. For example, try evaluating a 9th-order univariate cumulant on a new sample
several times:
```python 
kstat(np.random.randn(1000, 1), (0,) * 9)
```
Not only does the function take several seconds to return, but repeats of this experiment can
lead to widely different values of the <i>k</i>-statistic, despite the fact that normal 
distributions have ninth-order cumulants of zero. 
The runtime of ```kstat()``` on <i>n</i>th-order indices scales with Bell's number B(n), so... 
I do not recommend trying <i>k</i>-statistics of order 10 or higher.

## License, Citation, and Acknowledgements
PyMoments by Kevin D. Smith is licensed under a non-commercial Creative Commons license 
([CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)). When possible, please cite
this package:
```
@misc{PyMoments:2020,
  author = {Kevin D. Smith},
  title = {PyMoments: A Python toolkit for unbiased estimation of multivariate statistical moments},
  howpublished = {\texttt{https://github.com/KevinDalySmith/PyMoments}},
  year = 2020 
}
```
This work was supported in part by the U.S. Defense Threat Reduction Agency, under grant HDTRA1-19-1-0017.
