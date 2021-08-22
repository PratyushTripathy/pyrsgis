#pyrsgis/raster

import os
import numpy as np
from .. import doc_address
from copy import deepcopy

# add exception for deprecated version of gdal
try:
    import gdal
except:
    from osgeo import gdal

class _create_ds():

    def __init__(self, ds):
        self.Projection = ds.GetProjection()
        self.GeoTransform = ds.GetGeoTransform()
        self.RasterCount = ds.RasterCount
        self.RasterXSize = ds.RasterXSize
        self.RasterYSize = ds.RasterYSize
        self.DataType = ds.GetRasterBand(1).DataType
        self.update_bbox()

    def GetProjection(self):
        return(self.Projection)

    def GetGeoTransform(self):
        return(self.GeoTransform)

    def RasterCount(self):
        return(self.RasterCount)

    def RasterXSize(self):
        return(self.RasterXSize)

    def RasterYSize(self):
        return(self.RasterYSize)

    def DataType(self):
        return(self.DataType)

    def update_bbox(self):
        self.ul_lon, self.cell_xsize, _, self.ul_lat, _, self.cell_ysize = self.GeoTransform
        self.lr_lon = self.ul_lon + (self.RasterXSize * self.cell_xsize)
        self.lr_lat = self.ul_lat + (self.RasterYSize * self.cell_ysize)

        self.bbox = tuple([[self.ul_lon, self.lr_lat], [self.lr_lon, self.ul_lat]])

def _extract_bands(ds, bands):
    if ds.RasterCount > 1:
        layer, row, col = ds.RasterCount, ds.RasterYSize, ds.RasterXSize
        if (type(bands) == type(list())) or (type(bands) == type(tuple())):
            array = np.random.randint(1, size=(len(bands), row, col))
            for n, index in enumerate(bands):
                tempArray = ds.GetRasterBand(index)
                array[n, :, :] = tempArray.ReadAsArray()
            if array.shape[0] == 1:
                array = np.reshape(array, (row, col))
        elif type(bands) == type(1):
            array = ds.GetRasterBand(bands).ReadAsArray()
    else:
        array = ds.ReadAsArray()
    return(array)
    
def read(file, bands='all'):
    """
    Read raster file

    The function reads the raster file and generates two object. The first one is a
    datasource object and the second is a numpy array that contains cell values of the
    bands.

    Parameters
    ----------
    file            : datasource object
                      Path to the input file.
                      
    bands           : integer, tuple, list or 'all'
                      Bands to read. This can either be a specific band number you wish
                      to read or a list or tuple of band numbers or 'all'.

    Returns
    -------
    datasource      : datasource object
                      A data source object that contains the metadata of the raster file.
                      Information such as the number of rows and columns, number of bands,
                      data type of raster, projection, cellsize, geographic extent etc. are
                      stored in this datasource object.

    data_array      : numpy array
                      A 2D or 3D numpy array that contains the DN values of the raster file.
                      If the input file is a single band raster, the function returns a 2D array.
                      Whereas, if the input file is a multiband raster, this function returns a
                      3D array.
                      
    Attributes
    ----------
    RasterCount     : integer
                      The total number of bands in the input file.
                      
    RasterXSize     : integer
                      Height of the raster represented as the number of rows.
                      
    RasterYSize     : integer
                      Width of the raster represented as the number of columns.
                      
    Projection      : projection object
                      The projection of the input file.
                      
    GeoTransform    : geotransform object
                      This is the Geotransform tuple of the input file. The tuple
                      can be converted to list and updated to change various properties
                      of the raster file.
    
    Examples
    --------
    >>> from pyrsgis import raster
    >>> input_file = r'E:/path_to_your_file/raster_file.tif'
    >>> ds, data_arr = raster.read(input_file)

    The 'data_arr' is a numpy array. The 'ds' is the datasource object that
    contains details about the raster file.

    >>> print(ds.RasterXSize, ds.RasterYSize)

    The output from the above line will be equal to the followng line:

    >>> print(arr.shape)

    Please note that if the input file is a multispectral raster, the 'arr.shape'
    command will result a tuple of size three, where the number of bands will be at
    the first index. For multispectral input files, the 'arr.shape' will be equal
    to the following line:

    >>> print(ds.RasterCount, ds.RasterXSize, ds.RasterYSize)
    
    """
    
    ds = gdal.Open(file)
    if type(bands) == type('all'):
        if bands.lower()=='all':
            array = ds.ReadAsArray()
            ds = _create_ds(ds)
            return(ds, array)
    elif type(bands) == type(list()) or\
         type(bands) == type(tuple()) or\
         type(bands) == type(1):
        array = _extract_bands(ds, bands)
        ds = _create_ds(ds)
        return(ds, array)
    else:
        print("Inappropriate bands selection. Please use the following arguments:\n1) bands = 'all'\n2) bands = [2, 3, 4]\n3) bands = 2")
        return(None, None)

