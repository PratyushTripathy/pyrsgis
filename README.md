# Python-for-Remote-Sensing-and-GIS
PyRSGIS is a powerful module to read, manipulate and export geo-rasters. The module is built on the GDAL library, and is very efficient for various geospatial analysis. 

Please find few example below:

Let's import the module by using the below code<br/>
`import pyrsgis as rg`

We will first start with reading raster and perform some basic operations.
Make sure your current working directory is the same where the raster files are located, if not use the following command:<br/>
`import os`<br/>
`os.chdir("d:/yourDirectory")`

Please skip the last two lines of code if the directory is already set to the files location.<br/>
Considering that the raster bands are stacked already, reading a multispectral data would be:<br/>
`yourRaster = rg.readtif("yourFilename.tif")`<br/>

After the above code, various properties of the raster can be assessed.<br/>
`print(yourRaster.rows)`<br/>
`print(yourRaster.cols)`<br/>
will give you the number of rows and columns.<br/>

The number of bands can be checked using:<br/>
`print(yourRaster.nbands)`<br/>

Any particular band can be extarcted using:<br/>
`yourBand = yourRaster.getband(bandNumber)`<br/>

The above code returns the band as array which can be visualised using:<br/>
`yourRaster.display(yourBand)`<br/>

The extracted band can be exported using:<br/>
`yourRaster.export(yourBand, "yourOutputFilename.tif")`<br/>
This saves the extracted band to the same directory.<br/>

If stacked properly, the satellite sensor can also be determined.<br/>
`print(yourRaster.satellite)`<br/>

If the above code shows the correct satellite sensor correctly, then this getting this should be easy:<br/>
`print(yourRaster.bandIndex)`<br/>
This will show correctly the band number for available bands.<br/>

The NDVI (Normalised Difference Vgetaton Index) can be computed easily.<br/>
`yourndvi = yourRaster.ndvi()`<br/>
This returns the NDVI array,which can be exported using the same command used for the band above.<br/>

`yourRaster.export(yourndvi, 'yourNDVI.tif', datatype='float')`<br/>
One thing to notice is that the NDVI is of float datatype, whereas the raw bands are integer datatype. Float data export uses more space on hard drive, so the default has been set to integer. Therefore, to export any float datatype, the argument should be passed explicitly.
