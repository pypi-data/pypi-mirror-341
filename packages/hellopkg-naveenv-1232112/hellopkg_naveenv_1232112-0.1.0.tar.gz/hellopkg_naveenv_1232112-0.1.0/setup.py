# setup.py
from setuptools import setup, find_packages

setup(
    name='hellopkg_naveenv_1232112',                # This will be your pip install name
    version='0.1.0',
    packages=find_packages(),
    description='A simple Hello World package',
    author='Naveenv',
    author_email='you@example.com',
    url='https://github.com/yourusername/hellopkg',  # Optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
