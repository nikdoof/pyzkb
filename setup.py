#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'requests==2.3.0',
]

test_requirements = []

setup(
    name='pyzkb',
    version='0.1a',
    description='Python module for accessing the ZKillboard API',
    long_description=readme + '\n\n' + history,
    author='Andrew Williams',
    author_email='andy@tensixtyone.com',
    url='https://github.com/nikdoof/pyzkb',
    packages=[
        'pyzkb',
    ],
    package_dir={'pyzkb':
                 'pyzkb'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='pyzkb',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)