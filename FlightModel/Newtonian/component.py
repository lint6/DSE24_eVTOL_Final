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

def ExampleFunction(Constant): #the input modify the function that is to be returned
    return lambda variable: variable*Constant #Return a function that can be stored in a variable

'''Verification Functions''' #functions used for verification of the simulation model
def SCfunc_RotorThrust(R): #Mimic single input (RPM) function for thrust
    #TODO Finish up Ct calculation
    area = np.pi * R**2
    rho = 1.225
    return lambda state, rpm: area*rho*(SCfunc_RPM2RadSec(rpm)*R)**2*-0.0087

def SCfunc_RotorTorque(R, clockwise): #Mimic single input (RPM) function for torque
    #TODO Finish up Cq calculation
    area = np.pi * R**2
    rho = 1.225
    if clockwise:
        return lambda state, rpm: area*rho*(SCfunc_RPM2RadSec(rpm)*R)**2*0.0001*R
    else:
        return lambda state, rpm: area*rho*(SCfunc_RPM2RadSec(rpm)*R)**2*0.0001*R*-1
    