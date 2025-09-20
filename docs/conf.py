# conf.py -- Sphinx configuration for pyrsgis documentation

from __future__ import annotations
import os
import sys
from pathlib import Path
from importlib.metadata import version as pkg_version, PackageNotFoundError

# -- Path setup --------------------------------------------------------------
# Add the project root to sys.path so autodoc finds your modules
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC if SRC.exists() else ROOT))

# -- Project information -----------------------------------------------------
project = "pyrsgis"
author = "Pratyush Tripathy"
copyright = "2025, Pratyush Tripathy"

# Don't import pyrsgis here (it may import heavy deps).
# Ask the installed package for its version instead:
try:
    release = pkg_version("pyrsgis")   # full version, e.g. 0.4.2b1
except PackageNotFoundError:
    release = "0.0.0"
version = ".".join(release.split(".")[:2])  # short X.Y

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",                                    # Markdown support
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",                            # NumPy/Google docstrings
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "IPython.sphinxext.ipython_console_highlighting", # needs ipython
    "matplotlib.sphinxext.plot_directive",            # needs matplotlib
    "numpydoc",
]

# Let Sphinx generate autosummary pages automatically
autosummary_generate = True
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# Mock heavy/optional deps so autodoc can import your modules on RTD
autodoc_mock_imports = [
    "osgeo", "osgeo.gdal", "osgeo.ogr", "osgeo.osr",
    "rasterio", "gdal", "xarray",
    "sklearn", "sklearn.feature_extraction", "sklearn.ensemble",
    "skimage", "skimage.filters",
    # add others here if needed
]

# Intersphinx (set tuple 2 to None so Sphinx fetches objects.inv)
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- HTML output -------------------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_title = f"{project} v{release}"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme_options = {
    "logo": {"text": "pyrsgis"},
    "show_nav_level": 2,
    "navigation_depth": 4,
    "navbar_start": ["navbar-logo", "navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
}

# Optional: logo in docs/_static/
# html_logo = "_static/pyrsgis_logo.png"

# If you want linkcode later, wire this up to your GitHub repo.
def linkcode_resolve(domain, info):
    return None
