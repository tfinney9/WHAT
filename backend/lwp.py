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
    uz = (u_star)/(vonKarmanConstant) * (numpy.log((z-d)/(z0)))
    return uz
    
"""
uz_2 = velocity at z=z2
uz_1 = velocity at z=z1
d = zero plane displacement (meters)
z0 = surface roughness (meters)
"""     
def twoPointNeutral_uz(uz_1,z1,z2,z0,d):
    uz_2 = uz_1*(numpy.log((z2-d)/z0)/(numpy.log((z1-d)/z0)))
    return uz_2
    
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
As Described by "An Introduction to Environmental Biophysics"
(Campbell, Norman)
Page 72 equation 5.4
"""
def simpleCanopyModel(u_h,a,z,h):
    u_z = u_h*numpy.exp(a*(z/h-1.))
    return u_z
    

def calcSimplecCanopyToLWP(u_h,z_out,canopy_height,
                          canopy_roughness,initial_height,surface,ZPD):
    """
    Height is less than the canopy
    use the simple canopy model to find
    the wind at the top of the canopy 
    and then use that to find the wind at the desired z
    """
    canopy_attenuation=attenuation[surface]
    u_top=simpleCanopyModel(u_h,canopy_attenuation,
                            canopy_height,initial_height)
    u_lwp=twoPointNeutral_uz(u_top,canopy_height,z_out,
                             canopy_roughness,ZPD)
                             
    return u_lwp

def calcLWPToSimpleCanopy(uz_init,init_height,z_out,canopy_height,canopy_roughness,surface,ZPD):
    """
    Reverse of above
    """
    canopy_attenuation=attenuation[surface]
    u_top=twoPointNeutral_uz(uz_init,init_height,canopy_height,canopy_roughness,ZPD)
    u_inCanopy=simpleCanopyModel(u_top,canopy_attenuation,z_out,canopy_height)
    return u_inCanopy

def calcIntraSimpleCanopy(u,z_out,z_in,surface):
    canopy_attenuation=attenuation[surface]
    u_inCanopy=simpleCanopyModel(u,canopy_attenuation,z_out,z_in)
    return u_inCanopy



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
Attentuation Coefficients
"""
atten_conifer=1.1
atten_deciduous=0.4
atten_zero=0.0
atten_wheat=2.5
atten_corn=2.0
atten_crapcorn=2.8
atten_sunflower=1.3

attenuation = {"sea water":atten_zero,
             "glacier":atten_zero,
             "lake":atten_zero,
             "tundra":atten_zero,
             "long grass":atten_wheat,
             "crops":atten_corn,
             "urban":atten_zero,
             "evergreen needle-leaf trees":atten_conifer,
             "evergreen broadleaf trees":atten_deciduous,
             "deciduous needle-leaf trees":atten_conifer,
             "deciduous broadleaf trees":atten_deciduous,
             "tropical trees":atten_deciduous,
             "drought deciduous trees":atten_conifer,
             "shrubs":atten_sunflower,
             "short grass and forbs":atten_sunflower,
             "swamp":atten_deciduous,
             "desert":atten_zero,
             "mixed wood forests":atten_conifer}    

            
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
