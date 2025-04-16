from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='minha_lib_aula02-package',
    version='1.0.0',
    packages=find_packages(),
    description='Execercio para criar uma biblioteca',
    author='Wellington (RM364772)',
    author_email='wellington@nuvsolutions.com.br',
    url='https://github.com/nuvsolutions/minha_lib_aula02',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
