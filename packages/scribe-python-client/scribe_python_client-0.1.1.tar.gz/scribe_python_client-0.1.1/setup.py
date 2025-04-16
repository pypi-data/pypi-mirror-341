from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='scribe-python-client',
    version='0.1.1',
    packages=find_packages(include=['scribe_python_client', 'scribe_python_client.*']),
    install_requires=[
        'requests',
        'PyJWT'
    ],
    entry_points={
        'console_scripts': [
            'scribe-client=scribe_python_client.cli:main',
        ],
    },
    description='A Python client for interacting with ScribeHub.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Daniel Nebenzahl',
    author_email='dn@scribesecurity.com',
    url='https://github.com/scribe-security/scribe-python-client',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)