import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrsgis",
    version="0.3.8",
    author="Pratyush Tripathy",
    author_email="pratkrt@gmail.com",
    description="A package to read, process and export GeoTIFFs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pratkrt/Python-for-Remote-Sensing-and-GIS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS"
    ],
)
