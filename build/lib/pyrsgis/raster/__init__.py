#pyrsgis
#raster
import gdal

def read(file, band='all'):
    ds = gdal.Open(file)
    if band=='all':
        band = ds.ReadAsArray()
    else:
        band = ds.GetRasterBand(band)
        band = band.ReadAsArray()
    return(ds, band)

def export(band, ds, filename='outFile.tif', dtype='int'):
    driver = gdal.GetDriverByName("GTiff")
    if dtype == 'float':
            self.outdata = self.driver.Create(filename, col, row, 1, gdal.GDT_Float32) # option: GDT_UInt16, GDT_Float32
    elif dtype == 'int':
            self.outdata = self.driver.Create(filename, col, row, 1, gdal.GDT_UInt16) # option: GDT_UInt16, GDT_Float32
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjection())
    outdata.GetRasterBand(1).WriteArray(band)
    outdata.GetRasterBand(1).SetNoDataValue(0)
    outdata.FlushCache() 
    outdata = None
