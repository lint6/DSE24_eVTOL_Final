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
import time
from aircraft import *
from controller import *

def SCfunc_FlightSimulation(aircraft, runtime, Run=True, dt=0.1):
    if Run:
        print('Warning: Simulation Running')
        '''DOWNWARD IS POSTIVE'''
        '''DOWNWARD IS POSTIVE'''
        '''DOWNWARD IS POSTIVE'''
        start_time = time.time()
        log_time = [0]
        runtime = runtime
        # Initial Condition
        # Position
        pos_x = 0
        pos_y = 0
        pos_z = 0
        # Angles
        ang_x = 0
        ang_y = 0
        ang_z = 0
        # Velocity
        vel_x = 0
        vel_y = 0
        vel_z = 0
        # Rotational Velocity
        rot_x = 0
        rot_y = 0
        rot_z = 0

        # Aircraft Config
        rotor_count = 6
        
        # Control
        setpoint_pos = np.array([0,0,-20])
        setpoint_ang = np.array([0,0,0])
        setpoint_vel = np.array([0,0,0])
        setpoint_rot = np.array([0,0,0])
        rpm = np.ones(rotor_count) * .25* 4000
        far_distance = 75
        close_distance = 25
        allocation = np.array([[0, 0, 0.1, 0, 0, -0.1],
                               [0.1, 0.1, 0, -0.1, -0.1, 0],
                               [0.1, -0.1, 0, 0.1, -0.1, 0],
                               [1, 1, 1, 1, 1, 1]]) # Roll, Pitch, Yaw, Hover
        
        
        
        # Misc
        time_mark = time.time()
        
        
        # Logging
        log_state = [[[pos_x,pos_y,pos_z]], # Position
                     [[ang_x,ang_y,ang_z]], # Angle
                     [[vel_x, vel_y, vel_z]], # Velocity
                     [[rot_x, rot_y, rot_z]], # Rotation
                     [[0, 0, 0]], # Acceleration
                     [[0, 0, 0]]] # Acceleration Angular
        log_state_spherical = [[[0,0,0]], # Target
                               [[0,0,0]], # Velocity
                               [[0,0,0]]] # Control
        log_forces = [[[0,0,0]], [[0,0,0]]] # [Forces, moments]
        log_extras = [[[0,0,0,0]], [[0,0,0]], [[0,0,0]], [[0,0,0,0]], [[0,0]]] 
        log_error_cartesian= [[[0,0,0]], [[0,0,0]], [[0,0,0]], [[0,0,0]]] # [position, angle, velocity, rotation]
        log_error_spherical= [[[0,0,0]], [[0,0,0]], [[0,0,0]]] # [Flight, Angle]
        log_acc = [[[0,0,0]],[[0,0,0]]] # [position, yaw]
        log_setpoints = [[setpoint_pos],[setpoint_ang],[[0,0,0]]] # [position, angle, velocity, rotation]
        log_control = [[rpm],[]]
        
        while Run:
            '''Simulation Loop'''
            # Setpoints
            # if log_time[-1]>0:
            #     setpoint_pos = [0,0,-200]
            # if log_time[-1]>15:
            #     setpoint_pos = [500,0,-60]
            # if log_time[-1]>45:
            #     setpoint_pos = [550,0,-150]
            # if log_time[-1]>60:
            #     setpoint_pos = [5000,0,-300]
            # if log_time[-1]>120:
            #     setpoint_pos = [5500,0,-30]
            # setpoint_pos = [500*np.sin(log_time[-1]/100),500*np.cos(log_time[-1]/100),np.clip(-0.5*log_time[-1]-100, a_min=-5000, a_max=0)]
            
            
            # Acceleration
            lat_acc_x = aircraft.forces[0] / (aircraft.mass)
            lat_acc_y = aircraft.forces[1] / (aircraft.mass) 
            lat_acc_z = aircraft.forces[2] / (aircraft.mass) + 9.81
            print(aircraft.forces)
            
            
            ang_acc = np.linalg.inv(aircraft.inertia).dot(aircraft.moments)
            ang_acc_x = ang_acc[0]
            ang_acc_y = ang_acc[1]
            ang_acc_z = ang_acc[2]
            
            dvel = [lat_acc_x, lat_acc_y, lat_acc_z]
            drot = ang_acc
            
            # Velocity
            vel_x = vel_x + lat_acc_x * dt
            vel_y = vel_y + lat_acc_y * dt
            vel_z = vel_z + lat_acc_z * dt 
            if pos_z >= 0:
                if vel_z >=0:
                    vel_z = 0
            
            rot_x = rot_x + ang_acc_x * dt 
            rot_y = rot_y + ang_acc_y * dt 
            rot_z = rot_z + ang_acc_z * dt 
            vel = [vel_x,vel_y,vel_z]
            rot = [rot_x,rot_y,rot_z]
            
            # Position
            pos_x = pos_x + vel_x * dt
            pos_y = pos_y + vel_y * dt 
            pos_z = pos_z + vel_z * dt
            if pos_z > 0:
                pos_z = 0
                
            ang_x = ang_x + rot_x * dt
            ang_y = ang_y + rot_y * dt
            if ang_z + rot_z * dt > 180:
                ang_z = ang_z + rot_z * dt - 360
            if ang_z + rot_z * dt < -180:
                ang_z = ang_z + rot_z * dt + 360
            else:
                ang_z = ang_z + rot_z * dt 
                
            ang_x = np.clip(ang_x, a_max=90, a_min=-90)
            ang_y = np.clip(ang_y, a_max=90, a_min=-90)
            ang_z = np.clip(ang_z, a_max=180, a_min=-180)
            
            pos = [pos_x,pos_y,pos_z]
            ang = [ang_x,ang_y,ang_z]

            

            log_state[0].append(pos)  # Position
            log_state[1].append(ang)  # Angle
            log_state[2].append(vel)  # Velocity
            log_state[3].append(rot)  # Rotation (Angular velocity)
            log_state[4].append(dvel) # Acceleration
            log_state[5].append(drot) # Acceleration Angular
            
            # Cartesian Errors
            log_error_cartesian[0].append(setpoint_pos - log_state[0][-1])
            log_error_cartesian[1].append(setpoint_ang - log_state[1][-1])
            log_error_cartesian[2].append(setpoint_vel - log_state[2][-1])
            log_error_cartesian[3].append(setpoint_rot - log_state[3][-1])
            
            # Sphereical
            # States
            vect_tgt = SCfunc_CartesianToSpherical(log_error_cartesian[0][-1])[1]
            vect_vel = SCfunc_CartesianToSpherical(log_state[2][-1])[1]
            log_state_spherical[0].append(vect_tgt)
            log_state_spherical[1].append(vect_vel)
            log_state_spherical[2].append([0,0,0]) # For compeletness, updated in SCcon_ForwardFlight if in autopilot
            
            # Controllers
            autopilot = False
            flybywire = False
            if autopilot: # Waypoint mode, mimicing autopilot
                throttle_ForwardFlight, log_state_spherical[2], log_error_spherical, setpoint_ang_for = SCcon_ForwardFlight(log_state_spherical, log_state, log_error_spherical, allocation, dt=dt)
                
                throttle_HoverFlight, setpoint_vel, setpoint_ang_hov, log_error_cartesian[2], log_error_cartesian[1] = SCcon_HoverFlight(log_state, log_error_cartesian, allocation, dt=dt)

                throttle = SCfunc_LinearRamp(far_distance, close_distance, vect_tgt[0], throttle_ForwardFlight, throttle_HoverFlight)
                
                setpoint_ang = SCfunc_LinearRamp(far_distance, close_distance, vect_tgt[0], np.array(setpoint_ang_for), np.array(setpoint_ang_hov))
                mix_value = SCfunc_LinearRamp(far_distance, close_distance, vect_tgt[0], 0, 1) # 0 for forward and 1 for hover

            elif flybywire: # angle mode, mimicing fly-by-wire
                # TODO: Finish implemting FBW control scheme
                print(log_error_cartesian[-1])
                
            else: # Uncontrolled Flight
                throttle = 0
                mix_value = 0
                
            rpm = SCfunc_RotorRPM(throttle, rpm, dt)
            
            # Update aircraft
            for i in range(len(rpm)): #Limiting RPM
                if rpm[i] < 0:
                    rpm[i] = 0
                if rpm[i] > 4000:
                    rpm[i] = 4000
                    
                    
            updates = [ SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm[0]]], u_moments=[[0],[0],[rpm[0]]]), # Rotor 1
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm[1]]], u_moments=[[0],[0],[rpm[1]]]), # Rotor 2
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm[2]]], u_moments=[[0],[0],[rpm[2]]]), # Rotor 3
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm[3]]], u_moments=[[0],[0],[rpm[3]]]), # Rotor 4
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm[3]]], u_moments=[[0],[0],[rpm[3]]]), # Rotor 5
                        SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm[3]]], u_moments=[[0],[0],[rpm[3]]]), # Rotor 6
                        SCfunc_UpdateAssembly(), #1
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),#4
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),#10
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly(),#20
                        SCfunc_UpdateAssembly(),
                        SCfunc_UpdateAssembly()]
            state = [i[-1] for i in log_state]
            aircraft.Update(state = state, update_variables = updates)
            
            # Logging
            log_forces[0].append(aircraft.forces)
            log_forces[1].append(aircraft.moments)
            log_setpoints[0].append(setpoint_pos)
            log_setpoints[1].append([setpoint_ang[0],setpoint_ang[1],setpoint_ang[2]])
            log_setpoints[2].append(setpoint_vel)
            log_extras[0].append(rpm/4000)
            log_extras[1].append(setpoint_pos)
            log_extras[2].append([setpoint_ang[0],setpoint_ang[1],setpoint_ang[2]])
            log_extras[4].append([mix_value, 1-mix_value])
            # log_extras[3].append([np.max(throttle_hover), np.max(throttle_rotate_x), np.max(throttle_rotate_y), np.max(throttle_rotate_z)])

            log_time.append(log_time[-1]+dt)

            '''Exit Conditions'''
            if time.time() - start_time >= 600:
                Run = False
                print('Run time reached, simulation exited')
            if log_time[-1] >= runtime:
                Run = False
                print('Simulation Completed')
            if time.time() - time_mark >= 3 :
                print(f'Progress: {log_time[-1]/runtime*100 :.2f}% | {time.time()-start_time:.1f}/600 sec')
                time_mark = time.time()
            if Run == False:
                print(f' {time.time()-start_time:.2f} seconds')
        return log_state, log_forces, log_time, log_extras, log_acc, log_setpoints
        

def ExampleFunction(Constant): #the input modify the function that is to be returned
    return lambda variable: variable*Constant #Return a function that can be stored in a variable

def SCfunc_RotorRPM(throttle, current_rpm, dt, counter_torque = 0, max_torque = 500, inertia_rotor = 60, radius = 1):
    omega = SCfunc_RPM2RadSec(current_rpm)
    tip_speed = omega * radius
    counter_torque += 0.0001 * np.pi * radius**3 * 1.225 *  tip_speed**2#temp value for rotor resistance
    torque_delivery = throttle * max_torque
    detla_omega = (torque_delivery - counter_torque)/inertia_rotor
    rpm_new = SCfunc_RadSec2RPM(omega + detla_omega*dt)
    return rpm_new