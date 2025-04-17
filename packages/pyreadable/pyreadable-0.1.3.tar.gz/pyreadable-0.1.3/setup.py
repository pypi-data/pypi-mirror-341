from setuptools import setup, find_packages

setup(
    name='pyreadable',
    version='0.1.3',
    author='Archit Anant',
    description='Check PDFs for Machine Readability',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown', 
    python_requires='>=3.7',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',
    ],
    install_requires=[
        "pymupdf>=1.25.5",
        "PyPDF2>=3.0.1"
        ]
)