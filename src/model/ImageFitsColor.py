#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Image #Heritage
import pyfits
import numpy as np


# The FITS format is the most popular way to save and interchange astronomical data. The files are organized in units each of which contains a human readable header and a data. This structure is refereed as HDUs (Header/DATA Unit).
# http://python-astro.blogspot.fr/2012/03/play-with-fits-files.html

def readFITS(path):
    """ Opening FITS files and loading the image data """
    path = path
    hdu_list = pyfits.open(path, uint=True, do_not_scale_image_data=False) # returns an object called an HDUList which is a list-like collection of HDU objects.
    image_data = hdu_list[0].data # hdulist[0] is the primary HDU, hdulist[1] is the first extension HDU, etc. The data attribute of the HDU object will return a numpy ndarray object.
    hdu_list.close() # the headers will still be accessible after the HDUList is closed
    return (hdu_list, image_data)


class ImageFitsColor(Image.Image):
    """docstring for ImageFitsColor"""
    def __init__(self, fitsPath_red, fitsPath_green, fitsPath_blue):
        """ Convert separate FITS images (RGB) to 3-color array (ndarray)
            Need fitsPathRed, fitsPathGreen, fitsPathBlue : each file is inside a folder give by the path
        """
        # Load FITS images (RGB) and convert to 3-color array (ndarray)
        self._hdulistRed, dataRed = readFITS(fitsPath_red)
        self._hdulistGreen, dataGreen = readFITS(fitsPath_green)
        self._hdulistBlue, dataBlue = readFITS(fitsPath_blue)
        height,width = dataGreen.shape
        size = (height,width)
        self._dataType = dataGreen.dtype.name
        ##print('')
        ##print('DATATYPE')
        ##print(self._dataType)
        rgbArray = np.empty(shape=(height,width,3),dtype=self._dataType)
        rgbArray[:,:,0] = dataRed 
        rgbArray[:,:,1] = dataGreen
        rgbArray[:,:,2] = dataBlue
        ##print('ConvertFIFTS')
        ##print(rgbArray[:,:,0])
        ndarray = rgbArray
        # SuperClass Constructor
        super(ImageFitsColor,self).__init__(path,ndarray,size)


    def gethdulist(self):
        """ Return the HDUlist of ImageFitsColor"""
        return (self._hdulistRed, self._hdulistGreen, self.hdulistBlue)

    def getDataType(self):
        """ Return data type of ImageFitsColor """
        return self._file




#---------- TESTS -------------#

if __name__ == '__main__':
    import imageio
    path = '../../Pictures_test/'
    fits = ImageFitsColor(path+'test_red.fits',path+'test_green.fits',path+'test_blue.fits')
    imageio.imsave('../../Pictures_test/testImageFITS.tiff', fits.getndarray())

#------------------------------#

