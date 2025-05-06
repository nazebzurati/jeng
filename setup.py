from setuptools import find_packages, setup

with open("readme.md", "r") as doc:
    long_description = doc.read()

setup(
    name="jeng",
    version="1.0.1",
    license="MIT",
    description="A simple WITSML client with utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nazeb Zurati",
    author_email="nazeb04@gmail.com",
    url="https://github.com/nazebzurati/jeng",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    py_modules=[
        "jeng",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "python",
        "witsml",
        "soap-client",
        "pandas",
    ],
    install_requires=[
        "zeep>=4.3.1",
        "xmltodict>=0.14.0",
        "pandas>=2.2.3",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.5",
            "pytest-dependency>=0.6.0",
            "pytest-env>=1.1.5",
            "black>=25.1.0",
            "isort>=6.0.1",
            "check-manifest>=0.50",
            "twine>=6.1.0",
            "coverage>=7.8.0",
        ],
    },
)
