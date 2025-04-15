from setuptools import setup, find_packages

setup(
    name='SF10020UNO',  # Nombre de mi librería
    version='0.1.7',  # Primera versión 
    author='Carlos Manuel Solís Flores',  # Nombre
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales',  # Breve descripción
    packages=find_packages(),
    install_requires=['numpy'],  # Dependencias si tuvieras
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
)
