from setuptools import setup, find_packages
import os
import re

# Read version from version.py
with open(os.path.join('hivecraft', 'version.py'), 'r') as f:
    version_file = f.read()
    version_match = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name='hivecraft',
    version=version,
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    tests_require=[
        'pytest>=6.0.0',
        'pytest-cov>=2.10.0',
    ],
    entry_points={
        'console_scripts': [
            'hivecraft=hivecraft.__main__:main',
        ],
    },
    author='Éric PHILIPPE',
    author_email='ericphlpp@proton.me',
    description='Hivecraft is a tool to create, test and compile a folder with .alghive extension.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Eric-Philippe/AlgoHive',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)