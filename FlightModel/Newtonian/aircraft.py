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
from physics import *


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
    radius_rotor = 1.22 #radius of rotor
    radius_rotor_ring = 2.93 # radius of rotor position ring
    rotor_mass = 81.47/6
    rotor_inertia =[[SCphy_Inertia_Disc(23.32, 1.22)[0],0,0],
                    [0,SCphy_Inertia_Disc(23.32, 1.22)[1],0],
                    [0,0,SCphy_Inertia_Disc(23.32, 1.22)[2]]]
    
    motor_mass = 82.68/6
    motor_inertia =[[SCphy_Inertia_Cylinder(26.314,0.114, 0.086 )[0],0,0],
                    [0,SCphy_Inertia_Cylinder(26.314,0.114, 0.086 )[1],0],
                    [0,0,SCphy_Inertia_Cylinder(26.314,0.114, 0.086 )[2]]]
    
    arm_mass = 38.729/6
    arm_inertia = [[SCphy_Inertia_Rod(38.729/6, 2.93)[0],0,0],
                   [0,SCphy_Inertia_Rod(38.729/6, 2.93)[1],0],
                   [0,0,SCphy_Inertia_Rod(38.729/6, 2.93)[2]]]
    
    pax_mass = 185/2
    pax_inertia = [[SCphy_Intertia_Sphere(185/2, 0.6)[0],0,0],
                   [0,SCphy_Intertia_Sphere(185/2, 0.6)[1],0],
                   [0,0,SCphy_Intertia_Sphere(185/2, 0.6)[2]]]
    
    rotor_1 = SCobj_ForcePoint( forces   = [SCfunc_RotorDrag(radius_rotor, X=True), SCfunc_RotorDrag(radius_rotor), SCfunc_RotorThrust(radius_rotor)], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, SCfunc_RotorTorque(radius_rotor, clockwise=True)],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(1*np.pi/3), 
                                            radius_rotor_ring * np.cos(1*np.pi/3),
                                            -1.6],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    rotor_2 = SCobj_ForcePoint( forces   = [SCfunc_RotorDrag(radius_rotor, X=True), SCfunc_RotorDrag(radius_rotor), SCfunc_RotorThrust(radius_rotor)], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, SCfunc_RotorTorque(radius_rotor, clockwise=False)],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(2*np.pi/3), 
                                            radius_rotor_ring * np.cos(2*np.pi/3),
                                            -1.6],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
    
    rotor_3 = SCobj_ForcePoint( forces   = [SCfunc_RotorDrag(radius_rotor, X=True), SCfunc_RotorDrag(radius_rotor), SCfunc_RotorThrust(radius_rotor)], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, SCfunc_RotorTorque(radius_rotor, clockwise=True)],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi), 
                                            radius_rotor_ring * np.cos(np.pi),
                                            -1.6],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
    
    rotor_4 = SCobj_ForcePoint( forces   = [SCfunc_RotorDrag(radius_rotor, X=True), SCfunc_RotorDrag(radius_rotor), SCfunc_RotorThrust(radius_rotor)], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, SCfunc_RotorTorque(radius_rotor, clockwise=True)],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(4*np.pi/3), 
                                            radius_rotor_ring * np.cos(4*np.pi/3),
                                            -1.6],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
    
    rotor_5 = SCobj_ForcePoint( forces   = [SCfunc_RotorDrag(radius_rotor, X=True), SCfunc_RotorDrag(radius_rotor), SCfunc_RotorThrust(radius_rotor)], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, SCfunc_RotorTorque(radius_rotor, clockwise=False)],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(5*np.pi/3), 
                                            radius_rotor_ring * np.cos(5*np.pi/3),
                                            -1.6],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
        
    rotor_6 = SCobj_ForcePoint( forces   = [SCfunc_RotorDrag(radius_rotor, X=True), SCfunc_RotorDrag(radius_rotor), SCfunc_RotorThrust(radius_rotor)], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, SCfunc_RotorTorque(radius_rotor, clockwise=False)],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(0), 
                                            radius_rotor_ring * np.cos(0),
                                            -1.6],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    motor_1 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi/3), 
                                            radius_rotor_ring * np.cos(np.pi/3),
                                            -1.2],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
    
    motor_2 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(2*np.pi/3),
                                            radius_rotor_ring * np.cos(2*np.pi/3),
                                            -1.2],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    motor_3 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi), 
                                            radius_rotor_ring * np.cos(np.pi),
                                            -1.2],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    motor_4 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(4*np.pi/3), 
                                            radius_rotor_ring * np.cos(4*np.pi/3),
                                            -1.2],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    motor_5 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(5*np.pi/3), 
                                            radius_rotor_ring * np.cos(5*np.pi/3),
                                            -1.2],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
        
    motor_6 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(0), 
                                            radius_rotor_ring * np.cos(0),
                                            -1.2],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    arm_1   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi/3)/2,
                                            radius_rotor_ring * np.cos(np.pi/3)/2,
                                            -0.6],   # [m from the body axis origin ]
                                rotation = [0,-17.6126,30],)  # euler angle degrees 
    arm_2   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [radius_rotor_ring * np.sin(2*np.pi/3)/2,
                                            radius_rotor_ring * np.cos(2*np.pi/3)/2,
                                            -0.6],   # [m from the body axis origin ]
                                rotation = [0,-17.6126,-30],)  # euler angle degrees 
    arm_3   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi)/2,
                                            radius_rotor_ring * np.cos(np.pi)/2,
                                            -0.6],   # [m from the body axis origin ]
                                rotation = [0,-17.6126,-90],)  # euler angle degrees 
    arm_4   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [radius_rotor_ring * np.sin(4*np.pi/3)/2,
                                            radius_rotor_ring * np.cos(4*np.pi/3)/2,
                                            -0.6],   # [m from the body axis origin ]
                                rotation = [0,-17.6126,-150],)  # euler angle degrees 
    arm_5   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [radius_rotor_ring * np.sin(5*np.pi/3)/2,
                                            radius_rotor_ring * np.cos(5*np.pi/3)/2,
                                            -0.6],   # [m from the body axis origin ]
                                rotation = [0,-17.6126,150],)  # euler angle degrees 
    arm_6   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [radius_rotor_ring * np.sin(6*np.pi/3)/2,
                                            radius_rotor_ring * np.cos(6*np.pi/3)/2,
                                            -0.6],   # [m from the body axis origin ]
                                rotation = [0,-17.6126,90],)  # euler angle degrees 
    pax_1   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = pax_mass,       #[kg] 
                                inertia  = pax_inertia,
                                position = [1.6,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    pax_2   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = pax_mass,       #[kg] 
                                inertia  = pax_inertia,
                                position = [1.6,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    bat_1   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 103.72,       #[kg] 
                                inertia  = [[SCphy_Intertia_Box(103.72, 66, 60, 13.8)[0],0,0],
                                            [0,SCphy_Intertia_Box(103.72, 66, 60, 13.8)[1],0],
                                            [0,0,SCphy_Intertia_Box(103.72, 66, 60, 13.8)[2]]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    bat_2   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 21,       #[kg] 
                                inertia  = [[SCphy_Intertia_Box(21, 14.7, 26.5, 20)[0],0,0],
                                            [0,SCphy_Intertia_Box(21, 14.7, 26.5, 20)[1],0],
                                            [0,0,SCphy_Intertia_Box(21, 14.7, 26.5, 20)[2]]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    PEMFC   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 35.67,       #[kg] 
                                inertia  = [[SCphy_Intertia_Box(35.67, 0.5923, 0.8133, 0.6204)[0],0,0],
                                            [0,SCphy_Intertia_Box(35.67, 0.5923, 0.8133, 0.6204)[1],0],
                                            [0,0,SCphy_Intertia_Box(35.67, 0.5923, 0.8133, 0.6204)[2]]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    body    = SCobj_ForcePoint( forces   = [SCfunc_bodydrag(), 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 74.108,       #[kg] 
                                inertia  = [[SCphy_Intertia_Sphere(74.108 + 74.108/0.113, 1.7/2)[0]-SCphy_Intertia_Sphere(74.108/0.113, (1.7/2) - 0.03)[0],0,0],
                                            [0,SCphy_Intertia_Sphere(74.108 + 74.108/0.113, 1.7/2)[1]-SCphy_Intertia_Sphere(74.108/0.113, (1.7/2) - 0.03)[1],0],
                                            [0,0,SCphy_Intertia_Sphere(74.108 + 74.108/0.113, 1.7/2)[2]-SCphy_Intertia_Sphere(74.108/0.113, (1.7/2) - 0.03)[2]]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    tank  = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 89.32,       #[kg] 
                                inertia  = [[SCphy_Inertia_Cylinder(89.32 + 89.32/0.113, 0.4611/2, 1.1841)[0]-SCphy_Inertia_Cylinder(89.32/0.113, 0.4611/2, 1.1841)[0],0,0],
                                            [0,SCphy_Inertia_Cylinder(89.32 + 89.32/0.113, 0.4611/2, 1.1841)[1]-SCphy_Inertia_Cylinder(89.32/0.113, 0.4611/2, 1.1841)[1],0],
                                            [0,0,SCphy_Inertia_Cylinder(89.32 + 89.32/0.113, 0.4611/2, 1.1841)[2]-SCphy_Inertia_Cylinder(89.32/0.113, 0.4611/2, 1.1841)[2]]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    flight_control   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce] [furninshing + extra on sheet]
                                   moments  = [0, 0, 0],   #[N*m]
                                   mass     = 43.63,       #[kg] 
                                   inertia  = [[0,0,0],
                                               [0,0,0],
                                               [0,0,0]],
                                   position = [1.5,0,0],   # [m from the body axis origin ]
                                   rotation = [0,0,0],)
    
    Electrical_system = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                   moments  = [0, 0, 0],   #[N*m]
                                   mass     = 24.89,       #[kg] 
                                   inertia  = [[0,0,0],
                                               [0,0,0],
                                               [0,0,0]],
                                   position = [0,0,0],   # [m from the body axis origin ]
                                   rotation = [0,0,0],)
    
    HTC = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                   moments  = [0, 0, 0],   #[N*m]
                                   mass     = 12.56,       #[kg] 
                                   inertia  = [[SCphy_Intertia_Box(12.56, np.sqrt(0.98), np.sqrt(0.98), 0.035)[0],0,0],
                                               [0,SCphy_Intertia_Box(12.56, np.sqrt(0.98), np.sqrt(0.98), 0.035)[1],0],
                                               [0,0,SCphy_Intertia_Box(12.56, np.sqrt(0.98), np.sqrt(0.98), 0.035)[2]]],
                                   position = [0,0,0],   # [m from the body axis origin ]
                                   rotation = [0,0,0],)
    
    Ballast = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                   moments  = [0, 0, 0],   #[N*m]
                                   mass     = 845.49-792.78,       #[kg] 
                                   inertia  = [[SCphy_Intertia_Box(12.56, np.sqrt(0.98), np.sqrt(0.98), 0.035)[0],0,0],
                                               [0,SCphy_Intertia_Box(12.56, np.sqrt(0.98), np.sqrt(0.98), 0.035)[1],0],
                                               [0,0,SCphy_Intertia_Box(12.56, np.sqrt(0.98), np.sqrt(0.98), 0.035)[2]]],
                                   position = [0,0,0],   # [m from the body axis origin ]
                                   rotation = [0,0,0],)

    '''Collect Points'''
    points = [rotor_1, rotor_2, rotor_3, rotor_4, rotor_5, rotor_6,
              motor_1, motor_2, motor_3, motor_4, motor_5, motor_6,
              arm_1, arm_2, arm_3, arm_4, arm_5, arm_6,
              pax_1, pax_2,
              bat_1, bat_2,
              body,
              tank,
              PEMFC,
              HTC,
              Electrical_system, flight_control,
              Ballast]
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
    aircraft = SCobj_Aircraft(points=SCcraft_Airligator(), position=[0,0,0], rotation=[0,0,0])
    print(aircraft.mass)
    print("Number of collected points are:", len(aircraft.points))

