import os
from setuptools import setup, find_packages


def get_requirements():
    packages = []

    with open("requirements.txt") as fd:
        for line in fd.readlines():
            if not line or line.startswith('-i'):
                continue
            packages.append(line.split(';', 1)[0])

    return packages


def get_version():
    with open(os.path.join('nefertem', '__init__.py')) as f:
        content = f.readlines()

    for line in content:
        if line.startswith('__version__ ='):
            # dirty, remove trailing and leading chars
            return line.split(' = ')[1][1:-2]
    raise ValueError("No version identifier found")


setup(
    name='kebechet',
    entry_points={
        'console_scripts': ['nefertem=nefertem.cli:cli']
    },
    version=get_version(),
    description='Check a Python codebase for issues and not so beautiful code',
    long_description='Check a Python codebase for issues and not so beautiful code',
    author='Fridolin Pokorny',
    author_email='fridolin@redhat.com',
    license='GPLv3+',
    packages=find_packages(),
    install_requires=get_requirements()
)
