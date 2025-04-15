from setuptools import setup, find_packages

setup(
    name='EM15008UNO',
    version='0.1.0',
    author='Héctor Echegoyen Montano',
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
