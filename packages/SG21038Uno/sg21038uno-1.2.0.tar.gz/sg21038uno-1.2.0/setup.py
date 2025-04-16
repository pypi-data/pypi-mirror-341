from setuptools import setup, find_packages

setup(
    name='SG21038Uno',
    version='1.2.0',
    description='Libreria  para resolver ecuaciones lineales y no lineales',
    author='Katherine Gámez',
    author_email='sg21038@ues.edu.sv',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
    python_requires='>=3.6',
)
