#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from math import sqrt

import Registration as reg
import TreatmentProcess as tproc


# REFERENCES :
# http://astro.dialou.fr/techniques/astrophotographie/capture-des-images-de-calibration/
# http://www.astrosurf.com/d_bergeron/astronomie/Bibliotheque/Traitement%20image/Pretraitement%20des%20images/traitement%20image.htm#Images%20DARK



# GENERAL METHODE ------------------------------------------------------------------------------------------------------------#


# MEDIAN : the median combination allow to eliminates pixels deviants. It is the one that we shall usually use to combine Flat field or dark (remove completely any tracks of artéfacts)
# so this combination eliminates space rays, tracks of satellites, travel of asteroids, etc.
# but we obtain a MASTERDARK with a S/N of the order of 25 % a 30 %

def median(ndarray_list):
	""" Create a median array from all array, i.e calcul the median for each pixel.
		> More the number of ndarray is, more the median will be precise !
		> All ndarray must have same dimensions !

		Parameters :
	     - ndarray_list : ndarray list of images.

	     Return :
	     - ndarray : ndarray in which each pixel match to pixels median
	"""
    # The ndarray need to have the same size
	for i in range(1,len(ndarray_list)):
	    if ndarray_list[0].shape != ndarray_list[i].shape:
	        raise ValueError("Median Error : ndarray need to have the same size")

	if len(ndarray_list) == 1:
    	# Shouldn't happen ...
		return ndarray_list
   	else:
    	# Initialise the median array at dimensions of frame
		t = np.copy(ndarray_list[0])
        # Fills the median array
       	h,l,r = t.shape
       	lenght = len(ndarray_list)
       	for i in range(0,h-1):
			for j in range(0,l-1):
				for k in range(0,r-1):
					liste = np.zeros((lenght))
					for frame in range(0,lenght-1):
						liste[frame] = ndarray_list[frame][i][j][k]
       	           	t[i][j][k] = np.median(liste)
			print "Median : " + str(i) + "/" + str(h-2)
        return t


# SIGMA-CLIP (SIGMA REJECT) : Better than the median. It is the one that we shall usually use to combine the LIGHT images, DARK, FLAT FIELD and DARK FOR FLAT FIELD.
# 1) From the set of corresponding pixel values from each source image, compute the mean (average) and standard deviation of these values.
# 2) Compute a new mean, omitting pixels from the above set that fall further away than threshold standard deviations from the mean. Use this new mean as the output value for this pixel location.
# 3) Repeat steps 1-2 for every pixel in the final image.

def sigmaReject(ndarray_list):
	""" Create a sigma reject array from all array, i.e calcul the sigma reject for each pixel.
		> More the number of ndarray is, more the sigma reject will be precise !
		> All ndarray must have same dimensions !

		Parameters :
	     - ndarray_list : ndarray list of images.

	     Return :
	     - ndarray : ndarray in which each pixel match to pixels sigmaReject
	"""
    # The ndarray need to have the same size
	for i in range(1,len(ndarray_list)):
	    if ndarray_list[0].shape != ndarray_list[i].shape:
	        raise ValueError("SigmaReject Error : ndarray need to have the same size")

	if len(ndarray_list) == 1:
    	# Shouldn't happen ...
		return ndarray_list
	else:
    	# Initialise the sigmaReject array at dimensions of frame
		t = np.copy(ndarray_list[0])
        # Fills the sigmaReject array
		h,l,r = ndarray_list[0].shape
		lenght = len(ndarray_list)
		for i in range(0,h-1):
			print "SigmaReject : " + str(i) + "/" + str(h-2)
			for j in range(0,l-1):
				for k in range(0,r-1):
					# from the set of corresponding pixel values from each source image, compute the average
					liste = []
					for frame in range(0,lenght-1):
						liste.append(ndarray_list[frame][i][j][k])
                   	mean = np.mean(liste)
                   	# Find standard deviation of these values
                   	variance = 0
                   	for frame in range(0,lenght-1):
                   		variance = variance + (ndarray_list[frame][i][j][k]-mean)**2
                   	variance = variance/lenght
                   	ecart_type = sqrt(variance)
                   	# Compute a new mean, omitting pixels from the above set that fall further away than threshold standard deviations from the mean.
                   	sigmaClip = np.zeros((lenght))
                   	for frame in range(0,lenght-1):
                   		if (ndarray_list[frame][i][j][k] <= ecart_type):
                   			sigmaClip[frame] = ndarray_list[frame][i][j][k]
                   	mean = np.mean(sigmaClip)
                   	t[i][j][k] = mean
        return t



