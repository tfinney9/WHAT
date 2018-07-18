#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 12:54:37 2018

@author: tanner
"""

import calcUnits
import lwp
import sys

#Dev Paths
#logPath = "/home/tanner/src/WHAT/backend/log/"

#Deploy Paths
logPath = "/home/ubuntu/hd2/src/WHAT/ui/log/"

lwp_msg=['','','','']

def calcSpd(wind_spd,wind_spd_units,surface,height,height_units,canopy_height):    
    """
    Input user params
    return height adjusted speed
    """
    metric_speed=calcUnits.convertFromJiveUnits(wind_spd,wind_spd_units)
    metric_height=calcUnits.distToMetric(height,height_units)         

    site_roughness=lwp.roughness[surface]
    site_height = calcUnits.distToMetric(canopy_height,height_units)
    zpd=lwp.calculateZPD(site_height,False)
    uz=lwp.neutral_uz(metric_speed,metric_height,site_roughness,zpd)

    lwp_msg[0]=str(metric_speed)
    lwp_msg[1]=str(metric_height)
    lwp_msg[2]=str(site_height)+" zpd: "+str(zpd)
    lwp_msg[3]=str(uz)    
    
    user_speed = calcUnits.convertToJiveUnits(uz,wind_spd_units)        
    return user_speed


#Get args from ui/cli
arg_windSpd=float(sys.argv[1])
arg_spdUnits=str(sys.argv[2])
arg_surface=str(sys.argv[3])
arg_height=float(sys.argv[4])
arg_canopy=float(sys.argv[5])
arg_hgtUnits=str(sys.argv[6])

#calculate adjusted speed
adjustedSpeed=calcSpd(arg_windSpd,arg_spdUnits,
                      arg_surface,arg_height,arg_hgtUnits,arg_canopy)

with open(logPath+"xLog","w") as f:
    f.write('Inputs:\n')
    f.write("Wind Speed: ")
    f.write(str(arg_windSpd))
    f.write(" ")
    f.write(str(arg_spdUnits))
    f.write("\n")
    f.write("Metric Wind Speed: ")
    f.write(str(lwp_msg[0]))
    f.write("\n")
    f.write("Surface: ")
    f.write(str(arg_surface))
    f.write("\n")
    f.write("Canopy Height: ")
    f.write(str(arg_canopy))
    f.write("\n")
    f.write("Height: ")
    f.write(str(arg_height))
    f.write("\n")
    f.write(str(arg_hgtUnits))
    f.write("\n")
    f.write("Metric Height: ")
    f.write(str(lwp_msg[1]))
    f.write("\nCH/ZPD: ")
    f.write(str(lwp_msg[2]))
    f.write("\n")
    f.write("Outputs:")
    f.write("\n")
    f.write("m_speed_out: ")
    f.write(lwp_msg[3])
    f.write("\n")
    f.write("user_speed: ")
    f.write(str(adjustedSpeed))
#    f.write("\n")
    f.write("\nErrors:\n")
    f.write(str(lwp.error_msg[0]))
    f.write("\n")
    f.close()

#return speed and unit
print(round(adjustedSpeed,2),arg_spdUnits,"at",arg_height,arg_hgtUnits)
