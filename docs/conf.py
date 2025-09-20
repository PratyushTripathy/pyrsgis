from importlib.metadata import version as pkg_version, PackageNotFoundError
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC if SRC.exists() else ROOT))

project = "pyrsgis"
author = "Pratyush Tripathy"

try:
    release = pkg_version("pyrsgis")
except PackageNotFoundError:
    release = "0.0.0"
version = ".".join(release.split(".")[:2])

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "IPython.sphinxext.ipython_console_highlighting",
    "matplotlib.sphinxext.plot_directive",
    "numpydoc",
]

# Don't mock GDAL now; it's installed by conda
autodoc_mock_imports = [
    "sklearn", "sklearn.feature_extraction", "sklearn.ensemble",
    "skimage", "skimage.filters",
    "rasterio", "xarray",             # mock if not needed in docs
]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
html_theme = "pydata_sphinx_theme"
html_title = f"{project} v{release}"
