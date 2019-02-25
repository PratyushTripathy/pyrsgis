#convert
#pyrsgis

import os, glob
import numpy as np
import gdal
import csv
from pyrsgis.raster import read

def onedimension(band):
    return(np.reshape(band, (band.shape[0]*band.shape[1])))

def rastertocsv(directory, filename='PyRSGIS_rasterToCSV.csv', negative=True, badrows=True):
    os.chdir(directory)

    data = []
    names = []
    for file in glob.glob("*.tif"):
        ds, band = read(file, band=1)
        nBands = ds.RasterCount
        for n in range(1,nBands+1):
            names.append(file[:-4]+"@"+str(n))
            ds, band = read(file, band=n)
            if negative==False:
                band[band<0] = 0
            band = onedimension(band)
            data.append(band)
    dataArray = np.array(data)
    dataArray = np.transpose(dataArray)
    if badrows == False:
        dataArray[~np.isfinite(dataArray)] = 0 #Replacing all the infinite and nan values to zero
    dataArray = dataArray[~(dataArray==0).all(1)]

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(names)
        for row in range(0,dataArray.shape[0]):
            rowData = dataArray[row]
            writer.writerow(rowData)

