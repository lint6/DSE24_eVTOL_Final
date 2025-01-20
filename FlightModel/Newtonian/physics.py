'''
NOT ACTAULLY USED

Created by Lintong

Simulation Model file
DO define function
DO define class
DO NOT script

Upstream
misc.py
class.py

Downstream
component.py
aircraft.py

'Functions that handle the bulk of physical relations'
'''
import numpy as np
from misc import *

def SCphy_Inertia_Disc(m,l):
    I_xx = 0
    I_yy = 0 
    I_zz = (1/2) * m * l**2 
    return I_xx, I_yy, I_zz

def SCphy_Inertia_Cylinder(m, r, l): # z going through the circle surface, 
    I_xx = ((1/4) * m * r**2) + ((1/12) * m * l**2)
    I_yy = ((1/4) * m * r**2) + ((1/12) * m * l**2)
    I_zz = ((1/2) * m * r**2)
    return I_xx, I_yy, I_zz


def SCphy_Intertia_Box(m, w, d, h): # w = width(y), d= depth(x), h = height(z)
    I_xx = ((1/12) * m * (w**2 + h**2))
    I_yy = ((1/12) * m * (h**2 + d**2))
    I_zz = ((1/12) * m * (w**2 + d**2))
    return I_xx, I_yy, I_zz

def SCphy_Intertia_Sphere(m, r):
    I_xx = (2/5) * m * r**2
    I_yy = (2/5) * m * r**2
    I_zz = (2/5) * m * r**2
    return I_xx, I_yy, I_zz

def SCphy_Inertia_Rod(m, l):
    I_xx = 0
    I_yy = 0 
    I_zz = (1/12) * m * l**2 
    return I_xx, I_yy, I_zz

def SCphy_ThrustCoef(state):
    if state:
        velocity = state[-1][0]
        alpha = state[-1][2]
    else:
        velocity = 0
        alpha = 0
    return SCfunc_CSV_reading(r"FlightModel\Newtonian\CSV_rotor_data", r"C_T_interpolated_iter4.csv", velocity, alpha)

def SCphy_TorqueCoef(state):
    if state:
        velocity = state[-1][0]
        alpha = state[-1][2]
    else:
        velocity = 0
        alpha = 0
    return SCfunc_CSV_reading(r"FlightModel\Newtonian\CSV_rotor_data", r"C_Q_interpolated_iter4.csv" , velocity, alpha)

def SCphy_XCoef(state):
    if state:
        velocity = state[-1][0]
        alpha = state[-1][2]
    else:
        velocity = 0
        alpha = 0
    return SCfunc_CSV_reading(r"FlightModel\Newtonian\CSV_rotor_data", r"C_X_interpolated_iter4.csv" , velocity, alpha)


def SCphy_Thrust(state, rpm, R, rho=1.225):
    CT = SCphy_ThrustCoef(state)
    area = np.pi * R**2
    tip_spd = SCfunc_RPM2RadSec(rpm)*R
    return CT * rho * area * tip_spd**2

def SCphy_Rotor_Drag(state, rpm, R, rho=1.225):
    CX = SCphy_XCoef(state)
    area = np.pi * R**2
    tip_spd = SCfunc_RPM2RadSec(rpm)*R
    Drag = CX * rho * area * tip_spd**2
    if state:
        beta = state[-1][1]
    else:
        beta = 0
    return Drag * np.cos(beta), Drag * np.sin(beta)


def SCphy_Torque(state, rpm, R, rho=1.225):
    CT = SCphy_TorqueCoef(state)
    area = np.pi * R**2
    tip_spd = SCfunc_RPM2RadSec(rpm)*R
    return CT * rho * area * tip_spd**2 * R