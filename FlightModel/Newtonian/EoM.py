'''
Created by Lintong

Simulation verification file
DO define function
DO NOT define class
DO NOT script

Upstream
None

Downstream
All

'''
import numpy as np 
from scipy.integrate import cumtrapz
import matplotlib.pyplot as plt 


#TODO: Unit Tests
# - Vertical Movement w/ total delta_T
# - Rotation Movement w/ delta_T per rotor
# - Yaw Movement w/ delta_M
# - Side movement from 

#Defining "constant" variable for now 
rpm = 1 
mass = 500
g = 9.81 

Inertia_matrix =np.array([[100, 0, 0],
                          [0, 100, 0],
                          [0, 0, 100]])
#Angle in degrees 
phi = 10
theta = 0 
psi = 0

#Inertia in x,y,z
I_xx = 10
I_yy = 10 
I_zz = 10 

#forces from each rotor 
T_1 = 5 * rpm  
T_2 = 5 * rpm 
T_3 = 5 * rpm
T_4 = 5 * rpm 

torque_1 = 0.025 * rpm 
torque_2 = 0.025 * rpm 
torque_3 = 0.025 * rpm 
torque_4 = 0.025 * rpm 

# Generating emty matrix for storing y_d_d, z_d_d, and phi_d_d 

b_matrix = np.array([[-(1/mass) * np.sin(phi), 0],
                     [(1/mass) * np.cos(phi), 0],
                     [0, 1/I_xx]])

u_matrix = np.array([2,3])

planar_acceleration_1 = np.array([0, -g, 0])

planar_acceleration_2 = b_matrix.dot(u_matrix.T)

planar_acceleration = planar_acceleration_1 + planar_acceleration_2
print("the planar accelration terms are :", planar_acceleration)

# Example inputs
time = np.linspace(0, 1, 10)  # Time array (0 to 10 seconds, 100 points)
acceleration = planar_acceleration  # Constant acceleration [a_y, a_z, alpha_phi]

# Expand acceleration to match time steps
acceleration = np.tile(acceleration, (len(time), 1))

# Integrate acceleration to get velocity (initial velocity = 0)
velocity = cumtrapz(acceleration, time, initial=0, axis=0)

# Integrate velocity to get distance (initial position = 0)
distance = cumtrapz(velocity, time, initial=0, axis=0)

print("the planar velocity terms are :", velocity)
print("the planar distance terms are :", distance)


# Plotting acceleration, velocity, and distance for each term
terms = ['y-axis', 'z-axis', 'phi (angular)']
labels = ['Acceleration', 'Velocity', 'Distance']

fig, axes = plt.subplots(3, 3, figsize=(15, 10), sharex=True)
for i, term in enumerate(terms):
    # Acceleration
    axes[0, i].plot(time, acceleration[:, i], label=f'{labels[0]} in {term}')
    axes[0, i].set_title(f'{labels[0]} vs Time ({term})')
    axes[0, i].set_ylabel(labels[0])
    axes[0, i].grid()
    axes[0, i].legend()

    # Velocity
    axes[1, i].plot(time, velocity[:, i], label=f'{labels[1]} in {term}')
    axes[1, i].set_title(f'{labels[1]} vs Time ({term})')
    axes[1, i].set_ylabel(labels[1])
    axes[1, i].grid()
    axes[1, i].legend()

    # Distance
    axes[2, i].plot(time, distance[:, i], label=f'{labels[2]} in {term}')
    axes[2, i].set_title(f'{labels[2]} vs Time ({term})')
    axes[2, i].set_xlabel('Time (s)')
    axes[2, i].set_ylabel(labels[2])
    axes[2, i].grid()
    axes[2, i].legend()

plt.tight_layout()
plt.show()