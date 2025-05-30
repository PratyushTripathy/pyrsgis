.. _api_ref:

pyrsgis API reference
======================

Reading and exporting GeoTIFFs
------------------------------

.. autosummary::
   :toctree: generated/

    pyrsgis.raster.read
    pyrsgis.raster.export

Clipping a raster
-----------------

.. autosummary::
   :toctree: generated/

    pyrsgis.raster.clip
    pyrsgis.raster.clip_file
    pyrsgis.raster.trim
    pyrsgis.raster.trim_array
    pyrsgis.raster.trim_file

Shifting a raster
-----------------

.. autosummary::
   :toctree: generated/

    pyrsgis.raster.shift
    pyrsgis.raster.shift_file

Reshaping GeoTIFF array for statistical analysis
------------------------------------------------

.. autosummary::
   :toctree: generated/

    pyrsgis.convert.array_to_table
    pyrsgis.convert.table_to_array
    pyrsgis.convert.raster_to_csv
    pyrsgis.convert.csv_to_raster

Creating image chips for deep learning
--------------------------------------

.. autosummary::
   :toctree: generated/

    pyrsgis.ml.array_to_chips
    pyrsgis.ml.array2d_to_chips
    pyrsgis.ml.raster_to_chips

Generating northing and easting raster
--------------------------------------

.. autosummary::
   :toctree: generated/

    pyrsgis.raster.north_east
    pyrsgis.raster.north_east_coordinates
    pyrsgis.raster.northing
    pyrsgis.raster.easting
