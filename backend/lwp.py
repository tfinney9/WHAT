# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 12:55:13 2018

@author: tanner
"""
import numpy

vonKarmanConstant = 0.41
error_msg=["No Errors To Report!"]
"""
u_star = friction veloctiy -> at ground level velocity
z0 = surface Roughness (meters)
d = zero plane displacement
z = height at uz
"""
def neutral_uz(u_star,z,z0,d):
    if(z-d)<0:
        d=0
        error_msg[0]="z-d<0!"
        
    uz = (u_star)/(vonKarmanConstant) * (numpy.log((z-d)/(z0)))
    return uz
    
"""
Calculate the Zero Plane Displacement
Wikipedia says it can be approximated between 2/3
and 3/4 of the obstacle height...
"""
def calculateZPD(canopy_height,aggressive):
    if aggressive==True:
        return canopy_height*2./3.
    if aggressive==False:
        return canopy_height*3./4.

"""
Roughness Values (meters)
http://www-das.uwyo.edu/~geerts/cwx/notes/chap14/roughness.html
http://collaboration.cmc.ec.gc.ca/science/rpn/gem/gem-climate/Version_3.3.0/dictionary_geophys.pdf
"""
roughness = {"sea water":0.001,
             "glacier":0.0003,
             "lake":0.001,
             "tundra":0.01,
             "long grass":0.08,
             "crops":0.08,
             "urban":1.35,
             "evergreen needle-leaf trees":1.5,
             "evergreen broadleaf trees":3.5,
             "deciduous needle-leaf trees":1.0,
             "deciduous broadleaf trees":2.0,
             "tropical trees":3.0,
             "drought deciduous trees":0.8,
             "shrubs":0.15,
             "short grass and forbs":0.02,
             "urban":1.5,
             "swamp":0.05,
             "desert":0.05,
             "mixed wood forests":1.5}    
            
"""
Canopy Heights
Making these up~~~~~
meters
"""        
#canopy_heights = {"water":0.0,
#                  "zero":0.0,
#                  "low_crops":1.0,
#                  "tall_crops":2.0,
#                  "trees":30.0,
#                  "shrubs":2.0,
#                  "urban":10}   

chWater=0.0
chZero=0.0
chLowCrops=1.0
chHighCrops=2.0
chTree=30.0
chShrub=2.0
chUrban=10.0
 
canopy_heights = {"sea water":chWater,
             "glacier":chZero,
             "lake":chWater,
             "tundra":chZero,
             "long grass":chLowCrops,
             "crops":chHighCrops,
             "urban":chUrban,
             "evergreen needle-leaf trees":chTree,
             "evergreen broadleaf trees":chTree,
             "deciduous needle-leaf trees":chTree,
             "deciduous broadleaf trees":chTree,
             "tropical trees":chTree,
             "drought deciduous trees":chTree,
             "shrubs":chShrub,
             "short grass and forbs":chShrub,
             "swamp":chZero,
             "desert":chZero,
             "mixed wood forests":chTree}   
