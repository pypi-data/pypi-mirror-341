from setuptools import setup, find_packages

setup(
    name='SE21003UNO',
    version='1.0.0',
    author='Ivan Everaldo Sanchez Escobar',
    author_email='se21003@ues.edu.sv',
    description='Librería creada para resolver sistemas de ecuaciones lineales y no lineales PARA LA MATERIA DE Cálculo Numérico para Desarrollo de Aplicaciones',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.21'
    ],
)
