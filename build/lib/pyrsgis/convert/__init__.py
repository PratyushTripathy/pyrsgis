#pyrsgis/convert

import os, glob
import numpy as np
import gdal
import csv
from ..raster import read
from ..raster import export

def changeDimension(arr):
    if len(arr.shape) == 3:
        layer, row, col = arr.shape
        temparr = np.random.randint(1, size=(row*col, layer))
        for n in range(0, layer):
            temparr[:,n] = np.reshape(arr[n,:,:], (row*col,))
        return(temparr)
    if len(arr.shape) == 2:
        row, col = arr.shape
        temparr = np.reshape(arr, (row*col,))
        return(temparr)
    else:
        print("Inconsistent shape of input array.\n2-d or 3-d array expected.")

def rastertocsv(path, filename='PyRSGIS_rasterToCSV.csv', negative=True, badrows=True, remove=[]):
    data = list()
    names = []

    if path.split('.')[-1].lower() == 'tif':
        
        ds, band = read(path)
        for n in range(1,ds.RasterCount+1):
            ds, band = read(path, bands=n)
            if negative==False:
                band[band<0] = 0
            for value in range(0, len(remove)):
                band[band==remove[value]] = 0
            band = np.ravel(band)
            band = np.ravel(band)
            data.append(band)
            names.append('Band@%d' % n)
    else:
        pass
        os.chdir(path)

        for file in glob.glob("*.tif"):
            print(file)
            ds, band = read(file, bands=1)
            nBands = ds.RasterCount
            for n in range(1,ds.RasterCount+1):
                names.append(file[:-4]+"@"+str(n))
                ds, band = read(file, bands=n)
                if negative==False:
                    band[band<0] = 0
                for value in range(0, len(remove)):
                    band[band==remove[value]] = 0
                band = np.ravel(band)
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

def csvtoraster(csvfile, referenceRaster, column=1, dtype='int'):
    column -= 1
    outFile = csvfile.replace('.csv', '.tif')

    ds, band = read(referenceRaster, bands=1)
    rows, cols = band.shape
    with open(csvfile) as csvdata:
        reader = csv.DictReader(csvdata)
        headers = reader.fieldnames
        data = []
        for row in reader:
            data.append(row[headers[column]])
    outArray = np.array(data)
    outArray = np.reshape(outArray, (rows, cols))
    export(outArray, ds, outFile, dtype=dtype)

