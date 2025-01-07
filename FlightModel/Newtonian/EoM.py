'''
Created by Lintong

Simulation verification file
DO define function
DO NOT define class
DO NOT script

Upstream
None

Downstream
All

'''
import numpy as np 


#TODO: Unit Tests
# - Vertical Movement w/ total delta_T
# - Rotation Movement w/ delta_T per rotor
# - Yaw Movement w/ delta_M
# - Side movement from 

#Defining "constant" variable for now 
rpm = 1 
mass = 500
g = 9.81 

Inertia_matrix =np.array([[100, 0, 0],
                          [0, 100, 0],
                          [0, 0, 100]])
#Angle in degrees 
phi = 10
theta = 0 
psi = 0

#Inertia in x,y,z
I_xx = 10
I_yy = 10 
I_zz = 10 

#forces from each rotor 
T_1 = 5 * rpm  
T_2 = 5 * rpm 
T_3 = 5 * rpm
T_4 = 5 * rpm 

torque_1 = 0.025 * rpm 
torque_2 = 0.025 * rpm 
torque_3 = 0.025 * rpm 
torque_4 = 0.025 * rpm 

# Generating emty matrix for storing y_d_d, z_d_d, and phi_d_d 

b_matrix = np.array([[-(1/mass) * np.sin(phi), 0],
                     [(1/mass) * np.cos(phi), 0],
                     [0, 1/I_xx]])

u_matrix = np.array([2,3])

planar_acceleration_1 = np.array([0, -g, 0])

planar_acceleration_2 = b_matrix.dot(u_matrix.T)

planar_acceleration = planar_acceleration_1 + planar_acceleration_2
print(planar_acceleration)