raster_dtype = {'byte': gdal.GDT_Byte,
                'cfloat32': gdal.GDT_CFloat32,
                'cfloat64': gdal.GDT_CFloat64,
                'cint16': gdal.GDT_CInt16,
                'cint32': gdal.GDT_CInt32,
                'float': gdal.GDT_Float32,
                'float32': gdal.GDT_Float32,
                'float64': gdal.GDT_Float64,
                'int': gdal.GDT_Int16,
                'int16': gdal.GDT_Int16,
                'int32': gdal.GDT_Int32,
                'uint8': gdal.GDT_Byte,
                'uint16': gdal.GDT_UInt16,
                'uint32': gdal.GDT_UInt32,
                }

def export(arr, ds, filename='pyrsgis_outFile.tif', dtype='default', bands='all', nodata=-9999, compress=None):
    """
    Export GeoTIFF file

    This function exports the GeoTIF file using a data source object
    and an array containing cell values.

    Parameters
    ----------
    arr             : array
                      A numpy array containing the cell values of
                      to-be exported raster. This can either be a 2D
                      or a 3D array. Please note that the channel
                      index should be in the beginning.
                      
    ds              : datasource object
                      The datasource object of a target reference raster.
                      
    filename        : string
                      Output file name ending with '.tif'. This can include
                      relative path or full path of the file.
                      
    dtype           : string
                      The data type of the raster to be exported. It can take
                      one of these values, 'byte', 'cfloat32', 'cfloat64',
                      'cint16', 'cint32', 'float', 'float32', 'float64',
                      'int', 'int16', 'int32', 'uint8', 'uint16', 'uint32'
                      or 'default'. The 'default' type value will take the
                      data type from the given datasource object. It is advised
                      to use a lower depth data value, this helps in reducing the
                      file size on the disk.
                      
    bands           : integer, list, tuple or 'all'
                      The band(s) you want to export. Please note that the band
                      number here is actual position on band instead of Python's default
                      index number. That is, the first band should be referred as 1.
                      The 'bands' parameter defaults to 1 and should only be tweaked when
                      the data array to be exported is a 3D array. If not specified, only the
                      first band of the 3D array will be exported.
                      
    nodata          : signed integer
                      The value that you want to tret as NULL or NoData in you output raster.
                      
    compress        : string
                      Compression type of your output raster. Options are 'LZW', 'DEFLATE'
                      and other methods that GDAL offers. Compressing the data can save a lot
                      of disk space without losing data. Some methods, for instance 'LZW'
                      can reduce the size of the raster from more than a GB to less than 20 MB.
   
    Examples
    --------
    >>> from pyrsgis import raster
    >>> input_file = r'E:/path_to_your_file/landsat8_multispectral.tif'
    >>> ds, data_arr = raster.read(input_file)
    >>> red_arr = data_arr[3, :, :]
    >>> nir_arr = data_arr[4, :, :]
    >>> ndvi_arr = (nir_arr - red_arr) / (nir_arr + red_arr)

    Or directly in one go:

    >>> ndvi_arr = (data_arr[4, :, :] - data_arr[3, :, :]) / (data_arr[4, :, :] + data_arr[3, :, :])

    And then export:

    >>> output_file = r'E:/path_to_your_file/landsat8_ndvi.tif'
    >>> raster.export(ndvi_arr, ds, output_file, dtype='float32')

    Note that the 'dtype' parameter here is explicitly defined as 'float32'
    since NDVI is a continuous data.
    
    """

    # if given file name does not end with .tif, add it
    if os.path.splitext(filename)[-1].lower() != '.tif':
        filename = filename + '.tif'
    
    #If dtype is default and matches with ds, use int16.
    #If dtype is default and disagrees with ds, use ds datatype.
    #If a dtype is specified, use that.
    
    if (dtype == 'default') and (ds.DataType == raster_dtype['int']):
        dtype = 'int'
    elif (dtype == 'default') and (ds.DataType != raster_dtype['int']):
        dtype = list(raster_dtype.keys())[list(raster_dtype.values()).index(ds.DataType)]
    else:
        pass

    if len(arr.shape) == 3:
        layers, row, col = arr.shape
    elif len(arr.shape) == 2:
        row, col = arr.shape
        layers = 1

    if type(bands) == type('all'):
        if bands.lower() == 'all':
            nBands = layers
            if nBands > 1:
                outBands = list(np.arange(1, layers+1))
            elif nBands == 1:
                outBands = [1]
                arr = np.reshape(arr, (1, row, col))
    if type(bands) == type(1):
        nBands = 1
    elif type(bands) == type(list()) or\
         type(bands) == type(tuple()):
        nBands = len(bands)
        outBands = bands
    driver = gdal.GetDriverByName("GTiff")

    if compress == None:
        outdata = driver.Create(filename, col, row, nBands, raster_dtype[dtype.lower()])
    else:
        outdata = driver.Create(filename, col, row, nBands, raster_dtype[dtype.lower()], options=['COMPRESS=%s'%(compress)])
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjection())
    if type(bands) == type(1):
        if layers > 1:
            outdata.GetRasterBand(nBands).WriteArray(arr[bands-1, :, :])
            outdata.GetRasterBand(nBands).SetNoDataValue(nodata)
        else:
            outdata.GetRasterBand(nBands).WriteArray(arr)
            outdata.GetRasterBand(nBands).SetNoDataValue(nodata)
    elif (type(bands) == type('all') and bands.lower()=='all') or\
         type(bands) == type([1, 2, 3])or\
         type(bands) == type(tuple()):
        for n, bandNumber in enumerate(outBands):
            outdata.GetRasterBand(n+1).WriteArray(arr[bandNumber-1,:,:])
            outdata.GetRasterBand(n+1).SetNoDataValue(nodata)
    outdata.FlushCache() 
    outdata = None