# AVERAGE : only for BIAS !

def average(ndarray_list):
	""" Create a average array from all array, i.e calcul the average for each pixel.
		> More the number of ndarray is, more the average will be precise !
		> All ndarray must have same dimensions !

		Parameters :
	     - ndarray_list : ndarray list of images.

	     Return :
	     - ndarray : ndarray in which each pixel match to pixels average
	"""
    # The ndarray need to have the same size
	for i in range(1,len(ndarray_list)):
	    if ndarray_list[0].shape != ndarray_list[i].shape:
	        raise ValueError("Average Error : ndarray need to have the same size")

	if len(ndarray_list) == 1:
    	# Shouldn't happen ...
		return ndarray_list
	else:
    	# Initialise the median array at dimensions of frame
		t = np.copy(ndarray_list[0])
        # Fills the median array
		h,l,r = t.shape
		lenght = len(ndarray_list)
		for i in range(0,h-1):
			for j in range(0,l-1):
				for k in range(0,r-1):
					liste = np.zeros((lenght))
					for frame in range(0,lenght-1):
						liste[frame] = ndarray_list[frame][i][j][k]
                   	t[i][j][k] = np.average(liste)
			print "Average : " + str(i) + "/" + str(h-2)
        return t



# The normalization consists in putting pixels in the same intensity before being combined

# By dividing the flat-field pixel value by the mean of all the pixels in the flat-field image, we arrive at the normalized pixel value.
# A pixel that has a value equal to the mean will be normalized to 1, while a pixel that has a value less than the mean will be normalized to less than 1, and pixels with values above the mean will be normalized to more than 1.
# Any image-processing program that performs calibration takes care of this normalization automatically, but it’s important to understand the process, as we’ll see when we talk about how to get good flats.


def normalize(ndarray_list):
	""" Normalize each ndarray and scale all
	> All ndarray must have same dimensions!

	Parameters :
	- ndarray_list : ndarray list of images


	Returns :
	- ndarray : ndarray in wich each pixel match to pixels normalize

	"""
	liste = []
	lenght = len(ndarray_list)
	print "Taille de la liste d'image à traiter : "+ str(lenght)
	# 1) Normalize each flat field, i.e. divide it by its mean entry value
	for i in range(lenght):
		print "Normalize 1/2 : " + str(i+1) + "/" + str(lenght)
		mean = np.mean(ndarray_list[i]) # Find the mean of the ndarray
		print "Moyenne de la " + str(i+1) + " image : " + str(mean)
		liste.append(mean)
		ndarray_list[i] = np.true_divide(ndarray_list[i], mean) # Divide ndarray by its mean, normalizing it
	# 2) Scale all of the fields’ means so that their individual averages are equal to one another
	meanofmean = sum(liste) / len(liste)  # Find the mean of the total set of ndarray_list
	print "Moyenne global de toutes les images : " + str(meanofmean)
	for i in range(lenght):
		print "Normalize 2/2 with : "+ str(i+1) + "/" + str(lenght)
		ndarray_list[i] = np.multiply(ndarray_list[i], np.true_divide(meanofmean, np.mean(ndarray_list[i]))) # Divide
	return ndarray_list



# MASTER DARK ---------------------------------------------------------------------------------------------------------------#

# Dark fields capture the noise inherent to the CCD array, which we would like to eliminate so the sensor doesn’t contaminate the light we’re collecting from the night sky

def processMasterDark(ndarray_list) :
	""" The MASTERDARK image will serve to remove the thermal noise and random noise on our LIGHT image

	Parameters :
	 - ndarray_list : ndarray list of darks.

	 Return :
	 - ndarray : MasterDark ndarray
	"""
	# 1) Create a sigma reject array from all of them, entry-by-entry.
	return sigmaReject(ndarray_list)


