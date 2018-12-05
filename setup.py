import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrsgis",
    version="0.0.3",
    author="Pratyush Tripathy",
    author_email="pratkrt@gmail.com",
    description="Boosting up satellite data processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pratkrt/Python-for-Remote-Sensing-and-GIS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