def north_east(arr, layer='both', flip_north=False, flip_east=False):
    """
    Generate row and column number arrays

    This function can generate 2D arrays containing row or column number
    of each cell, which are referred to as northing and easting arrays here.

    Parameters
    ----------
    arr          : array
                   A 2D or 3D numpy array.

    layer        : string
                   Either of these options: 'both', 'north', 'east'

    flip_north   : boolean
                   Whether to flip the northing array. If True, the
                   array will be flipped such that the values increase
                   from bottom to top instead of top to bottom, which
                   is the default way.

    flip_east   : boolean
                   Whether to flip the easting array. If True, the
                   array will be flipped such that the values increase
                   from right to left instead of left to right, which
                   is the default way.

    Returns
    -------
    array(s)     : 2D numpy array(s)
                   If ``layers`` argument was left default or set to 'both',
                   then the function returns a tuple of both the northing and
                   easting arrays. Otherwise, either northing or easting array will
                   be returned depending on the ``layers`` argument.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> input_file = r'E:/path_to_your_file/your_file.tif'
    >>> ds, data_arr = raster.read(your_file)
    >>> north_arr, east_arr = raster.north_east(data_arr)
    >>> print(north_arr.shape, east_arr.shape)

    The above line will generate both the arrays of same size as the input array.
    If you want either of north or east rasters, you can do so by specifying the
    ``layer`` parameter:

    >>> north_arr = raster.north_east(data_arr, layer='north')
    
    To check, you can display them one by one using matplotlib:
    
    >>> from matplotlib import pyplot as plt
    >>> plt.imshow(north_arr)
    >>> plt.show()
    >>> plt.imshow(east_arr)
    >>> plt.show()

    The arrays will be displayed as image one by one. You can hover over the
    displayed image to check the cell values. If you wish to flip the northing
    array upside down or easting array left to right, you can do so by specifying
    the ``flip_north`` and/or ``flip_east`` to ``True``.

    >>> north_arr, east_arr = raster.north_east(data_arr, flip_north=True, flip_east=True)

    You can again display these new arrays and hover the mouse to check values,
    which will now be different from the default ones.
    """
        
    if len(arr.shape) > 2 : _, row, col = arr.shape
    if len(arr.shape) == 2 : row, col = arr.shape

    north = np.linspace(1, row, row)
    east = np.linspace(1, col, col)
    east, north = np.meshgrid(east, north)

    if flip_north == True : north = np.flip(north, axis=0)
    if flip_east == True : east = np.flip(east, axis=1)
    
    if layer=='both':
        return(north, east)
    elif layer=='north':
        return(north)
    elif layer=='east':
        return(east)

def north_east_coordinates(ds, arr, layer='both'):
    """
    Generate arrays with cell latitude and longitude value.

    This function can generate arrays that contain the centroid latitude
    and longitude values of each cell.

    Parameters
    ----------
    ds           : datasource object
                   A datasource object of a raster, typically generated using the
                   ``pyrsgis.raster.read`` function.
             
    arr          : array
                   A 2D or 3D array of the raster corresponding to the daasource object.

    layer        : string
                   Either of these options: 'both', 'north', 'east'

    Returns
    -------
    array(s)     : 2D numpy array(s)
                   If ``layers`` argument was left default or set to 'both',
                   then the function returns a tuple of both the northing and
                   easting arrays. Otherwise, either northing or easting array will
                   be returned depending on the ``layers`` argument.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> input_file = r'E:/path_to_your_file/your_file.tif'
    >>> ds, data_arr = raster.read(your_file)
    >>> north_arr, east_arr = raster.north_east(data_arr)
    >>> print(north_arr.shape, east_arr.shape)

    The above line will generate both the arrays of same size as the input array.
    If you want either of north or east rasters, you can do so by specifying the
    ``layer`` parameter:

    >>> north_arr = raster.north_east(data_arr, layer='north')
    
    To check, you can display them one by one using matplotlib:
    
    >>> from matplotlib import pyplot as plt
    >>> plt.imshow(north_arr)
    >>> plt.show()
    >>> plt.imshow(east_arr)
    >>> plt.show()

    The arrays will be displayed as image one by one. You can hover over the
    displayed image to check the cell values.

    The generated latitude and longitude arrays can be exported using the following:
    
    >>> raster.export(north_arr, ds, r'E:/path_to_your_file/northing.tif', dtype='float32')
    >>> raster.export(east_arr, ds, r'E:/path_to_your_file/easting.tif', dtype='float32')
    
    """
    
    if layer.lower() == 'north': north = north_east(arr, layer='north')
    if layer.lower() == 'east': east = north_east(arr, layer='east')
    if layer.lower() == 'both': north, east = north_east(arr, layer='both')

    if 'north' in locals().keys(): north = list(ds.GeoTransform)[3] + (north * list(ds.GeoTransform)[-1] - list(ds.GeoTransform)[-1]/2)
    if 'east' in locals().keys(): east = list(ds.GeoTransform)[0] + (east * list(ds.GeoTransform)[1] - list(ds.GeoTransform)[1]/2)
        
    if layer=='both':
        return(north, east)
    elif layer=='north':
        return(north)
    elif layer=='east':
        return(east)
    
