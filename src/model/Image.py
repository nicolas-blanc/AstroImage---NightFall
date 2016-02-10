#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import imageio
import rawpy #Python wrapper for the LibRaw library (raw image decoder)
from rawpy import ColorSpace
from rawpy import DemosaicAlgorithm


class image(object):
    """docstring for image"""
    def __init__(self, path):
        super(image, self).__init__()

        # Load a RAW file
        self.file = rawpy.imread(path)
    	# self.raw_height, self.raw_width, self.height, self.width, self.top_margin, self.left_margin, self.iheight, self.iwidth, self.pixel_aspect, self.flip = self.file.size


    # Postprocess this file to obtain a numpy ndarray of shape (h,w,c)
    # 16 bits => la palette de couleur peut contenir 2^16 = 65536 couleurs
    def debayeurization(self):
    	self.img = self.file.postprocess(output_bps=16, output_color=ColorSpace.sRGB, demosaic_algorithm=DemosaicAlgorithm.AAHD, use_camera_wb=True,no_auto_bright=True)


    # To get back the size of the image
    def getSize(self):
    	return (self.height, self.width)


    def getFile(self):
        return self.file


    def getImageDebayeurization(self):
        return self.img




if __name__ == '__main__':
    path = '../../Pictures_test/DSC_0599.NEF'
    i1 = image(path)
    i1.debayeurization()
    imageio.imsave('../../Pictures_test/testFITS.tiff', i1.getImageDebayeurization())
