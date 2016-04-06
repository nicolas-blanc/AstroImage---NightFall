#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def shift_translation(src_image, target_image):
    """
    Translation registration by cross-correlation (like FFT upsampled cross-correlation)

    Parameters :
     - src_image : ndarray of the reference image.
     - target_image : ndarray of the image to register. /!\ Must be same dimensionality as src_image.

     Return :
      - shift : ndarray of the shift pixels vector required to register the target_image the with src_image.

    """
    # The two images need to have the same size
    if src_image.shape != target_image.shape:
        raise ValueError("Registration Error : The images need to have the same size")

    # In order to calcul the FFT(Fast Fourier Transform), we need convert the data type into real data
    src_image = np.array(src_image, dtype=np.complex128, copy=False)
    target_image = np.array(target_image, dtype=np.complex128, copy=False)
    src_freq = np.fft.fftn(src_image)
    target_freq = np.fft.fftn(target_image)

    # In order to calcul the shift in pixel, we need to compute the cross-correlation by an IFFT(Inverse Fast Fourier Transform)
    shape = src_freq.shape
    image_product = src_freq * target_freq.conj()
    cross_correlation = np.fft.ifftn(image_product)

    # Locate maximum in order to calcul the shift between two numpy array
    maxima = np.unravel_index(np.argmax(np.abs(cross_correlation)),cross_correlation.shape)
    midpoints = np.array([np.fix(axis_size / 2) for axis_size in shape])

    shift = np.array(maxima, dtype=np.float64)
    shift[shift > midpoints] -= np.array(shape)[shift > midpoints]

    # If its only one row or column the shift along that dimension has no effect : we set to zero.
    for dim in range(src_freq.ndim):
        if shape[dim] == 1:
            shift[dim] = 0

    return shift
