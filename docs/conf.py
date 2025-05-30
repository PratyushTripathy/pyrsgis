# conf.py -- Sphinx configuration for pyrsgis documentation

import os
import sys
from unittest import mock

# -- Path setup --------------------------------------------------------------

# Add the project root to sys.path for autodoc to find your modules
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'pyrsgis'
copyright = '2025, Pratyush Tripathy'
author = 'Pratyush Tripathy'

# Extract version dynamically, fallback to parsing __init__.py
try:
    import pyrsgis
    version = pyrsgis.__version__
except Exception:
    version = "unknown"
    with open('../pyrsgis/__init__.py') as f:
        for line in f:
            if "__version__" in line:
                version = line.split("=")[1].strip().strip('"').strip("'")
                break

# -- General configuration ---------------------------------------------------

# Mock unavailable or heavy modules for autodoc and RTD
MOCK_MODULES = [
    "osgeo", "osgeo.gdal", "osgeo.ogr", "osgeo.osr",
    "sklearn", "sklearn.feature_extraction", "sklearn.ensemble",
    "skimage", "skimage.filters"
]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.MagicMock()

# Sphinx extensions for enhanced docs
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

# Generate .rst files for autosummary directives
autosummary_generate = True

# Paths for custom templates and files to exclude from the build
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- HTML output options -----------------------------------------------------

# Use the PyData Sphinx Theme for modern, responsive docs
html_theme = "pydata_sphinx_theme"
html_title = f"{project} v{version}"

html_theme_options = {
    "logo": {"text": "pyrsgis"},
    "show_nav_level": 2,          # Sidebar: expand 2 levels of toctree
    "navigation_depth": 4,        # Max depth of sidebar navigation
    "navbar_start": ["navbar-logo", "navbar-nav"],  # Left: logo + nav links
    "navbar_end": ["theme-switcher", "navbar-icon-links"],  # Right: theme switcher
    # More options: https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/configuration.html
}

# Optional: use a logo image instead of just text (put your logo in _static/)
# html_logo = "_static/pyrsgis_logo.png"

# -- Misc options ------------------------------------------------------------

# Help builder for HTML docs
htmlhelp_basename = 'pyrsgisdoc'

# Dummy linkcode (enable for code linking to GitHub if desired)
def linkcode_resolve(domain, info):
    return None

