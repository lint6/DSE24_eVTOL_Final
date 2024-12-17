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

def SCfunc_EulerRotation():
    import numpy as np 
    from scipy.spatial.transform import Rotation  as R 

    print("in degrees")
    delta_euler_angle = [input("yaw angle"), input("pitch angle"), input("roll angle") ]

    rotation_sequence = "zyx"

    rotation = R.from_euler(rotation_sequence, delta_euler_angle, degrees=True)

    rotation_matrix = rotation.as_matrix()

    print ("rotation matrix is", rotation_matrix)

    # applying rotation to my vector 
    local_vector = np.array([input("x"), input("y"), input("z")], dtype=float)
    transformed_vector = rotation.apply(local_vector)
    print("It was", local_vector, "but now in global axis its", transformed_vector)

    #bring it back to normal 
    inverse_rotation = rotation.inv()
    inverse_transformed_vector = inverse_rotation.apply(transformed_vector)
    print("Inverting the matrix back to local axis system", inverse_transformed_vector)

print (SCfunc_EulerRotation())

