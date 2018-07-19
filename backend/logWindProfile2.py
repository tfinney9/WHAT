# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:11:05 2018

@author: tanner
"""

import calcUnits
import lwp
import numpy
import time
import getpass

com_msg=['']
dfName=['']
#Dev Paths
if getpass.getuser()=='tanner':
    logPath = "/home/tanner/src/WHAT/backend/log/"
    plotDataPath="/home/tanner/src/WHAT/backend/data/plots/"
#Deploy Paths
else:
    logPath = "/home/ubuntu/hd2/src/WHAT/ui/log/"
    plotDataPath="/home/ubuntu/hd2/src/WHAT/ui/log/plots/"

def writeLogFile():
    lFile=logPath+"xLog"
    with open(lFile,'w') as f:
        f.write(com_msg[0])

#generate data for a plot with just the lwp
def generate_neutralLWPData(mWindSpeed,wsUnits,mInHeight,mOHeight,hUnits,roughness,zpd,userArray):
    dataFile=plotDataPath+"pDat-"+str(int(time.time()))+".csv"
    z_arr=numpy.linspace(0,int(mOHeight*2))
    
    ff=open(dataFile,"w")    
    x_str = "Wind Speed at z ("+wsUnits+"),Height (z) ("+hUnits+"),color\n"        
    ff.write(x_str)
    
    for i in range(len(z_arr)):
        uz_i=lwp.twoPointNeutral_uz(mWindSpeed,mInHeight,z_arr[i],roughness,zpd)
        uz_nativeUnits=calcUnits.convertToJiveUnits(uz_i,wsUnits)
        hgt_nativeUnits=calcUnits.distFromMetric(z_arr[i],hUnits)
            
        if uz_i<0:
            continue
        if numpy.isnan(uz_i)==True:
            continue        
        
        ff.write(str(uz_nativeUnits))
        ff.write(",")
        ff.write(str(hgt_nativeUnits))
        ff.write("\n")
        
    ff.write(str(userArray[0])) #Out Speed
    ff.write(",")
    ff.write(str(userArray[1])) #Out Height
    ff.write(",Output\n")
    ff.write(str(userArray[2])) #In Speed
    ff.write(",")
    ff.write(str(userArray[3])) #In Height
    ff.write(",Input\n")
    ff.close()
    dfName[0]=dataFile       

     
def generate_simpleCanopyAndNeutralLWPData(xdir,mWindSpeed,wsUnits,mInHeight,mOHeight,mCanopyHeight,hUnits,surface,roughness,zpd,userArray):
    atten=lwp.attenuation[surface]
    dataFile=plotDataPath+"pDat-"+str(int(time.time()))+".csv"
    ff=open(dataFile,"w")    
    x_str = "Wind Speed at z ("+wsUnits+"),Height (z) ("+hUnits+"),color\n"        
    ff.write(x_str)
    uza=[]
    #==================================================================================
    # Solve LWP Then Canopy
    #==================================================================================
    if xdir==0: #init Height > Surface Height (LWP)
        z=numpy.linspace(mCanopyHeight,2.5*mCanopyHeight)
        for i in range(len(z)):
            uzlwp=lwp.twoPointNeutral_uz(mWindSpeed,mInHeight,z[i],roughness,zpd)
            if uzlwp<0:
                continue
            if numpy.isnan(uzlwp)==True:
                continue  
            
            uza.append(uzlwp)
            uz_nativeUnits=calcUnits.convertToJiveUnits(uzlwp,wsUnits)
            hgt_nativeUnits=calcUnits.distFromMetric(z[i],hUnits)
            ff.write(str(uz_nativeUnits))
            ff.write(",")
            ff.write(str(hgt_nativeUnits))
            ff.write("\n")

        #Now solve the canopy compnent using the lowest level speed in the LWP           
        cz=numpy.linspace(0,mCanopyHeight)
        for i in range(len(cz)):
            uzic=lwp.simpleCanopyModel(uza[0],atten,cz[i],mCanopyHeight)
            if uzic<0:
                continue
            if numpy.isnan(uzic)==True:
                continue  
            
            uz_nativeUnits=calcUnits.convertToJiveUnits(uzic,wsUnits)
            hgt_nativeUnits=calcUnits.distFromMetric(cz[i],hUnits)
            ff.write(str(uz_nativeUnits))
            ff.write(",")
            ff.write(str(hgt_nativeUnits))
            ff.write("\n")
            
    #==================================================================================
    # Canopy THEN LWP
    #==================================================================================
    if xdir==1: #init height is within the canopy    
        z=numpy.linspace(0,mCanopyHeight)
        for i in range(len(z)):
            uzic=lwp.simpleCanopyModel(mWindSpeed,atten,z[i],mInHeight)
            if uzic<0:
                continue
            if numpy.isnan(uzic)==True:
                continue  
        
            uza.append(uzic)
            uz_nativeUnits=calcUnits.convertToJiveUnits(uzic,wsUnits)
            hgt_nativeUnits=calcUnits.distFromMetric(z[i],hUnits)
            ff.write(str(uz_nativeUnits))
            ff.write(",")
            ff.write(str(hgt_nativeUnits))
            ff.write("\n")
        
        #Solve the LWP with the uppermost canopy solution
        cz=numpy.linspace(mCanopyHeight,int(2.5*mCanopyHeight))
        for i in range(len(cz)):
            uzlwp=lwp.twoPointNeutral_uz(uza[-1],mCanopyHeight,cz[i],roughness,zpd)
            if uzlwp<0:
                continue
            if numpy.isnan(uzlwp)==True:
                continue
            
            uz_nativeUnits=calcUnits.convertToJiveUnits(uzlwp,wsUnits)
            hgt_nativeUnits=calcUnits.distFromMetric(cz[i],hUnits)
            ff.write(str(uz_nativeUnits))
            ff.write(",")
            ff.write(str(hgt_nativeUnits))
            ff.write("\n")
    
    #Finally Write the Data Array stuff 
    ff.write(str(userArray[0])) #Out Speed
    ff.write(",")
    ff.write(str(userArray[1])) #Out Height
    ff.write(",Output\n")
    ff.write(str(userArray[2])) #In Speed
    ff.write(",")
    ff.write(str(userArray[3])) #In Height
    ff.write(",Input\n")
    ff.close()
    dfName[0]=dataFile      


def calc_neutralLWP(windSpeed,windSpeedUnits,initialHeight,canopyHeight,outputHeight,heightUnits,surface):
    """
    Execute Function for the
    neutral stability log wind profile function
    """    
    #Do some unit conversions
    mSpeed=calcUnits.convertFromJiveUnits(windSpeed,windSpeedUnits)
    mInitHeight=calcUnits.distToMetric(initialHeight,heightUnits)
    mCanopyHeight=calcUnits.distToMetric(canopyHeight,heightUnits)
    mOutHeight=calcUnits.distToMetric(outputHeight,heightUnits)
    
    f_msg="Inputs:\nWindSpeed: "+str(windSpeed)+" "+windSpeedUnits+\
    " ("+str(mSpeed)+" mps)\n"
    f_msg+="Height: "+str(initialHeight)+" "+heightUnits+" ("+str(mInitHeight)+" m)"+"\n"
    f_msg+="Canopy Height: "+str(canopyHeight)+" "+heightUnits+" ("+str(mCanopyHeight)+" m)"+"\n"
    f_msg+="Out Height: "+str(outputHeight)+" "+heightUnits+" ("+str(mOutHeight)+" m)"+"\n"
    f_msg+="Surface: "+surface+"\n"
    
    #Get some data from lwp
    surfaceRoughness=lwp.roughness[surface]
    #calulate the zero plane displacement
    zpd=lwp.calculateZPD(mCanopyHeight,False) 
    
    #do the real math
    uz=lwp.twoPointNeutral_uz(mSpeed,mInitHeight,mOutHeight,surfaceRoughness,zpd)
    
    #Convert back to user units
    outSpeed=calcUnits.convertToJiveUnits(uz,windSpeedUnits)  
    
    f_msg+="Outputs:\n"
    f_msg+="ZPD: "+str(zpd)+" m\n"    
    f_msg+="Uz: "+str(uz)+" mps\n"
    f_msg+="Out Speed: "+str(outSpeed)+" "+windSpeedUnits+"\n"
    com_msg[0]=f_msg
    
    uA=[outSpeed,outputHeight,windSpeed,initialHeight]    
    generate_neutralLWPData(mSpeed,windSpeedUnits,mInitHeight,mOutHeight,heightUnits,surfaceRoughness,zpd,uA)
    writeLogFile()    
    
    return outSpeed
    
def calc_simpleCanopyAndNeutralLWP(windSpeed,windSpeedUnits,initialHeight,canopyHeight,outputHeight,heightUnits,surface):
    """
    Adds the simple canopy model to allow calculations within
    the canopy and to extrapolate outwards
    """
    mSpeed=calcUnits.convertFromJiveUnits(windSpeed,windSpeedUnits)
    mInitHeight=calcUnits.distToMetric(initialHeight,heightUnits)
    mCanopyHeight=calcUnits.distToMetric(canopyHeight,heightUnits)
    mOutHeight=calcUnits.distToMetric(outputHeight,heightUnits)

    surfaceRoughness=lwp.roughness[surface]
    zpd=lwp.calculateZPD(mCanopyHeight,False) 
    
    f_msg="Inputs:\nWindSpeed: "+str(windSpeed)+" "+windSpeedUnits+\
    " ("+str(mSpeed)+" mps)\n"
    f_msg+="Height: "+str(initialHeight)+" "+heightUnits+" ("+str(mInitHeight)+" m)"+"\n"
    f_msg+="Canopy Height: "+str(canopyHeight)+" "+heightUnits+" ("+str(mCanopyHeight)+" m)"+"\n"
    f_msg+="Out Height: "+str(outputHeight)+" "+heightUnits+" ("+str(mOutHeight)+" m)"+"\n"
    f_msg+="Surface: "+surface+"\n"


    uz=[-1]
    agov=[-1]
    
    if mInitHeight>mCanopyHeight: #In LWP for inlet
        agov[0]=0
        if mOutHeight>mCanopyHeight: #In LWP for outlet
            uz[0]=lwp.twoPointNeutral_uz(mSpeed,mInitHeight,mOutHeight,surfaceRoughness,zpd)
        if mOutHeight<=mCanopyHeight: #In Canopy For Outlet
            uz[0]=lwp.calcLWPToSimpleCanopy(mSpeed,mInitHeight,mOutHeight,mCanopyHeight,surfaceRoughness,surface,zpd)
    
    if mInitHeight<mCanopyHeight: #in the Canopy for inlet
        agov[0]=1
        if mOutHeight<mCanopyHeight: #still in the canopy
            uz[0]=lwp.calcIntraSimpleCanopy(mSpeed,mOutHeight,mInitHeight,surface)
        if mOutHeight>=mCanopyHeight: #in the log for out
            uz[0]=lwp.calcSimplecCanopyToLWP(mSpeed,mOutHeight,mCanopyHeight,surfaceRoughness,mInitHeight,surface,zpd)   
    
    
    outSpeed=calcUnits.convertToJiveUnits(uz[0],windSpeedUnits)  
    
    f_msg+="Outputs:\n"
    f_msg+="ZPD: "+str(zpd)+" m\n"    
    f_msg+="Uz: "+str(uz)+" mps\n"
    f_msg+="Out Speed: "+str(outSpeed)+" "+windSpeedUnits+"\n"
    com_msg[0]=f_msg
    writeLogFile()
    
    uA=[outSpeed,outputHeight,windSpeed,initialHeight]    
    generate_simpleCanopyAndNeutralLWPData(agov[0],mSpeed,windSpeedUnits,mInitHeight,mOutHeight,mCanopyHeight,heightUnits,surface,surfaceRoughness,zpd,uA)    
    return outSpeed