'''
Created by Lintong

Component file
DO define function
DO NOT define class
DO NOT script

Upstream
N/A

Downstream
aircraft.py

'Functions that convert physical paremeters that needs to be updated mid flight'
'''
import numpy as np
from misc import *
from physics import *

def ExampleFunction(Constant): #the input modify the function that is to be returned
    return lambda variable: variable*Constant #Return a function that can be stored in a variable

'''Verification Functions''' #functions used for verification of the simulation model
def SCfunc_RotorThrust(R): #Mimic single input (RPM) function for thrust
    return lambda state, control: SCphy_Thrust(state, control, R) * (-1)

def SCfunc_RotorTorque(R, clockwise): #Mimic single input (RPM) function for torque
    if clockwise:
        return lambda state, control: SCphy_Torque(state, control, R)
    else:
        return lambda state, control: SCphy_Torque(state, control, R) * -1
    
def SCfunc_RotorDrag(R, X=False): #Mimic single input (RPM) function for thrust
    if X:
        return lambda state, control: SCphy_Rotor_Drag(state, control, R)[0]*(-1)
    else:
        return lambda state, control: SCphy_Rotor_Drag(state, control, R)[1]*(-1)

def SCfunc_bodydrag(): #Mimic single input (RPM) function for thrust
    return lambda state : SCphy_body_drag(state) * (-1)

