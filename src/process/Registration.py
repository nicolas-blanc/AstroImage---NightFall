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

    # Locate maximum
    maxima = np.unravel_index(np.argmax(np.abs(cross_correlation)),cross_correlation.shape)
    midpoints = np.array([np.fix(axis_size / 2) for axis_size in shape])

    shifts = np.array(maxima, dtype=np.float64)
    shifts[shifts > midpoints] -= np.array(shape)[shifts > midpoints]

    src_amp = np.sum(np.abs(src_freq) ** 2) / src_freq.size
    target_amp = np.sum(np.abs(target_freq) ** 2) / target_freq.size
    CCmax = cross_correlation.max()

    # If its only one row or column the shift along that dimension has no effect. We set to zero.
    for dim in range(src_freq.ndim):
        if shape[dim] == 1:
            shifts[dim] = 0

    return shifts



if __name__ == '__main__':
    from PIL import Image
    from skimage import data
    import imageio
    from ImageRaw import ImageRaw

#    img = data.imread('renard-marche-neige.jpeg')
#    img2 = data.imread('renard-marche-neige4.jpeg')
    path = '../../Pictures_test/lights/'
    img = ImageRaw(path + 'L_0022_IC405_ISO800_300s__15C.CR2').getndarray()
    img2 = ImageRaw(path + 'L_0022_IC405_ISO800_300s__13C.CR2').getndarray()
    imageio.imsave('light_ref.jpg', img)
    imageio.imsave('light_dec.jpg', img2)

    result = np.copy(img)
    h,l,r = img.shape

    shifts = shift_translation(img,img2)
    decalx = int(shifts[0])
    decaly = int(shifts[1])

    if decalx>=0 and decaly>=0 :
        for i in range(decalx,h):
            for j in range(decaly,l):
                result[i][j]=img2[-decalx+i][-decaly+j]
    if decalx<0 and decaly<0 :
        for i in range(0,h+h*decalx):
            for j in range(0,l+l*decaly):
                result[i+decalx][j+decaly]=img2[i][j]
    if decalx>=0 and decaly<0 :
        for i in range(decalx,h):
            for j in range(0,l+l*decaly):
                result[i][j+decaly]=img2[-decalx+i][j]
    if decalx<0 and decaly>=0 :
        for i in range(0,h+h*decalx):
            for j in range(decaly,l):
                result[i+decalx][j]=img2[i][-decaly+j]

    imageio.imsave('light_decal_register.jpg', result)
