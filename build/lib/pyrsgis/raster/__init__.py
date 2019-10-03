#pyrsgis/raster

import gdal
import numpy as np

class createDS():

    def __init__(self, ds):
        self.Projection = ds.GetProjection()
        self.GeoTransform = ds.GetGeoTransform()
        self.RasterCount = ds.RasterCount
        self.RasterXSize = ds.RasterXSize
        self.RasterYSize = ds.RasterYSize

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

def extractBands(ds, bands):
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
    ds = gdal.Open(file)
    if type(bands) == type('all'):
        if bands.lower()=='all':
            array = ds.ReadAsArray()
            ds = createDS(ds)
            return(ds, array)
    elif type(bands) == type(list()) or\
         type(bands) == type(tuple()) or\
         type(bands) == type(1):
        array = extractBands(ds, bands)
        ds = createDS(ds)
        return(ds, array)
    else:
        print("Inappropriate bands selection. Please use the following arguments:\n1) bands = 'all'\n2) bands = [2, 3, 4]\n3) bands = 2")
        return(None, None)

def export(band, ds, filename='pyrsgis_outFile.tif', dtype='int', bands=1):
    if len(band.shape) == 3:
        layers, row, col = band.shape
    elif len(band.shape) == 2:
        row, col = band.shape
        layers = 1

    if type(bands) == type('all'):
        if bands.lower() == 'all':
            nBands = layers
            if nBands > 1:
                outBands = list(np.arange(1, layers+1))
            elif nBands == 1:
                outBands = [1]
                band = np.reshape(band, (1, row, col))
    if type(bands) == type(1):
        nBands = 1
    elif type(bands) == type(list()) or\
         type(bands) == type(tuple()):
        nBands = len(bands)
        outBands = bands
    driver = gdal.GetDriverByName("GTiff")
    if dtype == 'float':
            outdata = driver.Create(filename, col, row, nBands, 6) # option: GDT_UInt16, GDT_Float32
    elif dtype == 'int':
            outdata = driver.Create(filename, col, row, nBands, 3) # option: GDT_UInt16, GDT_Float32
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjection())
    if type(bands) == type(1):
        if layers > 1:
            outdata.GetRasterBand(nBands).WriteArray(band[bands-1, :, :])
            outdata.GetRasterBand(nBands).SetNoDataValue(0)
        else:
            outdata.GetRasterBand(nBands).WriteArray(band)
            outdata.GetRasterBand(nBands).SetNoDataValue(0)
    elif (type(bands) == type('all') and bands.lower()=='all') or\
         type(bands) == type([1, 2, 3])or\
         type(bands) == type(tuple()):
        for n, bandNumber in enumerate(outBands):
            outdata.GetRasterBand(n+1).WriteArray(band[bandNumber-1,:,:])
            outdata.GetRasterBand(n+1).SetNoDataValue(0)
    outdata.FlushCache() 
    outdata = None

def northEast(array, layer='both'):
    row, col = array.shape
    north = np.linspace(1, row, row)
    east = np.linspace(1, col, col)
    east, north = np.meshgrid(east, north)
    if layer=='both':
        return(north, east)
    elif layer=='north':
        return(north)
    elif layer=='east':
        return(east)

def northing(referenceFile, outFile='pyrsgis_northing.tif', flip=True):
    ds, band = read(referenceFile, band=1)
    north = northEast(band, layer='north')
    if flip==True:
        north = np.flip(north, axis=0)
    export(north, ds, filename=outFile)

def easting(referenceFile, outFile='pyrsgis_easting.tif', flip=False):
    ds, band = read(referenceFile, band=1)
    east = northEast(band, layer='east')
    if flip==True:
        east = np.flip(east, axis=1)
    export(east, ds, filename=outFile)
    
def radiometricCorrection(arr, byte=8):
    if len(arr.shape) == 3:
        for bandNumber in range(arr.shape[0]):
            arr[bandNumber, :, :] = 2**byte*((arr[bandNumber, :, :] - arr[bandNumber, :, :].min()) / (arr[bandNumber, :, :].max() - arr[bandNumber, :, :].min()))
    else:
        arr = (arr - arr.min()) / (arr.max() - arr.min())
    arr = arr.astype(int)
    return(arr)
