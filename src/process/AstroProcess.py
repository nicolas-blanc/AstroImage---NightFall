#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import numpy as np
from math import sqrt

# INFO : 
# http://astro.dialou.fr/techniques/astrophotographie/capture-des-images-de-calibration/
# http://www.astrosurf.com/d_bergeron/astronomie/Bibliotheque/Traitement%20image/Pretraitement%20des%20images/traitement%20image.htm#Images%20DARK


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
	""" Create a sigma reject array from all array, i.e calcul the sigma reject for each pixel.
		> More the number of ndarray is, more the sigma reject will be precise !
		> All ndarray must have same dimensions !
	"""
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



# AVERAGE : only for BIAS !

def average(ndarray_list):
	""" Create a average array from all array, i.e calcul the average for each pixel.
		> More the number of ndarray is, more the average will be precise !
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
                   	t[i][j][k] = np.average(liste)
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

def processMasterDark(ndarray_list) :
	""" The MASTERDARK image will serve to remove the thermal noise and random noise on our LIGHT image
		> without MASTERBIAS
	"""
	# 1) Create a sigma reject array from all of them, entry-by-entry.
	masterdark = sigmaReject(ndarray_list)
	return masterdark


def processMasterDarkWithBias(ndarray_list, ndarray_masterBias) :
	""" The MASTERDARK image will serve to remove the thermal noise and random noise on our LIGHT image
		> with MASTERBIAS
	"""
	# 1) Subtract the master bias frame
	darks = list(ndarray_list)
	lenght = len(darks)
	h,l,r = darks[0].shape
    for i in range(lenght):
    	darks[i] = np.subtract(darks[i], ndarray_masterBias)
	# 2) Create a sigma reject array from all of them, entry-by-entry.
	masterdark = sigmaReject(darks)
	return masterdark


def processMasterDarkFlat(ndarray_list, ndarray_masterBias) :
	""" The MASTER DARK FLAT image will serve to calcul the MASTER FLAT FIELD WITH BIAS
	"""
	# 1) Subtract the master bias frame
	darkflats = list(ndarray_list)
	lenght = len(darkflats)
	h,l,r = darkflats[0].shape
    for i in range(lenght):
    	darkflats[i] = np.subtract(darkflats[i], ndarray_masterBias)
	# 2) Create a sigma reject array from all of them, entry-by-entry.
	masterdarkflat = sigmaReject(darkflats)
	return masterdarkflat


# MASTER FLAT ---------------------------------------------------------------------------------------------------------------#

# Flats are images portraying the sensitivity of individual pixels in the frame, which is illuminated uniformly

def processMasterFlat(ndarray_list, ndarray_masterDark) :
	""" The MASTERFLAT image will serve to remove all track of dusts, gradient, vignetting on our LIGHT image
		> Without MASTERBIAS
	"""
	# 1) Subtract the master dark frame
	flats = list(ndarray_list)
	lenght = len(flats)
	h,l,r = flats[0].shape
    for i in range(lenght):
    	flats[i] = np.subtract(flats[i], ndarray_masterDark)
	# 2) Normalize all frame
	flats = normalize(flats)
	# 3) Create a median array from all of them, entry-by-entry.
	masterflat = median(flats)
	return masterflat


def processMasterFlatWithBias(ndarray_list, ndarray_masterDarkFlat, ndarray_masterBias) :
	""" The MASTERFLAT image will serve to remove all track of dusts, gradient, vignetting on our LIGHT image
		> With MASTERBIAS & MasterDarkFlat
	"""
	# 1) Subtract the MasterBias and the MasterDarkFlat
	flats = list(ndarray_list)
	lenght = len(flats)
	h,l,r = flats[0].shape
    for i in range(lenght):
    	flats[i] = np.subtract(flats[i], ndarray_masterBias)
    	flats[i] = np.subtract(flats[i], ndarray_masterDarkFlat)
	# 2) Normalize all frame
	flats = normalize(flats)
	# 3) Create a median array from all of them, entry-by-entry.
	masterflat = median(flats)
	return masterflat


# MASTER BIAS ---------------------------------------------------------------------------------------------------------------#

# If you take your series of images DARK with same parameters (the same exposure time, same binning, same temperature) as the LIGHT images and for your images of FLAT FIELD, you will not need to set of images of BIAS.
# CAREFUL : OVERALL BY AVERAGE only !
def processMasterBias(ndarray_list) :
	""" The MASTERBIAS image will serve to remove the initial exposure level of pixels in our LIGHT
		> If you take your series of images DARK with same parameters (the same exposure time, same binning, same temperature) as the LIGHT images and for your images of FLAT FIELD, you will not need to set of images of BIAS.
	"""
	# 1) Create an average array from all of them, entry-by-entry.
	masterbias = average(ndarray_list)
	return masterbias


# LIGHT ----------------------------------------------------------------------------------------------------------------------#

# We will use master flat and dark field to clean up each light frame, which contains data about the night sky : (Light-Dark)/Flat

def calibration(ndarray_list, ndarray_masterDark, ndarray_masterFlat):
	""" The final result will be a perfectly corrected LIGHT image
		> without BIAS
	"""
	lights_list = list(ndarray_list)
	length = len(lights_list)
	# Use masterflat and masterdark to clean up each light frame
	for i in range(lenght):
		lights_list[i] = np.true_divide(np.subtract(lights_list[i], ndarray_masterDark), ndarray_masterFlat)
	# Normalize each light frame
	lights_list = normalize(lights_list)
	return lights_list


def calibrationWithBias(ndarray_list, ndarray_masterDark, ndarray_masterFlat, ndarray_masterBias):
	""" The final result will be a perfectly corrected LIGHT image
		> with BIAS
	"""
	lights_list = list(ndarray_list)
	length = len(lights_list)
	# Use masterflat, masterdark and masterbias to clean up each light frame
	for i in range(lenght):
		lights_list[i] = np.subtract(lights_list[i], ndarray_masterBias)
		lights_list[i] = np.true_divide(np.subtract(lights_list[i], ndarray_masterDark), ndarray_masterFlat)
	# Normalize each light frame
	lights_list = normalize(lights_list)
	return lights_list


def registration(ndarray_list):
	""" To overlap LIGHT image (after the calibration) """
	pass





