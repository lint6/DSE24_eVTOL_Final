'''
Created by Lintong

Controllers file
DO define function
DO NOT define class
DO NOT script

Upstream
None

Downstream
physics.py

'''

import numpy as np
from misc import *

def SCfunc_PIDController(error, k_p, t_i, t_d, dt, FULL=False): #Standard PID controller
    p_error = error[-1]
    i_error = np.sum(error) * dt
    d_error = (error[-1]-error[-2])/dt
    output = -k_p * (p_error + i_error/t_i + d_error*t_d)
    if FULL:
        print(p_error, d_error, i_error)
        return output, p_error, i_error, d_error
    else:
        return output

def SCfunc_PDController(error, k_p, t_d, dt): #Standard PID controller
    p_error = error[-1]
    d_error = (error[-1]-error[-2])/dt
    output = -k_p * (p_error + d_error*t_d)
    return output

def SCfunc_PController(error, k_p): #Standard P controller
    output = -k_p * error
    return output

def SCcon_ForwardFlight(state_in_1, state_in_2, error_in, allocation, dt):
    # Assign Data In
    vect_tgt = state_in_1[0] # Historical Vector to target, act as error
    vect_vel = state_in_1[1] # Historical Vector of AC velocity
    vect_con = state_in_1[2] # Historical Vector of control
    flight_error = error_in[0] #Historical error in flight control vector
    yaw_error = error_in[1] # Historical error in yaw
    pos = state_in_2[0] # Historical position
    ang = state_in_2[1] # Historical rotation
    allocation = allocation # Control allocation
    
    # Control Vector, spherical coord
    # vect_con = [vel, azimuth, altitude]
    vect_con = [np.clip(-1*SCfunc_PController(vect_tgt[-1][0], k_p=0.2), a_min=-25, a_max=25),
                vect_tgt[-1][1],
                SCfunc_LinearRamp(x1=-5, x2=-10, x=pos[-1][2], value1=-90, value2=vect_tgt[-1][2])]
    state_in_1[2].append(vect_con) # Add latest control vector to list

    # Error vectors for flight control
    flight_error = np.array(vect_con) - np.array(vect_vel)
    yaw_error = np.array(vect_vel).T[1] - np.array(ang).T[2]
    
    # Angle
    roll_set  = np.clip(SCfunc_PIDController(-1*np.array(flight_error).T[1], k_p=1, t_i=99999, t_d=0, dt=dt),
                    a_min=-30, a_max=30)
    pitch_set = np.clip(SCfunc_PIDController(np.array(flight_error).T[0], k_p=2, t_i=99999, t_d=0, dt=dt),
                    a_min=-30, a_max=30)
    ang_set = [roll_set,pitch_set,0]

    # Angle Error
    ang_error_now = np.array(ang_set) - np.array(ang[-1]) # Current error in angle
    error_in[2].append(ang_error_now) # Historical Error in angle
    
    # Throttle
    roll_throttle  = np.clip(SCfunc_PIDController(np.array(error_in[2]).T[0], k_p=0.05, t_i=250, t_d=5, dt=dt),
                             a_min=-1, a_max=1)
    pitch_throttle = np.clip(-1*SCfunc_PIDController(np.array(error_in[2]).T[1], k_p=1.25, t_i=150, t_d=1, dt=dt),
                             a_min=-1, a_max=1)
    yaw_throttle   = np.clip(-1*SCfunc_PIDController(yaw_error, k_p=0.012, t_i=120, t_d=0.3, dt=dt),
                             a_min=-1, a_max=1)
    hover_throttle = np.clip(SCfunc_PIDController(np.array(flight_error).T[2], k_p=1, t_i=999999999, t_d=0, dt=dt),
                             a_min=-1, a_max=1)

    # Allocation
    roll_throttle  = allocation[0] * roll_throttle
    pitch_throttle = allocation[1] * pitch_throttle
    yaw_throttle   = allocation[2] * yaw_throttle
    hover_throttle = allocation[3] * hover_throttle
    
    #Grouping
    throttle = 0
    # throttle += roll_throttle
    throttle += pitch_throttle
    # throttle += yaw_throttle
    throttle += hover_throttle
    # print(throttle)
    return throttle, state_in_1[2], error_in, ang_set


