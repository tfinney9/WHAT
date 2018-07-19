#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:45:39 2018

@author: tanner
"""

import sys

import logWindProfile2

arg_windSpd=float(sys.argv[1])
arg_spdUnits=str(sys.argv[2])
arg_surface=str(sys.argv[3])
arg_initialHeight=float(sys.argv[4])
arg_height=float(sys.argv[5])
arg_canopy=float(sys.argv[6])
arg_hgtUnits=str(sys.argv[7])
arg_SCM=str(sys.argv[8])


#Add in the simple Canopy Model
if arg_SCM=="TRUE":
    heightAdjustedSpeed=logWindProfile2.calc_simpleCanopyAndNeutralLWP(arg_windSpd,
                                                                       arg_spdUnits,
                                                                       arg_initialHeight,
                                                                       arg_canopy,
                                                                       arg_height,
                                                                       arg_hgtUnits,
                                                                       arg_surface)


#Else just do the normal one
else:
    heightAdjustedSpeed=logWindProfile2.calc_neutralLWP(arg_windSpd,
                                                        arg_spdUnits,
                                                        arg_initialHeight,
                                                        arg_canopy,
                                                        arg_height,
                                                        arg_hgtUnits,
                                                        arg_surface)


dataFileName=logWindProfile2.dfName[0]
                                                       
print(round(heightAdjustedSpeed,2),arg_spdUnits,"at",
      arg_height,arg_hgtUnits,":|:",dataFileName,":|:",
      heightAdjustedSpeed,":|:",arg_height)