from setuptools import setup, find_packages

import os
import imp

version_file = os.path.abspath('cquery/version.py')
version_mod = imp.load_source('version', version_file)
version = version_mod.version

setup(
    name='cQuery',
    version=version,
    description='Decentralised content queries',
    long_description=open('README.txt').read(),
    author='Marcus Ottosson',
    author_email='marcus@abstractfactory.com',
    url='https://github.com/abstractfactory/cquery',
    license="license.txt",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['cquery = cquery.__main__:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)
