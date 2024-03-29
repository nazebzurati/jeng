from setuptools import find_packages, setup

with open("readme.md", "r") as doc:
    long_description = doc.read()

setup(
    name="jeng",
    version="1.0.0",
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
        "zeep>=4.2.1",
        "xmltodict>=0.13.0",
        "pandas>=2.0.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-dependency>=0.5.1",
            "pytest-env>=0.8.2",
            "black>=23.7.0",
            "isort>=5.12.0",
            "check-manifest>=0.49",
            "twine>=4.0.2",
            "coverage>=7.2.7",
        ],
    },
)
