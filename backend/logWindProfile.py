#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:45:39 2018

@author: tanner
"""

import sys

import logWindProfile2 #this is the old lwp + exponential canopy
import logWindProfile3 #this is the new canopy-flow model + albini

use_crap=False

arg_windSpd=float(sys.argv[1])
arg_spdUnits=str(sys.argv[2])
arg_surface=str(sys.argv[3])
arg_initialHeight=float(sys.argv[4])
arg_height=float(sys.argv[5])
arg_canopy=float(sys.argv[6])
arg_hgtUnits=str(sys.argv[7])
arg_SCM=str(sys.argv[8])
arg_crownRatio = str(sys.argv[8])
arg_MODEL = str(sys.argv[9])

if  use_crap==True:
    """
    To use the old method, change the bool up at the top 
    this is not recomended
    """
    #The Math doesn't work out if the canopy height== the wind height
    # offset by .1 fixes it
    if arg_canopy==arg_initialHeight:
        arg_canopy-=0.1
        if arg_canopy<=0:
            arg_canopy=0
    
    
    #If the canopy is zero, don't use the model
    if arg_canopy==0:
        arg_SCM="FALSE"
    
    
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
          
          
          
else:
    """
    Use the new way
    """
    if arg_canopy==0: #canopy-flow doesn't handle 0 for a canopy very well, make it small and it works fine
        arg_canopy=0.1
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