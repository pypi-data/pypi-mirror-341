from setuptools import find_packages, setup
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'DESCRIPTION.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='newsbinpro_client',
    version='1.0.3',
    description='A client for the Newsbin Pro Usenet Downloader',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jonny Bergdahl',
    author_email='github@bergdahl.it',
    url='https://github.com/jonnybergdahl/Python-NewsbinPro-Client',
    license='MIT',
    packages=find_packages(include=["newsbinpro_client"], where='src'),
    package_dir={"": "src"},
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Home Automation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ]
)