def northing(reference_file, outFile='pyrsgis_northing.tif', value='number', flip=True, dtype='int16', compress=None):
    """
    Generate northing raster using a reference .tif file

    This function generates northing raster from a given raster file.

    Parameters
    ----------
    reference_file   : string
                       Path to a reference raster file for which the northing file
                       will be generated.

    outfile          : string
                       Path to the output northing file, ideally with '.tif' extension.

    value            : string
                       The desired value in the output raster. Available options are
                       'number', 'normalised' and 'coordinates'. 'number' will result in
                       the row number of the cells, 'normalised' will scale the row number
                       values such that the output raster ranges from 0 to 1. 'coordinates'
                       will result in raster that contain the latitude of centroid of each cell.

    flip             : boolean
                       Whether to flip the resulting raster or not. If ``True``, the
                       values in output northing raster will be flipped upside down.
                       Please note that this option is only viable when the ``value``
                       parameter is set to number or normalised. Flipping will not
                       work when the ``value`` parameter is set to coordinates.

    dtype            : string
                       The data type of the output raster.
                      
    compress        : string
                      Compression type of your output raster. Options are 'LZW', 'DEFLATE'
                      and other methods that GDAL offers. This is same as the ``pyrsgis.raster.export``
                      function.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> reference_file = r'E:/path_to_your_file/your_file.tif'
    >>> raster.northing(file1, r'E:/path_to_your_file/northing_number.tif', flip=False, value='number')

    This will save the file where cells calue represents the row number. Please note that the
    ``flip`` parameter defaults to ``True`` to replicate the way latitudes increase, that is,
    from bottom to top.

    If you want to normalise the output raster, switch the ``value`` parameter to 'normalised'.
    You can switch the ``flip`` parameter as per your requirement.

    >>> raster.northing(file1, r'E:/path_to_your_file/northing_normalised.tif', value='normalised')

    If you want the output file to have the latitude of cell centre, you can change the ``value``
    switch. Please note that the ``flip`` switch will be disabled when exporting as coordinates.

    >>> raster.northing(file1, r'E:/path_to_your_file/northing_coordinates.tif', value='coordinates')

    It has been found that significant reduction is disk space usage can be achieved by passing a
    compression type of the output raster, therefore, doing so is highly recommended. An example of
    using the ``compres`` parameter.

    >>> raster.northing(file1, r'E:/path_to_your_file/northing_number_compressed.tif', compress='DEFLATE')
        
    """
    
    ds, data_arr = read(reference_file, bands=1)  
    north = north_east(data_arr, layer='north')

    if value.lower() == 'coordinates':
        flip = False
        north = list(ds.GeoTransform)[3] + (north * list(ds.GeoTransform)[-1] - list(ds.GeoTransform)[-1]/2)
        dtype = 'float32'
        
    elif value.lower() == 'normalised':
        north += 1
        north /= north.max()
        dtype = 'float32'

    if flip == True : north = np.flip(north, axis=0)

    export(north, ds, filename=outFile, dtype=dtype, compress=compress)

def easting(reference_file, outfile='pyrsgis_easting.tif', value='number', flip=False, dtype='int16', compress=None):
    """
    Generate easting raster using a reference .tif file

    This function generates northing raster from a given raster file.

    Parameters
    ----------
    reference_file   : string
                       Path to a reference raster file for which the easting file
                       will be generated.

    outfile          : string
                       Path to the output easting file, ideally with '.tif' extension.

    value            : string
                       The desired value in the output raster. Available options are
                       'number', 'normalised' and 'coordinates'. 'number' will result in
                       the column number of the cells, 'normalised' will scale the column number
                       values such that the output raster ranges from 0 to 1. 'coordinates'
                       will result in raster that contain the longitude of centroid of each cell.

    flip             : boolean
                       Whether to flip the resulting raster or not. If ``True``, the
                       values in output northing raster will be flipped upside down.
                       Please note that this option is only viable when the ``value``
                       parameter is set to number or normalised. Flipping will not
                       work when the ``value`` parameter is set to coordinates.

    dtype            : string
                       The data type of the output raster.
                      
    compress         : string
                       Compression type of your output raster. Options are 'LZW', 'DEFLATE'
                       and other methods that GDAL offers. This is same as the ``pyrsgis.raster.export``
                       function.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> reference_file = r'E:/path_to_your_file/your_file.tif'
    >>> raster.easting(file1, r'E:/path_to_your_file/easting_number.tif', flip=False, value='number')

    This will save the file where cells calue represents the column number. Please note that the
    ``flip`` parameter defaults to ``False`` to replicate the way longitudes increase, that is,
    from left to right.

    If you want to normalise the output raster, switch the ``value`` parameter to 'normalised'.
    You can switch the ``flip`` parameter as per your requirement.

    >>> raster.easting(file1, r'E:/path_to_your_file/easting_normalised.tif', value='normalised')

    If you want the output file to have the longitude of cell centre, you can change the ``value``
    switch. Please note that the ``flip`` switch will be disabled when exporting as coordinates.

    >>> raster.easting(file1, r'E:/path_to_your_file/easting_coordinates.tif', value='coordinates')

    It has been found that significant reduction is disk space usage can be achieved by passing a
    compression type of the output raster, therefore, doing so is highly recommended. An example of
    using the ``compres`` parameter.

    >>> raster.easting(file1, r'E:/path_to_your_file/easting_number_compressed.tif', compress='DEFLATE')
        
    """
    
    ds, data_arr = read(reference_file, bands=1)
    east = north_east(data_arr, layer='east')

    if value.lower() == 'coordinates':
        flip = False
        east = list(ds.GeoTransform)[0] + (east * list(ds.GeoTransform)[1] - list(ds.GeoTransform)[1]/2)
        dtype = 'float32'
    
    elif value.lower() == 'normalised':
        east += 1
        east /= east.max()
        dtype = 'float32'
        
    if flip==True: east = np.flip(east, axis=1)        

    export(east, ds, filename=outfile, dtype=dtype, compress=compress)
    
