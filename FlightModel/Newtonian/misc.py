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

# def SCfunc_EulerRotation():
#     import numpy as np 
#     from scipy.spatial.transform import Rotation  as R 

#     print("in degrees")
#     delta_euler_angle = [input("yaw angle"), input("pitch angle"), input("roll angle") ]

#     rotation_sequence = "zyx"

#     rotation = R.from_euler(rotation_sequence, delta_euler_angle, degrees=True)

#     rotation_matrix = rotation.as_matrix()

#     print ("rotation matrix is", rotation_matrix)

#     # applying rotation to my vector 
#     local_vector = np.array([input("x"), input("y"), input("z")], dtype=float)
#     transformed_vector = rotation.apply(local_vector)
#     print("It was", local_vector, "but now in global axis its", transformed_vector)


#     #bring it back to normal 
#     inverse_rotation = rotation.inv()
#     inverse_transformed_vector = inverse_rotation.apply(transformed_vector)
#     print("Inverting the matrix back to local axis system", inverse_transformed_vector)
#     return transformed_vector

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

def SCfunc_Inertia_Disc(m,l):
    I_xx = 0
    I_yy = 0 
    I_zz = (1/12) * m * l**2 
    return I_xx, I_yy, I_zz

def SCfunc_Inertia_Cylinder(m, r, l): # z going through the circle surface, 
    I_xx = ((1/4) * m * r**2) + ((1/12) * m * l**2)
    I_yy = ((1/4) * m * r**2) + ((1/12) * m * l**2)
    I_zz = ((1/2) * m * r**2)
    return I_xx, I_yy, I_zz


def SCfunc_Intertia_Box(m, w, d, h): # w = width(y), d= depth(x), h = height(z)
    I_xx = ((1/12) * m * (w**2 + h**2))
    I_yy = ((1/12) * m * (h**2 + d**2))
    I_zz = ((1/12) * m * (w**2 + d**2))
    return I_xx, I_yy, I_zz

def SCfunc_Intertia_Sphere(m, r):
    I_xx = (2/5) * m * r**2
    I_yy = (2/5) * m * r**2
    I_zz = (2/5) * m * r**2
    return I_xx, I_yy, I_zz


DEBUG = False
if DEBUG:
    # print(SCfunc_EulerRotation([1,0,0],[10,5,10])[0])
    # print(SCfunc_CartesianToSpherical([15,-5,1]))
    print(SCfunc_LinearRamp(x1=0, x2=5, x=-5, value1=0, value2=-5))