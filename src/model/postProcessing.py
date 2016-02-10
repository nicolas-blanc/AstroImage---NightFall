#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
  
from __future__ import unicode_literals




#------------------------------- LOAD RAW IMAGE -----------------------------------#

import rawpy #Python wrapper for the LibRaw library (raw image decoder)
from rawpy import ColorSpace
from rawpy import DemosaicAlgorithm


# Load a RAW file 
def loadRaw(path) :
	return rawpy.imread(path)


# Postprocess this file to obtain a numpy ndarray of shape (h,w,c)
# 16 bits => la palette de couleur peut contenir 2^16 = 65536 couleurs 
def debayeurization(file) :
	return file.postprocess(output_bps=16, output_color=ColorSpace.sRGB, demosaic_algorithm=DemosaicAlgorithm.AAHD, use_camera_wb=True,no_auto_bright=True)


# To get back the size of the image
def getSize(file) :
	print(file.sizes)
	raw_height, raw_width, height, width, top_margin, left_margin, iheight, iwidth, pixel_aspect, flip= file.size
	return (height,width)


#---------- TESTS -------------#

import imageio

path = 'DSC_0599.NEF'
file = loadRaw(path)
array = debayeurization(file)
imageio.imsave('testFITS.tiff', array)





#---------------------------- LOAD AND STORE FITS IMAGE ---------------------------#

# The FITS format is the most popular way to save and interchange astronomical data. The files are organized in units each of which contains a human readable header and a data. This structure is refereed as HDUs (Header/DATA Unit).
# http://python-astro.blogspot.fr/2012/03/play-with-fits-files.html

import pyfits
import numpy as np

# Opening FITS files and loading the image data
def readFITS(path):
	path = path
	hdu_list = pyfits.open(path, uint=True, do_not_scale_image_data=False) # returns an object called an HDUList which is a list-like collection of HDU objects.
	image_data = hdu_list[0].data # hdulist[0] is the primary HDU, hdulist[1] is the first extension HDU, etc. The data attribute of the HDU object will return a numpy ndarray object.
	hdu_list.close() # the headers will still be accessible after the HDUList is closed
	return (hdu_list, image_data)

#hdu,image_data_red, image_data_green, image_data_blue = readFITS('M13_blue_0001.fits')
#print(hdu.info())


# Convert separate FITS images (RGB) to 3-color array (nparray)
def ConvertFITS(fitsPath_red, fitsPath_green, fitsPath_blue):
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
def ConvertToFITS(rgbArray, fitsName, LATOBS='Not informed', LONGOBS='Not informed') :
	
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



#-------------------------- PRE-PROCESSING --------------------------------------#







#-------------------------- POST-PROCESSING -------------------------------------#

import numpy as np #Fundamental package for scientific computing
import imageio

from PIL import Image #importation du sous-module Image du module PIL
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors
from math import sqrt


# To know limits of color values
# -> the number of bits/color (dtype) of the file determines the number of nuances by colors
def limitValues(ndarray):
	vmin, vmax = dtype_limitValues[ndarray.dtype.type]
	return vmin,vmax

dtype_limitValues = {np.uint8: (0, 255),
		           np.uint16: (0, 65535),
		           np.uint32: (0, 4294967295),
		           np.uint64: (0, 18446744073709551615),
		           # Useless ?!? :
				   np.int8: (-128, 127),
		           np.int16: (-32768, 32767),
		           np.int32: ((-2147483648, 2147483647)),
		           np.int64: (-9223372036854775808, 9223372036854775807)}


# Logarithmic correction : Classic method to restrain the scale of dynamics. 
# -> this processing allows a more global appreciation of the contents of the image by increasing the level of the low lights without distorting the high lights.    
def logCorrect(ndarray, gain=1):
    vmin,vmax = limitValues(ndarray)
    scale = float(vmax-vmin)
    #result = scale * gain * np.log2(1 + ndarray/scale)
    h,l,r=ndarray.shape
    t=np.copy(ndarray)
    for i in range(h):
		for j in range(l):
			for k in range(r):
				temp = scale * gain * np.log2(1 + t[i][j][k]/scale)
				if(temp < vmin):
					t[i][j][k] = vmin
				elif(temp > vmax) :
					t[i][j][k] = vmax
				else :
					t[i][j][k] = temp
    return t #ndarray.dtype.type(result)


# Gamma correction : Classic method which acts on light and contrast
# -> clears up the image and reveals details because the dark and clear tones are little modified while middletones are it more.
def gammaCorrect(ndarray, gamma=1, gain=1):
	if gamma < 0:
		raise ValueError("Parameter gamma should be a non-negative real number.")
	vmin,vmax = limitValues(ndarray)
	scale = float(vmax-vmin)
	#result = ((ndarray / scale) ** gamma) * scale * gain
	h,l,r=ndarray.shape
	t=np.copy(ndarray)
	for i in range(h):
		for j in range(l):
			for k in range(r):
				temp = ((t[i][j][k]/ scale) ** gamma) * scale * gain
				if(temp < vmin):
					t[i][j][k] = vmin
				elif(temp > vmax) :
					t[i][j][k] = vmax
				else :
					t[i][j][k] = temp
	return t #ndarray.dtype.type(result)


