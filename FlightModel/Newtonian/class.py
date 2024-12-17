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

class SCobj_ForcePoint(): #1 rotor+motor of the copter, using local coordinate system
    def __init__(self, force, moment, mass, inertia, ext_force):
        self.force = force
        self.moments = moment
        self.mass = mass
        self.inertia = inertia
        self.ext_force = ext_force
        self.magnitude = misc.SCfunc_ForceVector()[0]
        self.unit_vector = misc.SCfunc_ForceVector()[1]
        self.position_array = SCobj_BodyState.matrix_construction()[0]
        self.euler_array = SCobj_BodyState.matrix_construction()[1]
        self.state_array = SCobj_BodyState.matrix_construction()[2]
        






class SCobj_BodyState(): # linking local coordinate system to global  
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
