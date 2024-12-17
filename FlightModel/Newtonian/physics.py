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

def SCfunc_FlightSimulation(Run=True, dt=0.1):
    if Run:
        print('Warning: Simulation Running')

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
            lat_acc_x = 0
            lat_acc_y = 0
            lat_acc_z = 0
            ang_acc_x = 0
            ang_acc_y = 0
            ang_acc_z = 0
            
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
            
            #log data