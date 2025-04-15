from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Partner Simulator'
LONG_DESCRIPTION = 'A very basic chatbot based on openAI to console lonely engineering students... not me though, my girlfriend is wonderful :)'

setup(
    name='partnersimulator',
    version=VERSION,
    author='Aditya Jain',
    author_email='aditya.jain22@imperial.ac.uk',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
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