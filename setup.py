#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = []

test_requirements = []

data = dict(
    author="Ed Singleton",
    author_email="ed.singleton@cabinetoffice.gov.uk",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Utils for i.AI",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="i_dot_ai_utils",
    name="i_dot_ai_utils",
    packages=find_packages(include=["i_dot_ai_utils", "i_dot_ai_utils.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/singletoned/i_dot_ai_utils",
    version="0.1.0",
    zip_safe=False,
)


if __name__ == "__main__":
    setup(**data)
