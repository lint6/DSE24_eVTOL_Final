'''
Created by Lintong

Simulation Miscellaneous function file
DO define function
DO NOT define class
DO NOT script

Upstream
None

Downstream
All

'''

import numpy as np

def SCfunc_ForceVector(force_in):
    import numpy as np
    if type(force_in) == float or type(force_in) == int:
        raise ValueError('SCfunc_ForceVector: Non-vector force encountered')
    force_in = np.array(force_in)
    magnitude = np.linalg.norm(force_in)
    unit_vector = force_in/magnitude
    return magnitude, unit_vector

def SCfunc_EulerRotation(input_vector, rotation):
    import numpy as np
    # print(rotation)
    # Define Euler angles (in degrees)
    yaw   = rotation[2] # Rotation around Z-axis
    pitch = rotation[1] # Rotation around Y-axis
    roll  = rotation[0] # Rotation around X-axis

    # Convert angles to radians
    yaw = np.radians(yaw)
    pitch = np.radians(pitch)
    roll = np.radians(roll)

    # Rotation matrices
    Rz = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw),  np.cos(yaw), 0],
        [0,            0,           1]
    ])

    Ry = np.array([
        [np.cos(pitch),  0, np.sin(pitch)],
        [0,              1, 0           ],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])

    Rx = np.array([
        [1, 0,           0          ],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll),  np.cos(roll)]
    ])

    # Combine the rotation matrices based on the desired sequence
    # ZYX sequence (yaw, pitch, roll)
    rotation_matrix = Rz @ Ry @ Rx  
    # Transform the vector using the rotation matrix
    transformed_vector = rotation_matrix @ input_vector
    # To apply the inverse transformation
    inverse_rotation_matrix = np.linalg.inv(rotation_matrix)

    return transformed_vector, rotation_matrix, inverse_rotation_matrix

def SCfunc_CartesianToSpherical(vector_cartesian):
    r = np.sqrt(vector_cartesian[0]**2 + 
                vector_cartesian[1]**2 + 
                vector_cartesian[2]**2)
    theta = np.arctan2(vector_cartesian[1],vector_cartesian[0])
    phi = np.arctan2(np.sqrt(vector_cartesian[0]**2 + vector_cartesian[1]**2), vector_cartesian[2])
    vector_sp_rad = np.array([r,theta,-1*(phi-np.pi/2)])
    vector_sp_deg = np.array([r, np.rad2deg(theta), -1*(np.rad2deg(phi)-90)])
    return vector_sp_rad, vector_sp_deg

def SCfunc_LinearRamp(x1, x2, x, value1, value2):
    m = 1 / (x2 - x1)
    b = -1 * x1 / (x2 - x1)
    mix = np.clip(m*x+b, a_max=1, a_min=0)
    value = (1-mix)*value1 + (mix)*value2
    return value

def SCfunc_RPM2RadSec(RPM):
    return RPM/60 * 2 * np.pi

def SCfunc_RadSec2RPM(omega):
    return omega * 60 / (2*np.pi)

def SCfunc_CSV_reading(folder_path, file, velocity_input, alpha_input):

    import numpy as np
    import os
    import csv
    from scipy.interpolate import interp2d
    
    folder_path = folder_path
    file_name = file  # CSV filename
    cwd = os.getcwd()
    print("cwd:", cwd)
    file_path = os.path.join(cwd, folder_path, file_name)  # Full file path

    # Define alpha_v (angle of attack) and velocity ranges
    alpha_v_rad = np.linspace(-np.pi/2, np.pi/2, 100)  # 100 values from -90 to 90 degrees
    alpha_v_deg = alpha_v_rad * 180 / np.pi  # Convert radians to degrees
    velocities = np.linspace(0, 50, 100)  # 100 values from 0 to 50 m/s

    # Read CSV data into a NumPy array
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = np.array([list(map(float, row)) for row in reader])  # Convert to float array

    # Ensure the data has the correct shape (100x100)
    if data.shape != (100, 100):
        raise ValueError(f"Expected CSV shape (100,100), but got {data.shape}")

    # Create an interpolation function
    interp_func = interp2d(velocities, alpha_v_deg, data, kind='linear')

    # Interpolate the value at the given velocity and alpha
    interpolated_value = interp_func(velocity_input, alpha_input)[0]

    return interpolated_value

# Example Usage
velocity = 45  # Example velocity input
alpha = 30  # Example angle of attack input (degrees)
result = SCfunc_CSV_reading(r"FlightModel\Newtonian\CSV_rotor_data", r"C_T_interpolated_iter4.csv", velocity, alpha)
print("interpolated result is :", result) 

DEBUG = False
if DEBUG:
    # print(SCfunc_EulerRotation([1,0,0],[10,5,10])[0])
    # print(SCfunc_CartesianToSpherical([15,-5,1]))
    print(SCfunc_LinearRamp(x1=0, x2=5, x=-5, value1=0, value2=-5))