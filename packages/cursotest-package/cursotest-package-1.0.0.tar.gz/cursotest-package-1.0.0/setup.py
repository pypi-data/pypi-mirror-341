from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cursotest-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib CursoTest',
    author='Igor Januario',
    author_email='igorjanuariod@gmail.com',
    url='https://github.com/igorjanuario/CursoTest',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
