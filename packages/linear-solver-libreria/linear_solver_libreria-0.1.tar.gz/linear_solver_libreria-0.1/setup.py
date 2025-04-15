from setuptools import setup, find_packages

setup(
    name='linear-solver-libreria', 
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='cs23022 william ernesto cerna salazar ',
    author_email='cs23022@ues.edu.sv',
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/williamcerna/desktop-tutorial',  # opcional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)