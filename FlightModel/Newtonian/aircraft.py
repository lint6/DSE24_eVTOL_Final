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


def SCfunc_PointGeneration():
    '''Points'''
    example_point = SCobj_ForcePoint(forces=[0,0,ExampleFunction(50)],
                                     moments=[0,0,0],
                                     mass=0,
                                     inertia=[[0,0,0],
                                              [0,0,0],
                                              [0,0,0]],
                                     position = [0,0,0],
                                     rotation = [0,0,0],)
    
    '''Aircraft'''
    points = [example_point]
    return points
    
    
aircraft = SCobj_Aircraft(points=SCfunc_PointGeneration(), position=[0,0,0], rotation=[0,0,0])
print(aircraft.points[0].forces)
aircraft.UpdatePoints(update_variables=[[[0],[0],[20]]])
print(aircraft.points[0].forces)