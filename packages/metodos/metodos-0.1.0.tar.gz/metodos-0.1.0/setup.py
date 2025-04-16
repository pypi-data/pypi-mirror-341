from setuptools import setup, find_packages

setup(
    name='metodos',
    version='0.1.0',
    description='Solución de sistemas de ecuaciones por métodos numéricos',
    author='PC12028',
    packages=find_packages(),
    install_requires=['numpy'],
    python_requires='>=3.6',
)
