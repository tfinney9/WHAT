# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 10:47:44 2018

Wind Profile class

Calculate a wind profile using 

canopy-flow/Massman model

An improved canopy wind model for predicting wind
adjustment factors and wildland fire behavior

W.J. Massman, J.M. Forthofer, and M.A. Finney
2017
https://www.fs.usda.gov/treesearch/pubs/54040

AND/OR

Albini Baughman Canopy Model

ESTIMATING WINDSPEEDS FOR PREDICTING
WILDLAND FIRE BEHAVIOR

F. A. Albini and R. G. Baughman

USDA Forest Service
Research Paper INT-221
June 1979

@author: tanner
"""

import numpy
import subprocess
import time
import csv
from multiprocessing import Pool as ThreadPool
from functools import partial

#localLibraries
import calcUnits
import albini
#==================================================================================
# Wind Profile Class
#==================================================================================

class windProfile():
    """
    Generate a wind Profile
    Inputs and paths must be set
    """
    #Paths etc
    status_msg=""
    profile="stable"
    dataPath=""
    canopyFlowPath=""
    PlotDataPath=""    
    surfaceDataFile=""

    #inputs
    inputWindSpeed = 0.0 #meters per second
    inputWindHeight = 0.0  #meters
    surface = ""
    canopy_height = 0.0 #rough_h   
    outputWindHeight = 0.0
    
    #Outputs
    outputWindSpeed = 0.0 #Massman Out
    a_outputWindSpeed = 0.0 #Albini Out
    PlotDataFile=""   #Massman File  
    a_PlotDataFile="" #Albini File
    
    #Not Used Right Now
    zpd = 0.0 #Zero Plane Displacement rough_d
    inWindHeight=(inputWindHeight+canopy_height)-zpd

    #Tabulated Properties
    surfaceRoughess = 0.0 #This is the rougness of the canopy, used for lwp not for canopy-flow z0 (meters)
    leafAreaIndex = 3.28 #This is the number of leaves you hit on your way down
    dragCoeff = 0.20 #Drag Coefficient of the Canopy
    crownRatio = 0.7 #Amount of the "Tree/Vegetation" that is canopy vs stem
    subCanopyRoughness = 0.0075 #This is the roughness of the ground below the canopy   
    
    #Other Stuff that is important
    heightUnits="m"
    speedUnits="mps"
    dumpCanopy=0.0 #dump the canopy height on disk here if we don't need it

    #Control Options
    manualCanopy=False #if the user specifies a canopy (always will)
    useMutliProc=False #Use Multiprocessing
    useBuiltInOpt=False #Use a looping feature built into canopy-flow
    
    def set_paths(self,generalDataPath,canopyFlowPath):
        """
        Set the data paths for the entire thing to work
        NEED:
        generalDataPat: this points to ~/whatever/WHAT/backend/data/
        or something else as long as it properly configured
        
        canopyFlowPath: this points to where the canopy-flow
        program is compiled, must point to an executable
        or Massman won't work
        
        Note that on shiny servers
        the folders must be owned by shiny
        ie chgp shiny plots/
           chown shiny plots
        """
        self.dataPath = generalDataPath
        self.PlotDataPath = generalDataPath+"plots/"
        self.surfaceDataFile = generalDataPath+"canopy_types.csv"
        self.canopyFlowPath = canopyFlowPath
        
    def set_InputWindSpeed(self,wspd,ws_units):
        """
        Input the Known wind speed and the units you want to use
        mps mph kph cph fpf
        """
        self.inputWindSpeed=calcUnits.convertFromJiveUnits(wspd,ws_units)
        self.speedUnits=ws_units
    
    def set_InputWindHeight(self,inhgt,hgt_units):
        """
        Input the known wind speed height and units
        """
        self.inputWindHeight=calcUnits.distToMetric(inhgt,hgt_units)
        self.heightUnits=hgt_units
    
    def set_OutputWindHeight(self,outhgt,hgt_units):
        """
        Set the desired output wind speed and units
        """
        self.outputWindHeight=calcUnits.distToMetric(outhgt,hgt_units)
        self.heightUnits=hgt_units    
    
    def set_CanopyHeight(self,cpyhgt,hgt_units):
        """
        Set the canopy height and units
        """
        self.canopy_height = calcUnits.distToMetric(cpyhgt,hgt_units)
        self.heightUnits=hgt_units   
        self.manualCanopy=True
        
    def set_surface(self,surface):
        """
        Set the surface type/canopy type
        some properties are stored locally such as the
        leaf area index
        drag coefficient 
        and roughness
        a default canopy height is also availble
        but disabled
        """
        if self.manualCanopy==False:
            self.surface,self.canopy_height,self.leafAreaIndex,self.dragCoeff,self.surfaceRoughess = getSurfaceProperties(surface,self.surfaceDataFile)
        else:
            self.surface,self.dumpCanopy,self.leafAreaIndex,self.dragCoeff,self.surfaceRoughess = getSurfaceProperties(surface,self.surfaceDataFile)
            
    def get_InputWindSpeed(self,ws_units):
        """
        Retreive a stored value in the requested units
        """
        return calcUnits.convertToJiveUnits(self.inputWindSpeed,ws_units)

    def get_OutputWindHeight(self,hgt_units):
        return calcUnits.distFromMetric(self.outputWindHeight,hgt_units)
    
    def get_InputWindHeight(self,hgt_units):
        return calcUnits.distFromMetric(self.inputWindHeight,hgt_units)
            
    def get_CanopyHeight(self,hgt_units):
        return calcUnits.distFromMetric(float(self.canopy_height),hgt_units)
    
    def get_OutputWindSpeed(self,ws_units):
        return calcUnits.convertToJiveUnits(self.outputWindSpeed,ws_units)
        
    def get_aOutputWindSpeed(self,ws_units):
        return calcUnits.convertToJiveUnits(self.a_outputWindSpeed,ws_units)
        
        
    def tpn_uz(self):
        """
        Calculate the Log Wind Profile using class variables
        """
        self.outputWindSpeed = twoPointNeutral_uz(self.inputWindSpeed,
                                                  self.inputWindHeight,
                                                  self.outputWindHeight,
                                                  self.surfaceRoughess,
                                                  self.zpd)
    def a_uz(self):
        """
        use the Albini canopy model (see albini_uz())
        """
        self.a_outputWindSpeed,self.a_PlotDataFile = albini_uz_Wrapper(self.inputWindSpeed,
                                                                   self.inputWindHeight,
                                                                   self.outputWindHeight,
                                                                   self.canopy_height,
                                                                   self.crownRatio,
                                                                   self.surfaceRoughess,
                                                                   self.PlotDataPath,
                                                                   [self.speedUnits,
                                                                    self.heightUnits])
        
    def cf_uz(self):
        """
        Use the Massman canopy model (see canopyFlow_uz())
        """
        self.outputWindSpeed,self.PlotDataFile,self.status_msg = canopyFlow_uz(self.canopyFlowPath,
                                                                               self.dataPath,
                                                                               self.PlotDataPath,
                                                                               self.inputWindSpeed,
                                                                               self.inputWindHeight,
                                                                               self.outputWindHeight,
                                                                               self.canopy_height,
                                                                               self.subCanopyRoughness,
                                                                               self.leafAreaIndex,
                                                                               self.dragCoeff,
                                                                               self.crownRatio,
                                                                               [self.speedUnits,
                                                                                self.heightUnits])
                                                                               
                                          
    def writeLogText(self):
        f_msg="Inputs:\nWindSpeed: "+str(self.get_InputWindSpeed(self.speedUnits))+" "+self.speedUnits+\
        " ("+str(self.inputWindSpeed)+" mps)\n"
        f_msg+="Height: "+str(self.get_InputWindHeight(self.heightUnits))+" "+self.heightUnits+\
        " ("+str(self.inputWindHeight)+" m)"+"\n"
        f_msg+="Canopy Height: "+str(self.get_CanopyHeight(self.heightUnits))+" "+self.heightUnits+\
        " ("+str(self.canopy_height)+" m)"+"\n"
        f_msg+="Out Height: "+str(self.get_OutputWindHeight(self.heightUnits))+" "+self.heightUnits+\
        " ("+str(self.outputWindHeight)+" m)"+"\n"
        f_msg+="Surface: "+self.surface+"\nLAI: "+str(self.leafAreaIndex)+"\nCrownRatio: "+str(self.crownRatio)+"\n"
        f_msg+="Outputs:\n"
        f_msg+="Out Speed: "+str(self.get_OutputWindSpeed(self.speedUnits))+" "+self.speedUnits+"\n"
        return f_msg
    
#==================================================================================
# General Functions
#==================================================================================
def getSurfaceProperties(surface,surfacePath):
    """
    open up the surface properties file and
    read in some data
    Source: Massman canopy flow paper
    """
    f=open(surfacePath,"r")
    sDat=list(csv.reader(f))
    sDat=numpy.array(sDat)
    sLoc=numpy.where(sDat==surface)
    f.close()
    return sDat[sLoc[0]][0][0],float(sDat[sLoc[0]][0][1]),float(sDat[sLoc[0]][0][2]),float(sDat[sLoc[0]][0][3]),float(sDat[sLoc[0]][0][4])
                       
def getZPD(canopy_height,model):
    """
    Calculate the Zero Plane Displacement
    """
    if(model=="three_quaters"):
        return canopy_height*3./4.
    if(model=="two_thirds"):
        return canopy_height*3./4.
    if(model=="WindNinja"):
        return canopy_height*0.63 #See Line 3589 in ninja.cpp
 
def twoPointNeutral_uz(uz_1,z1,z2,z0,d):
    """
    uz_2 = velocity at z=z2
    uz_1 = velocity at z=z1
    d = zero plane displacement (meters)
    z0 = surface roughness (meters)
    
    https://en.wikipedia.org/wiki/Log_wind_profile
    """     
    uz_2 = uz_1*(numpy.log((z2-d)/z0)/(numpy.log((z1-d)/z0)))
    return uz_2       

def albini_uz_Wrapper(uz_1,z1,z2,canopy_height,crownRatio,z0c,dataPath,unitSet):
    """
    Integreate albini.py into windProfile
    See albini.py for more info
    """
    uz_2, zArray,uArray = albini.albini_uz(uz_1,z1,z2,canopy_height,crownRatio,z0c)
    namedList=["Albini","Input","Output"]
    colorList=["3","0","1"]

    dataFile=dataPath+"pDat-"+str(int(time.time()))+"-1.csv" #Open the datafile
    ff=open(dataFile,"w")    
    #write the header
#    x_str = "Wind Speed at z ("+unitSet[0]+"),Height (z) ("+unitSet[1]+"),color\n" 
    x_str = "Wind Speed at z ("+unitSet[0]+"),Height (z) ("+unitSet[1]+"),color,name\n"               
    ff.write(x_str)     
    
    for i in range(len(zArray)):
        uz_native=calcUnits.convertToJiveUnits(uArray[i],unitSet[0]) #convert each thing back to local units
        hg_native=calcUnits.distFromMetric(zArray[i],unitSet[1])
        ff.write(str(uz_native))
        ff.write(",")
        ff.write(str(hg_native))
#        ff.write(",%s\n"%colorList[0])
        ff.write(",%s,%s\n"%(colorList[0], namedList[0]))


    
    nativeOT_spd = calcUnits.convertToJiveUnits(uz_2,unitSet[0])
    nativeOT_hgt = calcUnits.distFromMetric(z2,unitSet[1])
    nativeIN_spd = calcUnits.convertToJiveUnits(uz_1,unitSet[0])
    nativeIN_hgt = calcUnits.distFromMetric(z1,unitSet[1])

    ff.write(str(nativeOT_spd)) #Out Speed
    ff.write(",")
    ff.write(str(nativeOT_hgt)) #Out Height
#    ff.write(",%s\n"%colorList[2])
    ff.write(",%s,%s\n"%(colorList[2], namedList[2]))
    ff.write(str(nativeIN_spd)) #In Speed
    ff.write(",")
    ff.write(str(nativeIN_hgt)) #In Height
#    ff.write(",%s\n"%colorList[1])
    ff.write(",%s,%s\n"%(colorList[1], namedList[1]))
    ff.close()
    
    return uz_2,dataFile

def canopyFlow_uz(canopyFlowPath,canopyFlowDataPath,plotDataPath,uz_1,z1,z2,canopy_height,z0g,LAI,Cd,CR,unitSet):
    """
    Use canopy-flow to generate a wind profile
    https://github.com/firelab/canopy-flow

    which uses the model detailed in:

    An improved canopy wind model for predicting wind
    adjustment factors and wildland fire behavior
    
    W.J. Massman, J.M. Forthofer, and M.A. Finney
    2017
    https://www.fs.usda.gov/treesearch/pubs/54040
    """
    namedList=["Massman","Input","Output"]
#    colorList=["Yellow","Yellow","green"]
    colorList=["2","0","1"]


    CFMSG=""
    
    dataFile=plotDataPath+"pDat-"+str(int(time.time()))+"-0.csv" #Open the datafile
    ff=open(dataFile,"w")    
    #write the header
#    x_str = "Wind Speed at z ("+unitSet[0]+"),Height (z) ("+unitSet[1]+"),color\n"     
    x_str = "Wind Speed at z ("+unitSet[0]+"),Height (z) ("+unitSet[1]+"),color,name\n"        
    ff.write(x_str)
    
#==============================#
# Figure out the max
# profile height
# and then double it
#==============================#

    zMax=canopy_height #figure out the range over which to generate a plot
    if(z2>=z1):
        zMax=z2 #use out height if its bigger
    if(z1>z2):
        zMax=z1 #use in height if its bigger
    if(canopy_height>z1 and canopy_height>z2):
        zMax=canopy_height #else just use the canopy
    zArray = numpy.linspace(0,2*int(zMax)) #generate an array
    
#==============================#
# Solve for the entire profile #
# Using the  vec method        #
#==============================#
    CF_data = canopyFlow_uzArray(canopyFlowPath,canopyFlowDataPath,uz_1,z1,canopy_height,z0g,LAI,Cd,CR,zArray)
    for i in range(len(CF_data)):
        uz_native = calcUnits.convertToJiveUnits(CF_data[i],unitSet[0])
        hg_native=calcUnits.distFromMetric(zArray[i],unitSet[1])
        ff.write(str(uz_native))
        ff.write(",")
        ff.write(str(hg_native))
#        ff.write(",%s\n"%colorList[0])
        ff.write(",%s,%s\n"%(colorList[0], namedList[0]))

         
#==============================#
# Solve for the user point     #
# Using the single method      #
#==============================#   
    CF_spd = canopyFlow_uzPoint(canopyFlowPath,uz_1,z1,canopy_height,z0g,LAI,Cd,CR,z2)        
    #write the inputs and specific outputs so that the user knows we did what they asked    
    nativeCF_spd = calcUnits.convertToJiveUnits(CF_spd,unitSet[0])
    nativeCF_hgt = calcUnits.distFromMetric(z2,unitSet[1])
    nativeIN_spd = calcUnits.convertToJiveUnits(uz_1,unitSet[0])
    nativeIN_hgt = calcUnits.distFromMetric(z1,unitSet[1])
    
    ff.write(str(nativeCF_spd)) #Out Speed
    ff.write(",")
    ff.write(str(nativeCF_hgt)) #Out Height
#    ff.write(",%s\n"%colorList[2])
    ff.write(",%s,%s\n"%(colorList[2], namedList[2]))
    ff.write(str(nativeIN_spd)) #In Speed
    ff.write(",")
    ff.write(str(nativeIN_hgt)) #In Height
#    ff.write(",%s\n"%colorList[1])
    ff.write(",%s,%s\n"%(colorList[1], namedList[1]))
    ff.close()
    
    return CF_spd,dataFile,CFMSG
    
    
def canopyFlow_uzArray(exec_path,dataPath,uz_1,z1,canopy_height,z0g,LAI,Cd,CR,zArray):
    """    
    Use the vector option inside canopy-flow (branch WHAT)
    write to disk a list of the heights we want
    tell canopy-flow this path
    then get a file with the output heights
    """
    control_arg = "vec"
    inFile=dataPath+"zData/cDat-1.csv"       
    outFile=dataPath+"zData/cDat-2.csv"
    
    uzData=[]    #initialize a list
    
    with open(inFile,"w") as f: #Write the list of heights we want
        for i in range(len(zArray)):
            f.write(str(zArray[i]))
            f.write("\n")
        
    #Generate a list of all the args for canopy-flow
    command_list=[str(exec_path),control_arg,str(uz_1),str(z1),str(canopy_height),
                  str(z0g),str(LAI),str(Cd),str(CR),str(inFile),str(outFile)]
  
    #run canopy-flow
    CF_out = subprocess.check_output(command_list)                             
    CF_out=CF_out.decode()
    ai=CF_out.find("-:") #find the output
    fi=CF_out.find(":-")
    result = CF_out[ai+2:fi]
    if(result=="Done"): #means that it worked!
        with open(outFile,"r") as f: #Open the output file
            fDat = list(csv.reader(f))
            if(fDat[0][0]=="CanopyFlow output:"): #Must have this, otherwise it didn't work
                fDat.pop(0) #get rid of the header
                for i in range(len(fDat)): #iterate over the rest
                    try:                    
                        fSubDat=float(fDat[i][0]) #try to cast it as a float, just to be safe
                    except:
                        fSubDat=float(0) #if we can't cast it as a float, return a 0
            
                    uzData.append(fSubDat) #append to the list
                
                return uzData
            else:
                return [] #if we fail, return an emtpy list
    else:
        return [] #if we really fail, return an empty list
                
def canopyFlow_uzPoint(exec_path,uz_1,z1,canopy_height,z0g,LAI,Cd,CR,z2):
    """
    Pass a single height to canopy Flow
    this doesn't use disk, and instead uses a pipe
    """
    control_arg = "single"

    command_list=[str(exec_path),control_arg,str(uz_1),str(z1),str(canopy_height),
                  str(z0g),str(LAI),str(Cd),str(CR),str(z2)]
                  
    CF_out = subprocess.check_output(command_list)                             
    CF_out=CF_out.decode()
    ai=CF_out.find("-:")
    fi=CF_out.find(":-")
    result = CF_out[ai+2:fi]
    try:
        result = float(result)
    except:
        result = float(0)
        pass
    
    return result   
    
    
##Debug Stuff
#import matplotlib.pyplot as pyplot    
    
#oH = 10 #m
#path = "/home/tanner/src/canopy/build/canopy_flow"
#uz_1 = 10 #mps
#z1 = 120 #m
#canopy_height = 100 #m
#z0g = 0.0075 #m
#LAI = 2.0
#Cd = 0.20
#CR = 0.7
#dataPath = "/home/tanner/src/WHAT/backend/data/" 
#zArray = numpy.linspace(0,z1*2.0)

#cData = canopyFlow_uzArray(path,uz_1,z1,canopy_height,z0g,LAI,Cd,CR,path,dataPath,zArray)
#cData = canopyFlow_uzPoint(path,uz_1,z1,canopy_height,z0g,LAI,Cd,CR,path,oH)

#print(cData)
#pyplot.plot(cData,zArray)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    