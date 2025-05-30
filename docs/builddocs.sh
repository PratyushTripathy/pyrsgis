#!/bin/bash
make apidoc
rm -f generated/pyrsgis.rst generated/pyrsgis.raster.rst generated/pyrsgis.convert.rst generated/pyrsgis.ml.rst generated/pyrsgis.utils.rst
make html
