.. Install

Installation
============

Recommended: Conda/Mamba Installation
-------------------------------------

The easiest way to get started with `pyrsgis` is to use the provided `environment.yml` file, which sets up a compatible environment with all necessary dependencies.
This method works with both `conda` and `mamba`:

.. code-block:: bash

    # Using mamba (recommended for speed)
    mamba env create -f environment.yml

    # Or with conda
    conda env create -f environment.yml

Then activate the environment:

.. code-block:: bash

    mamba activate pyrsgis
    # or
    conda activate pyrsgis

This ensures all required libraries are installed in versions known to work with `pyrsgis`.

Alternative: Installation with requirements.txt
-----------------------------------------------

You can also use the `requirements.txt` file to install dependencies in your existing Python environment:

.. code-block:: bash

    pip install -r requirements.txt

PyPI Installation (pip)
-----------------------

`pyrsgis` is available on the `Python Package Index`_.
To install the latest **stable** version with pip:

.. code-block:: bash

    pip install pyrsgis

To install a specific version, specify it explicitly (see `release history`_ for available versions):

.. code-block:: bash

    pip install pyrsgis==0.4.2b1

**Note:** The latest stable and pre-release versions may differ.

Pre-release Installation (Beta Version)
---------------------------------------

The current beta release is **0.4.2b1**.
To install this pre-release version from PyPI, use:

.. code-block:: bash

    pip install --pre pyrsgis

The `--pre` flag allows pip to install pre-release (beta, alpha, or release candidate) versions.

Conda/Anaconda Installation
---------------------------

`pyrsgis` is also available on Anaconda Cloud (community channel):

.. code-block:: bash

    conda install -c pratyusht pyrsgis

**Note:** The conda version may lag behind PyPI. The recommended installation is via the provided `environment.yml` if you use conda or mamba.

Supported Python Versions
-------------------------

`pyrsgis` supports Python **3.7 and above**.
Older versions (3.5–3.8) are still supported in legacy releases, but for best results, use a modern Python 3 environment.

Contributing to pyrsgis
-----------------------

`pyrsgis` is an open-source, non-profit project—contributions are welcome!
To contribute:

1. Fork the `GitHub repo`_.
2. Clone your fork locally.
3. Create a new branch and make your changes.
4. Open a pull request for review.

Suggestions, issues, and feature requests are also appreciated.

.. _Python Package Index: https://pypi.org/project/pyrsgis/
.. _release history: https://pypi.org/project/pyrsgis/#history
.. _Anaconda: https://anaconda.org/pratyusht/pyrsgis
.. _GitHub repo: https://github.com/PratyushTripathy/pyrsgis
