# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:17:09 2018

@author: tanner

Implementation of the Albini Canopy Model

Model and Assumptions are detailed in:

ESTIMATING WINDSPEEDS FOR PREDICTING
WILDLAND FIRE BEHAVIOR

F. A. Albini and R. G. Baughman

USDA Forest Service
Research Paper INT-221
June 1979
"""

import numpy

import matplotlib.pyplot as pyplot

def albini_uz(uz_1,z1,z2,canopy_height,crownRatio,z0c):
    """
    Calculate a profile using the albini model
    below the canopy
    and a log wind profile above the canopy
    """
    ZPDOpt="WindNinja"
    ZPD=getZPD(canopy_height,ZPDOpt)
    
    if z2<canopy_height:
        if z1<canopy_height:        
            uz_2 = albiniCanopyToTop_uz(uz_1,crownRatio,canopy_height)
#            return uz_2
        if z1>=canopy_height:
            uz_H = twoPointNeutral_uz(uz_1,z1,canopy_height,z0c,ZPD)
            uz_2 = albiniTopToCanopy_uz(uz_H,crownRatio,canopy_height)
#            return uz_2
    if z2>=canopy_height:
        if(z1<canopy_height):
            uz_H = albiniCanopyToTop_uz(uz_1,crownRatio,canopy_height)
            uz_2 = twoPointNeutral_uz(uz_H,canopy_height,z2,z0c,ZPD)
#            return uz_2
        if(z1>=canopy_height):
            uz_2 = twoPointNeutral_uz(uz_1,z1,z2,z0c,ZPD)
    
    zA,uA = albini_uzDataArray(uz_1,uz_2,z1,z2,canopy_height,crownRatio,z0c)    
    return uz_2,zA,uA

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
    
    Note that if quantity: c2
    
            (z1 - d)
    c2 =    -------- < 1
               z0            
    
    non-physical reults will occur
    
    """ 
    c2 = (z1-d)/(z0)
    if(c2<=1.0):
        return uz_1
    uz_2 = uz_1*(numpy.log((z2-d)/z0)/(numpy.log((z1-d)/z0)))
    if(uz_2<0.0):
        uz_2 = 0.0
    return uz_2

def albiniTopToCanopy_uz(uH,crownRatio,H):
    """
    Page 8 Equation 20 uC(uH)
    """
    f = VFF_fromCrownRatio(crownRatio)
    uC = uH*0.555/(numpy.sqrt(f*H))
    return uC
    
def albiniCanopyToTop_uz(uC,crownRatio,H):
    """
    Modified Equation 20 in terms of uH(uC)
    """
    f = VFF_fromCrownRatio(crownRatio)
    uH = (numpy.sqrt(f*H)*uC)/(0.555)
    return uH
    
def VFF_fromCrownRatio(crownRatio):
    """
    Get the Volume Filling Fraction AKA:
    Crown Filling Fraction <?php (VFF===CFF===f) ?>
    
    See
    FARSITE: Fire Area
    Simulator—Model
    Development and
    Evaluation
    
    Mark A. Finney
    
    Research Paper
    RMRS-RP-4 Revised
    March 1998, revised
    February 2004
    
    https://www.fs.fed.us/rm/pubs/rmrs_rp004.pdf
    
    Page 18 Equation [45]
    <Verbatim> 
    Equation [45] assumes tree crowns are conical, occupying one-third 
    the volume of a cylinder of the same dimensions. Multiplying
    by (p/4) accounts for gaps in a square horizontal packing of 
    circular crowns.
    </Verbatim>
    """    
    f = (crownRatio)*numpy.pi/(12.)
    return f
    
def albini_uzDataArray(uz_1,uz_2,z1,z2,canopy_height,crownRatio,z0c):
    """
    Generate an array of values for plotting using the 
    Albini canopy Model + Log Wind Profile
    """
#    if(canopy_height<=z0c):
#        return []
    
    ZPDOpt="WindNinja"
    ZPD=getZPD(canopy_height,ZPDOpt)
    zMax=canopy_height #figure out the range over which to generate a plot
    if(z2>=z1):
        zMax=z2 #use out height if its bigger
    if(z1>z2):
        zMax=z1 #use in height if its bigger
    if(canopy_height>z1 and canopy_height>z2):
        zMax=canopy_height #else just use the canopy
    #    zArray = numpy.linspace(0,2*int(zMax)) #generate an array

    if(z1<canopy_height):
        uz_H = albiniCanopyToTop_uz(uz_1,crownRatio,canopy_height)
#        print(uz_H)
        zca = numpy.linspace(0,canopy_height,25) #an array of zs for plotting
        uzA = numpy.repeat(uz_H,25) #Velocities within the canopy are the same
#        print(uzA)        
        
        zcb = numpy.linspace(canopy_height,2*int(zMax))
        uzB = []
        for i in range(len(zcb)):
            uz_i = twoPointNeutral_uz(uz_H,canopy_height,zcb[i],z0c,ZPD)
            uzB.append(uz_i)
    
    if(z1>=canopy_height):
        zcb = numpy.linspace(canopy_height,2*int(zMax),25)
        uzB = []
        for i in range(len(zcb)):
            uz_i = twoPointNeutral_uz(uz_1,z1,zcb[i],z0c,ZPD)
            uzB.append(uz_i)
        
        zca = numpy.linspace(0,canopy_height,25) #an array of zs for plotting
       
        if(canopy_height>0.1):
           uz_H = albiniTopToCanopy_uz(uzB[0],crownRatio,canopy_height)
           uzA = numpy.repeat(uz_H,25) #Velocities within the canopy are the same
        else:
            uzA = numpy.repeat(0,25)
        
    outZA = list(zca)
    outZA.extend(list(zcb))

    outUZ = list(uzA)
    outUZ.extend(list(uzB))
    
    return outZA,outUZ
#    print(uzB[0])
#    print(uz_H)
#    pyplot.figure(0)
#    pyplot.plot(uz_1,z1,"ro")
#    pyplot.plot(uz_2,z2,"bo")
#    pyplot.plot(uzB[0],canopy_height,"go")
#    pyplot.hlines(canopy_height,0,20)
#    pyplot.plot(uzA,zca)
#    pyplot.plot(uzB,zcb)
    
    
    
#uz 1 uz 2 z1 z2 canopy_height cR z0c
#albini_uzDataArray(10,17.15,5,30,5,0.2,2)
#albini_uz(10,10,100,50,0.7,0.5)
#albini_uz(10,120,10,100,0.7,0.5)
#albini_uz(10,10,60,100,0.7,0.5)
#albini_uz(10,150,120,100,0.7,0.5)


#zs = numpy.linspace(2.0,50)
#us = []
#ZPD=getZPD(2.0,"WindNinja")
#for i in range(len(zs)):
#    uzu = twoPointNeutral_uz(10,20,zs[i],2.0,ZPD)
#    us.append(uzu)
#pyplot.figure(0)
#pyplot.plot(us,zs,'k.')
#
##pyplot.xlim(-1000,600)
##pyplot.ylim(0,6)
#pyplot.plot(10,2.0,'ro')







