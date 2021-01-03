# Python-for-Remote-Sensing-and-GIS
**pyrsgis** enables the user to read, process and export GeoTIFFs. The module is built on the GDAL library, but is much more convenient when it comes to reading and exporting GeoTIFs. **pyrsgis** also supports reading satellite data directly from .tar.gz files. However, reading from .tar.gz files is currently in its beta phase. Please do not use this package for commercial purpose without my explicit permission. Researchers/ academicians are welcomed for feedback and technical support. Since this is an open-source volunatry project, collaborations are most welcome. Please write to me at [pratkrt@gmail.com](mailto:pratkrt@gmail.com)


See installation command using pip on the PyPi page - [link](https://pypi.org/project/pyrsgis/)<br/>

**Recommended citation:**<br/>
Tripathy, P. pyrsgis: A Python package for remote sensing and GIS. V0.3.2 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3470674.svg)](https://doi.org/10.5281/zenodo.3470674)

# Sample code
## 1. Reading .tif extension file
Import the module and define the input file path.<br/>
```Python
from pyrsgis import raster

file_path = r'D:/your_file_name.tif'
```
* To read all the bands of a stacked satellite image:<br/>
```Python
ds, arr = raster.read(file_path, bands='all')
```
where, **ds** is the data source similar to GDAL and **arr** is the numpy array that contains all the bands of the input raster. The **arr** can be 2D or 3D depending on the input data. One can check the shape of the array using the `print(arr.shape)` command. The `bands` argument in the `raster.read` function defaults to `'all'`.<br/>

* To read a list of bands of a stacked satellite image:<br/>
```Python
ds, arr = raster.read(file_path, bands=[2, 3, 4])
```
Passing the band numbers in a list returns bands 2, 3 & 4 as three-dimensional numpy array.<br/>

* To read a specific band from stacked satellite image:<br/>
```Python
ds, arr = raster.read(file_path, bands=2)
```
Passing a single band number returns that particular band as two-dimensional numpy array.<br/>

* To read a single band TIF file:<br/>
```Python
ds, arr = raster.read(file_path)
```
Since the `bands` argument defaults to `'all'`, this will read all the bands in the input file, here, one band only.<br/>

## 2. Exporting .tif extension file
In all the below examples, it is assumed that the number of rows and columns, and the cell size of the input and output rasters are the same. All these are stored in the `ds` variable, please see details here: link.<br/>
* To export all bands of a 3D array:<br/>
```Python
raster.export(arr, ds, "sample_file_all_bands.tif", dtype='int', bands='all')
```
The `dtype` argument in the above function defaults to `'int'`, which is 8-bit integer. Please be careful to change this while exporting arrays with large values. Similarly, to export float type array (eg. NDVI), use `dtype = 'float'`<br/>
Other options for the `dtype` argument are: 'byte', 'cfloat32', 'cfloat64', 'cint16', 'cint32', 'float32', 'float64', 'int16', 'int32', 'uint8', 'uint16', 'uint32'

* To export a list of bands of a 3D array:<br/>
```Python
raster.export(arr, ds, "sample_file_bands_234.tif", bands=[2, 3, 4])
```

* To export any one band of a 3D array:<br/>
```Python
raster.export(arr, ds, "sample_file_band_3.tif", bands=3)
```

* To export a single band array:<br/>
```Python
raster.export(arr, ds, "sample_file.tif")
```
where, `arr` should be a 2D array.<br/>

To read the TAR file directly:<br/>
`yourData = rg.readtar("yourFilename.tar.gz")`<br/>

Similarly, stacked TIFF file can be read:<br/>
`yourData = rg.readtif("yourFilename.tif")`<br/>

After the above code, various properties of the raster can be assessed.<br/>
`print(yourData.rows)`<br/>
`print(yourData.cols)`<br/>
will give you the number of rows and columns.<br/>

The number of bands can be checked using:<br/>
`print(yourData.nbands)`<br/>

The satellite sensor can also be determined.<br/>
`print(yourRaster.satellite)`<br/>

If the above code shows the correct satellite sensor correctly, then this getting this should be easy:<br/>
`print(yourRaster.bandIndex)`<br/>
This will show correctly the band number for available bands.<br/>

Any particular band can be extarcted using:<br/>
`yourBand = yourData.getband(bandNumber)`<br/>

The above code returns the band as array which can be visualised using:<br/>
`display(yourBand)`<br/>
or
`display(yourData.getband(bandNumber))`<br/>
The map can directly be saved as an image.<br/>

Map title can also be assigned:<br/>
`display(yourBand, maptitle='Your Map Title')`<br/>

The extracted band can be exported using:<br/>
`yourData.export(yourBand, "yourOutputFilename.tif")`<br/>
This saves the extracted band to the same directory.<br/>
If exporting a float data type (raster with decimal values), please define the datatype explicitly, default is 'int':<br/>
`yourData.export(yourBand, "yourOutputFilename.tif", datatype='float')`<br/>

The NDVI (Normalised Difference Vegetaton Index) can be computed easily.<br/>
`yourndvi = yourData.ndvi()`<br/>
This returns the NDVI array,which can be exported using the same command used for the band above.<br/>

Any normalised difference indev can be computed using:<br/>
`yourIndex = yourData.nordif(bandNumber2, bandNumber1)`<br/>
Which performs (band2-band1)/(band2+band1) in the back end.<br/>

`yourRaster.export(yourndvi, 'yourNDVI.tif', datatype='float')`<br/>
Be careful that the NDVI is of float datatype, whereas the raw bands are integer datatype. Float data export uses more space on hard drive, so the default has been set to integer. Therefore, to export any float datatype, the argument should be passed explicitly.<br/>

Raster files can also be easily converted into CSV files which is mainly required for statistical analysis.<br/>
`from pyrsgis.convert import rastertocsv`<br/>

Assign the directory where raster files are located<br/>
`yourDir = "D:\\yourRasterFolder"`<br/>
`rastertocsv(yourDir, filename='yourFilename.csv')`<br/>

Generally the NoData or NULL values in the raster become random negative values, negatives can be removed using:<br/>
`rastertocsv(yourDir, filename='yourFilename.csv', negative=False)`<br/>

At times the NoData or NULL values in raster become '127' or '65536', they can also be removed by declaring explicitly<br/>
`rastertocsv(yourDir, filename='yourFilename.csv', remove=[127, 65536])`<br/>
This is a trial and check process, please check the generated CSV file for such issues<br/>

Bad rows in the CSV file represents the cell that has zero values in all the rasters and takes a lot of storage space, it can be eliminated using:<br/>
`rastertocsv(yourDir, filename='yourFilename.csv', badrows=False)`<br/>

pyrsgis also allows the user to quickly create the northing and easting coordinates using a reference raster<br/>
The flip option can be use to flip the resulting rasters.<br/>

`from pyrsgis.raster import northing, easting`<br/>

`referenceRaster = 'E:/Example/landcover.tif'`<br/>
`northing(referenceFile, outFile='pyrsgis_northing.tif', flip=True)`<br/>
`easting(referenceFile, outFile='pyrsgis_easting.tif', flip=False)`<br/>

