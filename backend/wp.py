# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 10:47:44 2018

Wind Profile Important stuff

@author: tanner
"""

import numpy
import subprocess
import time
import calcUnits
import csv
from multiprocessing import Pool as ThreadPool
from functools import partial

class windProfile():
    """
    Generate a wind Profile
    Inputs and paths must be set
    """
    status_msg=""
    profile="stable"
    canopyFlowPath=""
    PlotDataPath=""    
    PlotDataFile=""    
    surfaceDataFile=""
    
    inputWindSpeed = 0.0 #meters per second
    inputWindHeight = 0.0  #meters
    surfaceRoughess = 0.0 #meters z0
    surface = ""
    zpd = 0.0 #Zero Plane Displacement rough_d
    canopy_height = 0.0 #rough_h   
    outputWindHeight = 0.0
    outputWindSpeed = 0.0
    inWindHeight=(inputWindHeight+canopy_height)-zpd
    
    leafAreaIndex = 3.28 #This is the number of leaves you hit on your way down
    dragCoeff = 0.20
    crownRatio = 0.7 
    subCanopyRoughness = 0.0075 #This is the roughness of the ground below the canopy   
    
    heightUnits="m"
    speedUnits="mps"
    manualCanopy=False
    dumpCanopy=0.0
    
    useMutliProc=False
    
    def set_InputWindSpeed(self,wspd,ws_units):
        self.inputWindSpeed=calcUnits.convertFromJiveUnits(wspd,ws_units)
        self.speedUnits=ws_units
    
    def set_InputWindHeight(self,inhgt,hgt_units):
        self.inputWindHeight=calcUnits.distToMetric(inhgt,hgt_units)
        self.heightUnits=hgt_units
    
    def set_OutputWindHeight(self,outhgt,hgt_units):
        self.outputWindHeight=calcUnits.distToMetric(outhgt,hgt_units)
        self.heightUnits=hgt_units    
    
    def set_CanopyHeight(self,cpyhgt,hgt_units):
        self.canopy_height = calcUnits.distToMetric(cpyhgt,hgt_units)
        self.heightUnits=hgt_units   
        self.manualCanopy=True
        
    def set_surface(self,surface):
        if self.manualCanopy==False:
            self.surface,self.canopy_height,self.leafAreaIndex,self.dragCoeff = getSurfaceProperties(surface,self.surfaceDataFile)
        else:
            self.surface,self.dumpCanopy,self.leafAreaIndex,self.dragCoeff = getSurfaceProperties(surface,self.surfaceDataFile)
            
    def get_InputWindSpeed(self,ws_units):
        return calcUnits.convertToJiveUnits(self.inputWindSpeed,ws_units)

    def get_OutputWindHeight(self,hgt_units):
        return calcUnits.distFromMetric(self.outputWindHeight,hgt_units)
    
    def get_InputWindHeight(self,hgt_units):
        return calcUnits.distFromMetric(self.inputWindHeight,hgt_units)
            
    def get_CanopyHeight(self,hgt_units):
        return calcUnits.distFromMetric(float(self.canopy_height),hgt_units)
    
    def get_OutputWindSpeed(self,ws_units):
        return calcUnits.convertToJiveUnits(self.outputWindSpeed,ws_units)
        
        
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
        use the Albini canopy model
        """
        self.outputWindSpeed=self.outputWindSpeed
        
    def cf_uz(self):
        """
        use the Masserman canopy model
        """
        self.outputWindSpeed,self.PlotDataFile,self.status_msg = canopyFlow_uz(self.inputWindSpeed,
                                                                             self.inputWindHeight,
                                                                             self.outputWindHeight,
                                                                             self.canopy_height,
                                                                             self.canopyFlowPath,
                                                                             self.subCanopyRoughness,
                                                                             self.leafAreaIndex,
                                                                             self.dragCoeff,
                                                                             self.crownRatio,
                                                                             self.PlotDataPath,
                                                                             [self.speedUnits,
                                                                              self.heightUnits],
                                                                              self.useMutliProc)
                                          
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

                                                             

 
def twoPointNeutral_uz(uz_1,z1,z2,z0,d):
    """
    uz_2 = velocity at z=z2
    uz_1 = velocity at z=z1
    d = zero plane displacement (meters)
    z0 = surface roughness (meters)
    """     
    uz_2 = uz_1*(numpy.log((z2-d)/z0)/(numpy.log((z1-d)/z0)))
    return uz_2

def getZPD(canopy_height,model):
    if(model=="three_quaters"):
        return canopy_height*3./4.
    if(model=="two_thirds"):
        return canopy_height*3./4.
    if(model=="WindNinja"):
        return canopy_height*0.63 #See Line 3589 in ninja.cpp
        
def linear_uz(uz_1,z1,zpd,canopy_height):
    return 0

def albini_uz():
    return 0

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
    return sDat[sLoc[0]][0][0],sDat[sLoc[0]][0][1],sDat[sLoc[0]][0][2],sDat[sLoc[0]][0][3]

