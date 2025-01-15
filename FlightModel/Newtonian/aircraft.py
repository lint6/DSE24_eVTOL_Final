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

'''The axis are always in the order of X Y Z'''
'''X+ to the front of aircraft'''
'''Y+ to the right of the aircraft'''
'''Z+ to the down of the aircraft'''
'''Rotation follow right-hand rule'''

def ExampleFunction(Constant): #the input modify the function that is to be returned
    return lambda variable: variable*Constant #Return a function that can be stored in a variable

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

def SCfunc_PointGeneration(): #Returns a list of points with ForcePoint class, modify this function to add or remove points from the aicraft
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

'''Verification Functions''' #functions used for verification of the simulation model
'''Start'''
def SCfunc_VerifyThrust(R): #Mimic single input (RPM) function for thrust
    #TODO Finish up Ct calculation
    area = np.pi * R**2
    rho = 1.225
    return lambda state, rpm: area*rho*(SCfunc_RPM2RadSec(rpm)*R)**2*-0.0087

def SCfunc_VerifyTorque(R, clockwise): #Mimic single input (RPM) function for torque
    #TODO Finish up Cq calculation
    area = np.pi * R**2
    rho = 1.225
    if clockwise:
        return lambda state, rpm: area*rho*(SCfunc_RPM2RadSec(rpm)*R)**2*0.0001*R
    else:
        return lambda state, rpm: area*rho*(SCfunc_RPM2RadSec(rpm)*R)**2*0.0001*R*-1

def SCfunc_VerifyAircraft(): #Returns a list of points with ForcePoint class, modify this function to add or remove points from the aicraft
    '''Points'''
    rotor_1 = SCobj_ForcePoint(forces   = [0, 0, SCfunc_VerifyThrust(1.2)], #[N, WITHOUT gravitational froce]
                                     moments  = [0, 0, SCfunc_VerifyTorque(1.2, clockwise=True)],   #[N*m]
                                     mass     =  0,       #[kg] 
                                     inertia  =[[0,0,0],   # [....]
                                                [0,0,0],
                                                [0,0,0]],
                                     position = [1,1,0],   # [m from the body axis origin ]
                                     rotation = [10,0,0],)  # euler angle degrees 
    rotor_2 = SCobj_ForcePoint(forces   = [0, 0, SCfunc_VerifyThrust(1.2)], #[N, WITHOUT gravitational froce]
                                     moments  = [0, 0, SCfunc_VerifyTorque(1.2, clockwise=False)],   #[N*m]
                                     mass     =  0,       #[kg] 
                                     inertia  =[[0,0,0],   # [....]
                                                [0,0,0],
                                                [0,0,0]],
                                     position = [1,-1,0],   # [m from the body axis origin ]
                                     rotation = [-10,0,0],)  # euler angle degrees 
    rotor_3 = SCobj_ForcePoint(forces   = [0, 0, SCfunc_VerifyThrust(1.2)], #[N, WITHOUT gravitational froce]
                                     moments  = [0, 0, SCfunc_VerifyTorque(1.2, clockwise=True)],   #[N*m]
                                     mass     =  0,       #[kg] 
                                     inertia  =[[0,0,0],   # [....]
                                                [0,0,0],
                                                [0,0,0]],
                                     position = [-1,-1,0],   # [m from the body axis origin ]
                                     rotation = [-10,0,0],)  # euler angle degrees 
    rotor_4 = SCobj_ForcePoint(forces   = [0, 0, SCfunc_VerifyThrust(1.2)], #[N, WITHOUT gravitational froce]
                                     moments  = [0, 0, SCfunc_VerifyTorque(1.2, clockwise=False)],   #[N*m]
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
'''End'''

Testing = False
if Testing:
    aircraft = SCobj_Aircraft(points=SCfunc_VerifyAircraft(), position=[0,0,0], rotation=[0,0,0])
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