def radiometric_correction(arr, pixel_depth=8, return_minmax=False, min_val=None, max_val=None):
    if len(arr.shape) == 3:
        if min_val == None: min_val = list()
        if max_val == None: max_val = list()
        
        for bandNumber in range(arr.shape[0]):
            min_val.append(arr[bandNumber, :, :].min())
            max_val.append(arr[bandNumber, :, :].max())
            
            arr[bandNumber, :, :] = 2**pixel_depth*((arr[bandNumber, :, :] - min_val[-1]) / (max_val[-1] - min_val[-1]))
    else:
        if min_val == None: min_val = arr.min()
        if max_val == None: max_val = arr.max()
        
        arr = (arr - min_val) / (max_val - min_val)
        
    if return_minmax == True:
        return arr, min_val, max_val
    else:
        return arr

def shift(ds, x=0, y=0, shift_type='coordinate'):
    """
    Shift the datasource of a raster file

    This function can modify the geographic extent in the datasource object of the
    raster file. When the modified datasource object is used, the exported raster
    file will be shifted towards a given direction.

    Parameters
    ----------
    ds           : datasource object
                   A datasource object of the raster. Ideally, the datasource should be the
                   same as one generated by the ``pyrsgis.raster.read`` function.

    shift_type   : string
                   Available options are 'coordinates' and 'cell', which correspond to
                   shifting the datasource either by the projection units of the raster
                   or by number of cells respectively.

    x            : number
                   The amount of shift required in x direction (longitude). Please note that
                   this can not be float value if the ``shift_type`` parameter is set to 'cell'.

    y            : number
                   The amount of shift required in y direction (latitude). Please note that
                   this can not be float value if the ``shift_type`` parameter is set to 'cell'.

    Returns
    -------
    new_ds       : datasource object
                   A new modified datasource object which when used to export a raster will
                   result in a shifted raster file.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> infile = r'E:/path_to_your_file/your_file.tif'
    >>> ds, data_arr = raster.read(infile)
    >>> new_ds = raster.shift(ds, x=10, y=10)
    >>> print('Original bounding box:', ds.bbox)
    >>> print('Modified bounding box:', new_ds.bbox)
    Original geo transform: ([752895.0, 1405185.0], [814215.0, 1466805.0])
    Modified geo transform: ([752905.0, 1405195.0], [814225.0, 1466815.0])

    Notice that the bounding box values in the ``ds`` object have both shifted
    by 10 units. Negative values can be given to shift the ``ds`` onject in the opposite
    direction.

    The ``ds`` object can also be shifted by number of cells by switching the ``shift_type``
    parameter.

    >>> new_ds = raster.shift(ds, x=10, y=10, shift_type='cell')
    >>> print('Modified bounding box:', new_ds.GeoTransform)
    Modified geo transform: ([753195.0, 1405485.0], [814515.0, 1467105.0])

    Notice that the modified ``ds`` object is now shifted by 10*cell size (30 - a Landsat
    data used for demonstration).

    The modified ``ds`` object can be used to export raste file.

    >>> raster.export(data_arr, new_ds, r'E:/path_to_your_file/shifted_file.tif')
    
    """
    
    if shift_type.lower() in ['coordinate', 'cell']:

        new_ds = deepcopy(ds)
        out_transform = list(new_ds.GeoTransform)

        if shift_type.lower() == 'coordinate':
            delta_x = x
            delta_y = y
        elif shift_type.lower() == 'cell':
            delta_x = x * out_transform[1]
            delta_y = -y * out_transform[-1]

        out_transform[0] +=  delta_x
        out_transform[3] +=  delta_y
        new_ds.GeoTransform = tuple(out_transform)

        new_ds.update_bbox()

        return(new_ds)
    else:
        print("Invalid shift_type. Acceptable options are " + \
              "'coordinate' and 'cell'. Please see the documentation at %s" % (doc_address))

