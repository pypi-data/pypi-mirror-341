from setuptools import setup, find_packages

setup(
    name='pylearn-flask-api-utils',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask_jwt_extended',
    ],
    author='Clement Dada',
    author_email='dadaauthourity23@gmail.com',
    description='Shared utilities for Pylearn Flask API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/auth-inv-hub/pylearn-library-flask-api-utils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
