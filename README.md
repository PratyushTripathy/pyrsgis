# Python-for-Remote-Sensing-and-GIS
*pyrsgis* enables the user to read, process and export GeoTIFFs. The module is built on the GDAL library, but is much more convenient when it comes to reading and exporting GeoTIFs. *pyrsgis* also supports reading satellite data directly from .tar.gz files. However, reading from .tar.gz files is currently in its beta phase. Please do not use this package for commercial purpose without my explicit permission. Researchers/ academicians are welcomed for feedback and technical support. Since this is an open-source volunatry project, collaborations are most welcome. Please write to me at [pratkrt@gmail.com](mailto:pratkrt@gmail.com)

To install using pip, see the PyPI page - [link](https://pypi.org/project/pyrsgis/)<br/>
To install using conda, see the Anaconda page - [link](https://anaconda.org/pratyusht/pyrsgis)

**Recommended citation:**<br/>
Tripathy, P. pyrsgis: A Python package for remote sensing and GIS. V0.3.5 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3470674.svg)](https://doi.org/10.5281/zenodo.3470674)

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
where, `ds` is the data source similar to GDAL and `arr` is the numpy array that contains all the bands of the input raster. The `arr` can be 2D or 3D depending on the input data. One can check the shape of the array using the `print(arr.shape)` command. The `bands` argument in the `raster.read` function defaults to `'all'`.<br/>

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
These are the options for the `dtype` argument: `byte`, `cfloat32`, `cfloat64`, `cint16`, `cint32`, `float32`, `float64`, `int16`, `int32`, `uint8`, `uint16`, `uint32`.<br/>
The NoData value can be explicitly defined using the `nodata` parameter, this defaults to `-9999`.

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

* Example with all default parameters:<br/>
```Python
out_file_path = r'D:/sample_file.tif'
raster.export(band, ds, filename='pyrsgis_outFile.tif', dtype='int', bands=1, nodata=-9999)
```
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
The `value` argument defaults to `number`. It can be changed to `normalised` to get a normalised layer. The other option for `value` argument is `coordinates`, which produces the raster layer with cell centroids. Please note that if the `value` argument is set to `normalised`, it will automatically adjust the flip value, i.e. False, both in easting and northing functions. Similarly, the `dtype` parameter auto-adjusts with the data type, but can be changed to a higher pixel depth when `value` argument is `number`. Example with all parameters:<br/>


```Python
northing(reference_file_path, outFile='pyrsgis_northing.tif', flip=True, value='number', dtype='int16')
easting(reference_file_path, outFile='pyrsgis_easting.tif', flip=False, value='number', dtype='int16')
```
</p>
</details>

<details><summary><b>5. Shifting raster layers</b></summary>
<p>
You can shift the raster layers using either the 'shift' or 'shift_file' function. The 'shift' function allows to shift the raster in the backend, whereas, the 'shift_file' directly shifts the GeoTIF file and stores another file.<br/>
  
To shift in the backend:<br/>
```Python
from pyrsgis import raster

# Define the path to the input file and get the data source
infile = r"D:/path_to_your_file/input.tif"
ds, arr = raster.read(infile)

# Define the amount of shift required
delta_x = 15
delta_y = 11.7

# shift the raster
shifted_ds = raster.shift(ds, x=delta_x, y=delta_y, shift_type)

# if you wish to export
raster.export(arr, ds, out_file, dtype='int', bands=1, nodata=-9999)
```
Here, 'ds' is the data source object that is created when the raster is read using 'raster.read' command. 'x' and 'y' are the distance for shifting the raster. The 'shift_type' command let's you move the raster either by the raster units or number of cells, the valid options are 'unit' and 'cell'. By default, the 'shift_type' is 'unit'.<br/>

To shift a GeoTIFF file:<br/>
```Python
from pyrsgis import raster

# Define the path to the input and output file
infile = r"D:/path_to_your_file/input.tif"
outfile = r"D:/path_to_your_file/shifted_output.tif"

# Define the amount of shift required
delta_x = 15
delta_y = 11.7

# shift the raster
raster.shift_file(infile, x=delta_x, y=delta_y, outfile=outfile, shift_type='unit', dtype='uint16')
```
Most of the parameters are same as the 'shift' function. The 'dtype' parameter is same as used in the 'raster.export' function.<br/>
</p>
</details>
  
<details><summary><b>6. Reading directly from .tar.gz files (beta)</b></summary>
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
This computes (band2-band1)/(band2+band1) in the back end and returns a numpy array. The resulting array can be exported using:<br/>
```Python
out_file_path = r'D:/your_ndvi.tif'
your_data.export(your_ndvi, out_file_path, datatype='float')
```
Be careful with the float type of NDVI.<br/>
</p>
</details>
