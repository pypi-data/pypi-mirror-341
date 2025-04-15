import pathlib
from setuptools import setup, find_packages 
HERE = pathlib.Path(__file__).parent
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') 
LONG_DESC_TYPE = "text/markdown"
setup(
    name='HG22017UNO',
    version='0.2.3',
    author='Jose HErnandez',
    author_email='hg22017@ues.edu.sv',
    description='A library for solving linear and nonlinear systems of equations using various methods.',
    packages=find_packages(),
    install_requires=['numpy>=1.10 ','scipy>=1.0'],
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)