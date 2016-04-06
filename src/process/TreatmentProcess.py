#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np #Fundamental package for scientific computing
from math import sqrt
import colorsys


# GLOBAL METHODE ------------------------------------------------------------------------------------------------------------#

def limitValues(ndarray):
	""" To know limits of color values
		> the number of bits/color (dtype) of the file determines the number of nuances by colors

		Parameters :
	     - ndarray : ndarray of image.
	"""
	vmin, vmax = dtype_limitValues[ndarray.dtype.type]
	return vmin,vmax

dtype_limitValues = {np.uint8: (0, 255),
		           np.uint16: (0, 65535),
		           np.uint32: (0, 4294967295),
		           np.uint64: (0, 18446744073709551615),
		           # Useless ?!? :
				   np.int8: (-128, 127),
		           np.int16: (-32768, 32767),
		           np.int32: (-2147483648, 2147483647),
		           np.int64: (-9223372036854775808, 9223372036854775807)}


def previsualisation(ndarray):
	""" To see the previsualisation of a treatment

	Parameters :
	 - ndarray : ndarray of image.
	 """
	pass


# CONVERT FUNCTION ------------------------------------------------------------------------------------------------------------#


def rgb2gray(rgbArray):
	""" Convert a rgb image into a gray image

	Parameters :
	- ndarray rgb

	returns :
	- ndarray gray
	"""
	r, g, b = rgbArray[:,:,0], rgbArray[:,:,1], rgbArray[:,:,2]
	gray = rgbArray.dtype.type(0.2989 * r + 0.5870 * g + 0.1140 * b)
	print(gray)
	return gray


def rgb_to_hls(ndarray):
	""" Convert the color from RGB coordinates to HLS coordinates.

	Parameters :
	 - ndarray rgb

	Returns :
	 - 3D ndarray where the 3th dimension is : 0 hue, 1 saturation, 2 value
	 """
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


def hls_to_rgb(ndarray):
	""" Convert the color from HLS coordinates to RGB coordinates.

	Parameters :
	 - ndarray hls

	returns :
	 - ndarray rgb
	 """
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


def rgb_to_hsv(ndarray):
	""" Convert the color from RGB coordinates to HSV coordinates.

	Parameters :
	 - ndarray rgb

	returns :
	 - ndarray hsv
	 """
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


def hsv_to_rgb(ndarray):
	""" Convert the color from HSV coordinates to RGB coordinates.

	Parameters :
	 - ndarray hsv

	returns :
	 - ndarray rgb
	 """
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


# DENOISING -----------------------------------------------------------------------------------------------------------------#

def medianFilter(ndarray):
	""" Median Filter : Easy and effective method to remove a part of the noise on an image

	Parameters :
	 - ndarray rgb

	returns :
	 - ndarray rgb
	"""
	medfilter = np.zeros((9))
	h,l,r=ndarray.shape
	t=np.copy(ndarray)
	for i in range(1,h-1):
	    for j in range(1,l-1):
	    	for k in range(r):
		       	medfilter[0] = t[i-1][j-1][k]
		       	medfilter[1] = t[i-1][j][k]
		       	medfilter[2] = t[i-1][j+1][k]
		       	medfilter[3] = t[i][j-1][k]
		       	medfilter[4] = t[i][j][k]
		       	medfilter[5] = t[i][j+1][k]
		       	medfilter[6] = t[i+1][j-1][k]
		       	medfilter[7] = t[i+1][j][k]
		       	medfilter[8] = t[i+1][j+1][k]
		       	median = np.median(medfilter, axis=None)
		       	t[i][j][k] = median
	return t



# CONTRAST ------------------------------------------------------------------------------------------------------------------#

def logCorrect(ndarray, gain=1):
	""" Logarithmic correction : Classic method to restrain the scale of dynamics.
		> this processing allows a more global appreciation of the contents of the image by increasing the level of the low lights without distorting the high lights.

		Parameters :
		 - ndarray rgb
		 - gain

		returns :
		 - ndarray rgb
	"""
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


def gammaCorrect(ndarray, gamma=1, gain=1):
	""" Gamma correction : Classic method which acts on light and contrast
		> clears up the image and reveals details because the dark and clear tones are little modified while middletones are it more.

		Parameters :
		 - ndarray rgb
		 - gamma
		 - gain

		returns :
		 - ndarray rgb
	"""
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



# LUMINOSITY ----------------------------------------------------------------------------------------------------------------#

def luminosityCorrect(ndarray, gamma=1):
	""" To change luminosity

	Parameters :
	 - ndarray rgb
	 - gamma

	returns :
	 - ndarray rgb
	 """
	if gamma < 0:
		raise ValueError("Parameter gamma should be a non-negative real number.")
	vmin,vmax = limitValues(ndarray)
	scale = float(vmax-vmin)
	result = ndarray**gamma * scale**(1-gamma)
	return ndarray.dtype.type(result)



# SATURATION ----------------------------------------------------------------------------------------------------------------#

def saturationCorrect(ndarray,gain=0.5):
	""" To change saturation of an RGB color thank to the HSP color system.

	Parameters :
	 - ndarray rgb
	 - gain :
		0.0 creates a black-and-white image.
		0.5 reduces the color saturation by half.
		1.0 causes no change.
		2.0 doubles the color saturation.

	returns :
	 - ndarray rgb
	"""
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


# WHITE BALANCE --------------------------------------------------------------------------------------------------------------#

def Histogram(ndarray):
	"""	Return histogram of ndarray with the centers of bins
	/!\ For color ndarrays, the function should be used separately on each channel to obtain a histogram for each color channel.

	Parameters :
	ndarray : ndarray rgb of the input ndarray

	Returns :
	hist : ndarray with all values of the histogram.
	bin_centers : ndarray with the center of the bins
	"""
	vmin,vmax = limitValues(ndarray)
	nbins = vmax+1 # Number of bins used to calculate histogram = number of values color
	h,l = ndarray.shape
	hist,bin_edges = np.histogram(ndarray.flatten(),bins=nbins,normed=True) # For color ndarrays, the function should be used separately on each channel to obtain a histogram for each color channel
	bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
	return hist, bin_centers


# Ref: http://en.wikipedia.org/wiki/Histogram_equalization
def EqualizeHistogram(ndarray):
	""" Return ndarray after histogram equalization :
		1) Get image histogram
		2) Calcul cumulative distribution function
		3) Normalize
		4) Linear interpolation of cdf

	Parameters :
	ndarray rgb

	Returns
	ndarray after histogram equalization.
	"""
	hist, bin_centers = Histogram(ndarray) # 1) Histogram of the the input ndarray
	cdf = hist.cumsum() # 2) Calcul the cumulative sum of the elements along a given axis.
	vmin,vmax = limitValues(ndarray)
	cdf = vmax*cdf / cdf[-1] #3) Normalize the cumulative sum
	result = np.interp(ndarray.flatten(), bin_centers, cdf) # 4) Linear Interpolation
	return result.reshape(ndarray.shape)






# ASTRO-TREATMENT ------------------------------------------------------------------------------------------------------------#

def deletionGreenDominant(ndarray, loss=10):
	""" To delet the green dominant

	Parameters :
	 - ndarray rgb
	 - loss

	returns :
	 - ndarray rgb
	 """
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
	return t


def deletionLightPollution(ndarray):
	# EqualizeHistogram ????
	pass
