'''
Created by Lintong

Simulation Physcis file
DO define function
DO NOT define class
DO NOT script

Upstream
aircraft.py
controller.py

Downstream
SimulationUI.py
Main.py

'''
import numpy as np
import classbank 
import time
from aircraft import *
from controller import *

def SCfunc_FlightSimulation(aircraft, runtime, Run=True, dt=0.5):
    if Run:
        print('Warning: Simulation Running')
        '''DOWNWARD IS POSTIVE'''
        '''DOWNWARD IS POSTIVE'''
        '''DOWNWARD IS POSTIVE'''
        start_time = time.time()
        log_time = [0]
        runtime = runtime
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
        # Rotation angle wrt axis
        ang_pos_x = 0
        ang_pos_y = 0
        ang_pos_z = 0
        # Aircraft Config
        rotor_count = 4
        
        # Control Inputs
        setpoint_pos = [20,0,-100]
        setpoint_ang = [0,0,0]
        
        # Misc
        time_mark = time.time()
        
        
        # Logging
        log_state = [[[pos_x,pos_y,pos_z]],[[ang_pos_x,ang_pos_y,ang_pos_z]],[[vel_x, vel_y, vel_z]]]
        log_forces = [[0]]
        log_extras = [[[0,0,0,0]],[[0,0,0]],[[0,0,0]]]
        log_error= [[[0],[0],[0]],[[0],[0],[0]]]
        log_acc = [[[0],[0],[0]],[[0],[0],[0]]]
        while Run:
            
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
            lat_acc_x = aircraft.forces[0] / (aircraft.mass) 
            lat_acc_y = aircraft.forces[1] / (aircraft.mass) 
            lat_acc_z = aircraft.forces[2] / (aircraft.mass) + 9.81
            
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
            if pos_z > 0:
                pos_z = 0
            ang_pos_x = ang_pos_x + rot_x * dt
            ang_pos_y = ang_pos_y + rot_y * dt
            if ang_pos_z + rot_z * dt > 180:
                ang_pos_z = ang_pos_z + rot_z * dt - 360
            if ang_pos_z + rot_z * dt < -180:
                ang_pos_z = ang_pos_z + rot_z * dt + 360
            ang_pos_z = ang_pos_z + rot_z * dt 
            ang_pos_x = np.clip(ang_pos_x, a_max=90, a_min=-90)
            ang_pos_y = np.clip(ang_pos_y, a_max=90, a_min=-90)
            ang_pos_z = np.clip(ang_pos_z, a_max=180, a_min=-180)
            # side slip angle
            # angtle of atack -- geomatry how force functino, hiahdfbvjkadbfjkhadbfv
            
            # Controllers
            # Angle Error

            # print(f'setpoint {setpoint_pos[0]}')
            # print(f'position {pos_x}')
            ang_tgt = np.arctan2(setpoint_pos[1]-pos_y, setpoint_pos[0]-pos_x) * 180/np.pi #angle from the aicraft to the target
            if (ang_tgt - ang_pos_z) > 180:  #difference between the aircraft yaw and the yaw of the target
                ang_diff = ang_tgt - ang_pos_z + 360
            if (ang_tgt - ang_pos_z) < -180:  
                ang_diff = ang_tgt - ang_pos_z - 360
            else:
                ang_diff = ang_tgt - ang_pos_z
            mag_diff = np.linalg.norm([setpoint_pos[1]-pos_x,setpoint_pos[0]-pos_y]) #magnitude of difference between planar elements
            lon_diff = np.cos(np.radians(ang_diff)) * mag_diff
            lat_diff = np.sin(np.radians(ang_diff)) * mag_diff


            log_error[0][0].append(lon_diff)
            log_error[0][1].append(lat_diff)
            log_error[0][2].append(setpoint_pos[2] - pos_z)
            
            setpoint_ang[2] = ang_tgt #yaw angle
            setpoint_ang[1] = np.clip(SCfunc_PIDController(log_error[0][0], k_p=0.02, t_i=500, t_d=0, dt=dt), a_min=-30, a_max=30) #pitch angle
            setpoint_ang[0] = np.clip(-1 * SCfunc_PIDController(log_error[0][1], k_p=1, t_i=10, t_d=3.1, dt=dt), a_min=-30, a_max=30) #roll angle
            
            log_error[1][0].append(setpoint_ang[0])
            log_error[1][1].append(setpoint_ang[1])
            log_error[1][2].append(ang_diff)
            # Controllers
            rpm_hover = np.ones(rotor_count) * SCfunc_PIDController(log_error[0][2], k_p=12.5, t_i=10, t_d=3.1, dt=dt)
            rpm_rotate_x = np.array([-1,1,1,-1]) * -1 * SCfunc_PIDController(log_error[1][0], k_p=10, t_i=50, t_d=1, dt=dt)            
            rpm_rotate_y = np.array([1,1,-1,-1]) * -1 * SCfunc_PIDController(log_error[1][1], k_p=10, t_i=50, t_d=1, dt=dt)
            print(rpm_rotate_y)
            rpm_rotate_z = np.array([-1,1,-1,1]) * -1 * SCfunc_PIDController(log_error[1][2], k_p=50, t_i=50, t_d=5, dt=dt)
            rpm = rpm_hover + rpm_rotate_x + rpm_rotate_y + rpm_rotate_z

            for i in range(len(rpm)):
                if rpm[i] < 0:
                    rpm[i] = 0
                if rpm[i] > 4000:
                    rpm[i] = 4000
            if pos_z > 0:
                pos_z = 0
                
                
                
            
            # Update aircraft
            position = [pos_x, pos_y, pos_z]
            rotation = [ang_pos_x, ang_pos_y, ang_pos_z]
            velocity = [vel_x, vel_y, vel_z]
            aircraft.UpdateAircraftState(position, rotation)
            updates = [ SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm[0]]], u_moments=[[0],[0],[rpm[0]]]), 
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm[1]]], u_moments=[[0],[0],[rpm[1]]]),
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm[2]]], u_moments=[[0],[0],[rpm[2]]]), 
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm[3]]], u_moments=[[0],[0],[rpm[3]]]),
                        SCfunc_UpdateAssembly()]
            aircraft.UpdatePoints(update_variables = updates)
            # Logging
            log_state[0].append(position)
            log_state[1].append(rotation)
            log_state[2].append(velocity)
            log_forces[0].append(aircraft.forces)
            
            log_extras[0].append(rpm/4000)
            log_extras[1].append(setpoint_pos)
            log_extras[2].append([setpoint_ang[0],setpoint_ang[1],setpoint_ang[2]])

            log_time.append(log_time[-1]+dt)
            
            log_acc[0][0].append(lat_acc_x)
            log_acc[0][1].append(lat_acc_y)
            log_acc[0][2].append(lat_acc_z)
            
            '''Exit Conditions'''
            if time.time() - start_time > 60:
                Run = False
                print('Run time reached, simulation exited')
            if log_time[-1] > runtime:
                Run = False
                print('Simulation time reached, simulation exited')
            if time.time() - time_mark > 5 :
                print(f'Progress: {log_time[-1]/runtime*100 :.2f}%')
                time_mark = time.time()
        return log_state, log_forces, log_time, log_extras, log_acc
        

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
