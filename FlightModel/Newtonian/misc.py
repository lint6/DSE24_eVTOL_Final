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
    if type(force_in) == float or type(force_in) == int:
        raise ValueError('SCfunc_ForceVector: Non-vector force encountered')
    force_in = np.array(force_in)
    magnitude = np.linalg.norm(force_in)
    