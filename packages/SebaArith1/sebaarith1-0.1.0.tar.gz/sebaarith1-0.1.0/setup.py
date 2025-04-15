from setuptools import setup, find_packages

setup(
    name='SebaArith1',
    version='0.1.0', 
    author='Antony Seba',
    author_email='sebaantony.phd201002@iiitkottayam.ac.in',
    description='A simple arithmetic package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
)
    