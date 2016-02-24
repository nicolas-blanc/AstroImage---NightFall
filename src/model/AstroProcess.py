#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import numpy as np


# GENERAL METHODE ------------------------------------------------------------------------------------------------------------#

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
	dark = median(ndarray_list)
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
	lights = list(ndarray_list)
	length = len(lights)
	for i in range(lenght):
		lights[i] = np.true_divide(np.subtract(lights[i], ndarray_masterDark), ndarray_masterFlat)






