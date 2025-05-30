# Configuration file for the Sphinx documentation builder.

import os
import sys
from unittest import mock

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'pyrsgis'
copyright = '2025, Pratyush Tripathy'
author = 'Pratyush Tripathy'

try:
    import pyrsgis
    version = pyrsgis.__version__
except:
    with open('../pyrsgis/__init__.py') as f:
        for line in f:
            if "__version__" in line:
                version = line.split("=")[1].strip().strip('"').strip("'")
                break

# -- General configuration ---------------------------------------------------

# Mock heavy or unavailable modules
MOCK_MODULES = [
    "osgeo", "osgeo.gdal", "osgeo.ogr", "osgeo.osr",
    "sklearn", "sklearn.feature_extraction", "sklearn.ensemble",
    "skimage", "skimage.filters"
]

for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.MagicMock()


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

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- HTML output -------------------------------------------------------------

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
import sphinx_bootstrap_theme
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_title = f"{project} v{version}"
htmlhelp_basename = 'pyrsgisdoc'

autosummary_generate = True

def linkcode_resolve(domain, info):
    return None