def canopyFlowMulti_uz(outHeight,path,uz_1,z1,canopy_height,z0g,LAI,Cd,CR,spdUnits):
    """
    Multiprocessing option for plotting
    """
    commandList = [str(path),str(uz_1),str(z1),str(outHeight),str(canopy_height),str(z0g),str(LAI),str(Cd),str(CR)]
    CF_out = subprocess.check_output(commandList) #solve for the height
    CF_out=CF_out.decode()
    ai=CF_out.find("-:")
    fi=CF_out.find(":-")
    try:
        uz_i = float(CF_out[ai+2:fi])    #try to cast as float
    except:
        uz_i = 0.0 #this probably means its nan and therefore just throw a zero
        pass

    uz_native=calcUnits.convertToJiveUnits(uz_i,spdUnits) #convert each thing back to local units
    return uz_native

def canopyFlow_uz(uz_1,z1,z2,canopy_height,path,z0g,LAI,Cd,CR,dataPath,unitSet,optMulti):
    """
    use the Masserman/Forthofer Canopy Model to 
    generate a wind profile
    
    Also generate datapoints for plotting
    """
    commandList = [str(path),str(uz_1),str(z1),str(z2),str(canopy_height),str(z0g),str(LAI),str(Cd),str(CR)]
#    print(commandList)
    CF_out = subprocess.check_output(commandList) #Solve for the requested height
    CF_out=CF_out.decode()
    
    ai=CF_out.find("-:")
    fi=CF_out.find(":-")
#    print(CF_out)
    try:
        CF_spd = float(CF_out[ai+2:fi]) #find that height in the output
    except:
        CF_spd=0.0
        pass
    
#    CF_spd = CF_out[ai+2:fi]
    CFMSG=""
    
    dataFile=dataPath+"pDat-"+str(int(time.time()))+".csv" #Open the datafile
    ff=open(dataFile,"w")    
    #write the header
    x_str = "Wind Speed at z ("+unitSet[0]+"),Height (z) ("+unitSet[1]+"),color\n"        
    ff.write(x_str)
    
    #Generate an Array of heights to iterate over
    zMax=canopy_height #figure out the range over which to generate a plot
    if(z2>=z1):
        zMax=z2 #use out height if its bigger
    if(z1>z2):
        zMax=z1 #use in height if its bigger
    if(canopy_height>z1 and canopy_height>z2):
        zMax=canopy_height #else just use the canopy
    
    zArray = numpy.linspace(0,2*int(zMax)) #generate an array
    
    if optMulti==False:
        for i in range(len(zArray)):
            commandList = [str(path),str(uz_1),str(z1),str(zArray[i]),str(canopy_height),str(z0g),str(LAI),str(Cd),str(CR)]
            CF_out = subprocess.check_output(commandList) #solve for each height
            CF_out=CF_out.decode()
            ai=CF_out.find("-:")
            fi=CF_out.find(":-")
            try:
                uz_i = float(CF_out[ai+2:fi])    #try to cast as float
            except:
                uz_i = 0.0 #this probably means its nan and therefore just throw a zero
                pass
            if uz_i<0:
                continue
            if numpy.isnan(uz_i)==True:
                continue
            
            uz_native=calcUnits.convertToJiveUnits(uz_i,unitSet[0]) #convert each thing back to local units
            hg_native=calcUnits.distFromMetric(zArray[i],unitSet[1])
            ff.write(str(uz_native))
            ff.write(",")
            ff.write(str(hg_native))
            ff.write("\n")
            
    if optMulti==True:
        pool = ThreadPool(len(zArray))
        component = partial(canopyFlowMulti_uz,path=path,uz_1=uz_1,
                            z1=z1,canopy_height=canopy_height,z0g=z0g,
                            LAI=LAI,Cd=Cd,CR=CR,spdUnits=unitSet[0])
        result = pool.map(component,zArray)
        pool.close()
        pool.join()
        
        for i in range(len(zArray)):
            hg_native=calcUnits.distFromMetric(zArray[i],unitSet[1])
            ff.write(str(result[i]))
            ff.write(",")
            ff.write(str(hg_native))
            ff.write("\n")
                
        
    #write the inputs and specific outputs so that the user knows we did what they asked    
    nativeCF_spd = calcUnits.convertToJiveUnits(CF_spd,unitSet[0])
    nativeCF_hgt = calcUnits.distFromMetric(z2,unitSet[1])
    nativeIN_spd = calcUnits.convertToJiveUnits(uz_1,unitSet[0])
    nativeIN_hgt = calcUnits.distFromMetric(z1,unitSet[1])
    
    ff.write(str(nativeCF_spd)) #Out Speed
    ff.write(",")
    ff.write(str(nativeCF_hgt)) #Out Height
    ff.write(",Output\n")
    ff.write(str(nativeIN_spd)) #In Speed
    ff.write(",")
    ff.write(str(nativeIN_hgt)) #In Height
    ff.write(",Input\n")
    ff.close()
    
    return CF_spd,dataFile,CFMSG