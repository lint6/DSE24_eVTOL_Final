'''
Created by Lintong

Aircraft file
DO define function
DO NOT define class
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


def SCfunc_CreateAircraft():
    '''Points'''
    example_point = SCobj_ForcePoint(forces=ExampleFunction(1),
                                     moments=[0,0,0],
                                     mass=0,
                                     inertia=[[0,0,0],[0,0,0],[0,0,0]],
                                     position = [0,0,0],
                                     rotation = [0,0,0],
                                     toggle=[0,0,0,0,0,0])
    
    '''Aircraft'''
    aircraft = SCobj_Aircraft()