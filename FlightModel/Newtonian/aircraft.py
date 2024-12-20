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

def ExampleFunction(Constant): #the input modify the function that is to be returned
    return lambda variable: variable*Constant #Return a function that can be stored in a variable

def SCfunc_UpdateAssembly(u_forces   = [[0],[0],[0]],
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
    
aircraft = SCobj_Aircraft(points=SCfunc_PointGeneration(), position=[0,0,0], rotation=[0,0,0])
print(aircraft.forces)
print('---------Updating Points------------')
updates = [SCfunc_UpdateAssembly(u_forces=[[0],[0],[2]]), 
           SCfunc_UpdateAssembly(u_forces=[[0],[0],[5]])]
aircraft.UpdatePoints(update_variables=updates)
print(aircraft.forces)
print('---------Updating Points------------')
updates = [SCfunc_UpdateAssembly(u_forces=[[0],[0],[4]]), 
           SCfunc_UpdateAssembly(u_forces=[[0],[0],[8]])]
aircraft.UpdatePoints(update_variables=updates)
print(aircraft.forces)