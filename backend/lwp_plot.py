# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 16:00:34 2018

@author: tanner
"""

import matplotlib.pyplot as pyplot
import lwp
import numpy


surf_type='evergreen needle-leaf trees'

surf_height=lwp.canopy_heights[surf_type]
surf_rough=lwp.roughness[surf_type]

u0=4
z=numpy.linspace(0,100)
uz=[]

for i in range(len(z)):
    ui=lwp.neutral_uz(u0,z[i],surf_rough,surf_height)
    uz.append(ui)
    
pyplot.plot(uz,z)


