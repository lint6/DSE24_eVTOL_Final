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
    example_point = SCobj_ForcePoint(forces   = [0,0,ExampleFunction(50)],
                                     moments  = [0,0,0],
                                     mass     =  10,
                                     inertia  =[[0,0,0],
                                                [0,0,0],
                                                [0,0,0]],
                                     position = [0,0,0],
                                     rotation = [0,0,0],)
    print(example_point.forces_func)
    '''Collect Points'''
    points = [example_point]
    return points
    
    5
aircraft = SCobj_Aircraft(points=SCfunc_PointGeneration(), position=[0,0,0], rotation=[0,0,0])
print(aircraft.forces)
print('---------Updating Points------------')
aircraft.UpdatePoints(update_variables=SCfunc_UpdateAssembly(u_forces=[[0],[0],[2]]))
print(aircraft.forces)