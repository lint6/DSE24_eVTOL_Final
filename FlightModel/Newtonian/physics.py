'''
Created by Lintong

Simulation Physcis file
DO define function
DO NOT define class
DO NOT script

Upstream
None

Downstream
SimulationUI.py
Main.py

'''
import numpy as np
import classbank 

def SCfunc_FlightSimulation(Run=True, dt=0.1):
    if Run:
        print('Warning: Simulation Running')
        aircraft = classbank.SCobj_Aircraft()
        #initializing
        mass = sum()
        i_xx = 0
        i_yy = 0
        i_zz = 0
        i_xy = 0
        i_xz = 0
        i_yz = 0
        lat_acc_x = 0
        lat_acc_y = 0
        lat_acc_z = 0
        ang_acc_x = 0
        ang_acc_y = 0
        ang_acc_z = 0
        vel_x = 0
        vel_y = 0
        vel_z = 0
        rot_x = 0
        rot_y = 0
        rot_z = 0
        pos_x = 0
        pos_y = 0
        pos_z = 0
        ang_pos_x = 0
        ang_pos_y = 0
        ang_pos_z = 0
        
        while Run:
            '''Exit Conditions'''
            
            '''Simulation Loop'''
            #Below is the information we have when we cerate an object using Aircraft

            """
            class SCobj_Aircraft():
                def __init__(self, points, position, rotation):
                    self.points = points #list of ForcePoint objects
                    self.mass = None 
                    self.cog = None # 1x3 matrix 
                    self.intertia = None #Tensor
                    self.forces = None # 1x3 matrix
                    self.position = np.array(position) #position of the aircraft in global space 1x3 matrix
                    self.rotation = np.array(rotation) #rotation of the aircraft in global space 1x3 matrix
                    self.UpdatePoints()
            """
            
            #get current acceleration
            lat_acc_x = aircraft.force[0] / (aircraft.mass * 9.81) 
            lat_acc_y = aircraft.force[1] / (aircraft.mass * 9.81) 
            lat_acc_z = aircraft.force[2] / (aircraft.mass * 9.81) 
            ang_acc_x = aircraft.moment[0] / aircraft.inertia[0]
            ang_acc_y = aircraft.moment[1] / aircraft.inertia[1]
            ang_acc_z = aircraft.moment[2] / aircraft.inertia[2]
            
            #new velocity
            vel_x = aircraft.vel_x + lat_acc_x * dt
            vel_y = aircraft.vel_y + lat_acc_y * dt
            vel_z = aircraft.vel_z + lat_acc_z * dt 
            rot_x = aircraft.rot_vel_x + ang_acc_x * dt 
            rot_y = aircraft.rot_vel_y + ang_acc_y * dt 
            rot_z = aircraft.rot_vel_z + ang_acc_z * dt 
            
            #new position
            pos_x = pos_x + vel_x * dt
            pos_y = pos_y + vel_y * dt 
            pos_z = pos_z + vel_z * dt
            ang_pos_x = ang_pos_x + rot_x * dt
            ang_pos_y = ang_pos_y + rot_y * dt
            ang_pos_z = ang_pos_z + rot_z * dt 

            # side slip angle
            # angtle of atack -- geomatry how force functino, hiahdfbvjkadbfjkhadbfv

           
            return pos_x, pos_y, pos_z, ang_pos_x, ang_pos_y, ang_pos_z
        

def ExampleFunction(Constant): #the input modify the function that is to be returned
    return lambda variable: variable*Constant #Return a function that can be stored in a variable


#x = [u,w] should have u and w in the x list
def SCfunc_parameter_velo():
    return lambda x : np.sqrt(x[0]**2 + x[1]**2)

#x = [u,w,theta]
def SCfunc_parameter_alpha_attack():
    return lambda x : x[2] - np.arctan(x[1]/x[0])

var = SCfunc_parameter_velo()
var1 = 
#x = [var(x),omega, ]
def SCfun_parameter_Mu():
    return 

def SCfun_parameter_llambda():
    return 

def 