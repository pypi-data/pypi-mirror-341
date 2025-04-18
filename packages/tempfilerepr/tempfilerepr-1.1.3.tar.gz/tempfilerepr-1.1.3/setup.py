import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tempfilerepr',
    version='1.1.3',
    author='Nasr',
    author_email='nasr2python@gmail.com',
    description='Encoder and decoder for the temp encoding.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://t.me/NasrPy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
