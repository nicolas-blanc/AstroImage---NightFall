#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyfits


class Image(object):
    """ Image represented by ndarray (library numpy) """
    def __init__(self, path, ndarray, size):
    	""" Convert image to 3-color array (ndarray) """
        super(Image, self).__init__()
        self._path = path
        self._ndarray = ndarray
        self._size = size

    def getPath(self):
        """ To get back the path of the Image """
        return self._path

    def getndarray(self):
       """ To get back the ndarray of the Image """
       return self._ndarray

    def getSize(self):
    	""" Return the size of Image"""
    	return self._size

    def saveToFits(self, path, fitsName, LATOBS='Not informed', LONGOBS='Not informed'):
        """ Save a 3-color array to separate FITS images """
    	npr = self._ndarray[:,:,0]
    	#print("CONVERT TO FITS")
    	#print(npr)
    	npg = self._ndarray[:,:,1]
    	npb = self._ndarray[:,:,2]

    	red = pyfits.PrimaryHDU()
    	red.header['LATOBS'] = LATOBS
    	red.header['LONGOBS'] = LONGOBS
    	red.data = npr
    	#print("DATA LOAD")
    	#print(red.data)
    	red.writeto(path+fitsName+'_red.fits')

    	green = pyfits.PrimaryHDU()
    	green.header['LATOBS'] = LATOBS
    	green.header['LONGOBS'] = LONGOBS
    	green.data = npg
    	green.writeto(path+fitsName+'_green.fits')

    	blue = pyfits.PrimaryHDU()
    	blue.header['LATOBS'] = LATOBS
    	blue.header['LONGOBS'] = LONGOBS
    	blue.data = npb
    	blue.writeto(path+fitsName+'_blue.fits')
