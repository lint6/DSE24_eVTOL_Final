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

def SCfunc_CreateAircraft():
    '''Points'''
    example_point = SCobj_ForcePoint(force=[],
                                     )