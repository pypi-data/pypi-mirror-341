
from setuptools import setup, find_packages

setup(
    name='UM22006UNO',
    version='0.1',
    packages=find_packages(),
    install_requires=['numpy', 'scipy'],
    author='UM22006',
    author_email='um22006@example.com',
    description='Librería para resolver ecuaciones lineales y no lineales',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/UM22006/UM22006UNO',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
