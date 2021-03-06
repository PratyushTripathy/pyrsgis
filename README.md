# Python-for-Remote-Sensing-and-GIS
*pyrsgis* enables the user to read, process and export GeoTIFFs. The module is built on the GDAL library, but is much more convenient when it comes to reading and exporting GeoTIFs. *pyrsgis* also supports reading satellite data directly from .tar.gz files. However, reading from .tar.gz files is currently in its beta phase. Please do not use this package for commercial purpose without my explicit permission. Researchers/ academicians are welcomed for feedback and technical support. Since this is an open-source volunatry project, collaborations are most welcome. Please write to me at [pratkrt@gmail.com](mailto:pratkrt@gmail.com)

To install using pip, see the PyPI page - [link](https://pypi.org/project/pyrsgis/)<br/>
To install using conda, see the Anaconda page - [link](https://anaconda.org/pratyusht/pyrsgis)

**Recommended citation:**<br/>
Tripathy, P. pyrsgis: A Python package for remote sensing and GIS. V0.3.2 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3470674.svg)](https://doi.org/10.5281/zenodo.3470674)

# Sample code
<details><summary><b>1. Reading .tif extension file</b></summary>
<p>
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
</p>
</details>

<details><summary><b>2. Exporting .tif extension file</b></summary>
<p>
In all the below examples, it is assumed that the number of rows and columns, and the cell size of the input and output rasters are the same. All these are stored in the `ds` variable, please see details here: link.<br/>
  
* To export all bands of a 3D array:<br/>
```Python
out_file_path = r'D:/sample_file_all_bands.tif'
raster.export(arr, ds, out_file_path, dtype='int', bands='all')
```
The `dtype` argument in the above function defaults to `'int'`, which is 8-bit integer. Please be careful to change this while exporting arrays with large values. Similarly, to export float type array (eg. NDVI), use `dtype = 'float'`. Data type of high pixel-depth, e.g. Integer32, Integer64, or float type uses more space on hard drive, so the default has been set to integer. To export any float datatype, the argument should be passed explicitly.<br/>
These are the options for the `dtype` argument: 'byte', 'cfloat32', 'cfloat64', 'cint16', 'cint32', 'float32', 'float64', 'int16', 'int32', 'uint8', 'uint16', 'uint32'

* To export a list of bands of a 3D array:<br/>
```Python
out_file_path = r'D:/sample_file_bands_234.tif'
raster.export(arr, ds, out_file_path, bands=[2, 3, 4])
```

* To export any one band of a 3D array:<br/>
```Python
out_file_path = r'D:/sample_file_band_3.tif'
raster.export(arr, ds, out_file_path, bands=3)
```

* To export a single band array:<br/>
```Python
out_file_path = r'D:/sample_file.tif'
raster.export(arr, ds, out_file_path)
```
where, `arr` should be a 2D array.<br/>
</p>
</details>

<details><summary><b>3. Converting TIF to CSV</b></summary>
<p>
GeoTIFF files can be converted to CSV files using *pyrsgis*. Every band is flattened to a single-dimensional array, and converted to CSV. These are very useful for statistical analysis.<br/>
Import the function:<br/>
  
```Python
from pyrsgis.convert import rastertocsv
```

To convert all the bands present in a folder:
```Python
your_dir = r"D:/your_raster_directory"
out_file_path = r"D:/yourFilename.csv"

rastertocsv(your_dir, filename=out_file_path)
```

Generally the NoData or NULL values in the raster become random negative values, negatives can be removed using the `negative` argument:<br/>
```Python
rastertocsv(your_dir, filename=out_file_path, negative=False)
```

At times the NoData or NULL values in raster become '127' or '65536', they can also be removed by declaring explicitly.<br/>
```Python
rastertocsv(your_dir, filename=out_file_path, remove=[127, 65536])
```
This is a trial and check process, please check the generated CSV file for such issues and handle as required.<br/>

Similarly, there are bad rows in the CSV file, representing zero value in all the bands. This takes a lot of unnecessary space on drive, it can be eliminated using:<br/>
```Python
rastertocsv(your_dir, filename=out_file_path, badrows=False)
```
</p>
</details>

<details><summary><b>4. Creating northing and easting using a reference raster</b></summary>
<p>
  
pyrsgis allows to quickly create the northing and easting rasters using a reference raster, as shown below:<br/>
<img src="https://raw.githubusercontent.com/PratyushTripathy/pyrsgis/master/media/northing_easting.png" height="225" width="640">

The cell value in the generated rasters are the row and column number of the cell. To generate these GeoTIFF files, start by importing the function:

```Python
from pyrsgis.raster import northing, easting

reference_file_path = r'D:/your_reference_raster.tif'

northing(reference_file_path, outFile= r'D:/pyrsgis_northing.tif', flip=True)
easting(reference_file_path, outFile= r'D:/pyrsgis_easting.tif', flip=False)
```
As the name suggests, the `flip` argument flips the resulting rasters.<br/>
</p>
</details>

<details><summary><b>5. Reading directly from .tar.gz files (beta)</b></summary>
<p>
  
Currently, only Landsat data is supported.<br/>
```Python
import pyrsgis

file_path = r'D:/your_file_name.tar.gz'
your_data = pyrsgis.readtar(file_path)
```
The above code reads the data and stores in the `your_data` variable.<br/>

Various properties of the raster can be assessed using the following code:<br/>
```Python
print(your_data.rows)
print(your_data.cols)
```
This will display the number of rows and columns of the input data.<br/>

Similarly, the number of bands can be checked using:<br/>
```Python
print(your_data.nbands)
```

On reading the .tar.gz files directly, pyrsgis determines the satellite sensor. This can be checked using:<br/>
```Python
print(your_data.satellite)
```
This will display the satellite sensor, for instance, Landsat-5, Landsat-8, etc.<br/>

If the above code shows the correct satellite sensor, then the list of band names of the sensor (in order) can easily be checked using:<br/>
```Python
print(your_data.bandIndex)
```

Any particular band can be extarcted using:<br/>
```Python
band_number = 1
your_band = your_data.getband(band_number)
```
The above code returns the band as array which can be visualised using:<br/>

```Python
display(your_band, maptitle='Title of your image', cmap='PRGn')
```
or, directly using:
```Python
band_number = 1
display(your_data.getband(band_number), maptitle='Title of your image', cmap='PRGn')
```
The generated map can directly be saved as an image.<br/>

The extracted band can be exported using:<br/>
```Python
out_file_path = r'D:/sample_output.tif'
your_data.export(your_band, out_file_path)
```
This saves the extracted band to the same directory.<br/>

To export the float type raster, please define the `datatype` explicitly, default is 'int':<br/>
```Python
your_data.export(your_band, out_file_path, datatype='float')
```

The NDVI (Normalised Difference Vegetaton Index) can be computed easily.<br/>
```Python
your_ndvi = your_data.ndvi()
```

Normalised difference index between any two bands can be computed using:<br/>
```Python
norm_diff = your_data.nordif(bandNumber2, bandNumber1)
```
This computes (band2-band1)/(band2+band1) in the back end and returns a numpy array. THe resulting arracy can be exported using:<br/>
```Python
out_file_path = r'D:/your_ndvi.tif'
your_data.export(your_ndvi, out_file_path, datatype='float')
```
Be careful with the float type of NDVI.<br/>
</p>
</details>
