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
from misc import *

class SCobj_ForcePoint(): #1 rotor+motor of the copter, using local coordinate system
    def __init__(self, force, moment, mass, inertia, position, rotation):
        self.force = np.array(force) # purely in z direction [0,0,something] 
        self.moments = np.array(moment)
        self.mass = mass
        self.inertia = np.array(inertia) #3x3 tensor
        self.position = np.array(position)
        self.rotation = np.array(rotation)
        
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        
        
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
        self.points = points #list of ForcePoint objects
        self.position = position #position of the aircraft in global space
        self.rotation = rotation #rotation of the aircraft in global space
        self.mass = self.Mass() #total mass of all points attached to the aircraft
        self.cog = self.COG() #location of center of gravity
        self.inertia = self.Inertia() #find inertia tensor of the full aircraft
        self.force = self.Force()
        self.moment = self.Moments()

    def Mass(self):
        mass = 0
        for i in range(len(self.points)):
            mass += self.points[i].mass
        return mass
    
    def COG(self): #TODO add in COG calc
        pass
    
    def Inertia(self):
        inertia = np.array([[0,0,0],[0,0,0],[0,0,0]])
        for i in range(len(self.points)):
            intertia_pt = self.points[i].rotation_mat @ self.points[i].inertia @ self.points[i].rotation_mat.T
            intertia_pt = np.add(intertia_pt, self.points[i].mass * (np.dot(self.points[i].position, self.points[i].position)*np.identity(3) - np.outer(self.points[i].position, self.points[i].position)))
            inertia = np.add(intertia_pt, inertia)
        inertia = np.add(inertia, self.mass * (np.dot(self.cog, self.cog)*np.identity(3) - np.outer(self.cog, self.cog)))
        return inertia
    
    def Force(self):
        force = np.array([0,0,0])
        for i in range(len(self.points)):
            force_pt = self.points[i].force @ self.points[i].rotation_mat
            force = np.add(force, force_pt)
        return force
    
    def Moments(self):
        moments = [0,0,0]
        for i in range(len(self.points)):
            force_pt = self.points[i].force @ self.points[i].rotation_mat
            moments_pt = np.add(self.points[i].moments, np.cross(self.points[i].position, force_pt))
            moments = np.add(moments, moments_pt)
        return moments