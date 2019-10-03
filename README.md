# Python-for-Remote-Sensing-and-GIS
PyRSGIS is a powerful module to read, manipulate and export geo-rasters. The module is built on the GDAL library, and is very efficient for various geospatial analysis. Please do not use this package for commercial purpose without my explicit permission. Researchers/ academicians are welcomed for feedback and technical support.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3470674.svg)](https://doi.org/10.5281/zenodo.3470674)

The module is capable of processing Landsat data from the downloaded TAR files itself.

Please find few example below:

Let's import the module by using the below code<br/>
`import pyrsgis as rg`

We will first start with reading raster and perform some basic operations.
Make sure your current working directory is the same where the raster files are located, if not use the following command:<br/>
`import os`<br/>
`os.chdir("d:/yourDirectory")`

Please skip the above two lines of code if the directory is already set to the files location.<br/>

To read bands of a stacked satellite image,<br>
(1) For all bands:<br/>
`dataSource, yourArray = raster.read(file, bands='all')`<br/>
Which returns the data source containing projection information, and a NumPy array.<br/>

To read a list of bands from stacked images:<br/>
(2) For list of bands:<br/>
`dataSource, yourArray = raster.read(file, bands=[2, 3, 4])`<br/>
Which returns bands 2, 3 & 4 as three-dimensional NumPy array.<br/>

To read a specific band from stacked image:<br/>
(3) For a specific band:<br/>
`dataSource, yourArray = raster.read(file, bands=2)`<br/>
Which returns band number 2 as two-dimensional NumPy array.<br/>

To export the bands from the above read data,<br/>
(1) For all bands:<br/>
`raster.export(yourArray, dataSource, "sample_extracted.tif", dtype='int', bands='all')`<br/>
By default, `dtype = 'int'`, to export float type array (eg. NDVI), use `dtype = 'float'`<br/>

(2) For list of bands:<br/>
`raster.export(yourArray, dataSource, "sample_extracted.tif", bands=[2, 3, 4])`<br/>

(3) For a specific band:<br/>
`raster.export(yourArray, dataSource, "sample_extracted.tif", bands=3)`<br/>


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


