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
from simulation import *
import matplotlib.pyplot as plt

aircraft = SCobj_Aircraft(points=SCcraft_Airligator(), position=[0,0,0], rotation=[0,0,0])
log_state, log_forces, log_time, log_extras, log_acc, log_setpoints, log_control = SCfunc_FlightSimulation(aircraft, runtime=60)


fig_pos, pos_plt = plt.subplots(4)
pos_plt[0].title.set_text('Position')
pos_plt[0].plot(log_time, np.array(log_state[0]).T[0], label = 'Aircraft')
pos_plt[0].plot(log_time, np.array(log_setpoints[0]).T[0], 'r', label = 'setpoint')
pos_plt[0].legend()
pos_plt[0].set_ylabel('X (m)')

pos_plt[1].plot(log_time, np.array(log_state[0]).T[1], label = 'Aircraft')
pos_plt[1].plot(log_time, np.array(log_setpoints[0]).T[1], 'r', label = 'setpoint')
pos_plt[1].set_ylabel('Y (m)')

pos_plt[2].plot(log_time, -1*np.array(log_state[0]).T[2], label = 'Aircraft')
pos_plt[2].plot(log_time, -1*np.array(log_setpoints[0]).T[2], 'r', label = 'setpoint')
pos_plt[2].legend()
pos_plt[2].set_ylabel('Z (m)')

pos_plt[3].plot(log_time, np.array(np.array(log_control[0]).T[0]), label = 'Rotor1')
pos_plt[3].plot(log_time, np.array(np.array(log_control[0]).T[1]), label = 'Rotor2')
pos_plt[3].plot(log_time, np.array(np.array(log_control[0]).T[2]), '--', label = 'Rotor3')
pos_plt[3].plot(log_time, np.array(np.array(log_control[0]).T[3]), '-.', label = 'Rotor4')
pos_plt[3].plot(log_time, np.array(np.array(log_control[0]).T[4]), '-.', label = 'Rotor5')
pos_plt[3].plot(log_time, np.array(np.array(log_control[0]).T[5]), '--', label = 'Rotor6')
pos_plt[3].legend()
pos_plt[3].set_ylabel('RPM')
pos_plt[3].set_xlabel('time (s)')

fig_ang, ang_plt = plt.subplots(4)
ang_plt[0].title.set_text('Rotation')
ang_plt[0].plot(log_time, np.array(log_state[1]).T[0], label = 'Aircraft')
ang_plt[0].plot(log_time, np.array(log_setpoints[1]).T[0], 'r', label = 'setpoint')
ang_plt[0].legend()
ang_plt[0].set_ylabel('Roll (deg)')

ang_plt[1].plot(log_time, np.array(log_state[1]).T[1], label = 'Aircraft')
ang_plt[1].plot(log_time, np.array(log_setpoints[1]).T[1], 'r', label = 'setpoint')
ang_plt[1].set_ylabel('Pitch (deg)')

ang_plt[2].plot(log_time, np.array(log_state[1]).T[2], label = 'Aircraft')
ang_plt[2].plot(log_time, np.array(log_setpoints[1]).T[2], 'r', label = 'setpoint')
ang_plt[2].set_ylabel('Yaw (deg)')

ang_plt[3].plot(log_time, np.array(np.array(log_extras[4]).T[0]), label = 'Hover')
ang_plt[3].plot(log_time, np.array(np.array(log_extras[4]).T[1]), label = 'Forward')
ang_plt[3].legend()
ang_plt[3].set_ylabel('Flight mode divide')
ang_plt[3].set_xlabel('Time (s)')

fig_vel, vel_plt = plt.subplots(3)
vel_plt[0].title.set_text('Velocity')
vel_plt[0].plot(log_time, np.array(log_state[2]).T[0], label = 'Aircraft')
# ang_plt[0].plot(log_time, np.array(log_setpoints[1]).T[0], 'r', label = 'setpoint')
vel_plt[0].legend()
vel_plt[0].set_ylabel('X_dot')

vel_plt[1].plot(log_time, np.array(log_state[2]).T[1], label = 'Aircraft')
# ang_plt[1].plot(log_time, np.array(log_setpoints[1]).T[1], 'r', label = 'setpoint')
vel_plt[1].set_ylabel('Y_dot')

vel_plt[2].plot(log_time, -1*np.array(log_state[2]).T[2], label = 'Aircraft')
ang_plt[2].plot(log_time, np.array(log_setpoints[1]).T[2], 'r', label = 'setpoint')
vel_plt[2].set_ylabel('Z_dot')
vel_plt[2].set_xlabel('time')

fig_rot, rot_plt = plt.subplots(3)
rot_plt[0].title.set_text('Rotation rate')
rot_plt[0].plot(log_time, np.array(log_state[3]).T[0], label = 'Aircraft')
# ang_plt[0].plot(log_time, np.array(log_setpoints[1]).T[0], 'r', label = 'setpoint')
rot_plt[0].legend()
rot_plt[0].set_ylabel('X_rot')

rot_plt[1].plot(log_time, np.array(log_state[3]).T[1], label = 'Aircraft')
# ang_plt[1].plot(log_time, np.array(log_setpoints[1]).T[1], 'r', label = 'setpoint')
rot_plt[1].set_ylabel('Y_rot')

rot_plt[2].plot(log_time, np.array(log_state[3]).T[2], label = 'Aircraft')
# ang_plt[2].plot(log_time, np.array(log_setpoints[1]).T[2], 'r', label = 'setpoint')
rot_plt[2].set_ylabel('Z_rot')
rot_plt[2].set_xlabel('time')

# fltpath = plt.figure(figsize=(12,10))
# path = fltpath.add_subplot( projection='3d')
# path.plot(np.array(log_state[0]).T[0],
#           np.array(log_state[0]).T[1],
#           -1*np.array(log_state[0]).T[2],
#           label = 'Aircraft')
# path.plot(np.array(log_setpoints[0]).T[0],
#           np.array(log_setpoints[0]).T[1],
#           -1*np.array(log_setpoints[0]).T[2],
#           label = 'Setpoint',
#           marker = '^',
#           )
# path.set_xlabel('X')
# path.set_ylabel('Y')
# path.set_zlabel('Z')
# path.set_aspect('equal')
# path.legend()

plt.show()

input()