from setuptools import setup, find_packages


VERSION = '0.0.3'
DESCRIPTION = 'Youtube Autonomous Mongo database module'
LONG_DESCRIPTION = 'Youtube Autonomous Mongo database module to interact with a mongo database easy.'

setup(
    name = "yta_mongo", 
    version = VERSION,
    author = "Daniel Alcalá",
    author_email = "<danielalcalavalera@gmail.com>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [
        'yta_general_utils',
        'pymongo'
    ],
    
    keywords = [
        'youtube autonomous mongo database module',
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)