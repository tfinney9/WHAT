# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 13:32:24 2018

@author: tanner

Units utility for WHAT
uses pint to convert wind speeds and heights between various systems
Also does temperature
"""

import pint

u=pint.UnitRegistry()

"""
Wind Speed

Valid Units for Wind Speed

mps
kph
mph
kts
cph
fpf

Convert all to meters per second
"""

def convertFromJiveUnits(tribal_value,unit):
    if(unit=="mps"):
        return tribal_value
    else:
        if(unit=="kph"):
            spd=tribal_value*u.kph
            return (spd.to(u.meter/u.second)).magnitude
        if(unit=="mph"):
            spd=tribal_value*u.mph
            return (spd.to(u.meter/u.second)).magnitude
        if(unit=="kts"):
            spd=tribal_value*u.kts
            return (spd.to(u.meter/u.second)).magnitude
        if(unit=="cph"):
            spd=tribal_value*u.chain/u.hour
            return (spd.to(u.meter/u.second)).magnitude
        if(unit=="fpf"):
            spd=tribal_value*u.furlong/u.fortnight
            return (spd.to(u.meter/u.second)).magnitude

    
def convertToJiveUnits(metric_value,to_unit):
    if(to_unit=="mps"):
        return metric_value
    else:
        if(to_unit=="kph"):
            spd=metric_value*u.meter/u.second
            return (spd.to(u.kph)).magnitude
        if(to_unit=="mph"):
            spd=metric_value*u.meter/u.second
            return (spd.to(u.mph)).magnitude
        if(to_unit=="kts"):
            spd=metric_value*u.meter/u.second
            return (spd.to(u.kts)).magnitude
        if(to_unit=="cph"):
            spd=metric_value*u.meter/u.second
            return (spd.to(u.chain/u.hour)).magnitude  
        if(to_unit=="fpf"):
            spd=metric_value*u.meter/u.second
            return (spd.to(u.furlong/u.fortnight)).magnitude 
        
"""
Distance (Height)

Valid Units

Meters
Feet
Chains
Furlongs


"""    

def distToMetric(tribal_value,unit):
    if(unit=="m"):
        return tribal_value
    else:
        if(unit=="ft"):
            dst=tribal_value*u.feet
            return (dst.to(u.meter)).magnitude
        if(unit=="chain"):
            dst=tribal_value*u.chain
            return (dst.to(u.meter)).magnitude
        if(unit=="furlong"):
            dst=tribal_value*u.furlong
            return (dst.to(u.meter)).magnitude
            
def distFromMetric(metric_value,to_unit):
    if(to_unit=="m"):
        return metric_value
    else:
        if(to_unit=="ft"):
            dst=metric_value*u.m
            return (dst.to(u.ft)).magnitude
        if(to_unit=="chain"):
            dst=metric_value*u.m
            return (dst.to(u.chain)).magnitude
        if(to_unit=="furlong"):
            dst=metric_value*u.m
            return (dst.to(u.furlong)).magnitude

def tempETM(temperature):
    """
    Converts Temp from F To C
    """
    tempQ=u.Quantity
    fTemp=tempQ(temperature,u.degF)
    cTemp=fTemp.to(u.degC)
    return cTemp.magnitude

def tempMTE(temperature):
    """
    Converts temp from C To F
    """
    tempQ=u.Quantity
    cTemp=tempQ(temperature,u.degC)
    fTemp=cTemp.to(u.degF)
    return fTemp.magnitude
    
def tempToK(temp_C):
        return temp_C+273.15
    
def tempFromK(temp_K):
        return temp_K-273.15
        
        
        
        
        
        
        
        
        
        
        
        