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
    sDataFile = "/home/tanner/src/WHAT/backend/data/"
#Deploy Paths
else:
    logPath = "/home/ubuntu/hd2/src/WHAT/ui/log/"
    plotDataPath="/home/ubuntu/hd2/src/WHAT/ui/log/plots/"
    canopyFlowPath="/home/ubuntu/src/canopy/build/canopy_flow"
    sDataFile = "/home/ubuntu/hd2/src/WHAT/backend/data/" #note that if we get more data files
    #change this to generic and specify below
    
def writeLogFile(com_msg):
    """
    Write a log file
    """
    lFile=logPath+"xLog"
    with open(lFile,'w') as f:
        f.write(com_msg)
        f.close()
        

def calc_windProfile(inputSpeed,windUnits,inputHeight,outputHeight,canopyHeight,heightUnits,crownRatio,surface,model):
    """
    setup a windProfile object, populate it with values and then
    run canopy-flow
    Returns the desired wind speed and the path
    to a datafile where the profile data is stored
    
    model indicates which profile model to use
    options are Massman / Albini
    """
        
    
    #Set up the wind profile  
    wind=wp.windProfile()
    wind.set_paths(sDataFile,canopyFlowPath)
    wind.useMutliProc=True
    wind.set_InputWindSpeed(float(inputSpeed),windUnits)
    wind.set_InputWindHeight(float(inputHeight),heightUnits)
    wind.set_OutputWindHeight(float(outputHeight),heightUnits)
    wind.set_CanopyHeight(float(canopyHeight),heightUnits)
    wind.crownRatio=float(crownRatio)
    wind.set_surface(surface)
    

    if(model=="Massman"):
        wind.cf_uz()
        outputWindSpeed = [wind.get_OutputWindSpeed(windUnits),"NAN"]
        outDataFile = [wind.PlotDataFile,"NAN"]        
        
    if(model=="Albini"):
        wind.a_uz()
        outputWindSpeed = ["NAN",wind.get_aOutputWindSpeed(windUnits)]
        outDataFile = ["NAN",wind.a_PlotDataFile]        

    if(model=="Both"):
        wind.cf_uz()
        wind.a_uz()
        
        outputWindSpeed = [wind.get_OutputWindSpeed(windUnits),
                           wind.get_aOutputWindSpeed(windUnits)]
        outDataFile = [wind.PlotDataFile,wind.a_PlotDataFile]
#    else:
#        outputWindSpeed = ["NAN","NAN"]
#        outDataFile = ["NAN","NAN"]
        
    writeLogFile(wind.writeLogText())              
    return outputWindSpeed,outDataFile    

#start=time.time()
#                    is  isu  ih oh  ch  hu  cr   sf
#x,y=calc_windProfile(10,"mph",20,50,100,"ft",0.7,"Spruce","Both")
#x,y=calc_windProfile(10,"mph",100,20,65,"ft",0.7,"Spruce")
#stop=time.time()
#print(stop-start)
#print(x)