'''
Created by Lintong

Simulation Class definition file
DO NOT define function
DO define class
DO NOT script

Upstream
None

Downstream
All

'''

import numpy as np
from misc import *

class SCobj_ForcePoint():
    def __init__(self, forces, moments, mass, inertia, position, rotation, toggle):
        self.forces_local = np.array(forces) #in local frame
        self.moments_local = np.array(moments) #in local frame
        self.mass = mass
        self.inertia = np.array(inertia) #in local frame
        self.position = np.array(position) #position of the point in body frame
        self.rotation = np.array(rotation) #rotation of the point in body frame
        
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        ''' IMPORTANT'''
        ''' All force and moments stored in this class is already rotated to be the next level of reference frame
            !!But the translation component is not included here!!'''
        self.forces  = self.rotation_mat @ np.array(forces) 
        self.moments = self.rotation_mat @ np.array(moments)
        self.inertia = self.rotation_mat @ np.array(inertia) @ self.rotation_mat.T
    
    def Update(self, #variables to update, one element for each term. 
               u_forces=[[0],[0],[0]], 
               u_moments=[[0],[0],[0]],
               u_mass=[[0],[0],[0]],
               u_inertia=[[0],[0],[0]],
               u_position=[[0],[0],[0]],
               u_rotation=[[0],[0],[0]]):
        self.forces_local = [self.forces_local[0](np.array(u_forces[0])), 
                             self.forces_local[1](np.array(u_forces[1])), 
                             self.forces_local[2](np.array(u_forces[2]))]
        self.moments_local = np.array(moments) #in local frame
        self.mass = mass
        self.inertia_local = np.array(inertia) #in local frame
        self.position = np.array(position) #position of the point in body frame
        self.rotation = np.array(rotation) #rotation of the point in body frame
        
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        ''' IMPORTANT'''
        ''' All force and moments stored in this class is already rotated to be the next level of reference frame
            !!But the translation component is not included here!!'''
        self.forces  = self.rotation_mat @ self.forces_local
        self.moments = self.rotation_mat @ self.moments_local
        self.inertia = self.rotation_mat @ self.inertia_local @ self.rotation_mat.T
        
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
        self.position = np.array(position) #position of the aircraft in global space
        self.rotation = np.array(rotation) #rotation of the aircraft in global space
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        self.mass = self.Mass() #total mass of all points attached to the aircraft
        self.cog = self.COG() #location of center of gravity, in body frame
        ''' IMPORTANT'''
        ''' All force and moments stored in this class is already rotated to be the next level of reference frame
            !!But the translation component is not included here!!'''
        self.forces  = self.rotation_mat @ self.Forces() #total force experianced by the aircraft
        self.moments = self.rotation_mat @ self.Moments() #total moments experianced by the aircraft
        self.inertia = self.rotation_mat @ self.Inertia() @ self.rotation_mat.T #inertia tensor of the full aircraft

    def Mass(self): #total mass of all points
        mass = 0
        for i in range(len(self.points)):
            mass += self.points[i].mass
        return mass
    
    def COG(self): #location of center of gravity, in body frame
        cog = [0,0,0]
        for i in range(len(self.points)):
            cog = np.add(cog, self.points[i].mass * self.points[i].position)
        cog = cog/self.mass
        return cog
            
    def Inertia(self): #find inertia tensor of the full aircraft
        inertia = np.array([[0,0,0],[0,0,0],[0,0,0]])
        for i in range(len(self.points)):
            intertia_pt = np.add(intertia_pt, self.points[i].mass * (np.dot(self.points[i].position, self.points[i].position)*np.identity(3) - np.outer(self.points[i].position, self.points[i].position))) #parallel axis theorem
            inertia = np.add(intertia_pt, inertia) 
        inertia = np.add(inertia, self.mass * (np.dot(self.cog, self.cog)*np.identity(3) - np.outer(self.cog, self.cog))) #parallel axis theorem w.r.t. the cog
        return inertia
    
    def Forces(self): 
        forces = np.array([0,0,0])
        for i in range(len(self.points)):
            forces = np.add(forces, self.points[i].forces)
        return forces
    
    def Moments(self):
        moments = np.array([0,0,0])
        for i in range(len(self.points)):
            moments_pt = np.add(self.points[i].moments, np.cross(self.points[i].position + self.cog, self.points[i].forces))
            moments = np.add(moments, moments_pt)
        return moments