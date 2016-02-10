#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import imageio
import rawpy #Python wrapper for the LibRaw library (raw image decoder)
from rawpy import ColorSpace
from rawpy import DemosaicAlgorithm

# The FITS format is the most popular way to save and interchange astronomical data. The files are organized in units each of which contains a human readable header and a data. This structure is refereed as HDUs (Header/DATA Unit).
# http://python-astro.blogspot.fr/2012/03/play-with-fits-files.html
import pyfits
import numpy as np



#-------------------- Image --------------------#
class Image(object):
    """docstring for Image"""
    def __init__(self, path):
        super(Image, self).__init__()
        self.path = path


    # To get back the size of the image
    def getSize(self):
    	return (self.height, self.width)


    def getFile(self):
        return self.file




#-------------------- ImageRaw --------------------#
class ImageRaw(Image):
    """docstring for ImageRaw"""
    def __init__(self, path):
        super(ImageRaw, self).__init__(path)
        # Load a RAW file
        self.file = rawpy.imread(path)
        # Erreur sur cette ligne, me dit que size n'existe pas
    	# self.raw_height, self.raw_width, self.height, self.width, self.top_margin, self.left_margin, self.iheight, self.iwidth, self.pixel_aspect, self.flip = self.file.size


    # Postprocess this file to obtain a numpy ndarray of shape (h,w,c)
    # 16 bits => la palette de couleur peut contenir 2^16 = 65536 couleurs
    def debayeurization(self):
    	self.img = self.file.postprocess(output_bps=16, output_color=ColorSpace.sRGB, demosaic_algorithm=DemosaicAlgorithm.AAHD, use_camera_wb=True,no_auto_bright=True)


    def getImageDebayeurization(self):
        return self.img



#-------------------- ImageFits --------------------#
class ImageFits(Image):
    """docstring for ImageFits"""
    def __init__(self, path):
        super(ImageFits, self).__init__(path)


    # Opening FITS files and loading the image data
    def readFITS(self, path):
    	path = path
    	hdu_list = pyfits.open(path, uint=True, do_not_scale_image_data=False) # returns an object called an HDUList which is a list-like collection of HDU objects.
    	image_data = hdu_list[0].data # hdulist[0] is the primary HDU, hdulist[1] is the first extension HDU, etc. The data attribute of the HDU object will return a numpy ndarray object.
    	hdu_list.close() # the headers will still be accessible after the HDUList is closed
    	return (hdu_list, image_data)

    #hdu,image_data_red, image_data_green, image_data_blue = readFITS('M13_blue_0001.fits')
    #print(hdu.info())


    # Convert separate FITS images (RGB) to 3-color array (nparray)
    def ConvertFITS(self, fitsPath_red, fitsPath_green, fitsPath_blue):
    	hdu_list_red, image_data_red = readFITS(fitsPath_red)
    	hdu_list_green, image_data_green = readFITS(fitsPath_green)
    	hdu_list_blue, image_data_blue = readFITS(fitsPath_blue)
    	height,width = image_data_red.shape
    	dataType = image_data_red.dtype.name
    	#print('')
    	#print('DATATYPE')
    	#print(dataType)
    	rgbArray = np.empty(shape=(height,width,3),dtype=dataType)
    	rgbArray[:,:,0] = image_data_red
    	rgbArray[:,:,1] = image_data_green
    	rgbArray[:,:,2] = image_data_blue
    	#print('ConvertFIFTS')
    	#print(rgbArray[:,:,0])
    	return rgbArray


    # Converting a 3-color array to separate FITS images
    def ConvertToFITS(self, rgbArray, fitsName, LATOBS='Not informed', LONGOBS='Not informed') :

    	npr = rgbArray[:,:,0]
    	#print("CONVERT TO FITS")
    	#print(npr)
    	npg = rgbArray[:,:,1]
    	npb = rgbArray[:,:,2]

    	red = pyfits.PrimaryHDU()
    	red.header['LATOBS'] = LATOBS
    	red.header['LONGOBS'] = LONGOBS
    	red.data = npr
    	#print("DATA LOAD")
    	#print(red.data)
    	red.writeto(fitsName+'_red.fits')

    	green = pyfits.PrimaryHDU()
    	green.header['LATOBS'] = LATOBS
    	green.header['LONGOBS'] = LONGOBS
    	green.data = npg
    	green.writeto(fitsName+'_green.fits')

    	blue = pyfits.PrimaryHDU()
    	blue.header['LATOBS'] = LATOBS
    	blue.header['LONGOBS'] = LONGOBS
    	blue.data = npb
    	blue.writeto(fitsName+'_blue.fits')



#---------- TESTS -------------#

#import imageio

#path = 'DSC_0599.NEF'
#file = loadRaw(path)
#array = debayeurization(file)

#ConvertToFITS(array,'test')
#rgbArray = ConvertFITS('test_red.fits', 'test_green.fits', 'test_blue.fits')
#imageio.imsave('testFITS.tiff', rgbArray)

if __name__ == '__main__':
    path = '../../Pictures_test/DSC_0599.NEF'
    iR1 = ImageRaw(path)
    iR1.debayeurization()
    imageio.imsave('../../Pictures_test/testFITS.tiff', iR1.getImageDebayeurization())
