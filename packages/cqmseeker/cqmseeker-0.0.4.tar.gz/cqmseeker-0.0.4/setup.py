#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages, Extension

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Meinolf Sellmann",
    author_email='info@insideopt.com',
    python_requires='>=3.11.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Microsoft :: Windows'
    ],
    description="InsideOpt Seeker Windows Python 311 Distribution",
    install_requires=requirements,
    long_description=readme, 
    keywords='insideopt, seeker, optimization',
    name='cqmseeker',
    test_suite='tests',
    version='0.0.4',
    packages=find_packages(include=['cqmseeker', 'cqmseeker.*', '*.so', '*.pyd']),
    package_data={'cqmseeker': ['*.so', '*.pyd', 'cqmseeker.py', 'bin/*', 'scripts/*']},
    zip_safe=False,
)
