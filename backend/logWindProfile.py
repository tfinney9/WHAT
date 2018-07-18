#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 12:54:37 2018

@author: tanner
"""

import calcUnits
import lwp
import sys
import numpy
import time

#Dev Paths
#logPath = "/home/tanner/src/WHAT/backend/log/"
#plotDataPath="/home/tanner/src/WHAT/backend/data/plots/"

#Deploy Paths
logPath = "/home/ubuntu/hd2/src/WHAT/ui/log/"
plotDataPath="/home/ubuntu/hd2/src/WHAT/ui/log/plots/"

lwp_msg=['','','','','']
generate_plot=[False]


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
    
    user_speed = calcUnits.convertToJiveUnits(uz,wind_spd_units)        

    if generate_plot[0]==True:
        datFile=plotDataPath+"pDat-"+str(int(time.time()))+".csv"
        z_arr=numpy.linspace(0,int(metric_height*2))
        
        fWrite = open(datFile,"w")        
        
        x_str = "Wind Speed at z ("+wind_spd_units+"),Height (z) ("+height_units+"),color\n"        
        fWrite.write(x_str)
        
        for i in range(len(z_arr)):
            uz_i = lwp.neutral_uz(metric_speed,z_arr[i],site_roughness,zpd)
            uz_nativeUnits=calcUnits.convertToJiveUnits(uz_i,wind_spd_units)
            hgt_nativeUnits=calcUnits.distFromMetric(z_arr[i],height_units)
            
            if(uz_i<0):
                continue
            if(numpy.isnan(uz_i)==True):
                continue      
            
            fWrite.write(str(uz_nativeUnits))
            fWrite.write(",")
            fWrite.write(str(hgt_nativeUnits))
            fWrite.write("\n")
        
        fWrite.write(str(user_speed))
        fWrite.write(",")
        fWrite.write(str(height))
        fWrite.write(",Output\n")
        fWrite.write(str(wind_spd))
        fWrite.write(",")
        fWrite.write(str(0))
        fWrite.write(",Input\n")
        lwp_msg[4]="Data File Written!"
        fWrite.close()
    else:
        datFile=""
        lwp_msg[4]="Data File Not Written"

    lwp_msg[0]=str(metric_speed)
    lwp_msg[1]=str(metric_height)
    lwp_msg[2]=str(site_height)+" zpd: "+str(zpd)
    lwp_msg[3]=str(uz)    
    
    return user_speed,datFile


#Get args from ui/cli
arg_windSpd=float(sys.argv[1])
arg_spdUnits=str(sys.argv[2])
arg_surface=str(sys.argv[3])
arg_height=float(sys.argv[4])
arg_canopy=float(sys.argv[5])
arg_hgtUnits=str(sys.argv[6])
generate_plot[0]=True

#calculate adjusted speed
adjustedSpeed,dataFileName=calcSpd(arg_windSpd,arg_spdUnits,
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
    f.write(str(lwp_msg[4]))
    f.write("\n")
    f.close()

#return speed and unit
print(round(adjustedSpeed,2),arg_spdUnits,"at",
      arg_height,arg_hgtUnits,":|:",dataFileName,":|:",adjustedSpeed,":|:",arg_height)
