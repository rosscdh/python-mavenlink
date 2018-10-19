import os
from setuptools import setup, find_packages

REQUIREMENTS = [
    'click',
    'ruamel.yaml',
    'requests',
    'arrow',
    'marshmallow',
    #'requests-oauth2',
    'Jinja2'
]

BASE_PATH = os.path.dirname(__file__)

with open(os.path.join(BASE_PATH, 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

VERSION = os.getenv('RELEASE_VERSION', '0.0.1')

setup(
    name='mavenlink',
    version=VERSION,
    packages=find_packages(),  # include all packages under src
    #package_dir={'':'src'},   # tell distutils packages are under src
    package_data={
        # If any package contains *.txt files, include them:
        '': ['.mavenlink.yaml'],
        # And include any *.dat files found in the 'data' subdirectory
        # of the 'mypkg' package, also:
        # 'mypkg': ['data/*.dat'],
    },
    install_requires=REQUIREMENTS,
    license='MIT License',
    description='A cli client to consume data and prepare a timesheet for submission to Mavenlink',
    long_description=README,
    url='',
    author='Ross Crawford-d\'Heureuse',
    author_email='sendrossemail@gmail.com',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    entry_points={'console_scripts': [
        'mavenlink=mavenlink.cli:run',
    ], },
)
