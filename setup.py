
from setuptools import setup

setup(
    name='PyMoments',
    version='1.0.0',
    description='Unbiased estimators for multivariate statistical moments',
    url='https://github.com/KevinDalySmith/PyMoments',
    author='Kevin D. Smith',
    author_email='kevinsmith@ucsb.edu',
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    keywords='statistics',
    packages=['PyMoments', 'tests'],
    package_data={'tests': ['data/*.csv']},
    install_requires=['numpy'],
    test_suite='tests'
)