def shift_file(file, shift_type='coordinate', x=0, y=0, outfile=None, dtype='default'):
    """
    Shift and export raster file in one go

    This function can export a shifted version of the input raster file.

    Parameters
    ----------
    file         : string
                   Name or path of the file to be shifted.

    shift_type   : string
                   Available options are 'coordinates' and 'cell', which correspond to
                   shifting the raster either by the projection units of the raster
                   or by number of cells respectively.

    x            : number
                   The amount of shift required in x direction (longitude). Please note that
                   this can not be float value if the ``shift_type`` parameter is set to 'cell'.

    y            : number
                   The amount of shift required in y direction (latitude). Please note that
                   this can not be float value if the ``shift_type`` parameter is set to 'cell'.

    outfile      : string
                   Outpt raster file name or path, ideally with a '.tif' extension.

    dtype        : string
                   The data type of the output raster. If nothing is passed, the data type is
                   picked from the ``ds`` object.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> infile = r'E:/path_to_your_file/your_file.tif'
    >>> outfile = r'E:/path_to_your_file/shifted_file.tif'
    >>> raster.shift_file(infile, x=10, y=10, outfile=outfile)

    The exported file will be shifted by 10 units in the x and y directions.
    You may pass negative values to shift the raster in the opposite direction.

    The raster file can also be shifted by number of cells by switching the ``shift_type``
    parameter.

    >>> raster.shift_file(infile, x=10, y=10, outfile=outfile, shift_type='cell')

    """
    
    ds, arr = read(file)
    out_ds = shift(ds, x, y, shift_type)

    if outfile == None:
        outfile = '%s_shifted.tif' % (os.path.splitext(file)[0])

    export(array, ds, filename=outfile, dtype=dtype)

def clip(ds, data_arr, x_min, x_max, y_min, y_max):
    """
    ds              : datasource object
                      A datasource object of the raster. Ideally, the datasource should be the
                      same as one generated by the ``pyrsgis.raster.read`` function.

    data_arr        : array
                      A 2D or 3D array to clip.

    x_min           : integer or float
                      The lower longitude value.

    x_max           : integer or float
                      The upper longitude value.

    y_min           : integer or float
                      The lower latitude value.

    y_max           : integer or float
                      The upper latitude value.


    Returns
    -------
    ds              : datasource object
                      A modified ``ds`` object.

    clipped_array   : array
                      A 2D or 3D array. This is the clipped version of the input array.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> infile = r'E:/path_to_your_file/your_file.tif'
    >>> ds, data_arr = raster.read(infile)
    >>> print('Original bounding box:', ds.bbox)
    >>> print('Original shape of raster:', data_arr.shape)
    Original bounding box: ([752893.9818, 1405185.0], [814213.9818, 1466805.0])
    Original shape of raster: (2054, 2044)

    This is the original raster data. Now clip the raster using a bounding box of
    your choice.

    >>> new_ds, clipped_arr = raster.clip(ds, data_arr, x_min=770000, x_max=790000, y_min=1420000, y_max=1440000)
    >>> print('Clipped bounding box:', ds.bbox)
    >>> print('Clipped shape of raster:', data_arr.shape)
    Clipped bounding box: ([770023.9818, 1420005.0], [789973.9818, 1439985.0])
    Clipped shape of raster: (666, 665)

    Note that the raster extent and the data array has now been clipped using the
    given bounding box. The raster can now easily be exported.

    >>> raster.export(clipped_arr, new_ds, r'E:/path_to_your_file/clipped_file.tif')
    
    """
    
    # if array is multiband, take the first band
    temp_array = data_arr[0, :, :] if len(data_arr.shape) == 3 else data_arr
    
    north, east = north_east_coordinates(ds, temp_array, layer='both')

    # make values beyond the lat long zero
    temp_array[north < (y_min - ds.cell_ysize/2)] = 0
    temp_array[north > (y_max + ds.cell_ysize/2)] = 0
    temp_array[east < (x_min + ds.cell_xsize/2)] = 0
    temp_array[east > (x_max - ds.cell_xsize/2)] = 0

    # get the bouding box and clip the array
    non_zero_index = np.nonzero(temp_array)
    row_min, row_max = non_zero_index[0].min(), non_zero_index[0].max()+1
    col_min, col_max = non_zero_index[1].min(), non_zero_index[1].max()+1

    # modify the metadata
    north = north[row_min:row_max, col_min:col_max]
    east = east[row_min:row_max, col_min:col_max]
    #print(north.shape, east.shape)
    #print(north.min(), east.max())

    geo_transform = list(ds.GeoTransform)
    geo_transform[3] = north.max() - (ds.GeoTransform[-1] / 2)
    geo_transform[0] = east.min() - (ds.GeoTransform[1] / 2)
    out_ds = deepcopy(ds)
    out_ds.GeoTransform = tuple(geo_transform)
    out_ds.RasterYSize, out_ds.RasterXSize = north.shape
    out_ds.update_bbox()

    if len(data_arr.shape) == 3:
        return(out_ds, data_arr[:, row_min:row_max, col_min:col_max])
    else:
        return(out_ds, data_arr[row_min:row_max, col_min:col_max])

