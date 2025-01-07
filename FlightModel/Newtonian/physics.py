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
import time
from aircraft import *

def SCfunc_FlightSimulation(aircraft, Run=True, dt=0.1):
    if Run:
        print('Warning: Simulation Running')
        '''DOWNWARD IS POSTIVE'''
        '''DOWNWARD IS POSTIVE'''
        '''DOWNWARD IS POSTIVE'''
        start_time = time.time()
        log_time = [0]
        #initializing
        # Velocity
        vel_x = 0
        vel_y = 0
        vel_z = 0
        # Rotational Velocity
        rot_x = 0
        rot_y = 0
        rot_z = 0
        # Position
        pos_x = 0
        pos_y = 0
        pos_z = 0
        # Rotation
        ang_pos_x = 0
        ang_pos_y = 0
        ang_pos_z = 0
        
        # Logging
        log_state = [[[pos_x,pos_y,pos_z]],[[ang_pos_x,ang_pos_y,ang_pos_z]]]
        log_forces = [[0]]
        log_extras = [[0],[0]]
        log_errors = [0]
        while Run:
            
            '''Exit Conditions'''
            if time.time() - start_time > 10:
                Run = False
                print('Run time reached, simulation exited')
            if log_time[-1] > 60:
                Run = False
                print('Simulation time reached, simulation exited')
                
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
            lat_acc_x = aircraft.forces[0] / (aircraft.mass * 9.81) 
            lat_acc_y = aircraft.forces[1] / (aircraft.mass * 9.81) 
            lat_acc_z = aircraft.forces[2] / (aircraft.mass * 9.81) + 9.81
            
            ang_acc = np.linalg.inv(aircraft.inertia).dot(aircraft.moments)
            
            
            ang_acc_x = ang_acc[0]
            ang_acc_y = ang_acc[1]
            ang_acc_z = ang_acc[2]
            
            #new velocity
            vel_x = vel_x + lat_acc_x * dt
            vel_y = vel_y + lat_acc_y * dt
            vel_z = vel_z + lat_acc_z * dt 
            rot_x = rot_x + ang_acc_x * dt 
            rot_y = rot_y + ang_acc_y * dt 
            rot_z = rot_z + ang_acc_z * dt 
            
            #new position
            pos_x = pos_x + vel_x * dt
            pos_y = pos_y + vel_y * dt 
            pos_z = pos_z + vel_z * dt
            ang_pos_x = ang_pos_x + rot_x * dt
            ang_pos_y = ang_pos_y + rot_y * dt
            ang_pos_z = ang_pos_z + rot_z * dt 

            # side slip angle
            # angtle of atack -- geomatry how force functino, hiahdfbvjkadbfjkhadbfv
            
            # Controllers
            if log_time[-1]<10:
                desired = 100
            elif log_time[-1]<30:
                desired = 50
            elif log_time[-1]<45:
                desired = 150
                
            log_errors.append(-desired - pos_z)
            integral_time = int(1 / dt)
            if len(log_state[0])>=integral_time:
                I_error = log_errors[-integral_time:]
                I_error = np.array(I_error).T[-1]
                I_error = np.sum(np.array(I_error)*dt)
            else:
                I_error = log_errors
                I_error = np.array(I_error).T[-1]
                I_error = np.sum(np.array(I_error)*dt)
            Con_P = 5 * log_errors[-1]
            Con_I = 150 * I_error
            Con_D = 45 * (log_errors[-1]-log_errors[-2]) / dt
            RPM = (Con_P + Con_I + Con_D) * -1
            
            
            
            
            if RPM < 0:
                RPM = 0
            if RPM > 4000:
                RPM = 4000
            # Update aircraft
            position = [pos_x, pos_y, pos_z]
            rotation = [ang_pos_x, ang_pos_y, ang_pos_z]
            aircraft.UpdateAircraftState(position, rotation)
            updates = [ SCfunc_UpdateAssembly(u_forces=[[0],[0],[RPM]], u_moments=[[0],[0],[RPM]]), 
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[RPM]], u_moments=[[0],[0],[RPM]]),
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[RPM]], u_moments=[[0],[0],[RPM]]), 
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[RPM]], u_moments=[[0],[0],[RPM]]),
                        SCfunc_UpdateAssembly()]
            aircraft.UpdatePoints(update_variables = updates)
            # Logging
            log_state[0].append([pos_x,pos_y,pos_z])
            log_state[1].append([ang_pos_x,ang_pos_y,ang_pos_z]) 
            log_forces[0].append(aircraft.forces)
            log_extras[0].append(RPM/4000)
            log_extras[1].append(desired)
            log_time.append(log_time[-1]+dt)
        return log_state, log_forces, log_time, log_extras
        

def ExampleFunction(Constant): #the input modify the function that is to be returned
    return lambda variable: variable*Constant #Return a function that can be stored in a variable


#x = [u,w, theta, R, omega] should have u and w in the x list
def SCfunc_parameter_velo():
    return lambda x : np.sqrt(x[0]**2 + x[1]**2)

def SCfunc_parameter_alpha_attack():
    return lambda x : x[2] - np.arctan(x[1]/x[0])

var = SCfunc_parameter_velo()
var1 = SCfunc_parameter_alpha_attack()

# x.append(var)
# x.append(var1)
# x = [u,w,theta, R, omega, var(x), var1(x)]
def SCfun_parameter_Mu():
    return lambda x : x[5]/(x[4]*x[3]) * np.cos(x[6])

def SCfun_parameter_llambda_c():
    return  lambda x : x[5]/(x[4]*x[3]) * np.sin(x[6])
