'''
Created by Lintong

Simulation Class definition file
DO NOT define function
DO define class
DO NOT script

Upstream
None

Downstream
model.py

'''

import numpy as np
import misc as misc

class SCobj_ForcePoint():
    def __init__(self, force, moment, mass, inertia, ext_force):
        self.force = force
        self.moments = moment
        self.mass = mass
        self.inertia = inertia
        self.ext_force = ext_force
        self.magnitude = misc.SCfunc_ForceVector()[0]
        self.unit_vector = misc.SCfunc_ForceVector()[1]



class SCobj_BodyState():
    def __init__(self, x, y, z, theta, phi, psi):
        self.x = x 
        self.y = y 
        self.z = z 
        self.theta = theta 
        self.phi = phi
        self.psi = psi 
        self.pos_array = None 
        self.euler_angle_array = None 
        self.state_array = None 

        return 
    
    def matrix_construction(self):
        self.pos_array = np.array([self.x, self.y, self.z])
        self.euler_angle_array = np.array([self.theta, self.phi, self.psi])
        self.state_array = np.array([self.x, self.y, self.z, self.theta, self.phi, self.psi ])
        return self.pos_array, self.euler_angle_array, self.state_array
    
    def force_vector_contruction(self):
