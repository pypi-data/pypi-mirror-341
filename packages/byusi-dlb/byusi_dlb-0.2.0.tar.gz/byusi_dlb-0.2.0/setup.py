# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="byusi-dlb",
    version="0.2.0",
    author="ByUsi",
    description="Multi-threaded downloader with Rich progress bars",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://gitee.com/byusi/dlb",
    packages=find_packages(),
    install_requires=[
        "rich>=10.0.0",
        "requests>=2.25.1",
        "python-dotenv>=0.19.0"
    ],
    entry_points={
        'console_scripts': [
            'dlb=dlb.cli:main'
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)