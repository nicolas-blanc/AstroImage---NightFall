#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from Model import Model

class ModelTreatment(Model):
    """ Allow to save the work on the final light, with the history of treatments process """
    def __init__(self, original_picture_ndarray):
        super(ModelTreatment, self).__init__()  
        self._origin = original_picture_ndarray
        self._treatment = {}


# TREATMENT ------------------------------------------------#
    def gettreatment(self, nametreatment):
      """ To get back the reverse-treatment of the treatment """
      return (self._treatment).get(nametreatment)

    def addtreatment(self, nametreatment, reversetreatment):
      """ To add the reverse-treatment of a treatment at the dictionary of treatment
          > at each modification of the original picture, add the reverse-treatment at this list !
      """
      self._treatment[nametreatment] = reverse

    def deltreatment(self, nametreatment):
      """ To remove a treatment in the treatment dictionary """
      del self._treatment[nametreatment]
