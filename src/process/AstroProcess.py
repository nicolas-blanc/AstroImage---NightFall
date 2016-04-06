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


#---------- TESTS -------------#

if __name__ == '__main__':

	import imageio
	from PIL import Image
	from skimage import data

	import sys
	path1 = '../image/'
	sys.path.append(path1)
	from ImageRaw import ImageRaw

# MasterDark :
	path = '../../Pictures_test/darks/'
	dark1 = ImageRaw(path + 'D_0003_IC405_ISO800_300s__13C.CR2').getndarray()
	dark3 = ImageRaw(path + 'D_0015_IC405_ISO800_300s__13C.CR2').getndarray()
	dark4 = ImageRaw(path + 'D_0014_IC405_ISO800_300s__13C.CR2').getndarray()
	dark5 = ImageRaw(path + 'D_0013_IC405_ISO800_300s__13C.CR2').getndarray()
	dark7 = ImageRaw(path + 'D_0012_IC405_ISO800_300s__13C.CR2').getndarray()
	dark8 = ImageRaw(path + 'D_0011_IC405_ISO800_300s__13C.CR2').getndarray()
	dark9 = ImageRaw(path + 'D_0010_IC405_ISO800_300s__13C.CR2').getndarray()
	dark11 = ImageRaw(path + 'D_0003_IC405_ISO800_300s__13C.CR2').getndarray()
	result_dark = processMasterDark([dark1,dark3,dark4,dark5,dark7,dark8,dark9,dark11])
	imageio.imsave('../../Pictures_test/testMasterDark.tiff', result_dark)
	del dark1
	del dark3
	del dark4
	del dark5
	del dark7
	del dark8
	del dark9
	del dark11
	del result_dark

