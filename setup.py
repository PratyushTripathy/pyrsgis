import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages=setuptools.find_packages()
#packages = packages + ['numpy', 'scikit-learn']

setuptools.setup(
    name="pyrsgis",
    version="0.4.1",
    author="Pratyush Tripathy",
    author_email="pratkrt@gmail.com",
    description="A Python package for remote sensing and GIS applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PratyushTripathy/pyrsgis",
    packages=packages,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
