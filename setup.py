from setuptools import setup, find_packages

setup(
    name='ncsdaemon',
    version='0.1',
    url='http://github.com/nathanjordan/jsoncanon',
    license='MIT',
    author='Nathan Jordan',
    author_email='natedagreat27274@gmail.com',
    description="""A Python library that creates a canonicalized version of a
                   JSON document for hashing and cryptography""",
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read(),
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
)