# MasterFlat :
	result_dark = data.imread('../../Pictures_test/testMasterDark.tiff')
	path = '../../Pictures_test/flats/'
	flat1 = ImageRaw(path + 'IMG_3090.CR2').getndarray()
	flat2 = ImageRaw(path + 'IMG_3089.CR2').getndarray()
	flat3 = ImageRaw(path + 'IMG_3088.CR2').getndarray()
	flat4 = ImageRaw(path + 'IMG_3087.CR2').getndarray()
	flat5 = ImageRaw(path + 'IMG_3086.CR2').getndarray()
	flat6 = ImageRaw(path + 'IMG_3085.CR2').getndarray()
	flat7 = ImageRaw(path + 'IMG_3084.CR2').getndarray()
	flat8 = ImageRaw(path + 'IMG_3083.CR2').getndarray()
	flat9 = ImageRaw(path + 'IMG_3082.CR2').getndarray()
	flat10 = ImageRaw(path + 'IMG_3081.CR2').getndarray()
	flat11 = ImageRaw(path + 'IMG_3079.CR2').getndarray()
	flat12 = ImageRaw(path + 'IMG_3078.CR2').getndarray()
	flat13 = ImageRaw(path + 'IMG_3077.CR2').getndarray()
	flat14 = ImageRaw(path + 'IMG_3076.CR2').getndarray()
	flat15 = ImageRaw(path + 'IMG_3075.CR2').getndarray()
	flat16 = ImageRaw(path + 'IMG_3074.CR2').getndarray()
	flat17 = ImageRaw(path + 'IMG_3073.CR2').getndarray()
	flat18 = ImageRaw(path + 'IMG_3072.CR2').getndarray()
	flat19 = ImageRaw(path + 'IMG_3071.CR2').getndarray()
	flat20 = ImageRaw(path + 'IMG_3070.CR2').getndarray()
	flat21 = ImageRaw(path + 'IMG_3069.CR2').getndarray()
	flat22 = ImageRaw(path + 'IMG_3068.CR2').getndarray()
	flat23 = ImageRaw(path + 'IMG_3067.CR2').getndarray()
	flat24 = ImageRaw(path + 'IMG_3066.CR2').getndarray()
	flat25 = ImageRaw(path + 'IMG_3065.CR2').getndarray()
	flat26 = ImageRaw(path + 'IMG_3064.CR2').getndarray()
	flat27 = ImageRaw(path + 'IMG_3063.CR2').getndarray()
	flat28 = ImageRaw(path + 'IMG_3062.CR2').getndarray()
	flat29 = ImageRaw(path + 'IMG_3061.CR2').getndarray()
	flat30 = ImageRaw(path + 'IMG_3060.CR2').getndarray()
	flat31 = ImageRaw(path + 'IMG_3059.CR2').getndarray()
	result_flat = processMasterFlat([flat1,flat2,flat3,flat4,flat5,flat6,flat7,flat8,flat9,flat10,flat11,flat12,flat13,flat14,flat15,flat16,flat17,flat18,flat19,flat20,flat21,flat22,flat23,flat24,flat25,flat26,flat27,flat28,flat29,flat30,flat31],result_dark)
	imageio.imsave('../../Pictures_test/testMasterFlat.jpg', result_flat)
	del flat1
	del flat2
	del flat3
	del flat4
	del flat5
	del flat6
	del flat7
	del flat8
	del flat9
	del flat10
	del flat11
	del flat12
	del flat13
	del flat14
	del flat15
	del flat16
	del flat17
	del flat18
	del flat19
	del flat20
	del flat21
	del flat22
	del flat23
	del flat24
	del flat25
	del flat26
	del flat27
	del flat28
	del flat29
	del flat30
	del flat31
	del result_flat

 Registration :
	path = '../../Pictures_test/lights/'
	img = ImageRaw(path + 'L_0022_IC405_ISO800_300s__15C.CR2').getndarray()
	img2 = ImageRaw(path + 'L_0021_IC405_ISO800_300s__15C.CR2').getndarray()
	img3 = ImageRaw(path + 'L_0014_IC405_ISO800_300s__15C.CR2').getndarray()
	img4 = ImageRaw(path + 'L_0014_IC405_ISO800_300s__15C.CR2').getndarray()
	img5 = ImageRaw(path + 'L_0014_IC405_ISO800_300s__15C.CR2').getndarray()
	img6 = ImageRaw(path + 'L_0014_IC405_ISO800_300s__15C.CR2').getndarray()
	img7 = ImageRaw(path + 'L_0014_IC405_ISO800_300s__15C.CR2').getndarray()
	img8 = ImageRaw(path + 'L_0014_IC405_ISO800_300s__15C.CR2').getndarray()

	img9 = ImageRaw(path + 'L_0020_IC405_ISO800_300s__14C.CR2').getndarray()
	img10 = ImageRaw(path + 'L_0019_IC405_ISO800_300s__14C.CR2').getndarray()
	img11 = ImageRaw(path + 'L_0020_IC405_ISO800_300s__12C.CR2').getndarray()
	img12 = ImageRaw(path + 'L_0015_IC405_ISO800_300s__12C.CR2').getndarray()
	img13 = ImageRaw(path + 'L_0003_IC405_ISO800_300s__12C.CR2').getndarray()
	img14 = ImageRaw(path + 'L_0001_IC405_ISO800_300s__12C.CR2').getndarray()

	img15 = ImageRaw(path + 'L_0022_IC405_ISO800_300s__13C.CR2').getndarray()
	img16 = ImageRaw(path + 'L_0021_IC405_ISO800_300s__13C.CR2').getndarray()
	img17 = ImageRaw(path + 'L_0018_IC405_ISO800_300s__13C.CR2').getndarray()
	img18 = ImageRaw(path + 'L_0016_IC405_ISO800_300s__13C.CR2').getndarray()
	img19 = ImageRaw(path + 'L_0007_IC405_ISO800_300s__13C.CR2').getndarray()
	img20 = ImageRaw(path + 'L_0004_IC405_ISO800_300s__13C.CR2').getndarray()
	img21 = ImageRaw(path + 'L_0002_IC405_ISO800_300s__13C.CR2').getndarray()

	img22 = ImageRaw(path + 'L_0019_IC405_ISO800_300s__10C.CR2').getndarray()
	img23 = ImageRaw(path + 'L_0009_IC405_ISO800_300s__18C.CR2').getndarray()

	result = processMasterFlat([img,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12,img13,img14,img15,img16,img17,img18,img19,img20,img21,img22,img23])
	imageio.imsave('light_register.tiff', result)
	del img
	del img1
	del img2
	del img3
	del img4
	del img5
	del img6
	del img7
	del img8
	del img9
	del img10
	del img11
	del img12
	del img13
	del img14
	del img15
	del img16
	del img17
	del img18
	del img19
	del img20
	del img21
	del img22
	del img23

#------------------------------#
