'''
Created by Lintong

Simulation UI file
DO NOT define function
DO NOT define class
DO script

Upstream
aircraft.py

Downstream
None
'''

import numpy as np
# from classbank import SCobj_ForcePoint, SCobj_Aircraft

# rotor_fr = SCobj_ForcePoint(force=[0,0,1], 
#                             moment=[0,0,0], 
#                             mass=20, 
#                             inertia=0)
pos = np.array([1,0,1])
A = np.array([[5,0,0],[0,5,0],[0,0,5]])
print(
    np.add(A, 10 * (np.dot(pos, pos)*np.identity(3) - np.outer(pos, pos)))
)