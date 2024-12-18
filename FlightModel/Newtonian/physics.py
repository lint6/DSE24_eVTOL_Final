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
            ang_acc_y = aircraft.moment[1] / aircraft.inertia[]
            ang_acc_z = 
            
            #get velocity
            vel_x = 0
            vel_y = 0
            vel_z = 0
            rot_x = 0
            rot_y = 0
            rot_z = 0
            
            #get position
            pos_x = 0
            pos_y = 0
            pos_z = 0
            ang_x = 0
            ang_y = 0
            ang_z = 0
            
            #update forces
            state = np.array 
            #log data