def clip_file(file, x_min, x_max, y_min, y_max, outfile=None):
    """
    Clip and export raster file in one go

    This function can clip a raster file by using minimum and maximum latitude
    and longitude values.

    Parameters
    ----------
    file            : string
                      Input file name or path to clip.

    x_min           : integer or float
                      The lower longitude value.

    x_max           : integer or float
                      The upper longitude value.

    y_min           : integer or float
                      The lower latitude value.

    y_max           : integer or float
                      The upper latitude value.

    outfile         : string
                      Name or path to store the clipped raster file.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> infile = r'E:/path_to_your_file/your_file.tif'
    >>> outfile = r'E:/path_to_your_file/clipped_file.tif'
    >>> raster.clip_file(infile, x_min=770000, x_max=790000, y_min=1420000, y_max=1440000, outfile=outfile)

    The catch here is that the user should be aware of and has to assign the minimum
    and maximum latitude and longitude values. If you are not sure of the extent to
    clip, you may want to first read the raster file, plot and find your area of interest
    and check the bounding box of the input raster. To do so, please check the
    ``pyrsgis.raster.clip`` function.
    
    """
    
    ds, array = read(file)

    ds, array = clip(ds, array, x_min, x_max, y_min, y_max)
    
    if outfile == None:
        outfile = '%s_clipped.tif' % (os.path.splitext(file)[0])
    
    export(array, ds, filename=outfile, bands='all')

def trim_array(data_arr, remove='negative', return_clip_index=False):
    """
    Trim raster array to remove NoData value at the edge

    This function trims an array by removing the given unwanted value. Note that the function
    will trim array for the smallest possible bounding box outside which all the cells in the
    input array have the value equal to the value passed using ``remove`` parameter.

    Parameters
    ----------
    data_arr         : array
                       A 2D or 3D array to clip. Ideally this should be a raster array that has
                       unimportant value at the edges (NoData cells in most cases).

    remove           : integer or float or string
                       The value to be considered as irrelevant at the edges. It can be a
                       integer or a float number. An additional option 'negative' is also
                       available that will treat negative values of the array as unnecessary.

    return_clip_index: boolean
                       Whether to return the index used for clipping. If ``True``, the function
                       will return both, the clipped array and a list cointaining [x_min, y_min]
                       and  [x_max, y_max] representing column and row indexes.

    Returns
    -------
    trimmed_arr      : array
                       A trimmed array.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> infile = r'E:/path_to_your_file/your_file.tif'
    >>> ds, data_arr = raster.read(infile)
    >>> new_arr = raster.trim_array(data_arr, remove=-9999)
    >>> print('Shape of the input array:', data_arr.shape)
    >>> print('Shape of the trimmed array:', new_arr.shape)
    Shape of the input array: (15000, 15900)
    Shape of the trimmed array: (7059, 7685)

    In the above example a raster file which was masked using a polygon but the option 'match extent
    of the raster with extent of the input polygon' was disabled has been used for demonstration.
    Although this is a classic example of observing unnecessary padding at the edges of a raster file,
    there can be many more reason for the same. In this particular case, useful values were only towards
    a corner of the raster surround by NoData cells. Hence, the actual extent of the file was much larger
    (and unnecessary).

    In a similar fashion, any other value can be used to trim the raster array. Using the 'negative'
    option for the ``remove`` parameter will treat negative values as unnecessary. It should be noted
    that cells within the 'meaningful' region of the raster that have value same as the ``remove`` value
    will remain unaffected by the trimming process.
    
    """
    
    out_array = deepcopy(data_arr)

    # remove undesired values
    if type(remove) == type('negative'):
        if remove.lower() == 'negative': out_array[out_array < 0] = 0
    else:
        out_array[out_array == remove] = 0

    # get the bouding box and clip the array
    non_zero_index = np.nonzero(out_array)
    row_min, row_max = non_zero_index[0].min(), non_zero_index[0].max()+1
    col_min, col_max = non_zero_index[1].min(), non_zero_index[1].max()+1

    if return_clip_index:
        return data_arr[row_min:row_max, col_min:col_max], [[col_min, row_min], [col_max, row_max]]
    else:
        return data_arr[row_min:row_max, col_min:col_max]
    