def processMasterDarkWithBias(ndarray_list, ndarray_masterBias) :
	""" The MASTERDARK image will serve to remove the thermal noise and random noise on our LIGHT image

	Parameters :
	 - ndarray_list : ndarray list of darks.
	 - ndarray_masterBias : MasterBias ndarray

	 Return :
	 - ndarray : MasterDark ndarray
	"""
	# 1) Subtract the master bias frame
	darks = list(ndarray_list)
	lenght = len(darks)
	h,l,r = darks[0].shape
	for i in range(lenght):
		darks[i] = np.subtract(darks[i], ndarray_masterBias)
	# 2) Create a sigma reject array from all of them, entry-by-entry.
	return sigmaReject(darks)


def processMasterDarkFlat(ndarray_list, ndarray_masterBias) :
	""" The MASTER DARK FLAT image will serve to calcul the MASTER FLAT FIELD WITH BIAS

	Parameters :
	 - ndarray_list : ndarray list of flats.
	 - ndarray_masterBias : MasterBias ndarray

	 Return :
	 - ndarray : MasterDarkFlat ndarray
	"""
	# 1) Subtract the master bias frame
	darkflats = list(ndarray_list)
	lenght = len(darkflats)
	h,l,r = darkflats[0].shape
	for i in range(lenght):
		darkflats[i] = np.subtract(darkflats[i], ndarray_masterBias)
	# 2) Create a sigma reject array from all of them, entry-by-entry.
	return sigmaReject(darkflats)


# MASTER FLAT ---------------------------------------------------------------------------------------------------------------#

# Flats are images portraying the sensitivity of individual pixels in the frame, which is illuminated uniformly

def processMasterFlat(ndarray_list, ndarray_masterDark) :
	""" The MASTERFLAT image will serve to remove all track of dusts, gradient, vignetting on our LIGHT image

	Parameters :
	 - ndarray_list : ndarray list of flats.
	 - ndarray_masterDark : MasterDark ndarray

	 Return :
	 - ndarray : Masterflat ndarray
	"""
	# 1) Subtract the master dark frame
	lenght = len(ndarray_list)
	h,l,r = ndarray_list[0].shape
	vmin,vmax = tproc.limitValues(ndarray_list[0])
	#for frame in range(lenght):
	#	print "Substract Dark to Flats : " + str(frame+1) + "/" + str(lenght)
	#	ndarray_list[frame] = np.subtract(ndarray_list[frame],ndarray_masterDark)
	#	for i in range(h):
	#		for j in range(l):
	#			for k in range(r):
	#				if(ndarray_list[frame][i][j][k] < vmin):
	#					ndarray_list[frame][i][j][k] = vmin
	# 2) Normalize all frame
	# 3) Create a median array from all of them, entry-by-entry.
	return median(normalize(ndarray_list))


