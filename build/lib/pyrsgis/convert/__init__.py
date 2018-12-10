#convert
#pyrsgis

import os, glob
import numpy as np
import gdal
import csv
from pyrsgis.raster import read

def onedimension(band):
    return(np.reshape(band, (band.shape[0]*band.shape[1])))

def rastertocsv(directory, filename='PyRSGIS_rasterToCSV.csv'):
    os.chdir(directory)

    data = []
    names = []
    for file in glob.glob("*.tif"):
        names.append(file[:-4])
        ds, band = read(file)
        band = onedimension(band)
        data.append(band)

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(names)
        for row in range(0,data[0].shape[0]):
            rowData = []
            for d in data:
                rowData.append(d[row])
            writer.writerow(rowData)