def SCcon_HoverFlight(state_in, error_in, allocation, dt):
    # Assign Data In
    vel = state_in[2] # Historical velocity
    rot = state_in[3] # Historical rotational velocity
    ang = state_in[1] # Historical rotation
    allocation = allocation # Control allocation
    
    #DEBUG
    TUNING_vel = False
    TUNING_ang = False

    # Errors
    pos_error = error_in[0] # Historical position error, Cartesian
    ang_error = error_in[1] # Historical angle error, Cartesian
    vel_error = error_in[2] # Historical velocity error
    rotate_z = np.array(ang) * [0,0,1]
    pos_error_loc =[]
    for i in range(len(pos_error)):
        pos_error_loc.append(SCfunc_EulerRotation(pos_error[i], rotate_z[i])[0])
        
    # Velocity
    Vx_set = np.clip(SCfunc_PIDController(-1*np.array(pos_error_loc).T[0], k_p=1.2, t_i=99999, t_d=2, dt=dt),
                     a_min=-5, a_max=5)
    Vy_set = np.clip(SCfunc_PIDController(-1*np.array(pos_error_loc).T[1], k_p=1.2, t_i=99999, t_d=2, dt=dt),
                     a_min=-5, a_max=5)
    Vz_set = np.clip(-1*SCfunc_PIDController(np.array(pos_error).T[2], k_p=1.6, t_i=250, t_d=0.35, dt=dt),
                     a_min=-5, a_max=5)
    if TUNING_vel:
        vel_set = [0,0,-50]
    else:
        vel_set = [Vx_set,Vy_set,Vz_set]

    # Velocity Error
    vel_error_now = np.array(vel_set) - np.array(vel[-1])
    vel_error.append(vel_error_now) # Historical error in velocity
    
    # Angle
    roll_set  = np.clip(SCfunc_PIDController(-1*np.array(vel_error).T[1], k_p=1, t_i=99999, t_d=0, dt=dt),
                    a_min=-30, a_max=30)
    pitch_set = np.clip(SCfunc_PIDController(np.array(vel_error).T[0], k_p=1, t_i=99999, t_d=0, dt=dt),
                    a_min=-30, a_max=30)
    yaw_set   = ang[-1][2]
    if TUNING_ang:
        ang_set = [0,0,0]
    else:
        ang_set = [roll_set,pitch_set,yaw_set]
        
    # Angle Error
    ang_error_now = np.array(ang_set) - np.array(ang[-1]) # Current error in angle
    ang_error.append(ang_error_now) # Historical Error in angle
    
    # Throttle
    roll_throttle  = np.clip(SCfunc_PIDController(np.array(ang_error).T[0], k_p=0.05, t_i=250, t_d=5, dt=dt),
                             a_min=-1, a_max=1)
    pitch_throttle = np.clip(SCfunc_PIDController(-1*np.array(ang_error).T[1], k_p=0.05, t_i=250, t_d=5, dt=dt),
                             a_min=-1, a_max=1)
    yaw_throttle   = np.clip(SCfunc_PIDController( -1 *np.array(rot).T[2], k_p=0.012, t_i=120, t_d=0.3, dt=dt),
                             a_min=-1, a_max=1)
    hover_throttle = np.clip(SCfunc_PIDController(np.array(vel_error).T[2], k_p=0.5, t_i=9999999999, t_d=1.25, dt=dt),
                             a_min=-1, a_max=1)

    # Allocation
    roll_throttle  = allocation[0] * roll_throttle
    pitch_throttle = allocation[1] * pitch_throttle
    yaw_throttle   = allocation[2] * yaw_throttle
    hover_throttle = allocation[3] * hover_throttle
    
    #Grouping
    throttle = 0
    throttle += roll_throttle
    throttle += pitch_throttle
    throttle += yaw_throttle
    throttle += hover_throttle
    
    return throttle, vel_set, ang_set, vel_error, ang_error
