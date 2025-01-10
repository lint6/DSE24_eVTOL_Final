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
6
import numpy as np
from aircraft import *
from physics import *
import matplotlib.pyplot as plt

aircraft = SCobj_Aircraft(points=SCfunc_VerifyAircraft(), position=[0,0,0], rotation=[0,0,0])
log_state, log_forces, log_time, log_extras, log_acc, log_error, log_setpoints = SCfunc_FlightSimulation(aircraft, runtime=1*60)

fig_pos, pos_plt = plt.subplots(4)
pos_plt[0].title.set_text('Position')
pos_plt[0].plot(log_time, np.array(log_state[0]).T[0], label = 'Aircraft')
pos_plt[0].plot(log_time, np.array(log_setpoints[0]).T[0], 'r', label = 'setpoint')
pos_plt[0].legend()
pos_plt[0].set_ylabel('X')

pos_plt[1].plot(log_time, np.array(log_state[0]).T[1], label = 'Aircraft')
pos_plt[1].plot(log_time, np.array(log_setpoints[0]).T[1], 'r', label = 'setpoint')
pos_plt[1].set_ylabel('Y')

pos_plt[2].plot(log_time, -1*np.array(log_state[0]).T[2], label = 'Aircraft')
pos_plt[2].plot(log_time, -1*np.array(log_setpoints[0]).T[2], 'r', label = 'setpoint')
pos_plt[2].set_ylabel('Z')

pos_plt[3].plot(log_time, np.array(np.array(log_extras[0]).T[0]), '--',label = 'FR Rotor')
pos_plt[3].plot(log_time, np.array(np.array(log_extras[0]).T[1]), '--',label = 'FL Rotor')
pos_plt[3].plot(log_time, np.array(np.array(log_extras[0]).T[2]), label = 'RL Rotor')
pos_plt[3].plot(log_time, np.array(np.array(log_extras[0]).T[3]), label = 'RR Rotor')
pos_plt[3].legend()
pos_plt[3].set_ylabel('RPM (normalized)')
pos_plt[3].set_xlabel('time')

fig_ang, ang_plt = plt.subplots(4)
ang_plt[0].title.set_text('Rotation')
ang_plt[0].plot(log_time, np.array(log_state[1]).T[0], label = 'Aircraft')
ang_plt[0].plot(log_time, np.array(log_setpoints[1]).T[0], 'r', label = 'setpoint')
ang_plt[0].legend()
ang_plt[0].set_ylabel('X (Roll)')

ang_plt[1].plot(log_time, np.array(log_state[1]).T[1], label = 'Aircraft')
ang_plt[1].plot(log_time, np.array(log_setpoints[1]).T[1], 'r', label = 'setpoint')
ang_plt[1].set_ylabel('Y (Pitch)')

ang_plt[2].plot(log_time, np.array(log_state[1]).T[2], label = 'Aircraft')
ang_plt[2].plot(log_time, np.array(log_setpoints[1]).T[2], 'r', label = 'setpoint')
ang_plt[2].set_ylabel('Z (Yaw)')

ang_plt[3].plot(log_time, np.array(np.array(log_extras[3]).T[0]), '--',label = 'Hover')
ang_plt[3].plot(log_time, np.array(np.array(log_extras[3]).T[1]), '--',label = 'Roll')
ang_plt[3].plot(log_time, np.array(np.array(log_extras[3]).T[2]), label = 'Pitch')
ang_plt[3].plot(log_time, np.array(np.array(log_extras[3]).T[3]), label = 'Yaw')
ang_plt[3].legend()
ang_plt[3].set_ylabel('Throttle (Avg)')
ang_plt[3].set_xlabel('time')

# plt.tight_layout()
plt.show()
plt.clf()

fltpath = plt.figure(figsize=(12,10))
path = fltpath.add_subplot( projection='3d')
path.plot(np.array(log_state[0]).T[0],
          np.array(log_state[0]).T[1],
          -1*np.array(log_state[0]).T[2],
          label = 'Aircraft')
path.plot(np.array(log_setpoints[0]).T[0],
          np.array(log_setpoints[0]).T[1],
          -1*np.array(log_setpoints[0]).T[2],
          label = 'Setpoint',)
        #   marker = '^')



path.set_xlabel('X')
path.set_ylabel('Y')
path.set_zlabel('Z')
path.set_aspect('equal')
path.legend()
fltpath.show()

input()