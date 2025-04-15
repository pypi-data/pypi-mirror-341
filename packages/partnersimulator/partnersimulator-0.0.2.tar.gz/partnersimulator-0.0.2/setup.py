from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Partner Simulator'
with open('partnersimulator/ReadMe.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='partnersimulator',
    version=VERSION,
    author='Aditya Jain',
    author_email='aditya.jain22@imperial.ac.uk',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['openai', 'polars'],
    keywords=['creepy','parasocial'],
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows"
    ]
)