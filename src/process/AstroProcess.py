#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import numpy as np
from math import sqrt




# GENERAL METHODE ------------------------------------------------------------------------------------------------------------#

# MEDIAN : the median combination allow to eliminates pixels deviants. It is the one that we shall usually use to combine Flat field (remove completely any tracks of artéfacts)
# so this combination eliminates space rays, tracks of satellites, travel of asteroids, etc. 
# but we obtain a MASTERDARK with a S/N of the order of 25 % a 30 %

def median(ndarray_list):
	""" Create a median array from all array, i.e calcul the median for each pixel.
		> More the number of ndarray is, more the median will be precise !
		> All ndarray must have same dimensions !
	"""
    if len(ndarray_list) == 1:
    	# Shouldn't happen ...
        return ndarray_list
    else:
    	# Initialise the median array at dimensions of frame
        t = np.copy(frame_list[0])
        # Fills the median array
        h,l,r = ndarray_list[0].shape
        lenght = len(ndarray_list)
		for i in range(h):
			for j in range(l):
				for k in range(r):
					liste = []
					for frame in range(lenght):
						liste.append(ndarray_list[frame][i][j][k])
                   	t[i][j][k] = np.median(liste)
        return t


# SIGMA-CLIP (SIGMA REJECT) : Better than the median. It is the one that we shall usually use to combine the LIGHT images, DARK, FLAT FIELD and DARK FOR FLAT FIELD.
# 1) From the set of corresponding pixel values from each source image, compute the mean (average) and standard deviation of these values.
# 2) Compute a new mean, omitting pixels from the above set that fall further away than threshold standard deviations from the mean. Use this new mean as the output value for this pixel location.
# 3) Repeat steps 1-2 for every pixel in the final image.

def sigmaReject(ndarray_list):
	""" """
    if len(ndarray_list) == 1:
    	# Shouldn't happen ...
        return ndarray_list
    else:
    	# Initialise the sigmaReject array at dimensions of frame
        t = np.copy(frame_list[0])
        # Fills the sigmaReject array
        h,l,r = ndarray_list[0].shape
        lenght = len(ndarray_list)
		for i in range(h):
			for j in range(l):
				for k in range(r):
					# from the set of corresponding pixel values from each source image, compute the average
					liste = []
					for frame in range(lenght):
						liste.append(ndarray_list[frame][i][j][k])
                   	mean = np.mean(liste)
                   	# Find standard deviation of these values
                   	variance = 0
                   	for frame in range(lenght):
                   		variance = variance + (ndarray_list[frame][i][j][k]-mean)**2
                   	variance = variance/lenght
                   	ecart_type = sqrt(variance)
                   	# Compute a new mean, omitting pixels from the above set that fall further away than threshold standard deviations from the mean.
					sigmaClip = []
					for frame in range(lenght):
						if (ndarray_list[frame][i][j][k] <= ecart_type):
							sigmaClip.append(ndarray_list[frame][i][j][k])
                   	t[i][j][k] = np.mean(sigmaClip)
        return t



# The normalization consists in putting pixels in the same intensity before being combined

def normalize(ndarray_list):
    """ Normalize each ndarray and scale all
    """   
    t = list(ndarray_list)
    liste = []
    lenght = len(t)
    # 1) Normalize each flat field, i.e. divide it by its mean entry value
    for i in range(lenght):
        mean = np.mean(t[i]) # Find the mean of the ndarray
        liste.append(mean)
        t[i] = np.divide(t[i], mean) # Divide ndarray by its mean, normalizing it
    # 2) Scale all of the fields’ means so that their individual averages are equal to one another
    meantotal = sum(liste) / len(liste)  # Find the mean of the total set of ndarray_list
    for i in range(lenght):
        t[i] = np.multiply(t[i], np.divide(meantotal, np.mean(t[i]))) # Divide 
    return t



# MASTER DARK ---------------------------------------------------------------------------------------------------------------#

# Dark fields capture the noise inherent to the CCD array, which we would like to eliminate so the sensor doesn’t contaminate the light we’re collecting from the night sky

def ProcessMasterDark(ndarray_list) :
	# 1) Create a median array from all of them, entry-by-entry.
	dark = sigmaReject(ndarray_list)
	return dark



# MASTER FLAT ---------------------------------------------------------------------------------------------------------------#

# Flats are images portraying the sensitivity of individual pixels in the frame, which is illuminated uniformly

def ProcessMasterFlat(ndarray_list, ndarray_masterDark) :
	# 1) Subtract the master dark frame
	flat = list(ndarray_list)
	lenght = len(flat)
	h,l,r = t[0].shape
    for i in range(lenght):
    	flat[i] = np.subtract(flat[i], ndarray_masterDark)
	# 2) Normalize all frame
	flat = normalize(t)
	# 3) Create a median array from all of them, entry-by-entry.
	falt = median(flat)
	return flat



# LIGHT ----------------------------------------------------------------------------------------------------------------------#

# We will use master flat and dark field to clean up each light frame, which contains data about the night sky : (Light-Dark)/Flat

def Calibration(ndarray_list, ndarray_masterDark, ndarray_masterFlat):
	lights_list = list(ndarray_list)
	length = len(lights_list)
	# Use masterflat and masterdark to clean up each light frame
	for i in range(lenght):
		lights_list[i] = np.true_divide(np.subtract(lights_list[i], ndarray_masterDark), ndarray_masterFlat)
	# Normalize each light frame
	lights_list = normalize(lights_list)
	return lights_list







