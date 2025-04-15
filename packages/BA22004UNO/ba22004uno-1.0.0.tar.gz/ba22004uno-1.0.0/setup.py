from setuptools import setup, find_packages

setup(
    name='BA22004UNO',  # Cambiar por tu carnet real
    version='1.0.0',
    description='esta libreria es para resolver sistemas de ecuaciones lineales y no lineales con varios metodos numericos',
    author='Tu Nombre',
    author_email='alejandrobarillas1@gmail.com',
    packages=find_packages(),
    install_requires=['numpy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    python_requires='>=3.6',
)
