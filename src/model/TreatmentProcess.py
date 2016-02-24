#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


import numpy as np #Fundamental package for scientific computing
from math import sqrt

# GLOBAL METHODE ------------------------------------------------------------------------------------------------------------#

def limitValues(ndarray):
	""" To know limits of color values
		> the number of bits/color (dtype) of the file determines the number of nuances by colors
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
		           np.int32: ((-2147483648, 2147483647)),
		           np.int64: (-9223372036854775808, 9223372036854775807)}



# DENOISING -----------------------------------------------------------------------------------------------------------------#



# CONTRAST ------------------------------------------------------------------------------------------------------------------#

def logCorrect(ndarray, gain=1):
	""" Logarithmic correction : Classic method to restrain the scale of dynamics. 
		> this processing allows a more global appreciation of the contents of the image by increasing the level of the low lights without distorting the high lights.    
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
	""" To change de luminosity """
	if gamma < 0:
		raise ValueError("Parameter gamma should be a non-negative real number.")
	vmin,vmax = limitValues(ndarray)
	scale = float(vmax-vmin)
	result = ndarray**gamma * scale**(1-gamma)
	return ndarray.dtype.type(result)



# SATURATION ----------------------------------------------------------------------------------------------------------------#

def saturationCorrect(ndarray,gain=0.5):
	""" To change the saturation of an RGB color thank to the HSP color system. The "change" parameter works like this:
		0.0 creates a black-and-white image.
		0.5 reduces the color saturation by half.
		1.0 causes no change.
		2.0 doubles the color saturation. 
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



# ASTRO-TREATMENT ------------------------------------------------------------------------------------------------------------#

def deletionGreenDominant(ndarray, loss=10):
	""" To delet the green dominant """
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


def deletionLightPollution(ndarray):
	pass











#---------- TESTS -------------#

if __name__ == '__main__':
    import imageio
    from ImageRaw import ImageRaw
    path = '../../Pictures_test/'
    raw = ImageRaw(path + 'DSC_6027.NEF')
    ndarray = raw.getndarray()
    imageio.imsave('../../Pictures_test/testImageNEF.tiff', ndarray)
    ndarray1 = logCorrect(ndarray)
    imageio.imsave('../../Pictures_test/testlogCorrect.tiff', ndarray1)
    ndarray2 = gammaCorrect(ndarray)
    imageio.imsave('../../Pictures_test/testgammaCorrect.tiff', ndarray2)
    ndarray3 = luminosityCorrect(ndarray)
    imageio.imsave('../../Pictures_test/testluminosityCorrect.tiff', ndarray3)
    ndarray4 = saturationCorrect(ndarray)
    imageio.imsave('../../Pictures_test/testsaturationCorrect.tiff', ndarray4)
    ndarray5 = deletionGreenDominant(ndarray)
    imageio.imsave('../../Pictures_test/testdeletionGreenDominant.tiff', ndarray5)

#------------------------------#













