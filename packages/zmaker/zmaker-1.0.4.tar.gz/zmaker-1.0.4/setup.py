from setuptools import setup, find_packages

setup(
    name='zmaker',
    version='1.0.4',
    description='Custom directory packer and filter',
    author='nopdoor',
    author_email='opn148199@gmail.com',
    packages=find_packages(),
    install_requires=[
        'reqinstall',
        'zsender'
    ],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
