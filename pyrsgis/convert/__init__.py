#pyrsgis/convert

import os, glob
import numpy as np
import pandas as pd
import csv
from ..raster import read
from ..raster import export
from .. import doc_address


def changeDimension():
    print('The "changeDimension()" function has moved to "array_to_table()". ' +
          'Please check the pyrsgis documentation at %s for more details.' % (doc_address))


def array_to_table(arr):
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

        
def table_to_array(table, n_rows=None, n_cols=None):
    if len(table.shape) > 2:
        print('A three dimensional array was provided, which is currently not supported. ' + 
              'Please check the pyrsgis documentation at %s' % (doc_address))
        return None
    
    elif len(table.shape) > 1:
        n_bands = table.shape[1]

        if n_bands > 1:
            out_arr = np.zeros((n_bands, n_rows, n_cols))

            for n in range(0, n_bands):
                out_arr[n, :, :] = np.reshape(table[:, n], (n_rows, n_cols))
    else:
        out_arr = np.reshape(table, (n_rows, n_cols))

    return out_arr


def raster_to_csv(path, filename='pyrsgis_rastertocsv.csv', negative=True, badrows=True, remove=[]):
    data_df = pd.DataFrame()
    names = []

    # If an input file is provided
    if os.path.splitext(path)[-1].lower()[-3:] == 'tif':
        ds, arr = read(path)
        header = os.path.splitext(os.path.basename(path))[0]

        if ds.RasterCount > 1:
            for n in range(0, ds.RasterCount):
                data_df['%s@%d' % (header, n+1)] = np.ravel(arr[n, :, :])
        else:
            data_df['%s@%d' % (header, 1)] = np.ravel(arr)

    # If a directory is provided
    else:
        os.chdir(path)

        for file in glob.glob("*.tif"):
            print('Reading file %s..' % (file))
            header = os.path.basename(file)
            
            ds, arr = read(file)
            n_bands = ds.RasterCount

            if n_bands > 1:
                for n in range(0, n_bands):
                    data_df['%s@%d' % (header, n+1)] = np.ravel(arr[n, :, :])
            else:
                data_df['%s@%d' % (header, 1)] = np.ravel(arr)

    # Based on passed arguments, check for negatives and values to be removed
    if negative==False:
        data_df[data_df < 0] = 0

    for value in range(0, len(remove)):
        data_df[data_df == remove[value]] = 0

                
    if badrows == False:
        data_df = data_df[(data_df.T != 0).any()]

    # export the file
    data_df.to_csv(filename, index=False)

def csv_to_raster(csvfile, ref_raster, filename=None,
                  dtype='int', compress='default', nodata=-9999):

    if filename == None:
        filename = csvfile.replace('.csv', '.tif')

    ds, _ = read(ref_raster, bands=1)
    _ = None
    rows, cols = ds.RasterXSize, ds.RasterYSize

    data_df = pd.read_csv(csvfile)
    data_arr = data_df.to_numpy()
    data_df = None
        
    data_arr = np.reshape(data_arr, (rows, cols))
    
    export(data_arr, ds, filename, dtype=dtype, compress=compress, nodata=nodata)

def pandas_to_raster(data_df, x_col, y_col, ref_raster, filename='pyrsgis_pandastoraster.tif',
                     columns=None, x_range=None, y_range=None, dtype='int', compress='default',
                     nodata=-9999):
    # get minimum and maximum value for x
    if x_range == None:
        x_min = data_df[x_col].min()
        x_max = data_df[x_col].max()
    else:
        try:
            x_min, x_max = x_range
        except:
            print('Please provide a list containing range for "x_range" parameter.')
                
    if y_range == None:
        y_min = data_df[y_col].min()
        y_max = data_df[y_col].max()
    else:
        try:
            y_min, y_max = y_range
        except:
            print('Please provide a list containing range for "y_range" parameter.')

    # normalise and scale the x and y columns
    data_df[x_col] = data_df[x_col] - x_min
    data_df[y_col] = data_df[y_col] - y_min

    # generate raster to export
    ds, _ = raster.read(ref_raster)
    _ = None
    data_arr = np.zeros((data_df.shape[1] - 2, ds.RasterXSize, ds.RasterYSize))

    if columns == None:
        columns = list(df.keys())
        for col in [x_col, y_col]:
            columns.remove(col)

    for x_idx in data_df[x_col].values:
        for y_idx in data_df[y_col].values:
            for n, item in enumerate(columns):
                data_arr[n, x_id, y_idx] = data_df[item]

    # export the raster
    raster.export(data_arr, ds, filename, dtype=dtype, compress=compress, nodata=nodata)
        
    
