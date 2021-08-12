# pyrsgis/beta

#Importing all the necessary libraries
import os, glob, datetime
# add exception for deprecated version of gdal
try:
    import gdal
except:
    from osgeo import gdal
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import warnings, shutil
import tarfile, tempfile
from ..raster import read, export, _create_ds

try:
    from matplotlib_scalebar.scalebar import ScaleBar
except:
    pass
        
#Disabling annoying warnings
warnings.filterwarnings("ignore")

#This creates a class for raster, and based on the format of input
#it decides whether input is stacked raster data or .tar.gz file
class readtar():
    oldDir = os.getcwd()

    def __init__(self, name):
        self.oldDir = os.getcwd()
        self.name = name
        self.fileName, self.ext = os.path.splitext(self.name)
        self.initiated = False
        if (self.ext == ".gz") or (self.ext == ".GZ"):
            self.type = "TARfile"
            self.nbands = self.initiateTAR()
            self.band = self.getband(1)
            self.band = None
            self.satellite = self.sensor()
            self.bandIndex = self.checkBandIndex()
        else:
            self.type = "Unidentified data format"
            print("Warning! Expected file type is .tar.gz")

    #This method reads the TAR file and returns the number of TIFF files in it          
    def initiateTAR(self):
        global filesList
        global tarTifList
        self.initiate = True
        self.tarTifList = []
        with tarfile.open(self.name, 'r:gz') as self.tar:
            self.filesList = self.tar.getnames()
            for self.files in self.filesList:
                if (self.files[-4:] == '.TIF') or (self.files[-4:] == '.tif'):
                    self.tarTifList.append(self.files)
            return(len(self.tarTifList)-1)

    #This method creates a temporary directory to extract .tar.gz files
    #This section only executes if input is a tar file
    def createTempDirectory(self):
        try:
            self.tempDirPath = None
            self.tempDirPath = tempfile.TemporaryDirectory('pyrsgis')
            self.tempDir = str(self.tempDirPath).split(" ")[1]
            self.tempDir = self.tempDir[1:-2]
            self.tempDir = self.tempDir.split("\\\\")
            self.tempDirPath = self.tempDir
            self.tempDir[-1] = 'pyrsgis'
            self.tempDir = "\\\\".join(self.tempDir)
            self.tempDirPath.pop()
            self.tempDirPath = "\\\\".join(self.tempDirPath)
##          print("Temporary directory created in \n%s" % self.tempDir)
        except FileNotFoundError:
            pass

    #This method acts as a generator if the input is a tarfile
    def generatorTAR(self, nBand):
        global createdFile
        self.createdFile = []
        self.nBand = str(nBand)
        self.nCreated = 0
        for self.tarinfo in self.tar:
            self.folder = os.path.split(self.tarinfo.name)[0]
            self.fileName = os.path.splitext(self.tarinfo.name)[0]
            self.bandName = self.fileName.split('_')[-1]
            self.ext = os.path.splitext(self.tarinfo.name)[1]
            if (self.ext == ".tif") or (self.ext == ".TIF"):
                if (self.bandName == ("B"+str(self.nBand))):
                    self.createdFile.append(self.tarinfo.name)
                    if self.nCreated > 0:
                        print("Creating temporary file %s" % self.tarinfo.name)
                        self.nCreated += 1
                    yield self.tarinfo

    #This method returns the band in the form of an array
    def getband(self, nBand):
        if self.type == "TARfile":
            with tarfile.open(self.name, 'r:gz') as self.tar:
                self.createTempDirectory()
                if not os.path.exists(self.tempDir):
                    os.mkdir(self.tempDir)
                os.chdir(self.tempDir)
                self.tar.extractall(members=self.generatorTAR(nBand))
            self.ds, self.band = read(self.createdFile[0], bands=1)
            if self.initiated == False:
                self.rows = self.ds.RasterYSize
                self.cols = self.ds.RasterXSize
                self.projection = self.ds.GetProjection()
                self.geotransform = self.ds.GetGeoTransform()
                self.initiated = True
            self.ds = createDS(self.ds)
            # Goes back to the old directory and deletes the temporary directory
            os.chdir(self.oldDir)
            self.clearMemory()
            return(self.band)

    def extractBand(self, bands='All', filename='pyrsgisExtarctedBands.tif'):
        if type(bands)==type(str()):
            tempArray = np.random.randint(1, size=(self.nbands, self.rows, self.cols))
            for n in range(0, self.nbands):
                tempArray[n,:,:] = self.getband(n+1)
        elif type(bands) == type(list()):
            tempArray = np.random.randint(1, size=(len(bands), self.rows, self.cols))
            for n, index in enumerate(bands):
                tempArray[n,:,:] = self.getband(index)
        export(tempArray, self.ds, filename, bands='All')

    #This method calculates the normalised differnce of any two given bands  
    def nordif(self, band2, band1):
        self.band1 = self.getband(band1)
        self.band2 = self.getband(band2)
        return((self.band2-self.band1)/(self.band2+self.band1))

    #This method saves the processed image in the drive  
    def export(self, array, outfile='pyrsgisRaster.tif', dtype='int'):
        export(array, self.ds, filename=outfile, dtype=dtype)

    #This method clears everything stored in the virtual momry to reduce load   
    def clearMemory(self):
        os.chdir(self.tempDirPath)
        for folder in glob.glob("*pyrsgis"):
            shutil.rmtree(folder)
        os.chdir(self.oldDir)
        
    #This method decides the index of the bands depending on the sensor type
    def checkBandIndex(self):
        if self.satellite == 'Landsat - 4/5  TM':
            return({'blue':1,
                    'green':2,
                    'red':3,
                    'nir':4,
                    'swir1':5,
                    'thermal':6,
                    'swir':7})
        elif self.satellite == 'Landsat - 7':
            return({'blue':1,
                    'green':2,
                    'red':3,
                    'nir':4,
                    'swir1':5,
                    'thermal1':6,
                    'thermal2':7,
                    'swir2':8,
                    'panchromatic':9})
        elif self.satellite == 'Landsat - 8':
            return({'aerosol':1,
                    'blue':2,
                    'green':3,
                    'red':4,
                    'nir':5,
                    'swir1':6,
                    'swir2':7,
                    'panchromatic':8,
                    'cirrus':9,
                    'tirs1':10,
                    'tirs2':11})

    #This method decides the satellite sensor, depending on the number of bands
    def sensor(self):
        try:
            if (self.type == "TARfile") and (self.nbands == 7):
                return('Landsat - 4/5  TM')
            elif (self.type == "TARfile") and (self.nbands == 9):
                return('Landsat - 7')
            elif (self.type == "TARfile") and (self.nbands) == 11:
                return('Landsat - 8')
        except:
            print('Warning! Input data has no match in the inventory')        
        
    #This method returns the NDVI of the input file
    def ndvi(self):
        try:
            self.redband = self.getband(self.bandIndex['red'])
            self.nirband = self.getband(self.bandIndex['nir'])
            self.ndviband = ((self.nirband-self.redband)/(self.nirband+self.redband))
        except KeyError:
            print('One of the required band was not found.')
        self.redband = None
        self.nirband = None
        return(self.ndviband)

