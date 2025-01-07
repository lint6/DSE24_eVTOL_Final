'''
Created by Lintong

Simulation UI file
DO NOT define function
DO NOT define class
DO script

Upstream
aircraft.py

Downstream
None
'''

import numpy as np
from aircraft import *
from physics import *
import matplotlib.pyplot as plt

aircraft = SCobj_Aircraft(points=SCfunc_VerifyAircraft(), position=[0,0,0], rotation=[0,0,0])
log_state, log_forces, log_time, log_extras = SCfunc_FlightSimulation(aircraft)

plt.plot(log_time, -1*np.array(log_state[0]).T[2])
plt.plot(log_time, log_extras[1], 'r')
plt.xlabel('time')
plt.ylabel('Height')
plt.show()
plt.clf()
plt.plot(log_time, log_extras[0])
plt.show()