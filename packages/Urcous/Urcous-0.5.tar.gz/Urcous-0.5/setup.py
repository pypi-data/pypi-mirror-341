from setuptools import setup, find_packages
import codecs

setup(
    name="Urcous",
    version="0.05",
    description="Urcous 2D and 3D engine library for python 2.4",
    author="Vladik",
    author_email="vladhruzd25@gmail.com",
    url="",
    packages=find_packages(),
    classifiers = [
        'Programming Language :: Python :: 2.4',
        'Topic :: Multimedia :: Graphics',
        'License :: OSI Approved :: MIT License'
    ],
    long_description=codecs.open('README.txt', 'r', 'utf-8').read(),
    long_description_content_type='text/plain',
    license="MIT"
)