class readtif():
    oldDir = os.getcwd()

    def __init__(self, name):
        self.name = name
        self.fileName, self.ext = os.path.splitext(self.name)
        self.initiated = False
        self.type = "TIFFfile"
        self.band = self.getband(1)
        self.band = None
        self.satellite = self.sensor()
        self.bandIndex = self.checkBandIndex()

    #This method returns the band in the form of an array
    def getband(self, nBand, datatype='int'):
        self.ds, self.band = read(self.name, bands=nBand)
        if datatype == 'float':
            self.band = self.band.astype(float)
        if self.initiated == False:
            self.rows = self.ds.RasterYSize
            self.cols = self.ds.RasterXSize
            self.nbands = self.ds.RasterCount
            self.projection = self.ds.GetProjection()
            self.geotransform = self.ds.GetGeoTransform()
            self.initiated = True
        self.ds = None
        return(self.band)

    #This method calculates the normalised difference of any two given bands  
    def nordif(self, band2, band1):
        self.band1 = self.getband(band1)
        self.band1 = self.band1.astype(float)
        self.band2 = self.getband(band2)
        self.band2 = self.band2.astype(float)
        return((self.band2-self.band1)/(self.band2+self.band1))

    #This method saves the processed image in the drive  
    def export(self, array, outfile='pyrsgisRaster.tif', datatype='int'):
        export(array, self.ds, filename=outfile, dtype=datatype)
        
    #This method clears everything stored in the virtual momry to reduce load   
    def clearMemory(self):
        self.band = None
        self.ds = None
        
    #This method decides the index of the bands depending on the sensor type
    def checkBandIndex(self):
        if self.satellite == 'Landsat - 4/5  TM':
            return({'blue':1,
                    'green':2,
                    'red':3,
                    'nir':4,
                    'swir1':5,
                    'thermal':6,
                    'swir':7})
        elif self.satellite == 'Landsat - 7':
            return({'blue':1,
                    'green':2,
                    'red':3,
                    'nir':4,
                    'swir1':5,
                    'thermal1':6,
                    'thermal2':7,
                    'swir2':8,
                    'panchromatic':9})
        elif self.satellite == 'Landsat - 8':
            return({'aerosol':1,
                    'blue':2,
                    'green':3,
                    'red':4,
                    'nir':5,
                    'swir1':6,
                    'swir2':7,
                    'panchromatic':8,
                    'cirrus':9,
                    'tirs1':10,
                    'tirs2':11})

    #This method decides the satellite sensor, depending on the number of bands
    def sensor(self):
        try:
            if (self.nbands == 7):
                return('Landsat - 4/5  TM')
            elif (self.nbands == 8):
                return('Landsat - 7')
            elif (self.nbands) == 11:
                return('Landsat - 8')
            elif (self.nbands) == 1:
                return('Panchromatic data')   
        except:
            print('Warning! Input data has no match in the inventory')        
        
    #This method returns the NDVI of the input file
    def ndvi(self):
        try:
            self.redband = self.getband(self.bandIndex['red'])
            self.nirband = self.getband(self.bandIndex['nir'])
            self.ndviband = ((self.nirband-self.redband)/(self.nirband+self.redband))
        except KeyError:
            print('ERROR! One of the required band was not found.')
        self.redband = None
        self.nirband = None
        return(self.ndviband)

def radioCorrection(band, maxVal=255):
    band = np.nan_to_num(band)
    return((band-band.min())/(band.max()-band.min())*maxVal)

#This method shows the band using matplotlib
def display(band, maptitle = 'Pyrsgis Raster', cmap='PRGn'):
    plt.title(maptitle, fontsize=20)
    legend = cm.ScalarMappable(cmap=cmap)
    legend.set_array(np.array([band.min(), band.min()+band.max()/2, band.max()]))
    plt.colorbar(legend)
    plt.imshow(band, cmap=cmap)
    try:
        scalebar = ScaleBar(30)
    except:
        raise ModuleNotFoundError("Please install matplotlib_scalebar library to use this feature.")
    plt.gca().add_artist(scalebar)
    plt.show()
