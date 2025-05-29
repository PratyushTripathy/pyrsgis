
# -*- coding: utf-8 -*-
"""
Tests for pyrsgis package
"""
import numpy as np

''' Tests for pyrsgis.raster

Naming rules:
1. class: Test{filename}{Class}{method} with appropriate camel case
2. function: test_{method}_t{test_id}
Notes on how to test:
0. Make sure [pytest](https://docs.pytest.org) has been installed: `pip install pytest`
1. execute `pytest {directory_path}` in terminal to perform all tests in all testing files inside the specified directory
2. execute `pytest {file_path}` in terminal to perform all tests in the specified file
3. execute `pytest {file_path}::{TestClass}::{test_method}` in terminal to perform a specific test class/method inside the specified file
4. after `pip install pytest-xdist`, one may execute "pytest -n 4" to test in parallel with number of workers specified by `-n`
5. for more details, see https://docs.pytest.org/en/stable/usage.html
'''

#import pytest
import os
from pyrsgis import raster
import numpy as np
import pytest

# define all the file paths to run the test on
DATA_DIR = 'data/'
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
MULTIBAND_FILEPATH = f'{DATA_DIR}/raster_multiband.tif'
SINGLEBAND_DISCRETE_FILEPATH = f'{DATA_DIR}/raster_singleband_discrete.tif'
SINGLEBAND_CONTINUOUS_FILEPATH = f'{DATA_DIR}/raster_singleband_continuous.tif'

class TestPyrsgisRaster:
    ''' Test for raster.read instantiation '''

    def test_init_t0(self):
        ds_singleband_continuous, arr_singleband_continuous = raster.read(SINGLEBAND_CONTINUOUS_FILEPATH)
        ds_singleband_discrete, arr_singleband_discrete = raster.read(SINGLEBAND_DISCRETE_FILEPATH)
        ds_multiband, arr_multiband = raster.read(MULTIBAND_FILEPATH)

        for ds in [ds_singleband_continuous, ds_singleband_discrete, ds_multiband]:
            assert type(ds.GeoTransform) == type(tuple())
            assert type(ds.Projection) == type(str())
            assert type(ds.RasterCount) == type(int())
            assert type(ds.RasterXSize) == type(int())
            assert type(ds.RasterYSize) == type(int())

        print('pyrsgis.raster tests ran successfully!')


    @pytest.mark.xfail
    def test_init_t1(self):
        ds_singleband_continuous, arr_singleband_continuous = raster.read(SINGLEBAND_CONTINUOUS_FILEPATH)
        assert type(arr_singleband_continuous) == type(np.array())

# call the modules in the class and run the tests
TestPyrsgisRaster().test_init_t0()