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
physics.py

NOT ACTAULLY USED
'''
import numpy as np
import classbank

vel1 = [0,10,0]
rot  = [0,4,0]
r = [5,5,0]
vel2 = vel1 + np.cross(rot, r)
print(vel2)