def processMasterFlatWithBias(ndarray_list, ndarray_masterDarkFlat, ndarray_masterBias) :
	""" The MASTERFLAT image will serve to remove all track of dusts, gradient, vignetting on our LIGHT image

	Parameters :
	 - ndarray_list : ndarray list of flats.
	 - ndarray_masterBias : MasterBias ndarray
	 - ndarray_masterDarkFlat : MasterDarkFlat ndarray

	 Return :
	 - ndarray : MasterFlat ndarray
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
	return median(flats)


# MASTER BIAS ---------------------------------------------------------------------------------------------------------------#

# If you take your series of images DARK with same parameters (the same exposure time, same binning, same temperature) as the LIGHT images and for your images of FLAT FIELD, you will not need to set of images of BIAS.
# CAREFUL : OVERALL BY AVERAGE only !
def processMasterBias(ndarray_list) :
	""" The MASTERBIAS image will serve to remove the initial exposure level of pixels in our LIGHT
		> If you take your series of images DARK with same parameters (the same exposure time, same binning, same temperature) as the LIGHT images and for your images of FLAT FIELD, you will not need to set of images of BIAS.

		Parameters :
		 - ndarray_list : ndarray list of bias

		 Return :
		 - ndarray : MasterBias ndarray
	"""
	# 1) Create an average array from all of them, entry-by-entry.
	return average(ndarray_list)


# LIGHT ----------------------------------------------------------------------------------------------------------------------#

# We will use master flat and dark field to clean up each light frame, which contains data about the night sky : (Light-Dark)/Flat

def calibration(ndarray_list, ndarray_masterDark, ndarray_masterFlat):
	""" The final result will be a perfectly corrected LIGHT image

	Parameters :
	 - ndarray_list : ndarray list of lights.
	 - ndarray_masterDark : MasterDark ndarray
	 - ndarray_masterFlat : MasterFlat ndarray

	 Return :
	 - ndarray : ndarray list of lights calibrated.
	"""
	lights_list = list(ndarray_list)
	length = len(lights_list)
	# Use masterflat and masterdark to clean up each light frame
	for i in range(lenght):
		lights_list[i] = np.true_divide(np.subtract(lights_list[i], ndarray_masterDark), ndarray_masterFlat)
	# Normalize each light frame
	return normalize(lights_list)


def calibrationWithBias(ndarray_list, ndarray_masterDark, ndarray_masterFlat, ndarray_masterBias):
	""" The final result will be a perfectly corrected LIGHT image

	Parameters :
	 - ndarray_list : ndarray list of lights.
	 - ndarray_masterDark : MasterDark ndarray
	 - ndarray_masterFlat : MasterFlat ndarray
	 - ndarray_masterBias : MasterBias ndarray

	 Return :
	 - ndarray : ndarray list of lights calibrated.
	"""
	lights_list = list(ndarray_list)
	length = len(lights_list)
	# Use masterflat, masterdark and masterbias to clean up each light frame
	for i in range(lenght):
		lights_list[i] = np.subtract(lights_list[i], ndarray_masterBias)
		lights_list[i] = np.true_divide(np.subtract(lights_list[i], ndarray_masterDark), ndarray_masterFlat)
	# Normalize each light frame
	return normalize(lights_list)


def alignment(ndarray_ref, ndarray_list):
	""" To align the LIGHT image according to a references image

	Parameters :
	 - ndarray_ref : ndarray of the light reference.
	 - ndarray_list : ndarray list of the lights which must be aligned

	 Return :
	 - ndarray_list : ndarray list of all the aligned lights.
	"""
	lenght = len(ndarray_list)
	h,l,r = ndarray_ref.shape

	for nb in range(lenght) :
		# The result is always calculated from the ref image
		result = np.copy(ndarray_ref)
		# Calcul the shift factor
		shift = reg.shift_translation(ndarray_ref,ndarray_list[nb])
		decalx = int(shift[0])
		decaly = int(shift[1])
		# Apply the shift factor, according to its sign
		if decalx>=0 and decaly>=0 :
			for i in range(decalx,h):
				for j in range(decaly,l):
					result[i][j]=ndarray_list[nb][i-decalx][j-decaly]
		if decalx<0 and decaly<0 :
		    for i in range(0-decalx,h):
		        for j in range(0-decaly,l):
		            result[i+decalx][j+decaly]=ndarray_list[nb][i][j]
		if decalx>=0 and decaly<0 :
		    for i in range(decalx,h):
		        for j in range(0-decaly,l):
		            result[i][j+decaly]=ndarray_list[nb][i-decalx][j]
		if decalx<0 and decaly>=0 :
		    for i in range(0-decalx,h):
		        for j in range(decaly,l):
		            result[i+decalx][j]=img2[i][j-decaly]
		# Apply the changes to the image
		ndarray_list[nb] = result
	return (ndarray_ref,ndarray_list)

def registration(ndarray_ref, ndarray_list):
	""" To overlap LIGHT image (after the calibration)

	Parameters :
	 - ndarray_ref : ndarray of the light reference.
	 - ndarray_list : ndarray list of the lights which must be aligned

	 Return :
	 - ndarray_list : ndarray list of all the registred lights.
	 """
	ndarray_ref,ndarray_list = alignment(ndarray_ref, ndarray_list)
	ndarray_list.append(ndarray_ref)
	return sigmaReject(ndarray_list)
