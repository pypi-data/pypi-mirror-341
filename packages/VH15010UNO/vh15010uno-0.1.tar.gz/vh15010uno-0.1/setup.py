from setuptools import setup, find_packages

setup(
    name='VH15010UNO',
    version='0.1',
    packages=find_packages(),
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales',
    author='Ricardo Alfredo Valencia Hernández',
    author_email='vh15010@ues.edu.sv',
    license='MIT',
    install_requires=['numpy'],
)
