import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrsgis",
    version="0.1.5",
    author="Pratyush Tripathy",
    author_email="pratkrt@gmail.com",
    description="Processing satellite data directly from TAR files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pratkrt/Python-for-Remote-Sensing-and-GIS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
