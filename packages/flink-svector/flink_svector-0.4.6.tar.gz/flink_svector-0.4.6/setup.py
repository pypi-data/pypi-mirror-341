import os

from setuptools import find_packages, setup

setup(
    name="flink-svector",
    version="0.4.6",
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
    author_email="team@svector.co.in",
    description="A distributed version control system for tracking changes in source code",
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type="text/markdown",
    url="https://github.com/siddharth-coder8/flink",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)