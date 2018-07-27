# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 15:43:25 2018

@author: tanner

Wrapper for wp.py for use with either the CLI or Shiny-gui
"""

import wp
import getpass
import time
#Dev Paths
if getpass.getuser()=='tanner': 
    logPath = "/home/tanner/src/WHAT/backend/log/"
    plotDataPath="/home/tanner/src/WHAT/backend/data/plots/"
    canopyFlowPath="/home/tanner/src/canopy/build/canopy_flow"
    sDataFile = "/home/tanner/src/WHAT/backend/data/canopy_types.csv"
#Deploy Paths
else:
    logPath = "/home/ubuntu/hd2/src/WHAT/ui/log/"
    plotDataPath="/home/ubuntu/hd2/src/WHAT/ui/log/plots/"
    canopyFlowPath="/home/ubuntu/src/canopy/build/canopy_flow"
    sDataFile = "/home/ubuntu/hd2/src/WHAT/backend/data/canopy_types.csv" #note that if we get more data files
    #change this to generic and specify below
    
def writeLogFile(com_msg):
    """
    Write a log file
    """
    lFile=logPath+"xLog"
    with open(lFile,'w') as f:
        f.write(com_msg)
        f.close()
        

def calc_windProfile(inputSpeed,windUnits,inputHeight,outputHeight,canopyHeight,heightUnits,crownRatio,surface):
    """
    setup a windProfile object, populate it with values and then
    run canopy-flow
    Returns the desired wind speed and the path
    to a datafile where the profile data is stored
    """
    #Set up the wind profile  
    wind=wp.windProfile()
    wind.useMutliProc=True
    wind.set_InputWindSpeed(inputSpeed,windUnits)
    wind.set_InputWindHeight(inputHeight,heightUnits)
    wind.set_OutputWindHeight(outputHeight,heightUnits)
    wind.set_CanopyHeight(canopyHeight,heightUnits)
    wind.crownRatio=crownRatio
    wind.canopyFlowPath = canopyFlowPath
    wind.PlotDataPath = plotDataPath
    wind.surfaceDataFile = sDataFile
    wind.set_surface(surface)
    wind.cf_uz()
    
    #get outputs
    outputWindSpeed = wind.get_OutputWindSpeed(windUnits)
    outDataFile = wind.PlotDataFile    
    
    writeLogFile(wind.writeLogText())          
    return outputWindSpeed,outDataFile    

#start=time.time()
#                    is  isu  ih oh  ch  hu  cr   sf
#x,y=calc_windProfile(10,"mph",20,50,100,"ft",0.7,"Spruce")
#x,y=calc_windProfile(10,"mph",100,20,65,"ft",0.7,"Spruce")
#stop=time.time()
#print(stop-start)
#print(x)