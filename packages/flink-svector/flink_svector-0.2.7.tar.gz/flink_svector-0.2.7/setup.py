import os

from setuptools import find_packages, setup

setup(
    name="flink-svector",
    version="0.2.7",
    packages=find_packages(),
    install_requires=[
        'firebase-admin',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'flink=flink.flink:main',
        ],
    },
    author="Siddharth Shah",
    author_email="your.email@example.com",
    description="A custom Git-like version control system",
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type="text/markdown",
    url="https://github.com/siddharthshah/flink",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)