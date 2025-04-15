from setuptools import setup, find_packages

setup(
    name='JM21008UNO',
    version='0.1.0',
    author='jeffrey juárez',
    author_email='jm21008@ues.edu.sv',
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jeffreyMangandi/JM21008UNO',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
        install_requires=[
        "numpy>=1.21.0",  # Dependencias necesarias
    ],
)