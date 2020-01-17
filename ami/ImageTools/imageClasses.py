import gdal
import numpy as np
from matplotlib import cm
import matplotlib.colors as colors
import matplotlib.colorbar as cbar
import matplotlib.pyplot as plt
import os
from datetime import datetime as dt
from PIL import Image
import ImageTools.index_generator as ig

class GeoreferencedImage():
"""
Abstract class for georeferenced images
This class is currently under construction and does not do anything yet.
It will have child classes MultiBandImage and SingleBandImage
"""
    def __init__(self, **kwargs):
        if 'filepath' in kwargs:
            pass
        elif 'bands' in kwargs:
            pass
        elif 'copy' in kwargs:
            pass
        
        if 'output_directory' in kwargs.keys():
            pass
        if 'output_base' in kwargs.keys():
            pass
        self._bands = kwargs['bands']
        self.kwargs = kwargs

    def export(self, filename):
        pass
    
    def resize(self, resize_factor, copy=False):
        pass
    
    def saveGeoTiff(self, bands, filepath, dtype, options, **kwargs):  # bands is list of np arrays or a 3d np array
        num_bands = len(bands)
        driver = gdal.GetDriverByName('GTiff')
        shape = bands[0].shape[::-1]
        file = driver.Create(filepath, shape[0], shape[1], num_bands, dtype, options=options)
        if num_bands > 1:
            for band, i in zip(bands, range(1, num_bands+1)):
                file.GetRasterBand(i).WriteArray(band)
        elif 'index' in kwargs.keys() and 'fill' in kwargs.keys() and kwargs['fill']:
            index = kwargs['index']
            data = np.ma.masked_outside(bands[0], ig.ranges[index][0], ig.ranges[index][1])
            file.GetRasterBand(1).WriteArray(data.filled(-10000))
        else:
            file.GetRasterBand(1).WriteArray(bands[0])  
            
        file.SetProjection(self._projection)
        file.SetGeoTransform(self._geo_transform)
        file.FlushCache()
        file = None
        return filepath
    
    def saveGeoPNG(self, bands, filepath, dtype, options, **kwargs):
        pass
    
class MultiBandImage(GeoreferencedImage):
    def __init__(self, bands, **kwargs)
        pass
    
    def export(self, filename):
        pass
    
    
class SingleBandImage(GeoreferencedImage):
    def __init__(self, band, **kwargs):
        pass
        
    def colormapToMultiBandImage(colormap):
        data = None
        return MultiBandImage(data, colormap=colormap)
        
    