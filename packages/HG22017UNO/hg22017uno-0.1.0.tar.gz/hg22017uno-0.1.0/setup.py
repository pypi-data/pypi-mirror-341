from setuptools import setup, find_packages

setup(
    name='HG22017UNO',
    version='0.1.0',
    author='Jose HErnandez',
    author_email='hg22017@ues.edu.sv',
    description='A library for solving linear and nonlinear systems of equations using various methods.',
    packages=find_packages(),
    install_requires=['numpy>=1.10'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)