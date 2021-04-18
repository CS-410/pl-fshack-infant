import sys 
from os import path
from setuptools import setup

# Make sure we are running Python 3.5+
if 10 * sys.version_info[0] + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'fshack_infant',
    version          = '1.0',
    description      = 'An app to ...',
    long_description = readme,
    author           = 'FNNDSC',
    author_email     = 'dev@babyMRI.org',
    url              = 'http://wiki',
    packages         = ['fshack_infant'],
    install_requires = ['chrisapp', 'pudb'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
                'fshack_infant = fshack_infant.__main__:main'
            ]
        }
)