# Luminosity correction : 
def luminosityCorrect(ndarray, gamma=1):
	if gamma < 0:
		raise ValueError("Parameter gamma should be a non-negative real number.")
	vmin,vmax = limitValues(ndarray)
	scale = float(vmax-vmin)
	result = ndarray**gamma * scale**(1-gamma)
	return ndarray.dtype.type(result)


# Deletion of Green Dominant
def deletionGreenDominant(ndarray, loss=10):
	vmin,vmax = limitValues(ndarray)
	h,l,r=ndarray.shape
	t=np.copy(ndarray)
	for i in range(h):
		for j in range(l):
			temp = t[i][j][1] - loss
			if(temp < vmin):
				t[i][j][1] = vmin
			elif(temp > vmax) :
				t[i][j][1] = vmax
			else :
				t[i][j][1] = temp
            #t[i][j][0]=0
            #t[i][j][2]=0
	return t


# Convert a rgb image into a gray image
def rgb2gray(rgbArray):
    r, g, b = rgbArray[:,:,0], rgbArray[:,:,1], rgbArray[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    print(gray)
    return gray


# To change the saturation of an RGB color thank to the HSP color system. The "change" parameter works like this:
#    0.0 creates a black-and-white image.
#    0.5 reduces the color saturation by half.
#    1.0 causes no change.
#    2.0 doubles the color saturation.
def saturationCorrect(ndarray,gain):
	Pr = 0.2989
	Pg = 0.5870
	Pb = 0.1140
	vmin,vmax = limitValues(ndarray)
	h,l,r=ndarray.shape
	t=np.copy(ndarray)
	for i in range(h):
		for j in range(l):
			P = sqrt( float(t[i][j][0])*float(t[i][j][0])*Pr + float(t[i][j][1])*float(t[i][j][1])*Pg + float(t[i][j][2])*float(t[i][j][2])*Pb )
			for k in xrange(r):
				temp = P+((t[i][j][k])-P)*gain
				if(temp < vmin):
					t[i][j][k] = vmin
				elif(temp > vmax) :
					t[i][j][k] = vmax
				else :
					t[i][j][k] = temp
	return t
 


#---------- TESTS -------------#

#path = 'DSC_0599.NEF'
#file = loadRaw(path)
#array = debayeurization(file)
#array = deletionGreenDominant(array)
#print(array.dtype.type)
#imageio.imsave('default.tiff', array)



#im=Image.open("lena.png") #ouverture d'une image au format png dans Python.
#tab=np.array(im)

#result = rgb_to_hls(tab)
#image = Image.fromarray(result)
#image.show()
























#-------- Convert function -------------#

import colorsys
import numpy as np

# Convert the color from RGB coordinates to HLS coordinates.
# -> return a 3D nparray where the 3th dimension is : 0 hue, 1 saturation, 2 value
def rgb_to_hls(ndarray):
	h,l,r=ndarray.shape
	t=np.copy(ndarray)
	for i in range(h):
		for j in range(l):
			red = t[i][j][0]
			green = t[i][j][1]
			blue = t[i][j][2]
			hue,lightness,saturation = colorsys.rgb_to_hls(red, green, blue)
			t[i][j][0] = hue
			t[i][j][1] = lightness
			t[i][j][2] = saturation
	return t

# Convert the color from HLS coordinates to RGB coordinates.
def hls_to_rgb(ndarray):
	h,l,r=ndarray.shape
	t=np.copy(ndarray)
	for i in range(h):
		for j in range(l):
			hue = t[i][j][0]
			lightness = t[i][j][1]
			saturation = t[i][j][2]
			red,green,blue = colorsys.hls_to_rgb(hue, lightness, saturation)
			t[i][j][0] = red
			t[i][j][1] = green
			t[i][j][2] = blue
	return t

# Convert the color from RGB coordinates to HSV coordinates.
def rgb_to_hsv(ndarray):
	h,l,r=ndarray.shape
	t=np.copy(ndarray)
	for i in range(h):
		for j in range(l):
			red = t[i][j][0]
			green = t[i][j][1]
			blue = t[i][j][2]
			hue,saturation,value = colorsys.rgb_to_hls(red, green, blue)
			t[i][j][0] = hue
			t[i][j][1] = saturation
			t[i][j][2] = value
	return t

# Convert the color from HSV coordinates to RGB coordinates.
def hsv_to_rgb(ndarray):
	h,l,r=ndarray.shape
	t=np.copy(ndarray)
	for i in range(h):
		for j in range(l):
			hue = t[i][j][0]
			saturation = t[i][j][1]
			value = t[i][j][2]
			red,green,blue = colorsys.hsv_to_rgb(hue, saturation, value)
			t[i][j][0] = red
			t[i][j][1] = green
			t[i][j][2] = blue
	return t

    








