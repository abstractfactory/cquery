from setuptools import setup, find_packages

f = open('README.md')
readme = f.read().strip()

f = open('LICENSE.md')
license = f.read().strip()

setup(
    name='cQuery',
    version='0.0.2',
    description='Decentralised content queries',
    long_description=readme,
    author='Marcus Ottosson',
    author_email='marcus@abstractfactory.com',
    url='https://github.com/abstractfactory/cquery',
    license=license,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
