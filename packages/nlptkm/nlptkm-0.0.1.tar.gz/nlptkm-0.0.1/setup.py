from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'NLP Packing Help '

# Setting up
setup(
    name="nlptkm",
    version=VERSION,
    author="NeuralNine (Florian Dedov)",
    author_email="jack2018@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",

    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

