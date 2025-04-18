from setuptools import setup, find_packages

setup(
    name='amazing_filters',
    version='1.1',
    description='A package for embedding and applying easy image filters',
    author='Rodrigo Ginde',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
    python_requires='>=3.7',
)