def trim(ds, data_arr, remove):
    """
    Trim raster array and modify ds

    This function trims the raster array by removing the given unwanted value and update datasource
    object accordingly. Note that the function will trim array for the smallest possible bounding
    box outside which all the cells in the input array have the value equal to the value passed
    using ``remove`` parameter.

    Parameters
    ----------
    ds               : datasource object
                       A datasource object of the raster. Ideally, the datasource should be the
                       same as one generated by the ``pyrsgis.raster.read`` function.
                      
    data_arr         : array
                       A 2D or 3D array to clip. Ideally this should be a raster array that has
                       unimportant value at the edges (NoData cells in most cases).

    remove           : integer or float or string
                       The value to be considered as irrelevant at the edges. It can be a
                       integer or a float number. An additional option 'negative' is also
                       available that will treat negative values of the array as unnecessary.

    Returns
    -------
    new_ds           : datasource object
                       The modified ``ds`` object that can be used to export the trimmed raster.
    
    trimmed_arr      : array
                       A trimmed array.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> infile = r'E:/path_to_your_file/your_file.tif'
    >>> ds, data_arr = raster.read(infile)
    >>> new_ds, new_arr = raster.trim(ds, data_arr, remove=-9999)
    >>> print('Shape of the input array:', data_arr.shape)
    >>> print('Shape of the trimmed array:', new_arr.shape)
    Shape of the input array: (15000, 15900)
    Shape of the trimmed array: (7059, 7685)

    In the above example a raster file which was masked using a polygon but the option 'match extent
    of the raster with extent of the input polygon' was disabled has been used for demonstration.
    Although this is a classic example of observing unnecessary padding at the edges of a raster file,
    there can be many more reason for the same. In this particular case, useful values were only towards
    a corner of the raster surround by NoData cells. Hence, the actual extent of the file was much larger
    (and unnecessary).

    In a similar fashion, any other value can be used to trim the raster array. Using the 'negative'
    option for the ``remove`` parameter will treat negative values as unnecessary. It should be noted
    that cells within the 'meaningful' region of the raster that have value same as the ``remove`` value
    will remain unaffected by the trimming process.

    The trimmed raster can be exported with the following line:
    
    >>> raster.export(new_arr, new_ds, r'E:/path_to_your_file/trimmed_file.tif')
    
    """

    if len(data_arr.shape) == 2:
        temp_arr = deepcopy(data_arr)
    elif len(data_arr.shape) > 2:
        temp_arr = deepcopy(data_arr[0, :, :])
    else:
        print('Inconsistent shape of array received. Please check!')

    # trim the array using trim function, get the bbox
    _, bbox = trim_array(temp_arr, remove=remove, return_clip_index=True)
    [col_min, row_min], [col_max, row_max] = bbox

    # update the dds object by generating north and east rasters
    north, east = north_east_coordinates(ds, temp_arr, layer='both')

    north = north[row_min:row_max, col_min:col_max]
    east = east[row_min:row_max, col_min:col_max]

    geo_transform = list(ds.GeoTransform)
    geo_transform[3] = north.max() - (ds.GeoTransform[-1] / 2)
    geo_transform[0] = east.min() - (ds.GeoTransform[1] / 2)
    out_ds = deepcopy(ds)
    out_ds.GeoTransform = tuple(geo_transform)
    out_ds.RasterYSize, out_ds.RasterXSize = north.shape
    out_ds.update_bbox()

    if len(data_arr.shape) == 2:
        return out_ds, data_arr[row_min:row_max, col_min:col_max]
    elif len(data_arr.shape) > 2:
        return out_ds, data_arr[:, row_min:row_max, col_min:col_max]

def trim_file(filename, remove, outfile):
    """
    Trim and export raster file

    This function trims and exports the raster array by removing the given unwanted value
    Note that the function will trim raster file for the smallest possible bounding box outside
    which all the cells in the raster have the value equal to the value passed
    using ``remove`` parameter. This function is built on the ``pyrsgis.raster.trim``
    function.

    Parameters
    ----------
    file            : string
                      Input file name or path to trim.

    remove          : integer or float or string
                      The value to be considered as irrelevant at the edges. It can be a
                      integer or a float number. An additional option 'negative' is also
                      available that will treat negative values of the array as unnecessary.

    outfile         : string
                      Name or path to store the trimemd raster file.

    Examples
    --------
    >>> from pyrsgis import raster
    >>> infile = r'E:/path_to_your_file/your_file.tif'
    >>> outfile = r'E:/path_to_your_file/trimmed_file.tif'
    >>> raster.trim_file(infile, -9999, outfile)

    In the above example a raster file which was masked using a polygon but the option 'match extent
    of the raster with extent of the input polygon' was disabled has been used for demonstration.
    Although this is a classic example of observing unnecessary padding at the edges of a raster file,
    there can be many more reason for the same. In this particular case, useful values were only towards
    a corner of the raster surround by NoData cells. Hence, the actual extent of the file was much larger
    (and unnecessary).

    In a similar fashion, any other value can be used to trim the raster array. Using the 'negative'
    option for the ``remove`` parameter will treat negative values as unnecessary. It should be noted
    that cells within the 'meaningful' region of the raster that have value same as the ``remove`` value
    will remain unaffected by the trimming process.

    """
    
    # read the file
    ds, data_arr = read(filename)

    # handle non-georeferenced raster (make y cell size negative)
    if not ds.GeoTransform[-1] < 0:
        corrected_geotransform = list(ds.GeoTransform)
        corrected_geotransform[-1] *= -1
        ds.GeoTransform = tuple(corrected_geotransform)
        
    # call trim function
    new_ds, new_arr = trim(ds, data_arr, remove=remove)
    
    # export the outfile
    export(new_arr, new_ds, outfile)

