from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='giter',
    packages=find_packages(),
    author='David Voigt',
    description='Command line application to quickly set up new repositories on Github and add it as origin to your local repo.',
    long_description=long_description,
    url='https://github.com/Xcal1bur/Giter',
    license='GNU General Public License v3.0',
    install_requires=['requests', 'bs4']
)