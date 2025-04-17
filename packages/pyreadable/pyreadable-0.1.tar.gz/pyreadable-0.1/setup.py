from setuptools import setup, find_packages

setup(
    name='pyreadable',
    version='0.1',
    author='Archit Anant',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown', 
    install_requires=[
        "pymupdf>=1.25.5",
        "PyPDF2>=3.0.1"
        ]
)