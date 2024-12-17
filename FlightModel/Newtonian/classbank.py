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
    def __init__(self, force, moment, mass, inertia):
        self.force = force # purely in z direction [0,0,something] 
        self.moments = moment
        self.mass = mass
        self.inertia = inertia #array with 7 elements
        self.position_array = SCobj_BodyState.matrix_construction()[0]
        self.euler_array = SCobj_BodyState.matrix_construction()[1]
        self.state_array = SCobj_BodyState.matrix_construction()[2]
        return 




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
    
<<<<<<< HEAD:FlightModel/Newtonian/classbank.py
class SCobj_Aircraft():
    def __init__(self, statevector, children):
        state_vector = SCobj_BodyState(statevector)
        children = children 
=======
class SCobj_ParentState():
    def __init__(self, children):
        self.state_vector = SCobj_BodyState.__init__()
        self.children = children 
        return 
>>>>>>> aade9580b5daa0874c37fbd6a672bdc121a66e87:FlightModel/Newtonian/class.py

    def gather_phy_child(self):
        return 