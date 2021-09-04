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
autodoc_mock_imports = ['mock', 'sphinx_bootstrap_theme']

import mock
import sphinx_bootstrap_theme

sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------
project = 'pyrsgis'
copyright = '2021, Pratyush Tripathy'
author = 'Pratyush Tripathy'

# The full version, including alpha/beta/rc tags
try:
    import pyrsgis
    version = pyrsgis.__version__
except:
    with open('../pyrsgis/__init__.py') as f:
        for line in f:
            if line.find("__version__") >= 0:
                version = line.split("=")[1].strip()
                version = version.strip('"').strip("'")
                continue


# -- General configuration ---------------------------------------------------
#sys.path.insert(0, os.path.abspath('../'))

MOCK_MODULES = [
    'numpy',
    'gdal',
    'scikit-learn',
    'scikit-image',
    'pandas']

for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.Mock()
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "IPython.sphinxext.ipython_console_highlighting",
    "matplotlib.sphinxext.plot_directive",
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.viewcode"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme_options = {
    'navbar_title': "pyrsgis",
    'navbar_sidebarrel': False,
    'navbar_class': "navbar navbar-inverse",
    'navbar_fixed_top': "true",
    'source_link_position': 'footer',
    'bootstrap_version': "3",
    'navbar_links': [
        ("Installation", "installation"),
        ("API", "api")]
    }
    

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_title = "%s v%s Documentation" % ('pyrsgis', version)

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']
htmlhelp_basename = 'pyrsgisdoc'

# add this dummy function
def linkcode_resolve(domain, info):
    return None

