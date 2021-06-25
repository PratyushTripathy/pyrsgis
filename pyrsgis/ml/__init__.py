#pyrsgis/ml

import copy
import numpy as np
from ..raster import read
from sklearn.feature_extraction import image

# define a function to create image chips from single band array
def imageChipsFromSingleBandArray(data_array, x_size=5, y_size=5):
    out_array = copy.copy(data_array)
    out_array = np.pad(out_array, (int(x_size/2),int(y_size/2)), 'reflect')
    out_array = image.extract_patches_2d(out_array, (x_size, y_size))

    return(out_array)
    
# define a function to create image chips from array
def imageChipsFromArray(data_array, x_size=5, y_size=5):
    
    # if array is a single band image
    if len(data_array.shape) == 2:
        return(imageChipsFromSingleBandArray(data_array, x_size=x_size, y_size=y_size))

    # if array is a multi band image  
    elif len(data_array.shape) > 2:
        data_array = copy.copy(data_array)
        data_array = np.rollaxis(data_array, 0, 3)
        
        for band in range(data_array.shape[2]):
            temp_array = imageChipsFromSingleBandArray(data_array[:, :, band], x_size=x_size, y_size=y_size)

            if band == 0:
                out_array = np.expand_dims(temp_array, axis=3)
            else:
                out_array = np.concatenate((out_array, np.expand_dims(temp_array, axis=3)), axis=3)

        return(out_array)
    
    # if shape of the image is less than two dimensions, raise error  
    else:
        raise Exception("Sorry, only two or three dimensional arrays allowed.")

# define a function ti create image chips from TIF file
def imageChipsFromFile(infile, x_size=5, y_size=5):
    ds, data_array = read(infile)

    return(imageChipsFromArray(data_array, x_size=x_size, y_size=y_size))
