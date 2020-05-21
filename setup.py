from setuptools import find_packages, setup

from cloudipsp.configuration import __version__

desc = """
    Cloudipsp python sdk. 
    Docs   - https://docs.fondy.eu/
    README - https://github.com/cloudipsp/python-sdk/blob/master/README.md
  """

requires_list = [
    'requests',
    'six'
]

setup(
    name='cloudipsp',
    version=__version__,
    url='https://github.com/cloudipsp/python-sdk/',
    license='MIT',
    description='Python SDK for cloudipsp clients.',
    long_description=desc,
    author='Dmitriy Miroshnikov',
    packages=find_packages(where='.', exclude=('tests*',)),
    install_requires=requires_list,
    classifiers=[
        'Environment :: Web Environment',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ])
