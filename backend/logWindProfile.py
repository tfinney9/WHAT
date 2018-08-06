#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:45:39 2018

@author: tanner

Command Line interface for WHAT

"""

import sys

import logWindProfile2 #this is the old lwp + exponential canopy
import logWindProfile3 #this is the new canopy-flow model + albini

use_crap=False

arg_windSpd=float(sys.argv[1]) #known wind speed
arg_spdUnits=str(sys.argv[2]) #wind speed units
arg_surface=str(sys.argv[3]) #surface name ie spruce or barren
arg_initialHeight=float(sys.argv[4]) #height of known wind speed
arg_height=float(sys.argv[5]) #output height
arg_canopy=float(sys.argv[6]) #canopy height
arg_hgtUnits=str(sys.argv[7]) #height units
arg_SCM=str(sys.argv[8]) #Not USED
arg_crownRatio = str(sys.argv[8]) #crown ratio, amount of tree/thing that is canopy vs stem
arg_MODEL = str(sys.argv[9]) #which model to use (Massman,Albini,Both)
         
          
if use_crap==False:
    """
    Use the new way
    """
    if arg_canopy==0: #canopy-flow doesn't handle 0 for a canopy very well, make it small and it works fine
        arg_canopy=0.01
    heightAdjustedSpeed,dataFileName=logWindProfile3.calc_windProfile(arg_windSpd,
                                                                     arg_spdUnits,
                                                                     arg_initialHeight,
                                                                     arg_height,
                                                                     arg_canopy,
                                                                     arg_hgtUnits,
                                                                     arg_crownRatio,
                                                                     arg_surface,
                                                                     arg_MODEL)
                 
#     outStr = "Calculated Wind Speed: Massman Model: "  
    hStr = "Calculated Wind Speed: " 
    delim=";"                                                             
    massmanStr="Massman: NAN"
    albiniStr="Albini: NAN"
    
    mPathStr=delim+"X"    
    aPathStr=delim+"X"
    
    mbStr=delim+"X"
    abStr=delim+"X"
    if(heightAdjustedSpeed[0]!="NAN"):
        massmanStr = "Massman Model: "+str(round(heightAdjustedSpeed[0],2))+" "+str(arg_spdUnits)+\
        " at "+str(arg_height)+" "+str(arg_hgtUnits)+" "
        
        mPathStr=delim+dataFileName[0]
        
        mbStr=delim+str(heightAdjustedSpeed[0])+delim+str(arg_height)
        
    if(heightAdjustedSpeed[1]!="NAN"):
        albiniStr = "Albini Model: "+str(round(heightAdjustedSpeed[1],2))+" "+str(arg_spdUnits)+\
        " at "+str(arg_height)+" "+str(arg_hgtUnits)+" " 
        
        aPathStr=delim+dataFileName[1]
        
        abStr=delim+str(heightAdjustedSpeed[1])+delim+str(arg_height)

    outStr = hStr+massmanStr+albiniStr+mPathStr+aPathStr+mbStr+abStr
    print(outStr)
        
#    print(round(heightAdjustedSpeed,2),arg_spdUnits,"at",
#    arg_height,arg_hgtUnits,":|:",dataFileName,":|:",
#    heightAdjustedSpeed,":|:",arg_height)