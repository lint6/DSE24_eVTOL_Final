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
    def __init__(self, force, moment, mass, inertia, position, rotation):
        self.force = np.array(force) # purely in z direction [0,0,something] 
        self.moments = np.array(moment)
        self.mass = mass
        self.inertia = np.array(inertia) #3x3 tensor
        self.position = np.array(position)
        self.rotation = np.array(rotation)
        return 




class SCobj_BodyState(): # linking local coordinate system to global UNUSED  
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
    
class SCobj_Aircraft():
    def __init__(self, points, position, rotation):
        self.points = points #list of objects
        self.position = position
        self.rotation = rotation
        self.mass = self.Mass()

    def Mass(self):
        mass = 0
        for i in range(len(self.points)):
            mass += self.points[i].mass
        return mass
            
    def Inertia(self):
        inertia = 0
        for i in ra