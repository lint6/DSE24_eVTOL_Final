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
    def __init__(self, forces, moments, mass, inertia, position, rotation):
        #Functions
        self.forces_func = forces  # [0,0,0]
        self.moments_func = moments
        self.mass_func = mass
        self.inertia_func = inertia
        self.position_func = position
        self.rotation_func = rotation
        #Values
        self.forces = forces*1
        self.moments = moments*1
        self.mass = mass*1
        self.inertia = inertia*1
        self.position = position*1
        self.rotation = rotation*1
        #rotation matrices
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        self.Update()
        ''' IMPORTANT'''
        ''' All force and moments stored in this class is already rotated to be in the body frame
            !!positions and rotation are in body frame!!'''

    def Update(self, #variables to update, one element for each term. 
               u_forces   = [[0],[0],[0]],  #VARIABLES ONLY IF THE FORCE IS GIVEN BY A FUNCTION
               u_moments  = [[0],[0],[0]],  
               u_mass     =  [0],            
               u_inertia  = [[0,0,0],       
                             [0,0,0],       
                             [0,0,0]],      
               u_position = [[0],[0],[0]], 
               u_rotation = [[0],[0],[0]]):

        function_def = type(lambda x: x) #telling Python what a lambda function is so we can do conditions later
        for i in range(len(self.forces_func)): #update force base on functions
            if type(self.forces_func[i]) == function_def:
                self.forces[i] = float(self.forces_func[i](np.array(u_forces[i])))
        self.forces_local = np.array(self.forces)

        for i in range(len(self.moments_func)): #update moments base on functions
            if type(self.moments_func[i]) == function_def:
                self.moments[i] = float(self.moments_func[i](np.array(u_moments[i])))
        self.moments_local = np.array(self.moments)
        
        if type(self.mass_func) == function_def: #update mass base on functions
            self.mass = float(self.mass_func(u_mass))
        
        for i in range(len(self.inertia_func)): #update inertia base on functions
            for j in range(len(self.inertia_func[i])):
                if type(self.inertia_func[i][j]) == function_def:
                    self.inertia[i] = float(self.inertia_func[i][j](np.array(u_inertia[i][j])))
        self.inertia_local = np.array(self.inertia)

        for i in range(len(self.position_func)): #update position base on functions
            if type(self.position_func[i]) == function_def:
                self.position[i] = float(self.position_func[i](np.array(u_position[i])))
        self.position = np.array(self.position)
        
        for i in range(len(self.rotation_func)): #update rotation base on functions
            if type(self.rotation_func[i]) == function_def:
                self.rotation[i] = float(self.rotation_func[i](np.array(u_rotation[i])))
        self.rotation = np.array(self.rotation)
        
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        ''' IMPORTANT'''
        ''' All force and moments stored in this class is already rotated to be the next level of reference frame
            !!But the translation component is not included here!!'''
        self.forces  = self.rotation_mat @ self.forces_local
        self.moments = self.rotation_mat @ self.moments_local
        self.inertia = self.rotation_mat @ self.inertia_local @ self.rotation_mat.T

'''
# class SCobj_BodyState(): # linking local coordinate system to global UNUSED  
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
'''   

class SCobj_Aircraft():
    def __init__(self, points, position, rotation):
        self.points = points #list of ForcePoint objects
        self.position = np.array(position) #position of the aircraft in global space
        self.rotation = np.array(rotation) #rotation of the aircraft in global space
        self.mass = self.Mass() #total mass of all points attached to the aircraft
        self.cog = self.COG() #location of center of gravity, in body frame
        self.forces_body = self.Forces()
        self.moments_body = self.Moments()
        self.mass = self.Mass()
        self.inertia_body = self.Inertia()
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        self.UpdatePoints()
        ''' IMPORTANT'''
        ''' All force and moments stored in this class is already rotated to be in the earth frame
            !!positions and rotation are in earth frame!!'''
        
    def Mass(self): #total mass of all points
        mass = 0
        for i in range(len(self.points)):
            mass += self.points[i].mass
        return mass
    
    def COG(self): #location of center of gravity, in body frame
        cog = [0,0,0]
        for i in range(len(self.points)):
            cog = np.add(cog, self.points[i].mass * self.points[i].position)
        cog = np.array(cog)/self.mass
        return cog
            
    def Inertia(self): #find inertia tensor of the full aircraft
        inertia = np.array([[0,0,0],[0,0,0],[0,0,0]])
        for i in range(len(self.points)):
            intertia_pt = np.add(self.points[i].inertia, self.points[i].mass * (np.dot(self.points[i].position, self.points[i].position)*np.identity(3) - np.outer(self.points[i].position, self.points[i].position))) #parallel axis theorem
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
    

    def UpdatePoints(self, update_variables=None):
        '''
        Notes about the update_variables list
        The update_variables are are list of the full set of variables to update, 
        see aircraft.SCfunc_UpdateAssembly() for the structure of one entry.
        even if there is nothing to update generate a empty list so the loop doesnt break
        '''
        if update_variables:
            for i in range(len(self.points)):
                update_variables_rot = update_variables[i]
                for j in range(len(update_variables_rot)):
                    if np.array(update_variables_rot[j]).size == 3:
                        update_variables_rot[j] = self.points[i].rotation_mat_inv @ update_variables_rot[j]
                    if np.array(update_variables_rot[j]).size == 9:
                        update_variables_rot[j] = self.points[i].rotation_mat_inv @ update_variables_rot[j] @ self.points[i].rotation_mat_inv.T
                        
                self.points[i].Update(u_forces   = update_variables_rot[0],
                                    u_moments  = update_variables_rot[1],
                                    u_mass     = update_variables_rot[2],
                                    u_inertia  = update_variables_rot[3],
                                    u_position = update_variables_rot[4],
                                    u_rotation = update_variables_rot[5])
            
        self.mass = self.Mass() #total mass of all points attached to the aircraft
        self.cog = self.COG() #location of center of gravity, in body frame
        self.forces_body = self.Forces()
        self.moments_body = self.Moments()
        self.mass = self.Mass()
        self.inertia_body = self.Inertia()
        
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        ''' IMPORTANT'''
        ''' All force and moments stored in this class is already rotated to be the next level of reference frame
            !!But the translation component is not included here!!'''
        self.forces  = self.rotation_mat @ self.forces_body #total force experianced by the aircraft
        self.moments = self.rotation_mat @ self.moments_body #total moments experianced by the aircraft
        self.inertia = self.rotation_mat @ self.inertia_body @ self.rotation_mat.T #inertia tensor of the full aircraft