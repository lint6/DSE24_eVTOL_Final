'''
Created by Lintong

Controllers file
DO define function
DO NOT define class
DO NOT script

Upstream
None

Downstream
physics.py

'''

import numpy as np

def SCfunc_PIDController(error, k_p, t_i, t_d, dt): #Standard PID controller
    p_error = error[-1]
    i_error = np.sum(error) * dt
    d_error = (error[-1]-error[-2])/dt
    output = -k_p * (p_error + i_error/t_i + d_error*t_d)
    return output

def SCfunc_PController(error, k_p): #Standard P controller
    output = -k_p * error
    return output