'''
NOT ACTAULLY USED

Created by Lintong

Simulation Model file
DO define function
DO define class
DO NOT script

Upstream
misc.py
class.py

Downstream
component.py
aircraft.py

'Functions that handle the bulk of physical relations'
'''
import numpy as np

def SCfunc_Inertia_Disc(m,l):
    I_xx = 0
    I_yy = 0 
    I_zz = (1/12) * m * l**2 
    return I_xx, I_yy, I_zz

def SCfunc_Inertia_Cylinder(m, r, l): # z going through the circle surface, 
    I_xx = ((1/4) * m * r**2) + ((1/12) * m * l**2)
    I_yy = ((1/4) * m * r**2) + ((1/12) * m * l**2)
    I_zz = ((1/2) * m * r**2)
    return I_xx, I_yy, I_zz


def SCfunc_Intertia_Box(m, w, d, h): # w = width(y), d= depth(x), h = height(z)
    I_xx = ((1/12) * m * (w**2 + h**2))
    I_yy = ((1/12) * m * (h**2 + d**2))
    I_zz = ((1/12) * m * (w**2 + d**2))
    return I_xx, I_yy, I_zz

def SCfunc_Intertia_Sphere(m, r):
    I_xx = (2/5) * m * r**2
    I_yy = (2/5) * m * r**2
    I_zz = (2/5) * m * r**2
    return I_xx, I_yy, I_zz