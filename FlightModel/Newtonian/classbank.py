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
        # Functions
        self.forces_func = forces  # [0,0,0]
        self.moments_func = moments
        self.mass_func = mass
        self.inertia_func = inertia
        self.position_func = position
        self.rotation_func = rotation
        
        # Values
        self.forces = forces*1
        self.moments = moments*1
        self.mass = mass*1
        self.inertia = inertia*1
        self.position = position*1
        self.rotation = rotation*1
        
        # make local frame vectors
        self.forces_local = np.array(self.forces)
        self.moments_local = np.array(self.moments)
        self.inertia_local = np.array(self.inertia)
        
        self.Update()
        ''' IMPORTANT'''
        ''' All force and moments stored in this class is already rotated to be in the body frame
            !!positions and rotation are in body frame!!'''
    def UpdateForcePointState(self, state):
        # 0 position
        # 1 rotation
        # 2 velocity
        # 3 angular velocity
        # 4 acceleration NOT CORRECT
        # 5 angular acceleration NOT CORRECT
        # 6 [speed, sideslip, angle of attack]
        
        # Updating self state to be within the local frame of the point
        if state:
            for i in range(len(state)):
                self.state[i] = self.rotation_mat @ state[i]
            self.state.append([0,0,0])
            self.state[2] = self.state[2] + np.cross(self.state[3], self.position) # Add in velocity from rotation
            self.state[6] = SCfunc_CartesianToSpherical(self.state[2])[1] # The vector of side slip and aoa
            self.state[0] = self.position
            self.state[1] = self.rotation
            self.state = self.state[:7]
        
    def Update(self, #variables to update, one element for each term. 
               state = None,
               u_forces   = [[0],[0],[0]],  #VARIABLES ONLY IF THE FORCE IS GIVEN BY A FUNCTION
               u_moments  = [[0],[0],[0]],  
               u_mass     =  [0],            
               u_inertia  = [[0,0,0],       
                             [0,0,0],       
                             [0,0,0]],
               u_position = [[0],[0],[0]],
               u_rotation = [[0],[0],[0]]):
        
        # initial
        function_def = type(lambda x: x) #telling Python what a lambda function is so we can do conditions later
        self.state = state
        
        # Making rotation Matrix
        self.rotation = np.array(self.rotation)
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        
        # Updating point state
        self.UpdateForcePointState(state)

        # Update ForcePoint property
        for i in range(len(self.forces_func)): #update force base on functions
            if type(self.forces_func[i]) == function_def:
                self.forces_local[i] = float(self.forces_func[i](state, np.array(u_forces[i])))
        self.forces_local = [float(i) for i in self.forces_local]

        for i in range(len(self.moments_func)): #update moments base on functions
            if type(self.moments_func[i]) == function_def:
                self.moments_local[i] = float(self.moments_func[i](state, np.array(u_moments[i])))
        self.moments_local = [float(i) for i in self.moments_local]
        
        if type(self.mass_func) == function_def: #update mass base on functions
            self.mass = float(self.mass_func(state, u_mass))
        
         
        for i in range(len(self.inertia_func)): #update inertia base on functions
            for j in range(len(self.inertia_func[i])):
                if type(self.inertia_func[i][j]) == function_def:
                    self.inertia_local[i] = float(self.inertia_func[i][j](state, np.array(u_inertia[i][j])))
        for i in range(len(self.inertia_local)):
            for j in range(len(self.inertia_local[i])):
                self.inertia_local[i][j] = np.array(self.inertia_local[i][j])

        for i in range(len(self.position_func)): #update position base on functions wrt AC frame
            if type(self.position_func[i]) == function_def:
                self.position[i] = float(self.position_func[i](state, np.array(u_position[i])))
        self.position = np.array(self.position)
        
        for i in range(len(self.rotation_func)): #update rotation base on functions wrt AC frame
            if type(self.rotation_func[i]) == function_def:
                self.rotation[i] = float(self.rotation_func[i](state, np.array(u_rotation[i])))

        ''' IMPORTANT'''
        ''' All force and moments stored in this class is already rotated to be the next level of reference frame
            !!But the translation component is not included here!!'''
            
        # Update rotation matrix after the point updates
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        
        # Rotate force, moment, and inertia backinto the AC frame
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
        self.Update()
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
    

    def Update(self, state=None, update_variables=None):
        '''
        Notes about the update_variables list
        The update_variables are are list of the full set of variables to update, 
        see aircraft.SCfunc_UpdateAssembly() for the structure of one entry.
        even if there is nothing to update generate a empty list so the loop doesnt break
        '''
        
        # Update Aircraft State
        self.UpdateAircraftState(state)
        
        # Making rotation Matrix
        self.rotation_mat = SCfunc_EulerRotation([0,0,0], self.rotation)[1]
        self.rotation_mat_inv = SCfunc_EulerRotation([0,0,0], self.rotation)[2]
        
        # Rotating states into aicraft frame
        state_rotated = []
        if state:
            for i in state:
                state_rotated.append(self.rotation_mat @ i)
            state_rotated[0] = self.position # Changing position back to global
            state_rotated[1] = self.rotation # Changing rotation back to global
        
        # Updating ForcePoints
        if update_variables:
            for i in range(len(self.points)):
                self.points[i].Update(state=state_rotated,
                                    u_forces   = update_variables[i][0],
                                    u_moments  = update_variables[i][1],
                                    u_mass     = update_variables[i][2],
                                    u_inertia  = update_variables[i][3],
                                    u_position = update_variables[i][4],
                                    u_rotation = update_variables[i][5],
                                    )
        
        # Update aircraft properity
        self.mass = self.Mass()
        self.cog = self.COG()
        self.forces_body = self.Forces()
        self.moments_body = self.Moments()
        self.inertia_body = self.Inertia()

        ''' IMPORTANT'''
        ''' All force and moments stored in this class is already rotated to be the next level of reference frame
            !!But the translation component is not included here!!'''
        self.forces  = self.rotation_mat @ self.forces_body #total force experianced by the aircraft
        self.moments = self.rotation_mat @ self.moments_body #total moments experianced by the aircraft
        self.inertia = self.rotation_mat @ self.inertia_body @ self.rotation_mat.T #inertia tensor of the full aircraft
    
    def UpdateAircraftState(self, state):
        if state:
            self.position = state[0]
            self.rotation = state[1]