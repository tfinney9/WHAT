#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 12:54:37 2018

@author: tanner
"""

import calcUnits
import lwp
import sys

logPath = "/home/tanner/src/WHAT/backend/log/"

def calcSpd(wind_spd,wind_spd_units,surface,height,height_units):    
    """
    Input user params
    return height adjusted speed
    """
    metric_speed=calcUnits.convertFromJiveUnits(wind_spd,wind_spd_units)
    metric_height=calcUnits.distToMetric(height,height_units)         

    site_roughness=lwp.roughness[surface]
    site_height=lwp.canopy_heights[surface]
    zpd = lwp.calculateZPD(site_height,True)
    uz=lwp.neutral_uz(metric_speed,metric_height,site_roughness,zpd)
    
    user_speed = calcUnits.convertToJiveUnits(uz,wind_spd_units)        
    return user_speed


#Get args from ui/cli
arg_windSpd=float(sys.argv[1])
arg_spdUnits=str(sys.argv[2])
arg_surface=str(sys.argv[3])
arg_height=float(sys.argv[4])
arg_hgtUnits=str(sys.argv[5])

#calculate adjusted speed
adjustedSpeed=calcSpd(arg_windSpd,arg_spdUnits,
                      arg_surface,arg_height,arg_hgtUnits)

with open(logPath+"xLog","w") as f:
    f.write('Inputs:\n')
    f.write(str(arg_windSpd))
    f.write("\n")
    f.write(str(arg_spdUnits))
    f.write("\n")
    f.write(str(arg_surface))
    f.write("\n")
    f.write(str(arg_height))
    f.write("\n")
    f.write(str(arg_hgtUnits))
    f.write("\n")
    f.write("Outputs:")
    f.write("\n")
    f.write(str(adjustedSpeed))
    f.write("\nErrors:\n")
    f.write(str(lwp.error_msg[0]))
    f.write("\n")
    f.close()

#return speed and unit
print(round(adjustedSpeed,2),arg_spdUnits,"at",arg_height,arg_hgtUnits)