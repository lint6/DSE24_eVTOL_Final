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

DEBUG = False
if DEBUG:
    print(SCfunc_EulerRotation([1,0,0],[10,5,10])[0])