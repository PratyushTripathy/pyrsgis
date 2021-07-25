# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os, sys
sys.path.insert(0, os.path.abspath('../'))
autodoc_mock_imports = ['mock', 'sphinx_bootstrap_theme']

import mock
import sphinx_bootstrap_theme

# -- Project information -----------------------------------------------------

project = 'pyrsgis'
copyright = '2021, Pratyush Tripathy'
author = 'Pratyush Tripathy'

# add version info
sys.path.insert(0, os.path.abspath("../.."))

import pyrsgis
version = pyrsgis.__version__

# -- General configuration ---------------------------------------------------
sys.path.insert(0, os.path.abspath('../..'))

MOCK_MODULES = [
    'numpy',
    'GDAL',
    'scikit-learn']

for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.Mock()
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme_options = {
    "github_url": "https://github.com/PratyushTripathy/pyrsgis"
    }
    

html_theme = "pydata_sphinx_theme"
#html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_title = "%s v%s Documentation" % ('pyrsgis', version)

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
htmlhelp_basename = 'pyrsgisdoc'
