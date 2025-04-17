from setuptools import setup, find_packages

setup(
    name='pyreadable',
    version='0.1.2',
    author='Archit Anant',
    description='Convert DOCX to PDF and analyze text layout in PDFs.',
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