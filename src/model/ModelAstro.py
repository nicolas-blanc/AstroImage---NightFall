#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from Model import Model

class ModelAstro(Model):
    """ Allow to save lights, darks, flats, bias, and masters, whitout history """
    def __init__(self):
        super(ModelAstro, self).__init__()
        self._light = []
        self._dark = []
        self._flat = []
        seld._bias = []
        self._masterDark = null
        self._masterFlat = null
        self._masterBias = null


# LIGHT -------------------------------------------------#
    def getLight(self):
      """ To get back the list of light """
      return self._light

    def addLight(self, light):
      """ To add a light at the list of light """
      self._light = self._light.append(light)  

    def delLight(self, num):
      """ To remove a light in the list of light """
      del self._light[num]



# DARK --------------------------------------------------#
    def getDark(self):
      """ To get back the list of Dark """
      return self._dark

    def addDark(self, Dark):
      """ To add a Dark at the list of Dark """
      self._dark = self._dark.append(Dark)  

    def delDark(self, num):
      """ To remove a Dark in the list of Dark """
      del self._dark[num]


# FLAT --------------------------------------------------#
    def getFlat(self):
      """ To get back the list of Flat """
      return self._flat

    def addFlat(self, Flat):
      """ To add a Flat at the list of Flat """
      self._flat = self._flat.append(Flat)  

    def delFlat(self, num):
      """ To remove a Flat in the list of Flat """
      del self._flat[num]


# BIAS (OFFSET) ------------------------------------------#
    def getBias(self):
      """ To get back the list of Bias """
      return seld._bias

    def addBias(self, Bias):
      """ To add a Bias at the list of Bias """
      seld._bias = seld._bias.append(Bias)  

    def delBias(self, num):
      """ To remove a Bias in the list of Bias """
      del seld._bias[num]


# MASTER DARK ------------------------------------------#
    def getMasterDark(self):
      """ To get back the masterDark """
      return self._masterDark

    def setMasterDark(self, masterDark):
      """ To add the masterDark """
      self._masterDark = masterDark

    def delMasterDark(self):
      """ To remove the masterDark """
      self._masterDark = []


# MASTER FLAT -------------------------------------------#
    def getMasterFlat(self):
      """ To get back the masterFlat """
      return self._masterFlat

    def setMasterFlat(self, masterFlat):
      """ To add the masterflat """
      self._masterFlat = masterFlat

    def delMasterFlat(self):
      """ To remove the masterFlat """
      self._masterFlat = []


# MASTER BIAS (OFFSET) -----------------------------------#
    def getMasterBias(self):
      """ To get back the masterBias """
      return self._masterBias

    def setMasterBias(self, masterBias):
      """ To add the masterBias """
      self._masterBias = masterBias

    def delMasterBias(self):
      """ To remove the masterBias """
      self._masterBias = []







