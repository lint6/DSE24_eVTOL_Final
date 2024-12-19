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
        ang_x = 0
        ang_y = 0
        ang_z = 0
        
        while Run:
            '''Exit Conditions'''
            
            '''Simulation Loop'''
            #sum forces
            f_x = sum()
            f_y = sum()
            f_z = sum()
            m_x = sum()
            m_y = sum()
            m_z = sum()
            
            #get acceleration
            lat_acc_x = aircraft.force[0] / aircraft.mass 
            lat_acc_y = aircraft.force[1] / aircraft.mass
            lat_acc_z = aircraft.force[2] / aircraft.mass
            ang_acc_x = aircraft.moment[0] / aircraft.inertia[0]
            ang_acc_y = aircraft.moment[1] / aircraft.inertia[1]
            ang_acc_z = aircraft.moment[2] / aircraft.inertia[2]
            
            #get velocity
            vel_x = aircraft.vel_x + lat_acc_x * dt
            vel_y = aircraft.vel_y + lat_acc_y * dt
            vel_z = aircraft.vel_z + lat_acc_z * dt 
            rot_x = aircraft.rot_vel_x + ang_acc_x * dt 
            rot_y = aircraft.rot_vel_y + ang_acc_y * dt 
            rot_z = aircraft.rot_vel_z + ang_acc_z * dt 
            
            #get position
            pos_x += vel_x * dt
            pos_y += vel_y * dt 
            pos_z += vel_z * dt
            ang_pos_x += rot_x * dt
            ang_pos_y += rot_y * dt
            ang_pos_z += rot_z * dt 
            
            #update forces
            #log data
            return pos_x, pos_y, pos_z