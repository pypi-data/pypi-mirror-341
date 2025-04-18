#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib

from setuptools import find_packages, setup


def get_requires():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        file_content = f.read()
        lines = [line.strip() for line in file_content.strip().split("\n") if not line.startswith("#")]
        return lines

def main():
    setup(
        name="cyze",
        version='0.1.0',
        author="Winter.Yu",
        author_email="winter741258@gmail.com",
        description="Cythonize Python Project",
        long_description=open("README.md", "r", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        keywords=[],
        license="Apache 2.0 License",
        url="",
        packages=find_packages("."),
        entry_points={
        'console_scripts': [
            'cyze = cyze.cyze:main'
        ]
    },
        python_requires=">=3.8.0",
        install_requires=get_requires(),
        # extras_require=extra_require,
        # classifiers=[
        #     # "Development Status :: 1 - Beta",
        #     "Intended Audience :: Developers",
        #     "Intended Audience :: Education",
        #     "Intended Audience :: Science/Research",
        #     "License :: OSI Approved :: Apache Software License",
        #     "Operating System :: OS Independent",
        #     "Programming Language :: Python :: 3",
        #     "Programming Language :: Python :: 3.8",
        #     "Programming Language :: Python :: 3.9",
        #     "Programming Language :: Python :: 3.10",
        #     "Programming Language :: Python :: 3.11",
        #     "Programming Language :: Python :: 3.12",
        #     "Programming Language :: Python :: 3.13",
        #     "Topic :: Scientific/Engineering :: Artificial Intelligence",
        # ],
    )


if __name__ == "__main__":
    main()
