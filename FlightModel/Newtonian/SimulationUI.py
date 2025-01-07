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
log_state, log_forces, log_time, log_extras, log_acc = SCfunc_FlightSimulation(aircraft, runtime=50)

fig, axs = plt.subplots(5)


axs[0].plot(log_time, -1*np.array(log_state[0]).T[2], label = 'Aircraft')
# axs[0].plot(log_time, log_extras[1], 'r', label = 'setpoint')
axs[0].set_ylabel('Height')

axs[1].plot(log_time, np.array(log_state[1]).T[1], label = 'Aircraft')
# axs[1].plot(log_time, log_extras[2], 'r', label = 'setpoint')
axs[1].set_ylabel('Pitch')

axs[2].plot(log_time, np.array(log_state[1]).T[0], label = 'Aircraft')
# axs[2].plot(log_time, log_extras[2], 'r', label = 'setpoint')
axs[2].set_ylabel('Roll')
print(log_extras[2])
axs[3].plot(log_time, np.array(log_extras[2]).T[1], label = 'Aircraft')
# axs[3].plot(log_time, log_extras[2], 'r', label = 'setpoint')
axs[3].set_ylabel('Setpoint Pitch')

axs[4].plot(log_time, np.array(np.array(log_extras[0]).T[0]), '--',label = 'FR Rotor')
axs[4].plot(log_time, np.array(np.array(log_extras[0]).T[1]), '--',label = 'FL Rotor')
axs[4].plot(log_time, np.array(np.array(log_extras[0]).T[2]), label = 'RL Rotor')
axs[4].plot(log_time, np.array(np.array(log_extras[0]).T[3]), label = 'RR Rotor')
axs[4].legend()
axs[4].set_ylabel('RPM (normalized)')

axs[4].set_xlabel('time')

plt.show()
plt.clf

plt.plot(log_time, log_acc[0][0])
plt.plot(log_time, log_acc[0][1])
plt.plot(log_time, log_acc[0][2])
plt.show()
