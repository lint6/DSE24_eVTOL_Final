'''
Created by Lintong

Aircraft file
DO define function
DO define class
DO NOT script

Upstream
classbank.py

Downstream
SimulationUI

'The point of this file is that we make a function with all the 
aicraft parts built in so we can just call the function to get 
a full aircraft '
'''

from classbank import *
from misc import *
from component import *
import numpy as np

'''The axis are always in the order of X Y Z'''
'''X+ to the front of aircraft'''
'''Y+ to the right of the aircraft'''
'''Z+ to the down of the aircraft'''
'''Rotation follow right-hand rule'''

def SCfunc_UpdateAssembly(u_forces   = [[0],[0],[0]], #Assembles the ForcePoint update variables
                          u_moments  = [[0],[0],[0]],
                          u_mass     =  [0],
                          u_inertia  = [[0,0,0],
                                        [0,0,0],
                                        [0,0,0]],
                          u_position = [[0],[0],[0]],
                          u_rotation = [[0],[0],[0]]):
    variables = [u_forces, u_moments, u_mass, u_inertia, u_position, u_rotation]
    return variables

def SCcraft_Airligator():
    radius_rotor = 1.17 #radius of rotor
    radius_rotor_ring = 5 # radius of rotor position ring
    rotor_mass = 0
    rotor_inertia =[[0,0,0],
                    [0,0,0],
                    [0,0,0]]
    motor_mass = 22.3
    motor_inertia =[[0,0,0],
                    [0,0,0],
                    [0,0,0]]
    arm_mass = 0
    arm_inertia = [[0,0,0],
                   [0,0,0],
                   [0,0,0]]
    pax_mass = 0
    pax_inertia = [[0,0,0],
                   [0,0,0],
                   [0,0,0]]
    
    rotor_1 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi/3), 
                                            radius_rotor_ring * np.cos(np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
    
    rotor_2 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(2*np.pi/3), 
                                            radius_rotor_ring * np.cos(2*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    rotor_3 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi), 
                                            radius_rotor_ring * np.cos(np.pi),
                                            0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    rotor_4 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(4*np.pi/3), 
                                            radius_rotor_ring * np.cos(4*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    rotor_5 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(5*np.pi/3), 
                                            radius_rotor_ring * np.cos(5*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
        
    rotor_6 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(0), 
                                            radius_rotor_ring * np.cos(0),
                                            0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    motor_1 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi/3), 
                                            radius_rotor_ring * np.cos(np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
    
    motor_2 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(2*np.pi/3), 
                                            radius_rotor_ring * np.cos(2*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    motor_3 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi), 
                                            radius_rotor_ring * np.cos(np.pi),
                                            0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    motor_4 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(4*np.pi/3), 
                                            radius_rotor_ring * np.cos(4*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    motor_5 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(5*np.pi/3), 
                                            radius_rotor_ring * np.cos(5*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
        
    motor_6 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(0), 
                                            radius_rotor_ring * np.cos(0),
                                            0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    arm_1   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    arm_2   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    arm_3   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    arm_4   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    arm_5   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    arm_6   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    pax_1   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = pax_mass,       #[kg] 
                                inertia  = pax_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    pax_2   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = pax_mass,       #[kg] 
                                inertia  = pax_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    bat_1   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 0,       #[kg] 
                                inertia  = [[0,0,0],
                                            [0,0,0],
                                            [0,0,0]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    bat_2   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 0,       #[kg] 
                                inertia  = [[0,0,0],
                                            [0,0,0],
                                            [0,0,0]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    body_1  = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 0,       #[kg] 
                                inertia  = [[0,0,0],
                                            [0,0,0],
                                            [0,0,0]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    tank_1  = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 0,       #[kg] 
                                inertia  = [[0,0,0],
                                            [0,0,0],
                                            [0,0,0]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    '''Collect Points'''
    points = [rotor_1, rotor_2, rotor_3, rotor_4, rotor_5, rotor_6,
              motor_1, motor_2, motor_3, motor_4, motor_5, motor_6,
              arm_1, arm_2, arm_3, arm_4, arm_5, arm_6,
              pax_1, pax_2,
              bat_1, bat_2,
              body_1,
              tank_1]
    return points
     
def SCcraft_PointGenerationExample(): #Returns a list of points with ForcePoint class, modify this function to add or remove points from the aicraft
    '''Points'''
    example_point = SCobj_ForcePoint(forces   = [0,10,ExampleFunction(3)], #[N, WITHOUT gravitational froce]
                                     moments  = [0,0,0],   #[N*m]
                                     mass     =  10,       #[kg] 
                                     inertia  =[[0,0,0],   # [....]
                                                [0,0,0],
                                                [0,0,0]],
                                     position = [0,0,0],   # [m from the body axis origin ]
                                     rotation = [0,20,0],)  # euler angle degrees 
    
    example_point2 = SCobj_ForcePoint(forces  = [0,10,ExampleFunction(3)], #[N, WITHOUT gravitational froce]
                                     moments  = [0,0,0],   #[N*m]
                                     mass     =  10,       #[kg] 
                                     inertia  =[[0,0,0],   # [....]
                                                [0,0,0],
                                                [0,0,0]],
                                     position = [0,0,0],   # [m from the body axis origin ]
                                     rotation = [0,0,0],)  # euler angle degrees 

    '''Collect Points'''
    points = [example_point, example_point2]
    return points

def SCcraft_VerifyAircraft(): #Returns a list of points with ForcePoint class, modify this function to add or remove points from the aicraft
    '''Points'''
    rotor_1 = SCobj_ForcePoint(forces   = [0, 0, SCfunc_RotorThrust(1.2)], #[N, WITHOUT gravitational froce]
                                     moments  = [0, 0, SCfunc_RotorTorque(1.2, clockwise=True)],   #[N*m]
                                     mass     =  0,       #[kg] 
                                     inertia  =[[0,0,0],   # [....]
                                                [0,0,0],
                                                [0,0,0]],
                                     position = [1,1,0],   # [m from the body axis origin ]
                                     rotation = [10,0,0],)  # euler angle degrees 
    rotor_2 = SCobj_ForcePoint(forces   = [0, 0, SCfunc_RotorThrust(1.2)], #[N, WITHOUT gravitational froce]
                                     moments  = [0, 0, SCfunc_RotorTorque(1.2, clockwise=False)],   #[N*m]
                                     mass     =  0,       #[kg] 
                                     inertia  =[[0,0,0],   # [....]
                                                [0,0,0],
                                                [0,0,0]],
                                     position = [1,-1,0],   # [m from the body axis origin ]
                                     rotation = [-10,0,0],)  # euler angle degrees 
    rotor_3 = SCobj_ForcePoint(forces   = [0, 0, SCfunc_RotorThrust(1.2)], #[N, WITHOUT gravitational froce]
                                     moments  = [0, 0, SCfunc_RotorTorque(1.2, clockwise=True)],   #[N*m]
                                     mass     =  0,       #[kg] 
                                     inertia  =[[0,0,0],   # [....]
                                                [0,0,0],
                                                [0,0,0]],
                                     position = [-1,-1,0],   # [m from the body axis origin ]
                                     rotation = [-10,0,0],)  # euler angle degrees 
    rotor_4 = SCobj_ForcePoint(forces   = [0, 0, SCfunc_RotorThrust(1.2)], #[N, WITHOUT gravitational froce]
                                     moments  = [0, 0, SCfunc_RotorTorque(1.2, clockwise=False)],   #[N*m]
                                     mass     =  0,       #[kg] 
                                     inertia  =[[0,0,0],   # [....]
                                                [0,0,0],
                                                [0,0,0]],
                                     position = [-1,1,0],   # [m from the body axis origin ]
                                     rotation = [10,0,0],)  # euler angle degrees 
    body = SCobj_ForcePoint(forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                     moments  = [0, 0, 0],   #[N*m]
                                     mass     =  718,       #[kg] 
                                     inertia  =[[100,0,0],   # [....]
                                                [0,100,0],
                                                [0,0,100]],
                                     position = [0,0,0],   # [m from the body axis origin ]
                                     rotation = [0,0,0],)  # euler angle degrees 

    '''Collect Points'''
    points = [rotor_1, rotor_2, rotor_3, rotor_4, body]
    return points

def SCcraft_FastAircraft(): # Fast flying fixed-wing aircraft
    engine  = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 0,       #[kg] 
                                inertia  = [[0,0,0],
                                            [0,0,0],
                                            [0,0,0]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 

'''End'''

Testing = False
if Testing:
    aircraft = SCobj_Aircraft(points=SCcraft_VerifyAircraft(), position=[0,0,0], rotation=[0,0,0])
    # print(aircraft.forces)
    # print(aircraft.moments)
    print('---------Updating Points------------')
    rpm1 = 5
    rpm2 = 2
    rpm3 = 8
    rpm4 = 10
    updates = [SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm1]], u_moments=[[0],[0],[rpm1]]), 
            SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm1]], u_moments=[[0],[0],[rpm1]]),
            SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm1]], u_moments=[[0],[0],[rpm1]]), 
            SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm1]], u_moments=[[0],[0],[rpm1]]),
            SCfunc_UpdateAssembly()]
    aircraft.UpdatePoints(update_variables=updates)
    # print(aircraft.forces)
    print(aircraft.moments)
    print('---------Updating Points------------')
    updates = [SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm4]], u_moments=[[0],[0],[rpm4]]), 
            SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm4]], u_moments=[[0],[0],[rpm4]]),
            SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm2]], u_moments=[[0],[0],[rpm2]]), 
            SCfunc_UpdateAssembly(u_forces=[[0],[0],[rpm2]], u_moments=[[0],[0],[rpm2]]),
            SCfunc_UpdateAssembly()]
    aircraft.UpdatePoints(update_variables=updates)
    # print(aircraft.forces)
    print(aircraft.moments)